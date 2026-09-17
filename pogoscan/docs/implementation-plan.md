# pogoscan Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A Raspberry Pi 5 tool that reads an AD7705/TM7705 module over SPI0, records one averaged measurement per click on a 21×21 grid through a vanilla-JS web page, and renders and exports the heatmap.

**Architecture:** A small Python package `pogoscan` (driver → measurement → scan state → stdlib HTTP server) with a simulator twin of the ADC so everything is testable without hardware; a single static HTML/JS/CSS page talks to the JSON API. Every measured point is written to disk atomically.

**Tech Stack:** Python 3.13 standard library (`http.server`, `json`, `statistics`, `threading`, `dataclasses`), `spidev` 3.6 and `gpiozero` 2.0.1 on the Pi (lazy imports), pytest 8 on the dev box, vanilla JS + `<canvas>`.

**Spec:** `docs/superpowers/specs/2026-09-17-pogoscan-design.md` — every signature and JSON shape below is copied from it; read §5 of the spec before starting any task.

## Global Constraints

- Python ≥ 3.11, standard library only, plus `spidev`/`gpiozero` imported **lazily inside `AD7705.__init__`** (never at module import time); no numpy, no Flask, no React, no CDN resources in the page.
- Project root: `/home/projects/pogopin/pogoscan/` (already contains `pogoscan/__init__.py`, `tests/__init__.py`, `pytest.ini`, `.gitignore`, `README.md`). Run tests from that root with `python3 -m pytest`.
- Do **not** run `git init`/commit (the workspace has no repository and the user has not asked for one); the "Commit" steps below are replaced by "Run the full test suite".
- Hardware constants: crystal 4.9152 MHz → `clock_byte` gives 0x0C for 50 Hz; SPI mode 3, 500 kHz; DRDY GPIO25 active low; RESET GPIO24 active low; gain 128, bipolar, unbuffered, Vref 2.5 V → LSB 0.5960 µV.
- API and file formats: exactly spec §5.3 and §5.4. The page uses only those endpoints.
- Every file must stay small and single-purpose; keep functions pure where the spec lists them as pure.

---

## File map

| File | Responsibility | Task |
|---|---|---|
| `pogoscan/ad7705.py` | register encoding, `AD7705`, `SimulatedAD7705`, exceptions | 1, 2, 3 |
| `tests/fakes.py` | `FakeSpi`, `FakeDrdy`, `FakeReset` | 2 |
| `tests/test_ad7705.py` | driver tests | 1, 2, 3 |
| `pogoscan/measure.py`, `tests/test_measure.py` | `trimmed_mean`, `PointResult`, `measure_point` | 4 |
| `pogoscan/scan.py`, `tests/test_scan.py` | `ScanConfig`, `Scan`, `new_scan`, `list_scans`, `open_scan` | 5 |
| `pogoscan/server.py`, `tests/test_server.py` | HTTP API, static files, simulation plate | 6 |
| `pogoscan/check.py`, `tests/test_check.py` | hardware self-test CLI | 7 |
| `pogoscan/static/index.html`, `app.js`, `style.css`, `tests/test_static.py` | web page | 8 |
| `deploy.sh`, `README.md` | deployment and usage | 9 |

Dependency order: 1 → 2 → 3 → 4 → 5 → 6 → 7; 8 depends only on the API contract (can run in parallel with 2–7); 9 last.

---

### Task 1: Register encoding and code conversion (pure functions)

**Files:**
- Create: `pogoscan/ad7705.py`
- Test: `tests/test_ad7705.py`

**Interfaces:**
- Produces: `REG_*`, `MODE_*`, `GAIN_CODES`, `comm_byte`, `setup_byte`, `clock_byte`, `code_to_volts` (spec §5.1). Used by Tasks 2, 3, 7.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_ad7705.py
import pytest
from pogoscan.ad7705 import (REG_COMM, REG_SETUP, REG_CLOCK, REG_DATA, MODE_NORMAL, MODE_SELF_CAL,
                             comm_byte, setup_byte, clock_byte, code_to_volts)

def test_comm_byte_matches_datasheet_examples():
    assert comm_byte(REG_CLOCK, read=False) == 0x20
    assert comm_byte(REG_CLOCK, read=True) == 0x28
    assert comm_byte(REG_SETUP, read=False) == 0x10
    assert comm_byte(REG_SETUP, read=True) == 0x18
    assert comm_byte(REG_DATA, read=True) == 0x38
    assert comm_byte(REG_COMM, read=True) == 0x08
    assert comm_byte(REG_SETUP, read=False, channel=1) == 0x11
    assert comm_byte(REG_COMM, read=False, standby=True) == 0x04

def test_setup_byte_bit_layout():
    assert setup_byte(MODE_SELF_CAL, 128) == 0x78          # MD=01 G=111 B/U=0 (bipolar) BUF=0 FSYNC=0
    assert setup_byte(MODE_NORMAL, 128) == 0x38
    assert setup_byte(MODE_NORMAL, 1, bipolar=False, buffered=True, fsync=True) == 0x07
    with pytest.raises(KeyError):
        setup_byte(MODE_NORMAL, 3)

def test_clock_byte_for_each_crystal():
    assert clock_byte(4.9152e6, 50) == 0x0C     # CLKDIV=1 CLK=1 FS=00
    assert clock_byte(4.9152e6, 500) == 0x0F
    assert clock_byte(2.4576e6, 60) == 0x05     # power-on default value
    assert clock_byte(1e6, 20) == 0x00
    assert clock_byte(2e6, 25) == 0x09          # CLKDIV=1 CLK=0 FS=01
    assert clock_byte(4.9152e6, 50, clkdis=True) == 0x1C
    with pytest.raises(ValueError):
        clock_byte(4.9152e6, 20)                # 20 Hz needs a 1 MHz effective clock
    with pytest.raises(ValueError):
        clock_byte(3e6, 50)

def test_code_to_volts():
    assert code_to_volts(32768) == 0.0
    assert code_to_volts(0) == pytest.approx(-2.5 / 128)
    assert code_to_volts(65535) == pytest.approx(2.5 / 128 * 32767 / 32768)
    assert code_to_volts(32768, bipolar=False) == pytest.approx(2.5 / 128 / 2)
    assert code_to_volts(32768 + 1) - code_to_volts(32768) == pytest.approx(0.596e-6, rel=1e-3)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd /home/projects/pogopin/pogoscan && python3 -m pytest tests/test_ad7705.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'pogoscan.ad7705'`

- [ ] **Step 3: Write the minimal implementation**

```python
# pogoscan/ad7705.py
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_ad7705.py -v`
Expected: 4 passed

- [ ] **Step 5: Run the full suite**

Run: `python3 -m pytest`
Expected: all passed

---

### Task 2: `AD7705` driver class with fakes

**Files:**
- Modify: `pogoscan/ad7705.py` (append the class)
- Create: `tests/fakes.py`
- Test: `tests/test_ad7705.py` (append)

**Interfaces:**
- Consumes: Task 1 functions.
- Produces: `class AD7705` with `reset()`, `write_register(reg, value, nbytes=1, channel=None)`, `read_register(reg, nbytes=1, channel=None) -> int`, `configure(*, rate=50, gain=128, bipolar=True, buffered=False, channel=0)`, `self_calibrate(timeout=2.0) -> float`, `wait_drdy(timeout=1.0)`, `read_code(timeout=1.0) -> int`, `read_codes(n, timeout=1.0) -> list[int]`, `lsb_volts` property, `volts(code)`, `microvolts(code)`, `close()`, attributes `channel, gain, rate, bipolar, buffered, vref, crystal_hz, simulated=False`. Fakes `FakeSpi(miso_open=False)`, `FakeDrdy(active=True)`, `FakeReset()` used by Tasks 4, 7.

- [ ] **Step 1: Write the fakes**

```python
# tests/fakes.py
"""Test doubles for the AD7705 driver. FakeSpi emulates the communications-register protocol."""
from pogoscan.ad7705 import (REG_COMM, REG_SETUP, REG_CLOCK, REG_DATA, REG_TEST, REG_OFFSET, REG_GAIN, REG_SIZES)

POWER_ON = {REG_SETUP: 0x01, REG_CLOCK: 0x05, REG_DATA: 0x8000, REG_TEST: 0x00, REG_OFFSET: 0x1F4000, REG_GAIN: 0x5761AB}


class FakeSpi:
    def __init__(self, miso_open: bool = False):
        self.miso_open = miso_open          # True: every read returns zeros (open DOUT wire)
        self.log: list[list[int]] = []      # every xfer2 payload
        self.data_queue: list[int] = []     # codes returned by successive data-register reads
        self.data_reads = 0
        self.resets = 0
        self.selfcals = 0
        self._ones = 0
        self._pending = None                # (reg, read, size, collected_bytes)
        self.regs = dict(POWER_ON)

    def _reset_state(self):
        self.regs = dict(POWER_ON); self._pending = None; self._ones = 0; self.resets += 1

    def xfer2(self, data):
        self.log.append(list(data))
        out = []
        for b in data:
            if self._pending is None:
                self._ones = self._ones + 8 if b == 0xFF else 0
                if self._ones >= 32:
                    self._reset_state(); out.append(0); continue
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
        return self.regs[reg]

    def _write_value(self, reg, value):
        if reg == REG_SETUP and (value >> 6) != 0:   # a calibration: the chip clears MD bits when done
            self.selfcals += 1
            value &= 0x3F
        self.regs[reg] = value


