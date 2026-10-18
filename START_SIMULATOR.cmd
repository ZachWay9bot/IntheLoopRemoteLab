@echo off
setlocal
cd /d "%~dp0"
py -m remotelab
echo.
py -m unittest discover -s tests -v
pause
