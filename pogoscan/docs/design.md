# pogoscan — manual 21×21 potential map with an AD7705 on a Raspberry Pi 5

**Date:** 2026-09-17 · **Status:** approved in chat (design presented and accepted) · **Path:** architectural (new project)

## 1. Purpose

Lab tool for the SCP contact-cell prototype. One measuring pogo pin is pressed by hand onto a steel plate at 21×21 positions on a 3 mm pitch (60 mm × 60 mm). A fixed reference contact on the plate is the second input. For every position the operator clicks **Measure** in a web page served by the Pi; the Pi reads the AD7705/TM7705 module (HW-146) over SPI0, averages a burst of samples, stores the result and updates a heatmap in the browser. At the end the operator downloads the heatmap (PNG) and the data (CSV/JSON).

Non-goals: automation of probe motion, multi-channel scanning, sub-0.1 µV accuracy (the AD7705 cannot deliver it; see `SCP papers/10 - … .md` §12), user accounts, any JavaScript framework.

## 2. Hardware facts (verified 2026-09-17 on the Pi over SSH)

| Item | Value |
|---|---|
| Host | Raspberry Pi 5 Model B, Debian 13 (trixie), kernel 6.18, Python 3.13.5, user `pi` in groups `spi`, `gpio` |
| Installed | `python3-spidev` 3.6, `python3-gpiozero` 2.0.1, `python3-lgpio` 0.2.2. **No numpy, no Flask.** |
| SPI0 | enabled at runtime and persisted (`dtparam=spi=on` appended to `/boot/firmware/config.txt`, backup kept); `/dev/spidev0.0` present |
| Wiring (user) | RST=GPIO24 (white), DRDY=GPIO25 (yellow), CS=CE0/GPIO8 (purple), DIN=MOSI/GPIO10 (blue), DOUT=MISO/GPIO9 (orange), SCK=SCLK/GPIO11 (green) |
| Module | HW-146, TM7705 clone of AD7705, **4.9152 MHz crystal** → driver sets CLKDIV=1, CLK=1 → 50/60/250/500 Hz |
| Analog | ADC powered at 5 V from a separate supply; AIN1(+) = moving pin, AIN1(−) = fixed reference contact; reference contact also wired once to module GND |
| Probe result | First probe: writes worked (DRDY 50.0 Hz) but reads returned zeros, GPIO9 electrically open. After the user added a 5 V→3.3 V level shifter on DOUT/DRDY and restored the ADC supply, `python3 -m pogoscan.check` reports PASS: clock 0x0C and setup 0x38 read back, self-calibration 181 ms, DRDY 50.5 Hz, 100-sample burst stdev 0.53–0.62 µV (datasheet: 0.6 µV rms). |
| SPI mode | Mode 3 (SCLK idles high, DIN sampled on rising edge, DOUT valid after falling edge), ≤ 500 kHz |

## 3. Measurement method

- AD7705 channel AIN1 (CH1 CH0 = 00), **gain 128, bipolar, unbuffered, 50 Hz** update rate, Vref 2.5 V (module reference). Full scale ±19.53 mV, LSB = 0.596 µV.
- Self-calibration (MD = 01) once when a scan is created or on demand; the driver waits for DRDY and verifies the mode bits cleared.
- Per click: read `discard + n` conversions (default 4 + 100 = 2.08 s at 50 Hz), drop the first `discard` (filter settling is 4 × 1/rate after any change), convert the rest to µV and compute:
  - `value_uv` = **trimmed mean** (drop 10 % of samples at each end) — primary value; averaging with ~1 LSB rms of noise gives sub-LSB resolution, a median would stay quantised to 0.6 µV steps
  - `median_uv`, `mean_uv`, `stdev_uv`, `min_uv`, `max_uv`, `n_kept`, raw `codes` (kept for re-analysis)
