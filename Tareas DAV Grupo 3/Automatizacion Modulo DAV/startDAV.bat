@echo off
set PYTHONIOENCODING=utf-8

echo =======================================
echo Instalando dependencias del modulo DAV
echo =======================================
"%~dp0FreeCADCmd.exe" -c "import FreeCAD; FreeCAD.loadModule('DAV'); print('Instalacion completada.'); import sys; sys.exit(0)"

#echo.
#echo =======================================
#echo Abriendo FreeCAD con DAV...
echo =======================================
start "" "%~dp0FreeCAD.exe" --module=DAV %*