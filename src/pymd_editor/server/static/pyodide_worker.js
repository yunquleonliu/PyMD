/**
 * PyMD Editor — Pyodide Web Worker (Phase 4)
 *
 * Runs Python/markdown2 inside a browser Web Worker via WebAssembly.
 * First load downloads ~25 MB from the Pyodide CDN (cached by browser
 * after that). On slow connections the status messages keep the UI informed.
 *
 * Message protocol
 * ─────────────────
 * Incoming (main → worker):
 *   { id: number, type: 'render', markdown: string }
 *
 * Outgoing (worker → main):
 *   { type: 'status',  message: string }          — progress during init
 *   { type: 'ready' }                             — fully initialised
 *   { id, type: 'result', html: string }          — render result
 *   { id, type: 'error',  error: string }         — render failure
 *   { type: 'fatal',   error: string }            — init failure
 */

'use strict';

const PYODIDE_VERSION = '0.26.4';
const PYODIDE_INDEX   = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

// Load the Pyodide bootstrap script synchronously (classic Worker)
importScripts(PYODIDE_INDEX + 'pyodide.js');

let pyodide = null;

// Python helper installed once Pyodide + markdown2 are ready
const RENDER_PY = `
import markdown2

_EXTRAS = [
    "fenced-code-blocks",
    "tables",
    "strike",
    "task_list",
    "code-friendly",
    "toc",
]

def _render(text):
    return markdown2.markdown(text or "", extras=_EXTRAS)
`;

// ── Initialisation ────────────────────────────────────────────────────────────

async function initialize() {
  post({ type: 'status', message: 'Loading Python runtime (WASM)…' });

  pyodide = await loadPyodide({ indexURL: PYODIDE_INDEX });

  post({ type: 'status', message: 'Installing markdown2…' });

  // micropip is included in the 'full' build
  await pyodide.loadPackage('micropip');
  await pyodide.runPythonAsync(`
import micropip
await micropip.install('markdown2')
`);

  // Compile the render helper once
  pyodide.runPython(RENDER_PY);

  post({ type: 'ready' });
}

// ── Message handler ───────────────────────────────────────────────────────────

self.onmessage = function (e) {
  const { id, type, markdown } = e.data;
  if (type !== 'render') return;

  if (!pyodide) {
    post({ id, type: 'error', error: 'Pyodide not ready yet' });
    return;
  }

  try {
    // Use globals.set to avoid string-escaping issues with raw markdown
    pyodide.globals.set('_md_in', markdown || '');
    const html = pyodide.runPython('_render(_md_in)');
    post({ id, type: 'result', html });
  } catch (err) {
    post({ id, type: 'error', error: String(err) });
  }
};

// ── Helpers ───────────────────────────────────────────────────────────────────

function post(msg) { self.postMessage(msg); }

// Start immediately
initialize().catch(err => post({ type: 'fatal', error: String(err) }));
