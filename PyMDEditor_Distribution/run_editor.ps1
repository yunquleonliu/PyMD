# PyMD Editor 启动脚本 (PowerShell)
# 支持：双击启动 或 拖拽 .md 文件

param(
    [string]$FilePath
)

# 设置工作目录为脚本所在目录
Set-Location -LiteralPath $PSScriptRoot

# 检查是否有虚拟环境，优先使用虚拟环境
if (Test-Path ".venv\Scripts\python.exe") {
    $pythonCmd = ".venv\Scripts\python.exe"
} else {
    $pythonCmd = "python"
}

# 启动编辑器
if ($FilePath) {
    & $pythonCmd -m src.pymd_editor.main $FilePath
} else {
    & $pythonCmd -m src.pymd_editor.main
}
