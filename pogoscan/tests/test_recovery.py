"""The ADC loses its registers when its supply blinks or RESET is pulsed; the server must recover on its own."""
import json
import threading
import http.client

import pytest

from pogoscan.ad7705 import AD7705, SimulatedAD7705
from pogoscan.server import App, make_server
from tests.fakes import FakeSpi, FakeDrdy, FakeReset


def test_driver_detects_power_on_defaults_and_reinitialises():
    spi = FakeSpi()
    adc = AD7705(spi=spi, drdy=FakeDrdy(True), reset=FakeReset())
    adc.reset(); adc.configure()
    assert adc.is_configured() is True
    spi._reset_state()                       # what a supply glitch does: registers back to 0x05 / 0x01
    assert adc.is_configured() is False
    adc.initialize()
    assert adc.is_configured() is True and spi.selfcals == 1 and spi.regs[1] == 0x38


def test_simulator_has_the_same_recovery_surface():
    sim = SimulatedAD7705()
    assert sim.is_configured() is True
    sim.initialize()
    assert sim.calibrations == 1


@pytest.fixture
def hw(tmp_path):
    spi = FakeSpi()
    adc = AD7705(spi=spi, drdy=FakeDrdy(True), reset=FakeReset())
    adc.reset(); adc.configure()
    app = App(adc=adc, data_dir=tmp_path, samples=10, discard=2)
    srv = make_server(app, "127.0.0.1", 0)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    conn = http.client.HTTPConnection("127.0.0.1", srv.server_address[1], timeout=10)

    def call(method, path, body=None):
        conn.request(method, path, body=None if body is None else json.dumps(body), headers={"Content-Type": "application/json"})
        r = conn.getresponse()
        return r.status, json.loads(r.read())
    yield call, spi
    srv.shutdown(); srv.server_close()


def test_server_reinitialises_after_a_chip_reset(hw):
    call, spi = hw
    st, d = call("POST", "/api/scan/new", {"name": "s", "rows": 1, "cols": 3, "samples": 10}); assert st == 200
    st, d = call("POST", "/api/measure", {}); assert st == 200
    spi._reset_state()                       # supply blink between two clicks
    assert spi.regs[1] == 0x01
    st, d = call("POST", "/api/measure", {})
    assert st == 200 and d["cell"]["n_kept"] == 10 and d["scan"]["progress"] == [2, 3]
    assert spi.regs[1] == 0x38 and spi.regs[2] == 0x0C and spi.resets >= 2
    st, d = call("GET", "/api/noise?n=5"); assert st == 200 and d["n"] == 5
