'use strict';
// pogoscan page. Talks only to the JSON API (spec §5.4); no build step, no external resources.
const $ = (id) => document.getElementById(id);
const state = { data: null, hover: null, focus: null, busy: false };

// ---- colour ---------------------------------------------------------------
// Sequential magnitude -> one hue, light -> dark (dataviz reference palette, blue steps 100..700).
// OKLCH lightness is monotone along the ramp (0.905 -> 0.338) and hue stays within 253-257 degrees.
const RAMP = ['#cde2fb', '#b7d3f6', '#9ec5f4', '#86b6ef', '#6da7ec', '#5598e7', '#3987e5',
              '#2a78d6', '#256abf', '#1c5cab', '#184f95', '#104281', '#0d366b'].map(hexToRgb);
// Chart chrome: text tokens for labels, neutral empty state, one accent for the cursor.
const INK = { primary: '#0b0b0b', secondary: '#52514e', muted: '#898781', surface: '#fcfcfb',
              empty: '#eeede8', hatch: '#c3c2b7', accent: '#e60049' };
const FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif';

function hexToRgb(h) { return [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16)); }

function colour(t) {
  if (!Number.isFinite(t)) t = 0;
  const x = Math.max(0, Math.min(1, t)) * (RAMP.length - 1);
  const i = Math.min(RAMP.length - 2, Math.floor(x)), f = x - i, a = RAMP[i], b = RAMP[i + 1];
  return `rgb(${a.map((v, k) => Math.round(v + (b[k] - v) * f)).join(',')})`;
}

