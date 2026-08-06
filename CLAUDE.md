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
├── IDEAS/            # Documentos de diseño, diagramas Mermaid
├── MODELO/           # Modelos Vosk y PyAudio (excluidos de git)
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
| CAD base | FreeCAD 1.x (Python 3.11–3.12) |
| Reconocimiento de voz | Vosk (`vosk-model-small-es-0.42`) |
| Captura de audio | PyAudio |
| Interfaz gráfica DAV | PySide6 (la misma que usa FreeCAD) |
| Lenguaje de extensión | Python |

> Las extensiones de FreeCAD **deben usar PySide6**, no PyQt, por compatibilidad constructiva con el framework nativo de FreeCAD.

### Punto de entrada

Los scripts se cargan desde la consola Python de FreeCAD o como macros. El DAVCore debe iniciarse igual que lo hace `FreeCADGuiInit.py`, es decir, al arrancar la aplicación.

### Diccionario de comandos por voz (`Dav/dic/`)

El árbol de comandos por voz vive en `Dav/dic/`, organizado por carpetas navegables (una carpeta = un nivel de contexto). Cada carpeta tiene:

- Un diccionario base (`<nombre>.py`) con las claves internas → callables de FreeCAD.
- Traducciones por idioma (`TraduceToEs.py`, `TraduceToEn.py`, `TraduceToPT.py`) que mapean frases habladas → los mismos callables.

`Dav/dic/base.py` es el punto de entrada: enlaza los módulos de nivel superior (`explorer`, `stdview`, `workbench`, `lineattributes`, `preferences`). El motor que recorre este árbol en runtime es `Browser` (`Dav/scr/.../GUIFreeCad/navigation/browser.py`), no el `DAVAgent` descripto arriba — ese diagrama es el diseño conceptual original; la implementación real usa `Browser.ProcessPhrase` + `DictionaryLoader`.

Los comandos de navegación del propio `Browser` (subir un nivel, mostrar el contexto actual) **no están hardcodeados en código**: viven en `Dav/dic/NavCommands/` igual que cualquier otro comando, para que el equipo pueda agregar sinónimos sin tocar `browser.py`.

> ⚠️ **`MainWindow.py`** (`Dav/scr/ComponentesDAV/InterfazDAV/`) usa un motor de voz propio (`_VoiceMap`/`_GroupMeta`) que lee de un diccionario de prueba aparte (`InterfazDAV/DiccionarioPrueba/`), **no** del árbol `Dav/dic/` ni de `Browser`. Son dos sistemas distintos — ver `Dav/docs/pendientes-dav.md` antes de asumir que un fix en uno aplica al otro.

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

```
main          ──────────────────────────────────────────○ (release v0.1.0)
pruebas       ──●──●──●──●──●── (P1, P2, P3, P4, PN …)
develop       ──────────────────○──────────────○──────────○──●
                      ↓              ↓               ↓
              WorkstationPart   Explorer        WorkstationPart2
              Implementation    Implementation  Implementation
              (magenta)         (rojo)          (azul oscuro)
```

- **`main`** — solo recibe `release` y `hotfix`
- **`pruebas`** — branch de pruebas continuas (P1…PN)
- **`develop`** — integración de features antes de release
- **Feature branches** — `WorkstationDraftImplementation`, `WorkstationPartImplementation`, `ExplorerImplementation`, etc.
- **`VoskImplementation`** (también llamado "DAVCore") — implementación del motor de voz
- **`DAVGUI`** — implementación de la interfaz gráfica
- **`HotFix0.x`** — correcciones urgentes sobre `main`

Convención de commit en feature branches: `Vv1`, `Vv2`, `VvDoc`, `VvN` / `Gv1`, `Gv2`, etc.

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
- **Rama de trabajo actual:** `pruebas`
- **Destino del PR:** rama `pruebas` del repositorio central (`DAv-Project-Team-UADER/DAV`)

> Nunca hacer PR directo a `main` ni a `develop`. Todo pasa primero por `pruebas`.

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

El modelo español pequeño está en `MODELO/vosk-model-small-es-0.42.zip` (39 MB, Apache 2.0).  
Para reconocimiento de mayor precisión existe `vosk-model-es-0.42` (1.4 GB).  
La integración con micrófono requiere **PyAudio** (`MODELO/PyAudio-0.2.14.tar.gz`).

---

## Licencias relevantes

| Componente | Licencia |
|---|---|
| FreeCAD (núcleo) | LGPL-2.1-or-later |
| Código DAV propio | GPL-3.0 |
| Vosk | Apache 2.0 |
| PyAudio | MIT |
| PySide6 | LGPL-3.0 |
