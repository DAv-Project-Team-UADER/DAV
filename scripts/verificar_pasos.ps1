# Verifica el entorno DAV paso a paso (sin abrir ventanas GUI).
# Uso: .\scripts\verificar_pasos.ps1
#      .\scripts\verificar_pasos.ps1 -FreeCADExe "L:\Programas\Freecad\bin\FreeCAD.exe"

param(
    [string]$FreeCADExe = "L:\Programas\Freecad\bin\FreeCAD.exe"
)

$ErrorActionPreference = "Continue"
$DavRepo = Split-Path -Parent $PSScriptRoot
$GuiRoot = Join-Path $DavRepo "GUIFreeCad"
if (-not (Test-Path $GuiRoot)) {
    $ParentRoot = Split-Path -Parent (Split-Path -Parent $DavRepo)
    $GuiRoot = Join-Path $ParentRoot "GUIFreeCad"
}
$GuiPy = Join-Path $GuiRoot ".venv\Scripts\python.exe"

function Step($n, $title) {
    Write-Host ""
    Write-Host "=== Paso $n : $title ===" -ForegroundColor Cyan
}

function Ok($msg) { Write-Host "  OK  $msg" -ForegroundColor Green }
function Warn($msg) { Write-Host "  !!  $msg" -ForegroundColor Yellow }
function Fail($msg) { Write-Host "  XX  $msg" -ForegroundColor Red }

Step 0 "Repo DAV (rama Pruebas)"
Push-Location $DavRepo
$branch = git branch --show-current 2>$null
if ($branch -eq "Pruebas") { Ok "Rama: Pruebas" } else { Warn "Rama actual: $branch (recomendado: Pruebas)" }
Pop-Location

Step 1 "GUIFreeCad (preferencias)"
if (-not (Test-Path $GuiPy)) { Fail "No hay .venv en GUIFreeCad. Ejecuta: cd GUIFreeCad; python -m venv .venv; pip install -r requirements.txt" }
else {
    Push-Location $GuiRoot
    & $GuiPy -c "import PySide6, vosk, sounddevice; from integration.launch_preferences import open_preferences; print('ok')" 2>$null
    if ($LASTEXITCODE -eq 0) { Ok "Dependencias e integration/" } else { Fail "Faltan deps en GUIFreeCad/.venv" }
    if (Test-Path "models\vosk-model-small-es-0.42") { Ok "Modelo Vosk ES en GUIFreeCad" } else { Warn "Falta modelo en GUIFreeCad/models (python scripts/setup_models.py)" }
    Pop-Location
}

Step 2 "InterfazDAV (asistente compañeros)"
Push-Location (Join-Path $DavRepo "InterfazDAV")
& $GuiPy -c "from MainWindow import MainWindow; print('ok')" 2>$null
if ($LASTEXITCODE -eq 0) { Ok "InterfazDAV importa con venv de GUIFreeCad" } else { Fail "InterfazDAV no importa" }
Pop-Location

Step 3 "Keychain (diccionarios)"
Push-Location (Join-Path $DavRepo "Keychain")
python -c "from Keychain import Keychain; k=Keychain('dic/explorer.py'); print(len(k.GetAllKeys()))" 2>$null
if ($LASTEXITCODE -eq 0) { Ok "Keychain lee dic/explorer.py" } else { Fail "Keychain fallo" }
Pop-Location

Step 4 "PruebaIntegracion (demo sin microfono)"
Push-Location $DavRepo
python -m PruebaIntegracion.main --demo --max-iter 2 --script "file enviar" "edit enviar" 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) { Ok "Motor voz+diccionarios (modo demo)" } else { Warn "PruebaIntegracion demo fallo o quedo colgado" }
Pop-Location

Step 5 "Mod DAV en FreeCAD"
$modPath = ""
if ($FreeCADExe -and (Test-Path $FreeCADExe)) {
    $fcHome = (Resolve-Path (Join-Path (Split-Path $FreeCADExe) "..")).Path
    $modPath = Join-Path $fcHome "Mod\DAV\InitGui.py"
}
if ($modPath -and (Test-Path $modPath)) { Ok "Mod instalado: $modPath" }
else { Warn "Mod DAV no instalado. Ejecuta: .\scripts\run_freecad_dav.ps1 -InstallOnly" }

Step 6 "Python FreeCAD + deps voz"
if (Test-Path $FreeCADExe) {
    & (Join-Path $PSScriptRoot "check_freecad_deps.ps1") -FreeCADExe $FreeCADExe 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { Ok "vosk/sounddevice en Python de FreeCAD" } else { Warn "Faltan deps en FreeCAD (check_freecad_deps.ps1 -Install)" }
} else { Warn "FreeCAD no encontrado en: $FreeCADExe" }

Step 7 "Puente GUIFreeCad desde Mod DAV"
if ((Test-Path $FreeCADExe) -and (Test-Path $modPath)) {
    $fcPy = Join-Path (Split-Path $FreeCADExe) "python.exe"
    $davMod = Split-Path $modPath
    $env:DAV_GUI_FREECAD_ROOT = $GuiRoot
    $env:DAV_MOD_ROOT = $davMod
    & $fcPy -c "import sys; sys.path[:0]=[r'$davMod', r'$GuiRoot']; from scr.gui.dav_commands import _guifreecad_root; assert _guifreecad_root().exists()" 2>$null
    if ($LASTEXITCODE -eq 0) { Ok "FreeCAD puede resolver GUIFreeCad" } else { Fail "Puente Dav -> GUIFreeCad roto" }
}

Write-Host ""
Write-Host "Siguiente: probar manualmente" -ForegroundColor Cyan
Write-Host "  1) GUIFreeCad:  cd GUIFreeCad && .venv\Scripts\activate && python main.py"
Write-Host "  2) InterfazDAV: cd InterfazDAV && ..\GUIFreeCad\.venv\Scripts\python.exe main.py"
Write-Host "  3) FreeCAD:     cd scripts && .\run_freecad_dav.ps1 -FreeCADExe `"$FreeCADExe`""
Write-Host ""