// ---- API ------------------------------------------------------------------
async function api(method, path, body) {
  const res = await fetch(path, { method, headers: { 'Content-Type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body) });
  const json = await res.json().catch(() => ({ error: `HTTP ${res.status}` }));
  if (!res.ok) throw new Error(json.error || `HTTP ${res.status}`);
  return json;
}

function toast(msg, isError) {
  const t = $('toast'); t.textContent = msg; t.classList.toggle('error', !!isError); t.hidden = false;
  clearTimeout(toast.timer); toast.timer = setTimeout(() => { t.hidden = true; }, isError ? 8000 : 4000);
}

async function refresh() {
  try { state.data = await api('GET', '/api/state'); render(); }
  catch (e) { $('status').textContent = 'server unreachable: ' + e.message; }
}

// Every action re-reads /api/state afterwards (spec §5.7): the page never assumes a request succeeded.
async function act(method, path, body) {
  if (state.busy) return null;
  state.busy = true; setButtons();
  try {
    const r = await api(method, path, body);
    if (r.cell) {
      const z = r.scan && r.scan.zero ? r.scan.zero.value_uv : null;
      toast(`(${r.cell.row}, ${r.cell.col}) = ${r.cell.value_uv.toFixed(2)} µV ± ${r.cell.stdev_uv.toFixed(2)}` + (z === null ? '' : ` · rel ${(r.cell.value_uv - z).toFixed(2)} µV`));
    }
    await refresh();
    return r;
  } catch (e) { toast(e.message, true); await refresh(); return null; }
  finally { state.busy = false; setButtons(); }
}

function isMeasuring() { return state.busy || !!(state.data && state.data.measuring); }

function setButtons() {
  const s = state.data && state.data.scan, measuring = isMeasuring();
  $('measure-btn').disabled = measuring || !s || (s.complete && !s.targeted);   // a complete scan re-measures only after a jump (goto)
  for (const id of ['undo-btn', 'zero-btn', 'zero-clear-btn', 'png-btn', 'new-btn']) $(id).disabled = measuring || (!s && id !== 'new-btn');
  for (const id of ['calibrate-btn', 'noise-btn', 'reinit-btn']) $(id).disabled = measuring;
  $('open-select').disabled = measuring;
  for (const id of ['csv-link', 'json-link']) $(id).classList.toggle('disabled', !s);
  $('measure-btn').textContent = measuring ? 'Measuring…' : 'Measure (Space)';
  $('spinner').hidden = !measuring;
}

// ---- state -> DOM -----------------------------------------------------------
function currentGrid() {
  const s = state.data.scan;
  return $('relative-toggle').checked ? s.grid : s.grid_raw;
}

function extent(grid) {
  let min = Infinity, max = -Infinity;
  for (const row of grid) for (const v of row) if (v !== null && Number.isFinite(v)) { if (v < min) min = v; if (v > max) max = v; }
  return min <= max ? [min, max] : [0, 1];
}

function scale(grid) {
  let min, max;
  if ($('scale-auto').checked || $('scale-min').value === '' || $('scale-max').value === '') {
    [min, max] = extent(grid);
    $('scale-min').value = min.toFixed(2); $('scale-max').value = max.toFixed(2);
  } else {
    min = parseFloat($('scale-min').value); max = parseFloat($('scale-max').value);
  }
  if (!(max > min)) max = min + 1;
  return [min, max];
}

function option(value, label, disabled) {
  const o = document.createElement('option'); o.value = value; o.textContent = label; o.disabled = !!disabled; return o;
}

function fillScanList(scans, currentId) {
  const sel = $('open-select'), sig = JSON.stringify(scans);
  if (sig !== fillScanList.sig) {   // rebuild only when the listing changed, so an open dropdown is not yanked away
    fillScanList.sig = sig;
    sel.replaceChildren(option('', 'choose…'), ...scans.map((x) => x.error
      ? option(x.id, `${x.id} (unreadable)`, true)
      : option(x.id, `${x.name} — ${x.progress[0]}/${x.progress[1]} — ${x.created}`)));
  }
  sel.value = currentId || '';
}

function render() {
  const d = state.data, s = d.scan;
  $('status').textContent = d.adc.simulated ? 'SIMULATED ADC' : `AD7705 gain ${d.adc.gain}, ${d.adc.rate} Hz, LSB ${d.adc.lsb_uv.toFixed(3)} µV`;
  $('adc-info').textContent = `${d.adc.samples} samples per point (+${d.adc.discard} settling)` + (d.adc.simulated ? ' · synthetic plate' : '');
  renderAdc(d.adc);
  fillScanList(d.scans, s && s.id);
  setButtons();
  if (!s) {
    $('next-cell').textContent = '–'; $('progress').textContent = 'no scan open'; $('last-value').textContent = '–';
    $('banner').hidden = true; $('hover').textContent = '';
    drawGrid(null); drawLegend(0, 1); renderTable(null);
    return;
  }
  const [r, c] = s.cursor, p = s.config.pitch_mm;
  $('next-cell').textContent = (s.complete && !s.targeted) ? 'scan complete (click a cell to re-measure it)' : `row ${r}, col ${c}  (x ${(c * p).toFixed(1)} mm, y ${(r * p).toFixed(1)} mm)`;
  $('progress').textContent = `${s.progress[0]} / ${s.progress[1]}` + (s.zero ? `  · zero ${s.zero.value_uv.toFixed(2)} µV` : '  · no zero');
  $('banner').hidden = !s.complete;
  const last = s.history[s.history.length - 1];
  if (last) {
    const cell = s.cells[`${last[0]},${last[1]}`];
    const relTxt = cell && s.zero ? `, rel ${(cell.value_uv - s.zero.value_uv).toFixed(2)}` : '';
    $('last-value').textContent = cell ? `(${last[0]}, ${last[1]}) ${cell.value_uv.toFixed(2)} µV ± ${cell.stdev_uv.toFixed(2)} (median ${cell.median_uv.toFixed(2)}${relTxt}, n ${cell.n_kept})` : '–';
  } else $('last-value').textContent = '–';
  drawGrid(s);
  renderTable(s);
  showCell(inspected());
}

// ---- heatmap ----------------------------------------------------------------
function layout(s, cv) {
  const cssW = cv.clientWidth || 630, dpr = window.devicePixelRatio || 1;
  const W = Math.max(630, Math.round(cssW * dpr));
  if (cv.width !== W || cv.height !== W) { cv.width = W; cv.height = W; }
  const k = W / cssW;                                   // backing pixels per CSS pixel
  const rows = s.config.rows, cols = s.config.cols;
  const left = 26 * k, top = 18 * k, pad = 4 * k;       // room for row/col index labels
  const cell = Math.min((W - left - pad) / cols, (W - top - pad) / rows);   // square cells: pitch is the same both ways
  return { W, k, rows, cols, left, top, cell, gap: Math.min(2 * k, cell / 5) };
}

function ring(ctx, L, r, c, style, lw) {
  // An outline with a 2px surface ring around it so it stays visible on the darkest and lightest cells.
  const inset = (lw + 2 * L.k) / 2, x = L.left + c * L.cell + inset, y = L.top + r * L.cell + inset, w = L.cell - 2 * inset;
  ctx.lineWidth = lw + 2 * L.k; ctx.strokeStyle = INK.surface; ctx.strokeRect(x, y, w, w);
  ctx.lineWidth = lw; ctx.strokeStyle = style; ctx.strokeRect(x, y, w, w);
}

function drawGrid(s, forExport) {
  const cv = $('heatmap'), ctx = cv.getContext('2d');
  ctx.fillStyle = INK.surface; ctx.fillRect(0, 0, cv.width, cv.height);
  if (!s) { drawGrid.layout = null; return; }
  const L = layout(s, cv); drawGrid.layout = L;
  const grid = currentGrid(), [min, max] = scale(grid), span = max - min;
  const g = L.gap, size = L.cell - g;
  ctx.lineWidth = Math.max(1, L.k);
  for (let r = 0; r < L.rows; r++) for (let c = 0; c < L.cols; c++) {
    const v = grid[r][c], x = L.left + c * L.cell + g / 2, y = L.top + r * L.cell + g / 2;
    if (v === null) {                                   // empty state: neutral fill plus a hatch hairline, never colour alone
      ctx.fillStyle = INK.empty; ctx.fillRect(x, y, size, size);
      ctx.strokeStyle = INK.hatch; ctx.beginPath(); ctx.moveTo(x, y + size); ctx.lineTo(x + size, y); ctx.stroke();
    } else {
      ctx.fillStyle = colour((v - min) / span); ctx.fillRect(x, y, size, size);
    }
  }
  // Row / column index labels in secondary ink; thin out when cells get small.
  const cellCss = L.cell / L.k, every = cellCss >= 16 ? 1 : cellCss >= 8 ? 5 : 10;
  ctx.fillStyle = INK.secondary; ctx.font = `${11 * L.k}px ${FONT}`;
  ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
  for (let c = 0; c < L.cols; c += every) ctx.fillText(String(c), L.left + (c + 0.5) * L.cell, L.top - 3 * L.k);
  ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
  for (let r = 0; r < L.rows; r += every) ctx.fillText(String(r), L.left - 4 * L.k, L.top + (r + 0.5) * L.cell);
  // Markers: inspected cell, last measured cell, cursor (next cell).
  const ins = forExport ? null : inspected();
  if (ins) ring(ctx, L, ins[0], ins[1], INK.secondary, 2 * L.k);
  const last = s.history[s.history.length - 1];
  if (last) ring(ctx, L, last[0], last[1], INK.primary, 2 * L.k);
  if (!s.complete || s.targeted) ring(ctx, L, s.cursor[0], s.cursor[1], INK.accent, 3 * L.k);
  drawLegend(min, max);
}

function drawLegend(min, max) {
  const lg = $('legend'), ctx = lg.getContext('2d'), dpr = window.devicePixelRatio || 1;
  const W = Math.round((lg.clientWidth || 300) * dpr), H = Math.round(14 * dpr);
  if (lg.width !== W || lg.height !== H) { lg.width = W; lg.height = H; }
  for (let x = 0; x < W; x++) { ctx.fillStyle = colour(x / Math.max(1, W - 1)); ctx.fillRect(x, 0, 1, H); }
  $('scale-min-label').textContent = min.toFixed(2); $('scale-max-label').textContent = max.toFixed(2);
}

// ---- inspection (hover, keyboard focus) --------------------------------------
function inspected() {
  if (state.hover) return state.hover;
  return document.activeElement === $('heatmap') ? state.focus : null;
}

function cellAt(ev) {
  const s = state.data && state.data.scan, L = drawGrid.layout; if (!s || !L) return null;
  const rect = $('heatmap').getBoundingClientRect();
  const px = (ev.clientX - rect.left) * (L.W / rect.width), py = (ev.clientY - rect.top) * (L.W / rect.height);
  const c = Math.floor((px - L.left) / L.cell), r = Math.floor((py - L.top) / L.cell);
  return (r >= 0 && r < L.rows && c >= 0 && c < L.cols) ? [r, c] : null;
}

function showCell(rc) {
  const s = state.data && state.data.scan, out = $('hover');
  if (!s || !rc) { out.textContent = ''; return; }
  const [r, c] = rc, p = s.config.pitch_mm, cell = s.cells[`${r},${c}`], v = currentGrid()[r][c];
  let text = `row ${r}, col ${c} · x ${(c * p).toFixed(1)} mm, y ${(r * p).toFixed(1)} mm · `;
  if (cell && v !== null) {
    text += `${v.toFixed(2)} µV ± ${cell.stdev_uv.toFixed(2)} (n ${cell.n_kept}`;
    if (s.zero && $('relative-toggle').checked) text += `, raw ${cell.value_uv.toFixed(2)}`;
    text += ')';
  } else text += 'not measured';
  out.textContent = text;
}

function setInspected(kind, rc) {
  const before = JSON.stringify(inspected());
  state[kind] = rc;
  if (JSON.stringify(inspected()) !== before && state.data && state.data.scan) drawGrid(state.data.scan);
  showCell(inspected());
}

function tlocal(iso) { const d = new Date(iso); return isNaN(d) ? String(iso) : d.toLocaleTimeString(); }

function renderAdc(a) {
  const st = a.status || {};
  $('adc-dot').className = 'dot ' + (st.level || 'info');
  $('adc-message').textContent = st.message || '–';
  $('adc-mode').textContent = a.simulated ? 'simulated (synthetic plate)' : 'AD7705 on SPI0, mode 3';
  const hx = (v) => (typeof v === 'number' ? '0x' + v.toString(16).toUpperCase().padStart(2, '0') : '–');
  $('adc-regs').textContent = ('clock' in st) ? `clock ${hx(st.clock)} · setup ${hx(st.setup)}${st.configured ? ' · OK' : ''}` : '–';
  $('adc-settings').textContent = `gain ${a.gain} · ${a.rate} Hz · LSB ${a.lsb_uv.toFixed(3)} µV · ${a.samples}+${a.discard} samples`;
  $('adc-last-measure').textContent = st.last_measure ? tlocal(st.last_measure) : '–';
  $('adc-last-noise').textContent = st.last_noise ? `${st.last_noise.mean_uv.toFixed(2)} µV ± ${st.last_noise.stdev_uv.toFixed(2)} (n ${st.last_noise.n}, ${tlocal(st.last_noise.time)})` : '–';
  $('adc-reinits').textContent = `${st.reinits || 0}` + (st.last_reinit ? ` (last ${tlocal(st.last_reinit)})` : '') + (st.calibrations ? ` · ${st.calibrations} calibrations` : '');
  $('adc-last-error').textContent = st.last_error ? `${tlocal(st.last_error_time)}: ${st.last_error}` : 'none';
  $('adc-checked').textContent = (st.checked_at ? tlocal(st.checked_at) : '–') + (st.busy ? ' (measuring now)' : '');
}

function renderTable(s) {
  const body = $('cell-table-body');
  if (!$('table-details').open) { body.replaceChildren(); return; }
  if (!s) { body.replaceChildren(); return; }
  const grid = currentGrid(), p = s.config.pitch_mm, rows = [];
  for (let r = 0; r < s.config.rows; r++) for (let c = 0; c < s.config.cols; c++) {
    const cell = s.cells[`${r},${c}`]; if (!cell) continue;
    const tr = document.createElement('tr');
    for (const v of [r, c, (c * p).toFixed(1), (r * p).toFixed(1), grid[r][c].toFixed(3), cell.value_uv.toFixed(3), cell.stdev_uv.toFixed(3), cell.n_kept, cell.timestamp]) {
      const td = document.createElement('td'); td.textContent = String(v); tr.appendChild(td);
    }
    rows.push(tr);
  }
  body.replaceChildren(...rows);
}

// ---- PNG export: heatmap + title + scale legend on one image ---------------------
function wrapLines(ctx, text, maxW) {
  // Greedy wrap on the " · " separators so a subtitle never runs off the image.
  const lines = []; let line = '';
  for (const part of text.split(' · ')) {
    const cand = line ? `${line} · ${part}` : part;
    if (line && ctx.measureText(cand).width > maxW) { lines.push(line); line = part; } else line = cand;
  }
  if (line) lines.push(line);
  return lines;
}

function downloadPng() {
  const s = state.data && state.data.scan; if (!s) return;
  const src = $('heatmap'), L = drawGrid.layout; if (!L) return;
  const k = L.k, pad = 12 * k, lh = 16 * k, barH = 12 * k, W = src.width + 2 * pad, textW = W - 2 * pad, barW = Math.round(W * 0.4);
  const out = document.createElement('canvas'), ctx = out.getContext('2d');
  const small = `${11 * k}px ${FONT}`;
  ctx.font = small;
  const rel = $('relative-toggle').checked && s.zero;
  const sub = wrapLines(ctx, `${rel ? `relative to zero (${s.zero.value_uv.toFixed(2)} µV)` : 'raw values'} · ${s.progress[0]}/${s.progress[1]} cells · pitch ${s.config.pitch_mm} mm · ${s.config.samples} samples/point · ${s.config.created}`, textW);
  const [min, max] = scale(currentGrid());
  const minLabel = min.toFixed(2), maxLabel = `${max.toFixed(2)} µV`, keyLabel = 'not measured';
  const legendW = ctx.measureText(minLabel).width + barW + ctx.measureText(maxLabel).width + 12 * k;
  const keyW = barH + 6 * k + ctx.measureText(keyLabel).width;
  const keyBeside = legendW + 24 * k + keyW <= textW;          // otherwise the key goes on a second footer line
  const head = pad + 20 * k + sub.length * lh + 4 * k, foot = pad + barH + (keyBeside ? 0 : barH + 8 * k) + pad;
  out.width = W; out.height = head + src.height + foot;         // sizing resets the context state, so fonts are set again below
  ctx.fillStyle = INK.surface; ctx.fillRect(0, 0, W, out.height);
  ctx.textBaseline = 'top'; ctx.fillStyle = INK.primary; ctx.font = `bold ${14 * k}px ${FONT}`;
  ctx.fillText(`${s.config.name} — ${s.id}`, pad, pad);
  ctx.fillStyle = INK.secondary; ctx.font = small;
  sub.forEach((line, i) => ctx.fillText(line, pad, pad + 20 * k + i * lh));
  drawGrid(s, true);                                             // the export carries no inspected-cell ring
  ctx.drawImage(src, pad, head);
  drawGrid(s);                                                   // restore the on-screen markers
  ctx.textBaseline = 'middle';
  const legend = (x0, y0) => {
    ctx.fillStyle = INK.secondary; ctx.fillText(minLabel, x0, y0 + barH / 2);
    const bx = x0 + ctx.measureText(minLabel).width + 6 * k;
    for (let x = 0; x < barW; x++) { ctx.fillStyle = colour(x / (barW - 1)); ctx.fillRect(bx + x, y0, 1, barH); }
    ctx.fillStyle = INK.secondary; ctx.fillText(maxLabel, bx + barW + 6 * k, y0 + barH / 2);
    return bx + barW + 6 * k + ctx.measureText(maxLabel).width;
  };
  const key = (x0, y0) => {
    ctx.fillStyle = INK.empty; ctx.fillRect(x0, y0, barH, barH);
    ctx.strokeStyle = INK.hatch; ctx.lineWidth = Math.max(1, k); ctx.beginPath(); ctx.moveTo(x0, y0 + barH); ctx.lineTo(x0 + barH, y0); ctx.stroke();
    ctx.fillStyle = INK.secondary; ctx.fillText(keyLabel, x0 + barH + 6 * k, y0 + barH / 2);
  };
  const y = head + src.height + pad, end = legend(pad, y);
  if (keyBeside) key(end + 24 * k, y); else key(pad, y + barH + 8 * k);
  out.toBlob((blob) => {
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `${s.id}.png`; a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  });
}

// ---- wiring -------------------------------------------------------------------
function jumpTo(rc) {
  if (rc && confirm(`Jump to row ${rc[0]}, col ${rc[1]}?`)) act('POST', '/api/goto', { row: rc[0], col: rc[1] });
}

function wire() {
  const cv = $('heatmap');
  $('measure-btn').onclick = () => act('POST', '/api/measure', {});
  $('undo-btn').onclick = () => act('POST', '/api/undo', {});
  $('zero-btn').onclick = (ev) => { ev.currentTarget.blur(); if (confirm('Pin on the reference contact block? Measure zero now.')) act('POST', '/api/zero', {}); };
  $('zero-clear-btn').onclick = () => act('POST', '/api/zero/clear', {});
  $('calibrate-btn').onclick = async () => { const r = await act('POST', '/api/calibrate', {}); if (r) toast(`calibrated in ${(r.seconds * 1000).toFixed(0)} ms`); };
  $('noise-btn').onclick = async () => {
    const r = await act('GET', '/api/noise?n=50');
    if (!r) return;
    const sd = r.stdev_uv;
    const verdict = sd === 0 ? 'stuck line, no real conversions' : sd < 0.3 ? 'below the chip noise floor, check the input is really connected'
      : sd <= 1.2 ? 'normal, this is the ADC’s own noise (about 0.6 µV rms)' : 'high, look for pickup, a moving cable or a poor contact';
    toast(`noise over ${r.n} samples: mean ${r.mean_uv.toFixed(2)} µV, scatter ± ${sd.toFixed(2)} µV · ${verdict}`, sd > 1.2 || sd === 0);
  };
  $('reinit-btn').onclick = async () => { const r = await act('POST', '/api/adc/reinit', {}); if (r) toast(`ADC re-initialised, self-calibration ${(r.seconds * 1000).toFixed(0)} ms`); };
  $('new-btn').onclick = () => act('POST', '/api/scan/new', { name: $('new-name').value, rows: +$('new-rows').value, cols: +$('new-cols').value, pitch_mm: +$('new-pitch').value, samples: +$('new-samples').value });
  $('open-select').onchange = (e) => { if (e.target.value) act('POST', '/api/scan/open', { id: e.target.value }); };
  $('png-btn').onclick = downloadPng;
  for (const id of ['csv-link', 'json-link']) $(id).onclick = (e) => { if (e.currentTarget.classList.contains('disabled')) e.preventDefault(); };
  for (const id of ['relative-toggle', 'scale-auto', 'scale-min', 'scale-max']) {
    $(id).oninput = () => { if (id === 'scale-min' || id === 'scale-max') $('scale-auto').checked = false; if (state.data) render(); };
  }
  $('table-details').ontoggle = () => { if (state.data) renderTable(state.data.scan); };
  cv.onpointermove = (ev) => setInspected('hover', cellAt(ev));
  cv.onpointerleave = () => setInspected('hover', null);
  cv.onclick = (ev) => { const rc = cellAt(ev); if (rc) { state.focus = rc; jumpTo(rc); } };
  cv.onfocus = () => { if (!state.focus && state.data && state.data.scan) state.focus = state.data.scan.cursor.slice(); setInspected('focus', state.focus); };
  cv.onblur = () => setInspected('focus', state.focus);
  document.addEventListener('keydown', (ev) => {
    const tag = ev.target.tagName;
    if (['INPUT', 'SELECT', 'TEXTAREA', 'BUTTON', 'A', 'SUMMARY'].includes(tag)) return;   // native handling wins there
    if (ev.repeat && !ev.key.startsWith('Arrow')) return;   // a held key must not auto-repeat an action (measure, undo, jump); arrows may repeat
    if (ev.code === 'Space' || ev.code === 'Enter' || ev.code === 'NumpadEnter') { ev.preventDefault(); $('measure-btn').click(); return; }
    if (ev.key === 'u' || ev.key === 'U') { $('undo-btn').click(); return; }
    const s = state.data && state.data.scan;
    if (!s || ev.target !== cv) return;
    const moves = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] };
    if (moves[ev.key]) {
      ev.preventDefault();
      const [r, c] = state.focus || s.cursor, [dr, dc] = moves[ev.key];
      setInspected('focus', [Math.max(0, Math.min(s.config.rows - 1, r + dr)), Math.max(0, Math.min(s.config.cols - 1, c + dc))]);
    } else if (ev.key === 'j' || ev.key === 'J') jumpTo(state.focus);
  });
  window.addEventListener('resize', () => { if (state.data) render(); });
  refresh(); setInterval(() => { if (!state.busy) refresh(); }, 3000);
}
document.addEventListener('DOMContentLoaded', wire);
