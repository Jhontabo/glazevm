$ErrorActionPreference = 'SilentlyContinue'

# Never kill these: the shell, GlazeWM/Zebar themselves, core system processes,
# and shared host processes.
$blocked = @(
    'explorer', 'glazewm', 'zebar',
    'applicationframehost', 'runtimebroker', 'searchhost',
    'startmenuexperiencehost', 'shellexperiencehost', 'textinputhost',
    'sihost', 'taskhostw', 'ctfmon', 'fontdrvhost', 'lockapp', 'dllhost',
    'svchost', 'conhost', 'wmiprvse',
    'csrss', 'dwm', 'lsass', 'services', 'smss', 'wininit', 'winlogon', 'system'
)

$cli = (Get-Command glazewm -ErrorAction SilentlyContinue).Source
if (-not $cli) { $cli = 'C:\Program Files\glzr.io\GlazeWM\cli\glazewm.exe' }
if (-not (Test-Path $cli)) { exit 1 }

try {
    $query = (& $cli query focused) | ConvertFrom-Json
} catch {
    exit 1
}

$focused = $query.data.focused
if (-not $query.success -or -not $focused -or $focused.type -ne 'window') { exit 0 }

if ($focused.processName -and ($blocked -contains $focused.processName.ToLowerInvariant())) {
    exit 0
}

$handle = [int64]$focused.handle
$target = Get-Process | Where-Object { [int64]$_.MainWindowHandle -eq $handle } | Select-Object -First 1
if (-not $target) { exit 0 }

if ($blocked -contains $target.ProcessName.ToLowerInvariant()) { exit 0 }

$taskkill = Join-Path $env:SystemRoot 'System32\taskkill.exe'
if (Test-Path $taskkill) {
    & $taskkill /PID $target.Id /T /F | Out-Null
} else {
    Stop-Process -Id $target.Id -Force -ErrorAction SilentlyContinue
}
