# 解析项目目录和 Python 解释器。
$projectDir = $PSScriptRoot
$candidates = @(
    (Join-Path $projectDir '.venv\Scripts\pythonw.exe'),
    (Join-Path $env:USERPROFILE 'Documents\ChatGPT\test\yolo-project\.venv\Scripts\pythonw.exe'),
    'D:\python\pythonw.exe',
    (Join-Path $projectDir '.venv\Scripts\python.exe'),
    (Join-Path $env:USERPROFILE 'Documents\ChatGPT\test\yolo-project\.venv\Scripts\python.exe'),
    'D:\python\python.exe'
)

$python = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $python) {
    Add-Type -AssemblyName PresentationFramework
    [System.Windows.MessageBox]::Show('没有找到可用的 Python 环境，无法启动 YOLO 桌面应用。', 'YOLO 实时检测', 'OK', 'Error') | Out-Null
    exit 1
}

$outLog = Join-Path $env:TEMP 'yolo-desktop.out.log'
$errLog = Join-Path $env:TEMP 'yolo-desktop.err.log'
$desktopApp = Join-Path $projectDir 'desktop_app.py'

# 使用 pythonw 启动桌面程序，不显示控制台；日志用于排错。
Start-Process -FilePath $python -ArgumentList @('-X', 'utf8', $desktopApp) -WorkingDirectory $projectDir -RedirectStandardOutput $outLog -RedirectStandardError $errLog