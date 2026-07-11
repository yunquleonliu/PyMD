# PyMD

PyMD is a **local-first** document workspace for Markdown editing and multi-format conversion. Run everything on your own machine, or deploy it as a personal server to use as a shared File/DataHub across devices or with a small team.

## Phase 1 Features

- **Markdown editing** — live split-pane preview, WYSIWYG mode, dark/light theme
- **PDF conversion** — PDF → Markdown / Word / Excel / PowerPoint (backend-powered)
- **Markdown export** — Markdown → Word / PDF
- **File browser** — browse and manage `.md` and `.pdf` folders
- **PDF tools** — preview, merge, split, extract pages
- **AI assistant** — optional chat panel for writing assistance

## Quick Start

### Local mode (default)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
python -m pymd_editor.server.serve --dir data --host 127.0.0.1 --port 8765 --no-browser
```

Open `http://127.0.0.1:8765`.

### Personal server / File DataHub

Run the backend on any machine you control. Connect from other devices or share a document folder with a small team.

```bash
# On your server
python -m pymd_editor.server.serve --dir /path/to/docs --host 0.0.0.0 --port 8765
```

### Windows desktop app

```
run_editor.bat
```

Build a standalone EXE:

```bash
pyinstaller build_exe.spec --noconfirm
```

### Docker

```bash
docker compose up --build
```

## Keyboard Shortcuts (desktop app)

| Action | Shortcut |
|--------|----------|
| New | Ctrl+N |
| Open | Ctrl+O |
| Save | Ctrl+S |
| Save As | Ctrl+Shift+S |
| Export Word | Ctrl+Shift+W |
| Export PDF | Ctrl+Shift+P |
| Toggle Theme | Ctrl+T |

## Key Docs

- [DEPLOYMENT_MODES.md](DEPLOYMENT_MODES.md)
- [ARCHITECTURE_v2.0.md](ARCHITECTURE_v2.0.md)
- [AI_USAGE_GUIDE.md](AI_USAGE_GUIDE.md)

## License

MIT
