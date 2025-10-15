@echo off
REM PyMD Editor Launch Script
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (set PYTHON_CMD=".venv\Scripts\python.exe") else (set PYTHON_CMD=python)
if "%~1"=="" (%PYTHON_CMD% -m src.pymd_editor.main) else (%PYTHON_CMD% -m src.pymd_editor.main "%~1")
if errorlevel 1 pause
