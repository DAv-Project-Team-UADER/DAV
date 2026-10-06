# Test guide — PartDesign by voice

Covers the PartDesign commands that accept **dictated dimensions**: creating solids,
extruding profiles, cutting them and finishing them, without opening FreeCAD's dialogs.

All phrases are taken from the real dictionaries (`Dav/dic/`).

For the full flow from the 2D drawing and for Assembly, see
[voice-3d-testing-guide.md](voice-3d-testing-guide.md).

---

## Before you start

- FreeCAD with the DAV panel, **Spanish** language, new document open.
- If you get lost: **`donde estoy`** (where am I). To go up a level: **`subir`** (go up).
- **Confirming a value**: `enter` · `enviar` · `aceptar` · `confirmar` · `ok`
- **Aborting a pop-up**: `cancelar`

### Numbers: 0–99 are said normally, from 100 on they are spelled out

They are pronounced naturally up to 99: 0–30 directly, plus the tens (40, 50, 60, 70,
80, 90) and compounds (`treinta y cinco` = thirty-five).

From 100 on you must **spell them out**: `uno cero cero` gives 100. See
[voice-numbers-limits-and-proposal.md](voice-numbers-limits-and-proposal.md).

| To say | Say |
|---|---|
| −20 | `menos veinte` (minus twenty) |
| 12.5 | `doce coma cinco` (twelve point five) |

### How to get there

All the tests start with:

```
banco de trabajo → diseño de pieza
```

(workbench → part design) And from there you enter `aditivo` (additive), `sustractivo` (subtractive) or `modificar` (modify).

---

## What to expect from each command

| Category | Voice command | Prompts | What it does |
|---|---|---|---|
| Additive | `caja por medidas` (box by size) | 3 | box / cube |
| Additive | `cilindro por medidas` (cylinder by size) | 2 | cylinder |
| Additive | `extruir por medida` (extrude by size) | 1 | profile → solid |
| Additive | `revolucion por angulo` (revolution by angle) | 1 | profile → revolution |
| Additive | `esfera por radio` (sphere by radius) | 1 | sphere |
| Additive | `cono por medidas` (cone by size) | 3 | cone / frustum |
| Additive | `toro por medidas` (torus by size) | 2 | torus |
| Additive | `prisma por medidas` (prism by size) | 3 | regular prism |
| Subtractive | `vaciado por medida` (pocket by size) | 1 | pocket shaped like the profile |
| Subtractive | `agujero por medidas` (hole by size) | 2 | cylindrical hole |
| Subtractive | `ranura por angulo` (groove by angle) | 1 | groove by revolution |
| Subtractive | `cortar caja por medidas` (cut box by size) | 3 | subtracts a box |
| Subtractive | `cortar cilindro por medidas` (cut cylinder by size) | 2 | subtracts a cylinder |
| Subtractive | `cortar esfera por radio` (cut sphere by radius) | 1 | subtracts a sphere |
| Modify | `redondear por radio` (fillet by radius) | 1 | fillets all edges |
| Modify | `chaflan por medida` (chamfer by size) | 1 | chamfers all edges |
| Modify | `chaflan con angulo` (chamfer with angle) | 2 | chamfer with its own angle |
| Modify | `espesor por medida` (thickness by size) | 1 | hollows out leaving a wall |
| Transform | `patron lineal por medida` (linear pattern by size) | 2 | N copies in a line |
| Transform | `repetir cada` (repeat every) | 2 | N copies with spacing |
| Transform | `patron circular por medida` (circular pattern by size) | 2 | N copies in a circle |
| Transform | `escalar por factor` (scale by factor) | 2 | scales the solid |

---

## Test 1 — Cube

| Say | What happens |
|---|---|
| `banco de trabajo` → `diseño de pieza` → `aditivo` | |
| `caja por medidas` | opens the pop-up |
| `veinte enter` | length |
| `veinte enter` | width |
| `veinte enter` | height |

**Expected**: `[additive] Created box 20 x 20 x 20`

> Start here: if it fails, the problem is navigation or the numbers, not the
> commands.

---

## Test 2 — Cylinder

From `aditivo`:

| Say | What happens |
|---|---|
| `cilindro por medidas` | opens the pop-up |
| `diez enter` | radius |
| `cuarenta enter` | height |

**Expected**: `[additive] Created cylinder radius 10 height 40`

---

## Test 3 — Fillet the cube

With the cube from test 1 **selected** (click in the tree or the 3D view):

| Say | What happens |
|---|---|
| `subir` → `modificar` | enters the finishes |
| `redondear por radio` | opens the pop-up |
| `tres enter` | radius |

**Expected**: all edges rounded and
`[modify] Rounded '...' with radius 3`

> The radius must be **less than half the smallest side** of the solid. With a
> cube of 20, a radius of 3 works; one of 15 fails on recompute.

---

## Test 4 — Chamfer

With a solid selected, from `modificar`:

| Say | Then | Expected |
|---|---|---|
| `chaflan por medida` | `dos enter` | 2 mm chamfer at 45° |
| `chaflan con angulo` | `dos enter` / `treinta enter` | 2 mm chamfer at 30° |

**Expected**: `[modify] Chamfered '...' with size 2` (or `... at 30 degrees`).

---

## Test 5 — Hollow out

With a solid selected, from `modificar`:

| Say | What happens |
|---|---|
| `espesor por medida` | opens the pop-up |
| `dos enter` | wall thickness |

**Expected**: `[modify] Hollowed '...' leaving 2 of wall`

---

## Test 6 — Cut (subtractive)

These commands need a **2D profile selected**, just like `extruir`.

First draw a small square:

