"""Hardware self-test for the AD7705 wiring. Run on the Pi: python3 -m pogoscan.check

Steps (spec §5.6): spidev device file, reset + clock/setup register read-back, self-calibration,
DRDY rate, 100-sample noise burst. Exit status 0 on PASS, 1 on FAIL.
"""
from __future__ import annotations

import argparse
import os
import statistics
import sys
import time

from .ad7705 import REG_CLOCK, REG_SETUP, AD7705, AD7705Error, AD7705Timeout

MISO_HINT = "       hint: DOUT→MISO (GPIO9) open: check the orange wire, its solder joint at the module DOUT pin and the level shifter"
DRDY_HINT = "       hint: DRDY (GPIO25, yellow wire) never went low: check the wire, or the chip is not converting (no clock?)"
SPI_HINT = " — enable SPI: add dtparam=spi=on to /boot/firmware/config.txt and reboot"
RATE_TOLERANCE = 0.15        # relative error allowed on the DRDY rate
MIN_RATE_SECONDS = 0.5       # shorter runs cannot resolve the rate; it is reported but not judged


def run_checks(adc, expected_rate: int = 50, seconds: float = 2.0, spidev_path: str | None = None) -> tuple[bool, list[str]]:
    """Run every check on `adc` and return (all_passed, report_lines). Pure apart from the ADC I/O."""
    lines: list[str] = []
    ok = True

    def report(passed: bool, text: str) -> None:
        nonlocal ok
        ok = ok and passed
        lines.append(f"[{'PASS' if passed else 'FAIL'}] {text}")

    # 1. device file
    if spidev_path is not None:
        exists = os.path.exists(spidev_path)
        report(exists, f"{spidev_path} exists" + ("" if exists else SPI_HINT))
        if not exists:
            return False, lines

    # 2 + 3. reset, clock and setup registers written and read back (configure() verifies each write)
    try:
        adc.reset()
        adc.configure(rate=expected_rate, gain=128)
        read_register = getattr(adc, "read_register", None)      # the simulator has no registers
        clock = f"0x{read_register(REG_CLOCK):02X} " if read_register else ""
        setup = f"0x{read_register(REG_SETUP):02X} " if read_register else ""
        report(True, f"clock register {clock}read back correctly ({expected_rate} Hz)")
        report(True, f"setup register {setup}read back correctly (gain 128, bipolar, unbuffered)")
    except (AD7705Error, ValueError) as e:       # ValueError: a rate the crystal cannot produce
        report(False, f"clock register / setup register: {e}")
        if "0x00" in str(e):
            lines.append(MISO_HINT)
        return False, lines

    # 4. self-calibration
    try:
        t = adc.self_calibrate(timeout=2.0)
        report(True, f"self-calibration completed in {t * 1000:.0f} ms, setup register back in normal mode")
    except AD7705Timeout as e:
        report(False, f"self-calibration: {e}")
        lines.append(DRDY_HINT)
        return False, lines
    except AD7705Error as e:
        report(False, f"self-calibration: {e}")
        return False, lines

    # 5. DRDY rate: count conversions for `seconds`, capped at 1.5x the expected count so a DRDY
    #    stuck low is reported as an absurd rate instead of spinning for the whole period.
    max_reads = int(expected_rate * seconds * 1.5) + 2
    n, t0 = 0, time.monotonic()
    try:
        while n < max_reads and time.monotonic() - t0 < seconds:
            adc.read_code(timeout=1.0)
            n += 1
    except AD7705Timeout as e:
        report(False, f"DRDY: {e} after {n} conversions")
        lines.append(DRDY_HINT)
        return False, lines
    elapsed = max(time.monotonic() - t0, 1e-9)
    rate = n / elapsed
    text = f"DRDY rate {rate:.1f} Hz over {elapsed:.2f} s ({n} conversions, expected {expected_rate} Hz)"
    if getattr(adc, "simulated", False) or seconds < MIN_RATE_SECONDS:
        lines.append(f"[INFO] {text} — not judged (simulator or run shorter than {MIN_RATE_SECONDS} s)")
    else:
        rate_ok = n >= 3 and abs(rate - expected_rate) / expected_rate < RATE_TOLERANCE
        hint = "" if rate_ok else (" — DRDY stuck low or wrong clock register" if rate > expected_rate else " — too slow: wrong crystal setting?")
        report(rate_ok, text + hint)

    # 6. noise burst
    uv = [adc.microvolts(c) for c in adc.read_codes(100)]
    sd = statistics.pstdev(uv)
    burst_ok = 0.0 < sd < 5.0
    report(burst_ok, f"100-sample burst: mean {statistics.fmean(uv):.2f} µV, stdev {sd:.2f} µV, min {min(uv):.1f}, max {max(uv):.1f}"
           + ("" if burst_ok else " — stdev 0 means a stuck data line; > 5 µV means noise pickup or an open input"))
    return ok, lines


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="AD7705 wiring self-test")
    p.add_argument("--crystal", type=float, default=4.9152e6)
    p.add_argument("--rate", type=int, default=50)
    p.add_argument("--seconds", type=float, default=2.0, help="length of the DRDY rate measurement")
    p.add_argument("--drdy", type=int, default=25)
    p.add_argument("--reset", type=int, default=24)
    p.add_argument("--bus", type=int, default=0)
    p.add_argument("--device", type=int, default=0)
    args = p.parse_args(argv)
    path = f"/dev/spidev{args.bus}.{args.device}"
    if not os.path.exists(path):
        print(f"[FAIL] {path} missing{SPI_HINT}")
        print("RESULT: FAIL")
        return 1
    try:
        adc = AD7705(bus=args.bus, device=args.device, drdy_pin=args.drdy, reset_pin=args.reset, crystal_hz=args.crystal)
    except ImportError as e:
        print(f"[FAIL] cannot import the SPI/GPIO libraries: {e} — sudo apt install python3-spidev python3-gpiozero")
        print("RESULT: FAIL")
        return 1
    try:
        ok, lines = run_checks(adc, expected_rate=args.rate, seconds=args.seconds, spidev_path=path)
    finally:
        adc.close()
    print("\n".join(lines))
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
