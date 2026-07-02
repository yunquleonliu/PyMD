@echo off
REM PyMD Editor - 关联 .md 文件脚本 (可执行文件版本)
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

REM 获取当前脚本所在目录
set "INSTALL_DIR=%~dp0"
set "EDITOR_PATH=%INSTALL_DIR%dist\PyMDEditor\PyMDEditor.exe"

REM 检查可执行文件是否存在
if not exist "%EDITOR_PATH%" (
    echo.
    echo [错误] 未找到 PyMD Editor 可执行文件:
    echo %EDITOR_PATH%
    echo.
    echo 当前目录: %CD%
    echo 脚本目录: %INSTALL_DIR%
    echo.
    echo 请先运行 quick_build.bat 构建可执行文件
    pause
    exit /b 1
)

echo.
echo 找到可执行文件: %EDITOR_PATH%

echo.
echo [1/2] 注册文件关联到注册表...
echo.

REM 注册 .md 文件类型
echo 注册 .md 扩展名...
reg add "HKEY_CLASSES_ROOT\.md" /ve /d "PyMDEditor.Document" /f
if errorlevel 1 (
    echo [错误] 注册 .md 扩展名失败!
    echo 请确保以管理员身份运行此脚本
    pause
    exit /b 1
)
echo OK - .md 扩展名已注册

REM 设置文件类型描述
echo 设置文件类型描述...
reg add "HKEY_CLASSES_ROOT\PyMDEditor.Document" /ve /d "Markdown Document" /f
echo OK - 文件类型描述已设置

REM 设置默认图标
echo 设置默认图标...
reg add "HKEY_CLASSES_ROOT\PyMDEditor.Document\DefaultIcon" /ve /d "\"%EDITOR_PATH%\",0" /f
echo OK - 默认图标已设置

REM 设置双击打开命令
echo 设置打开命令...
reg add "HKEY_CLASSES_ROOT\PyMDEditor.Document\shell\open\command" /ve /d "\"%EDITOR_PATH%\" \"%%1\"" /f
if errorlevel 1 (
    echo [错误] 注册打开命令失败!
    pause
    exit /b 1
)
echo OK - 打开命令已设置

REM 添加右键菜单（所有文件）
echo 添加右键菜单...
reg add "HKEY_CLASSES_ROOT\*\shell\PyMDEditor" /ve /d "用 PyMD Editor 打开" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PyMDEditor\command" /ve /d "\"%EDITOR_PATH%\" \"%%1\"" /f
echo OK - 右键菜单已添加

echo [2/2] 刷新文件关联缓存...

REM 刷新 Windows 资源管理器
taskkill /f /im explorer.exe >nul 2>&1
timeout /t 1 /nobreak >nul
start explorer.exe

echo.
echo ========================================
echo   文件关联设置完成！
echo ========================================
echo.
echo 现在可以：
echo   ✓ 双击任意 .md 文件，将自动用 PyMD Editor 打开
echo   ✓ 右键任意文件，选择"用 PyMD Editor 打开"
echo.
echo 可执行文件位置:
echo   %EDITOR_PATH%
echo.
echo 如需取消关联，请运行 unregister_md_association.bat
echo.
pause
