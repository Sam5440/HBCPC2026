$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host "== HBCPC OJ EXE build =="
Write-Host "Root: $Root"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "python was not found in PATH."
}

if (-not (Get-Command g++ -ErrorAction SilentlyContinue)) {
    Write-Warning "g++ was not found in PATH. The EXE can still be built, but judging C++ submissions requires g++ at runtime."
}

python -m pip install -r requirements.txt

$MathJaxMain = Join-Path $Root "web\static\mathjax\es5\tex-chtml.js"
if (-not (Test-Path $MathJaxMain)) {
    if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
        throw "MathJax assets are missing and npm was not found in PATH. Install npm or restore web\static\mathjax."
    }
    Write-Host "MathJax assets missing; downloading mathjax@3 with npm..."
    $NpmDir = Join-Path $Root "build\npm_mathjax"
    if (Test-Path $NpmDir) {
        Remove-Item -Recurse -Force $NpmDir
    }
    npm install mathjax@3 --prefix $NpmDir
    $StaticMathJax = Join-Path $Root "web\static\mathjax"
    New-Item -ItemType Directory -Force $StaticMathJax | Out-Null
    Copy-Item -Recurse -Force (Join-Path $NpmDir "node_modules\mathjax\es5") (Join-Path $StaticMathJax "es5")
}

$OldExe = Join-Path $Root "HBCPC-OJ.exe"
$RunningExe = Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.Path -eq $OldExe }
if ($RunningExe) {
    Write-Host "Stopping running HBCPC-OJ.exe before rebuild..."
    $RunningExe | Stop-Process -Force
    Start-Sleep -Seconds 2
}
if (Test-Path $OldExe) {
    Remove-Item -Force $OldExe
}

$Spec = Join-Path $Root "HBCPC-OJ.spec"
if (Test-Path $Spec) {
    Remove-Item -Force $Spec
}

python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --name HBCPC-OJ `
    --collect-submodules markdown `
    --add-data "manifest.json;." `
    --add-data "problems;problems" `
    --add-data "data;data" `
    --add-data "checker;checker" `
    --add-data "web/templates;web/templates" `
    --add-data "web/static;web/static" `
    launcher.py

$BuiltExe = Join-Path $Root "dist\HBCPC-OJ.exe"
if (-not (Test-Path $BuiltExe)) {
    throw "PyInstaller finished but dist\HBCPC-OJ.exe was not found."
}

Copy-Item -Force $BuiltExe $OldExe

Write-Host ""
Write-Host "Build complete:"
Write-Host "  $OldExe"
Write-Host ""
Write-Host "Run it by double-clicking HBCPC-OJ.exe. It starts a local server and opens the browser automatically."
