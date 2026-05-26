@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0iniciar_dav.ps1" %*
set "EC=%ERRORLEVEL%"
if %EC% NEQ 0 pause
exit /b %EC%
