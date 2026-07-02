@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

echo ========================================
echo    PyMD Editor - Build and Package
echo ========================================
echo.

cd /d "%~dp0"

REM Step 1: Build with PyInstaller
echo [1/5] Building executable with PyInstaller...
pyinstaller build_exe.spec --noconfirm

if %errorlevel% neq 0 (
    echo ERROR: PyInstaller build failed!
    pause
    exit /b 1
)

REM Step 2: Copy python313.dll
echo.
echo [2/5] Copying python313.dll...
copy /Y "D:\InstalledTools\Python313\python313.dll" "dist\PyMDEditor\" >nul 2>&1

if %errorlevel% neq 0 (
    echo ERROR: Failed to copy python313.dll!
    pause
    exit /b 1
)

REM Step 3: Verify python313.dll exists
if exist "dist\PyMDEditor\python313.dll" (
    echo SUCCESS: python313.dll copied successfully!
) else (
    echo ERROR: python313.dll not found in dist folder!
    pause
    exit /b 1
)

REM Step 4: Create release directory and copy files
echo.
echo [3/5] Creating release package...
if exist "release\PyMD-v0.2.0-Windows" (
    rmdir /s /q "release\PyMD-v0.2.0-Windows" >nul 2>&1
)
mkdir "release\PyMD-v0.2.0-Windows" >nul 2>&1

echo Copying files...
xcopy "dist\PyMDEditor\*" "release\PyMD-v0.2.0-Windows\" /E /I /Y /Q >nul 2>&1

REM Create launcher script
echo @echo off > "release\PyMD-v0.2.0-Windows\Launch PyMD Editor.bat"
echo start "" "PyMDEditor.exe" %%* >> "release\PyMD-v0.2.0-Windows\Launch PyMD Editor.bat"

REM Copy documentation
copy /Y "README.md" "release\PyMD-v0.2.0-Windows\" >nul 2>&1
copy /Y "LICENSE" "release\PyMD-v0.2.0-Windows\" >nul 2>&1
copy /Y "QUICKSTART.md" "release\PyMD-v0.2.0-Windows\" >nul 2>&1
copy /Y "RELEASE_NOTES_v0.2.0.md" "release\PyMD-v0.2.0-Windows\" >nul 2>&1

REM Step 5: Create ZIP archive
echo.
echo [4/5] Creating ZIP archive...
cd release
powershell -Command "Compress-Archive -Path 'PyMD-v0.2.0-Windows\*' -DestinationPath 'PyMD-v0.2.0-Windows.zip' -Force" >nul 2>&1
cd ..

if exist "release\PyMD-v0.2.0-Windows.zip" (
    echo SUCCESS: ZIP archive created!
) else (
    echo ERROR: Failed to create ZIP archive!
    pause
    exit /b 1
)

REM Step 6: Show results
echo.
echo [5/5] Build complete!
echo.
echo ========================================
echo         BUILD SUMMARY
echo ========================================
echo.
echo Executable: dist\PyMDEditor\PyMDEditor.exe
echo python313.dll: INCLUDED
echo Release package: release\PyMD-v0.2.0-Windows\
echo ZIP archive: release\PyMD-v0.2.0-Windows.zip
echo.

for %%A in ("release\PyMD-v0.2.0-Windows.zip") do (
    set size=%%~zA
    set /a sizeMB=!size! / 1048576
    echo ZIP Size: !sizeMB! MB
)

echo.
echo ========================================
echo.
echo Next steps:
echo 1. Test the executable in: release\PyMD-v0.2.0-Windows\
echo 2. Upload PyMD-v0.2.0-Windows.zip to GitHub Release
echo 3. Use tag: v0.2.0-chat-enhancement
echo.
echo Press any key to test the executable...
pause >nul

cd "release\PyMD-v0.2.0-Windows"
start PyMDEditor.exe
