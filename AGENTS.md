# PyMD Agent Guide

This file defines how human developers and coding agents should work in this repo.

## Product Context

PyMD is a local-first document workspace and conversion bridge.

Read first:

- [README.md](README.md)
- [PROJECT_BLUEPRINT.md](PROJECT_BLUEPRINT.md)
- [DEPLOYMENT_MODES.md](DEPLOYMENT_MODES.md)
- [WORKSPACE_SYNC_ARCHITECTURE.md](WORKSPACE_SYNC_ARCHITECTURE.md)
- [LOCAL_VALIDATION.md](LOCAL_VALIDATION.md)

## Golden Rules

1. Do not blur lite mode and high-fidelity mode.
   Browser-only fallback is acceptable for demos, but quality-sensitive conversion must prefer backend execution.
2. Treat local folder binding and sync as separate concerns.
   `Open Folder` is frontend-initiated; sync is a workspace feature.
3. Preserve the three-mode architecture.
   Every major change should be evaluated against:
   - full local
   - official cloud
   - customer self-hosted
4. Keep the backend as the capability center.
   The frontend should coordinate, not silently downgrade quality-sensitive workflows.
5. Update docs when product boundaries change.

## Required Task Framing

When starting substantial work, state:

- goal
- target deployment mode
- quality requirement
- validation plan

Recommended template:

```text
Goal:
Target mode:
Quality requirement:
Constraints:
Validation:
```

## Deployment-Aware Thinking

Before changing behavior, ask:

1. Is this browser-only, backend-only, or hybrid?
2. Does this change affect local folder workflows?
3. Does this change break official cloud or self-hosted parity?
4. Does this need a new capability flag in `/api/health`?

## Sync-Aware Thinking

For anything involving files:

- local file tree may come from the browser
- backend file tree may come from the server
- sync is not yet fully implemented, so avoid assuming remote ownership of local files
- uploading a selected local file to backend conversion is valid and preferred for fidelity

## Validation Expectations

After meaningful code changes:

- run `python -m compileall src`
- run `node --check src\\pymd_editor\\server\\static\\app.js`
- regenerate `docs/` with `python build_web.py --out docs --base-url /PyMD/` if static assets changed
- use [LOCAL_VALIDATION.md](LOCAL_VALIDATION.md) for manual verification when behavior changes

## Current Strategic Direction

- GitHub Pages is the demo and documentation surface
- official product entry is `dataflowxx.dpdns.org`
- the shared frontend should connect to local, official, and self-hosted backends
- workspace sync is the next major foundation after backend mode selection
