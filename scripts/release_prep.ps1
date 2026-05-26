$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir
Set-Location $Root

Write-Host "Preparing release package contents..."

if (-not (Test-Path "HBCPC-OJ.exe")) {
    Write-Warning "HBCPC-OJ.exe not found. Run build_exe.ps1 first if you want the EXE included."
}

Write-Host "Tracked source tree:"
git ls-files
