@echo off
REM PyMD Editor Launch Script
REM Support: Double-click to start or drag .md files to this script icon

REM Set working directory to script location
cd /d "%~dp0"

REM Check for virtual environment, prefer virtual environment if available
if exist ".venv\Scripts\python.exe" (
    set PYTHON_CMD=".venv\Scripts\python.exe"
) else (
    set PYTHON_CMD=python
)

REM Pass file argument if provided (drag and drop support)  
if "%~1"=="" (
    %PYTHON_CMD% -m src.pymd_editor.main
) else (
    %PYTHON_CMD% -m src.pymd_editor.main "%~1"
)

REM Pause if error occurs to show error message
if errorlevel 1 pause
