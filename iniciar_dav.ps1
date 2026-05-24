# Un solo comando para preparar GUIFreeCad y abrir FreeCAD con DAV.
# Uso:
#   .\iniciar_dav.ps1
#   .\iniciar_dav.ps1 -FreeCADExe "L:\Programas\Freecad\bin\FreeCAD.exe"
#   .\iniciar_dav.ps1 -InstallOnly
#   Doble clic en iniciar_dav.bat (equivalente)

param(
    [string]$FreeCADExe = "",
    [string]$BuildDir = "",
    [switch]$InstallOnly,
    [switch]$SkipModels
)

$ErrorActionPreference = "Stop"

$RepoRoot = $PSScriptRoot
$GuiRoot = Join-Path $RepoRoot "GUIFreeCad"
$ScriptsDir = Join-Path $RepoRoot "scripts"
$RunScript = Join-Path $ScriptsDir "run_freecad_dav.ps1"
$VenvPy = Join-Path $GuiRoot ".venv\Scripts\python.exe"
$ReqFile = Join-Path $GuiRoot "requirements.txt"
$SetupModels = Join-Path $GuiRoot "scripts\setup_models.py"
$ModelEs = Join-Path $GuiRoot "models\vosk-model-small-es-0.42"

function Write-Step([string]$Text) {
    Write-Host ""
    Write-Host "== $Text ==" -ForegroundColor Cyan
}

function Write-Ok([string]$Text) {
    Write-Host "  OK  $Text" -ForegroundColor Green
}

function Write-Warn([string]$Text) {
    Write-Host "  !!  $Text" -ForegroundColor Yellow
}

function Get-SystemPython {
    try {
        $out = & py -3 -c "import sys; print(sys.executable)" 2>$null
        if ($LASTEXITCODE -eq 0 -and $out) { return $out.Trim() }
    } catch { }

    try {
        $out = & python -c "import sys; print(sys.executable)" 2>$null
        if ($LASTEXITCODE -eq 0 -and $out) { return $out.Trim() }
    } catch { }

    return $null
}

function Ensure-GuiVenv {
    param([string]$SystemPython)

    if (Test-Path -LiteralPath $VenvPy) {
        Write-Ok "Entorno virtual en GUIFreeCad\.venv"
        return
    }

    Write-Host "  Creando .venv en GUIFreeCad..."
    & $SystemPython -m venv (Join-Path $GuiRoot ".venv")
    if (-not (Test-Path -LiteralPath $VenvPy)) {
        throw "No se pudo crear GUIFreeCad\.venv"
    }
    Write-Ok "Entorno virtual creado"
}

function Ensure-GuiDependencies {
    param([string]$GuiPython)

    & $GuiPython -c "import PySide6, vosk, sounddevice" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Ok "Dependencias Python de GUIFreeCad"
        return
    }

    Write-Host "  Instalando requirements.txt..."
    & $GuiPython -m pip install --upgrade pip 2>$null | Out-Null
    & $GuiPython -m pip install -r $ReqFile
    if ($LASTEXITCODE -ne 0) {
        throw "Fallo pip install en GUIFreeCad"
    }
    Write-Ok "Dependencias instaladas"
}

function Ensure-VoskModels {
    param([string]$GuiPython)

    if ($SkipModels) {
        Write-Warn "Omitiendo descarga de modelos (-SkipModels)"
        return
    }

    if (Test-Path -LiteralPath $ModelEs) {
        Write-Ok "Modelo Vosk ES en GUIFreeCad\models"
        return
    }

    Write-Host "  Descargando modelos Vosk (solo la primera vez, puede tardar)..."
    & $GuiPython $SetupModels
    if ($LASTEXITCODE -ne 0) {
        throw "Fallo scripts\setup_models.py"
    }
    Write-Ok "Modelos Vosk listos"
}

Write-Host "DAV - inicio unificado" -ForegroundColor White
Write-Host "Repo: $RepoRoot"

if (-not (Test-Path -LiteralPath $GuiRoot)) {
    throw "No se encontro GUIFreeCad en: $GuiRoot"
}
if (-not (Test-Path -LiteralPath $RunScript)) {
    throw "No se encontro: $RunScript"
}

Write-Step "1/3 Python del sistema"
$sysPy = Get-SystemPython
if (-not $sysPy) {
  throw "No se encontro Python 3. Instala Python 3.10+ o usa 'py -3'."
}
Write-Ok $sysPy

Write-Step "2/3 GUIFreeCad (venv, deps, modelos)"
Ensure-GuiVenv -SystemPython $sysPy
Ensure-GuiDependencies -GuiPython $VenvPy
Ensure-VoskModels -GuiPython $VenvPy

Write-Step "3/3 FreeCAD + workbench DAV"
$runArgs = @()
if ($FreeCADExe) { $runArgs += "-FreeCADExe"; $runArgs += $FreeCADExe }
if ($BuildDir) { $runArgs += "-BuildDir"; $runArgs += $BuildDir }
if ($InstallOnly) { $runArgs += "-InstallOnly" }

& $RunScript @runArgs
exit $LASTEXITCODE
