@echo off
set PYTHONIOENCODING=utf-8

echo =======================================
echo Instalando dependencias del modulo DAV
echo =======================================

:: Ruta completa al Init.py (usamos %~dp0 para que sea portable)
set DAV_INIT=%~dp0Mod\DAV\Init.py

:: Ejecutamos FreeCADCmd usando exec() tal como funcionó en la consola
"%~dp0FreeCADCmd.exe" -c "exec(open(r'%DAV_INIT%').read()); import sys; sys.exit(0)"

echo.
echo =======================================
echo Abriendo FreeCAD con DAV...
echo =======================================
start "" "%~dp0FreeCAD.exe" --module=DAV %*