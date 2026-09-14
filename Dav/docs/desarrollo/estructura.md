# Estructura del repositorio

El repositorio mezcla dos cosas: el **código fuente de FreeCAD** (el fork base
que se trae completo) y el **código propio de DAV** (la capa de voz). Es
importante saber en qué mitad estás trabajando, porque los cabezales de
licencia y las reglas son distintos.

```
DAV/
├── FREECAD/          # Código fuente de FreeCAD (fork base, NO se toca de esto salvo que sea necesario)
│   ├── src/          #   Módulos Python y C++ de FreeCAD
│   │   ├── App/      #   Núcleo de la aplicación (FreeCADInit.py)
│   │   ├── Gui/      #   Interfaz gráfica (FreeCADGuiInit.py)
│   │   ├── Ext/freecad/  #   Extensiones Python propias de FreeCAD
│   │   └── Mod/      #   Workbenches: Draft, Sketcher, Part, PartDesign,
│   │                 #     Assembly, TechDraw, etc.
│   └── CMakeLists.txt
├── Dav/              # ⭐ TODO el código propio del proyecto DAV
│   ├── dic/          #   Árbol de comandos por voz (ver abajo)
│   ├── docs/         #   Documentación, planes, informes, normativas
│   ├── models/       #   Modelos Vosk es/en/pt (excluidos de git)
│   └── scr/          #   Código fuente en Python
│       ├── ComponentesDAV/
│       │   ├── IntegracionGUI/  # Motor Browser (navigation/) + montaje del panel
│       │   ├── InterfazDAV/     # DavPanel: el widget de la GUI (sin FreeCAD)
│       │   ├── Keychain/        # Lectura de claves de diccionarios
│       │   ├── Dav/             # InitGui.py — arranque dentro de FreeCAD
│       │   ├── Logos/
│       │   └── scripts/
│       ├── PruebaIntegracion/
│       ├── selection/           # CreateObjects — extracción de sub-elementos
│       └── validation/          # Validator — reglas de validación de comandos
└── CLAUDE.md
```

## Dónde vive cada cosa

| ¿Qué estás buscando? | ¿Dónde está? |
|---|---|
| Motor de navegación por voz (`Browser`) | `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/navigation/browser.py` |
| Árbol de comandos por voz | `Dav/dic/` |
| Traducción frase hablada → comando | `TraduceTo*.py` dentro de cada carpeta de `Dav/dic/` |
| Lectura de claves de diccionarios | `Dav/scr/ComponentesDAV/Keychain/` |
| Widget de la GUI (panel) | `Dav/scr/ComponentesDAV/InterfazDAV/DavPanel.py` |
| Extracción de sub-elementos (selección) | `Dav/scr/selection/` |
| Validación de comandos | `Dav/scr/validation/` |
| Modelos Vosk (no versionados) | `Dav/models/` |
| Documentación del proyecto | `Dav/docs/` |

## El árbol de comandos por voz (`Dav/dic/`)

Cada **carpeta** del árbol es un **nivel de contexto** y tiene:

- Un diccionario maestro: `<nombre>.py` con las **claves internas → callables**
  de FreeCAD (ej. `explorer.py`, `sketcher.py`).
- Traducciones por idioma: `TraduceToEs.py`, `TraduceToEn.py`, `TraduceToPT.py`
  que mapean **frases habladas → los mismos callables**.

`Dav/dic/base.py` es el punto de entrada: enlaza los módulos de nivel superior
(`explorer`, `stdview`, `workbench`, `lineattributes`, `preferences`).

El motor que recorre este árbol en runtime es `Browser`
(`Dav/scr/.../GUIFreeCad/navigation/browser.py`) + `DictionaryLoader`
(`navigation/dictionary_loader.py`).

> ⚠️ Importante: aunque históricamente existió un `DAVAgent` con
> `latentListening`, la implementación real usa `Browser.ProcessPhrase` +
> `DictionaryLoader`. Si un diagrama viejo te muestra `DAVAgent`, es el diseño
> conceptual original, no el código vigente.

## La GUI es un panel acoplado

El panel (`DavPanel`) es un `QDockWidget` que corre dentro de FreeCAD y se
alimenta del `Browser` **en proceso** vía
`Dav/scr/.../GUIFreeCad/integration/dav_dock_panel.py`. El widget no importa
FreeCAD: se le pasan datos y emite señales, así se puede testear aparte.

Ya no existen `MainWindow.py`, su motor de voz propio (`_VoiceMap`/`_GroupMeta`)
ni `DiccionarioPrueba/`: se retiraron al acoplar el panel.
