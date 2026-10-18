@echo off
setlocal
cd /d "%~dp0"
py -m remotelab run --config remotelab.json
