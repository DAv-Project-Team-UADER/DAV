# DAV — Diseño Asistido por Voz
**Práctica Educativa Territorial — Facultad de Ciencia y Tecnología (FCyT) — UADER**

---

## ¿Qué es DAV?

DAV es una interfaz de control por voz para FreeCAD, desarrollada como Práctica Educativa Territorial. El objetivo es construir un MVP que permita operar FreeCAD íntegramente mediante comandos de voz, usando Vosk como motor de reconocimiento y Python como lenguaje de extensión sobre el stack nativo de FreeCAD.

---

## Estructura del repositorio

```
DAV/
├── FREECAD/          # Código fuente de FreeCAD (fork base)
│   ├── src/          # Módulos Python y C++ de FreeCAD
│   │   ├── App/      # Núcleo de la aplicación (FreeCADInit.py)
│   │   ├── Gui/      # Interfaz gráfica (FreeCADGuiInit.py)
│   │   ├── Ext/freecad/  # Extensiones Python propias de FreeCAD
│   │   └── Mod/      # Workbenches: Draft, Sketcher, Part, PartDesign,
│   │                 #   Assembly, TechDraw, etc.
│   └── CMakeLists.txt
├── Dav/              # Todo el código propio del proyecto
│   ├── dic/          # Árbol de comandos por voz (ver más abajo)
│   ├── docs/         # Documentación, planes, informes, normativas
│   ├── models/       # Modelos Vosk es/en/pt (excluidos de git)
│   └── scr/          # Código fuente
│       ├── ComponentesDAV/
│       │   ├── IntegracionGUI/  # Motor Browser (navigation/) + montaje del panel
│       │   ├── InterfazDAV/     # DavPanel: el widget de la GUI (sin FreeCAD)
│       │   ├── Keychain/        # Lectura de claves de diccionarios
│       │   ├── Dav/             # InitGui.py — arranque dentro de FreeCAD
│       │   ├── Logos/
│       │   └── scripts/
│       ├── PruebaIntegracion/
│       ├── selection/           # CreateObjects — extracción de sub-elementos
│       └── validation/
└── CLAUDE.md
```

---

## Requerimientos funcionales del MVP

El sistema debe permitir controlar las siguientes características de FreeCAD **mediante la voz**:

| Módulo | Descripción |
|---|---|
| **Explorer** | Nuevo, abrir, guardar, exportar, cerrar archivos |
| **Viewer** | Cambio de vista (frontal, ortogonal, perspectiva), zoom, corte |
| **Draft** | Dibujo directo con líneas, anotaciones, modificaciones |
| **Sketcher** | Bocetos con restricciones geométricas sobre planos base |
| **PartDesign** | Extrusión, chaflán y otras operaciones 3D sobre cuerpos |
| **PartWorkspace** | Operaciones con piezas estándar (Part workbench) |
| **Assembly** | Ensamble y articulación de piezas con juntas |
| **TechDraw** | Tablero técnico: vistas, medidas, rótulo, exportación |

La interfaz gráfica (DAV GUI) debe además:
- **Arrancar con FreeCAD** (iniciarse automáticamente junto al programa)
- **Minimizarse** (mostrarse/ocultarse sin interrumpir el editor)
- **Dar historial** (navegar objetos creados y comandos aplicados)

---

## Arquitectura técnica

### DAVCore (motor de voz)

El DAVCore se ejecuta como un script Python dentro de la consola Python de FreeCAD. Corre en un hilo separado (`latentListening`) para no bloquear la UI.

```
DAVAgent
├── language: String
├── model: VoskModel
├── instructionsDic: Map
├── instructionHeader: List
├── latentListening(acceptedWords: List) : String
└── searchInstruction(key: String) : void

«Interface» VoskModel
├── loadModel(path: String)
└── recognize(audioStream: Stream) : String
```

### Stack de tecnologías

| Componente | Tecnología |
|---|---|
| CAD base | FreeCAD 1.x (Python 3.11–3.12 embebido) |
| Reconocimiento de voz | Vosk (`vosk-model-small-es-0.42`, más en/pt) |
| Captura de audio | PyAudio |
| Interfaz gráfica DAV | PySide6 (la misma que usa FreeCAD) |
| Lenguaje de extensión | Python |

