# Voice routes — Selection and object creation

Guide to testing the `Selection` module and the `CreateObjects` circuit by voice.
Phrases verified against the dictionaries in `Dav/dic/`.

---

## Route A — Create objects (triggers CreateObjects)

Exercises `CreateObjects` from `Dav/scr/selection/`, because every primitive in
`creation.py` invokes it when it finishes.

| Step | Say | Context |
|---|---|---|
| 1 | **"banco de trabajo"** (workbench) | `workbench` |
| 2 | **"borrador"** (draft) | `workbench > draft` |
| 3 | **"creacion"** (creation) | `draft > creation` |
| 4 | **"rectangulo"** (rectangle) | runs → `CreateObjects(...).Execute()` |

Other step-4 primitives: **"punto"** (point), **"poligono"** (polygon),
**"cuadrilatero"** (quadrilateral), **"dibujar rectangulo"** (draw rectangle),
**"marcar punto"** (mark point), **"dibujar poligono"** (draw polygon).

Each one calls `CreateObjects(ObjectName=..., Is3D=False).Execute()`
(`creation.py:31,38,45`), which is the path that goes through the `Tagger`.

Step-3 synonyms: creacion · creación · crear · crear objeto · primitivas.

---

## Route B — Navigate the selection

| Step | Say | Runs |
|---|---|---|
| 1 | **"seleccion"** (selection) | enters `selection` |
| 2 | **"siguiente"** (next) | `SelectNext()` |
| 3 | **"anterior"** (previous) | `SelectPrevious()` |
| 4 | **"todos"** (all) | `SelectAll()` |
| 5 | **"nada"** (none) | `DeselectAll()` |

Step-1 synonyms: seleccion · selección · seleccionar ·
seleccion de objetos · objetos.

Inside `selection` (these already existed in `Selection/TraduceToEs.py`):

- **next** — avanzar · otro · otra · pasar · siguiente · siguiente objeto ·
  objeto siguiente · siguiente elemento · seleccionar siguiente
- **previous** — retroceder · volver · anterior · anterior objeto ·
  objeto anterior · seleccionar anterior
- **selectall** — todos · todo · seleccionar todos · seleccionar todo ·
  seleccionar todos los objetos
- **deselectall** — nada · ninguno · ninguna · quitar · quitar todos ·
  desmarcar · desmarcar todo

Other leaves of the module: `current` (current object) and `count` (how many there are).

---

## Route C — Delete, search, paint and assign material

Besides walking through the selection, the module deletes, searches by name and
changes the appearance of what is selected, with no native dialogs (everything is
chosen by voice):

| To | Say | What it does |
|---|---|---|
| Delete the chosen object | **"borrar"** · "borrar objeto" · "eliminar" · "suprimir" | First **"siguiente"/"anterior"** until the object, then **"borrar"** |
| Search for an object by name | **"buscar por deletreo"** (search by spelling) · "deletrear" · "buscar objeto" | The name is spelled out and the closest match is selected |
| Paint | **"pintar objeto"** · "colorear objeto" · "cambiar color" · "poner color" | Short list of colors (rojo, naranja, amarillo, verde, celeste, azul, violeta, rosa, marrón, negro, blanco, gris: red, orange, yellow, green, light blue, blue, violet, pink, brown, black, white, gray) |
| Assign material | **"material de objeto"** · "poner material" · "elegir material" | Materials from the FreeCAD library (aluminio, acero, inoxidable, hierro, cobre, latón, bronce, titanio, oro, plata, PLA, ABS, plástico, acrílico, vidrio, madera: aluminium, steel, stainless, iron, copper, brass, bronze, titanium, gold, silver, PLA, ABS, plastic, acrylic, glass, wood); only the ones the installation has are offered |

- Color and material are applied to what is **selected**; if nothing is, choose
  first with **"siguiente"** or **"buscar por deletreo"**.
- In the color and material boxes, **"arriba"** (up) and **"abajo"** (down) move the
  selection, **"okey"** confirms it and **"cancelar"** exits without changing anything.
- **"borrar"** removes the object without asking for separate confirmation; to
  delete with voice confirmation use the global correction commands
  ("borrar objeto", "borrar último", "borrar rotos"; see the PDF manual).

Code: `Dav/dic/Selection/selection.py` and `_aspecto.py`.

---

## General navigation

Defined in `Dav/dic/NavCommands/TraduceToEs.py`, they work at any level:

| To | Say |
|---|---|
| Go up one level | **"subir"** · "atrás" · "salir" · "regresar" |
| See where you are | **"contexto"** · "dónde estoy" · "qué puedo decir" |
| Confirm | **"aceptar"** · "ok" · "confirmar" · "enviar" |
| Cancel | **"cancelar"** |

If you get lost, **"contexto"** lists what can be said at that point.

---

## Direct test from the Python console

Without going through voice, to isolate whether a problem is in the engine or in
the dictionary:

```python
import sys
sys.path.insert(0, r"C:\Users\Jose\Desktop\j\DAV\Dav\scr\selection")

from object_selection import ObjectSelection
sel = ObjectSelection()
sel.SelectAll()
sel.SelectNext()
print(sel.GetCurrentObject())
```

Creation + tagging circuit:

```python
import FreeCAD as App
from createobjects import CreateObjects

doc = App.ActiveDocument
CreateObjects(ObjectName=doc.ActiveObject.Name, Is3D=False).Execute()
```

---

## Translations added for this

The functions already existed; the entry phrases were missing, and without them
the submenu is unreachable by voice even though the dictionary works.

**`Dav/dic/TraduceToEs.py`** — `base.py` registered `"selection": selection`
but the root translation did not mention it: the whole module had no entry door.
The import and six phrases were added.

**`Dav/dic/Workbench/DraftWork/TraduceToEs.py`** — of the 14 submenus in
`DraftWork.py` only 11 were translated. `creation`, `drafting` and
`modification` were missing.

> When adding them, take care not to overwrite existing keys: `'modificar'` already
> pointed to `draft['modify']`, so `modification` ended up as `'modificaciones'`.
> A repeated key does not raise an error — the last one wins, silently.

Both fixes are already replicated in `TraduceToEn.py` and `TraduceToPT.py` (root and
`Workbench/DraftWork/`).
