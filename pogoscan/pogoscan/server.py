"""Stdlib HTTP server: JSON API for the scan plus the static page. Run: python3 -m pogoscan.server [--simulate]."""
from __future__ import annotations

import argparse
import json
import math
import mimetypes
import signal
import statistics
import sys
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from .ad7705 import AD7705, AD7705Error, AD7705Timeout, SimulatedAD7705
from .measure import measure_point
from .scan import Scan, ScanConfig, list_scans, new_scan, open_scan

STATIC_DIR = Path(__file__).parent / "static"
CONTENT_TYPES = {".html": "text/html; charset=utf-8", ".js": "application/javascript; charset=utf-8", ".css": "text/css; charset=utf-8"}
MAX_GRID_SIDE = 500          # rows/cols sanity limit for /api/scan/new
MAX_SAMPLES = 10_000         # samples per point sanity limit (10 000 at 50 Hz = 200 s per click)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def log(message: str) -> None:
    """One line on stderr (the systemd journal) with a timestamp."""
    print(time.strftime("%Y-%m-%d %H:%M:%S"), message, file=sys.stderr, flush=True)


def plate_uv(row: int, col: int, rows: int, cols: int) -> float:
    """Synthetic plate for --simulate: gradient along columns, weld band at row 10, hot spot at (4, 15)."""
    gradient = 1.0 * col / max(cols - 1, 1)
    weld = 5.0 * math.exp(-((row - 10) ** 2) / 2.0)
    spot = 3.0 * math.exp(-(((row - 4) ** 2 + (col - 15) ** 2)) / 8.0)
    return gradient + weld + spot


class Busy(Exception):
    """A measurement is running on the ADC (HTTP 409)."""


