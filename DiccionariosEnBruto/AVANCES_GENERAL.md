# Avances Generales — Diccionarios DAV

> Actualizado: 2026-06-03

---

## Estado por módulo

| Módulo | Tickets | Cobertura | Bugs pendientes | Estado |
| ------ | ------- | --------- | --------------- | ------ |
| **Explorer** | 59 | 59/59 ✅ | 0 | ✅ Listo |
| **LineAttributes** | 2 | 2/2 ✅ | 0 | ✅ Listo |
| **StdView** | 99 | 99/99 ✅ | 0 | ✅ Listo |
| **Workbench/Assembly** | 22 | 22/22 ✅ | 0 | ✅ Listo |
| **Workbench/PartDesign** | 36 | 36/36 ✅ | 0 — corregido 2026-06-03 | ✅ Listo |
| **Workbench/Sketcher** | 97 | 94/97 ✅ | 1 (`refraction`) + `intersection` por verificar versión | ⚠️ Casi completo |
| **Workbench/DraftWork** | 59 | 59/59 ✅ | 0 — corregido 2026-06-03 | ✅ Listo |
| **Workbench/TechDraw** | 44/44 ✅ | 44/44 ✅ | 0 — corregido 2026-06-03 | ✅ Listo |
| **Workbench/Part** | 24 | 24/24 ✅ | 0 — operaciones migradas a Opción B (API directa) 2026-06-03 | ✅ Listo |

---

## Explorer — resumen de sesión (2026-06-03)

Módulo auditado y corregido íntegramente. Resumen de cambios aplicados:

| # | Archivo | Corrección aplicada |
|---|---------|---------------------|
| 1 | `Tools/Tools.py` | `'clarify selection'` → `'clarifyselection'` |
| 2 | `Tools/Tools.py` | `'proyectutil'` → `'projectutil'` |
| 3 | `StructureToolbar/structure.py` | `'new Group'` → `'newgroup'`, `'link actions'` → `'linkactions'` |
| 4 | `StructureToolbar/linkActions/link.py` | 5 claves con espacios → `'makelink'`, `'relativelink'`, `'importlink'`, `'importalllinks'`, `'replacelink'` |
| 5 | `Explorer.py` | Importados `structure` y `additional`; agregados al `.update()` |
| 6 | `Edit.py` | Eliminados `'screenshot'` y `'note'` (duplicados de `Explorer.py`) |
| 7 | `Edit.py`, `Tools.py`, `Expressions.py` | Cabezal GPL duplicado unificado |
| 8 | `Expressions.py` | `'paste'` → `'pasteexpr'` (colisión con `edit['paste']`) |
| 9 | `AdditionalTools/Additional.py` | `'linkGroups'` → `'linkgroups'` (camelCase violaba convención) |

---

## StdView — resumen de sesión (2026-06-03)

Módulo auditado y corregido íntegramente. 99 tickets cubiertos. Resumen de cambios aplicados:

| # | Archivo | Corrección aplicada |
|---|---------|---------------------|
| 1 | `StdView.py` | Import de `Appearance` corregido (`appearance` en lugar de `Panels`); `update(appearance)` agregado; `'ayuda'` → `'help'` |
| 2 | `Appearance/Appearance.py` | Header GPL completado; `'faceColors'` → `'facecolors'`; agregados `'randomcolor'` y `'texturemapping'`; `'help': ayuda` |
| 3 | `Appearance/ayuda.py` | Entradas para `facecolors`, `randomcolor`, `texturemapping` agregadas |
| 4 | `Panels/Panels.py` | Variable exportada `panels` → `Panels` (consistencia con import en raíz); `'help': ayuda` |
| 5 | `StandardViews/StandardViews.py` | Eliminadas 4 entradas duplicadas/mal ubicadas: `clearviews`, `clippingview`, `drawstyleasis`, `aligntoselection`; `'help': ayuda` |
| 6 | `StandardViews/ayuda.py` | Eliminadas entradas correspondientes a los duplicados removidos |
| 7 | `Visibility/Visibility.py` | `'aligntoselection'` movido desde `StandardViews`; `'help': ayuda` |
| 8 | `Visibility/ayuda.py` | Entrada para `aligntoselection` agregada |
| 9 | `Clipping/Clipping.py`, `Material/Material.py` | Headers GPL completados; `'help': ayuda` |
| 10 | `Toolbars/Toolbars.py` | `'help'` (colisión con ayuda) renombrado a `'toolbarshelp'`; `'help': ayuda` agregado |
| 11 | `Toolbars/ayuda.py` | Claves actualizadas para coincidir con diccionario real |
| 12 | Todos los subdiccionarios | `from .ayuda import ayuda` y `'help': ayuda` agregados en los 13 submodules |

