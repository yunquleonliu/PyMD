@echo off
setlocal
REM PyMD Editor Windows distribution build script

echo ========================================
echo   PyMD Editor - Build Distribution
echo ========================================
echo.

set "PYTHON=.venv\Scripts\python.exe"
set "PYINSTALLER=.venv\Scripts\pyinstaller.exe"

if not exist "%PYTHON%" (
    echo [ERROR] Python from virtual environment not found: %PYTHON%
    echo Ensure install.bat has been run and .venv exists.
    goto :fail
)

if not exist "%PYINSTALLER%" (
    echo [ERROR] PyInstaller not found: %PYINSTALLER%
    echo Install with: %PYTHON% -m pip install pyinstaller
    goto :fail
)

    for /f "delims=" %%i in ('call "%PYTHON%" -c "import sys; sys.path.insert(0, 'src'); from pymd_editor.config import APP_VERSION; print(APP_VERSION)"') do set "VERSION=%%i"
if not defined VERSION set "VERSION=dev"

set "OUTPUT_BASE=PyMDEditor_Distribution"
set "OUTPUT_DIR=%OUTPUT_BASE%\PyMDEditor_v%VERSION%"
set "ZIP_NAME=PyMDEditor_Windows_v%VERSION%.zip"
set "DIST_DIR=dist\PyMDEditor"

echo [1/6] Cleaning previous build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "%OUTPUT_BASE%" rmdir /s /q "%OUTPUT_BASE%"
if exist "%ZIP_NAME%" del /q "%ZIP_NAME%"

echo [2/6] Running PyInstaller...
"%PYINSTALLER%" --noconfirm PyMDEditor.spec
if errorlevel 1 goto :fail

if not exist "%DIST_DIR%\PyMDEditor.exe" (
    echo [ERROR] PyMDEditor.exe was not produced.
    goto :fail
)

echo [3/6] Preparing distribution folder...
mkdir "%OUTPUT_DIR%" || goto :fail
mkdir "%OUTPUT_DIR%\app"

echo [4/6] Copying executable bundle...
xcopy /E /I /Y "%DIST_DIR%" "%OUTPUT_DIR%\app" >nul
if errorlevel 1 goto :fail

echo [5/6] Copying documentation and helper scripts...
copy "README.md" "%OUTPUT_DIR%\" >nul
copy "QUICKSTART.md" "%OUTPUT_DIR%\" >nul
copy "EXAMPLE.md" "%OUTPUT_DIR%\" >nul
copy "LICENSE" "%OUTPUT_DIR%\" >nul
copy "requirements.txt" "%OUTPUT_DIR%\" >nul
copy "install.bat" "%OUTPUT_DIR%\" >nul
copy "register_md_association.bat" "%OUTPUT_DIR%\" >nul
copy "unregister_md_association.bat" "%OUTPUT_DIR%\" >nul
copy "run_editor.bat" "%OUTPUT_DIR%\" >nul
copy "run_editor.ps1" "%OUTPUT_DIR%\" >nul
copy "START_HERE.txt" "%OUTPUT_DIR%\" >nul

echo [6/6] Creating release archive...
powershell -NoProfile -Command "Compress-Archive -Path '%OUTPUT_DIR%\*' -DestinationPath '%ZIP_NAME%' -Force"
if errorlevel 1 goto :fail

echo.
echo ========================================
echo   Distribution ready
echo ========================================
echo Output folder: %OUTPUT_DIR%
echo Release file : %ZIP_NAME%
echo.
echo Contents include:
echo   - app\PyMDEditor.exe (portable executable)
echo   - Helper scripts and quickstart docs
echo.
echo Tip: unzip and launch app\PyMDEditor.exe directly.
echo       Run register_md_association.bat to bind .md files.
echo.
goto :eof

:fail
echo.
echo [FAILED] Distribution build did not complete.
exit /b 1