@echo off
REM PyMD Editor 一键安装脚本
REM 自动完成：下载代码、创建虚拟环境、安装依赖、创建快捷方式

echo ========================================
echo   PyMD Editor 一键安装程序
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.11+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] 检测 Python 环境...
python --version

REM 设置安装目录
set "INSTALL_DIR=%USERPROFILE%\PyMDEditor"
echo.
echo [2/5] 安装目录: %INSTALL_DIR%
echo.

REM 创建安装目录
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
cd /d "%INSTALL_DIR%"

REM 创建虚拟环境
echo [3/5] 创建 Python 虚拟环境...
python -m venv .venv
if errorlevel 1 (
    echo [错误] 虚拟环境创建失败
    pause
    exit /b 1
)

REM 安装依赖
echo.
echo [4/5] 安装依赖包（需要几分钟）...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\pip.exe install PyQt6 PyQt6-WebEngine markdown2 python-docx
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

REM 创建源代码目录
if not exist "src\pymd_editor" mkdir "src\pymd_editor"

echo.
echo [5/5] 下载源代码...
REM 这里可以用 curl 或 git clone 下载
REM 现在先提示用户手动复制
echo.
echo ========================================
echo   安装即将完成！
echo ========================================
echo.
echo 请将以下文件复制到: %INSTALL_DIR%\src\pymd_editor\
echo   - main.py
echo   - app.py
echo   - renderer.py
echo   - exporter.py
echo   - __init__.py
echo.
echo 或者从 GitHub 下载完整代码包
echo.
pause

REM 创建桌面快捷方式脚本
echo [创建启动脚本]
(
echo @echo off
echo cd /d "%INSTALL_DIR%\src"
echo "%INSTALL_DIR%\.venv\Scripts\python.exe" -m pymd_editor.main
) > "%INSTALL_DIR%\PyMD_Editor.bat"

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 启动方式：
echo   双击: %INSTALL_DIR%\PyMD_Editor.bat
echo.
echo 可选：创建桌面快捷方式
echo   右键 PyMD_Editor.bat -^> 发送到 -^> 桌面快捷方式
echo.
pause
