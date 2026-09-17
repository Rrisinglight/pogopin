# tests/test_server.py
import argparse
import json
import threading
import http.client
import pytest
from pogoscan import server as server_mod
from pogoscan.server import App, make_server, plate_uv
from pogoscan.ad7705 import AD7705, SimulatedAD7705, REG_SETUP, REG_CLOCK
from tests.fakes import FakeSpi, FakeDrdy, FakeReset


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
    call.app = app
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


# --- review fixes ----------------------------------------------------------------
def test_make_adc_self_calibrates_after_reset(monkeypatch):
    """Datasheet: registers must be set up and a calibration run after RESET and after any clock/gain change."""
    spi = FakeSpi()
    monkeypatch.setattr(server_mod, "AD7705", lambda **kw: AD7705(spi=spi, drdy=FakeDrdy(True), reset=FakeReset()))
    args = argparse.Namespace(simulate=False, realtime=False, bus=0, device=0, drdy=25, reset=24, crystal=4.9152e6)
    adc = server_mod.make_adc(args)
    assert spi.resets == 1 and spi.regs[REG_CLOCK] == 0x0C and spi.regs[REG_SETUP] == 0x38 and adc.gain == 128
    assert spi.selfcals == 1


def test_open_scan_self_calibrates(tmp_path):
    adc = SimulatedAD7705(seed=1)
    app = App(adc=adc, data_dir=tmp_path, samples=5, discard=1)
    app.new_scan({"name": "a", "rows": 1, "cols": 1, "samples": 5})
    assert adc.calibrations == 1
    app.open_scan(app.scan.id)
    assert adc.calibrations == 2
    with pytest.raises(FileNotFoundError):
        app.open_scan("missing")
    assert adc.calibrations == 2                      # an unknown id never touches the ADC


def test_goto_then_measure_re_measures_a_complete_scan(client):
    client("POST", "/api/scan/new", {"name": "Sim", "rows": 2, "cols": 2, "samples": 20})
    for _ in range(4):
        client("POST", "/api/measure", {})
    st, _, data = client("POST", "/api/measure", {})
    assert st == 400 and "complete" in j(data)["error"]        # no cell chosen: still refused
    st, _, _ = client("POST", "/api/goto", {"row": 0, "col": 0}); assert st == 200
    st, _, data = client("POST", "/api/measure", {}); d = j(data)
    assert st == 200 and (d["cell"]["row"], d["cell"]["col"]) == (0, 0)
    assert d["scan"]["complete"] is True and d["scan"]["progress"] == [4, 4] and d["scan"]["cursor"] == [0, 0]
    assert d["scan"]["history"][-1] == [0, 0] and d["scan"]["cells"]["0,0"]["timestamp"] == d["cell"]["timestamp"]
    st, _, _ = client("POST", "/api/measure", {}); assert st == 400   # the chosen cell was consumed
    st, _, _ = client("POST", "/api/goto", {"row": 1, "col": 1}); assert st == 200
    st, _, data = client("POST", "/api/undo", {}); assert st == 200 and j(data)["scan"]["cursor"] == [0, 0]
    st, _, _ = client("POST", "/api/measure", {}); assert st == 200  # incomplete again: normal measuring


def test_new_scan_with_a_very_long_name_is_accepted(client):
    st, _, data = client("POST", "/api/scan/new", {"name": "x" * 300, "rows": 1, "cols": 1, "samples": 20})
    d = j(data)
    assert st == 200 and len(d["scan"]["id"]) <= 100 and d["scan"]["config"]["name"] == "x" * 300


def test_failed_new_scan_leaves_samples_consistent(tmp_path, monkeypatch):
    app = App(adc=SimulatedAD7705(seed=1), data_dir=tmp_path, samples=7, discard=1)
    app.new_scan({"name": "a", "rows": 1, "cols": 1, "samples": 7})
    first = app.scan

    def boom(data_dir, cfg):
        raise OSError("disk full")
    monkeypatch.setattr(server_mod, "new_scan", boom)
    with pytest.raises(OSError):
        app.new_scan({"name": "b", "rows": 1, "cols": 1, "samples": 9})
    assert app.scan is first and app.samples == 7 == app.scan.config.samples and app.measuring is False


def test_goto_racing_measure_is_not_lost(tmp_path):
    app = App(adc=SimulatedAD7705(seed=1), data_dir=tmp_path, samples=5, discard=1)
    app.new_scan({"name": "a", "rows": 3, "cols": 3, "samples": 5})
    orig, raced = app._acquire, []

    def racing_acquire():                      # another request's goto lands just before measure takes the ADC lock
        if not raced:
            raced.append(True); app.goto(2, 2)
        orig()
    app._acquire = racing_acquire
    out = app.measure()
    assert "2,2" in app.scan.cells and "0,0" not in app.scan.cells and app.scan.cursor == [0, 0]
    assert (out["cell"]["row"], out["cell"]["col"]) == (2, 2) and out["scan"]["cursor"] == [0, 0]


def test_measure_response_snapshot_matches_measured_scan(client):
    app = client.app
    st, _, data = client("POST", "/api/scan/new", {"name": "a", "rows": 1, "cols": 1, "samples": 20}); id_a = j(data)["scan"]["id"]
    st, _, data = client("POST", "/api/scan/new", {"name": "b", "rows": 2, "cols": 2, "samples": 20}); id_b = j(data)["scan"]["id"]
    orig, raced = app._release, []

    def racing_release():                      # an open_scan lands right after the measurement releases the ADC
        orig()
        if not raced:
            raced.append(True); app.open_scan(id_a)
    app._release = racing_release
    st, _, data = client("POST", "/api/measure", {}); d = j(data)
    assert st == 200 and d["scan"]["id"] == id_b and (d["cell"]["row"], d["cell"]["col"]) == (0, 0) and d["scan"]["progress"] == [1, 4]
    assert j(client("GET", "/api/state")[2])["scan"]["id"] == id_a
