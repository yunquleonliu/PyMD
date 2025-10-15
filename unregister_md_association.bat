@echo off
REM 取消 .md 文件关联

echo ========================================
echo   取消 .md 文件关联
echo ========================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if errorlevel 1 (
    echo [错误] 需要管理员权限！
    echo 请右键此脚本，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo 正在移除注册表项...

REM 删除注册表项
reg delete "HKEY_CLASSES_ROOT\.md" /f
reg delete "HKEY_CLASSES_ROOT\PyMDEditor.Document" /f /s
reg delete "HKEY_CLASSES_ROOT\*\shell\PyMDEditor" /f /s

echo.
echo 文件关联已取消
echo.
pause