- Optional **zero**: a measurement taken with the moving pin on the reference contact block; the page shows `value − zero` when a zero exists; raw values are always stored.
- Every completed point is written to disk immediately (atomic replace), so a crash or browser reload loses nothing.

## 4. Architecture

```
pogoscan/                      (new directory in /home/projects/pogopin; deployed to ~/pogoscan on the Pi)
├── pogoscan/
│   ├── __init__.py
│   ├── ad7705.py              register encoding, AD7705 driver, SimulatedAD7705, exceptions
│   ├── measure.py             trimmed_mean, PointResult, measure_point
│   ├── scan.py                ScanConfig, Scan (grid state, cursor, undo, persistence, CSV)
│   ├── server.py              stdlib ThreadingHTTPServer + JSON API + static files; python -m pogoscan.server
│   ├── check.py               hardware self-test CLI; python -m pogoscan.check
│   └── static/index.html, app.js, style.css   vanilla page: heatmap canvas, Measure button, controls
├── tests/                     pytest; fakes.py holds FakeSpi/FakeDrdy/FakeReset
├── data/                      scans (runtime, one directory per scan)
├── deploy.sh                  rsync to pi@10.16.226.244:~/pogoscan
├── pytest.ini, README.md
```

Dependencies: Python ≥ 3.11 standard library; `spidev` and `gpiozero` imported **lazily inside `AD7705.__init__`** so that tests and `--simulate` run on machines without them.

## 5. Contracts

### 5.1 `pogoscan/ad7705.py`

```python
REG_COMM, REG_SETUP, REG_CLOCK, REG_DATA, REG_TEST, REG_OFFSET, REG_GAIN = 0, 1, 2, 3, 4, 6, 7
MODE_NORMAL, MODE_SELF_CAL, MODE_ZS_CAL, MODE_FS_CAL = 0, 1, 2, 3
GAIN_CODES = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7}

def comm_byte(reg: int, read: bool, channel: int = 0, standby: bool = False) -> int
    # bit7 0/DRDY=0 | bits6-4 RS2..RS0=reg | bit3 R/W (1=read) | bit2 STBY | bits1-0 CH1 CH0
def setup_byte(mode: int, gain: int, bipolar: bool = True, buffered: bool = False, fsync: bool = False) -> int
    # bits7-6 MD | bits5-3 G2..G0 | bit2 B/U (0 = bipolar) | bit1 BUF | bit0 FSYNC
def clock_byte(crystal_hz: float, rate_hz: int, clkdis: bool = False) -> int
    # bits7-5 = 0 | bit4 CLKDIS | bit3 CLKDIV (1 when crystal is 4.9152 or 2 MHz) | bit2 CLK (1 for 2.4576 MHz effective, 0 for 1 MHz effective)
    # bits1-0 FS: CLK=1 → {50:0, 60:1, 250:2, 500:3}; CLK=0 → {20:0, 25:1, 100:2, 200:3}; ValueError otherwise
def code_to_volts(code: int, vref: float = 2.5, gain: int = 128, bipolar: bool = True) -> float
    # bipolar: (code - 32768) / 32768 * vref / gain ; unipolar: code / 65536 * vref / gain

class AD7705Error(Exception); class AD7705Timeout(AD7705Error)

class AD7705:
    def __init__(self, spi=None, drdy=None, reset=None, *, bus=0, device=0, drdy_pin=25, reset_pin=24,
                 crystal_hz=4.9152e6, vref=2.5, spi_hz=500_000)
        # spi: any object with xfer2(list[int]) -> list[int]; default spidev.SpiDev(bus, device) mode 3
        # drdy: object with .is_active (True when the pin is LOW); default gpiozero DigitalInputDevice(drdy_pin, pull_up=None, active_state=False)
        # reset: object with on()/off(); default gpiozero DigitalOutputDevice(reset_pin, initial_value=True); None = no reset line
    channel: int; gain: int; rate: int; bipolar: bool; buffered: bool; vref: float; crystal_hz: float
    simulated: bool = False
    def reset(self) -> None                       # reset pulse (off 1 ms, on, 10 ms) if reset present; then 4×0xFF (32 ones); 10 ms
    def write_register(self, reg: int, value: int, nbytes: int = 1, channel: int | None = None) -> None
    def read_register(self, reg: int, nbytes: int = 1, channel: int | None = None) -> int
    def configure(self, *, rate=50, gain=128, bipolar=True, buffered=False, channel=0) -> None
        # write clock, verify read-back; write setup (MODE_NORMAL, fsync=False), verify read-back; else AD7705Error("register read-back mismatch …")
    def self_calibrate(self, timeout: float = 2.0) -> float   # writes setup with MODE_SELF_CAL, waits DRDY low, verifies MD bits == 0, returns seconds taken
    def wait_drdy(self, timeout: float = 1.0) -> None          # poll drdy.is_active every 0.2 ms; AD7705Timeout
    def read_code(self, timeout: float = 1.0) -> int           # wait_drdy + read REG_DATA 2 bytes → 0..65535
    def read_codes(self, n: int, timeout: float = 1.0) -> list[int]
    @property
    def lsb_volts(self) -> float                                # vref/gain/32768 (bipolar) or /65536
    def volts(self, code: int) -> float ; def microvolts(self, code: int) -> float
    def close(self) -> None

class SimulatedAD7705:  # same public surface as AD7705 (reset, configure, self_calibrate, wait_drdy, read_code, read_codes, lsb_volts, volts, microvolts, close, attributes)
    simulated = True
    def __init__(self, *, rate=50, gain=128, vref=2.5, noise_uv=0.6, seed=0, realtime=False)
    source_volts: float          # differential input the simulator converts; set by the caller
    drift_uv_per_s: float = 0.02 # slow random-walk drift added to the input
    # read_code: code = clip(round((source_volts + drift + N(0, noise)) / lsb_volts) + 32768, 0, 65535); sleeps 1/rate when realtime
```

