param([string]$Python = 'python')
Push-Location (Split-Path $PSScriptRoot -Parent)
try { & $Python scripts/reproduce.py --suite core; $checkExit = $LASTEXITCODE }
finally { Pop-Location }
exit $checkExit
