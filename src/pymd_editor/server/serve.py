"""
PyMD Editor — Web Server Entry Point

Usage:
    python -m pymd_editor serve [--port 8765] [--dir PATH] [--no-browser]
    python -m pymd_editor.server.serve [--port 8765] [--dir PATH]
"""
from __future__ import annotations

import argparse
import threading
import time
import webbrowser
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pymd serve",
        description="Start PyMD Editor web server (local mode)",
    )
    parser.add_argument(
        "--port", type=int, default=8765,
        help="Port to listen on (default: 8765)",
    )
    parser.add_argument(
        "--dir", type=str, default=str(Path.home()),
        help="Base directory for file operations (default: home)",
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1",
        help=(
            "Host/IP to bind to (default: 127.0.0.1 — localhost only). "
            "Use 0.0.0.0 for Docker / server deployments."
        ),
    )
    parser.add_argument(
        "--no-browser", action="store_true",
        help="Do not open a browser window automatically",
    )
    args = parser.parse_args(argv)

    base_dir = Path(args.dir).expanduser().resolve()
    if not base_dir.is_dir():
        print(f"Error: '{base_dir}' is not a directory.")
        return 1

    _start_server(
        port=args.port,
        host=args.host,
        base_dir=base_dir,
        open_browser=not args.no_browser,
    )
    return 0


def _start_server(port: int, base_dir: Path, host: str = "127.0.0.1", open_browser: bool = True) -> None:
    import uvicorn
    from fastapi.staticfiles import StaticFiles

    # Import the shared app + configure base directory
    from pymd_editor.server import api as api_module
    api_module.BASE_DIR = base_dir

    # Mount the static web frontend AFTER API routes so /api/* takes priority
    static_dir = Path(__file__).parent / "static"
    if static_dir.is_dir():
        api_module.app.mount(
            "/", StaticFiles(directory=str(static_dir), html=True), name="static"
        )

    url = f"http://127.0.0.1:{port}" if host in ("0.0.0.0", "::") else f"http://{host}:{port}"
    print(f"\n  PyMD Editor  →  {url}")
    print(f"  File root    →  {base_dir}")
    print(f"  API docs     →  {url}/api/docs")
    print("  Press Ctrl+C to stop.\n")

    if open_browser:
        def _open_browser():
            time.sleep(0.9)
            webbrowser.open(url)
        threading.Thread(target=_open_browser, daemon=True).start()

    uvicorn.run(api_module.app, host=host, port=port, log_level="warning")


if __name__ == "__main__":
    raise SystemExit(main())
