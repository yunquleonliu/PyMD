# PyMD Deployment Modes

PyMD is organized around one shared frontend and three formal deployment modes.

## Mode 1 — Full local

The user runs frontend and backend on the same machine.

Recommended for:

- private work
- offline work
- single-user editing
- highest trust in local files

Run with:

```bash
pip install -r requirements.txt
pip install -e .
python -m pymd_editor.server.serve --dir data --host 127.0.0.1 --port 8765 --no-browser
```

## Mode 2 — Official cloud

The frontend connects to the official backend.

Official service entry:

- `https://dataflowxx.dpdns.org`

Recommended for:

- multi-device access
- official hosted conversion quality
- users who want backend-powered features without managing their own server

## Mode 3 — Customer self-hosted

The frontend connects to a customer-managed backend with the same API contract.

Recommended for:

- private infrastructure
- enterprise usage
- regulated or isolated environments

## Supporting Delivery Modes

### GitHub Pages demo

Role:

- demo
- lite mode
- docs
- release landing page

Non-role:

- production backend
- authoritative conversion quality

### Windows desktop app

Still supported as a local-native shell:

```text
run_editor.bat
```

## Frontend Backend Selector

The shared web UI supports:

| Option | Purpose |
|--------|---------|
| Auto | Try same-origin API, then localhost, then lite mode |
| Demo / Lite | Browser-only fallback |
| Localhost | Force local backend |
| Official Cloud | Force official backend |
| Custom server | Force a private backend URL |

## Workspace Sync Direction

For cloud and self-hosted modes:

- the frontend binds the local folder
- the frontend computes a workspace manifest
- the backend stores the remote workspace manifest
- sync decides upload, download, and conflicts

This prevents pretending that a remote backend can directly open the user's local filesystem.

## Backend API Contract

Every backend should expose:

- `GET /api/health`
- `POST /api/render`
- `GET /api/files`
- `GET /api/file`
- `POST /api/file`
- `DELETE /api/file`
- `POST /api/file/rename`
- `POST /api/folder`
- `POST /api/export/word`
- `GET /api/pdf/info`
- `GET /api/pdf/stream`
- `POST /api/pdf/extract`
- `POST /api/pdf/merge`
- `POST /api/pdf/insert`
- `POST /api/pdf/to-word`
- `POST /api/pdf/to-excel`
- `POST /api/pdf/to-ppt`
- `GET /api/workspaces/sync/manifest`
- `POST /api/workspaces/sync/manifest`
- `POST /api/workspaces/sync/diff`

## Health Payload

```json
{
  "status": "ok",
  "deployment_mode": "local",
  "features": {
    "pdf_to_word": true,
    "pdf_to_excel": true,
    "pdf_to_ppt": true,
    "workspace_sync_manifest": true,
    "workspace_sync_diff": true
  }
}
```
