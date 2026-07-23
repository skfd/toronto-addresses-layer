$taskName   = "kk-TorontoAddressLayer"
$projectDir = $PSScriptRoot
$logFile    = "$projectDir\logs\scheduler.log"

if (-not (Test-Path "$projectDir\logs")) {
    New-Item -ItemType Directory -Path "$projectDir\logs" | Out-Null
}

# A git process killed mid-write (a torn-down container with Code/ mounted is the
# usual culprit) leaves a zero-byte *.lock behind, and publish then fails every day
# until someone clears it by hand -- that cost six days of updates in July 2026.
# Sweep first, best-effort: joined with & so a hiccup here can never block the build.
$lockCheck = Join-Path (Split-Path $projectDir -Parent) "check-git-locks.ps1"
if (-not (Test-Path $lockCheck)) { Write-Warning "Lock sweeper not found: $lockCheck" }

$action = New-ScheduledTaskAction `
    -Execute "cmd.exe" `
    -Argument "/c cd /d `"$projectDir`" && (powershell -NoProfile -ExecutionPolicy Bypass -File `"$lockCheck`" -Clear & python -m addressvault.cli pull toronto --wait && python run.py update) >> `"$logFile`" 2>&1"

# The address-layerist engine never downloads; it reads the newest toronto-*.geojson
# from the vault. So pull first (--wait coalesces onto any in-flight pull), then
# build. 14:00 keeps it after the noon data refresh, so it usually reuses that day's
# snapshot rather than pulling the ~590 MB file cold.
$trigger  = New-ScheduledTaskTrigger -Daily -At "14:00"
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Hours 2) -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force

Write-Host "Scheduled '$taskName' to run daily at 14:00."
Write-Host "Log: $logFile"
