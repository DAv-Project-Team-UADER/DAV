# Test guide — from a square to an assembly, by voice

This guide covers what was added in PRs **#208**, **#209** and **#213**: creating
geometry by dictating dimensions, extruding it to 3D and joining parts with joints — all without
FreeCAD dialogs.

Every phrase in this guide is taken from the real dictionaries
(`Dav/dic/`). None is made up.

---

## Before you start

- Open FreeCAD with the DAV panel, **Spanish** language.
- Have a new document open.
- If you get lost: say **`donde estoy`** (where am I) — it lists the current context and the
  available options.
- To go up a level: **`subir`** (also `volver`, `atras`).

**Confirming a value** (after each number):
`enter` · `enviar` · `aceptar` · `confirmar` · `ok`

**Aborting a pop-up**: `cancelar`

### Numbers: 0–99 are said normally, from 100 on they are spelled out

They are pronounced naturally up to 99: 0–30 directly, plus the tens (40, 50, 60, 70,
80, 90) and compounds (`treinta y cinco` = thirty-five).

From 100 on you must **spell digit by digit**: `uno cero cero` gives
100, `tres seis cero` gives 360. It works, but it is awkward — see
[voice-numbers-limits-and-proposal.md](voice-numbers-limits-and-proposal.md).

The tests in this guide use values under 100 so the phrases sound
natural.

Other modifiers:

| To say | Say |
|---|---|
| −20 | `menos veinte` (minus twenty) |
| 12.5 | `doce coma cinco` (twelve point five) |

---

## How to report

For each test, write down:

1. **What you said** (the exact phrase).
2. **What came out in the Report View** — all commands print there, both
   success and error.
3. **Whether the object appeared in the tree** of the DAV panel.

---

## Test 1 — Direct cube

The quickest one. It confirms that navigation, the pop-up and the numbers work.

| Say | What happens |
|---|---|
| `banco de trabajo` (workbench) | enters the workbenches |
| `diseño de pieza` (part design) | enters PartDesign |
| `aditivo` (additive) | enters the additive operations |
| `caja por medidas` (box by size) | **opens the pop-up** |
| `veinte enter` | length |
| `veinte enter` | width |
| `veinte enter` | height |

**Expected**: a 20×20×20 cube and in the Report View:
`[additive] Created box 20 x 20 x 20`

> If this test fails, the problem is navigation or number recognition. Do not
> continue with the others until it is resolved.

---

## Test 2 — Cylinder

From `aditivo`:

| Say | What happens |
|---|---|
| `cilindro por medidas` (cylinder by size) | opens the pop-up |
| `diez enter` | radius |
| `cuarenta enter` | height |

**Expected**: cylinder r=10, h=40.

---

## Test 3 — The full flow: square → cube

**This is the main test.** It closes the 2D → 3D path without a mouse.

### Step A — draw the square

| Say | What happens |
|---|---|
| `banco de trabajo` | |
| `croquis` (sketch) | enters Sketcher |
| `geometria` (geometry) | enters the geometries |
| `rectangulo` (rectangle) | enters the rectangle submenu |
| `rectangulo por esquinas` (rectangle by corners) | **opens the pop-up** |
| `cero enter` | x1 |
| `cero enter` | y1 |
| `veinte enter` | x2 |
| `veinte enter` | y2 |

**Expected**: a 20×20 square and
`[geometry.rectangle] Created 'Rectangle' from (0,0) to (20,20)`

### Step B — select it

Click the rectangle (in the object tree or in the 3D view).

> This step **still needs the mouse**. Voice selection exists, but it is a
> different flow.

### Step C — extrude it

| Say | What happens |
|---|---|
| `subir` (up to the workbench level) | |
| `diseño de pieza` | |
| `aditivo` | |
| `extruir por medida` (extrude by size) | **opens the pop-up** |
| `treinta enter` | height |

**Expected**: the square becomes a 20×20×30 prism and
`[additive] Padded '...' by 30`

> **The most important step to test.** Internally the square (a
> `Part::Feature`) is converted to a sketch so it can be extruded. That conversion
> was only validated with stubs, never inside FreeCAD.

---

## Test 4 — Revolution

With a 2D profile selected, from `aditivo`:

| Say | What happens |
|---|---|
| `revolucion por angulo` (revolution by angle) | opens the pop-up |
| `noventa enter` | angle in degrees |

**Expected**: a 90° solid of revolution.

---

## Test 5 — Other 2D geometries

From `croquis` → `geometria`:

| Shape | Say | Example values |
|---|---|---|
| Circle | `circulo` → `circulo por centro` | `cero` / `cero` / `veinticinco` |
| Arc | `arco` → `arco por centro` | `cero` / `cero` / `veinticinco` / `cero` / `noventa` |
| Ellipse | `elipse` → `elipse por centro` | `cero` / `cero` / `cuarenta` / `veinte` |
| Polygon | `poligono` → `poligono por lados` | `seis` / `cero` / `cero` / `veinticinco` |
| Line | `linea` → `linea por puntos` | `cero` / `cero` / `treinta` / `treinta` |

