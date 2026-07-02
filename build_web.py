#!/usr/bin/env python3
"""
PyMD Editor — Static Web Build (Phase 3 / Phase 4 deployment)

Copies src/pymd_editor/server/static/ → dist/web/ and optionally patches
the base URL in manifest.json for GitHub Pages subdirectory deployments.

Usage
-----
  python build_web.py                            # → dist/web/
  python build_web.py --base-url /pymd-editor/  # GitHub Pages project page
  python build_web.py --out ./docs               # custom output dir
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

SRC = Path(__file__).parent / "src" / "pymd_editor" / "server" / "static"
DEFAULT_OUT = Path(__file__).parent / "dist" / "web"

STATIC_FILES = [
    "index.html",
    "style.css",
    "app.js",
    "manifest.json",
    "sw.js",
    "icon.svg",
    "pyodide_worker.js",
]


def main() -> int:
    p = argparse.ArgumentParser(description="Build static web app for deployment")
    p.add_argument("--out",      default=str(DEFAULT_OUT),
                   help="Output directory (default: dist/web)")
    p.add_argument("--base-url", default="/",
                   help="Base URL for GitHub Pages subdirectory, e.g. /pymd-editor/")
    p.add_argument("--clean",    action="store_true",
                   help="Remove the output directory before building")
    args = p.parse_args()

    out = Path(args.out)
    base_url: str = args.base_url
    if not base_url.endswith("/"):
        base_url += "/"

    if args.clean and out.exists():
        shutil.rmtree(out)
        print(f"  Cleaned {out}")

    out.mkdir(parents=True, exist_ok=True)

    # ── Copy static files ────────────────────────────────────────────────
    for fname in STATIC_FILES:
        src_file = SRC / fname
        if not src_file.exists():
            print(f"  WARN  {fname} not found, skipping")
            continue
        dst_file = out / fname
        shutil.copy2(src_file, dst_file)
        print(f"  copy  {fname}")

    # ── Patch manifest.json for non-root deployments ─────────────────────
    manifest_path = out / "manifest.json"
    if base_url != "/" and manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["start_url"] = base_url
        manifest["scope"]     = base_url
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"  patch manifest.json  start_url={base_url}")

    # ── Summary ──────────────────────────────────────────────────────────
    total = sum(1 for f in STATIC_FILES if (out / f).exists())
    print(f"\n  Built {total}/{len(STATIC_FILES)} files → {out.resolve()}")
    print("  Deploy this folder to any static host:")
    print("    GitHub Pages, Cloudflare Pages, Vercel, Netlify, S3, etc.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