---

## Comandos que no usan `Gui.runCommand`

Algunos módulos usan API Python directa en lugar de `Gui.runCommand`. Se clasifican en:

- **✅ Válido** — API directa correcta, produce el resultado esperado
- **⚠️ Funcional con limitaciones** — funciona pero con restricciones (parámetros fijos, hardcoded, sin diálogo o sin selección interactiva)
- **❌ Roto** — la implementación tiene errores que impiden la ejecución correcta

### Nota de diseño — Opción A vs Opción B

Todos los comandos que usan `Gui.runCommand` siguen la **Opción A**: la voz activa el comando y FreeCAD abre su diálogo nativo, donde el usuario termina la interacción con el mouse (selecciona aristas, ingresa valores, etc.). Este es el patrón correcto para el MVP.

La **Opción B** (API directa + selección programática) solo es viable para primitivas simples cuyos únicos parámetros son numéricos (box, cylinder, etc.) porque no requieren que el usuario seleccione geometría previa. Para todo lo demás — operaciones sobre geometría existente (chamfer, fillet, sweep, dimensiones TechDraw, constraints Sketcher) — la Opción B requeriría que el motor de voz también gestione qué objeto está seleccionado y qué aristas/vértices aplicar, lo cual excede el alcance del MVP.

**Los 16 archivos `part_*` fueron migrados a Opción A (`Gui.runCommand`) el 2026-06-03 y luego revertidos a Opción B (API directa `doc.addObject`) el 2026-06-03** para ejecutar la operación sin abrir diálogo, usando la selección activa. Ver tabla actualizada abajo.**

---

### Explorer — `File/File.py` y `Windows/Windows.py`

| Clave | Módulo | Implementación | Estado | Motivo |
| ----- | ------ | -------------- | ------ | ------ |
| `'new'` | `File.py` | `FreeCAD.newDocument()` | ✅ Válido | No hay `Std_New` accesible como `runCommand` desde script |
| `'save'` | `File.py` | `FreeCAD.activeDocument().save()` | ✅ Válido | Equivalente directo a `Std_Save` |
| `'quit'` | `Windows.py` | `Gui.getMainWindow().close()` | ✅ Válido | Cierre de ventana vía Qt; no hay `runCommand` equivalente |

### Workbench/Part — primitivas

Las primitivas usan API directa (Opción B) porque necesitan parámetros numéricos que `runCommand` no acepta. No requieren selección previa de ningún objeto.

| Archivo | Claves | Estado |
| ------- | ------ | ------ |
| `box/box.py` | `'box'` | ✅ Válido |
| `circle/circle.py` | `'circle'` | ✅ Válido |
| `cone/cone.py` | `'cone'`, `'primitive cone'` | ✅ Válido |
| `cylinder/cylinder.py` | `'cylinder'`, `'primitive cylinder'` | ✅ Válido |
| `ellipse/ellipse.py` | `'ellipse'` | ✅ Válido |
| `line/line.py` | `'line'` | ✅ Válido |
| `cube/cube.py` | `'cube'` | ⚠️ Funcional con limitaciones — duplicado semántico de `box` |
| `new_sketch/new_sketch.py` | `'nuevo boceto'`, `'nuevo sketch'`, `'crear sketch'` | ⚠️ Funcional con limitaciones — crea sketch sin plano; ya cubierto en Sketcher |

### Workbench/Part — operaciones (Opción B — API directa, selección previa)

Los 16 comandos `part_*` usan **Opción B**: el usuario selecciona el objeto antes de decir el comando, y la operación se ejecuta directamente via `doc.addObject("Part::*")` sin abrir diálogo. El resultado es un objeto paramétrico editable; el original se oculta automáticamente.

Tres comandos sin equivalente `Part::*` en el Document API (`color_per_face`, `cross_sections`, `projection_on_surface`) validan la selección antes de delegar a `Gui.runCommand`.

