# Un solo comando para preparar GUIFreeCad y abrir FreeCAD con DAV.
# Uso:
#   .\iniciar_dav.ps1
#   .\iniciar_dav.ps1 -FreeCADExe "L:\Programas\Freecad\bin\FreeCAD.exe"
#   .\iniciar_dav.ps1 -InstallOnly
#   .\iniciar_dav.ps1 -StartVoice
#   .\iniciar_dav.ps1 -RegistrarInicioWindows
#   Doble clic en iniciar_dav.bat (equivalente)

param(
    [string]$FreeCADExe = "",
    [string]$BuildDir = "",
    [switch]$InstallOnly,
    [switch]$SkipModels,
    [switch]$StartVoice,
    [switch]$NoStartVoice,
    [switch]$RegistrarInicioWindows
)

$ErrorActionPreference = "Continue"

$IntegrationRoot = $PSScriptRoot
$GuiRoot = Join-Path $IntegrationRoot "GUIFreeCad"

function Resolve-DavRepoRoot {
    # Sube hasta la raíz REAL del repo (FREECAD\ o Dav\dic\base.py). Evita el
    # placeholder ComponentesDAV\Dav\dic. Con el layout DavCore este wrapper
    # está en Dav\scr\ComponentesDAV\IntegracionGUI.
    $current = Split-Path -Parent $IntegrationRoot   # ComponentesDAV
    for ($i = 0; $i -lt 6; $i++) {
        $hasFreecad = Test-Path -LiteralPath (Join-Path $current "FREECAD")
        $hasRealDic = Test-Path -LiteralPath (Join-Path $current "Dav\dic\base.py")
        if ($hasFreecad -or $hasRealDic) { return $current }
        $parent = Split-Path -Parent $current
        if ($parent -eq $current) { break }
        $current = $parent
    }
    return (Split-Path -Parent $IntegrationRoot)
}

$RepoRoot = Resolve-DavRepoRoot

function Find-RunScript([string]$StartRepo) {
    $candidates = @(
        (Join-Path $StartRepo "ComponentesDAV\scripts\run_freecad_dav.ps1"),
        (Join-Path $StartRepo "componentesDAV\scripts\run_freecad_dav.ps1"),
        (Join-Path $StartRepo "scripts\run_freecad_dav.ps1")
    )
    foreach ($path in $candidates) {
        if (Test-Path -LiteralPath $path) { return $path }
    }

    $dir = $StartRepo
    while ($dir) {
        $candidate = Join-Path $dir "scripts\run_freecad_dav.ps1"
        if (Test-Path -LiteralPath $candidate) { return $candidate }
        $parent = Split-Path -Parent $dir
        if ($parent -eq $dir) { break }
        $dir = $parent
    }
    return $null
}

$RunScript = Find-RunScript $RepoRoot
if ($RunScript) {
    $ScriptsDir = Split-Path -Parent $RunScript
} else {
    $ScriptsDir = Join-Path $RepoRoot "ComponentesDAV\scripts"
}

$VenvPy = Join-Path $GuiRoot ".venv\Scripts\python.exe"
$ReqFile = Join-Path $GuiRoot "requirements.txt"
$SetupModels = Join-Path $GuiRoot "scripts\setup_models.py"
# El modelo puede vivir en el layout DavCore (Dav\models) o el previo
# (GUIFreeCad\models). Resolve-DavRepoRoot ya ubica la raíz del repo.
$ModelEsCandidates = @(
    (Join-Path (Resolve-DavRepoRoot) "Dav\models\vosk-model-small-es-0.42"),
    (Join-Path $GuiRoot "models\vosk-model-small-es-0.42")
)

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

    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    try {
        & $GuiPython -c "import PySide6, vosk, sounddevice" 2>$null
        $success = ($LASTEXITCODE -eq 0)
    } catch {
        $success = $false
    } finally {
        $ErrorActionPreference = $oldPreference
    }

    if ($success) {
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

    $modelPresent = $ModelEsCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if ($modelPresent) {
        Write-Ok "Modelo Vosk ES presente: $modelPresent"
        return
    }

    Write-Host "  Descargando modelos Vosk (solo la primera vez, puede tardar)..."
    & $GuiPython $SetupModels
    if ($LASTEXITCODE -ne 0) {
        throw "Fallo scripts\setup_models.py"
    }
    Write-Ok "Modelos Vosk listos"
}

function Register-DavWindowsStartup {
    param([switch]$Remove)

    $py = $VenvPy
    if (-not (Test-Path -LiteralPath $py)) {
        throw "No hay .venv en GUIFreeCad para configurar el inicio de Windows."
    }
    $flag = if ($Remove) { "False" } else { "True" }
    & $py -c "import sys; sys.path.insert(0, r'$GuiRoot'); from integration.windows_startup import sync_windows_startup; ok, msg = sync_windows_startup($flag); print(msg); raise SystemExit(0 if ok else 1)"
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudo configurar el inicio de Windows."
    }
    Write-Ok "Inicio de Windows configurado"
}

Write-Host "DAV - inicio unificado" -ForegroundColor White
Write-Host "Integracion: $IntegrationRoot"
Write-Host "Repo: $RepoRoot"

if (-not (Test-Path -LiteralPath $GuiRoot)) {
    throw "No se encontro GUIFreeCad en: $GuiRoot"
}
if (-not $RunScript) {
    throw "No se encontro run_freecad_dav.ps1 (buscado en ComponentesDAV\scripts y scripts\)."
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

Write-Step "3/3 FreeCAD + workbench DAV (sistema completo)"
$runArgs = @()
if ($FreeCADExe) { $runArgs += "-FreeCADExe"; $runArgs += $FreeCADExe }
if ($BuildDir) { $runArgs += "-BuildDir"; $runArgs += $BuildDir }
if ($InstallOnly) { $runArgs += "-InstallOnly" }
if ($StartVoice) { $runArgs += "-StartVoice" }
if ($NoStartVoice) { $runArgs += "-NoStartVoice" }

& $RunScript @runArgs
$exitCode = $LASTEXITCODE

if ($RegistrarInicioWindows) {
    Write-Step "Inicio automatico con Windows"
    Register-DavWindowsStartup
    if ($InstallOnly) { exit 0 }
}

exit $exitCode
