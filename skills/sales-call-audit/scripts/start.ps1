$ErrorActionPreference = 'Stop'
$taskCache = $env:SALES_COACH_CACHE
if (-not $taskCache) { $taskCache = Join-Path $env:LOCALAPPDATA 'sales-call-audit-local' }
$taskTools = Join-Path $taskCache 'tools'
New-Item -ItemType Directory -Force -Path $taskTools | Out-Null
$taskCommand = Get-Command uv -ErrorAction SilentlyContinue
$taskUv = Join-Path $taskTools 'uv.exe'
if ($taskCommand) { $taskUv = $taskCommand.Source }
elseif (-not (Test-Path $taskUv)) {
    if ($args -contains '--offline') { throw 'Offline setup unavailable: run online once first.' }
    Write-Host 'Preparing local tools. No account or API key needed.'
    $installer = Join-Path $taskTools 'uv-installer.ps1'
    Invoke-WebRequest 'https://astral.sh/uv/0.11.8/install.ps1' -OutFile $installer
    $env:UV_UNMANAGED_INSTALL = $taskTools
    & $installer
    if (-not (Test-Path $taskUv)) { throw 'Local runtime installation did not complete.' }
}
$env:PATH = "$(Split-Path $taskUv);$env:PATH"
$env:UV_PYTHON_INSTALL_DIR = Join-Path $taskCache 'python'
if ($args.Count -gt 0 -and $args[0] -eq '--install') {
    $forward = @($args | Select-Object -Skip 1)
    & $taskUv run --no-project --python 3.11 (Join-Path $PSScriptRoot 'install_skill.py') @forward
} else {
    $offline = @()
    if ($args -contains '--offline') { $offline = @('--offline') }
    & $taskUv @offline run --no-project --python 3.11 (Join-Path $PSScriptRoot 'run_local_audio.py') @args --cache $taskCache
}
exit $LASTEXITCODE
