"""ADC status block: live register check between measurements, events, re-init endpoint."""
import json
import threading
import http.client
from pathlib import Path

import pytest

from pogoscan.ad7705 import AD7705
from pogoscan.server import App, make_server
from tests.fakes import FakeSpi, FakeDrdy, FakeReset

STATIC = Path(__file__).resolve().parents[1] / "pogoscan" / "static"


def serve(app):
    srv = make_server(app, "127.0.0.1", 0)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    conn = http.client.HTTPConnection("127.0.0.1", srv.server_address[1], timeout=10)

    def call(method, path, body=None):
        conn.request(method, path, body=None if body is None else json.dumps(body), headers={"Content-Type": "application/json"})
        r = conn.getresponse()
        return r.status, json.loads(r.read())
    return srv, call


@pytest.fixture
def ok_client(tmp_path):
    spi = FakeSpi()
    adc = AD7705(spi=spi, drdy=FakeDrdy(True), reset=FakeReset())
    adc.reset(); adc.configure()
    srv, call = serve(App(adc=adc, data_dir=tmp_path, samples=10, discard=2))
    yield call, spi
    srv.shutdown(); srv.server_close()


def test_status_ok_then_warn_after_chip_reset_then_recovered(ok_client):
    call, spi = ok_client
    st, d = call("GET", "/api/state"); s = d["adc"]["status"]
    assert st == 200 and s["level"] == "ok" and s["clock"] == 0x0C and s["setup"] == 0x38 and s["configured"] is True
    assert s["reinits"] == 0 and s["last_error"] is None and s["checked_at"].endswith("+00:00") and s["busy"] is False
    spi._reset_state()
    st, d = call("GET", "/api/state"); s = d["adc"]["status"]
    assert s["level"] == "warn" and "power-on defaults" in s["message"] and s["clock"] == 0x05 and s["setup"] == 0x01
    call("POST", "/api/scan/new", {"name": "s", "rows": 1, "cols": 1, "samples": 10})   # configures + calibrates
    spi._reset_state()
    st, d = call("POST", "/api/measure", {}); assert st == 200
    st, d = call("GET", "/api/state"); s = d["adc"]["status"]
    assert s["level"] == "ok" and s["reinits"] == 1 and s["last_reinit"] and s["last_measure"]


def test_reinit_endpoint_and_noise_event(ok_client):
    call, spi = ok_client
    st, d = call("POST", "/api/adc/reinit", {}); assert st == 200 and d["ok"] is True and d["seconds"] >= 0
    st, d = call("GET", "/api/noise?n=5"); assert st == 200
    st, d = call("GET", "/api/state"); s = d["adc"]["status"]
    assert s["reinits"] == 1 and s["calibrations"] == 1 and s["last_noise"]["n"] == 5 and "time" in s["last_noise"]


def test_status_error_when_chip_silent_and_last_error_recorded(tmp_path):
    spi = FakeSpi(miso_open=True)
    adc = AD7705(spi=spi, drdy=FakeDrdy(True), reset=FakeReset())
    srv, call = serve(App(adc=adc, data_dir=tmp_path, samples=10, discard=2))
    try:
        st, d = call("GET", "/api/state"); s = d["adc"]["status"]
        assert s["level"] == "error" and "no response" in s["message"] and s["clock"] == 0 and s["setup"] == 0
        st, d = call("POST", "/api/scan/new", {"name": "s", "rows": 1, "cols": 1, "samples": 10})
        assert st == 500 and "mismatch" in d["error"]
        st, d = call("GET", "/api/state"); s = d["adc"]["status"]
        assert s["last_error"] and "mismatch" in s["last_error"] and s["last_error_time"]
    finally:
        srv.shutdown(); srv.server_close()


def test_page_has_status_block():
    html = (STATIC / "index.html").read_text()
    for cid in ("adc-status", "adc-dot", "adc-message", "adc-regs", "adc-last-error", "reinit-btn"):
        assert f'id="{cid}"' in html, cid
    js = (STATIC / "app.js").read_text()
    assert "/api/adc/reinit" in js and "function renderAdc" in js


def test_page_explains_noise_and_calibration():
    html = (STATIC / "index.html").read_text()
    assert 'id="help"' in html and "self-calibration" in html and "0.6" in html
    for cid in ("calibrate-btn", "noise-btn", "zero-btn"):
        assert f'id="{cid}" title="' in html, cid
    js = (STATIC / "app.js").read_text()
    assert "own noise" in js and "stuck line" in js
