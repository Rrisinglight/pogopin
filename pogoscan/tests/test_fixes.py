"""Regression tests for the post-review fixes (state payload, body validation, ids, CSV rounding, trim)."""
import json
import shutil
import threading
import http.client

import pytest

from pogoscan.ad7705 import SimulatedAD7705
from pogoscan.measure import PointResult, trimmed_mean
from pogoscan.scan import ScanConfig, new_scan, list_scans, open_scan
from pogoscan.server import App, make_server


def pr(v):
    return PointResult(value_uv=v, median_uv=v, mean_uv=v, stdev_uv=0.1, min_uv=v - 1, max_uv=v + 1,
                       n_total=104, n_kept=100, discarded=4, codes=[32768, 32769], duration_s=2.0, timestamp="2026-09-17T00:00:00+00:00")


@pytest.fixture
def client(tmp_path):
    app = App(adc=SimulatedAD7705(seed=1), data_dir=tmp_path, samples=10, discard=2)
    srv = make_server(app, "127.0.0.1", 0)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    conn = http.client.HTTPConnection("127.0.0.1", srv.server_address[1], timeout=10)

    def call(method, path, body=None, raw=None):
        data = raw if raw is not None else (None if body is None else json.dumps(body))
        conn.request(method, path, body=data, headers={"Content-Type": "application/json"})
        r = conn.getresponse()
        return r.status, json.loads(r.read() or b"null")
    yield call
    srv.shutdown(); srv.server_close()


def test_state_omits_raw_codes_but_measure_and_export_keep_them(client, tmp_path):
    client("POST", "/api/scan/new", {"name": "s", "rows": 1, "cols": 2, "samples": 10})
    st, d = client("POST", "/api/measure", {})
    assert st == 200 and len(d["cell"]["codes"]) == 10
    st, d = client("GET", "/api/state")
    cell = d["scan"]["cells"]["0,0"]
    assert "codes" not in cell and cell["n_kept"] == 10 and d["scan"]["targeted"] is False
    st, d = client("GET", "/api/export.json")
    assert len(d["cells"]["0,0"]["codes"]) == 10


def test_complete_scan_can_be_remeasured_after_goto(client):
    client("POST", "/api/scan/new", {"name": "s", "rows": 1, "cols": 1, "samples": 10})
    st, d = client("POST", "/api/measure", {}); assert st == 200 and d["scan"]["complete"] is True
    st, d = client("POST", "/api/measure", {}); assert st == 400
    st, d = client("POST", "/api/goto", {"row": 0, "col": 0}); assert d["scan"]["targeted"] is True
    st, d = client("POST", "/api/measure", {}); assert st == 200 and d["scan"]["targeted"] is False


def test_body_validation(client):
    st, d = client("POST", "/api/scan/new", raw="null"); assert st == 400 and "object" in d["error"]
    st, d = client("POST", "/api/scan/new", raw="[1,2]"); assert st == 400
    st, d = client("POST", "/api/scan/new", {"name": "s", "rows": 1, "cols": 1, "pitch_mm": 1e999}); assert st == 400
    st, d = client("GET", "/api/state"); assert d["scan"] is None


def test_list_scans_uses_directory_name(tmp_path):
    s = new_scan(tmp_path, ScanConfig(name="orig", rows=1, cols=1))
    shutil.copytree(tmp_path / s.id, tmp_path / "copy-of-orig")
    ids = {x["id"] for x in list_scans(tmp_path)}
    assert ids == {s.id, "copy-of-orig"}
    assert open_scan(tmp_path, "copy-of-orig").config.name == "orig"


def test_csv_coordinates_are_rounded(tmp_path):
    s = new_scan(tmp_path, ScanConfig(name="t", rows=1, cols=4, pitch_mm=0.1))
    s.record(0, 3, pr(1.0))
    assert s.to_csv().splitlines()[1].startswith("0,3,0.3,0.0,")


def test_trimmed_mean_rejects_negative_trim():
    with pytest.raises(ValueError):
        trimmed_mean([1.0, 2.0, 3.0], trim=-0.1)
