@echo off
REM 创建可分发的 PyMD Editor 包

echo ========================================
echo   PyMD Editor - 创建分发包
echo ========================================
echo.

set "OUTPUT_DIR=PyMDEditor_Distribution"
set "VERSION=1.0.0"

echo [1/4] 创建分发目录...
if exist "%OUTPUT_DIR%" rmdir /s /q "%OUTPUT_DIR%"
mkdir "%OUTPUT_DIR%"

echo [2/4] 复制源代码...
xcopy /E /I /Y "src" "%OUTPUT_DIR%\src"

echo [3/4] 复制文档和脚本...
copy "README.md" "%OUTPUT_DIR%\"
copy "QUICKSTART.md" "%OUTPUT_DIR%\"
copy "EXAMPLE.md" "%OUTPUT_DIR%\"
copy "LICENSE" "%OUTPUT_DIR%\"
copy "requirements.txt" "%OUTPUT_DIR%\"
copy "install.bat" "%OUTPUT_DIR%\"
copy "register_md_association.bat" "%OUTPUT_DIR%\"
copy "unregister_md_association.bat" "%OUTPUT_DIR%\"
copy "run_editor.bat" "%OUTPUT_DIR%\"
copy "run_editor.ps1" "%OUTPUT_DIR%\"
copy "START_HERE.txt" "%OUTPUT_DIR%\"

echo [4/4] 创建压缩包...
REM 需要 PowerShell 创建 ZIP
powershell -command "Compress-Archive -Path '%OUTPUT_DIR%\*' -DestinationPath 'PyMDEditor_v%VERSION%.zip' -Force"

echo.
echo ========================================
echo   分发包创建完成！
echo ========================================
echo.
echo 输出文件: PyMDEditor_v%VERSION%.zip
echo.
echo 用户只需：
echo   1. 解压缩 ZIP 文件
echo   2. 双击 install.bat 安装
echo   3. 双击 register_md_association.bat 关联 .md 文件
echo   4. 开始使用！
echo.
pause
