$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir
Set-Location $Root

$ReleaseRoot = Join-Path $Root "release"
$PackageRoot = Join-Path $ReleaseRoot "HBCPC2026"
$ZipPath = Join-Path $ReleaseRoot "HBCPC2026-release.zip"

if (Test-Path $ReleaseRoot) {
    Remove-Item -Recurse -Force $ReleaseRoot
}
New-Item -ItemType Directory -Force $PackageRoot | Out-Null

$IncludePaths = @(
    "problems",
    "data",
    "checker",
    "solutions",
    "scripts",
    "web",
    "subagents",
    "README.md",
    "DATA_RELIABILITY_REPORT.md",
    "SOLUTION_REPORT.md",
    "subagent_report.md",
    "problem_list.md",
    "manifest.json",
    "requirements.txt",
    "run.sh",
    "build_exe.ps1",
    "build_exe.bat",
    "launcher.py"
)

foreach ($item in $IncludePaths) {
    $src = Join-Path $Root $item
    if (-not (Test-Path $src)) {
        Write-Warning "Skipping missing item: $item"
        continue
    }
    Copy-Item -Recurse -Force $src -Destination $PackageRoot
}

Get-ChildItem -Path $Root -Filter "OJ*.md" -File | ForEach-Object {
    Copy-Item -Force $_.FullName -Destination $PackageRoot
}

$ExePath = Join-Path $Root "HBCPC-OJ.exe"
if (Test-Path $ExePath) {
    Copy-Item -Force $ExePath -Destination $PackageRoot
} else {
    Write-Warning "Root EXE not found: HBCPC-OJ.exe"
}

$IgnoreCandidates = @(
    "build",
    "dist",
    "web_runtime",
    "web\submissions",
    "web\build",
    "__pycache__"
)
foreach ($rel in $IgnoreCandidates) {
    $path = Join-Path $PackageRoot $rel
    if (Test-Path $path) {
        Remove-Item -Recurse -Force $path
    }
}

Get-ChildItem -Path $PackageRoot -Recurse -Force -Directory -Filter ".cph" | ForEach-Object {
    Remove-Item -LiteralPath $_.FullName -Recurse -Force
}

if (Test-Path $ZipPath) {
    Remove-Item -Force $ZipPath
}
Compress-Archive -Path (Join-Path $PackageRoot '*') -DestinationPath $ZipPath -Force

Write-Host "Release package created:"
Write-Host "  $ZipPath"
Write-Host "Package folder:"
Write-Host "  $PackageRoot"
