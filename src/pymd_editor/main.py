import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    # ── "serve" subcommand: start web server (no Qt needed) ──────────────
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        sys.argv.pop(1)  # remove 'serve' so serve.py argparse sees clean args
        try:
            from pymd_editor.server.serve import main as serve_main
        except ImportError as exc:
            print(f"Web server dependencies not installed: {exc}")
            print("Run:  pip install fastapi 'uvicorn[standard]'")
            sys.exit(1)
        sys.exit(serve_main())

    # ── Default: launch the Qt desktop app ───────────────────────────────
    from PyQt6.QtWidgets import QApplication
    try:
        from pymd_editor.app import MainWindow
    except ImportError:
        from .app import MainWindow

    app = QApplication(sys.argv)
    win = MainWindow()

    # If a file path is passed on the command line, open it automatically
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
        if file_path.exists() and file_path.suffix.lower() == ".md":
            win.load_file(file_path)

    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
