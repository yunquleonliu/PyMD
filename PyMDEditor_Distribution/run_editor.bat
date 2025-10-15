@echo off
REM PyMD Editor 启动脚本
REM 支持：双击启动 或 拖拽 .md 文件到此脚本图标

cd /d "%~dp0src"

REM 如果有参数（拖拽的文件），传递给编辑器
if "%~1"=="" (
    "%~dp0.venv\Scripts\python.exe" -m pymd_editor.main
) else (
    "%~dp0.venv\Scripts\python.exe" -m pymd_editor.main "%~1"
)

REM 如果出错，暂停显示错误信息
if errorlevel 1 pause
