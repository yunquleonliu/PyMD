# PyMD — Agent Instructions

PyMD is a Markdown workspace and document conversion tool with a Qt desktop app, a FastAPI web server, and a GitHub Pages demo. See [README.md](README.md) for the overview and [ARCHITECTURE_v2.0.md](ARCHITECTURE_v2.0.md) for design decisions.

---

## Build & Run

| Goal | Command |
|------|---------|
| Desktop app | `python -m pymd_editor.main` |
| Web server (local) | `python -m pymd_editor.server.serve --dir data --host 127.0.0.1 --port 8765 --no-browser` |
| Docker | `docker compose up --build` |
| Windows launcher | `run_editor.bat` |
| Build GitHub Pages | `python build_web.py --out docs --base-url /PyMD/` |
| Build Windows EXE | `pyinstaller build_exe.spec --noconfirm` |
| Install deps | `pip install -r requirements.txt` |
| Install package | `pip install -e .` ← **required after cloning** (`src/` layout) |

Requires **Python 3.9+**. The `.venv/` virtual environment is used by `run_editor.bat` if present.

---

## Source Layout

```
src/pymd_editor/
  main.py              # entry point; routes Qt vs. web mode
  app.py               # MainWindow (Qt GUI)
  renderer.py          # Markdown → HTML
  exporter.py          # Word / PDF export
  wysiwyg_editor.py    # WYSIWYG editing mode
  three_column_layout.py  # 3-pane layout + AI panel
  ai_framework.py      # AIProvider abstraction
  ai_settings.py       # AI configuration UI
  chat_components.py   # Chat UI widgets
  pdf_tools.py         # PDF viewer / merge / split
  html_to_markdown.py  # HTML → Markdown
  updater.py           # self-update
  config.py            # app configuration
  server/
    serve.py           # FastAPI app
    api.py             # REST endpoints
    static/            # web UI assets
```

Key conventions:
- Default language is Chinese (`_current_language = 'zh'`); English variants of docs use `_en` suffix.
- `_dirty` flag tracks unsaved changes; `_current_file` tracks the open file.
- Dark mode is synchronized between editor and preview panes.
- Optional dependencies (server, desktop) are guarded with conditional imports.

---

## Documentation Cleanup

The root folder contains **~50 Markdown files** accumulated across many feature cycles. When tasked with cleaning or reorganising docs:

### Categories of files

| Category | Keep? | Examples |
|----------|-------|---------|
| Primary docs | **Keep** | `README.md`, `README_en.md`, `ARCHITECTURE_v2.0.md`, `PROJECT_SUMMARY.md` |
| User-facing guides | **Keep** | `COMPLETE_USER_GUIDE*.md`, `QUICKSTART*.md`, `DEPLOYMENT_MODES.md` |
| Feature guides | **Keep if current** | `AI_USAGE_GUIDE.md`, `WYSIWYG_GUIDE.md`, `IMAGE_FEATURE_GUIDE.md`, `PDF_EXPORT_IMPROVEMENTS.md` |
| Build/release notes | **Archive or remove** | `BUILD_FIX_GUIDE.md`, `BUILD_SOLUTION_SUMMARY.md`, `BUILD_WINDOWS_EXE.md`, `CHANGELOG_v1.1.0.md`, `RELEASE_NOTES*.md`, `PHASE2_COMPLETION_REPORT.md` |
| One-off fix reports | **Remove** | `fix_status_report.md`, `IMAGE_FIX_SUMMARY.md`, `LATEX_RENDERING_FIX.md`, `drag_drop_fix.md`, `SOLUTION_SUMMARY_en.md` |
| Planning / proposals | **Remove** | `FEATURE_PLAN.md`, `CHAT_ENHANCEMENT_PLAN.md`, `OPTIMIZATION_PROPOSAL.md`, `PORTABLE_RUNTIME_PLAN.md`, `FEATURE_UPDATE_REPORT.md` |
| Test/scratch files | **Remove** | `drag_test.md`, `test_*.md`, `three_column_test.md`, `task.md`, `image_rendering_test.md` |
| Duplicate guides | **Consolidate** | `FILE_ASSOCIATION_GUIDE.md` + `MD_FILE_ASSOCIATION_GUIDE.md`; `WYSIWYG_GUIDE.md` + `WYSIWYG_SUMMARY.md` + `WYSIWYG_IMPLEMENTATION_CN.md` |

### Cleanup workflow

1. **Audit** — list all `.md` files in root: `Get-ChildItem *.md | Select-Object Name`.
2. **Classify** — map each file to a category above.
3. **Consolidate duplicates** before deleting — merge content if any unique information exists.
4. **Always confirm with the user before deleting any file** — some files may still be referenced externally or linked in the GitHub Pages site.
5. **Update `README.md`** links after removal so no broken references remain.

The `docs/` folder contains the built GitHub Pages site; do **not** manually edit files there — run `python build_web.py` to regenerate it.

---

## AI / Chat Features

- AI provider abstraction lives in `ai_framework.py`; user configuration in `ai_settings.py`.
- Supported backends: personal AI (local), Gemini API, smart routing.
- See [AI_USAGE_GUIDE.md](AI_USAGE_GUIDE.md) for end-user instructions.

---

## Deployment

Four modes are documented in [DEPLOYMENT_MODES.md](DEPLOYMENT_MODES.md):
1. **Full local (default)** — frontend + backend on user's machine, no internet required
2. **Personal server / File DataHub** — backend on a machine you control, connect from other devices
3. **Windows desktop app** — standalone Qt app (`run_editor.bat` or built EXE)
4. **Docker** — containerised personal server

Docker configuration: `docker-compose.yml` / `Dockerfile`.
