# Verifica / instala dependencias de voz en el Python de FreeCAD.
param(
    [string]$FreeCADExe = "",
    [switch]$Install
)

function Get-FreeCADPython {
    param([string]$FcExe)
    if ($FcExe) {
        $bin = Split-Path -Parent $FcExe
        $py = Join-Path $bin "python.exe"
        if (Test-Path $py) { return $py }
    }
    $reg = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\FreeCAD.exe"
    if (Test-Path $reg) {
        $fc = (Get-ItemProperty $reg)."(default)"
        $py = Join-Path (Split-Path $fc) "python.exe"
        if (Test-Path $py) { return $py }
    }
    return $null
}

$py = Get-FreeCADPython -FcExe $FreeCADExe
if (-not $py) {
    Write-Error "No se encontro python.exe de FreeCAD"
}

Write-Host "Python FreeCAD: $py"

$mods = @("sounddevice", "vosk", "numpy")
$missing = @()
foreach ($m in $mods) {
    & $py -c "import $m" 2>$null
    if ($LASTEXITCODE -ne 0) { $missing += $m } else { Write-Host "  OK  $m" -ForegroundColor Green }
}

if ($missing.Count -eq 0) {
    Write-Host "Todas las dependencias de voz estan instaladas." -ForegroundColor Green
    exit 0
}

Write-Host "Faltan: $($missing -join ', ')" -ForegroundColor Yellow
if ($Install) {
    & $py -m pip install sounddevice vosk numpy requests
    exit $LASTEXITCODE
}

Write-Host 'Ejecuta: .\check_freecad_deps.ps1 -Install'
exit 1
