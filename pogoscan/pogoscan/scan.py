"""Scan state: a rows×cols grid of PointResults, a cursor, an undo stack, atomic JSON persistence, CSV export."""
from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

from .measure import PointResult

CSV_HEADER = "row,col,x_mm,y_mm,value_uv,rel_uv,median_uv,mean_uv,stdev_uv,min_uv,max_uv,n_kept,timestamp"
MAX_SLUG = 64   # keeps "<slug>-<stamp>[-n]" far below the 255-byte filename limit whatever the operator types as a name


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:MAX_SLUG].rstrip("-")
    return s or "scan"


@dataclass
class ScanConfig:
    name: str
    rows: int = 21
    cols: int = 21
    pitch_mm: float = 3.0
    samples: int = 100
    discard: int = 4
    gain: int = 128
    rate: int = 50
    created: str = ""


class Scan:
    def __init__(self, scan_id: str, path: Path, config: ScanConfig):
        self.id, self.path, self.config = scan_id, Path(path), config
        self.cells: dict[str, dict] = {}
        self.history: list[list[int]] = []
        self.cursor: list[int] = [0, 0]
        self.zero: dict | None = None
        # True while the cursor sits on a cell chosen with goto() and not yet consumed by record()/undo(); this is
        # what lets a complete scan be re-measured cell by cell. Session state only: never persisted.
        self.targeted = False

    # --- helpers ---------------------------------------------------------
    @staticmethod
    def key(row: int, col: int) -> str:
        return f"{row},{col}"

    def _check(self, row: int, col: int) -> None:
        if not (0 <= row < self.config.rows and 0 <= col < self.config.cols):
            raise ValueError(f"cell ({row}, {col}) outside {self.config.rows}x{self.config.cols}")

    def _next_unmeasured(self, row: int, col: int) -> list[int]:
        """First unmeasured cell after (row, col) in row-major order, wrapping; (row, col) itself when none."""
        total = self.config.rows * self.config.cols
        start = row * self.config.cols + col
        for step in range(1, total + 1):
            i = (start + step) % total
            r, c = divmod(i, self.config.cols)
            if self.key(r, c) not in self.cells:
                return [r, c]
        return [row, col]

    # --- mutations (each saves) -------------------------------------------
    def record(self, row: int, col: int, result: PointResult) -> None:
        self._check(row, col)
        self.cells[self.key(row, col)] = {**result.to_dict(), "row": row, "col": col}
        self.history.append([row, col])
        self.cursor = self._next_unmeasured(row, col)
        self.targeted = False
        self.save()

    def undo(self) -> list[int] | None:
        if not self.history:
            return None
        row, col = self.history.pop()
        self.cells.pop(self.key(row, col), None)
        self.cursor = [row, col]
        self.targeted = False
        self.save()
        return [row, col]

    def goto(self, row: int, col: int) -> None:
        self._check(row, col)
        self.cursor = [row, col]
        self.targeted = True
        self.save()

    def set_zero(self, result: PointResult | None) -> None:
        self.zero = result.to_dict() if result is not None else None
        self.save()

    # --- queries ----------------------------------------------------------
    def zero_uv(self) -> float | None:
        return None if self.zero is None else self.zero["value_uv"]

    def progress(self) -> tuple[int, int]:
        return len(self.cells), self.config.rows * self.config.cols

    def complete(self) -> bool:
        m, t = self.progress()
        return m >= t

    def grid(self, relative: bool = True) -> list[list[float | None]]:
        z = self.zero_uv() if relative else None
        out = []
        for r in range(self.config.rows):
            row = []
            for c in range(self.config.cols):
                cell = self.cells.get(self.key(r, c))
                row.append(None if cell is None else cell["value_uv"] - (z or 0.0))
            out.append(row)
        return out

    def to_dict(self, include_codes: bool = True) -> dict:
        """API/state view. include_codes=False drops the raw sample codes (they stay in scan.json and the JSON export)."""
        m, t = self.progress()
        cells = self.cells if include_codes else {k: {kk: vv for kk, vv in v.items() if kk != "codes"} for k, v in self.cells.items()}
        return {"id": self.id, "config": asdict(self.config), "cells": cells, "history": self.history,
                "cursor": self.cursor, "zero": self.zero, "progress": [m, t], "complete": self.complete(),
                "targeted": self.targeted, "grid": self.grid(True), "grid_raw": self.grid(False)}

    def to_csv(self) -> str:
        z = self.zero_uv()
        lines = [CSV_HEADER]
        for r in range(self.config.rows):
            for c in range(self.config.cols):
                cell = self.cells.get(self.key(r, c))
                if cell is None:
                    continue
                rel = cell["value_uv"] - z if z is not None else cell["value_uv"]
                lines.append(",".join(str(x) for x in (
                    r, c, round(c * self.config.pitch_mm, 4), round(r * self.config.pitch_mm, 4), cell["value_uv"], rel, cell["median_uv"],
                    cell["mean_uv"], cell["stdev_uv"], cell["min_uv"], cell["max_uv"], cell["n_kept"], cell["timestamp"])))
        return "\n".join(lines) + "\n"

    # --- persistence ------------------------------------------------------
    def save(self) -> None:
        """Write to <path>.tmp, fsync, then os.replace so the file on disk is always complete."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"id": self.id, "config": asdict(self.config), "cells": self.cells, "history": self.history,
                   "cursor": self.cursor, "zero": self.zero}
        tmp = self.path.with_name(self.path.name + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=1)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, self.path)

    @classmethod
    def load(cls, path: Path) -> "Scan":
        path = Path(path)
        d = json.loads(path.read_text(encoding="utf-8"))
        s = cls(d["id"], path, ScanConfig(**d["config"]))
        s.cells, s.history, s.cursor, s.zero = d["cells"], d["history"], d["cursor"], d.get("zero")
        return s


def new_scan(data_dir: Path, config: ScanConfig) -> Scan:
    data_dir = Path(data_dir)
    if not config.created:
        config.created = datetime.now(timezone.utc).isoformat(timespec="seconds")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    base = f"{slugify(config.name)}-{stamp}"
    scan_id, n = base, 1
    while (data_dir / scan_id).exists():
        n += 1
        scan_id = f"{base}-{n}"
    s = Scan(scan_id, data_dir / scan_id / "scan.json", config)
    s.save()
    return s


def list_scans(data_dir: Path) -> list[dict]:
    """Readable scans newest first (by created, then id), then unreadable ones as {"id", "error"}."""
    data_dir = Path(data_dir)
    good: list[dict] = []
    bad: list[dict] = []
    if not data_dir.is_dir():
        return good
    for p in data_dir.iterdir():
        f = p / "scan.json"
        if not f.is_file():
            continue
        try:
            s = Scan.load(f)
            # the directory name is the id the API opens; a copied/renamed directory must list under its own name
            good.append({"id": p.name, "name": s.config.name, "created": s.config.created, "progress": list(s.progress())})
        except Exception as e:  # noqa: BLE001 - report, never crash the listing
            bad.append({"id": p.name, "error": f"unreadable: {e}"})
    good.sort(key=lambda x: (x["created"], x["id"]), reverse=True)
    bad.sort(key=lambda x: x["id"])
    return good + bad


def open_scan(data_dir: Path, scan_id: str) -> Scan:
    if not scan_id or scan_id in (".", "..") or "/" in scan_id or "\\" in scan_id:
        raise FileNotFoundError(scan_id)
    f = Path(data_dir) / scan_id / "scan.json"
    if not f.is_file():
        raise FileNotFoundError(scan_id)
    return Scan.load(f)
