$ErrorActionPreference = 'SilentlyContinue'

# Never kill these: the shell, GlazeWM/Zebar themselves, and core system processes.
$blocked = @(
    'explorer', 'glazewm', 'zebar',
    'csrss', 'dwm', 'lsass', 'services', 'smss', 'wininit', 'winlogon', 'system'
)

$cli = (Get-Command glazewm -ErrorAction SilentlyContinue).Source
if (-not $cli) { $cli = 'C:\Program Files\glzr.io\GlazeWM\cli\glazewm.exe' }
if (-not (Test-Path $cli)) { exit 1 }

$query = (& $cli query focused) | ConvertFrom-Json
$focused = $query.data.focused
if (-not $query.success -or $focused.type -ne 'window') { exit 0 }

$handle = [int64]$focused.handle
$target = Get-Process | Where-Object { [int64]$_.MainWindowHandle -eq $handle } | Select-Object -First 1
if (-not $target) { exit 0 }

if ($blocked -contains $target.ProcessName.ToLowerInvariant()) { exit 0 }

Stop-Process -Id $target.Id -Force -ErrorAction SilentlyContinue
