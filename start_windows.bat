@echo off
cd /d "%~dp0"
if defined ORION_PYTHON (
  set "PY=%ORION_PYTHON%"
  goto run
)
python --version >nul 2>nul
if not errorlevel 1 (
  set "PY=python"
  goto run
)
py --version >nul 2>nul
if errorlevel 1 goto failure
set "PY=py"
:run
"%PY%" --version
if errorlevel 1 goto failure
"%PY%" run.py demo
if errorlevel 1 goto failure
"%PY%" run.py compare --n 8
if errorlevel 1 goto failure
"%PY%" -m unittest discover -s tests -v
if errorlevel 1 goto failure
echo SUCCESS. Open results and START_HERE.md.
if /I not "%~1"=="--no-pause" pause
exit /b 0
:failure
echo FAILED. Copy the complete error into your research log. Read START_HERE.md.
if /I not "%~1"=="--no-pause" pause
exit /b 1