| Archivo | Claves | API | Estado |
| ------- | ------ | --- | ------ |
| `part_chamfer` | `'chaflan'`, `'chaflán'`, `'biselar'` | `Part::Chamfer` | ✅ Opción B |
| `part_fillet` | `'redondear bordes'`, `'fillet'`, `'redondear'` | `Part::Fillet` | ✅ Opción B |
| `part_extrude` | `'extruir'`, `'extrude'`, `'extruir objeto'` | `Part::Extrusion` | ✅ Opción B |
| `part_mirror` | `'espejo'`, `'reflejar'`, `'mirror'` | `Part::Mirroring` | ✅ Opción B |
| `part_revolve` | `'revolucion'`, `'revolución'`, `'revolve'` | `Part::Revolution` | ✅ Opción B |
| `part_loft` | `'hacer loft'`, `'loft'`, `'unir perfiles'` | `Part::Loft` (min. 2 perfiles) | ✅ Opción B |
| `part_sweep` | `'barrer perfil'`, `'sweep'`, `'barrido'` | `Part::Sweep` (perfil + camino) | ✅ Opción B |
| `part_ruled_surface` | `'superficie reglada'`, `'unir curvas'`, `'ruled surface'` | `Part::RuledSurface` (2 curvas) | ✅ Opción B |
| `part_offset` | `'desfase'`, `'offset'`, `'ensanchar'`, `'encoger'` | `Part::Offset3D` | ✅ Opción B |
| `part_offset2d` | `'contorno'`, `'borde'`, `'offset 2d'` | `Part::Offset2D` | ✅ Opción B |
| `part_scale` | `'escalar'`, `'agrandar'`, `'reducir'`, `'scale'` | `Part::Scale` | ✅ Opción B |
| `part_section` | `'intersección'`, `'obtener sección'`, `'section'` | `Part::Section` (2 objetos) | ✅ Opción B |
| `part_makeface` | `'crear cara'`, `'make face'`, `'cara'` | `Part.makeFilledFace` | ✅ Opción B |
| `part_projection_on_surface` | `'proyectar dibujo'`, `'proyectar'`, `'projection'` | `Part::ProjectionOnSurface` | ✅ Opción B |
| `part_color_per_face` | `'pintar cara'`, `'color por cara'`, `'colorear cara'` | sin API — valida sel. + `runCommand` | ⚠️ Híbrido |
| `part_cross_sections` | `'secciones transversales'`, `'cross sections'` | sin API — valida sel. + `runCommand` | ⚠️ Híbrido |

### Workbench/Sketcher — `constraints/constraints.py`

Los constraints usan Opción B porque requieren pasar el tipo y parámetros numéricos que `runCommand` no acepta. Funcionan con sketch activo y geometría ya creada. La selección de geometría (índices) está hardcodeada en valores por defecto.

| Claves | Implementación | Estado | Nota |
| ------ | -------------- | ------ | ---- |
| `'dimension'`, `'hdim'`, `'vdim'`, `'angle'`, `'radius'`, `'diameter'`, `'radiam'`, `'distance'` | `Sketcher.Constraint('...', ...)` | ⚠️ Funcional con limitaciones | Parámetros numéricos hardcodeados (ej. `15.0`, `18.0`); requiere sketch activo con geometría |
| `'toggleconstruction'` | `sketch.toggleConstruction(idx)` | ⚠️ Funcional con limitaciones | Índice de geometría hardcodeado |

### Workbench/TechDraw — `Dimensions/`

Las dimensiones TechDraw usan **Opción B** (API directa) porque el usuario que opera por voz no puede mover el mouse para hacer la selección después de que se abre el diálogo — el foco cambia. La implementación correcta lee la selección activa con `Gui.Selection.getSelectionEx()` antes de crear el objeto, de modo que el usuario selecciona la geometría primero y luego dice el comando.

`dimension/dimension.py` usa Opción A (`Gui.runCommand`) porque es el caso genérico que abre el diálogo y permite elegir el tipo interactivamente.

| Archivo | Clave | Patrón | Estado |
| ------- | ----- | ------ | ------ |
| `dimension/dimension.py` | `'dimension'` | Opción A — `Gui.runCommand` | ✅ Válido |
| `length/length.py` | `'length'` | Opción B — lee selección activa → `DrawViewDimension` tipo `Distance` | ✅ Válido |
| `horizontal/horizontal.py` | `'horizontal'` | Opción B — lee selección activa → tipo `DistanceX` | ✅ Válido |
| `extent/extent.py` | `'extent'` | Opción B — lee selección activa → `TechDraw.makeExtentDim` | ✅ Válido |
| `radius/radius.py` | `'radius'` | Opción B — lee selección activa → tipo `Radius` | ✅ Válido |
| `diameter/diameter.py` | `'diameter'` | Opción B — lee selección activa → tipo `Diameter` | ✅ Válido |
| `angle/angle.py` | `'angle'`, `'points'` | Opción B — lee selección activa → tipo `Angle` / `Angle3Pt` | ✅ Válido |

---

## LineAttributes — resumen de sesión (2026-06-03)

Módulo auditado y corregido. Resumen de cambios aplicados:

| # | Archivo             | Corrección aplicada                                          |
|---|---------------------|--------------------------------------------------------------|
| 1 | `LineAttributes.py` | Subdict anidado → `.update(attributes)` (claves aplanadas)   |
| 2 | `ayuda.py` (raiz)   | `'attributes'` → lista `'select'` y `'change'` directamente  |