class FakeDrdy:
    def __init__(self, active: bool = True):
        self.is_active = active


class FakeReset:
    def __init__(self):
        self.calls: list[str] = []

    def on(self):
        self.calls.append("on")

    def off(self):
        self.calls.append("off")
```

- [ ] **Step 2: Write the failing tests**

```python
# tests/test_ad7705.py (append)
from pogoscan.ad7705 import AD7705, AD7705Error, AD7705Timeout
from tests.fakes import FakeSpi, FakeDrdy, FakeReset


def make_adc(spi=None, drdy=None, reset=None):
    return AD7705(spi=spi or FakeSpi(), drdy=drdy or FakeDrdy(True), reset=reset if reset is not None else FakeReset(), crystal_hz=4.9152e6)


def test_reset_pulses_pin_and_sends_32_ones():
    spi, rst = FakeSpi(), FakeReset()
    adc = make_adc(spi, reset=rst)
    adc.reset()
    assert rst.calls == ["off", "on"]
    assert spi.log[-1] == [0xFF, 0xFF, 0xFF, 0xFF]
    assert spi.resets == 1


def test_write_and_read_register_use_comm_protocol():
    spi = FakeSpi(); adc = make_adc(spi)
    adc.write_register(2, 0x0C)                      # clock register
    assert spi.log[-1] == [0x20, 0x0C]
    assert adc.read_register(2) == 0x0C
    assert spi.log[-1] == [0x28, 0x00]
    adc.write_register(6, 0x123456, nbytes=3)        # offset register, 24 bits
    assert spi.log[-1] == [0x60, 0x12, 0x34, 0x56]
    assert adc.read_register(6, nbytes=3) == 0x123456


def test_configure_writes_clock_then_setup_and_verifies():
    spi = FakeSpi(); adc = make_adc(spi)
    adc.configure(rate=50, gain=128)
    assert spi.regs[2] == 0x0C and spi.regs[1] == 0x38
    assert (adc.rate, adc.gain, adc.bipolar, adc.buffered, adc.channel) == (50, 128, True, False, 0)


def test_configure_reports_open_miso_line():
    adc = make_adc(FakeSpi(miso_open=True))
    with pytest.raises(AD7705Error) as e:
        adc.configure()
    assert "0x00" in str(e.value) and "MISO" in str(e.value)


def test_self_calibrate_waits_for_drdy_and_checks_mode_bits():
    spi = FakeSpi(); adc = make_adc(spi)
    adc.configure()
    seconds = adc.self_calibrate(timeout=0.5)
    assert spi.selfcals == 1 and spi.regs[1] == 0x38 and 0 <= seconds < 0.5


def test_wait_drdy_times_out():
    adc = make_adc(drdy=FakeDrdy(False))
    with pytest.raises(AD7705Timeout):
        adc.wait_drdy(timeout=0.02)


def test_read_codes_pops_data_in_order_and_converts():
    spi = FakeSpi(); spi.data_queue = [32768, 32769, 32767]
    adc = make_adc(spi); adc.configure()
    codes = adc.read_codes(3)
    assert codes == [32768, 32769, 32767] and spi.data_reads == 3
    assert adc.microvolts(32769) == pytest.approx(0.596, rel=1e-3)
    assert adc.lsb_volts == pytest.approx(2.5 / 128 / 32768)
    assert adc.simulated is False
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_ad7705.py -v`
Expected: the 7 new tests FAIL with `ImportError: cannot import name 'AD7705'`

- [ ] **Step 4: Write the driver class**

```python
# pogoscan/ad7705.py (append)
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
        if drdy is None:
            from gpiozero import DigitalInputDevice
            drdy = DigitalInputDevice(drdy_pin, pull_up=None, active_state=False)
        if reset is None and reset_pin is not None:
            from gpiozero import DigitalOutputDevice
            reset = DigitalOutputDevice(reset_pin, initial_value=True)
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
        self.wait_drdy(timeout)
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

    def close(self) -> None:
        for dev in (self._spi, self._drdy, self._reset):
            close = getattr(dev, "close", None)
            if close:
                close()
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_ad7705.py -v`
Expected: 11 passed

- [ ] **Step 6: Run the full suite**

Run: `python3 -m pytest` — Expected: all passed

---

### Task 3: `SimulatedAD7705`

**Files:**
- Modify: `pogoscan/ad7705.py` (append)
- Test: `tests/test_ad7705.py` (append)

**Interfaces:**
- Produces: `SimulatedAD7705(*, rate=50, gain=128, vref=2.5, noise_uv=0.6, seed=0, realtime=False)` with the same public surface as `AD7705`, plus `source_volts: float`, `drift_uv_per_s: float`, `simulated = True`, `calibrations: int`. Used by Tasks 4, 6.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_ad7705.py (append)
import statistics
from pogoscan.ad7705 import SimulatedAD7705


def test_simulator_noise_and_offset_statistics():
    sim = SimulatedAD7705(seed=1)
    sim.configure(); sim.self_calibrate()
    sim.source_volts = 5e-6
    uv = [sim.microvolts(c) for c in sim.read_codes(2000)]
    assert statistics.mean(uv) == pytest.approx(5.0, abs=0.15)
    assert 0.45 < statistics.pstdev(uv) < 0.9          # ~0.6 µV rms plus quantisation
    assert sim.simulated is True and sim.calibrations == 1


def test_simulator_is_deterministic_and_clips():
    a, b = SimulatedAD7705(seed=7), SimulatedAD7705(seed=7)
    assert a.read_codes(20) == b.read_codes(20)
    a.source_volts = 1.0                                # far beyond ±19.5 mV full scale
    assert a.read_code() == 65535
    a.source_volts = -1.0
    assert a.read_code() == 0
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_ad7705.py -v` — Expected: ImportError for `SimulatedAD7705`

- [ ] **Step 3: Write the simulator**

```python
# pogoscan/ad7705.py (append)
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

    def close(self) -> None:
        pass
```

- [ ] **Step 4: Run the tests** — `python3 -m pytest tests/test_ad7705.py -v` — Expected: 13 passed
- [ ] **Step 5: Run the full suite** — `python3 -m pytest` — Expected: all passed

---

### Task 4: `measure.py`

**Files:**
- Create: `pogoscan/measure.py`
- Test: `tests/test_measure.py`

**Interfaces:**
- Consumes: any ADC with `read_codes(n)` and `microvolts(code)` (Tasks 2, 3).
- Produces: `trimmed_mean(values, trim=0.1) -> float`, `PointResult` dataclass with `to_dict()`/`from_dict()`, `measure_point(adc, n=100, discard=4, trim=0.1) -> PointResult`. Used by Tasks 5, 6.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_measure.py
import pytest
from pogoscan.measure import trimmed_mean, measure_point, PointResult
from pogoscan.ad7705 import SimulatedAD7705
from tests.fakes import FakeSpi, FakeDrdy, FakeReset
from pogoscan.ad7705 import AD7705


def test_trimmed_mean_drops_tails():
    assert trimmed_mean([1, 2, 3, 4, 100], trim=0.2) == 3.0      # drops 1 and 100
    assert trimmed_mean([5, 5, 5]) == 5.0
    assert trimmed_mean([1, 2]) == 1.5                            # n < 3 → plain mean
    assert trimmed_mean([1.0] * 10 + [50.0], trim=0.1) == pytest.approx(1.0)
    with pytest.raises(ValueError):
        trimmed_mean([])


def test_measure_point_discards_settling_samples_and_reports_stats():
    spi = FakeSpi()
    spi.data_queue = [0, 0, 0, 0] + [32768 + k for k in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)]
    adc = AD7705(spi=spi, drdy=FakeDrdy(True), reset=FakeReset())
    adc.configure()
    r = measure_point(adc, n=10, discard=4, trim=0.1)
    assert r.n_total == 14 and r.n_kept == 10 and r.discarded == 4
    assert r.codes == [32769 + k for k in range(10)]
    assert r.min_uv == pytest.approx(0.596, rel=1e-3) and r.max_uv == pytest.approx(5.96, rel=1e-3)
    assert r.median_uv == pytest.approx(adc.microvolts(32773) + adc.lsb_volts * 1e6 / 2, rel=1e-3)
    assert r.value_uv == pytest.approx(3.278, rel=1e-2)          # trimmed mean of codes 2..9 above zero
    assert r.timestamp.endswith("+00:00") and r.duration_s >= 0


