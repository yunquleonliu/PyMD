# 检查 .md 文件关联状态

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  检查 .md 文件关联状态" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查可执行文件
$exePath = Join-Path $PSScriptRoot "dist\PyMDEditor\PyMDEditor.exe"
Write-Host "可执行文件路径: $exePath" -ForegroundColor Gray
if (Test-Path $exePath) {
    Write-Host "✓ 可执行文件存在" -ForegroundColor Green
} else {
    Write-Host "✗ 可执行文件不存在" -ForegroundColor Red
}
Write-Host ""

# 检查注册表项
Write-Host "检查注册表项..." -ForegroundColor Yellow
Write-Host ""

# 检查 .md 扩展名
try {
    $mdValue = Get-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\.md" -Name "(Default)" -ErrorAction Stop
    Write-Host "✓ .md 扩展名已注册" -ForegroundColor Green
    Write-Host "  值: $($mdValue.'(Default)')" -ForegroundColor Gray
} catch {
    Write-Host "✗ .md 扩展名未注册" -ForegroundColor Red
}

# 检查文件类型
try {
    $docValue = Get-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\PyMDEditor.Document" -Name "(Default)" -ErrorAction Stop
    Write-Host "✓ PyMDEditor.Document 已注册" -ForegroundColor Green
    Write-Host "  值: $($docValue.'(Default)')" -ForegroundColor Gray
} catch {
    Write-Host "✗ PyMDEditor.Document 未注册" -ForegroundColor Red
}

# 检查打开命令
try {
    $cmdValue = Get-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\PyMDEditor.Document\shell\open\command" -Name "(Default)" -ErrorAction Stop
    Write-Host "✓ 打开命令已设置" -ForegroundColor Green
    Write-Host "  值: $($cmdValue.'(Default)')" -ForegroundColor Gray
} catch {
    Write-Host "✗ 打开命令未设置" -ForegroundColor Red
}

# 检查右键菜单
try {
    $menuValue = Get-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\*\shell\PyMDEditor" -Name "(Default)" -ErrorAction Stop
    Write-Host "✓ 右键菜单已添加" -ForegroundColor Green
    Write-Host "  值: $($menuValue.'(Default)')" -ForegroundColor Gray
} catch {
    Write-Host "✗ 右键菜单未添加" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Read-Host "按回车键退出"
