# Instala DAV en Mod de FreeCAD (sistema o usuario) sin abrir FreeCAD.
# Uso: .\install_dav_mod.ps1
#      .\install_dav_mod.ps1 -FreeCADExe "L:\Programas\Freecad\bin\FreeCAD.exe"

param([string]$FreeCADExe = "")

$ErrorActionPreference = "Stop"
& (Join-Path $PSScriptRoot "run_freecad_dav.ps1") -FreeCADExe $FreeCADExe -InstallOnly
