# PyMD Portable Runtime — Migration Plan

> **Constraint**: Data is ALWAYS local to the user.  
> **Runtime** can be: Web (WASM) · Local (localhost server) · User's server (Docker).

---

## Architecture Overview

```
┌──────────────────────────────────────────────────┐
│         Browser (universal UI layer)             │
│  Web App (HTML/CSS/JS)  +  File System Access    │
│               │              (data stays LOCAL)  │
└───────────────┼──────────────────────────────────┘
                │  REST /api/...
        ┌───────▼────────┐
        │   Runtime?     │  ← user picks one
        ├────────────────┤
        │ 1. WASM        │  Pyodide — Python runs IN the browser tab
        │ 2. Local       │  FastAPI on 127.0.0.1 — pip / .exe install
        │ 3. Server      │  Docker on VPS — share URL with team
        └────────────────┘
```

---

## Phase 1 — Local FastAPI Server  ✅ DONE (21/21 tests pass)

**Goal**: `python -m pymd_editor serve` → auto-opens browser at `http://localhost:8765`.  
Existing Qt desktop app is untouched (fully backward compatible).

### Tasks
- [x] `src/pymd_editor/server/__init__.py`
- [x] `src/pymd_editor/server/api.py` — FastAPI app with REST endpoints:
  - `GET  /api/health`
  - `POST /api/render`       render markdown → HTML
  - `GET  /api/files`        list .md files in a directory
  - `GET  /api/file`         read a file
  - `POST /api/file`         write / create a file
  - `DELETE /api/file`       delete a file
  - `POST /api/export/word`  download .docx
- [x] `src/pymd_editor/server/serve.py` — starts uvicorn + opens browser
- [x] `src/pymd_editor/server/static/index.html` — split-pane web UI
- [x] `src/pymd_editor/server/static/style.css`
- [x] `src/pymd_editor/server/static/app.js`
- [x] Update `requirements.txt` — add fastapi, uvicorn
- [x] Update `main.py` — support `serve` subcommand
- [x] Validate with smoke tests (`test_server.py`)

### How to run (after Phase 1)
```bash
# Option A — via main entry point
python -m pymd_editor serve --dir ~/Documents --port 8765

# Option B — direct
python -m pymd_editor.server.serve --dir ~/Documents
```

---

## Phase 2 — Docker / Self-hosted Server  ✅ DONE

**Goal**: `docker run -p 8765:8765 -v ~/docs:/data pymd/editor` → accessible from browser.

### Tasks
- [ ] `Dockerfile` — multi-stage build (Python slim image)
- [ ] `docker-compose.yml` — volume mount for local files
- [ ] Add `--host 0.0.0.0` flag for server mode (localhost-only by default for security)
- [ ] Optional: simple bearer-token auth for shared server deployments
- [ ] `docker_build.sh` / `docker_build.bat` — build helper scripts
- [ ] Publish image to Docker Hub: `pymd/editor`
- [ ] Update website/README with one-liner install

### How to run (after Phase 2)
```bash
docker run -p 8765:8765 -v ~/Documents:/data pymd/editor
# browse → http://localhost:8765
```

---

## Phase 3 — Hosted Web (PWA / Zero-install)  ✅ DONE

**Goal**: User visits a URL, browser shows "Install app" prompt. Works offline.  
Data is accessed via the browser's **File System Access API** (no server needed).

### Tasks
- [ ] Decouple frontend from FastAPI — make backend URL configurable
- [ ] Implement File System Access API adapter in `app.js`
  - `showDirectoryPicker()` for opening a folder
  - `FileSystemFileHandle` for read/write
- [ ] Offline fallback via Service Worker (`sw.js`)
- [ ] `manifest.json` — PWA manifest (icons, name, display: standalone)
- [ ] `sw.js` — cache shell + static assets
- [ ] GitHub Actions workflow: build → deploy to GitHub Pages
- [ ] Test "Install app" flow in Chrome / Edge

### How to use (after Phase 3)
```
Visit → https://<your-gh-pages-url>
Browser: "Add to home screen / Install PyMD Editor"
Click install → works as desktop app, data stays local
```

---

## Phase 4 — Pyodide WASM (no server, no install)  ✅ DONE

**Goal**: Python rendering logic (markdown2, PDF) runs in the browser via WebAssembly.  
Zero backend needed. Fully offline after first page load.

### Tasks
- [ ] Evaluate Pyodide compatibility: `markdown2`, `python-docx`, `pymupdf`
- [ ] Create `pyodide_worker.js` — Web Worker that loads Pyodide + pymd logic
- [ ] Implement message protocol between main thread and Worker
- [ ] Bundle `renderer.py`, `exporter.py` for Pyodide
- [ ] Fallback: if Pyodide fails, route to local server or show install prompt
- [ ] Bundle size optimisation (lazy-load Pyodide only when needed)

### How to use (after Phase 4)
```
Visit URL → markdown renders in browser tab, no server, no install
```

---

## Non-Goals (kept outside scope)
- Real-time collaboration (multi-user editing)
- Cloud storage sync (data stays local per design constraint)
- Mobile native apps

---

## Progress Tracker

| Phase | Status | Target |
|-------|--------|--------|
| 1 — Local FastAPI server + Web UI | ✅ Done (21/21 tests) | ✓ |
| 2 — Docker / self-hosted | ✅ Done | ✓ |
| 3 — Hosted PWA | ✅ Done | ✓ |
| 4 — Pyodide WASM | ✅ Done | ✓ |
