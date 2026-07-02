@echo off
echo ========================================
echo   PyMD Editor - Windows EXE Builder
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller>=6.0.0
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install PyInstaller!
        pause
        exit /b 1
    )
)
echo ✓ PyInstaller ready

echo Checking project requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install requirements!
    pause
    exit /b 1
)
echo ✓ Requirements installed

echo.
echo Step 2: Killing any running processes...
taskkill /F /IM PyMDEditor.exe 2>nul
taskkill /F /IM QtWebEngineProcess.exe 2>nul
timeout /t 2 /nobreak >nul

echo Step 3: Cleaning previous builds...
if exist "build" rmdir /s /q build 2>nul
if exist "dist" (
    echo Removing dist folder, please wait...
    powershell -Command "Get-Process | Where-Object {$_.Path -like '*PyMD*'} | Stop-Process -Force" 2>nul
    timeout /t 1 /nobreak >nul
    rmdir /s /q dist 2>nul
)
echo ✓ Cleaned

echo.
echo Step 4: Building Windows executable...
echo This may take several minutes...
pyinstaller build_exe.spec --noconfirm

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ Build completed successfully!
    echo ========================================
    echo.
    echo Executable location: dist\PyMDEditor\PyMDEditor.exe
    echo.
    echo Next: Run create_windows_release.bat to package the release
    echo.
) else (
    echo.
    echo ❌ Build failed!
    echo Please check the error messages above.
    echo.
)

pause
