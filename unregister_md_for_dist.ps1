# PyMD Editor - 取消 .md 文件关联 (PowerShell 版本)
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
Write-Host "  取消 .md 文件关联" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    Write-Host "[1/3] 删除 .md 文件类型关联..." -ForegroundColor Yellow
    Remove-Item -Path "Registry::HKEY_CLASSES_ROOT\.md" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✓ .md 文件类型关联已删除" -ForegroundColor Green
    
    Write-Host "[2/3] 删除 PyMDEditor 文件类型..." -ForegroundColor Yellow
    Remove-Item -Path "Registry::HKEY_CLASSES_ROOT\PyMDEditor.Document" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✓ PyMDEditor 文件类型已删除" -ForegroundColor Green
    
    Write-Host "[3/3] 删除右键菜单..." -ForegroundColor Yellow
    Remove-Item -Path "Registry::HKEY_CLASSES_ROOT\*\shell\PyMDEditor" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✓ 右键菜单已删除" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "刷新 Windows 资源管理器..." -ForegroundColor Yellow
    Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
    Start-Process explorer.exe
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  取消关联完成！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host ".md 文件关联已移除" -ForegroundColor White
    
} catch {
    Write-Host ""
    Write-Host "[错误] 取消关联失败!" -ForegroundColor Red
    Write-Host "错误信息: $_" -ForegroundColor Red
    Write-Host ""
    Read-Host "按回车键退出"
    exit 1
}

Write-Host ""
Read-Host "按回车键退出"