class App:
    """Application state shared by all request threads.

    `lock` is held for the whole duration of any ADC access (measure, zero, noise, calibrate, new scan);
    a request that needs the ADC while it is held gets `Busy` immediately instead of queueing.
    `state_lock` (re-entrant) guards every read or mutation of `scan`, so a state snapshot taken by a
    polling GET never sees a half-updated scan.
    """

    def __init__(self, adc, data_dir: Path, samples: int = 100, discard: int = 4):
        self.adc, self.data_dir, self.samples, self.discard = adc, Path(data_dir), samples, discard
        self.lock = threading.Lock()
        self.state_lock = threading.RLock()
        self.measuring = False
        self.scan: Scan | None = None
        self.events = {"started": _now(), "reinits": 0, "last_reinit": None, "calibrations": 0, "last_calibration": None,
                       "last_measure": None, "last_noise": None, "last_error": None, "last_error_time": None}
        self._last_live: dict = {}

    # -- state --------------------------------------------------------------
    def state(self) -> dict:
        with self.state_lock:
            scan = self.scan.to_dict(include_codes=False) if self.scan else None   # polled every 3 s: keep it small
        return {"scan": scan, "measuring": self.measuring,
                "adc": {"simulated": bool(getattr(self.adc, "simulated", False)), "gain": self.adc.gain, "rate": self.adc.rate,
                        "lsb_uv": self.adc.lsb_volts * 1e6, "samples": self.samples, "discard": self.discard,
                        "status": self.adc_status()},
                "scans": list_scans(self.data_dir)}

    def _acquire(self) -> None:
        if not self.lock.acquire(timeout=0.1):      # a status read holds the lock for a few ms; a measurement for seconds
            raise Busy("a measurement is already running")
        self.measuring = True

    def _release(self) -> None:
        self.measuring = False
        self.lock.release()

    def require_scan(self) -> Scan:
        if self.scan is None:
            raise ValueError("no scan open")
        return self.scan

    # -- ADC health ---------------------------------------------------------
    def _note_reinit(self) -> None:
        self.events["reinits"] += 1
        self.events["last_reinit"] = _now()

    def record_error(self, message: str) -> None:
        self.events["last_error"], self.events["last_error_time"] = message, _now()

    def adc_status(self) -> dict:
        """Live ADC health for the page. Registers are read only when no measurement holds the ADC lock."""
        live = None
        if self.lock.acquire(blocking=False):
            try:
                live = self.adc.read_status()
                self._last_live = {**live, "checked_at": _now()}
            except AD7705Error as e:
                self._last_live = {"error": str(e), "checked_at": _now()}
            finally:
                self.lock.release()
        st = dict(self._last_live)
        level, message = self._describe(st, busy=live is None)
        return {"level": level, "message": message, "busy": live is None, **st, **self.events}

    def _describe(self, st: dict, busy: bool) -> tuple[str, str]:
        def hx(v):
            return f"0x{v:02X}" if isinstance(v, int) else "–"
        if "error" in st:
            level, msg = "error", f"no response: {st['error']}"
        elif not st:
            level, msg = "info", "not checked yet"
        elif st.get("configured"):
            level, msg = "ok", f"responding and configured (gain {self.adc.gain}, {self.adc.rate} Hz)"
        else:
            clock, setup = st.get("clock"), st.get("setup")
            if clock == 0x05 and setup == 0x01:
                level, msg = "warn", "registers at power-on defaults (supply blinked or RESET pulsed); re-initialises on the next measurement"
            elif clock in (0x00, 0xFF) and setup in (0x00, 0xFF):
                level, msg = "error", f"no response (clock {hx(clock)}, setup {hx(setup)}): check the 5 V supply, the level shifter and the DOUT wire"
            else:
                level, msg = "warn", f"unexpected registers (clock {hx(clock)}, setup {hx(setup)}); re-initialises on the next measurement"
        if busy:
            msg += " · last check before the current measurement"
        return level, msg

    def reinit(self) -> float:
        """Operator-requested reset + configure + self-calibration."""
        self._acquire()
        try:
            seconds = self.adc.initialize()
            self._note_reinit()
            self.events["calibrations"] += 1
            self.events["last_calibration"] = _now()
            return seconds
        finally:
            self._release()

    def _ensure_ready(self) -> None:
        """Re-initialise the ADC if its registers are back at power-on defaults (supply blink or RESET pulse)."""
        is_configured = getattr(self.adc, "is_configured", None)
        if is_configured is not None and not is_configured():
            log("ADC registers at power-on defaults: re-initialising (reset, configure, self-calibrate)")
            self.adc.initialize()
            self._note_reinit()

    def _convert(self, fn):
        """Run one ADC acquisition; after a DRDY timeout re-initialise once and retry."""
        self._ensure_ready()
        try:
            return fn()
        except AD7705Timeout as e:
            log(f"ADC timeout ({e}); re-initialising and retrying once")
            self.adc.initialize()
            self._note_reinit()
            return fn()

    def _set_source(self, row: int | None, col: int | None) -> None:
        """Simulation only: point the simulated ADC at the synthetic plate (or at 0 V for zero/noise)."""
        if getattr(self.adc, "simulated", False):
            cfg = self.scan.config if self.scan else ScanConfig(name="")
            self.adc.source_volts = 0.0 if row is None else plate_uv(row, col, cfg.rows, cfg.cols) * 1e-6

    # -- actions (all raise Busy / ValueError / FileNotFoundError / AD7705Error) --
    def new_scan(self, body: dict) -> None:
        cfg = ScanConfig(name=str(body.get("name") or "scan"), rows=int(body.get("rows", 21)), cols=int(body.get("cols", 21)),
                         pitch_mm=float(body.get("pitch_mm", 3.0)), samples=int(body.get("samples", self.samples)), discard=self.discard,
                         gain=self.adc.gain, rate=self.adc.rate)
        if not (1 <= cfg.rows <= MAX_GRID_SIDE and 1 <= cfg.cols <= MAX_GRID_SIDE):
            raise ValueError(f"rows and cols must be between 1 and {MAX_GRID_SIDE}")
        if not (3 <= cfg.samples <= MAX_SAMPLES):
            raise ValueError(f"samples must be between 3 and {MAX_SAMPLES}")
        if not (0 < cfg.pitch_mm < 1e6):          # also rejects inf and nan
            raise ValueError("pitch_mm must be a positive number below 1e6")
        self._acquire()
        try:
            self.adc.configure(rate=self.adc.rate, gain=self.adc.gain)
            self.adc.self_calibrate()
            scan = new_scan(self.data_dir, cfg)  # may fail (disk); the previous scan and its sample count stay untouched
            with self.state_lock:
                self.scan, self.samples = scan, cfg.samples
        finally:
            self._release()

    def open_scan(self, scan_id: str) -> None:
        self._acquire()                      # never swap the scan under a running measurement
        try:
            scan = open_scan(self.data_dir, scan_id)
            self.adc.self_calibrate()        # fresh coefficients for this session: the ADC may have been reset or drifted since
            with self.state_lock:
                self.scan, self.samples = scan, scan.config.samples
        finally:
            self._release()

    def measure(self) -> dict:
        """Measure the cursor cell; returns the /api/measure payload {"cell": {...}, "scan": Scan.to_dict()}.

        The cursor is read and the response snapshot taken while the ADC lock is held, so a goto or open_scan
        from another request can neither be overridden by this measurement nor leak into its response.
        """
        self._acquire()
        try:
            with self.state_lock:
                scan = self.require_scan()
                if scan.complete() and not scan.targeted:
                    raise ValueError("scan is complete; click a cell (goto) to re-measure it, or undo the last point")
                row, col = scan.cursor
            self._set_source(row, col)
            result = self._convert(lambda: measure_point(self.adc, n=self.samples, discard=self.discard))
            self.events["last_measure"] = result.timestamp
            with self.state_lock:
                scan.record(row, col, result)
                return {"cell": {**result.to_dict(), "row": row, "col": col}, "scan": scan.to_dict()}
        finally:
            self._release()

    def undo(self) -> list[int] | None:
        scan = self.require_scan()
        self._acquire()
        try:
            with self.state_lock:
                return scan.undo()
        finally:
            self._release()

    def goto(self, row: int, col: int) -> None:
        scan = self.require_scan()
        self._acquire()
        try:
            with self.state_lock:
                scan.goto(row, col)
        finally:
            self._release()

    def zero(self) -> None:
        scan = self.require_scan()
        self._acquire()
        try:
            self._set_source(None, None)
            result = self._convert(lambda: measure_point(self.adc, n=self.samples, discard=self.discard))
            with self.state_lock:
                scan.set_zero(result)
        finally:
            self._release()

    def clear_zero(self) -> None:
        scan = self.require_scan()
        self._acquire()
        try:
            with self.state_lock:
                scan.set_zero(None)
        finally:
            self._release()

    def calibrate(self) -> float:
        self._acquire()
        try:
            self._ensure_ready()
            seconds = self.adc.self_calibrate()
            self.events["calibrations"] += 1
            self.events["last_calibration"] = _now()
            return seconds
        finally:
            self._release()

    def noise(self, n: int) -> dict:
        self._acquire()
        try:
            self._set_source(None, None)
            uv = [self.adc.microvolts(c) for c in self._convert(lambda: self.adc.read_codes(n))]
        finally:
            self._release()
        result = {"n": n, "mean_uv": statistics.fmean(uv), "stdev_uv": statistics.pstdev(uv) if n > 1 else 0.0,
                  "min_uv": min(uv), "max_uv": max(uv)}
        self.events["last_noise"] = {**result, "time": _now()}
        return result


