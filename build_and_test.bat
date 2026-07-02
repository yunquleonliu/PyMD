@echo off
echo ========================================
echo    Building PyMD Editor Executable
echo    Please wait, this takes 2-3 minutes...
echo ========================================
echo.

cd /d "%~dp0"

echo Building with PyInstaller...
pyinstaller build_exe.spec --noconfirm

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ Build completed successfully!
    echo ========================================
    echo.
    echo Executable location: dist\PyMDEditor_v0.2.0\PyMDEditor.exe
    echo.
    echo Testing the executable...
    echo.
    
    REM Test if python313.dll is in the dist folder
    if exist "dist\PyMDEditor_v0.2.0\python313.dll" (
        echo ✅ python313.dll found in dist folder
    ) else (
        echo ❌ Warning: python313.dll not found!
    )
    
    echo.
    echo Press any key to test run the executable...
    pause >nul
    
    cd dist\PyMDEditor_v0.2.0
    start PyMDEditor.exe
    
) else (
    echo.
    echo ❌ Build failed!
    echo Please check the error messages above.
    pause
)
