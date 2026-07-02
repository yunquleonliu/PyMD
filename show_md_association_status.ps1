# 显示 .md 文件关联的详细信息(不需要管理员权限)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  .md 文件关联详细信息" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 系统级关联 (HKEY_CLASSES_ROOT)
Write-Host "[系统级关联]" -ForegroundColor Yellow
Write-Host ""

$mdExt = "Registry::HKEY_CLASSES_ROOT\.md"
if (Test-Path $mdExt) {
    $defaultValue = (Get-ItemProperty -Path $mdExt -Name "(Default)" -ErrorAction SilentlyContinue).'(Default)'
    Write-Host ".md 文件类型: $defaultValue" -ForegroundColor White
} else {
    Write-Host ".md 未注册" -ForegroundColor Red
}

# 检查所有 PyMD 相关的类型
Write-Host ""
Write-Host "所有 PyMD 相关的类型:" -ForegroundColor Cyan
Get-ChildItem -Path "Registry::HKEY_CLASSES_ROOT" -ErrorAction SilentlyContinue | 
    Where-Object { $_.PSChildName -like "*PyMD*" } | 
    ForEach-Object {
        Write-Host "  - $($_.PSChildName)" -ForegroundColor White
    }

Write-Host ""
Write-Host "[用户级关联]" -ForegroundColor Yellow
Write-Host ""

# 2. 用户选择的程序列表
$openWithList = "Registry::HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.md\OpenWithList"
if (Test-Path $openWithList) {
    Write-Host "OpenWithList (打开方式列表):" -ForegroundColor Cyan
    $props = Get-ItemProperty -Path $openWithList
    $mruList = $props.MRUList
    
    if ($mruList) {
        Write-Host "  MRU 顺序: $mruList" -ForegroundColor Gray
        Write-Host ""
    }
    
    $props.PSObject.Properties | Where-Object { $_.Name -match '^[a-z]$' } | ForEach-Object {
        $marker = if ($_.Value -like "*PyMDEditor*") { " ← 残留!" } else { "" }
        $color = if ($_.Value -like "*PyMDEditor*") { "Yellow" } else { "White" }
        Write-Host "  $($_.Name): $($_.Value)$marker" -ForegroundColor $color
    }
} else {
    Write-Host "OpenWithList 不存在" -ForegroundColor Gray
}

Write-Host ""

# 3. 默认程序选择
$userChoice = "Registry::HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.md\UserChoice"
if (Test-Path $userChoice) {
    $progId = (Get-ItemProperty -Path $userChoice -Name "ProgId" -ErrorAction SilentlyContinue).ProgId
    Write-Host "默认程序 (UserChoice): $progId" -ForegroundColor White
} else {
    Write-Host "默认程序: 未设置" -ForegroundColor Gray
}

Write-Host ""

# 4. OpenWithProgids
$progids = "Registry::HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.md\OpenWithProgids"
if (Test-Path $progids) {
    Write-Host "OpenWithProgids:" -ForegroundColor Cyan
    $props = Get-ItemProperty -Path $progids
    $props.PSObject.Properties | Where-Object { $_.Name -ne 'PSPath' -and $_.Name -ne 'PSParentPath' -and $_.Name -ne 'PSChildName' -and $_.Name -ne 'PSProvider' } | ForEach-Object {
        $marker = if ($_.Name -like "*PyMDEditor*") { " ← 残留?" } else { ""  }
        $color = if ($_.Name -like "*PyMDEditor*") { "Yellow" } else { "White" }
        Write-Host "  - $($_.Name)$marker" -ForegroundColor $color
    }
}

Write-Host ""
Write-Host "[右键菜单]" -ForegroundColor Yellow
Write-Host ""

# 5. 右键菜单
$shellMenu = "Registry::HKEY_CLASSES_ROOT\*\shell\PyMDEditor"
if (Test-Path $shellMenu) {
    $menuText = (Get-ItemProperty -Path $shellMenu -Name "(Default)" -ErrorAction SilentlyContinue).'(Default)'
    $cmdPath = "Registry::HKEY_CLASSES_ROOT\*\shell\PyMDEditor\command"
    $command = (Get-ItemProperty -Path $cmdPath -Name "(Default)" -ErrorAction SilentlyContinue).'(Default)'
    
    Write-Host "右键菜单文本: $menuText" -ForegroundColor White
    Write-Host "执行命令: $command" -ForegroundColor Gray
} else {
    Write-Host "右键菜单未注册" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "说明:" -ForegroundColor Yellow
Write-Host "  - 标记 '← 残留!' 的项是可以清理的旧条目" -ForegroundColor Gray
Write-Host "  - 运行 clean_md_association_duplicates.ps1 清理这些残留" -ForegroundColor Gray
Write-Host ""