### 5.2 `pogoscan/measure.py`

```python
@dataclass
class PointResult:
    value_uv: float; median_uv: float; mean_uv: float; stdev_uv: float; min_uv: float; max_uv: float
    n_total: int; n_kept: int; discarded: int; codes: list[int]; duration_s: float; timestamp: str  # ISO 8601 UTC, seconds
    def to_dict(self) -> dict ; @classmethod from_dict(cls, d) -> "PointResult"
def trimmed_mean(values: list[float], trim: float = 0.1) -> float   # sort; drop int(trim*n) from each end; n<3 → plain mean; empty → ValueError
def measure_point(adc, n: int = 100, discard: int = 4, trim: float = 0.1) -> PointResult
    # codes = adc.read_codes(n + discard); kept = codes[discard:]; stats via statistics module; stdev = pstdev
```

### 5.3 `pogoscan/scan.py`

```python
@dataclass
class ScanConfig: name: str; rows: int = 21; cols: int = 21; pitch_mm: float = 3.0; samples: int = 100; discard: int = 4; gain: int = 128; rate: int = 50; created: str = ""
class Scan:
    id: str                 # directory name: <slug(name)>-<YYYYmmdd-HHMMSS>
    path: Path              # …/data/<id>/scan.json
    config: ScanConfig
    cells: dict[str, dict]  # "r,c" → PointResult.to_dict() + {"row": r, "col": c}
    history: list[list[int]]# [row, col] in the order recorded (undo stack)
    cursor: list[int]       # [row, col] next to measure
    zero: dict | None       # PointResult.to_dict() of the zero measurement
    def record(self, row, col, result: PointResult) -> None      # store, push history, cursor = next unmeasured cell after (row, col) row-major (wraps to first unmeasured), save
    def undo(self) -> list[int] | None                           # pop history, delete cell, cursor = that cell, save; None if nothing to undo
    def goto(self, row, col) -> None                             # bounds-checked, save
    def set_zero(self, result: PointResult | None) -> None       # save
    def zero_uv(self) -> float | None
    def progress(self) -> tuple[int, int]                        # (measured, rows*cols)
    def complete(self) -> bool
    def grid(self, relative: bool = True) -> list[list[float | None]]   # value_uv minus zero when relative and zero set
    def to_dict(self) -> dict     # {"id", "config", "cells", "history", "cursor", "zero", "progress": [m, total], "complete": bool, "grid": grid(True), "grid_raw": grid(False)}
    def save(self) -> None        # json to path.tmp then os.replace
    @classmethod load(cls, path: Path) -> "Scan"
    def to_csv(self) -> str       # header row,col,x_mm,y_mm,value_uv,rel_uv,median_uv,mean_uv,stdev_uv,min_uv,max_uv,n_kept,timestamp ; x_mm = col*pitch, y_mm = row*pitch; unmeasured cells omitted
def new_scan(data_dir: Path, config: ScanConfig) -> Scan
def list_scans(data_dir: Path) -> list[dict]      # [{"id", "name", "created", "progress": [m, total]}] newest first
def open_scan(data_dir: Path, scan_id: str) -> Scan
```

