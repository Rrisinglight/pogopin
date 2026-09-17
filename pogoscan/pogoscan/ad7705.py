"""AD7705/AD7706 (and TM7705 clone) driver: register encoding, SPI driver, simulator."""
from __future__ import annotations

import random
import time

REG_COMM, REG_SETUP, REG_CLOCK, REG_DATA, REG_TEST, REG_OFFSET, REG_GAIN = 0, 1, 2, 3, 4, 6, 7
REG_SIZES = {REG_COMM: 1, REG_SETUP: 1, REG_CLOCK: 1, REG_DATA: 2, REG_TEST: 1, REG_OFFSET: 3, REG_GAIN: 3}
MODE_NORMAL, MODE_SELF_CAL, MODE_ZS_CAL, MODE_FS_CAL = 0, 1, 2, 3
GAIN_CODES = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7}
_RATES_CLK1 = {50: 0, 60: 1, 250: 2, 500: 3}   # effective master clock 2.4576 MHz
_RATES_CLK0 = {20: 0, 25: 1, 100: 2, 200: 3}   # effective master clock 1 MHz


class AD7705Error(Exception):
    """Communication or configuration failure."""


class AD7705Timeout(AD7705Error):
    """DRDY did not assert in time."""


def comm_byte(reg: int, read: bool, channel: int = 0, standby: bool = False) -> int:
    """Communications register byte: 0/DRDY | RS2 RS1 RS0 | R/W | STBY | CH1 CH0."""
    return ((reg & 7) << 4) | ((1 if read else 0) << 3) | ((1 if standby else 0) << 2) | (channel & 3)


def setup_byte(mode: int, gain: int, bipolar: bool = True, buffered: bool = False, fsync: bool = False) -> int:
    """Setup register byte: MD1 MD0 | G2 G1 G0 | B/U (0 = bipolar) | BUF | FSYNC."""
    return ((mode & 3) << 6) | (GAIN_CODES[gain] << 3) | ((0 if bipolar else 1) << 2) | ((1 if buffered else 0) << 1) | (1 if fsync else 0)


def clock_byte(crystal_hz: float, rate_hz: int, clkdis: bool = False) -> int:
    """Clock register byte: 0 0 0 | CLKDIS | CLKDIV | CLK | FS1 FS0."""
    if abs(crystal_hz - 4.9152e6) < 1e4:
        clkdiv, clk = 1, 1
    elif abs(crystal_hz - 2.4576e6) < 1e4:
        clkdiv, clk = 0, 1
    elif abs(crystal_hz - 2e6) < 1e4:
        clkdiv, clk = 1, 0
    elif abs(crystal_hz - 1e6) < 1e4:
        clkdiv, clk = 0, 0
    else:
        raise ValueError(f"unsupported crystal frequency {crystal_hz} Hz")
    table = _RATES_CLK1 if clk else _RATES_CLK0
    if rate_hz not in table:
        raise ValueError(f"rate {rate_hz} Hz not available with a {crystal_hz} Hz crystal; choose one of {sorted(table)}")
    return ((1 if clkdis else 0) << 4) | (clkdiv << 3) | (clk << 2) | table[rate_hz]


def code_to_volts(code: int, vref: float = 2.5, gain: int = 128, bipolar: bool = True) -> float:
    """Convert a 16-bit output code to input volts (offset binary in bipolar mode)."""
    if bipolar:
        return (code - 32768) / 32768 * vref / gain
    return code / 65536 * vref / gain


