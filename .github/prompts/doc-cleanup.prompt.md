---
description: "Audit and clean up root-level Markdown docs: classify, flag duplicates, propose deletions, and update README links. Use when the docs folder feels cluttered."
argument-hint: "optional: specific files or categories to focus on"
agent: "agent"
tools: [file_search, grep_search, read_file, list_dir]
---

Audit the root-level Markdown documentation in this PyMD workspace and produce a cleanup plan.

## Steps

1. **List** all `.md` files in the workspace root with `list_dir`.

2. **Classify** each file using the categories defined in [AGENTS.md](../../AGENTS.md#documentation-cleanup):
   - Keep (primary docs, user-facing guides, current feature guides)
   - Archive or remove (build/release notes, one-off fix reports, planning/proposals)
   - Remove (test/scratch files)
   - Consolidate (duplicate or overlapping guides — check `_en` pairs too)

3. **Check for broken links** in `README.md` and `README_en.md` that reference files you plan to remove.

4. **Output a Markdown table** with columns:
   | File | Category | Action | Reason |

5. **List consolidation candidates** separately — show which files overlap and what unique content each holds.

6. **Do NOT delete any files yet.** Present the plan and wait for user confirmation before making any changes.

{{args}}
