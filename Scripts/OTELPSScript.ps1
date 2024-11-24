$ctlScript = 'C:\Program Files\Amazon\AWSOTelCollector\aws-otel-collector-ctl.ps1'
$status = (& $ctlScript -a status | ConvertFrom-Json).status

if ($status -eq "running") {
    Write-Host "AWSOTelCollector is running."
} else {
    Write-Host "AWSOTelCollector is not running. Starting the collector agent"
    & $ctlScript -a start
}