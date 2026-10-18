@echo off
setlocal
cd /d "%~dp0"
py -m remotelab once --config remotelab.json
pause
