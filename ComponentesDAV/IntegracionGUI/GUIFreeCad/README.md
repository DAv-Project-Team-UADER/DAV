# GUIFreeCad — Proyecto DAV

Interfaz con estilo FreeCAD para configurar preferencias por **clic** y por **voz** (Vosk). Incluye el **motor de voz unificado** que se conecta al diccionario CAD de `DAV-Luigi/PruebaIntegracion` sin modificar su código core.

> **Para el equipo (clone + FreeCAD + voz CAD):** leer [INTEGRACION_EQUIPO.md](INTEGRACION_EQUIPO.md)

## Requisitos

- Python 3.10+
- Micrófono (para comandos por voz)
- FreeCAD + repo [DAV-Luigi](https://github.com/Elluis1/DAV-Luigi) (rama `Pruebas`) para integración completa

## Instalación rápida (solo esta GUI)

```bash
cd GUIFreeCad
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/setup_models.py
python main.py
```

## Integración con FreeCAD

Layout esperado:

```
Repositorio DAVFreeCad/
├── GUIFreeCad/                 ← este repo
└── DAVFreecad-Pruebas/DAV-Luigi/
```

```powershell
cd DAVFreecad-Pruebas\DAV-Luigi\scripts
.\check_freecad_deps.ps1 -FreeCADExe "RUTA\FreeCAD.exe" -Install
.\run_freecad_dav.ps1 -FreeCADExe "RUTA\FreeCAD.exe" -InstallOnly
.\run_freecad_dav.ps1 -FreeCADExe "RUTA\FreeCAD.exe"
```

Workbench **DAV** → **Iniciar voz DAV** → comandos en pestaña **Informe**.

## Preferencias

| Opción | Valores |
|--------|---------|
| Idioma | Inglés, Español, Portugués |
| Modelo | Pequeño (local) / Grande (descarga) |
| Tema | Claro / Oscuro |
| Arranque | Voz DAV al abrir FreeCAD |

## Voz en Preferencias (ejemplos)

- `español`, `tema oscuro`, `modelo pequeño`, `aplicar`

## Voz CAD (con DAV-Luigi, ejemplos)

- `archivo enviar` → `nuevo enviar`
- `preferencias enviar`
- `editar enviar` → `deshacer enviar`

Patrón: **`comando enviar`** en la misma frase. Detalle en [INTEGRACION_EQUIPO.md](INTEGRACION_EQUIPO.md).

## Estructura

```
GUIFreeCad/
├── main.py
├── integration/          # Puente FreeCAD, sesión CAD, aliases ES/PT
│   ├── cad_voice_adapter.py
│   ├── dav_paths.py
│   ├── freecad_gui_bridge.py
│   ├── freecad_voice_setup.py
│   └── voice_bootstrap.py
├── speech/
│   ├── dav_voice_service.py   # Micrófono único
│   └── voice_commands.py
├── core/                 # settings, modelos, i18n
├── ui/                   # preferencias, temas
├── i18n/
├── assets/
├── models/               # Vosk (no en git; setup_models.py)
└── scripts/
```

Variable opcional si la ruta cambia: `DAV_GUI_FREECAD_ROOT`