### 5.4 `pogoscan/server.py` — HTTP/JSON API

`python -m pogoscan.server [--host 0.0.0.0] [--port 8080] [--data-dir data] [--simulate] [--crystal 4.9152e6] [--drdy 25] [--reset 24] [--bus 0] [--device 0]`

All responses are JSON except `/`, `/static/*`, `/api/export.csv`. Errors: `{"error": "<message>"}` with 400 (bad request / no scan / complete), 404 (unknown scan), 409 (busy: a measurement is running), 500 (ADC error, message included). One `threading.Lock` guards the ADC; a second request during a measurement gets 409 immediately. `ThreadingHTTPServer`, `allow_reuse_address = True`.

| Method & path | Body | Response |
|---|---|---|
| GET `/` | | `static/index.html` |
| GET `/static/<file>` | | file (`text/html`, `text/css`, `application/javascript`) |
| GET `/api/state` | | `{"scan": Scan.to_dict() or null, "measuring": bool, "adc": {"simulated": bool, "gain": 128, "rate": 50, "lsb_uv": 0.596, "samples": n, "discard": d}, "scans": list_scans()}` |
| POST `/api/scan/new` | `{"name": str, "rows": 21, "cols": 21, "pitch_mm": 3.0, "samples": 100}` | state; also runs `configure()` + `self_calibrate()` |
| POST `/api/scan/open` | `{"id": str}` | state |
| POST `/api/measure` | `{}` | `{"cell": {...PointResult, "row", "col"}, "scan": Scan.to_dict()}` — measures the cursor cell |
| POST `/api/undo` | `{}` | state |
| POST `/api/goto` | `{"row": r, "col": c}` | state |
| POST `/api/zero` | `{}` | state (measures with the same n/discard and stores as zero) |
| POST `/api/zero/clear` | `{}` | state |
| POST `/api/calibrate` | `{}` | `{"ok": true, "seconds": t}` |
| GET `/api/noise?n=50` | | `{"mean_uv", "stdev_uv", "min_uv", "max_uv", "n"}` quick burst without recording |
| GET `/api/export.csv` | | `text/csv`, `Content-Disposition: attachment; filename="<id>.csv"` |
| GET `/api/export.json` | | the scan file |

Simulation (`--simulate`): `SimulatedAD7705(realtime=False)`; before each measurement the server sets `adc.source_volts = plate_uv(row, col) * 1e-6` where `plate_uv(r, c) = 1.0 * c / (cols - 1) + 5.0 * exp(-((r - 10) ** 2) / 2.0) + 3.0 * exp(-(((r - 4) ** 2 + (c - 15) ** 2)) / 8.0)` (gradient + weld band at row 10 + a hot spot). Zero uses `source_volts = 0`.

