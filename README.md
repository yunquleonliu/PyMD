# PyMD

PyMD is a document workspace and conversion bridge built around one shared web UI and three deployment modes:

1. Full local
   Frontend and backend both run on the user's machine.
2. Official cloud
   Frontend connects to the official backend at `https://dataflowxx.dpdns.org`.
3. Customer self-hosted
   Frontend connects to a customer-managed backend that exposes the same API.

GitHub Pages is kept as the demo and lightweight entry. The real product entry is `dataflowxx.dpdns.org`, where high-fidelity conversion is expected to run through the Python backend.

## What PyMD Covers

- Markdown editing with preview and WYSIWYG support
- Folder browsing for subdirectories, `.md`, and `.pdf`
- PDF preview, extract, merge, insert
- Markdown export to Word
- PDF to Word and PDF to Excel through the backend
- One frontend that can switch between local, official cloud, and private backend

## Product Split

- `GitHub Pages`
  Demo, docs, release entry, browser-only fallback.
- `dataflowxx.dpdns.org`
  Official branded entry and production backend.
- Customer server
  Private deployment using the same backend contract.

## Quick Start

### Full local mode

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m pymd_editor.server.serve --dir data --host 127.0.0.1 --port 8765 --no-browser
```

Open `http://127.0.0.1:8765`.

### Local Docker mode

```bash
docker compose up --build
```

### Demo build for GitHub Pages

```bash
python build_web.py --out docs --base-url /PyMD/
```

## Backend Selection In The UI

The toolbar backend selector supports:

- `Auto`
- `Demo / Lite`
- `Localhost`
- `Official Cloud`
- `Custom server`

This lets the same UI connect to:

- a local backend on `127.0.0.1`
- your official backend on `dataflowxx.dpdns.org`
- a customer backend on their own domain

## Key Docs

- [DEPLOYMENT_MODES.md](DEPLOYMENT_MODES.md)
- [deploy/dataflowxx/README.md](deploy/dataflowxx/README.md)

## Current Direction

- GitHub Pages remains the public demo
- `dataflowxx.dpdns.org` becomes the official homepage and service entry
- the Python backend owns high-fidelity conversion quality
- customer private deployments reuse the same backend image and API

## License

MIT
