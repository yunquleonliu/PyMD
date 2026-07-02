# 清理 .md 文件关联中的 PyMDEditor 残留项
# 此脚本会自动请求管理员权限

# 检查是否以管理员身份运行
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "需要管理员权限,正在请求提升..." -ForegroundColor Yellow
    $scriptPath = $MyInvocation.MyCommand.Path
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" -Verb RunAs
    exit
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  清理 PyMDEditor 残留项" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$cleaned = 0

try {
    # 1. 清理 HKEY_CURRENT_USER 的 OpenWithList
    Write-Host "[1/4] 清理用户的 OpenWithList..." -ForegroundColor Yellow
    $openWithPath = "Registry::HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.md\OpenWithList"
    
    if (Test-Path $openWithPath) {
        $properties = Get-Item $openWithPath | Select-Object -ExpandProperty Property
        foreach ($prop in $properties) {
            if ($prop -match '^[a-z]$') {  # 只处理 a, b, c 等字母属性
                $value = (Get-ItemProperty -Path $openWithPath -Name $prop).$prop
                if ($value -like "*PyMDEditor*") {
                    Write-Host "  移除: $prop = $value" -ForegroundColor Gray
                    Remove-ItemProperty -Path $openWithPath -Name $prop -ErrorAction SilentlyContinue
                    $cleaned++
                }
            }
        }
        
        # 重建 MRUList
        $mruList = (Get-ItemProperty -Path $openWithPath -Name "MRUList" -ErrorAction SilentlyContinue).MRUList
        if ($mruList) {
            $newMruList = ($mruList.ToCharArray() | Where-Object { 
                $props = Get-ItemProperty -Path $openWithPath -ErrorAction SilentlyContinue
                $props.PSObject.Properties.Name -contains $_
            }) -join ''
            if ($newMruList -ne $mruList) {
                Set-ItemProperty -Path $openWithPath -Name "MRUList" -Value $newMruList
                Write-Host "  ✓ MRUList 已更新" -ForegroundColor Green
            }
        }
    }
    Write-Host "✓ OpenWithList 已清理" -ForegroundColor Green
    
    # 2. 清理 UserChoice (默认程序选择)
    Write-Host "[2/4] 检查 UserChoice..." -ForegroundColor Yellow
    $userChoicePath = "Registry::HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.md\UserChoice"
    
    if (Test-Path $userChoicePath) {
        $progId = (Get-ItemProperty -Path $userChoicePath -Name "ProgId" -ErrorAction SilentlyContinue).ProgId
        if ($progId -like "*PyMDEditor*") {
            Write-Host "  移除 UserChoice: $progId" -ForegroundColor Gray
            Remove-Item -Path $userChoicePath -Recurse -Force -ErrorAction SilentlyContinue
            $cleaned++
            Write-Host "  ✓ UserChoice 已移除" -ForegroundColor Green
        } else {
            Write-Host "  UserChoice: $progId (保留)" -ForegroundColor Gray
        }
    }
    
    # 3. 清理 OpenWithProgids
    Write-Host "[3/4] 检查 OpenWithProgids..." -ForegroundColor Yellow
    $progidsPath = "Registry::HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.md\OpenWithProgids"
    
    if (Test-Path $progidsPath) {
        $properties = Get-Item $progidsPath | Select-Object -ExpandProperty Property
        foreach ($prop in $properties) {
            if ($prop -like "*PyMDEditor*") {
                Write-Host "  移除: $prop" -ForegroundColor Gray
                Remove-ItemProperty -Path $progidsPath -Name $prop -ErrorAction SilentlyContinue
                $cleaned++
            }
        }
    }
    Write-Host "✓ OpenWithProgids 已检查" -ForegroundColor Green
    
    # 4. 清理 HKEY_CLASSES_ROOT 中的旧条目
    Write-Host "[4/4] 检查系统级注册表..." -ForegroundColor Yellow
    
    # 检查是否有多个 PyMDEditor 相关的类型
    $pymdItems = Get-ChildItem -Path "Registry::HKEY_CLASSES_ROOT" -ErrorAction SilentlyContinue | 
                 Where-Object { $_.PSChildName -like "*PyMD*" -and $_.PSChildName -ne "PyMDEditor.Document" }
    
    if ($pymdItems) {
        foreach ($item in $pymdItems) {
            Write-Host "  移除旧项: $($item.PSChildName)" -ForegroundColor Gray
            Remove-Item -Path $item.PSPath -Recurse -Force -ErrorAction SilentlyContinue
            $cleaned++
        }
    }
    Write-Host "✓ 系统级注册表已检查" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "刷新 Windows 资源管理器..." -ForegroundColor Yellow
    Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
    Start-Process explorer.exe
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  清理完成！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "已清理 $cleaned 个残留项" -ForegroundColor White
    Write-Host ""
    Write-Host "当前保留的注册:" -ForegroundColor Cyan
    Write-Host "  - PyMDEditor.Document (系统级文件类型)" -ForegroundColor White
    Write-Host "  - 右键菜单 '用 PyMD Editor 打开'" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "[错误] 清理失败!" -ForegroundColor Red
    Write-Host "错误信息: $_" -ForegroundColor Red
}

Write-Host ""
Read-Host "按回车键退出"
