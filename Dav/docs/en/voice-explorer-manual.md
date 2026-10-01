# Quick manual — Explorer by voice

## How it works

DAV navigates by **levels**, like a menu. You say one word to **enter** a submenu,
and another to **run** a command. You are always standing in a context, and only
the words of that context are recognized.

```
Base  →  explorador  →  archivo  →  guardar
         (enter)        (enter)     (run)
```

## Navigation commands (work in any context)

| To | Say |
| --- | --- |
| Go up one level | **subir** (go up), volver, atrás, salir, regresar, retroceder |
| See where you are and what you can say | **contexto** (context), dónde estoy, qué puedo decir, opciones disponibles, ubicación |

> If you get lost, say **«contexto»** — it lists the submenus and commands
> available at the current level.

These words are not hardcoded: they live in `Dav/dic/NavCommands/`, so synonyms can
be added without touching `browser.py`.

## Entering the Explorer

From Base, say: **«explorador»** (explorer)

## Explorer submenus

| Submenu | Words to enter |
| --- | --- |
| Files | **archivo**, archivos, carpeta, carpetas, folios |
| Edit | **editar**, edición, modificar, alterar |
| Print | **imprimir**, impresión, pdf, exportar pdf, generar pdf, impresora |
| Windows | **ventanas**, ventana |
| Expressions | **expresiones**, expresión |
| Tools | **herramientas**, utilidades |
| Structure | **estructura**, barra de estructura |
| Examples | **ejemplos**, quiero aprender, aprender, tutoriales |

## Direct commands (without entering any submenu)

While in `explorador`, these run directly:

- **refrescar** / recargar / actualizar (refresh)
- **captura** / foto / sacar foto / captura de pantalla / guardar pantalla (screenshot)
- **documento** / texto / documento de texto (text document)
- **desvincular** / desenlazar / quitar enlace (unlink)
- **congelar** / bloquear / inmovilizar (freeze)
- **variables** / conjunto de variables / set de variables (variable set)
- **todas las instancias** / seleccionar instancias (all instances)

## Commands inside each submenu

**archivo** (file) → nuevo · abrir · guardar · guardar como · guardar copia ·
revertir · combinar · importar · exportar · recientes · cargar imagen

**proyecto** (project) → nuevo · abrir · guardar · exportar · impresión 3D (no native dialogs; see below)

**editar** (edit) → deshacer · rehacer · cortar · copiar · pegar · duplicar ·
seleccionar todo · eliminar · posición · transformar · alinear · preferencias ·
propiedades · enviar a python · modo edición

**imprimir** (print) → imprimir · impresora · pdf

**ventanas** (windows) → cerrar · cerrar todo · salir

**expresiones** (expressions) → copiar documento · copiar todo · copiar selección ·
pegar expresión

**herramientas** (tools) → medir · medir distancia · limpiar selección · modo demo ·
personalizar · editar parámetros · utilidades de proyecto

**estructura** (structure) → pieza · grupo · enlace

All submenus also accept **ayuda** (help) / información / opciones.

## Project: open, save and export by voice

`archivo` uses FreeCAD's native dialogs, which cannot be driven by voice.
`proyecto` does the same thing with voice windows (`Dav/dic/Explorer/Proyecto/`):

- **abrir** (open) → walks through the folders: *siguiente* (next) / *anterior*
  (previous) move the selection, *abrir* enters the chosen folder, *subir* goes to
  the parent folder, *okey* picks the file, *cancelar* exits. It starts in the
  active document's folder or the last one used.
- **guardar** (save) → if the document already has a file, it saves there. If it is
  new, it asks for the folder (the suggested one or another, chosen with the same
  browser, where *okey* picks the folder you are in) and the name (the suggested one
  or one spelled out). If the file exists it asks for *sobrescribir* (overwrite).