```
subir → croquis → geometria → rectangulo → rectangulo por esquinas
cero / cero / diez / diez
```

Select it, and from `diseño de pieza` → `sustractivo`:

| Say | Then | Expected |
|---|---|---|
| `vaciado por medida` | `diez enter` | `Pocketed '...' by 10` |
| `ranura por angulo` | `noventa enter` | `Grooved '...' by 90 degrees` |

For the hole, draw a circle and select it:

| Say | Then | Expected |
|---|---|---|
| `agujero por medidas` | `seis enter` / `veinticinco enter` | `Drilled a hole of diameter 6 and depth 25` |

---

## Test 7 — Full flow: square → cube → filleted

It chains everything. It is the test with the most value.

| Step | Say |
|---|---|
| 1 | `banco de trabajo` → `croquis` → `geometria` → `rectangulo` |
| 2 | `rectangulo por esquinas` → `cero`/`cero`/`veinte`/`veinte` |
| 3 | *(click the rectangle to select it)* |
| 4 | `subir` up to workbench → `diseño de pieza` → `aditivo` |
| 5 | `extruir por medida` → `treinta enter` |
| 6 | *(click the solid)* |
| 7 | `subir` → `modificar` → `redondear por radio` → `tres enter` |

**Expected**: a 20×20×30 prism with filleted edges.

> Steps 3 and 6 **still need the mouse**. Voice selection exists but it is a
> different flow.

---

## Test 8 — More primitives

From `aditivo`, each one opens its pop-up:

| Say | Values | Result |
|---|---|---|
| `esfera por radio` | `quince` | sphere r=15 |
| `cono por medidas` | `diez` / `cero` / `veinticinco` | pointed cone |
| `cono por medidas` | `diez` / `cinco` / `veinticinco` | truncated cone |
| `toro por medidas` | `veinte` / `cinco` | torus (ring 20, tube 5) |
| `prisma por medidas` | `seis` / `diez` / `treinta` | hexagonal prism |

> For the torus, the tube radius must be **smaller** than the ring radius, or the
> command warns and creates nothing.

---

## Test 9 — Subtract primitives

With a solid already created, from `sustractivo`:

| Say | Values | Result |
|---|---|---|
| `cortar caja por medidas` | `diez` / `diez` / `veinte` | subtracts a box |
| `cortar cilindro por medidas` | `cinco` / `veinte` | subtracts a cylinder |
| `cortar esfera por radio` | `ocho` | subtracts a sphere |

They are subtracted from the **last body created**.

---

## Test 10 — Patterns and scaling

With an operation selected (for example the hole from test 6), from
`transformar` (transform):

| Say | Values | Result |
|---|---|---|
| `patron lineal por medida` | `cinco` / `ochenta` | 5 copies spread over 80 mm |
| `repetir cada` | `cinco` / `veinte` | 5 copies, one every 20 mm |
| `patron circular por medida` | `seis` / `trescientos sesenta`* | 6 copies in a full circle |
| `escalar por factor` | `dos` / `dos` | doubles the size |

\* **Note**: 360 cannot be pronounced as a word; it has to be spelled out:
`tres seis cero enter`. It works, but it is awkward — it is documented in
[voice-numbers-limits-and-proposal.md](voice-numbers-limits-and-proposal.md).

> The difference between the two linear patterns: `patron lineal por medida`
> spreads the copies along the dictated **total**; `repetir cada` uses the
> value as the **spacing between copies**.

---

## Test 11 — Errors must report

Implemented but **not tested inside FreeCAD**. Confirm that the message
appears in the Report View:

| Test | How | Expected message |
|---|---|---|
| Box with a zero side | `caja por medidas` → `veinte`/`cero`/`veinte` | `every dimension must be greater than zero` |
| Negative radius | `redondear por radio` → `menos uno` | `radius must be greater than zero` |
| Zero chamfer | `chaflan por medida` → `cero` | `size must be greater than zero` |
| Impossible angle | `chaflan con angulo` → `dos` / `doscientos` | `angle must be between 0 and 180` |
| No selection | `redondear por radio` without selecting anything | `select the solid to round first` |
| Cancel | `cancelar` in any pop-up | `Command cancelled by user` |

---

## Test 12 — The other languages

PartDesign had three folders with dictionaries that failed silently: the
loader isolates the broken module and continues with an empty map, so the phrases
simply did not respond, with no visible error.

| Language | Phrase | Should |
|---|---|---|
| English | `box by size` | open the box pop-up |
| English | `fillet by radius` | open the fillet pop-up |
| Portuguese | `caixa por medidas` | open the box pop-up |
| Portuguese | `chanfro por medida` | open the chamfer pop-up |

---

## How to report

For each test: **what you said**, **what came out in the Report View** and **whether the
object appeared in the tree** of the DAV panel.

---

## Where it is most likely to fail

None of this was run inside FreeCAD: it was validated with stubs, which confirm
the phrase routing and that the dictated values reach the correct properties
(`Pad.Length`, `Fillet.Radius`, `Chamfer.Angle`…), but not the interaction with
live FreeCAD.

The highest-risk points:

1. **Fillet and chamfer** — they are applied to **all edges** of the solid
   (`UseAllEdges`), because choosing single edges by voice is not practical. If the
   radius or size is too large for the part, the recompute fails: this is
   FreeCAD behavior, not the command's, but it is worth seeing what message
   appears.
2. **Subtractive** — the profile is converted from `Part::Feature` to a sketch, just
   as in `extruir`. With real curves it may behave differently than with the
   stub.
3. **`agujero por medidas`** — `DepthType = 1` is forced so it respects the dictated
   depth; it is worth confirming that the hole comes out with the requested depth and
   not through-all.
