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

# Genera el instalador DAV para Windows usando IExpress.
# Empaqueta el repo (sin FREECAD, modelos ni entornos) en payload.zip y lo
# vuelca dentro de un .exe auto-extraíble con los bootstrap de instalación.
#
# Uso:
#   .\build_iexpress_installer.ps1
#   .\build_iexpress_installer.ps1 -Version "1.1"
#
# Requiere IExpress (viene con Windows). El .exe queda en build\iexpress\.

param(
    [string]$Version = "1.0"
)

$ErrorActionPreference = "Stop"

function Resolve-DavRepoRoot {
    # Sube hacia la raíz REAL del repo (FREECAD\ o Dav\dic\base.py).
    $current = Split-Path -Parent $PSScriptRoot   # scripts
    for ($i = 0; $i -lt 6; $i++) {
        $hasFreecad = Test-Path -LiteralPath (Join-Path $current "FREECAD")
        $hasRealDic = Test-Path -LiteralPath (Join-Path $current "Dav\dic\base.py")
        if ($hasFreecad -or $hasRealDic) { return $current }
        $parent = Split-Path -Parent $current
        if ($parent -eq $current) { break }
        $current = $parent
    }
    throw "No se encontro la raiz del repo DAV desde $PSScriptRoot"
}

function New-InstallerPackageDir {
    param([string]$RepoRoot, [string]$Version)

    $base = Join-Path $RepoRoot "build\iexpress"
    $pkg = Join-Path $base "pkg"
    $payload = Join-Path $pkg "payload"

    if (Test-Path -LiteralPath $pkg) { Remove-Item -Recurse -Force $pkg }
    New-Item -ItemType Directory -Force -Path $payload | Out-Null

    $exeName = "DAV_Installer_$Version.exe"
    $baseOut = @{ Base = $base; Pkg = $pkg; Payload = $payload; Exe = (Join-Path $base $exeName) }
    return $baseOut
}

function Copy-RelevantSource {
    param([string]$RepoRoot, [string]$Payload)

    # Copia el repo sin los directorios pesados ni entornos virtuales.
    & robocopy $RepoRoot $Payload /E `
        /XD .git FREECAD models .venv __pycache__ build Build BUILD dist out `
        /XF *.pyc *.pyo *.log *.FCBak *.lock `
        /R:1 /W:1 /NFL /NDL /NJH /NJS /NP | Out-Null
    if ($LASTEXITCODE -ge 8) {
        throw "robocopy no pudo copiar el repo (exit $LASTEXITCODE)"
    }
}

function Compress-PayloadZip {
    param([string]$Payload, [string]$Pkg)

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $zip = Join-Path $Pkg "payload.zip"
    if (Test-Path -LiteralPath $zip) { Remove-Item -Force $zip }
    [System.IO.Compression.ZipFile]::CreateFromDirectory($Payload, $zip)
    return $zip
}

function Write-IExpressSed {
    param([string]$Pkg, [string]$Exe, [string]$Version)

    $sed = Join-Path $Pkg "dav_installer.sed"
    $sedText = @"
[Version]
Class=IEXPRESS
SEDVersion=3

[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=2
HideExtractAnimation=1
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=%InstallPrompt%
DisplayLicense=%DisplayLicense%
FinishMessage=%FinishMessage%
TargetName=%TargetName%
FriendlyName=%FriendlyName%
AppLaunched=%AppLaunched%
PostInstallCmd=%PostInstallCmd%
AdminQuietInstCmd=%AdminQuietInstCmd%
UserQuietInstCmd=%UserQuietInstCmd%
SourceFiles=SourceFiles

[Strings]
InstallPrompt=
DisplayLicense=
FinishMessage=
TargetName=$Exe
FriendlyName=DAV $Version - Instalador Windows
AppLaunched=cmd.exe /c bootstrap.cmd
PostInstallCmd=<None>
AdminQuietInstCmd=
UserQuietInstCmd=
FILE0="bootstrap.cmd"
FILE1="bootstrap.ps1"
FILE2="payload.zip"

[SourceFiles]
SourceFiles0=$Pkg\

[SourceFiles0]
%FILE0%=
%FILE1%=
%FILE2%=
"@
    Set-Content -LiteralPath $sed -Value $sedText -Encoding ASCII
    return $sed
}

function Invoke-IExpressBuild {
    param([string]$SedName, [string]$Pkg)

    # IExpress es app GUI: hay que esperarlo via cmd (bloqueante) para
    # capturar el exit code. CWD = carpeta del paquete.
    Push-Location $Pkg
    try {
        cmd /c "iexpress /N /Q $SedName"
        if ($LASTEXITCODE -ne 0) {
            throw "IExpress fallo al crear el instalador (exit $LASTEXITCODE)."
        }
    } finally {
        Pop-Location
    }
}

Write-Host "=== Generador de instalador DAV (IExpress) ===" -ForegroundColor Cyan
$repo = Resolve-DavRepoRoot
$out = New-InstallerPackageDir -RepoRoot $repo -Version $Version
Write-Host "Repo:  $repo"
Write-Host "Salida: $($out.Exe)"

Write-Host "Copiando fuentes del repo al payload..."
Copy-RelevantSource -RepoRoot $repo -Payload $out.Payload

Write-Host "Comprimiendo payload.zip..."
$zip = Compress-PayloadZip -Payload $out.Payload -Pkg $out.Pkg
Write-Host "payload.zip: $((Get-Item $zip).Length) bytes"

# Bootstrap planos (los necesita el exe en el temp de extraccion).
Copy-Item (Join-Path $PSScriptRoot "iexpress\bootstrap.cmd") $out.Pkg -Force
Copy-Item (Join-Path $PSScriptRoot "iexpress\bootstrap.ps1") $out.Pkg -Force

Write-Host "Generando SED y compilando el instalador..."
$sed = Write-IExpressSed -Pkg $out.Pkg -Exe $out.Exe -Version $Version
Invoke-IExpressBuild -SedName (Split-Path -Leaf $sed) -Pkg $out.Pkg

if (-not (Test-Path -LiteralPath $out.Exe)) {
    throw "No se genero el .exe: $($out.Exe)"
}
$size = "{0:N1} MB" -f ((Get-Item $out.Exe).Length / 1MB)
Write-Host "" 
Write-Host "Instalador generado: $($out.Exe) ($size)" -ForegroundColor Green
Write-Host "SED usado: $sed"