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

# Crea "ejecutar.lnk" junto a este script, apuntando a iniciar_dav.bat.
# Las rutas se calculan desde la ubicación del script, así que funciona
# en cualquier clon del repo. Correrlo una vez después de clonar.

$raiz  = $PSScriptRoot
$bat   = Join-Path $raiz 'iniciar_dav.bat'
$icono = Join-Path $raiz 'Dav\scr\ComponentesDAV\Logos\color.ico'
$lnk   = Join-Path $raiz 'ejecutar.lnk'

if (-not (Test-Path $bat)) { throw "No se encontró $bat" }

$ws = New-Object -ComObject WScript.Shell
$acceso = $ws.CreateShortcut($lnk)
$acceso.TargetPath       = $bat
$acceso.WorkingDirectory = $raiz
$acceso.IconLocation     = "$icono,0"
$acceso.Description      = 'Inicia DAV'
$acceso.Save()

Write-Host "Acceso directo creado: $lnk"
