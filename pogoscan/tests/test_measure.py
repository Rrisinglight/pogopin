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
