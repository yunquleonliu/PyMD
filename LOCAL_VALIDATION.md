# Local Validation Checklist

Use this checklist before considering a local build stable.

## 1. Start local full stack

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
python -m pymd_editor.server.serve --dir data --host 127.0.0.1 --port 8765 --no-browser
```

Open `http://127.0.0.1:8765`.

## 2. Health probe

Open:

- `http://127.0.0.1:8765/api/health`

Verify:

- `status = ok`
- `deployment_mode = local`
- `pdf_to_word = true`
- `pdf_to_excel = true`
- `pdf_to_ppt = true`
- `workspace_sync_manifest = true`
- `workspace_sync_diff = true`

## 3. Backend selector

Verify the frontend can switch to:

- `Auto`
- `Localhost`
- `Demo / Lite`
- `Custom server`

For local full-stack validation, keep it on `Auto` or `Localhost`.

## 4. File tree

Verify:

- files from `data/` are listed
- subdirectories appear
- `.md` files appear
- `.pdf` files appear
- open folder still works if browser file system access is used

## 5. Markdown workflow

Verify:

- create file
- save file
- save as
- reopen file
- preview render
- WYSIWYG edit
- export Markdown to Word

## 6. PDF workflow

Verify for at least one simple and one realistic PDF:

- preview PDF
- extract pages
- merge PDFs
- insert PDF into another PDF
- PDF → Word
- PDF → Excel
- PDF → PowerPoint

## 7. Local folder + backend path

This is critical.

Open a folder through the frontend and keep backend mode on `Localhost`.

Verify:

- local file tree is still shown
- PDF → Word uses backend quality
- PDF → Excel uses backend
- PDF → PowerPoint uses backend

## 8. Optional API smoke tests

Recommended automated checks:

- `POST /api/pdf/to-word`
- `POST /api/pdf/to-excel`
- `POST /api/pdf/to-ppt`
- `POST /api/pdf/upload/to-word`
- `POST /api/workspaces/sync/manifest`
- `POST /api/workspaces/sync/diff`
