param([string]$Python = 'python', [string]$Lean = 'lean')
Push-Location (Split-Path $PSScriptRoot -Parent)
try { & $Python scripts/reproduce.py --suite formal --lean $Lean; $checkExit = $LASTEXITCODE }
finally { Pop-Location }
exit $checkExit
