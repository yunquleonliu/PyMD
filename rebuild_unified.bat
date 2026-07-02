@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

echo ========================================
echo    PyMD Editor - Unified Rebuild
echo ========================================
echo.

cd /d "%~dp0"

REM Step 1: Clean old builds
echo [1/6] Cleaning old builds...
if exist "dist\PyMDEditor_v0.2.0" (
    echo Removing old versioned directory...
    rmdir /s /q "dist\PyMDEditor_v0.2.0" >nul 2>&1
)
if exist "dist\PyMDEditor" (
    echo Removing existing PyMDEditor directory...
    rmdir /s /q "dist\PyMDEditor" >nul 2>&1
)
if exist "build" (
    echo Removing build cache...
    rmdir /s /q "build" >nul 2>&1
)

REM Step 2: Build with PyInstaller
echo.
echo [2/6] Building executable with PyInstaller...
pyinstaller build_exe.spec --noconfirm

if %errorlevel% neq 0 (
    echo ERROR: PyInstaller build failed!
    pause
    exit /b 1
)

REM Step 3: Copy python313.dll
echo.
echo [3/6] Copying python313.dll...
copy /Y "D:\InstalledTools\Python313\python313.dll" "dist\PyMDEditor\" >nul 2>&1

if %errorlevel% neq 0 (
    echo ERROR: Failed to copy python313.dll!
    pause
    exit /b 1
)

REM Step 4: Verify python313.dll exists
if exist "dist\PyMDEditor\python313.dll" (
    echo SUCCESS: python313.dll copied successfully!
) else (
    echo ERROR: python313.dll not found in dist folder!
    pause
    exit /b 1
)

REM Step 5: Create release directory and copy files
echo.
echo [4/6] Creating release package...
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

REM Step 6: Create ZIP archive
echo.
echo [5/6] Creating ZIP archive...
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

REM Step 7: Show results
echo.
echo [6/6] Build complete!
echo.
echo ========================================
echo         BUILD SUMMARY
echo ========================================
echo.
echo Fixed location: dist\PyMDEditor\
echo Executable: dist\PyMDEditor\PyMDEditor.exe
echo python313.dll: INCLUDED
echo.
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
echo 统一的可执行文件位置:
echo   dist\PyMDEditor\PyMDEditor.exe
echo.
echo 以后每次构建都会输出到这个固定位置！
echo.
echo Press any key to test the executable...
pause >nul

cd "dist\PyMDEditor"
start PyMDEditor.exe
