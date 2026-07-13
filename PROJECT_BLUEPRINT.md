# PyMD Project Blueprint

## Project Definition

PyMD is a local-first document workspace and conversion bridge.

Its core purpose is to let users work on Markdown and document assets from a familiar folder-based workflow while reusing one shared web UI across different deployment modes.

The project is not only:

- a Markdown editor
- a PDF toolbox
- a format converter

It is intended to become:

- a local-first workspace
- a document sync surface
- a backend-powered conversion platform

## Product Principles

1. Local-first
   User files belong on the user's machine by default.
2. One UI, multiple runtimes
   The web UI should remain consistent across deployment modes.
3. Quality belongs to the backend
   High-fidelity conversions must prefer backend execution over browser-only fallbacks.
4. Folder workflow first
   Users should be able to bind a local folder and work from it naturally.
5. Sync is a product feature
   Cross-device and server-connected behavior should be modeled as workspace sync, not as remote filesystem browsing.

## Official Deployment Modes

### Mode 1 — Full local

- frontend on the user's machine
- backend on the user's machine
- files stored locally
- no cloud required

### Mode 2 — Official cloud

- frontend may run locally or via a web entry
- backend runs on the official server
- files may stay local first, with sync and conversion delegated to the server
- official endpoint: `https://dataflowxx.dpdns.org`

### Mode 3 — Customer subdomain self-hosted

- same frontend behavior
- same backend API
- backend owned by the customer inside their vLAN
- Dataflowxx assigns the HTTPS subdomain
- internal DNS or a managed tunnel routes the subdomain to the customer backend
- customer controls data boundary and deployment

## Secondary Delivery Modes

### GitHub Pages demo

Role:

- demo
- docs
- release landing page
- lite mode

Non-role:

- authoritative conversion quality
- official backend
- long-running document processing

### Desktop app

The Qt desktop app remains valid for:

- single-machine workflows
- Windows packaging
- users who prefer a native shell

## Architecture Layers

1. Experience layer
   Editor, file tree, preview, PDF tools, backend selector.
2. Runtime layer
   Browser-only, localhost backend, official cloud backend, customer subdomain backend.
3. Workspace layer
   Local folder binding, workspace indexing, sync planning.
4. Capability layer
   Render, export, PDF conversion, metadata extraction.
5. Host layer
   Local Python, Docker, official cloud, customer subdomain infrastructure, GitHub Pages demo.

## What Must Be Stable Going Forward

- README and top-level docs must reflect the same three-mode architecture
- `/api/health` remains the capability probe
- backend-powered conversion is the default for quality-sensitive actions
- local folder binding is always initiated from the frontend
- sync is treated as an explicit workspace feature, not as an accidental side effect

## Near-Term Roadmap

1. Stabilize docs and project structure
2. Formalize workspace sync
3. Strengthen conversion quality validation
4. Unify cloud and self-hosted backend packaging
5. Improve UX around backend choice and sync status
