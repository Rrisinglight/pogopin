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
    # Plan said 0x7C/0x3C, but bipolar is B/U = 0 (bit 2 clear): MD=01 G=111 -> 0x40|0x38 = 0x78, MD=00 -> 0x38.
    assert setup_byte(MODE_SELF_CAL, 128) == 0x78          # MD=01 G=111 bipolar unbuffered fsync=0
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


# ---------------------------------------------------------------------------
# Task 2: AD7705 driver class with fakes
# ---------------------------------------------------------------------------
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
    # Plan said 0x3C; bipolar means B/U = 0 so MODE_NORMAL gain 128 is 0x38 (see test_setup_byte_bit_layout).
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
    # Plan said 0x3C; after the chip clears MD bits, bipolar gain 128 reads back as 0x38 (B/U = 0).
    assert spi.selfcals == 1 and spi.regs[1] == 0x38 and 0 <= seconds < 0.5


def test_self_calibrate_ignores_stale_drdy_low_after_the_command():
    # Datasheet "Calibration": DRDY is normally still LOW when the command lands (the previous word was never
    # read) and can stay low for up to one modulator cycle before it goes HIGH for the calibration, so DRDY
    # must be ignored for that cycle.  A driver that polls at once sees the stale low, reads the setup
    # register while MD is still 01 (6/rate, Table 21) and reports a spurious "did not complete".
    spi = FakeSpi(cal_seconds=0.02)                     # MD bits busy 20 ms, DRDY low again at 30 ms
    adc = make_adc(spi, drdy=FakeDrdy(True, spi=spi, stale_s=200e-6))
    adc.configure()
    seconds = adc.self_calibrate(timeout=0.5)
    assert spi.selfcals == 1 and spi.regs[REG_SETUP] == 0x38
    assert seconds >= 0.03                              # waited for the real end of the sequence


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


# ---------------------------------------------------------------------------
# Task 3: SimulatedAD7705
# ---------------------------------------------------------------------------
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
