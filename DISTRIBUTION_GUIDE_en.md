# PyMD Editor - Distribution & Deployment Guide

## 🎯 Goal: Make it as simple as possible for users to get the tool

As you requested: **Simple, worry-free, voluntary payment**

---

## 📦 Option 1: GitHub Release (Recommended)

### Pros
✅ Free hosting  
✅ Automatic versioning  
✅ One-click download  
✅ Update notifications  

### Deployment steps

1. **Create GitHub repository**
   ```bash
   # Create new repo "pymd-editor" on GitHub
   git init
   git add .
   git commit -m "Initial release v1.0.0"
   git remote add origin https://github.com/yourusername/pymd-editor.git
   git push -u origin main
   ```

2. **Create Release**
   - Go to GitHub repo → Releases → Create a new release
   - Tag: `v1.0.0`
   - Upload: `PyMDEditor_v1.0.0.zip`

3. **User download link**
   ```
   https://github.com/yourusername/pymd-editor/releases/latest
   ```

### User workflow (3 steps)
```
1. Download PyMDEditor_v1.0.0.zip
2. Unzip and run install.bat
3. Run register_md_association.bat (optional, for .md association)
```

---

## 📦 Option 2: One-click install script (easiest)

### Principle
User runs a single command to download and install everything.

### Create installer

**File: `install_from_web.bat`**
```batch
@echo off
echo Downloading PyMD Editor from GitHub...
powershell -command "Invoke-WebRequest -Uri 'https://github.com/yourusername/pymd-editor/archive/refs/heads/main.zip' -OutFile 'pymd.zip'"
powershell -command "Expand-Archive -Path 'pymd.zip' -DestinationPath '%USERPROFILE%\PyMDEditor' -Force"
cd /d "%USERPROFILE%\PyMDEditor\pymd-editor-main"
call install.bat
```

### User workflow (1 step)
```
Run install_from_web.bat
```

---

## 📦 Option 3: PyPI release (for Python users)

### Pros
✅ Standard Python ecosystem  
✅ `pip install pymd-editor` one-step install  
✅ Automatic dependency management  

### Preparation

1. **Add `setup.py`**
   ```python
   from setuptools import setup, find_packages
   
   setup(
       name="pymd-editor",
       version="1.0.0",
       packages=find_packages("src"),
       package_dir={"": "src"},
       install_requires=[
           "PyQt6>=6.9.0",
           "PyQt6-WebEngine>=6.9.0",
           "markdown2>=2.5.0",
           "python-docx>=1.2.0",
       ],
       entry_points={
           "console_scripts": [
               "pymd-editor=pymd_editor.main:main",
           ],
       },
   )
   ```

2. **Publish to PyPI**
   ```bash
   pip install twine
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```

### User workflow (1 command)
```bash
pip install pymd-editor
pymd-editor  # Launch directly
```

---

## 🎯 Recommended strategy: Hybrid

### Phase 1: Quick start (current)
- ✅ **GitHub Release** - ZIP download
- ✅ **One-click install script** - `install.bat`
- ✅ **File association** - `register_md_association.bat`

**User workflow**:
```
https://github.com/yourusername/pymd-editor/releases
→ Download ZIP → Run install.bat
```

### Phase 2: Scale up (future)
- 🔄 **PyPI release** - `pip install pymd-editor`
- 🔄 **Auto-update** - built-in update checker
- 💡 **Cloud services** - paid sync/collab features

---

## 📊 .md file association options

### Option A: Windows registry (implemented)
✅ **Pros**: System-wide, double-click to open  
⚠️ **Cons**: Needs admin rights  
📝 **Use**: Run `register_md_association.bat`

### Option B: Right-click "Open with"
✅ **Pros**: No admin needed  
⚠️ **Cons**: Manual selection each time  
📝 **Use**: Right-click .md → Open with → run_editor.bat

### Option C: Drag & drop
✅ **Pros**: Simplest, zero setup  
📝 **Use**: Drag .md file onto run_editor.bat icon

---

## 📊 Recommended distribution workflow

### For regular users (3 steps)
```
1. Go to GitHub Release page
2. Download latest PyMDEditor_v1.0.0.zip
3. Unzip and double-click install.bat
```

### For tech users (1 command)
```bash
pip install pymd-editor  # after PyPI release
```

### For enterprise (easiest)
```
1. Place ZIP on internal server
2. Provide internal download link
3. Users unzip and run install.bat
```

---

## 💰 Voluntary payment strategy

### Current (free & open source)
- ✅ Completely free
- ✅ MIT license
- ✅ Source code public

### Future (optional paid services)
- 💡 **Cloud sync** - multi-device Markdown sync
- 💡 **Collab editing** - team real-time editing
- 💡 **Premium templates** - export template library
- 💡 **Priority support** - tech support & custom dev

**How to implement**:
- Core editor always free
- Cloud services as monthly subscription (e.g. $5/mo)
- Free trial available

---

## 🚀 What to do now

### Right now:

1. **Create GitHub repo**
   ```bash
   Run: create_distribution.bat
   Upload to GitHub
   ```

2. **Test file association**
   ```bash
   Run register_md_association.bat as admin
   Double-click any .md file to test
   ```

3. **Share with friends**
   ```
   Send PyMDEditor_v1.0.0.zip
   Tell them to run install.bat
   ```

---

## 📞 User support

### Docs
- ✅ `START_HERE_en.txt` - First use guide
- ✅ `QUICKSTART_en.md` - Quick start
- ✅ `README_en.md` - Full docs
- ✅ `EXAMPLE.md` - Feature demo

### Feedback
- GitHub Issues (recommended)
- Email support
- Community forum

---

**Summary**: GitHub Release + install.bat is currently the simplest way to distribute!
