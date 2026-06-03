# luigiIntegracionV1

Integración DAV (preferencias + voz unificada + FreeCAD) — entrega v1.

## Contenido

| Carpeta / archivo | Descripción |
|-------------------|-------------|
| `GUIFreeCad/` | GUI de preferencias, motor de voz, adaptador CAD |
| `iniciar_dav.ps1` | Un comando: venv, deps, modelos Vosk y FreeCAD |
| `iniciar_dav.bat` | Mismo arranque con doble clic |

## Arranque

```powershell
cd luigiIntegracionV1
.\iniciar_dav.ps1 -FreeCADExe "C:\ruta\bin\FreeCAD.exe"
```

Desde la raíz del repo también funciona: `.\iniciar_dav.ps1` (wrapper).

Guía completa: [`GUIFreeCad/INTEGRACION_EQUIPO.md`](GUIFreeCad/INTEGRACION_EQUIPO.md).
