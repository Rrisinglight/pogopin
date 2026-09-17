"""Test doubles for the AD7705 driver. FakeSpi emulates the communications-register protocol."""
import time

from pogoscan.ad7705 import (REG_COMM, REG_SETUP, REG_CLOCK, REG_DATA, REG_TEST, REG_OFFSET, REG_GAIN, REG_SIZES)

POWER_ON = {REG_SETUP: 0x01, REG_CLOCK: 0x05, REG_DATA: 0x8000, REG_TEST: 0x00, REG_OFFSET: 0x1F4000, REG_GAIN: 0x5761AB}


class FakeSpi:
    def __init__(self, miso_open: bool = False, cal_seconds: float = 0.0):
        self.miso_open = miso_open          # True: every read returns zeros (open DOUT wire)
        self.cal_seconds = cal_seconds      # MD bits stay 01 this long after a calibration command (Table 21: 6/rate)
        self.cal_started = None             # monotonic time of the last calibration command
        self.log: list[list[int]] = []      # every xfer2 payload
        self.data_queue: list[int] = []     # codes returned by successive data-register reads
        self.data_reads = 0
        self.resets = 0
        self.selfcals = 0
        self._ones = 0                      # consecutive 1 bits seen on DIN
        self._pending = None                # (reg, read, size, collected_bytes)
        self.regs = dict(POWER_ON)

    def _reset_state(self):
        self.regs = dict(POWER_ON); self._pending = None; self._ones = 0; self.resets += 1

    def xfer2(self, data):
        self.log.append(list(data))
        out = []
        for b in data:
            # Like the real interface, 32 consecutive ones on DIN reset it from *any* state
            # (a 4 x 0xFF burst must not be parsed as "read gain register" + 3 data bytes).
            self._ones = self._ones + 8 if b == 0xFF else 0
            if self._ones >= 32:
                self._reset_state(); out.append(0); continue
            if self._pending is None:
                reg, read = (b >> 4) & 7, bool(b & 8)
                if reg not in REG_SIZES:
                    out.append(0); continue
                self._pending = (reg, read, REG_SIZES[reg], [])
                out.append(0)
                continue
            reg, read, size, got = self._pending
            if read:
                value = self._read_value(reg)
                got.append(b)
                idx = len(got) - 1
                out.append(0 if self.miso_open else (value >> (8 * (size - 1 - idx))) & 0xFF)
            else:
                got.append(b); out.append(0)
            if len(got) == size:
                if not read:
                    value = 0
                    for x in got:
                        value = (value << 8) | x
                    self._write_value(reg, value)
                self._pending = None
        return out

    def _read_value(self, reg):
        if reg == REG_DATA:
            if len(self._pending[3]) == 0:      # first byte of a data read: pop the next code
                self.data_reads += 1
                self.regs[REG_DATA] = self.data_queue.pop(0) if self.data_queue else 0x8000
            return self.regs[REG_DATA]
        if reg == REG_COMM:
            return 0x00
        if reg == REG_SETUP and self.calibrating():
            return self.regs[reg] | 0x40    # MD = 01 until the calibration sequence has finished
        return self.regs[reg]

    def _write_value(self, reg, value):
        if reg == REG_SETUP and (value >> 6) != 0:   # a calibration: the chip clears MD bits when done
            self.selfcals += 1
            self.cal_started = time.monotonic()
            value &= 0x3F
        self.regs[reg] = value

    def calibrating(self) -> bool:
        return self.cal_started is not None and time.monotonic() - self.cal_started < self.cal_seconds


class FakeDrdy:
    """DRDY line (is_active == True means LOW, i.e. data ready).

    Without `spi` it is a constant level.  Linked to a FakeSpi it follows the chip through a calibration
    command the way the datasheet describes ("Calibration" section and Table 21): it keeps showing the
    stale LOW of the unread previous word for `stale_s` after the command (up to one modulator cycle,
    128/MCLK <= 128 us, on silicon), goes HIGH while the calibration runs and returns LOW once the first
    valid post-calibration word is ready, 1.5 x cal_seconds after the command (DRDY 9/rate vs MD 6/rate).
    """

    def __init__(self, active: bool = True, spi: "FakeSpi | None" = None, stale_s: float = 100e-6):
        self.active, self.spi, self.stale_s = active, spi, stale_s

    @property
    def is_active(self) -> bool:
        if self.spi is None or self.spi.cal_started is None:
            return self.active
        t = time.monotonic() - self.spi.cal_started
        if t < self.stale_s:
            return True                     # DRDY still low: the command has not been acted on yet
        return t >= 1.5 * self.spi.cal_seconds


class FakeReset:
    def __init__(self):
        self.calls: list[str] = []

    def on(self):
        self.calls.append("on")

    def off(self):
        self.calls.append("off")
