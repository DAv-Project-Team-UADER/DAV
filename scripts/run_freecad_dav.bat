@echo off
REM Arranca FreeCAD con DAV + GUIFreeCad (doble clic o desde cmd).
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_freecad_dav.ps1" %*
exit /b %ERRORLEVEL%