> El venv de desarrollo (`IntegracionGUI/GUIFreeCad/.venv`) usa Python 3.14, más
> nuevo que el Python embebido de FreeCAD. El código tiene que correr en ambos:
> los scripts que se cargan dentro de FreeCAD usan su intérprete, no el venv.
>
> Las extensiones de FreeCAD **deben usar PySide6**, no PyQt, por compatibilidad constructiva con el framework nativo de FreeCAD.

### Punto de entrada

Los scripts se cargan desde la consola Python de FreeCAD o como macros. El DAVCore debe iniciarse igual que lo hace `FreeCADGuiInit.py`, es decir, al arrancar la aplicación.

### Diccionario de comandos por voz (`Dav/dic/`)

El árbol de comandos por voz vive en `Dav/dic/`, organizado por carpetas navegables (una carpeta = un nivel de contexto). Cada carpeta tiene:

- Un diccionario base (`<nombre>.py`) con las claves internas → callables de FreeCAD.
- Traducciones por idioma (`TraduceToEs.py`, `TraduceToEn.py`, `TraduceToPT.py`) que mapean frases habladas → los mismos callables.

`Dav/dic/base.py` es el punto de entrada: enlaza los módulos de nivel superior (`explorer`, `stdview`, `workbench`, `lineattributes`, `preferences`). El motor que recorre este árbol en runtime es `Browser` (`Dav/scr/.../GUIFreeCad/navigation/browser.py`), no el `DAVAgent` descripto arriba — ese diagrama es el diseño conceptual original; la implementación real usa `Browser.ProcessPhrase` + `DictionaryLoader`.

Los comandos de navegación del propio `Browser` (subir un nivel, mostrar el contexto actual) **no están hardcodeados en código**: viven en `Dav/dic/NavCommands/` igual que cualquier otro comando, para que el equipo pueda agregar sinónimos sin tocar `browser.py`.

> La GUI es **`DavPanel`** (`Dav/scr/ComponentesDAV/InterfazDAV/DavPanel.py`), un
> `QDockWidget` que corre dentro de FreeCAD y se alimenta del `Browser` en
> proceso vía `integration/dav_dock_panel.py`. El widget no importa FreeCAD: se
> le pasan datos y emite señales, así se puede testear aparte.
>
> Ya no existen `MainWindow.py`, su motor de voz propio (`_VoiceMap`/`_GroupMeta`)
> ni `DiccionarioPrueba/`: se retiraron al acoplar el panel. Ver
> `Dav/docs/completados-dav.md`.

#### Regla crítica: subcontextos anidados, nunca aplanados

Al armar el diccionario maestro de una carpeta, cada submenú va **como valor
bajo su propia clave**, nunca fusionado con `.update(sub_dict)`:

```python
explorer.update({'file': file})   # CORRECTO — 'file' queda navegable
explorer.update(file)             # INCORRECTO — aplana las hojas del hijo
```

Aplanar rompe dos cosas en silencio: colisiona claves repetidas entre hojas
(`create`, `help`, `center`) quedándose solo con la última, y deja la carpeta
fuera del árbol navegable, con lo cual su `TraduceTo*.py` no se carga nunca.
Detalle completo en `Dav/docs/pendientes-dav.md` §4.

---

## Documentación del proyecto (`Dav/docs/`)

| Archivo | Contenido |
|---|---|
| `pendientes-dav.md` | Lo que sigue abierto: hallazgos de auditoría, convenciones y qué falta para el MVP. **Leer antes de tocar diccionarios o navegación.** |
| `completados-dav.md` | Lo ya resuelto, con la **causa real** de cada caso. Consultar antes de re-diagnosticar algo que parece conocido. |
| `plan-unificacion-guis.md` | Migración de la GUI a panel acoplado (etapas 1-4 hechas, queda la 5) |
| `acortador-gramatica-vosk.md` | Cómo se acota la gramática de Vosk al contexto activo. **Leer antes de tocar `SetGrammar` o el loop de audio.** |
| `manual-explorer-voz.md` | Guía de uso del Explorer por voz (comandos y ejemplos) |
| `plan-migracion-hilos-qthread.md` | Plan de migración a `QThread`. Escrito para `InterfazDAV`, que ya se retiró; queda como referencia del criterio |
| `plan_arbol_de_objetos_navegable.md` | Plan del árbol de objetos navegable |
| `diagramas/` | Un archivo por clase, con el nombre de la clase (`Browser.md`, `DavVoiceService.md`…). Índice y vista general en `diagramas/README.md` |
| `informes/`, `normativas/`, `licencias/` | Material de cátedra y documentación formal |

