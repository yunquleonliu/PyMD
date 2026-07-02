# PyMD Web Editor — Feature Plan v1.0

> **Principle**: Minimal, focused, ship-ready.  
> No bloat. No comparison with other tools. Every feature must earn its place.

---

## Current state (已完成 ✅)

| Area | Done |
|------|------|
| Server (Phase 1–4) | FastAPI, Docker, PWA, Pyodide WASM |
| File ops | List `.md`, Read, Write, Delete |
| Markdown | Render → HTML (Python server or Pyodide) |
| Export | `.docx` download via API |
| PDF logic (desktop) | Merge, Split, to DOCX, to Markdown — in `pdf_tools.py` |
| Web UI shell | Sidebar + editor pane + preview pane |

---

## Module P — PDF Tools  ⬅ Priority 1

> All heavy logic (`PyMuPDF`, `pdf2docx`) already exists in `pdf_tools.py`.  
> Work = writing API wrappers + a minimal PDF panel in the web UI.

### P1 · Extract pages
| | |
|---|---|
| Endpoint | `POST /api/pdf/extract` |
| Body | `{ "path": "report.pdf", "pages": "1-3,5,7" }` |
| Returns | Streamed PDF download |
| Backend | `fitz.open()` + `insert_pdf()` — already know how |

### P2 · Merge PDFs
| | |
|---|---|
| Endpoint | `POST /api/pdf/merge` |
| Body | `{ "paths": ["a.pdf","b.pdf"], "filename": "merged.pdf" }` |
| Returns | Streamed PDF download |
| Backend | `PDFConverter.merge_pdfs()` already works |

### P3 · Insert pages
| | |
|---|---|
| Endpoint | `POST /api/pdf/insert` |
| Body | `{ "base": "doc.pdf", "insert": "extra.pdf", "after_page": 3 }` |
| Returns | Streamed PDF download |
| Backend | `fitz` — `insert_pdf(doc, from_page, to_page, start_at)` |

### P4 · Convert to Word
| | |
|---|---|
| Endpoint | `POST /api/pdf/to-word` |
| Body | `{ "path": "report.pdf", "filename": "report.docx" }` |
| Returns | `.docx` download |
| Backend | `PDFConverter.to_docx()` already works |

### P5 · Convert to Excel (table extraction)
| | |
|---|---|
| Endpoint | `POST /api/pdf/to-excel` |
| Body | `{ "path": "report.pdf", "filename": "report.xlsx" }` |
| Returns | `.xlsx` download |
| Backend | `fitz` page text → heuristic row/col detection → `openpyxl` |
| New dep | `openpyxl>=3.1` |
| Note | Best-effort for simple tables; complex layouts are approximations |

### P6 · PDF info + page thumbnails (for the UI picker)
| | |
|---|---|
| `GET /api/pdf/info?path=` | `{ pages, title, author, size_bytes }` |
| `GET /api/pdf/thumb?path=&page=1` | PNG image of one page (for visual picker) |
| Backend | `fitz.open()` → `doc.load_page(n).get_pixmap()` |

### P7 · List PDF files
Extend existing `GET /api/files` with `?types=md,pdf` query param.  
Default stays `md` (no breaking change).

### PDF Web UI
```
[ PDF Tools panel — toggled from toolbar ]
┌────────────────────────────────────┐
│ 📄 Open PDF   [browse sidebar]     │
│                                    │
│  Pages: [1-3, 5]   [Extract ↓]    │
│                                    │
│  [Merge ↓]  drag PDFs here        │
│  [Insert]   after page: [__]      │
│                                    │
│  [→ Word]   [→ Excel]             │
└────────────────────────────────────┘
```
Single panel, all ops in one place. No separate tabs.

---

## Module M — Markdown WYSIWYG  ⬅ Priority 2

> **Chosen approach**: Markdown-assisted toolbar (not full contenteditable).  
> Buttons insert/wrap markdown syntax around the cursor selection.  
> Simpler, no extra library, stays 100% compatible with the existing render pipeline.

### M1 · Formatting toolbar
Buttons that wrap the current selection in the `<textarea>`:

