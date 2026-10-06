# Guide — a 5-piece pair of scissors, from voice to ANSI drawing

How to draw a scissors assembly (2 blades, 2 handles and 1 pivot bolt) by voice in DAV and
put it on a technical drawing with an ANSI title block, with a side view (scissors open at 50 %,
with a symmetry axis) and an isometric view (scissors closed).

![Finished drawing](../ejemplo-tijeras/tijeras_dav.png)

Files to compare with your result, in [ejemplo-tijeras/](../ejemplo-tijeras/):

| File | What it is |
|---|---|
| `tijeras_dav.FCStd` | the complete model (5 bodies, 2 assemblies, drawing) |
| `tijeras_dav.pdf` / `.png` | the exported drawing |
| `crear_tijeras.py` | builds all of the above with the FreeCAD API, using the same values as this guide |

> **What is tested and what is not.** The values, joints and «avanzar» (next) counts in this guide
> come from running the real DAV functions (`_InsertLink`, `_CreateJoint`, `listConnectors`) and
> the FreeCAD 1.1 solver: the model converges and there are no interferences except the
> blade/handle clamp, which is intentional. **Voice recognition was not tested.** The phrases
> are taken from the dictionaries in `Dav/dic/`. The TechDraw part (phase 4) is now
> done by voice; only the title block keeps mouse steps (🖱).

> **Also as a guided example inside DAV:** `explorador` → `ejemplos` → `ejemplos` → *Tijera de 5 piezas* (5-piece scissors). It covers the 5 parts and the closed assembly (phases 1 and 2); the open scissors and the drawing are only in this guide.

## Before you start

- FreeCAD with the DAV panel, **Spanish** language, new empty document.
- If you get lost: **`contexto`** (context). To go up a level: **`subir`** (go up). To abort a pop-up: **`cancelar`** (cancel).
- Each value is said and confirmed with **`enter`** (`ochenta enter` = eighty enter). Negatives: `menos diez` (minus ten).
  Decimals: `uno coma ocho` (one point eight). Numbers from 0 to 99 are said normally (all of them in this guide).
- In lists (bodies, parts, drawings) you start at the first item: **`avanzar`** moves to the
  next one and **`enviar`** (send) picks. «Avanzar ×3» = say it three times and then `enviar`.
- `subir ×N` means saying `subir` N times. `banco de trabajo` (workbench) only works from the main menu.

## The model

The scissors lie in the XY plane; the pivot bolt is the Z axis. Dimensions in mm.

| # | Part | What it is like |
|---|---|---|
| 1 | Blade A | triangle (80,0) (−10,−16) (−26,14) extruded 2; Ø20 tab at (−32,18); Ø4 bolt hole; Ø16 hole in the tab |
| 2 | Blade B | mirror of A in Y: (80,0) (−10,16) (−26,−14); tab at (−32,−18); bolt hole **Ø3.6** |
| 3 | Handle A | Ø28 × 4 ring at (−32,18), Ø16 hole |
| 4 | Handle B | same, at (−32,−18) |
| 5 | Bolt | head Ø10 × 2, shaft Ø4 × 2 (blade A), shaft Ø3.6 × 2 (blade B) |

Why this way: the **bolt is stepped** (Ø4 and Ø3.6) so the assembly stacks blade B alone
2 mm above A without asking you for any position joint. The **Ø16 holes** of blade and handle are
cylinders on the same axis: the blade↔handle fixed joint is made on them.

Opening: maximum 60°, so 50 % = 30° (each blade ±15° with respect to the X axis). It is achieved with a
distance joint between the handles: **23.3 mm** gap (closed it is 8).

## Phase 1 — the 5 parts

Blade A:

| # | Say | What happens |
|---|---|---|
| 1 | `banco de trabajo` → `croquis` → `geometria` → `triangulo` → `triangulo por vertices` | 6-value pop-up |
| 2 | `ochenta enter` `cero enter` `menos diez enter` `menos dieciseis enter` `menos veintiseis enter` `catorce enter` | blade A triangle |
| 3 | `subir ×3` → `diseño de pieza` → `aditivo` → `extruir por medida` | list of drawings |
| 4 | `enviar` · `dos enter` | body 1 (blade A) is created |
| 5 | `cilindro por medidas` · `diez` `dos` `menos treinta y dos` `dieciocho` `uno` (each with `enter`) · `no` · `enviar` | tab, added to body 1 |
| 6 | `subir` → `cortar` → `cortar cilindro por medidas` · `dos` `diez` `cero` `cero` `uno` · `enviar` | bolt hole |
| 7 | `cortar cilindro por medidas` · `ocho` `diez` `menos treinta y dos` `dieciocho` `uno` · `enviar` | tab hole |

Blade B (body 2):

