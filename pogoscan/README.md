# pogoscan

Manual 21×21 potential map with an AD7705/TM7705 16-bit ADC module (HW-146) on a Raspberry Pi 5.
One pogo pin is pressed by hand onto a steel plate every 3 mm; each click on **Measure** in the web page
records an averaged burst from the ADC and updates a heatmap. Design: `docs/design.md`, implementation plan: `docs/implementation-plan.md`.

## Wiring (Pi 5 header, BCM numbers)

| Module pin | Pi | Note |
|---|---|---|
| SCK | GPIO11 (SCLK, pin 23) | SPI mode 3, 500 kHz |
| DIN | GPIO10 (MOSI, pin 19) | Pi 3.3 V drives the 5 V chip fine (VIH 2.0 V) |
| DOUT | GPIO9 (MISO, pin 21) | **5 V output: needs a level shifter or divider** (e.g. 1.8 kΩ series, 3.3 kΩ to GND) |
| DRDY | GPIO25 (pin 22) | 5 V output: same level shifting |
| CS | GPIO8 (CE0, pin 24) | |
| RST | GPIO24 (pin 18) | |
| GND | GND (pin 20/25) | one ground wire; the plate's reference contact goes to module GND once |
| VCC | separate 5 V supply | 4.75–5.25 V; not the Pi's 3.3 V (reference 2.5 V would be out of spec) |

Enable SPI once: `dtparam=spi=on` in `/boot/firmware/config.txt` (already done on the lab Pi).

## Measurement settings

Channel AIN1 differential (AIN1+ = moving pin, AIN1− = fixed reference contact), gain 128, bipolar, unbuffered,
50 Hz (4.9152 MHz crystal → CLKDIV=1), Vref 2.5 V → full scale ±19.5 mV, LSB 0.596 µV. Per click: 4 settling
conversions discarded, then 100 conversions; the stored value is the 10 %-trimmed mean, with median, mean, stdev,
min, max and raw codes kept. Self-calibration runs when a scan is created and on demand. An optional **Zero**
measurement (pin on the reference block) is subtracted for display; raw values are always stored.

Limits: AD7705 noise ≈ 0.6 µV rms per conversion (≈ 0.06 µV after averaging 100), offset drift ≈ 0.1 µV/°C;
the pogo-pin fixture's thermal EMF (BeCu ≈ 5 µV/°C vs copper) dominates. Keep the plate and pins isothermal.

## Run

```bash
python3 -m pytest                       # on the dev box or the Pi
python3 -m pogoscan.check               # on the Pi: wiring self-test (register read-back, DRDY rate, noise)
python3 -m pogoscan.server              # on the Pi: http://<pi>:8080/
python3 -m pogoscan.server --simulate   # anywhere: simulated ADC with a synthetic plate
./deploy.sh                             # rsync to pi@10.16.226.244:~/pogoscan
```

Options: `--port 8080 --data-dir data --samples 100 --discard 4 --crystal 4.9152e6 --drdy 25 --reset 24 --bus 0 --device 0`.

## Service (starts at boot)

`pogoscan.service` runs the server as user `pi` from `/home/pi/pogoscan` on port 8080 and restarts it every 5 s
while the ADC supply is off (the server exits with status 1 until the registers read back). Install once:

```bash
./deploy.sh pi@10.16.226.244 --service      # copies the code, installs and enables the unit
sudo systemctl status pogoscan               # on the Pi
journalctl -u pogoscan -f                    # live log
sudo systemctl stop pogoscan                 # before running pogoscan.check or --simulate by hand (they need the SPI/GPIO)
```

Later deploys (`./deploy.sh`) restart the service automatically.

## Page

Measure (Space/Enter), Undo (U), Zero / Clear zero, Calibrate, Noise check, Re-init ADC, New scan, Open scan,
CSV / JSON / PNG download, auto or manual colour scale, relative-to-zero toggle, hover for cell values, click a cell to
jump to it, and an ADC status block (live register check, re-init count, last error).

- **Noise check**: 50 conversions (1 s) from whatever the pin touches, nothing recorded; reports mean and scatter. About
  0.6 µV scatter is the chip's own noise; more means pickup or a poor contact; 0 means a stuck line.
- **Calibrate**: AD7705 self-calibration (inputs shorted internally, zero and full-scale corrections stored in the chip,
  about 0.2 s). Removes errors inside the chip only (drift ≈ 0.1 µV/°C). Runs automatically on new/open scan and after re-init.
- **Zero**: pin on the reference contact block, one measurement stored and subtracted from the display. Removes offsets
  outside the chip (thermal EMF of pins, wires, connectors). Raw values are always kept.
- **Re-init ADC**: hardware reset, reprogramming and self-calibration; the server does it automatically after a supply
  blink or a DRDY timeout.

## API

| Method & path | Body | Response |
|---|---|---|
| GET `/api/state` | | `{scan, measuring, adc:{simulated,gain,rate,lsb_uv,samples,discard}, scans}` |
| POST `/api/scan/new` | `{name, rows, cols, pitch_mm, samples}` | state (configures + self-calibrates the ADC) |
| POST `/api/scan/open` | `{id}` | state |
| POST `/api/measure` | `{}` | `{cell, scan}` — measures the cursor cell |
| POST `/api/undo`, `/api/goto {row,col}`, `/api/zero`, `/api/zero/clear` | | state |
| POST `/api/calibrate` | `{}` | `{ok, seconds}` |
| POST `/api/adc/reinit` | `{}` | `{ok, seconds}` — reset, configure and self-calibrate the ADC by hand |
| GET `/api/noise?n=50` | | `{n, mean_uv, stdev_uv, min_uv, max_uv}` |
| GET `/api/export.csv`, `/api/export.json` | | downloads |

Errors are `{"error": msg}` with 400 (bad request / no scan / complete), 404, 409 (measurement in progress), 500 (ADC).

`state.adc.status` is the live ADC health shown in the page's ADC block: `level` (ok / warn / error / info), `message`,
the `clock` and `setup` register bytes read between measurements (0x0C / 0x38 expected; 0x05 / 0x01 means the chip was
reset by a supply blink; 0x00 or 0xFF means no response), `configured`, `checked_at`, `busy`, and the event counters
`reinits`, `last_reinit`, `calibrations`, `last_calibration`, `last_measure`, `last_noise`, `last_error`, `last_error_time`.
The server re-initialises the ADC automatically before a measurement when the registers are back at defaults, and once
more after a DRDY timeout; both events are logged to the journal.

## Data

`data/<name>-<timestamp>/scan.json` is rewritten atomically after every point. CSV columns:
`row,col,x_mm,y_mm,value_uv,rel_uv,median_uv,mean_uv,stdev_uv,min_uv,max_uv,n_kept,timestamp` (x = col·pitch, y = row·pitch).
