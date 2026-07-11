# PyMD Deployment Modes

PyMD is local-first. The default and recommended mode is a single user running everything on their own machine. A personal server mode enables multi-device access or small-team sharing via a File/DataHub.

## Mode 1 — Full local (default)

Frontend and backend both run on the user's machine. No internet required.

```bash
pip install -r requirements.txt
pip install -e .
python -m pymd_editor.server.serve --dir data --host 127.0.0.1 --port 8765 --no-browser
```

Open `http://127.0.0.1:8765`.

- All files stay on your machine
- No external dependencies
- Single user

## Mode 2 — Personal server / File DataHub

Run the backend on any machine you control. Connect from other devices or share a document folder with a small team.

```bash
# On the host machine
python -m pymd_editor.server.serve --dir /path/to/docs --host 0.0.0.0 --port 8765
```

Connect from any device by pointing the frontend to `http://<host-ip>:8765`.

Use cases:
- Access your docs from multiple computers
- Share a document folder with your team
- Run on a NAS or home server

## Mode 3 — Windows desktop app

Standalone Qt application. No browser needed.

```
run_editor.bat
```

Build a distributable EXE:

```bash
pyinstaller build_exe.spec --noconfirm
```

## Mode 4 — Docker

Containerised personal server, easiest to deploy on a remote machine.

```bash
docker compose up --build
```

## Frontend Backend Selector

The web UI toolbar backend selector supports:

| Option | Connects to |
|--------|-------------|
| Auto | Same-origin → localhost → browser-only |
| Demo / Lite | Browser-only (no backend) |
| Localhost | `http://127.0.0.1:8765` |
| Custom server | Your personal server URL |

## Backend API Contract

Every backend exposes:

- `GET /api/health`
- `POST /api/render`
- `GET /api/files`, `GET /api/file`, `POST /api/file`, `DELETE /api/file`, `POST /api/file/rename`
- `POST /api/folder`
- `POST /api/export/word`
- `GET /api/pdf/info`, `GET /api/pdf/stream`
- `POST /api/pdf/extract`, `POST /api/pdf/merge`, `POST /api/pdf/insert`
- `POST /api/pdf/to-word`, `POST /api/pdf/to-excel`, `POST /api/pdf/to-ppt`

## Health Payload

```json
{
  "status": "ok",
  "deployment_mode": "local",
  "features": {
    "folder_browse": true,
    "pdf_to_word": true,
    "pdf_to_excel": true,
    "pdf_to_ppt": true
  }
}
```