| # | Say | What happens |
|---|---|---|
| 8 | `subir ×2` → `croquis` → `geometria` → `triangulo` → `triangulo por vertices` · `ochenta` `cero` `menos diez` `dieciseis` `menos veintiseis` `menos catorce` | blade B triangle |
| 9 | `subir ×3` → `diseño de pieza` → `aditivo` → `extruir por medida` · **`avanzar ×2`** (the last in the list) · `enviar` · `dos enter` | body 2 |
| 10 | `cilindro por medidas` · `diez` `dos` `menos treinta y dos` `menos dieciocho` `uno` · `no` · `avanzar` · `enviar` | tab |
| 11 | `subir` → `cortar` → `cortar cilindro por medidas` · `uno coma ocho` `diez` `cero` `cero` `uno` · `avanzar` · `enviar` | bolt hole (Ø3.6) |
| 12 | `cortar cilindro por medidas` · `ocho` `diez` `menos treinta y dos` `menos dieciocho` `uno` · `avanzar` · `enviar` | hole |

Handles and bolt (each «new body» is `si` (yes)):

| # | Say | What happens |
|---|---|---|
| 13 | `subir` → `aditivo` → `cilindro por medidas` · `catorce` `cuatro` `menos treinta y dos` `dieciocho` `uno` · `si` | body 3 (handle A) |
| 14 | `subir` → `cortar` → `cortar cilindro por medidas` · `ocho` `diez` `menos treinta y dos` `dieciocho` `uno` · **`avanzar ×2`** · `enviar` | hole |
| 15 | `subir` → `aditivo` → `cilindro por medidas` · `catorce` `cuatro` `menos treinta y dos` `menos dieciocho` `uno` · `si` | body 4 (handle B) |
| 16 | `subir` → `cortar` → `cortar cilindro por medidas` · `ocho` `diez` `menos treinta y dos` `menos dieciocho` `uno` · **`avanzar ×3`** · `enviar` | hole |
| 17 | `subir` → `aditivo` → `cilindro por medidas` · `cinco` `dos` `cero` `cero` `menos uno` · `si` | body 5: bolt head |
| 18 | `cilindro por medidas` · `dos` `dos` `cero` `cero` `uno` · `no` · **`avanzar ×4`** · `enviar` | blade A shaft |
| 19 | `cilindro por medidas` · `uno coma ocho` `dos` `cero` `cero` `tres` · `no` · **`avanzar ×4`** · `enviar` | blade B shaft |

Order of the bodies in the lists: 1 blade A, 2 blade B, 3 handle A, 4 handle B, 5 bolt
(the panel shows them as `Body`, `Body001`…).

## Phase 2 — closed assembly

One assembly per scissors state: this way each TechDraw view uses a single source object.

| # | Say | List that appears |
|---|---|---|
| 20 | `subir ×2` → `ensamblaje` → `crear ensamblaje` | the new assembly becomes active |
| 21 | `insertar vinculo` | bodies: `enviar` (blade A) |
| 22 | `insertar vinculo` · `avanzar` · `enviar` | blade B |
| 23 | `insertar vinculo` · `avanzar ×2` · `enviar` | handle A |
| 24 | `insertar vinculo` · `avanzar ×3` · `enviar` | handle B |
| 25 | `insertar vinculo` · `avanzar ×4` · `enviar` | bolt |
| 26 | `anclar pieza` · `avanzar ×9` · `enviar` | the bolt link (5 bodies + 4 links before it) |
| 27 | `bisagra` | 1st list `avanzar ×9` `enviar` (bolt); 2nd `avanzar ×5` `enviar` (blade A). Faces: bolt `abajo` `enviar` (Ø4 cylinder); blade A `abajo ×2` `enviar` (Ø4 cylinder) |
| 28 | `bisagra` | 1st `avanzar ×9` `enviar`; 2nd `avanzar ×6` `enviar` (blade B). Faces: bolt `abajo ×2` `enviar` (Ø3.6); blade B `abajo ×2` `enviar` |
| 29 | `ensamble fijo` | 1st `avanzar ×5` `enviar` (blade A); 2nd `avanzar ×6` `enviar` (handle A). Faces: `abajo` `enviar` on each (Ø16 hole) |
| 30 | `ensamble fijo` | 1st `avanzar ×6` `enviar` (blade B); 2nd `avanzar ×7` `enviar` (handle B). Faces: `abajo` `enviar` on each |
| 31 | `resolver ensamblaje` | blade B rises 2 mm; everything snaps together |

In steps 27–30 the face list shows the cylinders first (from largest to smallest area):
if the panel says «Cilindro de radio 8» (cylinder of radius 8) it is the hole, «radio 2» the bolt one.

## Phase 3 — assembly open at 50 %

Same steps with **another assembly**. The part lists now include the 5 links of the
closed one, so the numbers go up by 5:

| # | Say | Result |
|---|---|---|
| 32 | `crear ensamblaje`, and 5 times `insertar vinculo` as in 21–25 | 5 new links |
| 33 | `anclar pieza` · `avanzar ×14` · `enviar` | bolt anchored |
| 34 | `bisagra` | 1st `avanzar ×14`; 2nd `avanzar ×10` (blade A); faces as in 27 |
| 35 | `bisagra` | 1st `avanzar ×14`; 2nd `avanzar ×11` (blade B); faces as in 28 |
| 36 | `ensamble fijo` | 1st `avanzar ×10`; 2nd `avanzar ×11`; faces as in 29 |
| 37 | `ensamble fijo` | 1st `avanzar ×11`; 2nd `avanzar ×12`; faces as in 30 |
| 38 | `junta por distancia` · `veintitres coma tres enter` | 1st list `avanzar ×12` `enviar` (handle A); 2nd `avanzar ×12` `enviar` (handle B); faces: `enviar` on both (Ø28 outer cylinder) |
| 39 | `resolver ensamblaje` | the scissors open ±15° |

If DAV warns about «2 assemblies in the document», double-click (🖱) the assembly you want
to use to activate it and repeat the command.

## Phase 4 — ANSI B drawing (ASME Y14.1, 17×11 in)

Third-angle projection (ASME Y14.3 standard, the usual one in the US). ANSI B title block from the
`ASME/ANSIB_Landscape.svg` template.

| # | Say / do | What happens |
|---|---|---|
| 40 | `subir` up to the main menu → `banco de trabajo` → `dibujo tecnico` → `pagina` → `plantilla` | opens the file browser |
| 41 | `abrir` (enters `ASME`) · `siguiente ×5` · `okey` | page with `ANSIB_Landscape.svg` |
| 42 | `subir` → `vistas` → `vista de objeto` · in the object list: **`buscar por deletreo`** → spell `te i jota e erre a` `espacio` `a be i e erre te a` (Tijera abierta, open scissors) · `okey` · `okey` | the box jumps to the closest object; `okey` picks it |
| 43 | The same command's questions follow: direction `superior` · scale `uno coma veinticinco enter` · X `uno cero cinco enter` · Y `uno seis cero enter` (hundreds are said digit by digit) | side view |
| 44 | `vista de objeto` · `buscar por deletreo` → `Tijera cerrada` (closed scissors) · `okey` · `isometrica` · `uno coma veinticinco enter` · `tres dos cinco enter` · `uno seis cero enter` | isometric view |
| 45 | `proyeccion de pagina` · `tercer angulo` | third angle |
| 46 | **Symmetry axis:** `lineas` → `eje de simetria` · view (`avanzar`/`okey`) · `horizontal` · `origen` | center line through the bolt, on the X axis |
| 47 | Overall dimensions: `cotas` → `extension` → `cotas totales` · view | length 117.56 and height 79.3 |
| 48 | Title block: `elementos` → `campos` fills in what comes from the document properties; the rest (title, number DAV-TJ-001, scale 5:4) is edited by double-clicking 🖱 | title block filled |
| 49 | `pagina` → `pdf` · folder and name by voice | PDF |

### Search by spelling

In any list of objects (views, assemblies, parts...), instead of saying `avanzar` a hundred times:

1. Say **`buscar por deletreo`** (`deletrear` or `buscar` is enough).
2. Spell the name letter by letter, with `espacio` between words and `borrar` to correct; `okey` closes.
3. The box jumps to the object that **most resembles it** (it tolerates the recognizer confusing
   neighboring letters such as be/de/pe/te) and names two other candidates. `okey` picks it; if it was not the one, repeat the search
   or continue with `avanzar`.

Outside a list, the same phrase selects the most similar object in the document (it asks you
«¿Es …?» (Is it …?) and you answer `si` or `no`).

### What still needs user review

- **Properties outside these commands** (for example changing only the scale of a view already created): `escala de vista`,
  `direccion de vista` and `posicion de vista` do it without going through the properties panel.
- The symmetry axis and the dimensions need the sheet in view; DAV opens it by itself, but if FreeCAD warns that it did not
  create the axis, open the page (double-click 🖱 in the tree) and repeat the command.
- These commands were verified by creating views, changing direction/scale/position/projection and overall dimensions in FreeCAD 1.1
  (headless, with simulated voice answers). **Voice recognition and drawing the axis (which requires the interface)
  were not tested.**

If you want to skip 42–49 and see the result, run `ejemplo-tijeras/crear_tijeras.py` with
`freecad.exe`: it generates the same drawing.

## Common problems

| Symptom | Cause and solution |
|---|---|
| «la figura no se pudo unir al cuerpo» (the shape could not be joined to the body) | the tab or the shafts do not touch the solid: check x, y, z |
| Blade B ends up on top of A in the same plane | the hinge with the Ø3.6 shaft is missing (step 28) |
| The open scissors come out inverted or tilted | repeat `resolver ensamblaje`; if it persists, delete the distance joint and recreate it |
| The lists show other numbers | count with the panel: `avanzar` until you see the right name |
