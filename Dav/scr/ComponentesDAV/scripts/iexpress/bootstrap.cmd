@echo off
REM Copyright (C) 2026 El Equipo del Proyecto DAV
REM Universidad Autonoma de Entre Rios (UADER)
REM Bajo la direccion de Guillermo Gerard y Gallo Fabricio David
REM
REM Bootstrap .cmd generado para el instalador DAV (IExpress).
REM Ejecuta bootstrap.ps1 que descomprime payload.zip y lanza iniciar_dav.bat.
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0bootstrap.ps1" %*
endlocal
exit /b %ERRORLEVEL%