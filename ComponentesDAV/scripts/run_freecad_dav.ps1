# Arranca FreeCAD del repo DAV con modulo DAV + preferencias GUIFreeCad.
# Uso: .\scripts\run_freecad_dav.ps1
#      .\scripts\run_freecad_dav.ps1 -BuildDir "C:\ruta\al\build"

param(
    [string]$BuildDir = "",
    [string]$FreeCADExe = "",
    [switch]$InstallOnly,
    [switch]$StartVoice,
    [switch]$NoStartVoice
)

$ErrorActionPreference = "Stop"

function Resolve-GuiFreeCadRoot {
    param([string]$RepoRoot)

    $candidates = @(
        (Join-Path $RepoRoot "componentesDAV\IntegracionGUI\GUIFreeCad"),
        (Join-Path $RepoRoot "IntegracionGUI\GUIFreeCad"),
        (Join-Path $RepoRoot "luigiIntegracionV1\GUIFreeCad"),
        (Join-Path $RepoRoot "GUIFreeCad")
    )
    foreach ($path in $candidates) {
        if (Test-Path -LiteralPath $path) { return $path }
    }
    $parent = Split-Path -Parent (Split-Path -Parent $RepoRoot)
    $sibling = Join-Path $parent "GUIFreeCad"
    if (Test-Path -LiteralPath $sibling) { return $sibling }
    return $candidates[0]
}

function Get-DavRepoPaths {
    $repo = Split-Path -Parent $PSScriptRoot
    $gui = Resolve-GuiFreeCadRoot -RepoRoot $repo

    $davCandidates = @(
        (Join-Path $repo "Dav"),
        (Join-Path $repo "componentesDAV\Dav")
    )
    $davMod = $davCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1

    if (-not $davMod) {
        $davMod = Join-Path $repo "Dav"
    }

    return @{
        DavRepo     = $repo
        GuiRoot     = $gui
        DavMod      = $davMod
        FreecadRoot = Join-Path $repo "FREECAD"
    }
}

function Get-DavLaunchConfig {
    param([string]$GuiRoot)

    $path = Join-Path $GuiRoot "config\dav_launch.json"
    if (-not (Test-Path -LiteralPath $path)) { return $null }
    try {
        return Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
    } catch {
        return $null
    }
}

function Save-DavLaunchConfig {
    param(
        [string]$GuiRoot,
        [string]$FcExe
    )

    $configDir = Join-Path $GuiRoot "config"
    New-Item -ItemType Directory -Force -Path $configDir | Out-Null
    $path = Join-Path $configDir "dav_launch.json"
    (@{ freecad_exe = $FcExe } | ConvertTo-Json) | Set-Content -LiteralPath $path -Encoding UTF8
}

function Test-StartupVoiceEnabled {
    param([string]$GuiRoot)

    $path = Join-Path $GuiRoot "config\settings.json"
    if (-not (Test-Path -LiteralPath $path)) { return $false }
    try {
        $settings = Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
        return [bool]$settings.startup_enabled
    } catch {
        return $false
    }
}

