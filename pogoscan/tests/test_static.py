# tests/test_static.py
from pathlib import Path

STATIC = Path(__file__).resolve().parents[1] / "pogoscan" / "static"


def test_page_references_assets_and_control_ids():
    html = (STATIC / "index.html").read_text()
    assert 'src="/static/app.js"' in html and 'href="/static/style.css"' in html
    for cid in ("heatmap", "measure-btn", "undo-btn", "zero-btn", "calibrate-btn", "noise-btn", "new-btn",
                "open-select", "csv-link", "json-link", "png-btn", "relative-toggle", "scale-min", "scale-max",
                "scale-auto", "status", "next-cell", "progress", "last-value", "toast", "legend"):
        assert f'id="{cid}"' in html, cid
    js = (STATIC / "app.js").read_text()
    for path in ("/api/state", "/api/measure", "/api/undo", "/api/goto", "/api/zero", "/api/scan/new", "/api/noise"):
        assert path in js, path
    assert "http://" not in js and "https://" not in html


# A held key auto-repeats keydown. Measure (Space/Enter) and Undo (U) must fire once per press, or a key held
# past one measurement records the next cell before the pin has moved. Arrow keys only move the inspected
# cell, so they may repeat. Checked by running app.js in node against a stubbed DOM, with a yield between
# events so each action's fetch chain finishes (busy resets) exactly as it does with a fast measurement.
KEY_REPEAT_HARNESS = r"""
const vm = require('vm'), fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');
const noop = () => {};
const ctx2d = new Proxy({}, { get: (t, k) => k === 'measureText' ? () => ({ width: 10 }) : (k in t ? t[k] : noop), set: (t, k, v) => { t[k] = v; return true; } });
function el(id, tag) {
  return { id, tagName: tag, disabled: false, hidden: false, textContent: '', value: '', checked: true, open: false,
    clientWidth: 630, width: 630, height: 630,
    classList: { toggle: noop, contains: () => false, add: noop, remove: noop },
    replaceChildren: noop, appendChild: noop, addEventListener: noop,
    getBoundingClientRect: () => ({ left: 0, top: 0, width: 630, height: 630 }),
    getContext: () => ctx2d, toBlob: noop,
    click() { if (!this.disabled && this.onclick) this.onclick(); } };
}
const elements = {}, listeners = {};
const document = {
  getElementById: (id) => elements[id] || (elements[id] = el(id, id === 'heatmap' ? 'CANVAS' : 'DIV')),
  createElement: (tag) => el('', tag.toUpperCase()),
  addEventListener: (type, fn) => (listeners[type] = listeners[type] || []).push(fn),
  activeElement: null, body: { tagName: 'BODY' },
};
const grid = [[null, null, null], [null, null, null], [null, null, null]];
const STATE = { adc: { simulated: true, gain: 128, rate: 50, lsb_uv: 0.1, samples: 10, discard: 2 }, scans: [],
  scan: { id: 's1', config: { name: 't', rows: 3, cols: 3, pitch_mm: 1, samples: 10, created: 'now' }, cursor: [0, 0], progress: [0, 9],
          complete: false, history: [], cells: {}, grid, grid_raw: grid, zero: null } };
const calls = [];
const fetch = async (path, opts) => { calls.push(`${(opts && opts.method) || 'GET'} ${path}`); return { ok: true, status: 200, json: async () => STATE }; };
const sandbox = { document, window: { devicePixelRatio: 1, addEventListener: noop }, fetch, confirm: () => false,
  setTimeout, clearTimeout, setInterval: noop, console };
vm.createContext(sandbox);
vm.runInContext(src, sandbox);
const settle = () => new Promise((r) => setTimeout(r, 5));
const key = (init) => { for (const fn of listeners.keydown) fn(Object.assign({ target: document.body, preventDefault: noop, repeat: false, key: '', code: '' }, init)); };
(async () => {
  listeners.DOMContentLoaded.forEach((fn) => fn()); await settle();
  calls.length = 0;
  key({ code: 'Space', key: ' ' }); await settle();
  for (let i = 0; i < 4; i++) { key({ code: 'Space', key: ' ', repeat: true }); await settle(); }
  key({ code: 'Enter', key: 'Enter', repeat: true }); await settle();
  key({ key: 'u', repeat: true }); await settle();
  document.activeElement = elements.heatmap;
  key({ key: 'ArrowRight', target: elements.heatmap }); key({ key: 'ArrowRight', target: elements.heatmap, repeat: true });
  console.log(JSON.stringify({ measure: calls.filter((c) => c === 'POST /api/measure').length,
    undo: calls.filter((c) => c === 'POST /api/undo').length, hover: elements.hover.textContent }));
})();
"""


def test_held_key_does_not_repeat_measure_or_undo(tmp_path):
    import json
    import shutil
    import subprocess

    import pytest

    node = shutil.which("node")
    if node is None:
        pytest.skip("node not installed")
    harness = tmp_path / "keyrepeat.js"
    harness.write_text(KEY_REPEAT_HARNESS)
    proc = subprocess.run([node, str(harness), str(STATIC / "app.js")], capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout.strip().splitlines()[-1])
    assert out["measure"] == 1, out          # one press, four Space repeats and one Enter repeat -> one measurement
    assert out["undo"] == 0, out             # a repeated U never undoes
    assert out["hover"].startswith("row 0, col 2"), out   # arrow repeats still move the inspected cell
