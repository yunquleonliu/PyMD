# PyMD Deployment Modes

PyMD is now organized around one shared frontend and three backend-capable deployment modes.

## The Three Modes

1. Full local
   The user runs both frontend and backend locally with `pymd serve` or Docker.
2. Official cloud
   The frontend connects to the official backend at `https://dataflowxx.dpdns.org`.
3. Customer self-hosted
   The frontend connects to a customer-managed backend with the same API and feature contract.

## Role Of GitHub Pages

GitHub Pages is not the official service backend.

Its role is:

- demo entry
- lightweight browser-only mode
- documentation and release landing page
- optional jump-off point to the official cloud

Its role is not:

- high-fidelity backend conversion
- long-running document processing
- the source of truth for production quality

## Role Of dataflowxx

`https://dataflowxx.dpdns.org` is the official branded service entry.

It should provide:

- the official homepage / brand entry
- the real web app entry under `/app/`
- the Python backend under `/api/*`
- high-fidelity PDF to Word / Excel conversion
- the same API contract used by private deployments

## Frontend Connection Model

The shared frontend supports these runtime choices:

- `Auto`
  Try same-origin API first, then localhost, then browser-only mode.
- `Demo / Lite`
  Force browser-only behavior.
- `Localhost`
  Connect to `http://127.0.0.1:8765`.
- `Official Cloud`
  Connect to `https://dataflowxx.dpdns.org`.
- `Custom server`
  Connect to a user-provided backend URL.

This keeps user interaction consistent even when deployment changes.

## Backend Contract

Every production backend should expose:

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

## Health Payload

`/api/health` should describe deployment mode and features:

```json
{
  "status": "ok",
  "deployment_mode": "cloud",
  "public_base_url": "https://dataflowxx.dpdns.org",
  "features": {
    "folder_browse": true,
    "pdf_to_word": true,
    "pdf_to_excel": true
  }
}
```

## Deployment Summary

- GitHub Pages
  Demo and docs only.
- `dataflowxx.dpdns.org`
  Official homepage, official app entry, official backend.
- Customer server
  Same backend image and same API, different domain and ownership.