function Resolve-VoiceAutostart {
    param(
        [string]$GuiRoot,
        [switch]$StartVoice,
        [switch]$NoStartVoice
    )

    if ($NoStartVoice) { return $false }
    if ($StartVoice) { return $true }
    return (Test-StartupVoiceEnabled -GuiRoot $GuiRoot)
}

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
            $props = Get-ItemProperty -LiteralPath $key -ErrorAction Stop
            $value = $props.'(default)'
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
    param([string]$FreecadRoot)

    $programFiles = $env:ProgramFiles
    $programFilesX86 = (Get-Item -LiteralPath 'Env:ProgramFiles(x86)' -ErrorAction SilentlyContinue).Value

    $roots = @(
        $programFiles,
        $programFilesX86,
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

function Install-DavWorkbench {
    param(
        [string]$DavMod,
        [string]$FcHome
    )

    $systemModRoot = Join-Path $FcHome "Mod"
    $installedPath = ""

    try {
        if (Install-DavModLink -ModRoot $systemModRoot -SourceDir $DavMod) {
            $installedPath = Join-Path $systemModRoot "DAV"
            Write-Host "DAV instalado en Mod del sistema: $installedPath" -ForegroundColor Green
        }
    } catch {
        $err = $_.Exception.Message
        Write-Host "No se pudo escribir en Mod del sistema (ejecutar PowerShell como admin?): $err" -ForegroundColor Yellow
    }

    if (-not $installedPath) {
        $userModRoot = Join-Path $env:APPDATA 'FreeCAD\v1-1\Mod'
        try {
            if (Install-DavModLink -ModRoot $userModRoot -SourceDir $DavMod) {
                $installedPath = Join-Path $userModRoot "DAV"
                Write-Host "DAV instalado en Mod de usuario: $installedPath" -ForegroundColor Green
            }
        } catch {
            $err = $_.Exception.Message
            Write-Host "Tampoco se pudo instalar en Mod de usuario: $err" -ForegroundColor Yellow
        }
    } else {
        $userDav = Join-Path $env:APPDATA 'FreeCAD\v1-1\Mod\DAV'
        if (Test-Path $userDav) {
            Remove-Item $userDav -Force -Recurse -ErrorAction SilentlyContinue
            Write-Host "Enlace duplicado eliminado: $userDav" -ForegroundColor DarkGray
        }
    }

    return $installedPath
}

function Resolve-FreeCADExe {
    param(
        [string]$FreeCADExe,
        [string]$BuildDir,
        [string]$FreecadRoot
    )

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
        $found = Find-FreeCADExe @($FreeCADExe)
        if ($found) { return $found }
    } elseif ($env:DAV_FREECAD_EXE) {
        $found = Find-FreeCADExe @($env:DAV_FREECAD_EXE)
        if ($found) { return $found }
    }

    $found = Get-FreeCADFromRegistry
    if ($found) { return $found }

    $found = Find-FreeCADExe $buildCandidates
    if ($found) { return $found }

    $programFiles = $env:ProgramFiles
    $programFilesX86 = (Get-Item -LiteralPath 'Env:ProgramFiles(x86)' -ErrorAction SilentlyContinue).Value

    $found = Find-FreeCADExe @(
        "$programFiles\FreeCAD 1.2\bin\FreeCAD.exe",
        "$programFiles\FreeCAD 1.0\bin\FreeCAD.exe",
        "$programFiles\FreeCAD 0.21\bin\FreeCAD.exe",
        "$programFiles\FreeCAD\bin\FreeCAD.exe",
        "$programFilesX86\FreeCAD 1.0\bin\FreeCAD.exe"
    )
    if ($found) { return $found }

    return Search-FreeCADOnDisk -FreecadRoot $FreecadRoot
}

$paths = Get-DavRepoPaths
$GuiRoot = $paths.GuiRoot
$DavMod = $paths.DavMod
$FreecadRoot = $paths.FreecadRoot

if (-not (Test-Path -LiteralPath $GuiRoot)) {
    throw "No se encontro GUIFreeCad en: $GuiRoot"
}
if (-not (Test-Path -LiteralPath (Join-Path $DavMod "InitGui.py"))) {
    throw "No se encontro el modulo Dav en: $DavMod"
}

$env:DAV_GUI_FREECAD_ROOT = $GuiRoot
$env:DAV_MOD_ROOT = $DavMod
$selectionRoot = Join-Path $paths.DavRepo "selection"
if (-not (Test-Path -LiteralPath $selectionRoot)) {
    $selectionRoot = Join-Path (Split-Path -Parent $paths.DavRepo) "selection"
}
$env:DAV_SELECTION_ROOT = $selectionRoot
$validationRoot = Join-Path $paths.DavRepo "validation"
if (-not (Test-Path -LiteralPath $validationRoot)) {
    $validationRoot = Join-Path (Split-Path -Parent $paths.DavRepo) "validation"
}
$env:DAV_VALIDATION_ROOT = $validationRoot
$dictionaryRoot = Join-Path $paths.DavRepo "DiccionariosEnBruto"
if (-not (Test-Path -LiteralPath $dictionaryRoot)) {
    $dictionaryRoot = Join-Path (Split-Path -Parent $paths.DavRepo) "DiccionariosEnBruto"
}
$env:DAV_DICTIONARY_ROOT = $dictionaryRoot
$env:DAV_OPEN_PREFS_ON_START = "0"
$env:DAV_AUTOLOAD_WORKBENCH = "1"

