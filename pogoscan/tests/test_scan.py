import json
import pytest
from pathlib import Path
from pogoscan.measure import PointResult
from pogoscan.scan import ScanConfig, Scan, new_scan, list_scans, open_scan, slugify


def pr(v):
    return PointResult(value_uv=v, median_uv=v, mean_uv=v, stdev_uv=0.1, min_uv=v - 1, max_uv=v + 1,
                       n_total=104, n_kept=100, discarded=4, codes=[32768], duration_s=2.0, timestamp="2026-09-17T00:00:00+00:00")


def test_new_scan_creates_directory_and_file(tmp_path):
    s = new_scan(tmp_path, ScanConfig(name="Weld A", rows=3, cols=2))
    assert s.path == tmp_path / s.id / "scan.json" and s.path.exists()
    assert s.id.startswith("weld-a-") and s.cursor == [0, 0] and s.progress() == (0, 6)
    assert s.config.created != ""


def test_record_advances_row_major_and_persists(tmp_path):
    s = new_scan(tmp_path, ScanConfig(name="t", rows=2, cols=3))
    s.record(0, 0, pr(1.0)); assert s.cursor == [0, 1]
    s.record(0, 1, pr(2.0)); s.record(0, 2, pr(3.0)); assert s.cursor == [1, 0]
    reloaded = Scan.load(s.path)
    assert reloaded.cells["0,2"]["value_uv"] == 3.0 and reloaded.cursor == [1, 0] and reloaded.history == [[0, 0], [0, 1], [0, 2]]


def test_cursor_skips_measured_cells_and_wraps(tmp_path):
    s = new_scan(tmp_path, ScanConfig(name="t", rows=2, cols=2))
    s.goto(1, 1); s.record(1, 1, pr(9.0))
    assert s.cursor == [0, 0]                       # wraps to the first unmeasured cell
    s.record(0, 0, pr(1.0)); s.record(0, 1, pr(2.0))
    assert s.cursor == [1, 0]
    s.record(1, 0, pr(3.0))
    assert s.complete() and s.cursor == [1, 0]       # stays put when complete


def test_undo_restores_cursor_and_removes_cell(tmp_path):
    s = new_scan(tmp_path, ScanConfig(name="t", rows=2, cols=2))
    s.record(0, 0, pr(1.0)); s.record(0, 1, pr(2.0))
    assert s.undo() == [0, 1] and "0,1" not in s.cells and s.cursor == [0, 1]
    assert s.undo() == [0, 0] and s.undo() is None


def test_goto_bounds(tmp_path):
    s = new_scan(tmp_path, ScanConfig(name="t", rows=2, cols=2))
    with pytest.raises(ValueError):
        s.goto(2, 0)


def test_zero_grid_and_csv(tmp_path):
    s = new_scan(tmp_path, ScanConfig(name="t", rows=2, cols=2, pitch_mm=3.0))
    s.record(0, 0, pr(4.0)); s.set_zero(pr(1.5))
    assert s.zero_uv() == 1.5
    assert s.grid() == [[2.5, None], [None, None]] and s.grid(relative=False) == [[4.0, None], [None, None]]
    csv = s.to_csv().splitlines()
    assert csv[0] == "row,col,x_mm,y_mm,value_uv,rel_uv,median_uv,mean_uv,stdev_uv,min_uv,max_uv,n_kept,timestamp"
    assert csv[1].startswith("0,0,0.0,0.0,4.0,2.5,")
    s.set_zero(None); assert s.zero_uv() is None and s.grid()[0][0] == 4.0
    d = s.to_dict()
    assert d["progress"] == [1, 4] and d["complete"] is False and d["grid"][0][0] == 4.0 and d["id"] == s.id


def test_list_and_open_scans(tmp_path):
    a = new_scan(tmp_path, ScanConfig(name="first", rows=1, cols=1))
    b = new_scan(tmp_path, ScanConfig(name="second", rows=1, cols=1))
    (tmp_path / "broken").mkdir(); (tmp_path / "broken" / "scan.json").write_text("{not json")
    listed = list_scans(tmp_path)
    assert [x["id"] for x in listed][:2] == sorted([a.id, b.id], reverse=True) or listed[0]["id"] in (a.id, b.id)
    assert any("error" in x for x in listed)
    assert open_scan(tmp_path, a.id).id == a.id
    with pytest.raises(FileNotFoundError):
        open_scan(tmp_path, "nope")
    assert slugify("Weld  #3 / left") == "weld-3-left"


def test_slug_is_bounded_and_goto_marks_a_target(tmp_path):
    assert len(slugify("x" * 300)) <= 64 and slugify("a" * 63 + "-b" * 40) == "a" * 63
    s = new_scan(tmp_path, ScanConfig(name="n" * 300, rows=1, cols=1))
    assert s.path.exists() and len(s.id) <= 100
    assert s.targeted is False
    s.goto(0, 0); assert s.targeted is True
    s.record(0, 0, pr(1.0)); assert s.targeted is False and s.complete()
    s.goto(0, 0); s.undo(); assert s.targeted is False
    s.goto(0, 0); assert Scan.load(s.path).targeted is False   # never persisted
