# PyMD Quick Start

## Option 1: Web server mode (recommended)

Start the local server and open in a browser:

```bash
pip install -r requirements.txt
pip install -e .
python -m pymd_editor.server.serve --dir data --host 127.0.0.1 --port 8765 --no-browser
```

Open `http://127.0.0.1:8765`.

### Personal server / File DataHub

Run on your own server for multi-device access:

```bash
python -m pymd_editor.server.serve --dir /path/to/docs --host 0.0.0.0 --port 8765
```

---

## Option 2: Windows desktop app

Double-click to launch (no browser needed):

```
run_editor.bat
```

Drag any `.md` file onto the desktop shortcut to open it directly.

---

## Option 3: Docker

```bash
docker compose up --build
```

---

## Keyboard shortcuts (desktop app)

| Action | Shortcut |
|--------|----------|
| New | Ctrl+N |
| Open | Ctrl+O |
| Save | Ctrl+S |
| Save As | Ctrl+Shift+S |
| Export Word | Ctrl+Shift+W |
| Export PDF | Ctrl+Shift+P |
| Toggle Theme | Ctrl+T |

---

See [DEPLOYMENT_MODES.md](DEPLOYMENT_MODES.md) for full deployment details.
