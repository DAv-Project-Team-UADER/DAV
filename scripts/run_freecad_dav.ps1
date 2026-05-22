# Arranca FreeCAD del repo DAV-Luigi con módulo DAV + preferencias GUIFreeCad.
# Uso: .\scripts\run_freecad_dav.ps1
#      .\scripts\run_freecad_dav.ps1 -BuildDir "C:\ruta\al\build"

param(
    [string]$BuildDir = "",
    [string]$FreeCADExe = "",
    [switch]$InstallOnly
)

$ErrorActionPreference = "Stop"
$DavLuigi = Split-Path -Parent $PSScriptRoot
# GUIFreeCad vive en Repositorio DAVFreeCad/ (no dentro de DAVFreecad-Pruebas/)
$RepoRoot = Split-Path -Parent (Split-Path -Parent $DavLuigi)
$GuiRoot = Join-Path $RepoRoot "GUIFreeCad"
$DavMod = Join-Path $DavLuigi "Dav"
$FreecadRoot = Join-Path $DavLuigi "FREECAD"

if (-not (Test-Path $GuiRoot)) {
    Write-Error "No se encontró GUIFreeCad en: $GuiRoot"
}
if (-not (Test-Path (Join-Path $DavMod "InitGui.py"))) {
    Write-Error "No se encontró el módulo Dav en: $DavMod"
}

$env:DAV_GUI_FREECAD_ROOT = $GuiRoot
$env:DAV_MOD_ROOT = $DavMod
# Preferencias solo con el boton/engranaje; workbench DAV si al arranque
$env:DAV_OPEN_PREFS_ON_START = "0"
$env:DAV_AUTOLOAD_WORKBENCH = "1"

function Install-DavModLink {
    param(
        [string]$ModRoot,
        [string]$SourceDir
    )
    if (-not $ModRoot) { return $false }
    New-Item -ItemType Directory -Force -Path $ModRoot | Out-Null
    $dest = Join-Path $ModRoot "DAV"
    if (Test-Path $dest) {
        Remove-Item $dest -Force -Recurse -ErrorAction SilentlyContinue
    }
    New-Item -ItemType Junction -Path $dest -Target $SourceDir | Out-Null
    return (Test-Path (Join-Path $dest "InitGui.py"))
}

function Find-FreeCADExe {
    param([string[]]$Candidates)
    foreach ($p in $Candidates) {
        if ($p -and (Test-Path -LiteralPath $p)) {
            return (Resolve-Path -LiteralPath $p).Path
        }
    }
    return $null
}

function Get-FreeCADFromRegistry {
    $keys = @(
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\FreeCAD.exe",
        "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\FreeCAD.exe"
    )
    foreach ($key in $keys) {
        try {
            $value = (Get-ItemProperty -LiteralPath $key -ErrorAction Stop)."(default)"
            if ($value -and (Test-Path -LiteralPath $value)) {
                return (Resolve-Path -LiteralPath $value).Path
            }
        } catch {
            continue
        }
    }
    return $null
}

function Search-FreeCADOnDisk {
    $roots = @(
        ${env:ProgramFiles},
        ${env:ProgramFiles(x86)},
        (Join-Path $env:LOCALAPPDATA "Programs"),
        "C:\FreeCAD",
        $FreecadRoot
    ) | Where-Object { $_ -and (Test-Path $_) }

    foreach ($root in $roots) {
        try {
            $hit = Get-ChildItem -LiteralPath $root -Filter "FreeCAD.exe" -Recurse -ErrorAction SilentlyContinue -Depth 6 |
                Select-Object -First 1 -ExpandProperty FullName
            if ($hit) { return $hit }
        } catch {
            continue
        }
    }
    return $null
}

$buildCandidates = @()
if ($BuildDir) {
    $buildCandidates += @(
        (Join-Path $BuildDir "bin\FreeCAD.exe"),
        (Join-Path $BuildDir "Release\bin\FreeCAD.exe"),
        (Join-Path $BuildDir "bin\FreeCAD.exe")
    )
}
$buildCandidates += @(
    (Join-Path $FreecadRoot "build\bin\FreeCAD.exe"),
    (Join-Path $FreecadRoot "build\Release\bin\FreeCAD.exe"),
    (Join-Path $FreecadRoot "build\windows\bin\FreeCAD.exe"),
    (Join-Path $FreecadRoot "build\Windows\bin\FreeCAD.exe")
)

if ($FreeCADExe) {
    $fcExe = Find-FreeCADExe @($FreeCADExe)
} elseif ($env:DAV_FREECAD_EXE) {
    $fcExe = Find-FreeCADExe @($env:DAV_FREECAD_EXE)
} else {
    $fcExe = $null
}

