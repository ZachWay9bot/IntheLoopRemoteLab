@echo off
setlocal
cd /d "%~dp0"
echo Running existing and new RemoteLab host tests...
py -m unittest discover -s tests -v
if errorlevel 1 (
 echo Unit tests failed. Nothing was flashed.
 pause
 exit /b 1
)
echo.
echo Running three offline firmware fixture adapters...
py -m tools.offline_three_firmware_smoke
set CODE=%ERRORLEVEL%
echo.
if not "%CODE%"=="0" echo Offline smoke failed. No hardware accessed.
pause
exit /b %CODE%
