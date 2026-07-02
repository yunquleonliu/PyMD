@echo off
echo ========================================
echo   PyMD Editor - Release Packager
echo ========================================
echo.

cd /d "%~dp0"

if not exist "dist\PyMDEditor_v0.2.0\PyMDEditor.exe" (
    echo ERROR: PyMDEditor.exe not found!
    echo Please run build_windows_exe.bat first.
    pause
    exit /b 1
)

echo Step 1: Creating release directory...
if exist "release\PyMD-v0.2.0-Windows" rmdir /s /q "release\PyMD-v0.2.0-Windows"
mkdir "release\PyMD-v0.2.0-Windows"

echo Step 2: Copying executable and dependencies...
xcopy "dist\PyMDEditor_v0.2.0\*" "release\PyMD-v0.2.0-Windows\" /E /I /Y

echo Step 3: Creating launcher script...
(
echo @echo off
echo start "" "PyMDEditor.exe" %%*
) > "release\PyMD-v0.2.0-Windows\Launch PyMD Editor.bat"

echo Step 4: Copying documentation...
copy "README.md" "release\PyMD-v0.2.0-Windows\" >nul
copy "LICENSE" "release\PyMD-v0.2.0-Windows\" >nul
copy "QUICKSTART.md" "release\PyMD-v0.2.0-Windows\" >nul

echo Step 5: Creating README for users...
(
echo # PyMD Editor v0.2.0 - Windows Release
echo.
echo ## Quick Start
echo.
echo 1. Double-click "Launch PyMD Editor.bat" or "PyMDEditor.exe" to start
echo 2. Open or create a markdown file
echo 3. Use the AI chat panel on the right for assistance
echo.
echo ## Features
echo - Real-time markdown preview
echo - AI-powered writing assistance
echo - Multiple AI provider support
echo - Modern gradient UI design
echo - Export to DOCX and HTML
echo.
echo ## System Requirements
echo - Windows 10 or later
echo - No Python installation required!
echo.
echo ## Support
echo Visit: https://github.com/yunquleonliu/PyMD
echo.
echo Enjoy your AI-enhanced markdown editing experience! 🎉
) > "release\PyMD-v0.2.0-Windows\README_Windows.txt"

echo Step 6: Creating release archive...
cd release
powershell -Command "Compress-Archive -Path 'PyMD-v0.2.0-Windows\*' -DestinationPath 'PyMD-v0.2.0-Windows.zip' -Force"
cd ..

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ Windows release package created!
    echo ========================================
    echo.
    echo Archive: release\PyMD-v0.2.0-Windows.zip
    echo.
    dir "release\PyMD-v0.2.0-Windows.zip" | findstr "PyMD-v0.2.0-Windows.zip"
    echo.
    echo Contents:
    echo - PyMDEditor.exe ^(Windows executable^)
    echo - All required DLLs and dependencies
    echo - Documentation and quick start guide
    echo - Launch script for easy startup
    echo.
    echo Next steps:
    echo 1. Test the executable in release\PyMD-v0.2.0-Windows\
    echo 2. Upload PyMD-v0.2.0-Windows.zip to GitHub Releases
    echo 3. Use tag: v0.2.0-chat-enhancement
    echo.
    echo Press any key to open the release directory...
    pause >nul
    explorer "release"
) else (
    echo.
    echo ❌ Failed to create release archive!
    pause
)
