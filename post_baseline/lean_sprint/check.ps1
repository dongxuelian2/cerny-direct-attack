param([string]$LeanExe = 'lean')
$ErrorActionPreference = 'Stop'
$env:LEAN_PATH = $PSScriptRoot
$sources = @('ResearchCore', 'AnchorPotentials', 'ThreeAnchorGraph', 'Cerny3Checked', 'Cerny4Checked')
$lines = @(& $LeanExe --version)
if ($LASTEXITCODE -ne 0) { throw 'Lean version check failed' }
foreach ($source in $sources) {
    $path = Join-Path $PSScriptRoot "$source.lean"
    $output = @(& $LeanExe -o (Join-Path $PSScriptRoot "$source.olean") $path 2>&1)
    $exitCode = $LASTEXITCODE
    $lines += "FILE $source.lean EXIT $exitCode"
    $lines += $output
    if ($exitCode -ne 0) { $lines | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot 'CHECK_LOG.txt'); throw "Failed: $source" }
    if ($output -match 'sorryAx') { throw "Untrusted proof hole: $source" }
}
$lines | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot 'CHECK_LOG.txt')
$lines
