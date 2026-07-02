@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

echo ========================================
echo   PyMD Editor - Quick Build (Fixed)
echo ========================================
echo.

cd /d "%~dp0"

REM Check Python DLL exists
if not exist "D:\InstalledTools\Python313\python313.dll" (
    echo ERROR: python313.dll not found at D:\InstalledTools\Python313\
    echo Please check your Python installation.
    pause
    exit /b 1
)

REM Clean build cache only (keep dist if it has working version)
echo [1/4] Cleaning build cache...
if exist "build" (
    rmdir /s /q "build" >nul 2>&1
)

REM Build with PyInstaller
echo.
echo [2/4] Building with PyInstaller...
echo This may take 2-3 minutes...
pyinstaller build_exe.spec --noconfirm

if %errorlevel% neq 0 (
    echo.
    echo ERROR: PyInstaller build failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)

REM Copy python313.dll
echo.
echo [3/4] Ensuring python313.dll is present...
copy /Y "D:\InstalledTools\Python313\python313.dll" "dist\PyMDEditor\" >nul 2>&1

if not exist "dist\PyMDEditor\python313.dll" (
    echo ERROR: Failed to copy python313.dll!
    pause
    exit /b 1
)

REM Verify executable exists
if not exist "dist\PyMDEditor\PyMDEditor.exe" (
    echo ERROR: PyMDEditor.exe not found!
    pause
    exit /b 1
)

echo SUCCESS: python313.dll copied!

REM Show summary
echo.
echo [4/4] Build complete!
echo.
echo ========================================
echo         BUILD SUCCESS
echo ========================================
echo.
echo Location: dist\PyMDEditor\
echo Executable: dist\PyMDEditor\PyMDEditor.exe
echo DLL Status: python313.dll INCLUDED
echo.

for /f %%A in ('dir /s /b "dist\PyMDEditor\*" ^| find /c /v ""') do set filecount=%%A
echo Total files: %filecount%
echo.

REM Clean up build directory to avoid confusion
echo Cleaning up build directory...
if exist "build" (
    rmdir /s /q "build" >nul 2>&1
    echo Build cache removed.
)

echo ========================================
echo.
echo Next steps:
echo 1. Test: cd dist\PyMDEditor ^&^& .\PyMDEditor.exe
echo 2. Register .md files: .\register_md_for_dist.bat (需要管理员)
echo 3. Package: Run create_release_package.bat
echo.
pause

exit /b 0
