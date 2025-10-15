# 🎯 PyMD Editor - File Association Guide

## Q1: How to associate .md files with PyMD Editor?

We offer **3 methods**, ranked by simplicity:

---

## 🥇 Method 1: Drag & Drop (zero setup, recommended!)

### Pros
- ✅ **Simplest** - no setup
- ✅ **No permissions** - no admin needed
- ✅ **Instant** - works immediately

### How to use

**A: Drag file onto icon**
```
1. Find any .md file
2. Drag it onto run_editor.bat icon
3. Editor opens the file automatically
```

**B: Create desktop shortcut (even easier)**
```
1. Right-click run_editor.bat
2. Send to → Desktop shortcut
3. (Optional) Rename to "PyMD Editor"
4. Drag files onto shortcut anytime
```

Tip: You can drag multiple .md files at once (opens each in turn)

---

## 🥈 Method 2: Right-click "Open with"

### Pros
- ✅ No admin needed
- ✅ Integrated into right-click menu
- ✅ Can set as default app

### Setup steps

**One-time setup:**
```
1. Right-click any .md file
2. Open with → Choose another app
3. Click "More apps" → Scroll to bottom
4. Click "Look for another app on this PC"
5. Browse to run_editor.bat and select it
6. ☑️ Check "Always use this app to open .md files"
7. Confirm
```

**After setup:**
- Double-click any .md file to open in PyMD Editor
- Right-click → Open with will show PyMD Editor

---

## 🥉 Method 3: Registry association (system-wide)

### Pros
- ✅ System-wide association
- ✅ Double-click to open
- ✅ Icon and description

### ⚠️ Cons
- Requires admin rights
- Modifies registry

### How to use

**Register association:**
```
1. Right-click register_md_association.bat
2. Run as administrator
3. Follow prompts
```

**Unregister:**
```
1. Right-click unregister_md_association.bat
2. Run as administrator
```

**Result:**
- Double-click any .md file opens in PyMD Editor
- Right-click any file shows "Open with PyMD Editor"

---

## 📊 Comparison Table

| Method         | Simplicity | Permissions | Recommended |
|---------------|------------|-------------|-------------|
| Drag & Drop   | ⭐⭐⭐⭐⭐      | None        | 🥇 Best     |
| Right-click   | ⭐⭐⭐⭐       | None        | 🥈 Good     |
| Registry      | ⭐⭐⭐        | Admin       | 🥉 Optional |

---

## 🎬 Recommended workflow

### For new users (easiest)
```
1. Unzip PyMD Editor to any folder
2. Right-click run_editor.bat → Send to desktop shortcut
3. Drag .md files onto desktop shortcut
✅ Done! No setup needed
```

### For frequent users (one-time setup)
```
1. Right-click any .md file
2. Open with → Choose run_editor.bat
3. Check "Always use"
✅ Double-click .md files to open
```

### For advanced users (system integration)
```
1. Run register_md_association.bat as admin
✅ Full system integration
```

---

## 🔧 Troubleshooting

### Q: Drag & drop doesn't work?
**A**: Make sure you drag onto run_editor.bat, not a folder

### Q: Python not found?
**A**: Check if `.venv` exists, run install.bat to reinstall

### Q: Double-click .md opens another app?
**A**: Right-click file → Open with → Choose PyMD Editor

### Q: Restore default app for .md?
**A**: 
- Method 2: Right-click → Open with → Choose another app
- Method 3: Run unregister_md_association.bat

---

## 💡 Advanced tips

### Create SendTo menu item
```
1. Win+R, type shell:sendto to open SendTo folder
2. Create shortcut to run_editor.bat in SendTo
3. Rename to "PyMD Editor"
4. Right-click any file → Send to → PyMD Editor
```

### Command line usage
```batch
# Open specific file
run_editor.bat "C:\path\to\file.md"

# Launch from command line
cd C:\PyMDEditor\src
..\venv\Scripts\python.exe -m pymd_editor.main file.md
```

---

## 🎯 Best practice

**For personal users**:
- Use **Method 1 (Drag & Drop)**, simplest

**For teams/companies**:
- Use **Method 2 (Right-click)**, one-time setup

**For developers**:
- Use **Method 3 (Registry)**, full integration

---

## 📌 Summary

**Most recommended**: Create desktop shortcut + drag & drop
- Zero setup
- No permissions
- No learning curve

**Just 30 seconds**:
```
1. Right-click run_editor.bat → Send to desktop shortcut
2. Drag .md file onto desktop icon
3. Start editing!
```

✅ Simple, worry-free, always available!