def test_measure_point_on_simulator_and_roundtrip():
    sim = SimulatedAD7705(seed=3); sim.source_volts = 2e-6
    r = measure_point(sim, n=100)
    assert r.value_uv == pytest.approx(2.0, abs=0.3) and r.stdev_uv < 1.0
    d = r.to_dict()
    assert PointResult.from_dict(d) == r and isinstance(d["codes"], list)
```

- [ ] **Step 2: Run the tests to verify they fail** — Expected: `ModuleNotFoundError: pogoscan.measure`

- [ ] **Step 3: Write the implementation**

```python
# pogoscan/measure.py
"""One measurement = a burst of conversions reduced to robust statistics."""
from __future__ import annotations

import statistics
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone


def trimmed_mean(values: list[float], trim: float = 0.1) -> float:
    if not values:
        raise ValueError("no values")
    if len(values) < 3:
        return statistics.fmean(values)
    ordered = sorted(values)
    k = int(len(ordered) * trim)
    kept = ordered[k:len(ordered) - k] if k else ordered
    return statistics.fmean(kept)


@dataclass
class PointResult:
    value_uv: float
    median_uv: float
    mean_uv: float
    stdev_uv: float
    min_uv: float
    max_uv: float
    n_total: int
    n_kept: int
    discarded: int
    codes: list[int]
    duration_s: float
    timestamp: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "PointResult":
        return cls(**{k: d[k] for k in cls.__dataclass_fields__})