class AD7705:
    """SPI driver. Pass fakes for spi/drdy/reset in tests; on the Pi they default to spidev + gpiozero."""

    simulated = False

    def __init__(self, spi=None, drdy=None, reset=None, *, bus=0, device=0, drdy_pin=25, reset_pin=24,
                 crystal_hz=4.9152e6, vref=2.5, spi_hz=500_000):
        if spi is None:
            import spidev  # lazy: not installed on the dev box
            spi = spidev.SpiDev()
            spi.open(bus, device)
            spi.max_speed_hz = spi_hz
            spi.mode = 3
        self._owns_gpio = False
        if drdy is None:
            from gpiozero import DigitalInputDevice
            drdy = DigitalInputDevice(drdy_pin, pull_up=None, active_state=False)
            self._owns_gpio = True
        if reset is None and reset_pin is not None:
            from gpiozero import DigitalOutputDevice
            reset = DigitalOutputDevice(reset_pin, initial_value=True)
            self._owns_gpio = True
        self._spi, self._drdy, self._reset = spi, drdy, reset
        self.crystal_hz, self.vref = crystal_hz, vref
        self.channel, self.gain, self.rate, self.bipolar, self.buffered = 0, 128, 50, True, False

    # --- low level -------------------------------------------------------
    def reset(self) -> None:
        if self._reset is not None:
            self._reset.off(); time.sleep(0.001); self._reset.on(); time.sleep(0.010)
        self._spi.xfer2([0xFF] * 4)          # 32 ones: interface back to "expect a comm byte"
        time.sleep(0.010)

    def write_register(self, reg: int, value: int, nbytes: int = 1, channel: int | None = None) -> None:
        ch = self.channel if channel is None else channel
        payload = [(value >> (8 * (nbytes - 1 - i))) & 0xFF for i in range(nbytes)]
        self._spi.xfer2([comm_byte(reg, False, ch)] + payload)

    def read_register(self, reg: int, nbytes: int = 1, channel: int | None = None) -> int:
        ch = self.channel if channel is None else channel
        resp = self._spi.xfer2([comm_byte(reg, True, ch)] + [0] * nbytes)
        value = 0
        for b in resp[1:]:
            value = (value << 8) | (b & 0xFF)
        return value

    # --- configuration ---------------------------------------------------
    def configure(self, *, rate: int = 50, gain: int = 128, bipolar: bool = True, buffered: bool = False, channel: int = 0) -> None:
        self.rate, self.gain, self.bipolar, self.buffered, self.channel = rate, gain, bipolar, buffered, channel
        cb = clock_byte(self.crystal_hz, rate)
        self.write_register(REG_CLOCK, cb)
        self._verify(REG_CLOCK, cb, "clock")
        sb = setup_byte(MODE_NORMAL, gain, bipolar, buffered)
        self.write_register(REG_SETUP, sb)
        self._verify(REG_SETUP, sb, "setup")

    def _verify(self, reg: int, expected: int, name: str) -> None:
        got = self.read_register(reg)
        if got != expected:
            hint = " (all zeros: the DOUT to MISO line is probably open)" if got == 0 else ""
            raise AD7705Error(f"{name} register read-back mismatch: wrote 0x{expected:02X}, read 0x{got:02X}{hint}")

    def self_calibrate(self, timeout: float = 2.0) -> float:
        t0 = time.monotonic()
        self.write_register(REG_SETUP, setup_byte(MODE_SELF_CAL, self.gain, self.bipolar, self.buffered))
        # Datasheet, "Calibration": if DRDY is low when the command is written (it normally is here, the
        # previous word is never read) it can take up to one modulator cycle (128/MCLK, <= 128 us) before it
        # goes high, so DRDY must be ignored for that cycle.  Polling straight away would catch the stale
        # low, and the setup register would still read MD = 01 (6/rate, Table 21).
        time.sleep(0.001)
        self.wait_drdy(timeout)                  # goes low again after 9/rate + tP with the first valid word
        got = self.read_register(REG_SETUP)
        if (got >> 6) != MODE_NORMAL:
            raise AD7705Error(f"self-calibration did not complete: setup register 0x{got:02X}")
        return time.monotonic() - t0

    # --- conversions -----------------------------------------------------
    def wait_drdy(self, timeout: float = 1.0) -> None:
        deadline = time.monotonic() + timeout
        while not self._drdy.is_active:
            if time.monotonic() > deadline:
                raise AD7705Timeout(f"DRDY did not go low within {timeout} s")
            time.sleep(0.0002)

    def read_code(self, timeout: float = 1.0) -> int:
        self.wait_drdy(timeout)
        return self.read_register(REG_DATA, 2)

    def read_codes(self, n: int, timeout: float = 1.0) -> list[int]:
        return [self.read_code(timeout) for _ in range(n)]

    @property
    def lsb_volts(self) -> float:
        return self.vref / self.gain / (32768 if self.bipolar else 65536)

    def volts(self, code: int) -> float:
        return code_to_volts(code, self.vref, self.gain, self.bipolar)

    def microvolts(self, code: int) -> float:
        return self.volts(code) * 1e6

    # --- recovery ----------------------------------------------------------
    def expected_registers(self) -> dict[int, int]:
        """Clock and setup bytes the chip must hold for the current settings (normal mode)."""
        return {REG_CLOCK: clock_byte(self.crystal_hz, self.rate),
                REG_SETUP: setup_byte(MODE_NORMAL, self.gain, self.bipolar, self.buffered)}

    def is_configured(self) -> bool:
        """False when the chip is back at power-on defaults (0x05 / 0x01): its supply blinked or RESET was pulsed."""
        return all(self.read_register(reg) == value for reg, value in self.expected_registers().items())

    def initialize(self) -> float:
        """Reset, re-apply the current settings and self-calibrate; returns the calibration time in seconds."""
        self.reset()
        self.configure(rate=self.rate, gain=self.gain, bipolar=self.bipolar, buffered=self.buffered, channel=self.channel)
        return self.self_calibrate()

    def read_status(self) -> dict:
        """Two register reads (a few ms, no effect on conversions): {"clock", "setup", "configured"}."""
        expected = self.expected_registers()
        clock, setup = self.read_register(REG_CLOCK), self.read_register(REG_SETUP)
        return {"clock": clock, "setup": setup, "configured": clock == expected[REG_CLOCK] and setup == expected[REG_SETUP]}

    def close(self) -> None:
        for dev in (self._spi, self._drdy, self._reset):
            close = getattr(dev, "close", None)
            if close:
                close()
        if self._owns_gpio:
            # gpiozero's lgpio backend keeps a notify thread; closing only the devices leaves it to die at
            # interpreter shutdown, which aborts Python 3.13 on the Pi 5 ("could not acquire lock for stderr").
            try:
                from gpiozero import Device
                if Device.pin_factory is not None:
                    Device.pin_factory.close()
            except Exception:  # noqa: BLE001 - best effort at shutdown
                pass