class Handler(BaseHTTPRequestHandler):
    app: App  # set by make_server

    def log_message(self, fmt, *args):  # quieter console
        pass

    # -- helpers ------------------------------------------------------------
    def _send(self, status: int, content_type: str, data: bytes, extra: dict[str, str] | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass                                  # client went away (page reload during a measurement): nothing to answer

    def _json(self, status: int, payload) -> None:
        self._send(status, "application/json; charset=utf-8", json.dumps(payload).encode())

    def _error(self, status: int, message: str) -> None:
        self._json(status, {"error": message})

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        if n < 0 or n > 1_000_000:
            raise ValueError("invalid Content-Length")
        raw = self.rfile.read(n) if n else b""
        if not raw:
            return {}
        try:
            body = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise ValueError(f"invalid JSON body: {e}") from e
        if not isinstance(body, dict):
            raise ValueError("JSON body must be an object")
        return body

    def _static(self, name: str) -> None:
        root = STATIC_DIR.resolve()
        target = (root / unquote(name)).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            self._error(404, "not found")
            return
        ctype = CONTENT_TYPES.get(target.suffix) or mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        self._send(200, ctype, target.read_bytes(), {"Cache-Control": "no-cache"})

    def _file(self, content_type: str, data: bytes, filename: str) -> None:
        self._send(200, content_type, data, {"Content-Disposition": f'attachment; filename="{filename}"'})

    def _handle(self, fn) -> None:
        """Run a route, mapping exceptions to the status codes of spec §5.4."""
        try:
            fn()
        except Busy as e:
            self._error(409, str(e))
        except FileNotFoundError as e:
            self._error(404, f"unknown scan {e}")
        except (ValueError, TypeError, KeyError) as e:
            self._error(400, str(e))
        except AD7705Error as e:
            log(f"ADC error on {self.command} {self.path}: {e}")
            self.app.record_error(str(e))
            self._error(500, f"ADC error: {e}")
        except Exception as e:  # noqa: BLE001 - always answer the client, never hang it
            traceback.print_exc(file=sys.stderr)
            self._error(500, f"internal error: {e}")

    # -- routing ------------------------------------------------------------
    def do_GET(self) -> None:
        self._handle(self._get)

    def do_POST(self) -> None:
        self._handle(self._post)

    def _get(self) -> None:
        url = urlparse(self.path)
        app = self.app
        if url.path == "/":
            return self._static("index.html")
        if url.path.startswith("/static/"):
            return self._static(url.path[len("/static/"):])
        if url.path == "/api/state":
            return self._json(200, app.state())
        if url.path == "/api/export.csv":
            with app.state_lock:
                scan = app.require_scan()
                return self._file("text/csv; charset=utf-8", scan.to_csv().encode(), f"{scan.id}.csv")
        if url.path == "/api/export.json":
            with app.state_lock:
                scan = app.require_scan()
                return self._file("application/json", scan.path.read_bytes(), f"{scan.id}.json")
        if url.path == "/api/noise":
            n = max(2, min(1000, int(parse_qs(url.query).get("n", ["50"])[0])))
            return self._json(200, app.noise(n))
        return self._error(404, "not found")

    def _post(self) -> None:
        path = urlparse(self.path).path
        app = self.app
        body = self._body()
        if path == "/api/scan/new":
            app.new_scan(body)
        elif path == "/api/scan/open":
            app.open_scan(str(body.get("id", "")))
        elif path == "/api/measure":
            return self._json(200, app.measure())
        elif path == "/api/undo":
            app.undo()
        elif path == "/api/goto":
            app.goto(int(body.get("row", -1)), int(body.get("col", -1)))
        elif path == "/api/zero":
            app.zero()
        elif path == "/api/zero/clear":
            app.clear_zero()
        elif path == "/api/adc/reinit":
            return self._json(200, {"ok": True, "seconds": app.reinit()})
        elif path == "/api/calibrate":
            return self._json(200, {"ok": True, "seconds": app.calibrate()})
        else:
            return self._error(404, "not found")
        return self._json(200, app.state())


class PogoServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def make_server(app: App, host: str, port: int) -> ThreadingHTTPServer:
    handler = type("BoundHandler", (Handler,), {"app": app})
    return PogoServer((host, port), handler)


def make_adc(args) -> object:
    if args.simulate:
        return SimulatedAD7705(realtime=args.realtime)
    adc = AD7705(bus=args.bus, device=args.device, drdy_pin=args.drdy, reset_pin=args.reset, crystal_hz=args.crystal)
    adc.reset()
    adc.configure(rate=50, gain=128)
    adc.self_calibrate()                 # datasheet: set up the registers *and* calibrate after a reset or a clock/gain change
    return adc


def main(argv=None) -> int:
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
    try:
        adc = make_adc(args)
    except ImportError as e:
        print(f"cannot open the ADC: {e} (install python3-spidev and python3-gpiozero, or use --simulate)", file=sys.stderr)
        return 1
    except AD7705Error as e:
        print(f"ADC error: {e}\nrun `python3 -m pogoscan.check` to diagnose the wiring, or start with --simulate", file=sys.stderr)
        return 1
    app = App(adc, Path(args.data_dir), samples=args.samples, discard=args.discard)
    try:
        srv = make_server(app, args.host, args.port)
    except OSError as e:
        print(f"cannot listen on {args.host}:{args.port}: {e}", file=sys.stderr)
        adc.close()
        return 1
    print(f"pogoscan {'SIMULATED' if getattr(adc, 'simulated', False) else 'AD7705'} on http://{args.host}:{srv.server_address[1]}/  "
          f"data in {app.data_dir.resolve()}", flush=True)

    def _terminate(signum, frame):            # SIGTERM (kill, systemd stop) → same clean exit as Ctrl-C
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, _terminate)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
        adc.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
