# PyMD Evolution Plan: The Artist's Document Assistant

## 1. Vision: "The Artist's Document Assistant"
We are moving away from a generic "Markdown Editor" to a **Creative Workspace**. The goal is to make writing feel like *crafting*.

### Core Pillars
1.  **Zero-Friction Access**: Installation should be invisible. "It just works."
2.  **Aesthetic First**: The tool itself should be a piece of art.
3.  **Creative AI**: AI not just for "fixing grammar", but for *inspiration* and *visuals*.

---

## 2. Strategy: "Easy Installation" (Windows & Mac)

### Windows: The "One-Click" Experience
*   **Current**: ZIP file -> Unzip -> Find EXE -> Run. (Too many steps for non-tech users).
*   **Target**: Professional Installer (`.exe` or `.msi`).
*   **Implementation**:
    *   Use **Inno Setup** to create a single setup file `PyMD_Setup_v0.4.0.exe`.
    *   **Features**:
        *   Auto-install to `AppData` (no admin rights needed) or `Program Files`.
        *   **Auto-associate .md files**: Double-click any markdown file to open PyMD.
        *   **Desktop Shortcut**: Created automatically.
        *   **Uninstaller**: Clean removal.

### Mac: The "Native" Feel
*   **Target**: `.dmg` file -> Drag to Applications.
*   **Implementation** (Proposed workflow):
    *   Use `pyinstaller` to build a `.app` bundle.
    *   Use `create-dmg` to package it into a drag-and-drop installer.
    *   **Crucial**: Notarization. We need an Apple Developer ID to sign the app, otherwise users get "Unidentified Developer" warnings.

### Updates
*   **Auto-Update**: The app should check for updates on launch and offer to "Update and Restart" without user intervention.

---

## 3. Strategy: "Artist's Features"

### A. "Zen Mode" (Immersive Writing)
*   **Concept**: A distraction-free mode that hides all UI (menus, sidebars).
*   **Visuals**:
    *   Background: Soft, dynamic gradients or user-selected "Mood Images".
    *   Typography: Curated, beautiful fonts (e.g., *Merriweather*, *Inter*, *Fira Code*).
    *   Sound: Optional ambient sounds (rain, cafe, white noise) - *Future Scope*.

### B. "Mood Board" Side Panel
*   **Concept**: Replace the "File Tree" with a "Creative Space".
*   **Features**:
    *   Drag and drop images for inspiration.
    *   Color palette generator based on the document content.
    *   Sticky notes.

### C. "Muse" AI (Creative Companion)
*   **Concept**: AI that acts as a co-author, not a spell-checker.
*   **Features**:
    *   **"Inspire Me"**: Button to generate 3 different directions for the current paragraph.
    *   **"Visualizer"**: Select text -> Generate an image (DALL-E/Stable Diffusion) to accompany it.
    *   **"Style Transfer"**: "Rewrite this like Hemingway", "Make it sound like a sci-fi novel".

---

## 4. Immediate Action Plan (Next 24 Hours)

1.  **Create Windows Installer**:
    *   Write `setup_script.iss` (Inno Setup script).
    *   Generate the `.exe` installer.
2.  **UI Polish (Quick Wins)**:
    *   Implement a basic "Zen Mode" toggle.
    *   Add a "Theme Selector" with 3 artist-curated themes (e.g., "Midnight Coffee", "Forest Walk", "Paper & Ink").
3.  **Documentation**:
    *   Update `README.md` to reflect the new "Artist" positioning.