### 5.5 Web page (`static/`)

Single page, vanilla JS, no build step, no external resources (works offline on the lab network).

- **Heatmap**: `<canvas>` grid rows × cols (row 0 at top, col 0 at left), cell colour from a sequential colour LUT over [min, max] of the shown values (auto by default; manual min/max inputs), unmeasured cells grey, the cursor cell outlined, the last measured cell marked. Legend bar with min/max labels and unit µV. Hover shows `row, col, x mm, y mm, value`. Clicking a cell asks "Jump here?" and calls `/api/goto`.
- **Controls**: big **Measure** button (also Space or Enter), Undo (U), Zero, Clear zero, Calibrate, Noise check (shows mean/stdev), New scan (name/rows/cols/pitch/samples), Open scan (list), Download CSV, Download JSON, Download PNG (canvas → blob → `<a download>`), toggle "relative to zero".
- **Status**: next cell `row/col` and `x/y mm`, progress `m / total`, last value ± stdev in µV, measuring spinner, complete banner, error toast. State refreshed after each action and every 3 s.
- The **dataviz** skill governs the colour map and legend; the page must stay usable at 1024 px width and on a phone in landscape.

### 5.6 `pogoscan/check.py`

`python -m pogoscan.check [--crystal 4.9152e6] [--drdy 25] [--reset 24] [--bus 0] [--device 0]` prints a report and exits 0 on PASS, 1 on FAIL:

1. `/dev/spidev<bus>.<device>` exists (hint: `dtparam=spi=on` in `/boot/firmware/config.txt`, reboot)
2. reset; write clock register, read back — PASS/FAIL (hint on FAIL with read-back 0x00: "DOUT→MISO (GPIO9) open: check the orange wire and its level shifter")
3. write setup register, read back
4. self-calibration time (ms) and setup read-back == normal mode
5. DRDY rate over 2 s vs expected (50 Hz)
6. 100-sample burst: mean, stdev, min, max in µV; warning if stdev == 0 (stuck) or > 5 µV

### 5.7 Error handling

- Driver: register read-back mismatch → `AD7705Error`; DRDY timeout → `AD7705Timeout`. The server converts these into `{"error": …}` 500 and leaves the scan state untouched.
- Scan persistence is atomic; `load()` of a truncated file raises and the server reports it in `list_scans()` as `{"id", "error"}`.
- The page never assumes a request succeeded: it re-reads `/api/state` after every action.

## 6. Testing

- `pytest` at the project root on the dev box (Python 3.13, no spidev/gpiozero): `tests/fakes.py` provides `FakeSpi` (emulates the comm-register protocol: keeps a register dict, logs transfers, returns register bytes on reads, DRDY-driven data), `FakeDrdy(is_active)`, `FakeReset` (records pulses).
- Unit tests for every function in §5.1–5.3; server tests start `ThreadingHTTPServer` on port 0 with the simulator and exercise every endpoint with `http.client`; a static smoke test checks `index.html` references `app.js`/`style.css` and contains the control ids `measure-btn`, `undo-btn`, `zero-btn`, `heatmap`, `status`.
- Browser check (by the integrator, not automated in pytest): run `python -m pogoscan.server --simulate`, open the page with the Playwright MCP tools, click Measure 5 times, verify the heatmap fills and the CSV downloads.
- Hardware check: `python -m pogoscan.check` on the Pi after the DOUT wire is fixed; then a real scan of a few cells.

## 7. Deployment

`deploy.sh` runs `rsync -a --delete --exclude data --exclude __pycache__ --exclude .pytest_cache ./ pi@10.16.226.244:~/pogoscan/` and prints the run commands. Run on the Pi: `cd ~/pogoscan && python3 -m pogoscan.server` then open `http://10.16.226.244:8080/`. No systemd unit in this version.