def measure_point(adc, n: int = 100, discard: int = 4, trim: float = 0.1) -> PointResult:
    t0 = time.monotonic()
    codes = adc.read_codes(n + discard)
    kept = codes[discard:]
    uv = [adc.microvolts(c) for c in kept]
    return PointResult(
        value_uv=trimmed_mean(uv, trim),
        median_uv=statistics.median(uv),
        mean_uv=statistics.fmean(uv),
        stdev_uv=statistics.pstdev(uv) if len(uv) > 1 else 0.0,
        min_uv=min(uv),
        max_uv=max(uv),
        n_total=len(codes),
        n_kept=len(kept),
        discarded=discard,
        codes=list(kept),
        duration_s=time.monotonic() - t0,
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
```

- [ ] **Step 4: Run the tests** — Expected: 3 passed. (If `test_measure_point_discards…` fails on the `value_uv` number, recompute: kept codes 32769..32778 → 0.596·(1..10) µV; trim 10 % of 10 = 1 from each end → mean of 2..9 → 5.5 × 0.596 = 3.278 µV.)
- [ ] **Step 5: Run the full suite** — Expected: all passed

---

### Task 5: `scan.py` — grid state, cursor, undo, persistence, CSV

**Files:**
- Create: `pogoscan/scan.py`
- Test: `tests/test_scan.py`

**Interfaces:**
- Consumes: `PointResult` (Task 4).
- Produces: `ScanConfig`, `Scan` (`record`, `undo`, `goto`, `set_zero`, `zero_uv`, `progress`, `complete`, `grid`, `to_dict`, `save`, `load`, `to_csv`, attributes `id, path, config, cells, history, cursor, zero`), `new_scan(data_dir, config)`, `list_scans(data_dir)`, `open_scan(data_dir, scan_id)`, `slugify(name)`. Used by Task 6.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_scan.py
import json
import pytest
from pathlib import Path
from pogoscan.measure import PointResult
from pogoscan.scan import ScanConfig, Scan, new_scan, list_scans, open_scan, slugify


def pr(v):
    return PointResult(value_uv=v, median_uv=v, mean_uv=v, stdev_uv=0.1, min_uv=v - 1, max_uv=v + 1,
                       n_total=104, n_kept=100, discarded=4, codes=[32768], duration_s=2.0, timestamp="2026-09-17T00:00:00+00:00")


def test_new_scan_creates_directory_and_file(tmp_path):
    s = new_scan(tmp_path, ScanConfig(name="Weld A", rows=3, cols=2))
    assert s.path == tmp_path / s.id / "scan.json" and s.path.exists()
    assert s.id.startswith("weld-a-") and s.cursor == [0, 0] and s.progress() == (0, 6)
    assert s.config.created != ""


def test_record_advances_row_major_and_persists(tmp_path):
    s = new_scan(tmp_path, ScanConfig(name="t", rows=2, cols=3))
    s.record(0, 0, pr(1.0)); assert s.cursor == [0, 1]
    s.record(0, 1, pr(2.0)); s.record(0, 2, pr(3.0)); assert s.cursor == [1, 0]
    reloaded = Scan.load(s.path)
    assert reloaded.cells["0,2"]["value_uv"] == 3.0 and reloaded.cursor == [1, 0] and reloaded.history == [[0, 0], [0, 1], [0, 2]]


def test_cursor_skips_measured_cells_and_wraps(tmp_path):
    s = new_scan(tmp_path, ScanConfig(name="t", rows=2, cols=2))
    s.goto(1, 1); s.record(1, 1, pr(9.0))
    assert s.cursor == [0, 0]                       # wraps to the first unmeasured cell
    s.record(0, 0, pr(1.0)); s.record(0, 1, pr(2.0))
    assert s.cursor == [1, 0]
    s.record(1, 0, pr(3.0))
    assert s.complete() and s.cursor == [1, 0]       # stays put when complete


def test_undo_restores_cursor_and_removes_cell(tmp_path):
    s = new_scan(tmp_path, ScanConfig(name="t", rows=2, cols=2))
    s.record(0, 0, pr(1.0)); s.record(0, 1, pr(2.0))
    assert s.undo() == [0, 1] and "0,1" not in s.cells and s.cursor == [0, 1]
    assert s.undo() == [0, 0] and s.undo() is None


def test_goto_bounds(tmp_path):
    s = new_scan(tmp_path, ScanConfig(name="t", rows=2, cols=2))
    with pytest.raises(ValueError):
        s.goto(2, 0)


def test_zero_grid_and_csv(tmp_path):
    s = new_scan(tmp_path, ScanConfig(name="t", rows=2, cols=2, pitch_mm=3.0))
    s.record(0, 0, pr(4.0)); s.set_zero(pr(1.5))
    assert s.zero_uv() == 1.5
    assert s.grid() == [[2.5, None], [None, None]] and s.grid(relative=False) == [[4.0, None], [None, None]]
    csv = s.to_csv().splitlines()
    assert csv[0] == "row,col,x_mm,y_mm,value_uv,rel_uv,median_uv,mean_uv,stdev_uv,min_uv,max_uv,n_kept,timestamp"
    assert csv[1].startswith("0,0,0.0,0.0,4.0,2.5,")
    s.set_zero(None); assert s.zero_uv() is None and s.grid()[0][0] == 4.0
    d = s.to_dict()
    assert d["progress"] == [1, 4] and d["complete"] is False and d["grid"][0][0] == 4.0 and d["id"] == s.id


def test_list_and_open_scans(tmp_path):
    a = new_scan(tmp_path, ScanConfig(name="first", rows=1, cols=1))
    b = new_scan(tmp_path, ScanConfig(name="second", rows=1, cols=1))
    (tmp_path / "broken").mkdir(); (tmp_path / "broken" / "scan.json").write_text("{not json")
    listed = list_scans(tmp_path)
    assert [x["id"] for x in listed][:2] == sorted([a.id, b.id], reverse=True) or listed[0]["id"] in (a.id, b.id)
    assert any("error" in x for x in listed)
    assert open_scan(tmp_path, a.id).id == a.id
    with pytest.raises(FileNotFoundError):
        open_scan(tmp_path, "nope")
    assert slugify("Weld  #3 / left") == "weld-3-left"
```

- [ ] **Step 2: Run the tests to verify they fail** — Expected: `ModuleNotFoundError: pogoscan.scan`

- [ ] **Step 3: Write the implementation**

```python
# pogoscan/scan.py
"""Scan state: a rows×cols grid of PointResults, a cursor, an undo stack, atomic JSON persistence, CSV export."""
from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

from .measure import PointResult

CSV_HEADER = "row,col,x_mm,y_mm,value_uv,rel_uv,median_uv,mean_uv,stdev_uv,min_uv,max_uv,n_kept,timestamp"


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "scan"


@dataclass
class ScanConfig:
    name: str
    rows: int = 21
    cols: int = 21
    pitch_mm: float = 3.0
    samples: int = 100
    discard: int = 4
    gain: int = 128
    rate: int = 50
    created: str = ""


class Scan:
    def __init__(self, scan_id: str, path: Path, config: ScanConfig):
        self.id, self.path, self.config = scan_id, Path(path), config
        self.cells: dict[str, dict] = {}
        self.history: list[list[int]] = []
        self.cursor: list[int] = [0, 0]
        self.zero: dict | None = None

    # --- helpers ---------------------------------------------------------
    @staticmethod
    def key(row: int, col: int) -> str:
        return f"{row},{col}"

    def _check(self, row: int, col: int) -> None:
        if not (0 <= row < self.config.rows and 0 <= col < self.config.cols):
            raise ValueError(f"cell ({row}, {col}) outside {self.config.rows}x{self.config.cols}")

    def _next_unmeasured(self, row: int, col: int) -> list[int]:
        total = self.config.rows * self.config.cols
        start = row * self.config.cols + col
        for step in range(1, total + 1):
            i = (start + step) % total
            r, c = divmod(i, self.config.cols)
            if self.key(r, c) not in self.cells:
                return [r, c]
        return [row, col]

    # --- mutations (each saves) -------------------------------------------
    def record(self, row: int, col: int, result: PointResult) -> None:
        self._check(row, col)
        self.cells[self.key(row, col)] = {**result.to_dict(), "row": row, "col": col}
        self.history.append([row, col])
        self.cursor = self._next_unmeasured(row, col)
        self.save()

    def undo(self) -> list[int] | None:
        if not self.history:
            return None
        row, col = self.history.pop()
        self.cells.pop(self.key(row, col), None)
        self.cursor = [row, col]
        self.save()
        return [row, col]

    def goto(self, row: int, col: int) -> None:
        self._check(row, col)
        self.cursor = [row, col]
        self.save()

    def set_zero(self, result: PointResult | None) -> None:
        self.zero = result.to_dict() if result is not None else None
        self.save()

    # --- queries ----------------------------------------------------------
    def zero_uv(self) -> float | None:
        return None if self.zero is None else self.zero["value_uv"]

    def progress(self) -> tuple[int, int]:
        return len(self.cells), self.config.rows * self.config.cols

    def complete(self) -> bool:
        m, t = self.progress()
        return m >= t

    def grid(self, relative: bool = True) -> list[list[float | None]]:
        z = self.zero_uv() if relative else None
        out = []
        for r in range(self.config.rows):
            row = []
            for c in range(self.config.cols):
                cell = self.cells.get(self.key(r, c))
                row.append(None if cell is None else cell["value_uv"] - (z or 0.0))
            out.append(row)
        return out

    def to_dict(self) -> dict:
        m, t = self.progress()
        return {"id": self.id, "config": asdict(self.config), "cells": self.cells, "history": self.history,
                "cursor": self.cursor, "zero": self.zero, "progress": [m, t], "complete": self.complete(),
                "grid": self.grid(True), "grid_raw": self.grid(False)}

    def to_csv(self) -> str:
        z = self.zero_uv()
        lines = [CSV_HEADER]
        for r in range(self.config.rows):
            for c in range(self.config.cols):
                cell = self.cells.get(self.key(r, c))
                if cell is None:
                    continue
                rel = cell["value_uv"] - z if z is not None else cell["value_uv"]
                lines.append(",".join(str(x) for x in (
                    r, c, c * self.config.pitch_mm, r * self.config.pitch_mm, cell["value_uv"], rel, cell["median_uv"],
                    cell["mean_uv"], cell["stdev_uv"], cell["min_uv"], cell["max_uv"], cell["n_kept"], cell["timestamp"])))
        return "\n".join(lines) + "\n"

    # --- persistence ------------------------------------------------------
    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"id": self.id, "config": asdict(self.config), "cells": self.cells, "history": self.history,
                   "cursor": self.cursor, "zero": self.zero}
        tmp = self.path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(payload, indent=1))
        os.replace(tmp, self.path)

    @classmethod
    def load(cls, path: Path) -> "Scan":
        path = Path(path)
        d = json.loads(path.read_text())
        s = cls(d["id"], path, ScanConfig(**d["config"]))
        s.cells, s.history, s.cursor, s.zero = d["cells"], d["history"], d["cursor"], d.get("zero")
        return s


def new_scan(data_dir: Path, config: ScanConfig) -> Scan:
    data_dir = Path(data_dir)
    if not config.created:
        config.created = datetime.now(timezone.utc).isoformat(timespec="seconds")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    scan_id = f"{slugify(config.name)}-{stamp}"
    n = 1
    while (data_dir / scan_id).exists():
        n += 1
        scan_id = f"{slugify(config.name)}-{stamp}-{n}"
    s = Scan(scan_id, data_dir / scan_id / "scan.json", config)
    s.save()
    return s


def list_scans(data_dir: Path) -> list[dict]:
    data_dir = Path(data_dir)
    out = []
    if not data_dir.exists():
        return out
    for p in sorted(data_dir.iterdir(), reverse=True):
        f = p / "scan.json"
        if not f.exists():
            continue
        try:
            s = Scan.load(f)
            out.append({"id": s.id, "name": s.config.name, "created": s.config.created, "progress": list(s.progress())})
        except Exception as e:  # noqa: BLE001 - report, never crash the listing
            out.append({"id": p.name, "error": f"unreadable: {e}"})
    return out


def open_scan(data_dir: Path, scan_id: str) -> Scan:
    f = Path(data_dir) / scan_id / "scan.json"
    if not f.exists() or "/" in scan_id or scan_id in ("", ".", ".."):
        raise FileNotFoundError(scan_id)
    return Scan.load(f)
```

- [ ] **Step 4: Run the tests** — `python3 -m pytest tests/test_scan.py -v` — Expected: 7 passed
- [ ] **Step 5: Run the full suite** — Expected: all passed

---

### Task 6: `server.py` — JSON API, static files, simulation

**Files:**
- Create: `pogoscan/server.py`
- Test: `tests/test_server.py`

**Interfaces:**
- Consumes: `AD7705`, `SimulatedAD7705`, `AD7705Error` (Tasks 2–3); `measure_point` (4); `ScanConfig, Scan, new_scan, list_scans, open_scan` (5).
- Produces: `plate_uv(row, col, rows, cols) -> float`, `make_adc(args)`, `class App` (holds adc, lock, scan, data_dir, samples, discard), `class Handler(BaseHTTPRequestHandler)`, `make_server(app, host, port) -> ThreadingHTTPServer`, `main(argv=None)`. Endpoints exactly as spec §5.4. Used by Task 8 (contract) and Task 9.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_server.py
import json
import threading
import http.client
import pytest
from pogoscan.server import App, make_server, plate_uv
from pogoscan.ad7705 import SimulatedAD7705


@pytest.fixture
def client(tmp_path):
    app = App(adc=SimulatedAD7705(seed=1), data_dir=tmp_path, samples=20, discard=2)
    srv = make_server(app, "127.0.0.1", 0)
    t = threading.Thread(target=srv.serve_forever, daemon=True); t.start()
    conn = http.client.HTTPConnection("127.0.0.1", srv.server_address[1], timeout=10)

    def call(method, path, body=None):
        conn.request(method, path, body=None if body is None else json.dumps(body), headers={"Content-Type": "application/json"})
        r = conn.getresponse(); data = r.read()
        return r.status, r.getheader("Content-Type"), data
    yield call
    srv.shutdown(); srv.server_close()


def j(data):
    return json.loads(data)


def test_state_without_scan(client):
    st, ct, data = client("GET", "/api/state")
    d = j(data)
    assert st == 200 and d["scan"] is None and d["measuring"] is False and d["adc"]["simulated"] is True
    assert d["adc"]["lsb_uv"] == pytest.approx(0.596, rel=1e-3) and d["adc"]["samples"] == 20


def test_measure_requires_scan(client):
    st, _, data = client("POST", "/api/measure", {})
    assert st == 400 and "error" in j(data)


def test_full_scan_flow(client):
    st, _, data = client("POST", "/api/scan/new", {"name": "Sim", "rows": 2, "cols": 2, "pitch_mm": 3.0, "samples": 20})
    d = j(data); assert st == 200 and d["scan"]["progress"] == [0, 4] and d["adc"]["samples"] == 20
    st, _, data = client("POST", "/api/measure", {})
    d = j(data); cell = d["cell"]
    assert st == 200 and (cell["row"], cell["col"]) == (0, 0) and cell["n_kept"] == 20 and d["scan"]["cursor"] == [0, 1]
    assert abs(cell["value_uv"] - plate_uv(0, 0, 2, 2)) < 0.6
    st, _, data = client("POST", "/api/undo", {}); assert j(data)["scan"]["cursor"] == [0, 0]
    st, _, data = client("POST", "/api/goto", {"row": 1, "col": 1}); assert j(data)["scan"]["cursor"] == [1, 1]
    st, _, data = client("POST", "/api/goto", {"row": 5, "col": 0}); assert st == 400
    st, _, data = client("POST", "/api/zero", {}); d = j(data); assert st == 200 and d["scan"]["zero"] is not None
    st, _, data = client("POST", "/api/zero/clear", {}); assert j(data)["scan"]["zero"] is None
    st, _, data = client("POST", "/api/calibrate", {}); assert st == 200 and j(data)["ok"] is True
    for _ in range(4):
        client("POST", "/api/measure", {})
    st, _, data = client("GET", "/api/state"); d = j(data); assert d["scan"]["complete"] is True
    st, _, data = client("POST", "/api/measure", {}); assert st == 400
    st, ct, data = client("GET", "/api/export.csv")
    assert st == 200 and ct.startswith("text/csv") and data.decode().splitlines()[0].startswith("row,col,x_mm")
    st, ct, data = client("GET", "/api/export.json"); assert st == 200 and j(data)["id"] == d["scan"]["id"]
    st, _, data = client("GET", "/api/noise?n=10"); d2 = j(data); assert st == 200 and d2["n"] == 10 and "stdev_uv" in d2
    st, _, data = client("POST", "/api/scan/open", {"id": d["scan"]["id"]}); assert st == 200
    st, _, data = client("POST", "/api/scan/open", {"id": "missing"}); assert st == 404


def test_static_and_unknown_routes(client):
    st, ct, data = client("GET", "/")
    assert st == 200 and ct.startswith("text/html") and b"app.js" in data
    st, ct, _ = client("GET", "/static/app.js"); assert st == 200 and ct.startswith("application/javascript")
    st, _, _ = client("GET", "/static/../server.py"); assert st in (400, 404)
    st, _, _ = client("GET", "/nope"); assert st == 404


def test_plate_pattern_has_weld_band_and_gradient():
    assert plate_uv(10, 0, 21, 21) > plate_uv(0, 0, 21, 21) + 4
    assert plate_uv(0, 20, 21, 21) > plate_uv(0, 0, 21, 21)
```

- [ ] **Step 2: Run the tests to verify they fail** — Expected: `ModuleNotFoundError: pogoscan.server`

- [ ] **Step 3: Write the server**

```python
# pogoscan/server.py
"""Stdlib HTTP server: JSON API for the scan plus the static page. Run: python3 -m pogoscan.server [--simulate]."""
from __future__ import annotations

import argparse
import json
import math
import mimetypes
import statistics
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from .ad7705 import AD7705, SimulatedAD7705, AD7705Error
from .measure import measure_point
from .scan import ScanConfig, Scan, new_scan, list_scans, open_scan

STATIC_DIR = Path(__file__).parent / "static"
CONTENT_TYPES = {".html": "text/html; charset=utf-8", ".js": "application/javascript; charset=utf-8", ".css": "text/css; charset=utf-8"}


def plate_uv(row: int, col: int, rows: int, cols: int) -> float:
    """Synthetic plate for --simulate: gradient along columns, weld band at row 10, hot spot at (4, 15)."""
    gradient = 1.0 * col / max(cols - 1, 1)
    weld = 5.0 * math.exp(-((row - 10) ** 2) / 2.0)
    spot = 3.0 * math.exp(-(((row - 4) ** 2 + (col - 15) ** 2)) / 8.0)
    return gradient + weld + spot


class Busy(Exception):
    pass


class App:
    def __init__(self, adc, data_dir: Path, samples: int = 100, discard: int = 4):
        self.adc, self.data_dir, self.samples, self.discard = adc, Path(data_dir), samples, discard
        self.lock = threading.Lock()
        self.measuring = False
        self.scan: Scan | None = None

    # -- state --------------------------------------------------------------
    def state(self) -> dict:
        return {"scan": self.scan.to_dict() if self.scan else None, "measuring": self.measuring,
                "adc": {"simulated": bool(getattr(self.adc, "simulated", False)), "gain": self.adc.gain, "rate": self.adc.rate,
                        "lsb_uv": self.adc.lsb_volts * 1e6, "samples": self.samples, "discard": self.discard},
                "scans": list_scans(self.data_dir)}

    def _acquire(self):
        if not self.lock.acquire(blocking=False):
            raise Busy("a measurement is already running")
        self.measuring = True

    def _release(self):
        self.measuring = False
        self.lock.release()

    def _set_source(self, row: int | None, col: int | None) -> None:
        if getattr(self.adc, "simulated", False):
            cfg = self.scan.config if self.scan else ScanConfig(name="")
            self.adc.source_volts = 0.0 if row is None else plate_uv(row, col, cfg.rows, cfg.cols) * 1e-6

    # -- actions (all raise Busy / ValueError / AD7705Error) ----------------
    def new_scan(self, body: dict) -> None:
        cfg = ScanConfig(name=str(body.get("name") or "scan"), rows=int(body.get("rows", 21)), cols=int(body.get("cols", 21)),
                         pitch_mm=float(body.get("pitch_mm", 3.0)), samples=int(body.get("samples", self.samples)), discard=self.discard,
                         gain=self.adc.gain, rate=self.adc.rate)
        if cfg.rows < 1 or cfg.cols < 1 or cfg.samples < 3:
            raise ValueError("rows and cols must be ≥ 1 and samples ≥ 3")
        self._acquire()
        try:
            self.adc.configure(rate=self.adc.rate, gain=self.adc.gain)
            self.adc.self_calibrate()
            self.samples = cfg.samples
            self.scan = new_scan(self.data_dir, cfg)
        finally:
            self._release()

    def open_scan(self, scan_id: str) -> None:
        self.scan = open_scan(self.data_dir, scan_id)
        self.samples = self.scan.config.samples

    def measure(self) -> dict:
        if self.scan is None:
            raise ValueError("no scan open")
        if self.scan.complete():
            raise ValueError("scan is complete; use goto or undo to re-measure a cell")
        row, col = self.scan.cursor
        self._acquire()
        try:
            self._set_source(row, col)
            result = measure_point(self.adc, n=self.samples, discard=self.discard)
            self.scan.record(row, col, result)
        finally:
            self._release()
        return {**result.to_dict(), "row": row, "col": col}

    def zero(self) -> None:
        if self.scan is None:
            raise ValueError("no scan open")
        self._acquire()
        try:
            self._set_source(None, None)
            self.scan.set_zero(measure_point(self.adc, n=self.samples, discard=self.discard))
        finally:
            self._release()

    def calibrate(self) -> float:
        self._acquire()
        try:
            return self.adc.self_calibrate()
        finally:
            self._release()

    def noise(self, n: int) -> dict:
        self._acquire()
        try:
            self._set_source(None, None)
            uv = [self.adc.microvolts(c) for c in self.adc.read_codes(n)]
        finally:
            self._release()
        return {"n": n, "mean_uv": statistics.fmean(uv), "stdev_uv": statistics.pstdev(uv) if n > 1 else 0.0, "min_uv": min(uv), "max_uv": max(uv)}


class Handler(BaseHTTPRequestHandler):
    app: App  # set by make_server

    def log_message(self, fmt, *args):  # quieter console
        pass

    # -- helpers ------------------------------------------------------------
    def _json(self, status: int, payload) -> None:
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _error(self, status: int, message: str) -> None:
        self._json(status, {"error": message})

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b""
        if not raw:
            return {}
        try:
            body = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"invalid JSON body: {e}") from e
        return body if isinstance(body, dict) else {}

    def _static(self, name: str) -> None:
        target = (STATIC_DIR / name).resolve()
        if not str(target).startswith(str(STATIC_DIR.resolve())) or not target.is_file():
            self._error(404, "not found")
            return
        data = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", CONTENT_TYPES.get(target.suffix, mimetypes.guess_type(str(target))[0] or "application/octet-stream"))
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)

    def _file(self, status: int, content_type: str, data: bytes, filename: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # -- routing ------------------------------------------------------------
    def do_GET(self) -> None:
        url = urlparse(self.path)
        try:
            if url.path == "/":
                return self._static("index.html")
            if url.path.startswith("/static/"):
                return self._static(url.path[len("/static/"):])
            if url.path == "/api/state":
                return self._json(200, self.app.state())
            if url.path == "/api/export.csv":
                if self.app.scan is None:
                    return self._error(400, "no scan open")
                return self._file(200, "text/csv; charset=utf-8", self.app.scan.to_csv().encode(), f"{self.app.scan.id}.csv")
            if url.path == "/api/export.json":
                if self.app.scan is None:
                    return self._error(400, "no scan open")
                return self._file(200, "application/json", self.app.scan.path.read_bytes(), f"{self.app.scan.id}.json")
            if url.path == "/api/noise":
                n = max(2, min(1000, int(parse_qs(url.query).get("n", ["50"])[0])))
                return self._json(200, self.app.noise(n))
            return self._error(404, "not found")
        except Busy as e:
            self._error(409, str(e))
        except ValueError as e:
            self._error(400, str(e))
        except AD7705Error as e:
            self._error(500, f"ADC error: {e}")

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            body = self._body()
            if path == "/api/scan/new":
                self.app.new_scan(body)
            elif path == "/api/scan/open":
                self.app.open_scan(str(body.get("id", "")))
            elif path == "/api/measure":
                cell = self.app.measure()
                return self._json(200, {"cell": cell, "scan": self.app.scan.to_dict()})
            elif path == "/api/undo":
                if self.app.scan is None:
                    raise ValueError("no scan open")
                self.app.scan.undo()
            elif path == "/api/goto":
                if self.app.scan is None:
                    raise ValueError("no scan open")
                self.app.scan.goto(int(body.get("row", -1)), int(body.get("col", -1)))
            elif path == "/api/zero":
                self.app.zero()
            elif path == "/api/zero/clear":
                if self.app.scan is None:
                    raise ValueError("no scan open")
                self.app.scan.set_zero(None)
            elif path == "/api/calibrate":
                return self._json(200, {"ok": True, "seconds": self.app.calibrate()})
            else:
                return self._error(404, "not found")
            return self._json(200, self.app.state())
        except Busy as e:
            self._error(409, str(e))
        except FileNotFoundError as e:
            self._error(404, f"unknown scan {e}")
        except (ValueError, TypeError) as e:
            self._error(400, str(e))
        except AD7705Error as e:
            self._error(500, f"ADC error: {e}")


def make_server(app: App, host: str, port: int) -> ThreadingHTTPServer:
    handler = type("BoundHandler", (Handler,), {"app": app})
    ThreadingHTTPServer.allow_reuse_address = True
    return ThreadingHTTPServer((host, port), handler)


def make_adc(args) -> object:
    if args.simulate:
        return SimulatedAD7705(realtime=args.realtime)
    adc = AD7705(bus=args.bus, device=args.device, drdy_pin=args.drdy, reset_pin=args.reset, crystal_hz=args.crystal)
    adc.reset()
    adc.configure(rate=50, gain=128)
    return adc


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description="pogoscan web server")
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=8080)
    p.add_argument("--data-dir", default="data")
    p.add_argument("--simulate", action="store_true", help="use the simulated ADC")
    p.add_argument("--realtime", action="store_true", help="simulator sleeps 1/rate per sample")
    p.add_argument("--samples", type=int, default=100)
    p.add_argument("--discard", type=int, default=4)
    p.add_argument("--crystal", type=float, default=4.9152e6)
    p.add_argument("--drdy", type=int, default=25)
    p.add_argument("--reset", type=int, default=24)
    p.add_argument("--bus", type=int, default=0)
    p.add_argument("--device", type=int, default=0)
    args = p.parse_args(argv)
    app = App(make_adc(args), Path(args.data_dir), samples=args.samples, discard=args.discard)
    srv = make_server(app, args.host, args.port)
    print(f"pogoscan {'SIMULATED' if getattr(app.adc, 'simulated', False) else 'AD7705'} on http://{args.host}:{srv.server_address[1]}/  data in {app.data_dir.resolve()}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
        app.adc.close()


if __name__ == "__main__":
    main()
```

Note for `test_static_and_unknown_routes`: it needs `static/index.html` and `static/app.js` to exist. If Task 8 has not landed yet, create minimal placeholders (`index.html` containing `<script src="/static/app.js"></script>` and an empty `app.js`) — Task 8 overwrites them.

- [ ] **Step 4: Run the tests** — `python3 -m pytest tests/test_server.py -v` — Expected: 5 passed
- [ ] **Step 5: Run the full suite** — Expected: all passed

---

### Task 7: `check.py` — hardware self-test

**Files:**
- Create: `pogoscan/check.py`
- Test: `tests/test_check.py`

**Interfaces:**
- Consumes: `AD7705`, `AD7705Error`, `clock_byte`, `setup_byte` (Tasks 1–2).
- Produces: `run_checks(adc, expected_rate=50, seconds=2.0, spidev_path=None) -> tuple[bool, list[str]]` (pure report builder; `spidev_path=None` skips the device-file check) and `main(argv=None)`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_check.py
from pogoscan.check import run_checks
from pogoscan.ad7705 import AD7705
from tests.fakes import FakeSpi, FakeDrdy, FakeReset


def test_run_checks_passes_with_working_fake():
    spi = FakeSpi(); spi.data_queue = [32768 + (i % 3) for i in range(200)]
    adc = AD7705(spi=spi, drdy=FakeDrdy(True), reset=FakeReset())
    ok, lines = run_checks(adc, expected_rate=50, seconds=0.05)
    text = "\n".join(lines)
    assert "clock register" in text and "PASS" in text and "stdev" in text
    assert ok is True


def test_run_checks_reports_open_miso():
    adc = AD7705(spi=FakeSpi(miso_open=True), drdy=FakeDrdy(True), reset=FakeReset())
    ok, lines = run_checks(adc, expected_rate=50, seconds=0.05)
    assert ok is False and any("MISO" in l for l in lines)
```

- [ ] **Step 2: Run the tests to verify they fail** — Expected: `ModuleNotFoundError: pogoscan.check`

- [ ] **Step 3: Write the implementation**

```python
# pogoscan/check.py
"""Hardware self-test for the AD7705 wiring. Run on the Pi: python3 -m pogoscan.check"""
from __future__ import annotations

import argparse
import os
import statistics
import sys
import time

from .ad7705 import AD7705, AD7705Error, AD7705Timeout


def run_checks(adc, expected_rate: int = 50, seconds: float = 2.0, spidev_path: str | None = None) -> tuple[bool, list[str]]:
    lines: list[str] = []
    ok = True

    def report(passed: bool, text: str) -> None:
        nonlocal ok
        ok = ok and passed
        lines.append(f"[{'PASS' if passed else 'FAIL'}] {text}")

    if spidev_path is not None:
        exists = os.path.exists(spidev_path)
        report(exists, f"{spidev_path} exists" + ("" if exists else " — enable SPI: add dtparam=spi=on to /boot/firmware/config.txt and reboot"))
        if not exists:
            return False, lines
    try:
        adc.reset()
        adc.configure(rate=expected_rate, gain=128)
        report(True, f"clock register 0x{adc.read_register(2):02X} and setup register 0x{adc.read_register(1):02X} read back correctly")
    except AD7705Error as e:
        report(False, f"clock register / setup register: {e}")
        if "0x00" in str(e):
            lines.append("       hint: DOUT→MISO (GPIO9) is open: check the orange wire, its solder joint at the module DOUT pin and the level shifter")
        return False, lines
    try:
        t = adc.self_calibrate(timeout=2.0)
        report(True, f"self-calibration completed in {t * 1000:.0f} ms")
    except AD7705Error as e:
        report(False, f"self-calibration: {e}")
        return False, lines
    # DRDY rate
    n, t0 = 0, time.monotonic()
    try:
        while time.monotonic() - t0 < seconds:
            adc.read_code(timeout=1.0)
            n += 1
    except AD7705Timeout as e:
        report(False, f"DRDY: {e}")
        return False, lines
    rate = n / max(time.monotonic() - t0, 1e-9)
    rate_ok = n >= 3 and (abs(rate - expected_rate) / expected_rate < 0.15 or getattr(adc, "simulated", False) or seconds < 0.5)
    report(rate_ok, f"DRDY rate {rate:.1f} Hz over {seconds:.1f} s (expected {expected_rate} Hz)")
    # noise burst
    uv = [adc.microvolts(c) for c in adc.read_codes(100)]
    sd = statistics.pstdev(uv)
    burst_ok = 0.0 < sd < 5.0
    report(burst_ok, f"100-sample burst: mean {statistics.fmean(uv):.2f} µV, stdev {sd:.2f} µV, min {min(uv):.1f}, max {max(uv):.1f}"
           + ("" if burst_ok else " — stdev 0 means a stuck line; > 5 µV means noise pickup or an open input"))
    return ok, lines


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="AD7705 wiring self-test")
    p.add_argument("--crystal", type=float, default=4.9152e6)
    p.add_argument("--rate", type=int, default=50)
    p.add_argument("--drdy", type=int, default=25)
    p.add_argument("--reset", type=int, default=24)
    p.add_argument("--bus", type=int, default=0)
    p.add_argument("--device", type=int, default=0)
    args = p.parse_args(argv)
    path = f"/dev/spidev{args.bus}.{args.device}"
    if not os.path.exists(path):
        print(f"[FAIL] {path} missing — enable SPI (dtparam=spi=on in /boot/firmware/config.txt) and reboot")
        return 1
    adc = AD7705(bus=args.bus, device=args.device, drdy_pin=args.drdy, reset_pin=args.reset, crystal_hz=args.crystal)
    try:
        ok, lines = run_checks(adc, expected_rate=args.rate, spidev_path=path)
    finally:
        adc.close()
    print("\n".join(lines))
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run the tests** — Expected: 2 passed
- [ ] **Step 5: Run the full suite** — Expected: all passed

---

### Task 8: Web page (`static/`)

**Files:**
- Create: `pogoscan/static/index.html`, `pogoscan/static/style.css`, `pogoscan/static/app.js`
- Test: `tests/test_static.py`

**Interfaces:**
- Consumes: the API in spec §5.4 only (`/api/state`, `/api/scan/new`, `/api/scan/open`, `/api/measure`, `/api/undo`, `/api/goto`, `/api/zero`, `/api/zero/clear`, `/api/calibrate`, `/api/noise?n=`, `/api/export.csv`, `/api/export.json`). Shape of `state.scan` = `Scan.to_dict()` (fields `id, config{rows, cols, pitch_mm, samples, name}, cells, history, cursor[row, col], zero, progress[m, total], complete, grid, grid_raw`).
- Produces: element ids `heatmap` (canvas), `measure-btn`, `undo-btn`, `zero-btn`, `zero-clear-btn`, `calibrate-btn`, `noise-btn`, `new-btn`, `open-select`, `csv-link`, `json-link`, `png-btn`, `relative-toggle`, `scale-min`, `scale-max`, `scale-auto`, `status`, `next-cell`, `progress`, `last-value`, `toast`, `legend` (canvas).

Before writing any drawing code, load the **dataviz** skill (`Skill` tool, name `dataviz`) and follow it for the colour map, legend and accessibility; keep the page a plain lab tool (no decoration, no frameworks, no external fonts or scripts).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_static.py
from pathlib import Path

STATIC = Path(__file__).resolve().parents[1] / "pogoscan" / "static"


def test_page_references_assets_and_control_ids():
    html = (STATIC / "index.html").read_text()
    assert 'src="/static/app.js"' in html and 'href="/static/style.css"' in html
    for cid in ("heatmap", "measure-btn", "undo-btn", "zero-btn", "calibrate-btn", "noise-btn", "new-btn",
                "open-select", "csv-link", "json-link", "png-btn", "relative-toggle", "scale-min", "scale-max",
                "scale-auto", "status", "next-cell", "progress", "last-value", "toast", "legend"):
        assert f'id="{cid}"' in html, cid
    js = (STATIC / "app.js").read_text()
    for path in ("/api/state", "/api/measure", "/api/undo", "/api/goto", "/api/zero", "/api/scan/new", "/api/noise"):
        assert path in js, path
    assert "http://" not in js and "https://" not in html
```

- [ ] **Step 2: Run the test to verify it fails** — Expected: FileNotFoundError or assertion on missing ids

- [ ] **Step 3: Write `index.html`**

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>pogoscan</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<header>
  <h1>pogoscan</h1>
  <div id="status" class="status">connecting…</div>
</header>
<main>
  <section class="map">
    <canvas id="heatmap" width="630" height="630" aria-label="potential heatmap"></canvas>
    <div class="legend-row"><span id="scale-min-label">min</span><canvas id="legend" width="300" height="14"></canvas><span id="scale-max-label">max</span><span class="unit">µV</span></div>
    <div class="scale">
      <label><input type="checkbox" id="scale-auto" checked> auto scale</label>
      <label>min <input type="number" id="scale-min" step="0.1"></label>
      <label>max <input type="number" id="scale-max" step="0.1"></label>
      <label><input type="checkbox" id="relative-toggle" checked> relative to zero</label>
    </div>
    <div id="hover" class="hover"></div>
  </section>
  <section class="panel">
    <div class="next">Next: <strong id="next-cell">–</strong></div>
    <div class="progress" id="progress">0 / 0</div>
    <button id="measure-btn" class="big">Measure <kbd>Space</kbd></button>
    <div class="last">Last: <span id="last-value">–</span></div>
    <div class="row">
      <button id="undo-btn">Undo <kbd>U</kbd></button>
      <button id="zero-btn">Zero</button>
      <button id="zero-clear-btn">Clear zero</button>
    </div>
    <div class="row">
      <button id="calibrate-btn">Calibrate</button>
      <button id="noise-btn">Noise check</button>
    </div>
    <details class="new">
      <summary>New scan</summary>
      <label>name <input id="new-name" value="weld"></label>
      <label>rows <input id="new-rows" type="number" value="21" min="1"></label>
      <label>cols <input id="new-cols" type="number" value="21" min="1"></label>
      <label>pitch mm <input id="new-pitch" type="number" value="3" step="0.1"></label>
      <label>samples <input id="new-samples" type="number" value="100" min="3"></label>
      <button id="new-btn">Start new scan</button>
    </details>
    <label>Open scan <select id="open-select"></select></label>
    <div class="row exports">
      <a id="csv-link" href="/api/export.csv" download>CSV</a>
      <a id="json-link" href="/api/export.json" download>JSON</a>
      <button id="png-btn">PNG</button>
    </div>
    <div class="adc" id="adc-info"></div>
  </section>
</main>
<div id="toast" class="toast" hidden></div>
<script src="/static/app.js"></script>
</body>
</html>
```

- [ ] **Step 4: Write `app.js`** (core; extend freely but keep the ids and endpoints)

```javascript
'use strict';
const $ = (id) => document.getElementById(id);
const state = { data: null, hover: null, busy: false };

async function api(method, path, body) {
  const res = await fetch(path, { method, headers: { 'Content-Type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body) });
  const json = await res.json().catch(() => ({ error: `HTTP ${res.status}` }));
  if (!res.ok) throw new Error(json.error || `HTTP ${res.status}`);
  return json;
}

function toast(msg, isError) {
  const t = $('toast'); t.textContent = msg; t.classList.toggle('error', !!isError); t.hidden = false;
  clearTimeout(toast.timer); toast.timer = setTimeout(() => { t.hidden = true; }, 4000);
}

async function refresh() {
  try { state.data = await api('GET', '/api/state'); render(); }
  catch (e) { $('status').textContent = 'server unreachable: ' + e.message; }
}

async function act(method, path, body) {
  if (state.busy) return;
  state.busy = true; setButtons();
  try {
    const r = await api(method, path, body);
    if (r.cell) toast(`(${r.cell.row}, ${r.cell.col}) = ${r.cell.value_uv.toFixed(2)} µV ± ${r.cell.stdev_uv.toFixed(2)}`);
    await refresh();
    return r;
  } catch (e) { toast(e.message, true); await refresh(); }
  finally { state.busy = false; setButtons(); }
}

function setButtons() {
  const s = state.data && state.data.scan;
  const measuring = state.busy || (state.data && state.data.measuring);
  $('measure-btn').disabled = measuring || !s || s.complete;
  for (const id of ['undo-btn', 'zero-btn', 'zero-clear-btn', 'calibrate-btn', 'noise-btn', 'png-btn']) $(id).disabled = measuring || (!s && id !== 'calibrate-btn' && id !== 'noise-btn');
  $('measure-btn').textContent = measuring ? 'Measuring…' : 'Measure (Space)';
}

// ---- colour map: sequential, perceptually ordered (see dataviz skill) ----
const STOPS = [[0.0, [68, 1, 84]], [0.25, [59, 82, 139]], [0.5, [33, 145, 140]], [0.75, [94, 201, 98]], [1.0, [253, 231, 37]]];
function colour(t) {
  t = Math.max(0, Math.min(1, t));
  for (let i = 1; i < STOPS.length; i++) {
    if (t <= STOPS[i][0]) {
      const [t0, c0] = STOPS[i - 1], [t1, c1] = STOPS[i], f = (t - t0) / (t1 - t0);
      return `rgb(${c0.map((v, k) => Math.round(v + (c1[k] - v) * f)).join(',')})`;
    }
  }
  return `rgb(${STOPS[STOPS.length - 1][1].join(',')})`;
}

function currentGrid() {
  const s = state.data.scan;
  return $('relative-toggle').checked ? s.grid : s.grid_raw;
}

function scale(grid) {
  const vals = grid.flat().filter((v) => v !== null);
  if ($('scale-auto').checked || !$('scale-min').value || !$('scale-max').value) {
    const min = vals.length ? Math.min(...vals) : 0, max = vals.length ? Math.max(...vals) : 1;
    $('scale-min').value = min.toFixed(2); $('scale-max').value = max.toFixed(2);
    return [min, max === min ? min + 1 : max];
  }
  return [parseFloat($('scale-min').value), parseFloat($('scale-max').value)];
}

function render() {
  const d = state.data, s = d.scan;
  $('status').textContent = d.adc.simulated ? 'SIMULATED ADC' : `AD7705 gain ${d.adc.gain}, ${d.adc.rate} Hz, LSB ${d.adc.lsb_uv.toFixed(3)} µV`;
  $('adc-info').textContent = `${d.adc.samples} samples per point (+${d.adc.discard} settling)`;
  const sel = $('open-select'); sel.innerHTML = '<option value="">choose…</option>' + d.scans.map((x) => `<option value="${x.id}">${x.error ? x.id + ' (unreadable)' : `${x.name} — ${x.progress[0]}/${x.progress[1]} — ${x.created}`}</option>`).join('');
  if (s) sel.value = s.id;
  setButtons();
  if (!s) { $('next-cell').textContent = '–'; $('progress').textContent = 'no scan open'; drawGrid(null); return; }
  const [r, c] = s.cursor, p = s.config.pitch_mm;
  $('next-cell').textContent = s.complete ? 'scan complete' : `row ${r}, col ${c}  (x ${(c * p).toFixed(1)} mm, y ${(r * p).toFixed(1)} mm)`;
  $('progress').textContent = `${s.progress[0]} / ${s.progress[1]}` + (s.zero ? `  · zero ${s.zero.value_uv.toFixed(2)} µV` : '');
  const last = s.history[s.history.length - 1];
  if (last) { const cell = s.cells[`${last[0]},${last[1]}`]; $('last-value').textContent = `(${last[0]}, ${last[1]}) ${cell.value_uv.toFixed(2)} µV ± ${cell.stdev_uv.toFixed(2)} (median ${cell.median_uv.toFixed(2)})`; }
  else $('last-value').textContent = '–';
  drawGrid(s);
}

function drawGrid(s) {
  const cv = $('heatmap'), ctx = cv.getContext('2d');
  ctx.clearRect(0, 0, cv.width, cv.height);
  if (!s) return;
  const rows = s.config.rows, cols = s.config.cols, grid = currentGrid();
  const cw = cv.width / cols, ch = cv.height / rows, [min, max] = scale(grid);
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const v = grid[r][c];
    ctx.fillStyle = v === null ? '#d9d9d9' : colour((v - min) / (max - min));
    ctx.fillRect(c * cw, r * ch, Math.ceil(cw), Math.ceil(ch));
  }
  ctx.strokeStyle = 'rgba(0,0,0,0.15)'; ctx.lineWidth = 1;
  for (let r = 0; r <= rows; r++) { ctx.beginPath(); ctx.moveTo(0, r * ch); ctx.lineTo(cv.width, r * ch); ctx.stroke(); }
  for (let c = 0; c <= cols; c++) { ctx.beginPath(); ctx.moveTo(c * cw, 0); ctx.lineTo(c * cw, cv.height); ctx.stroke(); }
  const last = s.history[s.history.length - 1];
  if (last) { ctx.strokeStyle = '#000'; ctx.lineWidth = 2; ctx.strokeRect(last[1] * cw + 2, last[0] * ch + 2, cw - 4, ch - 4); }
  if (!s.complete) { const [r, c] = s.cursor; ctx.strokeStyle = '#e60049'; ctx.lineWidth = 3; ctx.strokeRect(c * cw + 1.5, r * ch + 1.5, cw - 3, ch - 3); }
  const lg = $('legend'), lctx = lg.getContext('2d');
  for (let x = 0; x < lg.width; x++) { lctx.fillStyle = colour(x / (lg.width - 1)); lctx.fillRect(x, 0, 1, lg.height); }
  $('scale-min-label').textContent = min.toFixed(2); $('scale-max-label').textContent = max.toFixed(2);
}

function cellAt(ev) {
  const s = state.data && state.data.scan; if (!s) return null;
  const cv = $('heatmap'), rect = cv.getBoundingClientRect();
  const c = Math.floor((ev.clientX - rect.left) / rect.width * s.config.cols), r = Math.floor((ev.clientY - rect.top) / rect.height * s.config.rows);
  return (r >= 0 && r < s.config.rows && c >= 0 && c < s.config.cols) ? [r, c] : null;
}

function downloadPng() {
  const s = state.data.scan; if (!s) return;
  $('heatmap').toBlob((blob) => { const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `${s.id}.png`; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000); });
}

function wire() {
  $('measure-btn').onclick = () => act('POST', '/api/measure', {});
  $('undo-btn').onclick = () => act('POST', '/api/undo', {});
  $('zero-btn').onclick = () => { if (confirm('Pin on the reference contact block? Measure zero now.')) act('POST', '/api/zero', {}); };
  $('zero-clear-btn').onclick = () => act('POST', '/api/zero/clear', {});
  $('calibrate-btn').onclick = async () => { const r = await act('POST', '/api/calibrate', {}); if (r) toast(`calibrated in ${(r.seconds * 1000).toFixed(0)} ms`); };
  $('noise-btn').onclick = async () => { const r = await act('GET', '/api/noise?n=50'); if (r) toast(`noise: mean ${r.mean_uv.toFixed(2)} µV, stdev ${r.stdev_uv.toFixed(2)} µV over ${r.n} samples`); };
  $('new-btn').onclick = () => act('POST', '/api/scan/new', { name: $('new-name').value, rows: +$('new-rows').value, cols: +$('new-cols').value, pitch_mm: +$('new-pitch').value, samples: +$('new-samples').value });
  $('open-select').onchange = (e) => { if (e.target.value) act('POST', '/api/scan/open', { id: e.target.value }); };
  $('png-btn').onclick = downloadPng;
  for (const id of ['relative-toggle', 'scale-auto', 'scale-min', 'scale-max']) $(id).oninput = () => { if (id !== 'scale-auto' && id !== 'relative-toggle') $('scale-auto').checked = false; render(); };
  const cv = $('heatmap');
  cv.onmousemove = (ev) => { const rc = cellAt(ev); const s = state.data.scan; if (!rc) return; const v = currentGrid()[rc[0]][rc[1]]; const p = s.config.pitch_mm; $('hover').textContent = `row ${rc[0]}, col ${rc[1]} · x ${(rc[1] * p).toFixed(1)} mm, y ${(rc[0] * p).toFixed(1)} mm · ${v === null ? 'not measured' : v.toFixed(2) + ' µV'}`; };
  cv.onmouseleave = () => { $('hover').textContent = ''; };
  cv.onclick = (ev) => { const rc = cellAt(ev); if (rc && confirm(`Jump to row ${rc[0]}, col ${rc[1]}?`)) act('POST', '/api/goto', { row: rc[0], col: rc[1] }); };
  document.addEventListener('keydown', (ev) => {
    if (ev.target.tagName === 'INPUT' || ev.target.tagName === 'SELECT') return;
    if (ev.code === 'Space' || ev.code === 'Enter') { ev.preventDefault(); $('measure-btn').click(); }
    if (ev.key === 'u' || ev.key === 'U') $('undo-btn').click();
  });
  refresh(); setInterval(() => { if (!state.busy) refresh(); }, 3000);
}
document.addEventListener('DOMContentLoaded', wire);
```

- [ ] **Step 5: Write `style.css`** — system font, two-column layout (`main { display: grid; grid-template-columns: minmax(300px, 640px) 320px; gap: 24px }`, stacking to one column below 900 px), canvas `width: 100%; aspect-ratio: 1; image-rendering: pixelated`, the big button `min-height: 72px; font-size: 1.4rem`, disabled state greyed, `.toast` fixed bottom centre with `.error` red, `.hover` monospace, `kbd` styled small. No colours that fight the heatmap (neutral greys, one accent for the cursor `#e60049`).

- [ ] **Step 6: Run the test** — `python3 -m pytest tests/test_static.py -v` — Expected: 1 passed
- [ ] **Step 7: Run the full suite** — Expected: all passed
- [ ] **Step 8: Manual smoke** — `python3 -m pogoscan.server --simulate --port 8090 --data-dir /tmp/pogoscan-data` then open `http://127.0.0.1:8090/`, start a 5×5 scan, press Space 5 times, verify the heatmap fills, hover shows values, CSV and PNG download; stop the server.

---

### Task 9: `deploy.sh`, README

**Files:**
- Create: `deploy.sh`
- Modify: `README.md`

- [ ] **Step 1: Write `deploy.sh`**

```bash
#!/usr/bin/env bash
# Copy pogoscan to the Raspberry Pi. Usage: ./deploy.sh [pi@host]
set -euo pipefail
TARGET="${1:-pi@10.16.226.244}"
cd "$(dirname "$0")"
rsync -a --delete --exclude data --exclude __pycache__ --exclude .pytest_cache --exclude '*.pyc' ./ "$TARGET:~/pogoscan/"
echo "deployed to $TARGET:~/pogoscan"
echo "check wiring : ssh $TARGET 'cd ~/pogoscan && python3 -m pogoscan.check'"
echo "run server   : ssh $TARGET 'cd ~/pogoscan && python3 -m pogoscan.server'"
echo "simulate     : ssh $TARGET 'cd ~/pogoscan && python3 -m pogoscan.server --simulate'"
echo "then open    : http://${TARGET#*@}:8080/"
```

`chmod +x deploy.sh`.

- [ ] **Step 2: Write README.md** with: purpose (two sentences), wiring table (from spec §2), measurement settings (spec §3), `python3 -m pytest`, `python3 -m pogoscan.check`, `python3 -m pogoscan.server [--simulate]`, the API table (spec §5.4), the data layout (`data/<id>/scan.json`, CSV columns), and the known limitation (AD7705 noise ≈0.6 µV rms, drift 0.1 µV/°C; the fixture's thermal EMF dominates).

- [ ] **Step 3: Run the full suite** — Expected: all passed

---

## Self-review

- **Spec coverage:** §5.1 → Tasks 1–3; §5.2 → 4; §5.3 → 5; §5.4 → 6; §5.5 → 8; §5.6 → 7; §5.7 error handling → driver exceptions (2), atomic save + unreadable listing (5), API error mapping (6), page re-reads state after every action (8); §6 testing → each task; §7 → 9.
- **Type consistency:** `record(row, col, PointResult)`, `to_dict()["grid"]`, `cursor` as `[row, col]`, `progress` as `[m, total]` in JSON and `(m, total)` in Python, `lsb_volts` property, `read_codes(n)` are used identically in Tasks 4–8. `App.samples` is updated by `new_scan`/`open_scan` and reported in `state.adc.samples` (test in Task 6 checks `20`).
- **Placeholders:** none; every step has runnable content. The only deferred item is the dataviz-skill colour choice in Task 8, which the implementer applies on top of the working code above.
