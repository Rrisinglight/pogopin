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
