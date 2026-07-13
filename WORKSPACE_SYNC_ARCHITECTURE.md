# Workspace Sync Architecture

## Why Sync Matters

When the backend lives on another machine, it cannot open the user's local folder directly.

So `Open Folder` and `Sync` must be modeled separately:

- `Open Folder`
  Bind a local workspace from the frontend.
- `Sync`
  Compare the local workspace with a backend workspace and exchange changes.

This keeps the product local-first while still enabling cloud and private-server workflows.

## Core Model

### 1. Workspace binding

The frontend binds a local folder by using browser file system access.

The output is:

- a local folder handle
- a workspace id
- a current file tree

### 2. Workspace index

The frontend scans relevant files and emits metadata:

- `path`
- `size`
- `modified`
- `sha256`
- `deleted`

Relevant file types for phase 1:

- `.md`
- `.pdf`
- `.docx`
- `.xlsx`
- `.pptx`

### 3. Sync manifest

The backend stores the latest known manifest per workspace.

This is the minimum stable object:

```json
{
  "workspace_id": "my-notes",
  "client_id": "laptop-1",
  "updated_at": "2026-07-12T12:00:00Z",
  "files": [
    {
      "path": "notes/a.md",
      "size": 2048,
      "modified": 1752331200.0,
      "sha256": "..."
    }
  ]
}
```

### 4. Sync diff

The backend compares the current client manifest with the stored remote manifest.

The minimum diff result is:

- `upload`
- `download`
- `conflicts`

### 5. File exchange

After diffing:

- files in `upload` are pushed from local workspace to backend storage
- files in `download` are pulled from backend storage to the client
- files in `conflicts` require explicit UX

## Phase 1 API

Currently planned or scaffolded:

- `GET /api/workspaces/sync/manifest`
- `POST /api/workspaces/sync/manifest`
- `POST /api/workspaces/sync/diff`

Next recommended endpoints:

- `POST /api/workspaces/sync/upload`
- `GET /api/workspaces/sync/download`
- `POST /api/workspaces/sync/resolve`
- `GET /api/workspaces/sync/status`

## UX Rules

1. `Open Folder` is always frontend initiated.
2. High-quality conversion should work even for local files by uploading the chosen file to the backend.
3. File tree should be local-first when a local workspace is bound.
4. Sync state must be visible in the UI.
5. Cloud mode should never pretend to own the local filesystem.

## Recommended Conflict Policy

Phase 1:

- last-write-wins for simple non-conflict cases
- explicit conflict list when timestamps are equal but content differs

Phase 2:

- keep both copies
- add conflict markers for Markdown
- add version history

## What This Enables

- local folder + localhost backend
- local folder + official cloud backend
- local folder + customer private backend

That is the foundation needed for a true local-first, three-mode product.