---

## Instrucciones para el asistente (Claude)

- **No agregar `Co-Authored-By` ni ninguna mención al asistente** en los mensajes de commit.
- **No hacer `commit` ni `push` salvo que el usuario lo pida explícitamente.**

---

## Convenciones de código

### Nomenclatura

| Tipo | Convención | Ejemplo |
|---|---|---|
| Clases | PascalCase | `DavAgent`, `VoskModel` |
| Atributos / Propiedades | PascalCase | `LineColor`, `ShapeColor` |
| Funciones / Métodos | camelCase (minúscula inicial) | `addObject()`, `recompute()` |
| Uso interno | `_guiónBajo` | `_internalMethod` |

### Organización de archivos

- **Una clase = un archivo**
- **Un diccionario = un archivo**
- Nombre de archivo: igual que el nombre de la clase (`DavAgent.py`)

### Cabezal obligatorio (todos los archivos propios)

```python
# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.
```

> Los archivos de FreeCAD preexistentes deben conservar **su cabezal original** (LGPL-2.1-or-later).

### Documentación

- Documentar con **Mermaid** (diagramas de clases, arquitectura, flujos)
- Estándar **UML** para lo propio y lo que se consume de FreeCAD
- Herramienta sugerida: **Mermaid** integrado en Markdown

### Docstrings

- Toda clase y método público debe tener un **docstring** en **inglés**.
- Formato: primera línea corta (resumen), línea en blanco, luego secciones `Args:`, `Returns:`, `Example::` según corresponda.
- Los comentarios de desarrollador (`# ...`) van en **español**.
- El docstring es lo que los IDEs (VS Code, PyCharm) muestran como tooltip emergente al invocar la clase o el método.

### Principios de diseño

- **KISS** — Keep It Simple. Menos es más.
- **SOLID** — Responsabilidad Única, Abierto/Cerrado, Sustitución de Liskov, Segregación de Interfaces, Inversión de Dependencias.
- **Arquitectura Document-View** — la misma que usa FreeCAD internamente (Documento ↔ Vista ↔ Storage).

---

## GitFlow

Ramas que **existen hoy** en el repo central (`DAv-Project-Team-UADER/DAV`):

```
main      ────────────────────────────────○ (releases)
              ↑
DavCore   ──●──●──●──●──●──   ← rama de integración activa: todos los PRs van acá
              ↑     ↑     ↑
           forks personales de cada integrante
```

