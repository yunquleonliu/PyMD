@echo off
REM PyMD Editor - 关联 .md 文件脚本
REM 运行后，双击任意 .md 文件将自动用 PyMD Editor 打开

echo ========================================
echo   PyMD Editor - .md 文件关联工具
echo ========================================
echo.
echo 此操作将：
echo   1. 在注册表中注册 .md 文件关联
echo   2. 设置 PyMD Editor 为默认打开程序
echo   3. 添加右键菜单"用 PyMD Editor 打开"
echo.
echo 需要管理员权限，请确认继续...
pause

REM 检查管理员权限
net session >nul 2>&1
if errorlevel 1 (
    echo.
    echo [错误] 需要管理员权限！
    echo 请右键此脚本，选择"以管理员身份运行"
    pause
    exit /b 1
)

REM 获取当前脚本所在目录（即安装目录）
set "INSTALL_DIR=%~dp0"
set "EDITOR_PATH=%INSTALL_DIR%src\.venv\Scripts\python.exe"
set "MAIN_SCRIPT=%INSTALL_DIR%src\pymd_editor\main.py"

REM 检查编辑器是否存在
if not exist "%EDITOR_PATH%" (
    echo [错误] 未找到 Python 环境: %EDITOR_PATH%
    echo 请先运行 install.bat 安装
    pause
    exit /b 1
)

echo.
echo [1/3] 创建启动包装脚本...

REM 创建一个包装脚本，用于从命令行启动编辑器并打开文件
(
echo @echo off
echo cd /d "%INSTALL_DIR%src"
echo "%EDITOR_PATH%" -m pymd_editor.main "%%~1"
) > "%INSTALL_DIR%open_with_pymd.bat"

echo [2/3] 注册文件关联到注册表...

REM 注册 .md 文件类型
reg add "HKEY_CLASSES_ROOT\.md" /ve /d "PyMDEditor.Document" /f
reg add "HKEY_CLASSES_ROOT\PyMDEditor.Document" /ve /d "Markdown Document" /f
reg add "HKEY_CLASSES_ROOT\PyMDEditor.Document\DefaultIcon" /ve /d "%SystemRoot%\System32\notepad.exe,0" /f

REM 设置打开命令
reg add "HKEY_CLASSES_ROOT\PyMDEditor.Document\shell\open\command" /ve /d "\"%INSTALL_DIR%open_with_pymd.bat\" \"%%1\"" /f

REM 添加右键菜单
reg add "HKEY_CLASSES_ROOT\*\shell\PyMDEditor" /ve /d "用 PyMD Editor 打开" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PyMDEditor\command" /ve /d "\"%INSTALL_DIR%open_with_pymd.bat\" \"%%1\"" /f

echo [3/3] 刷新文件关联缓存...
REM 通知 Windows 刷新图标缓存
taskkill /f /im explorer.exe >nul 2>&1
start explorer.exe

echo.
echo ========================================
echo   文件关联设置完成！
echo ========================================
echo.
echo 现在可以：
echo   - 双击任意 .md 文件，将自动用 PyMD Editor 打开
echo   - 右键任意文件，选择"用 PyMD Editor 打开"
echo.
echo 如需取消关联，请运行 unregister_md.bat
echo.
pause