if (-not $fcExe) {
    $fcExe = Get-FreeCADFromRegistry
}
if (-not $fcExe) {
    $fcExe = Find-FreeCADExe $buildCandidates
}
if (-not $fcExe) {
    $fcExe = Find-FreeCADExe @(
        "${env:ProgramFiles}\FreeCAD 1.2\bin\FreeCAD.exe",
        "${env:ProgramFiles}\FreeCAD 1.0\bin\FreeCAD.exe",
        "${env:ProgramFiles}\FreeCAD 0.21\bin\FreeCAD.exe",
        "${env:ProgramFiles}\FreeCAD\bin\FreeCAD.exe",
        "${env:ProgramFiles(x86)}\FreeCAD 1.0\bin\FreeCAD.exe"
    )
}
if (-not $fcExe) {
    $fcExe = Search-FreeCADOnDisk
}

if (-not $fcExe) {
    Write-Host ""
    Write-Host "No se encontro FreeCAD.exe en este equipo." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opciones:" -ForegroundColor Cyan
    Write-Host "  1) Instalar FreeCAD: https://www.freecad.org/downloads.php"
    Write-Host "  2) Compilar DAV-Luigi\FREECAD y usar:"
    Write-Host '       .\run_freecad_dav.ps1 -BuildDir "C:\ruta\al\build"'
    Write-Host "  3) Si ya esta instalado en otra ruta:"
    Write-Host '       .\run_freecad_dav.ps1 -FreeCADExe "C:\ruta\bin\FreeCAD.exe"'
    Write-Host ""
    Write-Host "Mientras tanto, proba solo la GUI de preferencias:" -ForegroundColor Cyan
    Write-Host "  cd ..\..\..\GUIFreeCad"
    Write-Host "  .\.venv\Scripts\activate"
    Write-Host "  python main.py"
    exit 1
}

$fcDir = Split-Path -Parent $fcExe
$fcPython = Join-Path $fcDir "python.exe"
$env:DAV_FREECAD_PYTHON = $fcPython
$fcHome = (Resolve-Path (Join-Path $fcDir "..")).Path
$systemModRoot = Join-Path $fcHome "Mod"
$installedPath = ""

# 1) Mod del sistema (como Part, PartDesign…) — lo que recomienda FreeCAD
try {
    if (Install-DavModLink -ModRoot $systemModRoot -SourceDir $DavMod) {
        $installedPath = Join-Path $systemModRoot "DAV"
        Write-Host "DAV instalado en Mod del sistema: $installedPath" -ForegroundColor Green
    }
} catch {
    Write-Host "No se pudo escribir en Mod del sistema (¿ejecutar PowerShell como admin?): $($_.Exception.Message)" -ForegroundColor Yellow
}

# 2) Respaldo: Mod del usuario solo si fallo el del sistema (evitar cargar DAV dos veces)
if (-not $installedPath) {
    $userModRoot = Join-Path $env:APPDATA "FreeCAD\v1-1\Mod"
    try {
        if (Install-DavModLink -ModRoot $userModRoot -SourceDir $DavMod) {
            $installedPath = Join-Path $userModRoot "DAV"
            Write-Host "DAV instalado en Mod de usuario: $installedPath" -ForegroundColor Green
        }
    } catch {
        Write-Host "Tampoco se pudo instalar en Mod de usuario: $($_.Exception.Message)" -ForegroundColor Yellow
    }
} else {
    # Si uso Mod del sistema, quitar enlace duplicado en AppData
    $userDav = Join-Path $env:APPDATA "FreeCAD\v1-1\Mod\DAV"
    if (Test-Path $userDav) {
        Remove-Item $userDav -Force -Recurse -ErrorAction SilentlyContinue
        Write-Host "Enlace duplicado eliminado: $userDav" -ForegroundColor DarkGray
    }
}

if (-not $installedPath) {
    Write-Error "No se pudo instalar el enlace DAV en Mod de FreeCAD."
}

$env:DAV_MOD_ROOT = $installedPath

Write-Host "FreeCAD: $fcExe"
Write-Host "GUIFreeCad: $GuiRoot"
Write-Host "Preferencias: $(Join-Path $GuiRoot 'config\settings.json')"
Write-Host ""

$fcArgs = @()

$depsScript = Join-Path $PSScriptRoot "check_freecad_deps.ps1"
if (Test-Path $depsScript) {
    & $depsScript -FreeCADExe $fcExe
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Instalando dependencias de voz en Python de FreeCAD..." -ForegroundColor Yellow
        & $depsScript -FreeCADExe $fcExe -Install
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "No se pudieron instalar sounddevice/vosk. El microfono fallara en Preferencias."
        }
    }
}

if ($InstallOnly) {
    Write-Host "Instalacion lista. Abri FreeCAD o ejecuta sin -InstallOnly." -ForegroundColor Green
    exit 0
}

& $fcExe @fcArgs
exit $LASTEXITCODE
