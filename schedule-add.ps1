$taskName   = "kk-TorontoAddressLayer"
$projectDir = $PSScriptRoot
$logFile    = "$projectDir\logs\scheduler.log"

if (-not (Test-Path "$projectDir\logs")) {
    New-Item -ItemType Directory -Path "$projectDir\logs" | Out-Null
}

$action = New-ScheduledTaskAction `
    -Execute "cmd.exe" `
    -Argument "/c cd /d `"$projectDir`" && (python -m addressvault.cli pull toronto --wait && python run.py update) >> `"$logFile`" 2>&1"

# The address-layerist engine never downloads; it reads the newest toronto-*.geojson
# from the vault. So pull first (--wait coalesces onto any in-flight pull), then
# build. 14:00 keeps it after the noon data refresh, so it usually reuses that day's
# snapshot rather than pulling the ~590 MB file cold.
$trigger  = New-ScheduledTaskTrigger -Daily -At "14:00"
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Hours 2) -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force

Write-Host "Scheduled '$taskName' to run daily at 14:00."
Write-Host "Log: $logFile"