- **exportar** (export) → picks the format (STEP, IGES, STL, OBJ, DXF; with
  *arriba*/*abajo* and *okey*), then folder and name as in save. It exports the
  selection or, if there is none, everything visible.

- **nuevo** (new) → creates an empty project (equivalent to «nuevo» in `archivo`).
- **impresión 3D** (3D printing; also «impresión tres de», «preparar impresión») →
  like *exportar*, but with the formats that 3D-printing programs read (3MF, STL,
  OBJ) and only with **solid** parts: a sketch or a TechDraw sheet cannot be
  printed. If the name is not accepted as is, it is spelled out. When finished it
  reports the dimensions of what was exported.

File names cannot be dictated (they are not in Vosk's vocabulary): that is why the
list is browsed instead of saying them.

## Examples: learn by doing

Inside **ejemplos** (examples; the folder has no icon) there are two options:

| Option | Words | What it does |
| --- | --- | --- |
| User manual | **manual**, referencia | Opens the PDF in your language: `Manual_Usuario.pdf` in Spanish; `User_Manual.pdf` in English; `Manual_do_Usuario.pdf` in Portuguese |
| Examples | **ejemplos**, demostraciones, tutorial | Opens a selector with the guided examples |

Guided examples:

| Example | What you do | Dimensions |
| --- | --- | --- |
| **Sketch** (Croquis) | A circle with a radius constraint | 2D dimension |
| **Draft** | Rectangle, circle and polygon | 2D dimension |
| **House** (Casa) | A house using only 2D shapes with dictated dimensions (body, roof, door, windows, chimney); you learn to trim one shape with another | Lines by points and «modificar → cortar» (modify → trim) |
| **Label** (Rótulo) | A simple label with text in Draft | — |
| **TechDraw** | A circle on a sheet with its title block | — |
| **PartDesign** | A screw: shank, tip, head, chamfer and thread | 3D dimension and «tres de» (3D) view |
| **Die** (Dado) | A 20 mm die: the 1 face with a cylinder and the other five with a sketch and a pocket each | 3D dimension, the six views and «tres de» |
| **M6 flat washer** | A sketch with the hole (Ø 6.4) and the edge (Ø 12), extruded 1.6 mm in PartDesign and placed on a TechDraw sheet with an isometric view, a view of the sketch and the text «M6 arandela» | Diameter constraint and 2D dimension |
| **Bolt-nut** (Bulón-tuerca) | An M6 hex-head bolt (simplified from DIN 931) and its nut, made in PartDesign, inserted by voice into an assembly, with the bolt anchored and a cylindrical joint that brings the nut onto the axis through the faces you choose | Assembly with cylindrical joint and «tres de» view |
| **5-piece scissors** (Tijera de 5 piezas) | Two blades (extruded triangle with tab and holes), two handles (rings) and a stepped pivot, made in PartDesign and joined in an assembly with hinges and fixed joints. The version open at 50 % and the ANSI B drawing are in [voice-scissors-guide.md](voice-scissors-guide.md) | Assembly with hinge, fixed joints and «tres de» view |

Decimals are dictated with «punto» (point) in all three languages: «uno punto uno
uno» is 1.11. In Spanish «coma» (comma) is equivalent («uno coma uno uno»). Numbers
from 0 to 99 are said naturally («treinta y dos»); from 100 on, digit by digit
(«uno cero cero»).

The selector is driven with **retroceder** (back), **avanzar** (forward) and
**enviar** (send). Once the example is chosen, a window appears (it does not block
FreeCAD, so you can see how the part is built) that shows one **frame** at a time
with **what you would say to do it in DAV**: the path through the menus and then
the values dictated in the dialogs. When you say it all, in order, the action runs
and it moves on to the next frame.

For example, to draw a circle of radius 12 in a sketch:

```
banco → croquis → nuevo → enviar          (picks the XY plane)
geometría → círculo → círculo             (enters Geometry and Circle, and creates it)
cero → enviar → cero → enviar → doce → enviar     (center X, center Y and radius)
```

Each word or phrase on the path is a command; each value is confirmed with
**enviar**. What is dictated depends on the document: for example, in the Die, how
many times to say **abajo** (down) to reach a face in the list comes from the faces
the solid has at that moment (the window groups the repetitions: «abajo ×5»).

- **retroceder / avanzar**: review frames already done.
- **saltar** (skip): runs the frame without saying its words (useful if the
  microphone does not recognize it).
- **cancelar**: closes the example. When finished, **enviar** closes it.

Each example is the `steps()` functions in `Dav/dic/Explorer/Examples/_*.py`;
to add one, create a module with `TITLE` and `steps()` and add it to `_EXAMPLES` in `_demos.py`.

The words in each frame are checked against the real tree, in all three languages,
with `tests/verify_examples_paths.py` (see [`testing.md`](development/testing.md)): if the
dictionary changes and an example stops matching, that test flags it.

## Corrections by voice (from any context)

They live in the root dictionary (`Dav/dic/Correction/`), so they are said without
entering any submenu:

| To | Say |
| --- | --- |
| Undo | **deshacer**, deshacer cambio, deshacer último |
| Redo | **rehacer**, rehacer cambio |
| Delete the last created object | **borrar último**, eliminar último, quitar último |
| Delete a chosen object | **borrar objeto**, eliminar objeto, quitar objeto |
| Clean up objects with errors | **borrar rotos**, limpiar rotos, limpiar errores |

Deleting always **asks for confirmation by voice** and cannot be undone from here.
These are also said from anywhere: **medir** / cota / acotar (measure / dimension;
creates a dimension), the standard views with zoom (**frontal**, **arriba**,
**acercar**, **ajustar todo**…), **mover vista**, **minimizar** / **maximizar**
(the DAV panel) and **preferencias**.

## Complete examples

Save the file:

```
"explorador" → "archivo" → "guardar"
```

Export to PDF:

```
"explorador" → "imprimir" → "pdf"
```

Undo a change:

```
"explorador" → "editar" → "deshacer"
```

Take a screenshot (direct command, no submenu):

```
"explorador" → "captura"
```

## Tips

- **You do not need to go up to switch main menu**: from any level you can say
  «banco de trabajo» (workbench), «vista estándar» (standard view), etc. and it
  jumps straight there.
- **Accents do not matter**: «impresión» and «impresion» are recognized the same
  (the engine normalizes accents and eñes before comparing).
- **Avoid English words** (`sketcher`, `draft`, `techdraw`): the voice model is
  Spanish and recognizes them poorly. Always use the Spanish synonyms.
- If a word is not understood, try a synonym from the list — almost every command
  has two or three.

## Where this vocabulary comes from

All the words in this manual come from the real dictionaries:

- `Dav/dic/Explorer/TraduceToEs.py` — submenus and direct commands
- `Dav/dic/Explorer/<Submenu>/TraduceToEs.py` — commands of each submenu
- `Dav/dic/NavCommands/TraduceToEs.py` — subir / contexto

If synonyms are added there, this manual becomes outdated: it should be
regenerated from those files.

The **user manual in PDF** (`Manual_Usuario.pdf`, `User_Manual.pdf` and
`Manual_do_Usuario.pdf`, at the repository root) does regenerate itself: it reads
the real dictionaries (groups, commands, phrases in each language and icons) with
`python Dav/docs/manual/build_manual.py`. To add a function, just write its
description in `Dav/docs/manual/desc_*.py` and regenerate it; the script reports
which commands still lack a description.
