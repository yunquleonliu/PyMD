/**
 * PyMD Editor — Web Frontend
 * Vanilla JS, no build step required.
 *
 * Backend modes (auto-detected at startup):
 *   'api'    — Phase 1/2: calls /api/* on a local or Docker Python server
 *   'local'  — Phase 3:   uses browser File System Access API (no server)
 *   'none'   — no backend available; read-only preview still works
 */

'use strict';

// ── Inline preview CSS used in standalone (no-server) mode ───────────────────
const PREVIEW_LIGHT_CSS = `
  body{font-family:system-ui,sans-serif;max-width:820px;margin:0 auto;
       padding:24px;line-height:1.7;color:#1a1a1a;background:#fff}
  h1,h2,h3,h4,h5,h6{line-height:1.3;margin-top:1.4em;margin-bottom:.4em}
  code{background:#f5f5f5;padding:2px 5px;border-radius:3px;font-size:.9em}
  pre{background:#f5f5f5;padding:16px;overflow-x:auto;border-radius:6px}
  pre code{background:none;padding:0}
  blockquote{border-left:4px solid #ddd;margin:0;padding-left:16px;color:#666}
  table{border-collapse:collapse;width:100%}
  th,td{border:1px solid #ddd;padding:8px 12px}
  th{background:#f5f5f5}
  img{max-width:100%}
  hr{border:none;border-top:1px solid #ddd;margin:1.5em 0}
`;
const PREVIEW_DARK_CSS = PREVIEW_LIGHT_CSS
  .replace(/background:#fff/g,  'background:#1e1e1e')
  .replace(/color:#1a1a1a/g,    'color:#d4d4d4')
  .replace(/background:#f5f5f5/g,'background:#2d2d30')
  .replace(/color:#666/g,       'color:#9d9d9d')
  .replace(/border:1px solid #ddd/g, 'border:1px solid #444')
  .replace(/background:#f5f5f5\}/g, 'background:#2d2d30}');

function buildStandaloneHtml(bodyHtml, dark) {
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>${dark ? PREVIEW_DARK_CSS : PREVIEW_LIGHT_CSS}</style>
<script>
window.MathJax={tex:{inlineMath:[['$','$'],['\\\\(','\\\\)']],
  displayMath:[['$$','$$'],['\\\\[','\\\\]']]}};
<\/script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async><\/script>
</head>
<body>${bodyHtml}</body>
</html>`;
}

// ── Backend: API (Phase 1 / Phase 2) ─────────────────────────────────────────

class ApiBackend {
  async render(markdown, dark, basePath) {
    const resp = await fetch('/api/render', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ markdown, dark, base_path: basePath || undefined }),
    });
    if (!resp.ok) throw new Error(`Render HTTP ${resp.status}`);
    const { html } = await resp.json();
    return html;
  }

  async listFiles(dir = '') {
    const resp = await fetch('/api/files?dir=' + encodeURIComponent(dir));
    if (!resp.ok) throw new Error(`List files HTTP ${resp.status}`);
    return resp.json();     // { files, dir }
  }

  async readFile(path) {
    const resp = await fetch('/api/file?path=' + encodeURIComponent(path));
    if (!resp.ok) throw new Error(`Read file HTTP ${resp.status}`);
    return resp.json();     // { content, path, name }
  }

  async writeFile(path, content) {
    const resp = await fetch('/api/file', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path, content }),
    });
    if (!resp.ok) throw new Error(`Write file HTTP ${resp.status}`);
    return resp.json();     // { ok, path }
  }

  async exportWord(markdown, filename) {
    const resp = await fetch('/api/export/word', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ markdown, filename }),
    });
    if (!resp.ok) throw new Error(`Export HTTP ${resp.status}`);
    const blob = await resp.blob();
    _triggerDownload(blob, filename);
  }
}

// ── Phase 4: Pyodide renderer ─────────────────────────────────────────────────

class PyodideRenderer {
  constructor() {
    this._worker      = null;
    this._pending     = new Map();   // id → { resolve, reject }
    this._seq         = 0;
    this._ready       = false;
    this._initPromise = null;
    this._fatal       = false;
  }

  /** Idempotent — safe to call multiple times. */
  init() {
    if (this._initPromise) return this._initPromise;

    this._initPromise = new Promise((resolve, reject) => {
      try {
        this._worker = new Worker('/pyodide_worker.js');
      } catch (e) {
        this._fatal = true;
        reject(e);
        return;
      }

      this._worker.onmessage = ({ data }) => {
        const { id, type, html, error, message } = data;

        if (type === 'status') { showStatus(message); return; }

        if (type === 'ready') {
          this._ready = true;
          showStatus('Python (WASM) ready ✓');
          resolve();
          return;
        }

        if (type === 'fatal') {
          this._fatal = true;
          reject(new Error(error));
          return;
        }

        const cb = this._pending.get(id);
        if (!cb) return;
        this._pending.delete(id);
        type === 'error' ? cb.reject(new Error(error)) : cb.resolve(html);
      };

      this._worker.onerror = e => {
        this._fatal = true;
        reject(new Error(e.message || 'Worker error'));
      };
    });

    return this._initPromise;
  }

  get isReady() { return this._ready; }
  get hasFailed() { return this._fatal; }

  /** Send markdown → receive rendered HTML body. Rejects if not ready. */
  render(markdown) {
    return new Promise((resolve, reject) => {
      const id = ++this._seq;
      this._pending.set(id, { resolve, reject });
      this._worker.postMessage({ id, type: 'render', markdown });
    });
  }
}

// ── Backend: File System Access API (Phase 3 / PWA) ──────────────────────────

class LocalFsBackend {
  constructor() {
    this.dirHandle = null;          // FileSystemDirectoryHandle
    this._pyodide  = new PyodideRenderer();

    // Eagerly start loading Pyodide in the background; failures are silent
    // (render() gracefully falls back to marked.js)
    this._pyodide.init().catch(() => {});
  }

  async openFolder() {
    this.dirHandle = await window.showDirectoryPicker({ mode: 'readwrite' });
  }

  async render(markdown, dark /*, basePath — ignored in standalone */) {
    // Tier 1 — Pyodide + markdown2 (same quality as the Python server)
    if (this._pyodide.isReady) {
      try {
        const bodyHtml = await this._pyodide.render(markdown);
        return buildStandaloneHtml(bodyHtml, dark);
      } catch { /* fall through */ }
    }

    // Tier 2 — marked.js (fast, loaded from CDN in index.html)
    if (typeof marked !== 'undefined') {
      return buildStandaloneHtml(marked.parse(markdown || ''), dark);
    }

    // Tier 3 — placeholder while both are loading
    return buildStandaloneHtml(
      '<p style="color:#888"><em>Renderer loading…</em></p>', dark
    );
  }

  async listFiles(dir = '') {
    if (!this.dirHandle) return { files: [], dir: '' };
    const handle = dir ? await this._resolveDirPath(dir) : this.dirHandle;
    const files = [];
    for await (const [name, entry] of handle.entries()) {
      if (entry.kind === 'directory' && !name.startsWith('.')) {
        files.push({ name, path: dir ? `${dir}/${name}` : name, type: 'dir' });
      } else if (entry.kind === 'file' && name.toLowerCase().endsWith('.md')) {
        const file = await entry.getFile();
        files.push({
          name,
          path: dir ? `${dir}/${name}` : name,
          type: 'file',
          size: file.size,
          modified: file.lastModified / 1000,
        });
      }
    }
    files.sort((a, b) => {
      if (a.type !== b.type) return a.type === 'dir' ? -1 : 1;
      return a.name.localeCompare(b.name);
    });
    return { files, dir };
  }

  async readFile(path) {
    const parts = path.split('/');
    let handle = this.dirHandle;
    for (const part of parts.slice(0, -1)) {
      handle = await handle.getDirectoryHandle(part);
    }
    const fh = await handle.getFileHandle(parts.at(-1));
    const file = await fh.getFile();
    const content = await file.text();
    return { content, path, name: parts.at(-1) };
  }

  async writeFile(path, content) {
    const parts = path.split('/');
    let handle = this.dirHandle;
    for (const part of parts.slice(0, -1)) {
      handle = await handle.getDirectoryHandle(part, { create: true });
    }
    const fh = await handle.getFileHandle(parts.at(-1), { create: true });
    const writable = await fh.createWritable();
    await writable.write(content);
    await writable.close();
    return { ok: true, path };
  }

  async exportWord(markdown, filename) {
    // No Python server available — download raw Markdown instead
    const mdName = filename.replace(/\.docx$/i, '.md');
    _triggerDownload(new Blob([markdown], { type: 'text/markdown' }), mdName);
    showStatus('Saved as Markdown (Word export needs local server)', false);
  }

  async _resolveDirPath(relPath) {
    let handle = this.dirHandle;
    for (const part of relPath.split('/')) {
      handle = await handle.getDirectoryHandle(part);
    }
    return handle;
  }
}

// ── Backend detection ─────────────────────────────────────────────────────────

let backend = null;
let backendMode = 'none';

async function detectBackend() {
  // 1. Try the Python API server (Phase 1 local / Phase 2 Docker)
  try {
    const ctrl = new AbortController();
    const tid  = setTimeout(() => ctrl.abort(), 1500);
    const resp = await fetch('/api/health', { signal: ctrl.signal });
    clearTimeout(tid);
    if (resp.ok) {
      backend     = new ApiBackend();
      backendMode = 'api';
      _updateModeBadge('🖥 Local server');
      return;
    }
  } catch { /* server not running */ }

  // 2. File System Access API (Phase 3 PWA / standalone)
  if (typeof window.showDirectoryPicker === 'function') {
    backend     = new LocalFsBackend();
    backendMode = 'local';
    _updateModeBadge('📁 File System');
    document.getElementById('btn-open-folder').classList.remove('hidden');
    showStatus('Standalone mode — click 📂 Open Folder to browse files');
    return;
  }

  // 3. No backend — preview-only
  backendMode = 'none';
  _updateModeBadge('⚠ Preview only');
  showStatus('Run  pymd serve  to enable file operations', true);
}

function _updateModeBadge(label) {
  const el = document.getElementById('mode-badge');
  if (el) el.textContent = label;
}

// ── State ─────────────────────────────────────────────────────────────────────

const state = {
  currentPath: null,
  content:     '',
  dirty:       false,
  dark:        false,
  treeDir:     '',
  renderTimer: null,
  statusTimer: null,
  viewMode:    'split',    // split | source | preview | wysiwyg | pdf
};

// ── DOM refs ──────────────────────────────────────────────────────────────────

const elEditor    = document.getElementById('editor');
const elPreview   = document.getElementById('preview');
const elFilename  = document.getElementById('filename');
const elDirty     = document.getElementById('dirty-indicator');
const elStatus    = document.getElementById('status');
const elWordcount = document.getElementById('wordcount');
const elFileTree  = document.getElementById('file-tree');
const elStatusbar = document.querySelector('.statusbar');
const elSaveasModal = document.getElementById('saveas-modal');

// ── Boot ──────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', async () => {
  _injectModeBadge();
  wireEvents();
  registerServiceWorker();

  await detectBackend();

  if (backendMode === 'api') {
    await loadFileTree('');
  }
  await renderPreview();
});

function _injectModeBadge() {
  const badge = document.createElement('span');
  badge.id        = 'mode-badge';
  badge.className = 'mode-badge';
  badge.textContent = '…';
  document.querySelector('.statusbar').appendChild(badge);
}

function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {/* ignore */});
  }
}

// ── Event wiring ──────────────────────────────────────────────────────────────

function wireEvents() {
  elEditor.addEventListener('input', onEditorInput);
  document.addEventListener('keydown', onKeydown);

  document.getElementById('btn-new').addEventListener('click', newFile);
  document.getElementById('btn-new-file').addEventListener('click', promptNewFile);
  document.getElementById('btn-save').addEventListener('click', saveFile);
  document.getElementById('btn-export-word').addEventListener('click', exportWord);
  document.getElementById('btn-print').addEventListener('click', triggerPrint);
  document.getElementById('btn-open-folder').addEventListener('click', openFolder);

  document.getElementById('dark-toggle').addEventListener('change', e => {
    state.dark = e.target.checked;
    document.body.classList.toggle('dark', state.dark);
    renderPreview();
  });

  document.getElementById('saveas-cancel').addEventListener('click', closeSaveAsModal);
  document.getElementById('saveas-confirm').addEventListener('click', confirmSaveAs);
  document.getElementById('saveas-input').addEventListener('keydown', e => {
    if (e.key === 'Enter')  confirmSaveAs();
    if (e.key === 'Escape') closeSaveAsModal();
  });
  elSaveasModal.addEventListener('click', e => {
    if (e.target === elSaveasModal) closeSaveAsModal();
  });
}

// ── Editor input ──────────────────────────────────────────────────────────────

function onEditorInput() {
  state.content = elEditor.value;
  setDirty(true);
  updateWordCount();
  debounceRender();
}

function debounceRender() {
  clearTimeout(state.renderTimer);
  state.renderTimer = setTimeout(renderPreview, 280);
}

function updateWordCount() {
  const words = state.content.trim() ? state.content.trim().split(/\s+/).length : 0;
  elWordcount.textContent = words + ' word' + (words !== 1 ? 's' : '');
}

// ── Preview rendering ─────────────────────────────────────────────────────────

async function renderPreview() {
  if (!backend) return;
  if (state.viewMode === 'wysiwyg') { _syncWysiwygFromState(); return; }
  if (state.viewMode === 'pdf')     { return; }

  // Preserve scroll position across re-renders
  const savedY = elPreview.contentWindow?.scrollY ?? 0;

  try {
    const basePath = state.currentPath
      ? state.currentPath.split('/').slice(0, -1).join('/') || null
      : null;
    const html = await backend.render(state.content, state.dark, basePath);
    elPreview.srcdoc = html;
    elPreview.addEventListener('load', () => {
      elPreview.contentWindow?.scrollTo(0, savedY);
    }, { once: true });
  } catch (err) {
    console.error('[pymd] render error:', err);
  }
}

// ── File tree ─────────────────────────────────────────────────────────────────

async function loadFileTree(dir = '') {
  if (!backend || backendMode === 'none') return;
  state.treeDir = dir;
  try {
    const { files, dir: currentDir } = await backend.listFiles(dir);
    renderFileTree(files, currentDir);
  } catch (err) {
    console.error('[pymd] file tree error:', err);
  }
}

function renderFileTree(files, currentDir) {
  elFileTree.innerHTML = '';

  if (currentDir) {
    const parts  = currentDir.split('/');
    const parent = parts.length > 1 ? parts.slice(0, -1).join('/') : '';
    const back   = makeTreeItem('↑ ..', '', true);
    back.classList.add('back');
    back.addEventListener('click', () => loadFileTree(parent));
    elFileTree.appendChild(back);
  }

  if (!files.length) {
    const empty = document.createElement('div');
    empty.className = 'file-empty';
    empty.textContent = 'No .md files here';
    elFileTree.appendChild(empty);
    return;
  }

  for (const f of files) {
    const icon = f.type === 'dir' ? '📁' : '📄';
    const item = makeTreeItem(`${icon} ${f.name}`, f.path, f.type === 'dir');
    if (f.path === state.currentPath) item.classList.add('active');

    item.addEventListener('click', () =>
      f.type === 'dir' ? loadFileTree(f.path) : openFile(f.path)
    );
    elFileTree.appendChild(item);
  }
}

function makeTreeItem(label, path, isDir) {
  const el = document.createElement('div');
  el.className   = 'file-item' + (isDir ? ' dir' : '');
  el.dataset.path = path;
  el.textContent  = label;
  el.setAttribute('role', 'treeitem');
  return el;
}

// ── File open / save / new ────────────────────────────────────────────────────

async function openFile(path) {
  if (!backend) return;
  if (state.dirty && !confirmDiscard()) return;
  try {
    const { content, path: filePath, name } = await backend.readFile(path);
    state.currentPath = filePath;
    state.content     = content;
    elEditor.value    = content;
    elFilename.textContent = name;
    setDirty(false);
    updateWordCount();
    highlightActiveFile(filePath);
    await renderPreview();
    showStatus('Opened: ' + name);
  } catch (err) {
    showStatus('Error opening file', true);
    console.error(err);
  }
}

async function newFile() {
  if (state.dirty && !confirmDiscard()) return;
  state.currentPath = null;
  state.content     = '';
  elEditor.value    = '';
  elFilename.textContent = 'untitled.md';
  setDirty(false);
  updateWordCount();
  highlightActiveFile(null);
  await renderPreview();
}

async function saveFile() {
  if (!backend || backendMode === 'none') {
    showStatus('No backend — run  pymd serve  to save files', true);
    return;
  }
  if (!state.currentPath) { openSaveAsModal(); return; }
  await doSave(state.currentPath);
}

async function doSave(path) {
  try {
    const { path: savedPath } = await backend.writeFile(path, state.content);
    state.currentPath = savedPath;
    elFilename.textContent = savedPath.split('/').pop();
    setDirty(false);
    highlightActiveFile(savedPath);
    await loadFileTree(state.treeDir);
    showStatus('Saved ✓');
  } catch (err) {
    showStatus('Save failed', true);
    console.error(err);
  }
}

// ── Folder picker (Phase 3 standalone) ───────────────────────────────────────

async function openFolder() {
  if (backendMode !== 'local') return;
  try {
    await backend.openFolder();
    await loadFileTree('');
    showStatus('Folder opened: ' + backend.dirHandle.name);
  } catch (err) {
    if (err.name !== 'AbortError') {
      showStatus('Could not open folder', true);
    }
  }
}

// ── Save-As modal ─────────────────────────────────────────────────────────────

function openSaveAsModal() {
  const input = document.getElementById('saveas-input');
  input.value = state.currentPath || 'untitled.md';
  elSaveasModal.classList.add('open');
  setTimeout(() => { input.focus(); input.select(); }, 40);
}

function closeSaveAsModal() {
  elSaveasModal.classList.remove('open');
}

function confirmSaveAs() {
  let name = document.getElementById('saveas-input').value.trim();
  if (!name) return;
  if (!name.toLowerCase().endsWith('.md')) name += '.md';
  closeSaveAsModal();
  doSave(name);
}

function promptNewFile() {
  newFile().then(openSaveAsModal);
}

// ── Export ────────────────────────────────────────────────────────────────────

async function exportWord() {
  if (!state.content.trim()) { showStatus('Nothing to export', true); return; }
  if (!backend) { showStatus('No backend available', true); return; }

  const base  = state.currentPath
    ? state.currentPath.split('/').pop().replace(/\.md$/i, '')
    : 'document';
  const fname = base + '.docx';

  try {
    showStatus('Exporting…');
    await backend.exportWord(state.content, fname);
    showStatus('Exported: ' + fname);
  } catch (err) {
    showStatus('Export failed', true);
    console.error(err);
  }
}

function triggerPrint() {
  try {
    elPreview.contentWindow.focus();
    elPreview.contentWindow.print();
  } catch { window.print(); }
}

// ── Keyboard shortcuts ────────────────────────────────────────────────────────

function onKeydown(e) {
  const mod = e.ctrlKey || e.metaKey;
  if (mod && e.key === 's') { e.preventDefault(); saveFile(); }
  if (mod && e.key === 'n') { e.preventDefault(); newFile(); }
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function setDirty(d) {
  state.dirty = d;
  elDirty.textContent = d ? '●' : '';
}

function showStatus(msg, isError = false) {
  elStatus.textContent = msg;
  elStatusbar.classList.toggle('error', isError);
  clearTimeout(state.statusTimer);
  state.statusTimer = setTimeout(() => {
    elStatus.textContent = 'Ready — PyMD Editor';
    elStatusbar.classList.remove('error');
  }, 3500);
}

function confirmDiscard() {
  return confirm('You have unsaved changes. Discard them?');
}

function highlightActiveFile(path) {
  document.querySelectorAll('.file-item').forEach(el =>
    el.classList.toggle('active', el.dataset.path === path)
  );
}

function _triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a   = document.createElement('a');
  a.href     = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}


// ============================================================================
// FORMATTING TOOLBAR  (Module M)
// ============================================================================

const FMT_ACTIONS = {
  bold:      { wrap: ['**', '**'],        sample: 'bold text' },
  italic:    { wrap: ['_', '_'],          sample: 'italic text' },
  strike:    { wrap: ['~~', '~~'],        sample: 'strikethrough' },
  code:      { wrap: ['`', '`'],          sample: 'code' },
  codeblock: { wrap: ['\n```\n', '\n```\n'], sample: 'code here' },
  link:      { wrap: ['[', '](url)'],     sample: 'link text' },
  image:     { wrap: ['![', '](url)'],    sample: 'alt text' },
};

const FMT_LINE_ACTIONS = {
  h1:    '# ',
  h2:    '## ',
  h3:    '### ',
  ul:    '- ',
  ol:    '1. ',
  quote: '> ',
};

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.fmt-btn').forEach(btn => {
    btn.addEventListener('click', () => applyFormat(btn.dataset.action));
  });
});

function applyFormat(action) {
  if (action === 'hr') {
    insertAtCursor('\n\n---\n\n');
    return;
  }
  if (action === 'table') {
    insertAtCursor('\n| Column 1 | Column 2 | Column 3 |\n|----------|----------|----------|\n| Cell     | Cell     | Cell     |\n');
    return;
  }
  if (action in FMT_LINE_ACTIONS) {
    toggleLinePrefix(FMT_LINE_ACTIONS[action]);
    return;
  }
  if (action in FMT_ACTIONS) {
    const { wrap, sample } = FMT_ACTIONS[action];
    wrapSelection(wrap[0], wrap[1], sample);
  }
}

function wrapSelection(before, after, sample) {
  const start = elEditor.selectionStart;
  const end   = elEditor.selectionEnd;
  const sel   = elEditor.value.slice(start, end) || sample;
  const newVal = elEditor.value.slice(0, start) + before + sel + after + elEditor.value.slice(end);
  elEditor.value = newVal;
  elEditor.selectionStart = start + before.length;
  elEditor.selectionEnd   = start + before.length + sel.length;
  elEditor.focus();
  onEditorInput();
}

function insertAtCursor(text) {
  const pos = elEditor.selectionStart;
  elEditor.value = elEditor.value.slice(0, pos) + text + elEditor.value.slice(pos);
  elEditor.selectionStart = elEditor.selectionEnd = pos + text.length;
  elEditor.focus();
  onEditorInput();
}

function toggleLinePrefix(prefix) {
  const start = elEditor.selectionStart;
  const lineStart = elEditor.value.lastIndexOf('\n', start - 1) + 1;
  const lineVal   = elEditor.value.slice(lineStart);
  if (lineVal.startsWith(prefix)) {
    elEditor.value = elEditor.value.slice(0, lineStart) + lineVal.slice(prefix.length);
    elEditor.selectionStart = elEditor.selectionEnd = Math.max(lineStart, start - prefix.length);
  } else {
    elEditor.value = elEditor.value.slice(0, lineStart) + prefix + lineVal;
    elEditor.selectionStart = elEditor.selectionEnd = start + prefix.length;
  }
  elEditor.focus();
  onEditorInput();
}


// ============================================================================
// VIEW TOGGLE  (Module M2)
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
  ['split', 'source', 'preview', 'wysiwyg'].forEach(mode => {
    const btn = document.getElementById('vbtn-' + mode);
    if (btn) btn.addEventListener('click', () => setViewMode(mode));
  });
});

function setViewMode(mode) {
  const edPane  = document.getElementById('editor-pane');
  const prPane  = document.getElementById('preview-pane');
  const fmtBar  = document.getElementById('fmt-toolbar');
  const elWy    = document.getElementById('wysiwyg-editor');
  const elTa    = document.getElementById('editor');

  // Leaving WYSIWYG: sync edits back to state before switching away
  if (state.viewMode === 'wysiwyg' && mode !== 'wysiwyg') {
    _syncStateFromWysiwyg();
  }
  // Leaving PDF viewer: restore markdown preview
  if (state.viewMode === 'pdf' && mode !== 'pdf') {
    _closePdfViewer();
  }

  state.viewMode = mode;

  document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
  const activeBtn = document.getElementById('vbtn-' + mode);
  if (activeBtn) activeBtn.classList.add('active');

  // Default: textarea visible, wysiwyg hidden
  elTa?.classList.remove('hidden');
  elWy?.classList.add('hidden');

  if (mode === 'split') {
    edPane.classList.remove('hidden');
    prPane.classList.remove('hidden');
    fmtBar?.classList.remove('hidden');
    renderPreview();
  } else if (mode === 'source') {
    edPane.classList.remove('hidden');
    prPane.classList.add('hidden');
    fmtBar?.classList.remove('hidden');
  } else if (mode === 'preview') {
    edPane.classList.add('hidden');
    prPane.classList.remove('hidden');
    fmtBar?.classList.add('hidden');
    renderPreview();
  } else if (mode === 'wysiwyg') {
    edPane.classList.remove('hidden');
    prPane.classList.add('hidden');
    fmtBar?.classList.remove('hidden');
    elTa?.classList.add('hidden');
    elWy?.classList.remove('hidden');
    _syncWysiwygFromState();
  }
}


// ============================================================================
// FILE MANAGEMENT  (Module F)
// ============================================================================

// ── State ─────────────────────────────────────────────────────────────────────
let ctxTargetPath = null;    // path of item that was right-clicked
let pdfActivePath = null;    // currently selected PDF
const mergePaths  = [];      // list for PDF merge

// ── Boot ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  setupFileManagement();
  setupPdfModal();
  setupDragDrop();
  loadRecentFiles();
});

// ── Context menu ──────────────────────────────────────────────────────────────

function setupFileManagement() {
  const ctxMenu = document.getElementById('ctx-menu');

  // Close on outside click
  document.addEventListener('click', e => {
    if (!ctxMenu.contains(e.target)) ctxMenu.classList.add('hidden');
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') ctxMenu.classList.add('hidden');
  });

  document.getElementById('ctx-rename').addEventListener('click', () => {
    ctxMenu.classList.add('hidden');
    if (ctxTargetPath) openRenameModal(ctxTargetPath);
  });

  document.getElementById('ctx-delete').addEventListener('click', async () => {
    ctxMenu.classList.add('hidden');
    if (ctxTargetPath) await deleteFileWithConfirm(ctxTargetPath);
  });

  document.getElementById('ctx-info').addEventListener('click', () => {
    ctxMenu.classList.add('hidden');
    if (ctxTargetPath) showFileInfo(ctxTargetPath);
  });

  // Create folder
  document.getElementById('btn-new-folder').addEventListener('click', openNewFolderModal);

  document.getElementById('newfolder-cancel').addEventListener('click', () =>
    document.getElementById('newfolder-modal').classList.remove('open')
  );
  document.getElementById('newfolder-confirm').addEventListener('click', confirmCreateFolder);
  document.getElementById('newfolder-input').addEventListener('keydown', e => {
    if (e.key === 'Enter')  confirmCreateFolder();
    if (e.key === 'Escape') document.getElementById('newfolder-modal').classList.remove('open');
  });

  // Rename modal
  document.getElementById('rename-cancel').addEventListener('click', () =>
    document.getElementById('rename-modal').classList.remove('open')
  );
  document.getElementById('rename-confirm').addEventListener('click', confirmRename);
  document.getElementById('rename-input').addEventListener('keydown', e => {
    if (e.key === 'Enter')  confirmRename();
    if (e.key === 'Escape') document.getElementById('rename-modal').classList.remove('open');
  });
}

function showContextMenu(e, path) {
  e.preventDefault();
  ctxTargetPath = path;
  const menu = document.getElementById('ctx-menu');
  menu.classList.remove('hidden');
  menu.style.left = Math.min(e.clientX, window.innerWidth  - 160) + 'px';
  menu.style.top  = Math.min(e.clientY, window.innerHeight - 120) + 'px';
}

// ── Rename ────────────────────────────────────────────────────────────────────

function openRenameModal(path) {
  const input = document.getElementById('rename-input');
  input.value = path.split('/').pop();
  document.getElementById('rename-modal').classList.add('open');
  setTimeout(() => { input.focus(); input.select(); }, 40);
}

async function confirmRename() {
  const newName = document.getElementById('rename-input').value.trim();
  document.getElementById('rename-modal').classList.remove('open');
  if (!newName || !ctxTargetPath) return;

  try {
    const resp = await fetch('/api/file/rename', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: ctxTargetPath, new_name: newName }),
    });
    if (!resp.ok) { const d = await resp.json(); throw new Error(d.detail); }
    const { path: newPath } = await resp.json();
    if (state.currentPath === ctxTargetPath) {
      state.currentPath = newPath;
      elFilename.textContent = newName;
    }
    showStatus('Renamed ✓');
    loadFileTree(state.treeDir);
  } catch (err) {
    showStatus('Rename failed: ' + err.message, true);
  }
}

// ── Delete ────────────────────────────────────────────────────────────────────

async function deleteFileWithConfirm(path) {
  const name = path.split('/').pop();
  if (!confirm(`Delete "${name}"? This cannot be undone.`)) return;

  try {
    const resp = await fetch('/api/file?path=' + encodeURIComponent(path), { method: 'DELETE' });
    if (!resp.ok) { const d = await resp.json(); throw new Error(d.detail); }
    if (state.currentPath === path) await newFile();
    showStatus('Deleted: ' + name);
    loadFileTree(state.treeDir);
  } catch (err) {
    showStatus('Delete failed: ' + err.message, true);
  }
}

// ── Create folder ─────────────────────────────────────────────────────────────

function openNewFolderModal() {
  const input = document.getElementById('newfolder-input');
  input.value = '';
  document.getElementById('newfolder-modal').classList.add('open');
  setTimeout(() => input.focus(), 40);
}

async function confirmCreateFolder() {
  const name = document.getElementById('newfolder-input').value.trim();
  document.getElementById('newfolder-modal').classList.remove('open');
  if (!name) return;

  const folderPath = state.treeDir ? state.treeDir + '/' + name : name;
  try {
    const resp = await fetch('/api/folder', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: folderPath }),
    });
    if (!resp.ok) { const d = await resp.json(); throw new Error(d.detail); }
    showStatus('Folder created: ' + name);
    loadFileTree(state.treeDir);
  } catch (err) {
    showStatus('Failed: ' + err.message, true);
  }
}

// ── File info ─────────────────────────────────────────────────────────────────

async function showFileInfo(path) {
  try {
    const ext = path.split('.').pop().toLowerCase();
    if (ext === 'pdf') {
      const r = await fetch('/api/pdf/info?path=' + encodeURIComponent(path));
      const d = await r.json();
      alert(`📄 ${d.name}\nPages: ${d.pages}\nTitle: ${d.title || '—'}\nAuthor: ${d.author || '—'}\nSize: ${(d.size_bytes/1024).toFixed(1)} KB`);
    } else {
      alert(`📝 ${path.split('/').pop()}`);
    }
  } catch { /* ignore */ }
}

// ── Drag-and-drop: open by dropping files onto editor ────────────────────────

function setupDragDrop() {
  const drop = document.getElementById('editor-pane') || document.body;
  drop.addEventListener('dragover', e => { e.preventDefault(); drop.classList.add('drag-over'); });
  drop.addEventListener('dragleave', () => drop.classList.remove('drag-over'));
  drop.addEventListener('drop', async e => {
    e.preventDefault();
    drop.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (!file) return;
    if (file.name.endsWith('.md')) {
      if (state.dirty && !confirmDiscard()) return;
      const content = await file.text();
      state.content = content;
      state.currentPath = null;
      elEditor.value = content;
      elFilename.textContent = file.name + ' (unsaved)';
      setDirty(true);
      updateWordCount();
      await renderPreview();
    } else if (file.name.endsWith('.pdf') && backendMode === 'api') {
      showStatus('Drop PDF onto sidebar to use PDF Tools', false);
    }
  });
}

// ── Recent files (localStorage) ───────────────────────────────────────────────

const RECENT_KEY = 'pymd-recent-v1';

function addToRecent(path, name) {
  let recent = JSON.parse(localStorage.getItem(RECENT_KEY) || '[]');
  recent = recent.filter(r => r.path !== path);
  recent.unshift({ path, name, ts: Date.now() });
  recent = recent.slice(0, 10);
  localStorage.setItem(RECENT_KEY, JSON.stringify(recent));
}

function loadRecentFiles() {
  // Only show recent files if the tree is empty and we have API backend
  // (they get shown before the first folder is loaded)
}

// ── Extend renderFileTree to add context menus + PDF class ───────────────────

const _origRenderFileTree = renderFileTree;
// Override to add context-menu and PDF support
window.renderFileTree = function(files, currentDir) {
  elFileTree.innerHTML = '';

  if (currentDir) {
    const parts  = currentDir.split('/');
    const parent = parts.length > 1 ? parts.slice(0, -1).join('/') : '';
    const back   = makeTreeItem('↑ ..', '', true);
    back.classList.add('back');
    back.addEventListener('click', () => loadFileTree(parent));
    elFileTree.appendChild(back);
  }

  const recent = JSON.parse(localStorage.getItem(RECENT_KEY) || '[]');
  if (!files.length && !currentDir && recent.length) {
    const hdr = document.createElement('div');
    hdr.className   = 'recent-header';
    hdr.textContent = 'Recent';
    elFileTree.appendChild(hdr);
    for (const r of recent.slice(0, 5)) {
      const item = makeTreeItem('🕐 ' + r.name, r.path, false);
      item.addEventListener('click', () => openFile(r.path));
      item.addEventListener('contextmenu', e => showContextMenu(e, r.path));
      elFileTree.appendChild(item);
    }
    return;
  }

  if (!files.length) {
    const empty = document.createElement('div');
    empty.className = 'file-empty';
    empty.textContent = 'No files here';
    elFileTree.appendChild(empty);
    return;
  }

  for (const f of files) {
    const isPdf = f.ext === 'pdf';
    const icon  = f.type === 'dir' ? '📁' : (isPdf ? '📑' : '📄');
    const item  = makeTreeItem(`${icon} ${f.name}`, f.path, f.type === 'dir');
    if (isPdf) item.classList.add('pdf');
    if (f.path === state.currentPath) item.classList.add('active');

    if (f.type === 'dir') {
      item.addEventListener('click', () => loadFileTree(f.path));
    } else if (isPdf) {
      item.addEventListener('click', () => selectPdf(f.path));
      item.addEventListener('contextmenu', e => showContextMenu(e, f.path));
    } else {
      item.addEventListener('click', () => {
        openFile(f.path);
        addToRecent(f.path, f.name);
      });
      item.addEventListener('contextmenu', e => showContextMenu(e, f.path));
    }
    elFileTree.appendChild(item);
  }
};

// Patch loadFileTree to use types=md,pdf
const _origLoadFileTree = loadFileTree;
window.loadFileTree = async function(dir = '') {
  if (!backend || backendMode === 'none') return;
  state.treeDir = dir;
  try {
    const url  = `/api/files?dir=${encodeURIComponent(dir)}&types=md,pdf`;
    const resp = await fetch(url);
    if (!resp.ok) return;
    const { files, dir: currentDir } = await resp.json();
    window.renderFileTree(files, currentDir);
  } catch (err) {
    console.error('[pymd] file tree error:', err);
  }
};


// ============================================================================
// PDF TOOLS  (Module P)
// ============================================================================

function selectPdf(path) {
  pdfActivePath = path;
  updatePdfInfoBar(path);
  syncPdfPathDisplays(path);
  highlightActiveFile(path);
  _openPdfViewer(path);
}

async function updatePdfInfoBar(path) {
  const bar = document.getElementById('pdf-info-bar');
  if (!path) { bar.textContent = 'No PDF selected'; return; }
  bar.textContent = 'Loading…';
  try {
    const resp = await fetch('/api/pdf/info?path=' + encodeURIComponent(path));
    if (!resp.ok) throw new Error();
    const d = await resp.json();
    bar.textContent = `${d.name}  ·  ${d.pages} pages  ·  ${(d.size_bytes/1024).toFixed(0)} KB  ·  ${d.title || ''}`;
  } catch {
    bar.textContent = path.split('/').pop();
  }
}

function syncPdfPathDisplays(path) {
  const name = path ? path.split('/').pop() : '—';
  const ids  = ['pdf-toword-path','pdf-toexcel-path','pdf-insert-base'];
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = name || '—';
  });
}

function setupPdfModal() {
  // Tab switching
  document.querySelectorAll('.pdf-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.pdf-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.pdf-tab-content').forEach(c => c.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById('pdf-tab-' + tab.dataset.tab)?.classList.add('active');
    });
  });

  // Open/close
  document.getElementById('btn-pdf-tools').addEventListener('click', () => {
    document.getElementById('pdf-modal').classList.add('open');
    if (pdfActivePath) updatePdfInfoBar(pdfActivePath);
  });
  document.getElementById('pdf-modal-close').addEventListener('click', () =>
    document.getElementById('pdf-modal').classList.remove('open')
  );
  document.getElementById('pdf-modal').addEventListener('click', e => {
    if (e.target === document.getElementById('pdf-modal'))
      document.getElementById('pdf-modal').classList.remove('open');
  });

  // Extract
  document.getElementById('btn-pdf-extract').addEventListener('click', pdfExtract);

  // Merge
  document.getElementById('btn-pdf-merge-add').addEventListener('click', () => {
    if (pdfActivePath) addToMergeList(pdfActivePath);
    else showStatus('Select a PDF in the tree first', true);
  });
  document.getElementById('btn-pdf-merge-clear').addEventListener('click', () => {
    mergePaths.length = 0;
    document.getElementById('pdf-merge-list').innerHTML = '';
  });
  document.getElementById('btn-pdf-merge').addEventListener('click', pdfMerge);

  // Insert
  document.getElementById('btn-pdf-insert-pick').addEventListener('click', () => {
    if (pdfActivePath) {
      document.getElementById('pdf-insert-src').textContent = pdfActivePath.split('/').pop();
      document.getElementById('pdf-insert-src').dataset.path = pdfActivePath;
      showStatus('Insert source set: ' + pdfActivePath.split('/').pop());
    } else {
      showStatus('Select a PDF in the tree first', true);
    }
  });
  document.getElementById('btn-pdf-insert').addEventListener('click', pdfInsert);

  // To Word / Excel
  document.getElementById('btn-pdf-toword').addEventListener('click',  pdfToWord);
  document.getElementById('btn-pdf-toexcel').addEventListener('click', pdfToExcel);
}

// ── Merge list helpers ────────────────────────────────────────────────────────

function addToMergeList(path) {
  if (mergePaths.includes(path)) return;
  mergePaths.push(path);
  const list = document.getElementById('pdf-merge-list');
  const item = document.createElement('div');
  item.className = 'pdf-merge-item';
  item.dataset.path = path;
  item.innerHTML = `<span>${path.split('/').pop()}</span><button title="Remove">×</button>`;
  item.querySelector('button').addEventListener('click', () => {
    mergePaths.splice(mergePaths.indexOf(path), 1);
    item.remove();
  });
  list.appendChild(item);
}

// ── PDF operations ────────────────────────────────────────────────────────────

async function pdfExtract() {
  if (!pdfActivePath) { showStatus('Select a PDF first', true); return; }
  const pages = document.getElementById('pdf-extract-pages').value.trim();
  if (!pages) { showStatus('Enter page range (e.g. 1-3, 5)', true); return; }
  await _pdfApiDownload('/api/pdf/extract', { path: pdfActivePath, pages });
}

async function pdfMerge() {
  if (mergePaths.length < 2) { showStatus('Add at least 2 PDFs to merge', true); return; }
  const filename = document.getElementById('pdf-merge-filename').value.trim() || 'merged.pdf';
  await _pdfApiDownload('/api/pdf/merge', { paths: [...mergePaths], filename });
}

async function pdfInsert() {
  if (!pdfActivePath) { showStatus('Select base PDF in tree first', true); return; }
  const srcEl = document.getElementById('pdf-insert-src');
  const src   = srcEl.dataset.path;
  if (!src || src === pdfActivePath) {
    showStatus('Pick a different PDF as insert source', true); return;
  }
  const after = parseInt(document.getElementById('pdf-insert-after').value) || 0;
  await _pdfApiDownload('/api/pdf/insert', {
    base: pdfActivePath, insert: src, after_page: after,
  });
}

async function pdfToWord() {
  if (!pdfActivePath) { showStatus('Select a PDF first', true); return; }
  await _pdfApiDownload('/api/pdf/to-word', { path: pdfActivePath });
}

async function pdfToExcel() {
  if (!pdfActivePath) { showStatus('Select a PDF first', true); return; }
  await _pdfApiDownload('/api/pdf/to-excel', { path: pdfActivePath });
}

async function _pdfApiDownload(endpoint, body) {
  showStatus('Processing…');
  try {
    const resp = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!resp.ok) {
      const d = await resp.json().catch(() => ({}));
      throw new Error(d.detail || `HTTP ${resp.status}`);
    }
    const disposition = resp.headers.get('Content-Disposition') || '';
    let fname = disposition.match(/filename="?([^";\n]+)"?/)?.[1] || 'download';
    _triggerDownload(await resp.blob(), fname);
    showStatus('Downloaded: ' + fname);
  } catch (err) {
    showStatus('Error: ' + err.message, true);
    console.error(err);
  }
}


// ============================================================================
// PDF VIEWER  (in-pane browser-native rendering)
// ============================================================================

let _savedViewModeBeforePdf = 'split';  // restore when user leaves PDF

function _openPdfViewer(path) {
  const pdfBar    = document.getElementById('pdf-viewer-bar');
  const pdfIframe = document.getElementById('pdf-viewer');
  const mdIframe  = document.getElementById('preview');
  const paneTitle = document.getElementById('preview-pane-title');
  const prPane    = document.getElementById('preview-pane');
  const edPane    = document.getElementById('editor-pane');
  const fmtBar    = document.getElementById('fmt-toolbar');

  // Save current view mode so we can restore it when switching to an MD file
  if (state.viewMode !== 'pdf') _savedViewModeBeforePdf = state.viewMode;
  state.viewMode = 'pdf';

  // Highlight PDF view button or at least clear existing active state
  document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));

  // Show preview pane (where the PDF will display), hide editor
  edPane.classList.add('hidden');
  prPane.classList.remove('hidden');
  fmtBar?.classList.add('hidden');

  // Swap: hide markdown preview, show PDF viewer
  mdIframe.classList.add('hidden');
  pdfBar.classList.remove('hidden');
  pdfIframe.classList.remove('hidden');

  // Set filename in bar
  const name = path.split(/[/\\]/).pop();
  document.getElementById('pdf-viewer-name').textContent = name;
  paneTitle.textContent = '📑 ' + name;

  // Point iframe at the stream endpoint
  pdfIframe.src = '/api/pdf/stream?path=' + encodeURIComponent(path);

  showStatus('PDF: ' + name);
}

function _closePdfViewer() {
  const pdfBar    = document.getElementById('pdf-viewer-bar');
  const pdfIframe = document.getElementById('pdf-viewer');
  const mdIframe  = document.getElementById('preview');
  const paneTitle = document.getElementById('preview-pane-title');

  pdfBar.classList.add('hidden');
  pdfIframe.classList.add('hidden');
  pdfIframe.src = '';
  mdIframe.classList.remove('hidden');
  paneTitle.textContent = 'Preview';
}

document.addEventListener('DOMContentLoaded', () => {
  // PDF viewer toolbar buttons
  document.getElementById('pdf-viewer-download')?.addEventListener('click', () => {
    if (pdfActivePath) {
      const a = document.createElement('a');
      a.href     = '/api/pdf/stream?path=' + encodeURIComponent(pdfActivePath);
      a.download = pdfActivePath.split(/[/\\]/).pop();
      a.click();
    }
  });
  document.getElementById('pdf-viewer-tools')?.addEventListener('click', () => {
    document.getElementById('pdf-modal')?.classList.add('open');
    if (pdfActivePath) updatePdfInfoBar(pdfActivePath);
  });
});

// Patch openFile to exit PDF view when an MD file is opened
const _origOpenFile = openFile;
window.openFile = async function(path) {
  if (state.viewMode === 'pdf') {
    _closePdfViewer();
    state.viewMode = _savedViewModeBeforePdf;
    setViewMode(_savedViewModeBeforePdf);
  }
  await _origOpenFile(path);
};


// ============================================================================
// WYSIWYG MODE
// ============================================================================

let _turndown = null;
let _wysiwygTimer = null;

function _getTurndown() {
  if (_turndown) return _turndown;
  if (typeof TurndownService === 'undefined') return null;
  _turndown = new TurndownService({
    headingStyle:   'atx',
    bulletListMarker: '-',
    codeBlockStyle: 'fenced',
    emDelimiter:    '_',
    strongDelimiter: '**',
  });
  // Preserve <br> as two spaces + newline
  _turndown.addRule('lineBreak', {
    filter: 'br',
    replacement: () => '  \n',
  });
  return _turndown;
}

/** Render current state.content into the WYSIWYG div. */
function _syncWysiwygFromState() {
  const el = document.getElementById('wysiwyg-editor');
  if (!el) return;
  if (typeof marked === 'undefined') {
    el.innerHTML = '<em style="color:#888">marked.js not loaded — WYSIWYG unavailable</em>';
    return;
  }
  // Only refresh if not actively focused (avoids cursor-jump while typing)
  if (document.activeElement === el) return;
  el.innerHTML = marked.parse(state.content || '');
}

/** Convert WYSIWYG div innerHTML back to Markdown and update state. */
function _syncStateFromWysiwyg() {
  const el = document.getElementById('wysiwyg-editor');
  if (!el) return;
  const td = _getTurndown();
  if (!td) return;
  const md = td.turndown(el.innerHTML || '');
  state.content    = md;
  elEditor.value   = md;
  updateWordCount();
}

/** Handle input events in the WYSIWYG editor (debounced). */
function _onWysiwygInput() {
  clearTimeout(_wysiwygTimer);
  _wysiwygTimer = setTimeout(() => {
    _syncStateFromWysiwyg();
    setDirty(true);
  }, 400);
}

document.addEventListener('DOMContentLoaded', () => {
  const el = document.getElementById('wysiwyg-editor');
  if (!el) return;

  el.addEventListener('input', _onWysiwygInput);

  // Ctrl+B / Ctrl+I in WYSIWYG: use execCommand for native rich-text
  el.addEventListener('keydown', e => {
    if (e.ctrlKey || e.metaKey) {
      if (e.key === 'b') { e.preventDefault(); document.execCommand('bold'); }
      if (e.key === 'i') { e.preventDefault(); document.execCommand('italic'); }
      if (e.key === 's') { e.preventDefault(); _syncStateFromWysiwyg(); saveFile(); }
    }
  });
});

// Extend applyFormat to work in WYSIWYG mode via execCommand
const _origApplyFormat = applyFormat;
window.applyFormat = function(action) {
  if (state.viewMode !== 'wysiwyg') { _origApplyFormat(action); return; }
  const el = document.getElementById('wysiwyg-editor');
  el?.focus();
  switch (action) {
    case 'bold':      document.execCommand('bold');        break;
    case 'italic':    document.execCommand('italic');      break;
    case 'strike':    document.execCommand('strikeThrough'); break;
    case 'ul':        document.execCommand('insertUnorderedList'); break;
    case 'ol':        document.execCommand('insertOrderedList');   break;
    default:          _origApplyFormat(action);  // fall back for other actions
  }
  setTimeout(_onWysiwygInput, 50);
};

