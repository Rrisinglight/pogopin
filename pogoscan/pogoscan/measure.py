"""One measurement = a burst of conversions reduced to robust statistics."""
from __future__ import annotations

import statistics
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone


def trimmed_mean(values: list[float], trim: float = 0.1) -> float:
    """Mean after sorting and dropping int(trim * n) values from each end.

    Fewer than three values: plain mean. Empty: ValueError.
    """
    if not values:
        raise ValueError("no values")
    if len(values) < 3:
        return statistics.fmean(values)
    if trim < 0:
        raise ValueError("trim must be >= 0")
    ordered = sorted(values)
    k = int(len(ordered) * trim)
    if 2 * k >= len(ordered):            # never trim everything away
        k = (len(ordered) - 1) // 2
    kept = ordered[k:len(ordered) - k] if k else ordered
    return statistics.fmean(kept)


@dataclass
class PointResult:
    value_uv: float
    median_uv: float
    mean_uv: float
    stdev_uv: float
    min_uv: float
    max_uv: float
    n_total: int
    n_kept: int
    discarded: int
    codes: list[int]
    duration_s: float
    timestamp: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "PointResult":
        return cls(**{k: d[k] for k in cls.__dataclass_fields__})


def measure_point(adc, n: int = 100, discard: int = 4, trim: float = 0.1) -> PointResult:
    """Read discard + n conversions, drop the first `discard` (filter settling), reduce the rest."""
    if n < 1:
        raise ValueError("n must be at least 1")
    if discard < 0:
        raise ValueError("discard must not be negative")
    t0 = time.monotonic()
    codes = adc.read_codes(n + discard)
    kept = codes[discard:]
    uv = [adc.microvolts(c) for c in kept]
    return PointResult(
        value_uv=trimmed_mean(uv, trim),
        median_uv=statistics.median(uv),
        mean_uv=statistics.fmean(uv),
        stdev_uv=statistics.pstdev(uv) if len(uv) > 1 else 0.0,
        min_uv=min(uv),
        max_uv=max(uv),
        n_total=len(codes),
        n_kept=len(kept),
        discarded=discard,
        codes=list(kept),
        duration_s=time.monotonic() - t0,
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
