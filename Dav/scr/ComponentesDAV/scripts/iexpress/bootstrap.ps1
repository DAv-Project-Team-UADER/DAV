# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

# Bootstrap del instalador DAV empaquetado con IExpress.
# Descomprime payload.zip en %USERPROFILE%\DAV y arranca iniciar_dav.bat,
# que se encarga del entorno, dependencias, modelos Vosk y FreeCAD.

$ErrorActionPreference = "Continue"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$zip = Join-Path $root "payload.zip"
$dest = Join-Path $env:USERPROFILE "DAV"

Write-Host ""
Write-Host "=== Instalacion de DAV (Diseno Asistido por Voz) ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Destino: $dest"
Write-Host ""

if (-not (Test-Path -LiteralPath $zip)) {
    Write-Host "ERROR: no se encontro payload.zip al lado del instalador." -ForegroundColor Red
    exit 1
}

Write-Host "Descomprimiendo archivos de DAV..."
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Expand-Archive -LiteralPath $zip -DestinationPath $dest -Force

Write-Host "Archivos DAV listos en: $dest" -ForegroundColor Green
Write-Host ""
Write-Host "Arrancando DAV. La primera vez puede tardar: crea el entorno"
Write-Host "virtual, instala dependencias y descarga el modelo de voz." 
Write-Host ""

& (Join-Path $dest "iniciar_dav.bat")
exit $LASTEXITCODE