- **`main`** — solo recibe integraciones desde `DavCore`
- **`DavCore`** — rama de integración activa; **destino de todos los PRs**
- **`Develop`**, **`Pruebas`** — quedaron de la organización anterior; ya no
  reciben PRs nuevos (el último a `Pruebas` fue el #168)
- Ramas de equipo/feature puntuales: `Tade-Cami-Mica`,
  `feature/add-workbench-svg`, `fix/workbench-launcher`

> El diseño original preveía `develop` + feature branches por workbench
> (`WorkstationPartImplementation`, `ExplorerImplementation`, `VoskImplementation`,
> `DAVGUI`, `HotFix0.x`) con convención de commit `Vv1`/`Gv1`. En la práctica el
> equipo trabaja con forks personales que integran directo a `DavCore`; esas
> ramas ya no existen en el remoto.

---

## Organización por grupos y flujo de contribución

El proyecto se desarrolla en grupos de trabajo. Cada integrante trabaja sobre un **fork personal** del repositorio central ([DAv-Project-Team-UADER/DAV](https://github.com/DAv-Project-Team-UADER/DAV)).

### Flujo de trabajo individual

```
fork personal (julianAO2002/DAV)
    └── rama de trabajo (ej: pruebas, feature/Explorer)
            │
            │  Pull Request
            ▼
repositorio central (DAv-Project-Team-UADER/DAV) → rama pruebas
```

1. Cada integrante trabaja en su fork, en su rama correspondiente.
2. Al terminar una tarea, se abre un **Pull Request** desde la rama del fork hacia la rama `pruebas` del repositorio central.
3. El PR es revisado antes de ser integrado.

### Este fork

- **Repositorio original:** [`DAv-Project-Team-UADER/DAV`](https://github.com/DAv-Project-Team-UADER/DAV)
- **Este fork:** `julianAO2002/DAV`
- **Usuario:** `julianAO2002`
- **Grupo:** 4
- **Rama de trabajo actual:** `davcore-integracion`
- **Destino del PR:** rama `DavCore` del repositorio central (`DAv-Project-Team-UADER/DAV`)

> Nunca hacer PR directo a `main`. Todo pasa primero por `DavCore`, que después
> se integra a `main`.
>
> ⚠️ La rama de integración **cambió**: antes era `Pruebas` (así figura en PRs
> viejos, hasta el #168). Confirmar el destino vigente antes de abrir un PR —
> `gh pr list --repo DAv-Project-Team-UADER/DAV --limit 5` muestra contra qué
> rama están yendo los PRs actuales.

---

## Metodología de trabajo

- **Sprints semanales** con evaluación al cierre
- **KanBan** para seguimiento visual (tableros externos)
- **Issues en GitHub** con etiquetas por tipo (`bug`, `feature`, etc.)
- **Tickets** entregables en `.zip` con formato:
  ```
  <NombreApellidoEntregaN>.zip
  ```
  Cada ticket (`.txt`) documenta:
  - Nombre de la característica
  - Script nativo para invocarla
  - Breve descripción
  - Tipo (Función / Clase / Módulo)
  - Requiere / Devuelve
  - Palabras sugeridas para comandos por voz
  - Comentarios adicionales

### Criterios de evaluación

Crecimiento en Hard Skills · Aplicación de Hard Skills · Cumplimiento de Plazos · Compañerismo · Liderazgo · Trabajo en Equipo

---

## Cómo ejecutar un script en FreeCAD

```python
# Ejemplo mínimo de script FreeCAD (plantilla base)
import FreeCAD
from FreeCAD import Placement, Rotation, Vector
import FreeCADGui

DOC_NAME = "Wiki_Example"
DOC = FreeCAD.newDocument(DOC_NAME)
FreeCAD.setActiveDocument(DOC.Name)

ROT0 = Rotation(0, 0, 0)
VEC0 = Vector(0, 0, 0)

def set_view():
    if not FreeCADGui.GuiUp:
        return
    doc = FreeCADGui.ActiveDocument
    if doc is None:
        return
    view = doc.ActiveView
    if view is None:
        return
    if hasattr(view, "getSceneGraph"):
        view.viewAxometric()
        view.fitAll()
```

Los scripts se ejecutan desde la **Consola Python** integrada de FreeCAD (`Vista → Paneles → Consola de Python`) o como **Macros** (`Herramientas → Macros`).

---

## Modelo de voz

Los modelos viven en `Dav/models/` (excluidos de git, ver `Dav/models/README.md`):

| Modelo | Idioma |
|---|---|
| `vosk-model-small-es-0.42` | Español (39 MB, Apache 2.0) |
| `vosk-model-small-en-us-0.15` | Inglés |
| `vosk-model-small-pt-0.3` | Portugués |

Para reconocimiento de mayor precisión en español existe `vosk-model-es-0.42`
(1.4 GB), no incluido. La captura de micrófono usa **PyAudio**.

`core/model_manager.py` y `ui/download_dialog.py` (en `IntegracionGUI/GUIFreeCad/`)
descargan los modelos si faltan, así que no hace falta bajarlos a mano.

---

## Licencias relevantes

| Componente | Licencia |
|---|---|
| FreeCAD (núcleo) | LGPL-2.1-or-later |
| Código DAV propio | GPL-3.0 |
| Vosk | Apache 2.0 |
| PyAudio | MIT |
| PySide6 | LGPL-3.0 |