---

## Test 6 — Assembly with joints

| Say | What happens |
|---|---|
| `banco de trabajo` | |
| `ensamblaje` (assembly) | enters Assembly |
| `crear ensamblaje` (create assembly) | creates the assembly |
| `insertar vinculo` (insert link) | opens a list of the bodies: `avanzar` to change, `enviar` to pick. The link is placed to the right of those already inserted (repeat to have two) |
| `insertar pieza` (insert part) | inserts a new, empty part |

With **one part** (picked from a list: `avanzar` and `enviar`):

| Say | Expected |
|---|---|
| `anclar pieza` (ground part) | `[assembly] Grounded '...'` |

With **two parts** (picked in two lists in a row) and then **where each one is joined**: a list of faces that you walk through with `abajo` and pick with `enviar` (first the cylinders, by their axis, and then the flat faces from largest to smallest):

| Say | Then | Expected |
|---|---|---|
| `junta por distancia` (distance joint) | `veinticinco enter` | `Held '...' and '...' 25 apart` |
| `junta por angulo` (angle joint) | `noventa enter` | `Held '...' and '...' at 90 degrees` |
| `ensamble fijo` (fixed joint) | — | `Fixed '...' to '...'` |
| `bisagra` (hinge) | — | `Hinged '...' to '...'` |
| `junta deslizante` (slider joint) | — | `Slider between '...' and '...'` |

**Joints without dimensions** (two parts and where each one is joined):

| Say | What it does |
|---|---|
| `rotula` (ball joint) | free in any rotation |
| `junta de cilindro` (cylinder joint; or `junta cilindrica`) | rotates and slides on an axis |
| `junta paralela` (parallel joint) | keeps the parts parallel |
| `junta perpendicular` (perpendicular joint) | keeps the parts at a right angle |

**Transmission joints** (two parts and where each one is joined; they ask for radii):

| Say | Then | What it does |
|---|---|---|
| `junta de engranajes` (gear joint) | `veinte` / `diez` | meshes with that ratio |
| `junta de correa` (belt joint) | `treinta` / `quince` | pulleys joined by a belt |
| `junta de tornillo` (screw joint) | `cinco` | thread advance |
| `junta de cremallera` (rack joint) | `diez` | rack and pinion |

To verify the solver runs: `resolver ensamblaje` (solve assembly).

> The parts and the place where each one is joined are chosen by voice. Only cylinders and flat faces are offered: single edges or vertices cannot be chosen.

---

## Test 7 — Errors must report

These paths are implemented but **were not tested inside FreeCAD**.
Confirm that the message appears in the Report View:

| Test | How | Expected message |
|---|---|---|
| Zero radius | `circulo por centro` → `cero`/`cero`/`cero` | `radius must be greater than zero` |
| Impossible polygon | `poligono por lados` → `dos` | `a polygon needs at least 3 sides` |
| Box with a zero side | `caja por medidas` → `veinte`/`cero`/`veinte` | `every dimension must be greater than zero` |
| Joint without selection | `ensamble fijo` without selecting anything | `select two parts to join first` |
| Cancel | in any pop-up say `cancelar` | `Command cancelled by user` |
| Negatives | `menos veinte enter` | accepts −20 |
| Decimals | `doce coma cinco enter` | accepts 12.5 |

---

## Test 8 — The object tree bug

Verifies a specific fix: before, ellipses and polygons created by voice
**did not appear in the tree** of the DAV panel.

1. Create an **ellipse** (test 5).
2. Create a **polygon**.
3. Look at the object tree in the DAV panel.

**Expected**: both appear in the tree. If they do not, the fix did not work.

---

## Test 9 — The other languages

Three modules had dictionaries that failed silently: the loader isolates the broken
module and continues with an empty map, so the phrases simply did not
respond, with no visible error.

Change the panel language and test that they respond:

| Language | Phrase | Should |
|---|---|---|
| English | `box by size` | open the box pop-up |
| English | `line by points` | open the line pop-up |
| Portuguese | `caixa por medidas` | open the box pop-up |
| Portuguese | `junta fixa` | create a fixed joint |

The English PartDesign ones and **all of Assembly in Portuguese** were down
before these changes.

---

## Where it is most likely to fail

None of this was run inside FreeCAD: it was validated with stubs, which confirm
the phrase routing, the math and that the dictated values reach the correct
properties — but not the interaction with live FreeCAD.

The three highest-risk points:

1. **Step C of test 3** — the conversion from square to sketch.
   `addGeometry` with real curves may behave differently than with the stub.
2. **The joints of test 6** — `Vertex1` of each part is used as the default
   anchor point; with complex shapes it may not be the expected point.
3. **The whole navigation chain** — that
   `banco de trabajo` → `diseño de pieza` → `aditivo` works end to end with
   real voice recognition, not just in the dictionary.