| Button | Inserts |
|--------|---------|
| **B** | `**selected**` |
| _I_ | `_selected_` |
| H1 / H2 / H3 | `# ` / `## ` / `### ` at line start |
| `code` | `` `selected` `` |
| ``` ``` ``` | fenced block |
| Link | `[selected](url)` |
| Image | `![alt](url)` |
| — List | `- ` at line start |
| 1. List | `1. ` at line start |
| Table | minimal 3×2 table template |
| Horizontal rule | `\n---\n` |

Implementation: ~80 lines of JS, no library. `textarea.setSelectionRange` + `document.execCommand` pattern.

### M2 · Source / Preview toggle
Current split view stays. Add `[Source | Split | Preview]` toggle in toolbar.  
- **Source**: full-width textarea only  
- **Split**: current 50/50 (default)  
- **Preview**: full-width preview only

### M3 · Already done
- Live preview with 280 ms debounce ✅  
- Word count ✅  
- Ctrl+S / Ctrl+N ✅  
- Dark mode ✅

---

## Module F — File Management  ⬅ Priority 3

> Standard operations every file tool must have. None of these are optional.

### F1 · Rename file
| | |
|---|---|
| Endpoint | `POST /api/file/rename` |
| Body | `{ "path": "old.md", "new_name": "new.md" }` |
| UI | Right-click context menu on sidebar item → "Rename" |

### F2 · Create folder
| | |
|---|---|
| Endpoint | `POST /api/folder` |
| Body | `{ "path": "notes/projects" }` |
| UI | `+folder` button in sidebar header |

### F3 · Move / Copy file
| | |
|---|---|
| Endpoint | `POST /api/file/move` |
| Body | `{ "path": "a/b.md", "dest": "c/b.md", "copy": false }` |
| UI | Drag in sidebar (Phase 2 of this feature) or right-click → Move |

### F4 · Recent files (no API needed)
- Client-side only, stored in `localStorage`
- Max 10 entries, shown at top of sidebar when no folder is open
- Cleared when user opens a new folder

### F5 · File info panel
- Size, last modified — already returned by `GET /api/files`
- Show in a tooltip on hover in the sidebar

### F6 · Drag-and-drop open
- Drop a `.md` or `.pdf` file onto the editor pane → open it
- Web File API (`e.dataTransfer.files[0]`), no server call for reading
- Server call only needed for saving

### F7 · Delete — already done ✅
`DELETE /api/file` already implemented. Add confirmation dialog in UI.

### F8 · Keyboard shortcuts (file ops)
| Keys | Action |
|------|--------|
| `Ctrl+S` | Save (done ✅) |
| `Ctrl+Shift+S` | Save As |
| `Ctrl+N` | New file (done ✅) |
| `Ctrl+O` | Open file picker |
| `Delete` (in sidebar focus) | Delete selected file |
| `F2` (in sidebar focus) | Rename selected file |

---

## Module A — AI Assistant  ⬅ Priority 4 (optional / deferred)

> User's note: "如果实在没有必须的不能缺少的功能，可以暂时没有"  
> Verdict: **defer until P, M, F are solid.**

If ever added, keep it to two functions only:

| Function | Endpoint | What it does |
|----------|----------|--------------|
| Improve paragraph | `POST /api/ai/improve` | Rewrite selected text, return suggestion |
| Summarize document | `POST /api/ai/summarize` | Return 3-sentence summary |

Both require user-supplied API key (`Settings → AI Key`). No key = feature hidden.

---

## Implementation order

```
P6 (PDF info + thumb)       ← needed by PDF UI
P1 Extract                  ← most common PDF op
P2 Merge                    ← most common PDF op
P4 To Word                  ← already has most code
P3 Insert                   ← depends on P1 logic
P5 To Excel                 ← new dep, do last

M1 Formatting toolbar       ← pure JS, fast to build
M2 Split/Source/Preview     ← pure JS, fast to build

F1 Rename                   ← one endpoint + small UI
F2 Create folder            ← one endpoint + small UI
F4 Recent files             ← localStorage, no API
F6 Drag-and-drop            ← browser API, no server
F3 Move/Copy                ← one endpoint + drag UI
F8 Keyboard shortcuts       ← scattered small additions
```

---

## New dependencies

| Package | Used by | Install |
|---------|---------|---------|
| `openpyxl>=3.1` | P5 (Excel export) | add to `requirements.txt` |
| Everything else | already in `requirements.txt` | — |

---

## API surface summary (new endpoints)

```
GET  /api/pdf/info          ?path=
GET  /api/pdf/thumb         ?path=&page=1
POST /api/pdf/extract       { path, pages }
POST /api/pdf/merge         { paths, filename }
POST /api/pdf/insert        { base, insert, after_page }
POST /api/pdf/to-word       { path, filename }
POST /api/pdf/to-excel      { path, filename }
POST /api/file/rename       { path, new_name }
POST /api/folder            { path }
POST /api/file/move         { path, dest, copy? }
GET  /api/files             ?dir=&types=md,pdf   (extend existing)
```

Total new endpoints: **10**.  All follow the same security pattern (path validated against `BASE_DIR`).
