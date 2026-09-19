@echo off
setlocal
cd /d "%~dp0"
"%WINDIR%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File "%~dp0iniciar_dav.ps1" %*
set "EC=%ERRORLEVEL%"
if %EC% NEQ 0 pause
exit /b %EC%
