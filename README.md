# PyMD Editor: The Artist's Document Assistant

PyMD Editor is not just another Markdown editor. It is a **Creative Workspace** designed for writers, thinkers, and artists who want to craft beautiful documents without distraction.

![PyMD Editor Screenshot](https://via.placeholder.com/800x450?text=PyMD+Editor+Screenshot)

## ✨ Key Features

### 🎨 Artist-First Design
*   **Zen Mode (F11)**: Immerse yourself in your writing. One keystroke hides all distractions.
*   **Curated Themes**: Switch between "Midnight Coffee", "Forest Walk", and "Paper & Ink" to match your mood.
*   **Beautiful Typography**: Optimized for readability and aesthetics.

### 🤖 Creative AI Companion
*   **Intelligent Assistance**: Not just a spell-checker. Ask the AI to "Visualize this paragraph" or "Rewrite in a poetic style".
*   **Context Aware**: The AI understands your entire document context.

### � Powerful Core
*   **WYSIWYG Editing**: What You See Is What You Get. Edit tables and images directly.
*   **Three-Column Layout**: Editor, Preview, and AI Assistant side-by-side.
*   **Export Anywhere**: One-click export to PDF and Word (.docx).

## 📥 Installation

### Windows
1.  Download the latest installer (`PyMD_Setup_v0.4.0.exe`) from the [Releases](https://github.com/yunquleonliu/PyMD/releases) page.
2.  Double-click to install.
3.  Start writing! (PyMD automatically handles `.md` files).

### Mac (Coming Soon)
We are working on a native `.dmg` installer. For now, you can run from source.

## 🛠️ For Developers

### Running from Source
```bash
# Clone the repo
git clone https://github.com/yunquleonliu/PyMD.git
cd PyMD

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python src/pymd_editor/main.py
```

### Building the Installer (Windows)
1.  Install [Inno Setup](https://jrsoftware.org/isdl.php).
2.  Run `build_windows_exe.bat` to generate the executable.
3.  Open `setup.iss` with Inno Setup and compile.

## 📄 License
MIT License. Free for everyone.
