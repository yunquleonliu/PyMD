@echo off
REM 取消 .md 文件关联

echo ========================================
echo   取消 .md 文件关联
echo ========================================
echo.
echo 需要管理员权限...
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

echo.
echo [1/2] 删除注册表项...

REM 删除 .md 文件类型关联
reg delete "HKEY_CLASSES_ROOT\.md" /f >nul 2>&1

REM 删除 PyMDEditor 文件类型
reg delete "HKEY_CLASSES_ROOT\PyMDEditor.Document" /ve /f >nul 2>&1

REM 删除右键菜单
reg delete "HKEY_CLASSES_ROOT\*\shell\PyMDEditor" /f >nul 2>&1

echo [2/2] 刷新文件关联缓存...

REM 刷新 Windows 资源管理器
taskkill /f /im explorer.exe >nul 2>&1
timeout /t 1 /nobreak >nul
start explorer.exe

echo.
echo ========================================
echo   取消关联完成！
echo ========================================
echo.
echo .md 文件关联已移除
echo.
pause
