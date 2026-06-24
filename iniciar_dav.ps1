# Wrapper: delega en el launcher de IntegracionGUI (layout DavCore).
# Soporta tanto el layout nuevo (Dav\scr\ComponentesDAV\...) como el previo.
$candidates = @(
    "$PSScriptRoot\Dav\scr\ComponentesDAV\IntegracionGUI\iniciar_dav.ps1",
    "$PSScriptRoot\ComponentesDAV\IntegracionGUI\iniciar_dav.ps1"
)
$target = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $target) {
    Write-Error "No se encontro iniciar_dav.ps1 de IntegracionGUI en: $($candidates -join ', ')"
    exit 1
}
& $target @args
exit $LASTEXITCODE
