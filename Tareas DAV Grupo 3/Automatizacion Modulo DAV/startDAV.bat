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

:: ======================================================
:: Crear acceso directo en la carpeta de Inicio (sin errores de codificación)
:: ======================================================
echo Configurando inicio automático...
powershell -Command ^
  "$startupDir = [Environment]::GetFolderPath('Startup');" ^
  "$shortcutPath = Join-Path $startupDir 'startDAV.lnk';" ^
  "if (-not (Test-Path $shortcutPath)) {" ^
  "  $ws = New-Object -ComObject WScript.Shell;" ^
  "  $s = $ws.CreateShortcut($shortcutPath);" ^
  "  $s.TargetPath = '%~f0';" ^
  "  $s.WorkingDirectory = '%~dp0';" ^
  "  $s.WindowStyle = 7;" ^
  "  $s.Save();" ^
  "  Write-Host 'Acceso directo creado en:' $shortcutPath" ^
  "} else {" ^
  "  Write-Host 'El acceso directo ya existe.'" ^
  "}"


echo =======================================
echo Abriendo FreeCAD con DAV...
echo =======================================
start "" "%~dp0FreeCAD.exe" --module=DAV %*