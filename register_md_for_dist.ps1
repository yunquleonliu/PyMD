# PyMD Editor - 注册 .md 文件关联 (PowerShell 版本)
# 此脚本会自动请求管理员权限

# 检查是否以管理员身份运行
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "需要管理员权限,正在请求提升..." -ForegroundColor Yellow
    
    # 重新以管理员身份运行此脚本
    $scriptPath = $MyInvocation.MyCommand.Path
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" -Verb RunAs
    exit
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PyMD Editor - .md 文件关联工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 获取脚本所在目录
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$exePath = Join-Path $scriptDir "dist\PyMDEditor\PyMDEditor.exe"

Write-Host "脚本目录: $scriptDir" -ForegroundColor Gray
Write-Host "可执行文件路径: $exePath" -ForegroundColor Gray
Write-Host ""

# 检查可执行文件是否存在
if (-not (Test-Path $exePath)) {
    Write-Host "[错误] 未找到 PyMD Editor 可执行文件!" -ForegroundColor Red
    Write-Host "路径: $exePath" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先运行 quick_build.bat 构建可执行文件" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "按回车键退出"
    exit 1
}

Write-Host "✓ 找到可执行文件" -ForegroundColor Green
Write-Host ""

try {
    Write-Host "[1/5] 注册 .md 扩展名..." -ForegroundColor Yellow
    New-Item -Path "Registry::HKEY_CLASSES_ROOT\.md" -Force | Out-Null
    Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\.md" -Name "(Default)" -Value "PyMDEditor.Document"
    Write-Host "✓ .md 扩展名已注册" -ForegroundColor Green
    
    Write-Host "[2/5] 设置文件类型描述..." -ForegroundColor Yellow
    New-Item -Path "Registry::HKEY_CLASSES_ROOT\PyMDEditor.Document" -Force | Out-Null
    Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\PyMDEditor.Document" -Name "(Default)" -Value "Markdown Document"
    Write-Host "✓ 文件类型描述已设置" -ForegroundColor Green
    
    Write-Host "[3/5] 设置默认图标..." -ForegroundColor Yellow
    New-Item -Path "Registry::HKEY_CLASSES_ROOT\PyMDEditor.Document\DefaultIcon" -Force | Out-Null
    Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\PyMDEditor.Document\DefaultIcon" -Name "(Default)" -Value "`"$exePath`",0"
    Write-Host "✓ 默认图标已设置" -ForegroundColor Green
    
    Write-Host "[4/5] 设置打开命令..." -ForegroundColor Yellow
    New-Item -Path "Registry::HKEY_CLASSES_ROOT\PyMDEditor.Document\shell\open\command" -Force | Out-Null
    Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\PyMDEditor.Document\shell\open\command" -Name "(Default)" -Value "`"$exePath`" `"%1`""
    Write-Host "✓ 打开命令已设置" -ForegroundColor Green
    
    Write-Host "[5/5] 添加右键菜单..." -ForegroundColor Yellow
    New-Item -Path "Registry::HKEY_CLASSES_ROOT\*\shell\PyMDEditor" -Force | Out-Null
    Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\*\shell\PyMDEditor" -Name "(Default)" -Value "用 PyMD Editor 打开"
    New-Item -Path "Registry::HKEY_CLASSES_ROOT\*\shell\PyMDEditor\command" -Force | Out-Null
    Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\*\shell\PyMDEditor\command" -Name "(Default)" -Value "`"$exePath`" `"%1`""
    Write-Host "✓ 右键菜单已添加" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "刷新 Windows 资源管理器..." -ForegroundColor Yellow
    Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
    Start-Process explorer.exe
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  文件关联设置完成！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "现在可以：" -ForegroundColor Cyan
    Write-Host "  ✓ 双击任意 .md 文件，将自动用 PyMD Editor 打开" -ForegroundColor White
    Write-Host "  ✓ 右键任意文件，选择'用 PyMD Editor 打开'" -ForegroundColor White
    Write-Host ""
    Write-Host "可执行文件位置:" -ForegroundColor Gray
    Write-Host "  $exePath" -ForegroundColor Gray
    Write-Host ""
    Write-Host "如需取消关联，请运行 unregister_md_for_dist.ps1" -ForegroundColor Yellow
    
} catch {
    Write-Host ""
    Write-Host "[错误] 注册失败!" -ForegroundColor Red
    Write-Host "错误信息: $_" -ForegroundColor Red
    Write-Host ""
    Read-Host "按回车键退出"
    exit 1
}

Write-Host ""
Read-Host "按回车键退出"