class SimulatedAD7705:
    """Drop-in stand-in for AD7705: Gaussian noise (0.6 µV rms at gain 128 per datasheet Table 5) plus slow drift."""

    simulated = True

    def __init__(self, *, rate: int = 50, gain: int = 128, vref: float = 2.5, noise_uv: float = 0.6, seed: int = 0, realtime: bool = False):
        self.rate, self.gain, self.vref, self.noise_uv, self.realtime = rate, gain, vref, noise_uv, realtime
        self.bipolar, self.buffered, self.channel, self.crystal_hz = True, False, 0, 4.9152e6
        self.source_volts = 0.0
        self.drift_uv_per_s = 0.02
        self.calibrations = 0
        self._rng = random.Random(seed)
        self._drift_uv = 0.0

    def reset(self) -> None:
        self._drift_uv = 0.0

    def configure(self, *, rate: int = 50, gain: int = 128, bipolar: bool = True, buffered: bool = False, channel: int = 0) -> None:
        self.rate, self.gain, self.bipolar, self.buffered, self.channel = rate, gain, bipolar, buffered, channel

    def self_calibrate(self, timeout: float = 2.0) -> float:
        self.calibrations += 1
        self._drift_uv = 0.0
        return 0.06

    def wait_drdy(self, timeout: float = 1.0) -> None:
        if self.realtime:
            time.sleep(1.0 / self.rate)

    def read_code(self, timeout: float = 1.0) -> int:
        self.wait_drdy(timeout)
        self._drift_uv += self._rng.gauss(0.0, self.drift_uv_per_s / self.rate)
        volts = self.source_volts + (self._drift_uv + self._rng.gauss(0.0, self.noise_uv)) * 1e-6
        code = round(volts / self.lsb_volts) + (32768 if self.bipolar else 0)
        return max(0, min(65535, code))

    def read_codes(self, n: int, timeout: float = 1.0) -> list[int]:
        return [self.read_code(timeout) for _ in range(n)]

    @property
    def lsb_volts(self) -> float:
        return self.vref / self.gain / (32768 if self.bipolar else 65536)

    def volts(self, code: int) -> float:
        return code_to_volts(code, self.vref, self.gain, self.bipolar)

    def microvolts(self, code: int) -> float:
        return self.volts(code) * 1e6

    def is_configured(self) -> bool:
        return True

    def initialize(self) -> float:
        self.reset()
        return self.self_calibrate()

    def read_status(self) -> dict:
        return {"clock": None, "setup": None, "configured": True}

    def close(self) -> None:
        pass