if (-not $FreeCADExe) {
    $savedLaunch = Get-DavLaunchConfig -GuiRoot $GuiRoot
    if ($savedLaunch -and $savedLaunch.freecad_exe) {
        $FreeCADExe = [string]$savedLaunch.freecad_exe
    }
}

$fcExe = Resolve-FreeCADExe -FreeCADExe $FreeCADExe -BuildDir $BuildDir -FreecadRoot $FreecadRoot
if (-not $fcExe) {
    Write-Host ""
    Write-Host "No se encontro FreeCAD.exe en este equipo." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opciones:" -ForegroundColor Cyan
    Write-Host "  1) Instalar FreeCAD: https://www.freecad.org/downloads.php"
    Write-Host "  2) Compilar FREECAD del repo y usar:"
    Write-Host '       .\run_freecad_dav.ps1 -BuildDir "C:\ruta\al\build"'
    Write-Host "  3) Si ya esta instalado en otra ruta:"
    Write-Host '       .\run_freecad_dav.ps1 -FreeCADExe "C:\ruta\bin\FreeCAD.exe"'
    Write-Host ""
    Write-Host "Mientras tanto, proba solo la GUI de preferencias:" -ForegroundColor Cyan
    Write-Host "  cd ..\luigiIntegracionV1\GUIFreeCad"
    Write-Host "  .\.venv\Scripts\activate"
    Write-Host "  python main.py"
    exit 1
}

$fcDir = Split-Path -Parent $fcExe
$fcPython = Join-Path $fcDir "python.exe"
$env:DAV_FREECAD_PYTHON = $fcPython
$fcHome = Split-Path -Parent $fcDir

$installedPath = Install-DavWorkbench -DavMod $DavMod -FcHome $fcHome
if (-not $installedPath) {
    throw 'No se pudo instalar el enlace DAV en Mod de FreeCAD.'
}

$env:DAV_MOD_ROOT = $installedPath
Save-DavLaunchConfig -GuiRoot $GuiRoot -FcExe $fcExe

$voiceAutostart = Resolve-VoiceAutostart -GuiRoot $GuiRoot -StartVoice:$StartVoice -NoStartVoice:$NoStartVoice
if ($voiceAutostart) {
    $env:DAV_AUTO_START_VOICE = "1"
} else {
    Remove-Item Env:DAV_AUTO_START_VOICE -ErrorAction SilentlyContinue
}

$settingsPath = Join-Path $GuiRoot "config\settings.json"
Write-Host "FreeCAD: $fcExe"
Write-Host "GUIFreeCad: $GuiRoot"
Write-Host "Preferencias: $settingsPath"
Write-Host "Modulo DAV: $installedPath"
Write-Host "Voz al abrir: $(if ($voiceAutostart) { 'si (Preferencias o -StartVoice)' } else { 'no (activar en barra DAV o Preferencias)' })"
Write-Host ""

$depsScript = Join-Path $PSScriptRoot "check_freecad_deps.ps1"
if (Test-Path $depsScript) {
    & $depsScript -FreeCADExe $fcExe
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Instalando dependencias de voz en Python de FreeCAD..." -ForegroundColor Yellow
        & $depsScript -FreeCADExe $fcExe -Install
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "No se pudieron instalar sounddevice ni vosk. El microfono fallara en Preferencias."
        }
    }
}

if ($InstallOnly) {
    Write-Host "Instalacion lista. Abri FreeCAD o ejecuta sin -InstallOnly." -ForegroundColor Green
    exit 0
}

& $fcExe
exit $LASTEXITCODE
