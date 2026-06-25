# Avances — Módulo Workbench

> Revisado: 2026-06-25 (contraste código vs. avances)
> Revisión previa: 2026-06-03

Cubre: Assembly, DraftWork, Part, PartDesign, Sketcher, TechDraw (auditado íntegramente)

> **Nota 2026-06-25:** el código se modificó después del 2026-06-03 (se agregó
> `_lenient.LenientDict`, se importaron submódulos antes huérfanos y se renombraron
> archivos raíz). Las secciones de DraftWork y TechDraw fueron actualizadas para
> reflejar el estado real. Ver `AVANCES_GENERAL.md` → "Reconciliación 2026-06-25".

---

## Assembly

### Estructura

```
Workbench/Assembly/
├── AssemblyWorkbench.py    ← raíz, usa .update()
└── joint/
    └── joint.py
```

### Cobertura (22 tickets)

**✅ Cubiertos — todos los 22 tickets**

| Ticket | Comando | Archivo | Clave |
|--------|---------|---------|-------|
| `ticket_create_assembly` | `Gui.runCommand('Assembly_CreateAssembly', 0)` | `AssemblyWorkbench.py` | `'create'` |
| `ticket_insert_new_part` | `Gui.runCommand('Assembly_InsertNewPart', 0)` | `AssemblyWorkbench.py` | `'newpart'` |
| `ticket_insert_link` | `Gui.runCommand('Assembly_InsertLink', 0)` | `AssemblyWorkbench.py` | `'link'` |
| `ticket_solve_assembly` | `Gui.runCommand('Assembly_SolveAssembly', 0)` | `AssemblyWorkbench.py` | `'solve'` |
| `ticket_create_view` | `Gui.runCommand('Assembly_CreateView', 0)` | `AssemblyWorkbench.py` | `'view'` |
| `ticket_create_simulation` | `Gui.runCommand('Assembly_CreateSimulation', 0)` | `AssemblyWorkbench.py` | `'simulation'` |
| `ticket_create_bom` | `Gui.runCommand('Assembly_CreateBom', 0)` | `AssemblyWorkbench.py` | `'bom'` |
| `ticket_assembly_preferences` | `Gui.runCommand('Assembly_Preferences', 0)` | `AssemblyWorkbench.py` | `'preferences'` |
| `Ticket_Assembly_ToggleGrounded` | `Gui.runCommand('Assembly_ToggleGrounded', 1)` | `AssemblyWorkbench.py` | `'grounded'` |
| `Ticket_Assembly_CreateJointAngle` | `Gui.runCommand('Assembly_CreateJointAngle', 0)` | `joint.py` | `'angle'` |
| `Ticket_Assembly_CreateJointBall` | `Gui.runCommand('Assembly_CreateJointBall', 0)` | `joint.py` | `'ball'` |
| `Ticket_Assembly_CreateJointBelt` | `Gui.runCommand('Assembly_CreateJointBelt', 0)` | `joint.py` | `'belt'` |
| `Ticket_Assembly_CreateJointCylindrical` | `Gui.runCommand('Assembly_CreateJointCylindrical', 0)` | `joint.py` | `'cylindrical'` |
| `Ticket_Assembly_CreateJointDistance` | `Gui.runCommand('Assembly_CreateJointDistance', 0)` | `joint.py` | `'distance'` |
| `Ticket_Assembly_CreateJointFixed` | `Gui.runCommand('Assembly_CreateJointFixed', 0)` | `joint.py` | `'fixed'` |
| `Ticket_Assembly_CreateJointGears` | `Gui.runCommand('Assembly_CreateJointGears', 0)` | `joint.py` | `'gears'` |
| `Ticket_Assembly_CreateJointParallel` | `Gui.runCommand('Assembly_CreateJointParallel', 0)` | `joint.py` | `'parallel'` |
| `Ticket_Assembly_CreateJointPerpendicular` | `Gui.runCommand('Assembly_CreateJointPerpendicular', 0)` | `joint.py` | `'perpendicular'` |
| `Ticket_Assembly_CreateJointRackPinion` | `Gui.runCommand('Assembly_CreateJointRackPinion', 0)` | `joint.py` | `'rackpinion'` |
| `Ticket_Assembly_CreateJointRevolute` | `Gui.runCommand('Assembly_CreateJointRevolute', 0)` | `joint.py` | `'revolute'` |
| `Ticket_Assembly_CreateJointScrew` | `Gui.runCommand('Assembly_CreateJointScrew', 0)` | `joint.py` | `'screw'` |
| `Ticket_Assembly_CreateJointSlider` | `Gui.runCommand('Assembly_CreateJointSlider', 0)` | `joint.py` | `'slider'` |

**Bugs:** ninguno. Assembly es el módulo más limpio del proyecto.

---

## DraftWork

### Estructura

```
Workbench/DraftWork/
├── DraftWork.py             ← raíz, usa .update() + LenientDict — importa TODAS las subcarpetas ✅
├── annotation/annotation.py
├── annotation_style_editor/annotation_style_editor.py
├── arc/arc.py
├── circle/circle.py
├── circular_array/circular_array.py  ← importado como 'array' en DraftWork.py
├── creation/creation.py     ← ✅ importado (corregido)
├── curve/curve.py
├── dimension/dimension.py
├── Drafting/drafting.py     ← ✅ importado (corregido)
├── ellipse/ellipse.py
├── facebinder/facebinder.py
├── modification/modification.py  ← ✅ importado (corregido); subcarpeta array/ eliminada
└── modify/modify.py
```

> **Estado real 2026-06-25:** `DraftWork.py` (no `workbench.py`) importa los 12 submódulos
> con `.update()` y envuelve el resultado en `LenientDict`. Las carpetas `snap/` y
> `modification/array/` fueron **eliminadas**. Los archivos raíz y de subcarpeta fueron
> renombrados (`DraftWork.py`, `circular_array.py`, `annotation_style_editor.py`).

### Cobertura (59 tickets Draft)

**✅ Cubiertos y activos (en workbench.py)**

| Ticket | Comando | Archivo | Clave |
|--------|---------|---------|-------|
| `Draft_AnnotationStyleEditor` | `Gui.runCommand('Draft_AnnotationStyleEditor', 0)` | `annotation_style_editor/annotation.py` | `'editor'` |
| `Draft_Arc` | `Gui.runCommand('Draft_Arc', 0)` | `arc/arc.py` | `'center'` |
| `Draft_Arc_3Points` | `Gui.runCommand('Draft_Arc_3Points', 0)` | `arc/arc.py` | `'points'` |
| `Draft_BezCurve` | `Gui.runCommand('Draft_BezCurve', 0)` | `curve/curve.py` | `'bezier'` |
| `Draft_BSpline` | `Gui.runCommand('Draft_BSpline', 0)` | `curve/curve.py` | `'bspline'` |
| `Draft_CubicBezCurve` | `Gui.runCommand('Draft_CubicBezCurve', 0)` | `curve/curve.py` | `'cubic'` |
| `Draft_Circle` | `Gui.runCommand('Draft_Circle', 0)` | `circle/circle.py` | `'center'` |
| `Draft_CircularArray` | `Gui.runCommand('Draft_CircularArray', 0)` | `circular_array/array.py` | `'circular'` |
| `Draft_OrthoArray` | `Gui.runCommand('Draft_OrthoArray', 0)` | `circular_array/array.py` | `'ortho'` |
| `Draft_PolarArray` | `Gui.runCommand('Draft_PolarArray', 0)` | `circular_array/array.py` | `'polar'` |
| `Draft_PathArray` | `Gui.runCommand('Draft_PathArray', 0)` | `circular_array/array.py` | `'path'` |
| `Draft_PathLinkArray` | `Gui.runCommand('Draft_PathLinkArray', 0)` | `circular_array/array.py` | `'path_link'` |
| `Draft_PointArray` | `Gui.runCommand('Draft_PointArray', 0)` | `circular_array/array.py` | `'point'` |
| `Draft_PointLinkArray` | `Gui.runCommand('Draft_PointLinkArray', 0)` | `circular_array/array.py` | `'point_link'` |
| `Draft_Clone` | `Gui.runCommand('Draft_Clone', 0)` | `modify/modify.py` | `'clone'` |
| `Draft_Downgrade` | `Gui.runCommand('Draft_Downgrade', 0)` | `modify/modify.py` | `'downgrade'` |
| `Draft_Draft2Sketch` | `Gui.runCommand('Draft_Draft2Sketch', 0)` | `modify/modify.py` | `'sketch'` |
| `Draft_Edit` | `Gui.runCommand('Draft_Edit', 0)` | `modify/modify.py` | `'edit'` |
| `Draft_Fillet` | `Gui.runCommand('Draft_Fillet', 0)` | `modify/modify.py` | `'fillet'` |
| `Draft_Join` | `Gui.runCommand('Draft_Join', 0)` | `modify/modify.py` | `'join'` |
| `Draft_Move` | `Gui.runCommand('Draft_Move', 0)` | `modify/modify.py` | `'move'` |
| `Draft_Offset` | `Gui.runCommand('Draft_Offset', 0)` | `modify/modify.py` | `'offset'` |
| `Draft_Rotate` | `Gui.runCommand('Draft_Rotate', 0)` | `modify/modify.py` | `'rotate'` |
| `Draft_Dimension` | `Gui.runCommand('Draft_Dimension', 0)` | `dimension/dimension.py` | `'linear'` |
| `Draft_FlipDimension` | `Gui.runCommand('Draft_FlipDimension', 0)` | `dimension/dimension.py` | `'flip'` |
| `Draft_Text` | `Gui.runCommand('Draft_Text', 0)` | `annotation/annotation.py` | `'text'` |
| `Draft_ShapeString` | `Gui.runCommand('Draft_ShapeString', 0)` | `annotation/annotation.py` | `'shape_string'` |
| `Draft_Label` | `Gui.runCommand('Draft_Label', 0)` | `annotation/annotation.py` | `'label'` |
| `Draft_Ellipse` | `Gui.runCommand('Draft_Ellipse', 0)` | `ellipse/ellipse.py` | `'center'` |
| `Draft_Facebinder` | `Gui.runCommand('Draft_Facebinder', 0)` | `facebinder/facebinder.py` | `'create'` |

**✅ Módulos antes huérfanos, ahora importados en `DraftWork.py` (corregido)**

Estos módulos ya están activos en la raíz (antes la doc los daba como no importados):

| Módulo | Tickets cubiertos | Estado |
|--------|-----------------|--------|
| `Drafting/drafting.py` | `Draft_Wire` | ✅ importado |
| `creation/creation.py` | `Draft_Hatch`, `Draft_Point`, `Draft_Polygon`, `Draft_Rectangle` | ✅ importado |
| `modification/modification.py` | `Draft_Scale`, `Draft_Shape2DView`, `Draft_Slope`, `Draft_Split`, `Draft_Stretch`, `Draft_SubelementHighlight`, `Draft_Trimex`, `Draft_Upgrade`, `Draft_WireToBSpline` | ✅ importado |

**❌ Tickets sin ninguna cobertura**

| Ticket | Comando | Nota |
|--------|---------|------|
| `Draft_Line` | `Draft.make_line(p1, p2)` | API Nivel 2 — no existe en ningún dict; `Draft_Wire` (en `Drafting/`) es el equivalente GUI pero semánticamente distinto |

### Bugs DraftWork

> Bugs #1–#9 originales: la mayoría se corrigieron en código después del 2026-06-03.
> Estado verificado el 2026-06-25.

| # | Archivo | Problema | Estado |
|---|---------|----------|--------|
| 1 | `DraftWork.py` | No importaba `Drafting`, `creation`, `modification`, `snap` | ✅ Corregido — los 12 submódulos importados |
| 2 | `creation/creation.py` | `import FreeCad as Gui` — typo grave | ✅ Corregido — usa `import FreeCADGui as Gui` |
| 3 | `modification/array/array.py` | `import FreeCad as Gui` | ✅ Resuelto — carpeta eliminada |
| 4 | `modification/array/array.py` | `Gui.runCommand('Draft_ArrayTools', N)` inexistente | ✅ Resuelto — carpeta eliminada (arrays cubiertos en `circular_array/`) |
| 5 | `snap/snap.py` | `import FreeCad as Gui` | ✅ Resuelto — carpeta eliminada |
| 6 | `snap/snap.py` | Nombre de carpeta engañoso (contenía `Draft_Mirror`) | ✅ Resuelto — carpeta eliminada |
| 7 | `modification/array/array.py` | Duplicado de `circular_array/` | ✅ Resuelto — carpeta eliminada |
| 8 | `annotation/annotation.py` | `'shape_string'` con guión bajo | ✅ Corregido — usa `'shapestring'` |
| 9 | `circular_array/circular_array.py` | `'path_link'`/`'point_link'` con guión bajo | ✅ Corregido — usa `'pathlink'`/`'pointlink'` |
| 10 | `modification/modification.py` | Claves con guión bajo: `'shape_2d_view'`, `'subelement_highlight'`, `'wire_to_bspline'` — violan convención (sin separadores); además falta el cabezal GPL | ⚠️ **Pendiente** — renombrar a `'shape2dview'`, `'subelementhighlight'`, `'wiretobspline'` y agregar cabezal |

---

## PartDesign

### Estructura

```
Workbench/PartDesign/
├── partdesign.py       ← raíz, usa .update()
├── additive/additive.py
├── base/base.py
├── manage/manage.py
├── modify/modify.py
├── subtractive/subtractive.py
└── transform/transform.py
```

### Cobertura (36 tickets PartDesign)

**✅ Cubiertos — todos los 36 tickets**

| Ticket | Comando | Archivo | Clave |
|--------|---------|---------|-------|
| `PartDesign_Body` | `Gui.runCommand('PartDesign_Body', 0)` | `base.py` | `'body'` |
| `PartDesign_NewSketch` | `Gui.runCommand('PartDesign_NewSketch', 0)` | `base.py` | `'newsketch'` |
| `PartDesign_Clone` | `Gui.runCommand('PartDesign_Clone', 0)` | `base.py` | `'clone'` |
| `PartDesign_SubShapeBinder` | `Gui.runCommand('PartDesign_SubShapeBinder', 0)` | `base.py` | `'subshapebinder'` |
| `PartDesign_Pad` | `Gui.runCommand('PartDesign_Pad', 0)` | `additive.py` | `'pad'` |
| `PartDesign_Revolution` | `Gui.runCommand('PartDesign_Revolution', 0)` | `additive.py` | `'revolution'` |
| `PartDesign_AdditiveHelix` | `Gui.runCommand('PartDesign_AdditiveHelix', 0)` | `additive.py` | `'additivehelix'` |
| `PartDesign_AdditiveLoft` | `Gui.runCommand('PartDesign_AdditiveLoft', 0)` | `additive.py` | `'additiveloft'` |
| `PartDesign_AdditivePipe` | `Gui.runCommand('PartDesign_AdditivePipe', 0)` | `additive.py` | `'additivepipe'` |
| `PartDesign_AdditiveBox` | `Gui.runCommand('PartDesign_AdditiveBox', 0)` | `additive.py` | `'additivebox'` |
| `PartDesign_AdditiveCone` | `Gui.runCommand('PartDesign_AdditiveCone', 0)` | `additive.py` | `'additivecone'` |
| `PartDesign_AdditiveCylinder` | `Gui.runCommand('PartDesign_AdditiveCylinder', 0)` | `additive.py` | `'additivecylinder'` |
| `PartDesign_AdditiveEllipsoid` | `Gui.runCommand('PartDesign_AdditiveEllipsoid', 0)` | `additive.py` | `'additiveellipsoid'` |
| `PartDesign_AdditivePrism` | `Gui.runCommand('PartDesign_AdditivePrism', 0)` | `additive.py` | `'additiveprism'` |
| `PartDesign_AdditiveSphere` | `Gui.runCommand('PartDesign_AdditiveSphere', 0)` | `additive.py` | `'additivesphere'` |
| `PartDesign_AdditiveTorus` | `Gui.runCommand('PartDesign_AdditiveTorus', 0)` | `additive.py` | `'additivetorus'` |
| `PartDesign_AdditiveWedge` | `Gui.runCommand('PartDesign_AdditiveWedge', 0)` | `additive.py` | `'additivewedge'` |
| `PartDesign_Pocket` | `Gui.runCommand('PartDesign_Pocket', 0)` | `subtractive.py` | `'pocket'` |
| `PartDesign_Groove` | `Gui.runCommand('PartDesign_Groove', 0)` | `subtractive.py` | `'groove'` |
| `PartDesign_Hole` | `Gui.runCommand('PartDesign_Hole', 0)` | `subtractive.py` | `'hole'` |
| `PartDesign_SubtractiveBox` | `Gui.runCommand('PartDesign_SubtractiveBox', 0)` | `subtractive.py` | `'subtractivebox'` |
| `PartDesign_SubtractiveCone` | `Gui.runCommand('PartDesign_SubtractiveCone', 0)` | `subtractive.py` | `'subtractivecone'` |
| `PartDesign_SubtractiveCylinder` | `Gui.runCommand('PartDesign_SubtractiveCylinder', 0)` | `subtractive.py` | `'subtractivecylinder'` |
| `PartDesign_SubtractiveEllipsoid` | `Gui.runCommand('PartDesign_SubtractiveEllipsoid', 0)` | `subtractive.py` | `'subtractiveellipsoid'` |
| `PartDesign_SubtractiveHelix` | `Gui.runCommand('PartDesign_SubtractiveHelix', 0)` | `subtractive.py` | `'subtractivehelix'` |
| `PartDesign_SubtractiveLoft` | `Gui.runCommand('PartDesign_SubtractiveLoft', 0)` | `subtractive.py` | `'subtractiveloft'` |
| `PartDesign_SubtractivePipe` | `Gui.runCommand('PartDesign_SubtractivePipe', 0)` | `subtractive.py` | `'subtractivepipe'` |
| `PartDesign_SubtractivePrism` | `Gui.runCommand('PartDesign_SubtractivePrism', 0)` | `subtractive.py` | `'subtractiveprism'` |
| `PartDesign_SubtractiveSphere` | `Gui.runCommand('PartDesign_SubtractiveSphere', 0)` | `subtractive.py` | `'subtractivesphere'` |
| `PartDesign_SubtractiveTorus` | `Gui.runCommand('PartDesign_SubtractiveTorus', 0)` | `subtractive.py` | `'subtractivetorus'` |
| `PartDesign_SubtractiveWedge` | `Gui.runCommand('PartDesign_SubtractiveWedge', 0)` | `subtractive.py` | `'subtractivewedge'` |
| `PartDesign_Fillet` | `Gui.runCommand('PartDesign_Fillet', 0)` | `modify.py` | `'fillet'` |
| `PartDesign_Chamfer` | `Gui.runCommand('PartDesign_Chamfer', 0)` | `modify.py` | `'chamfer'` |
| `PartDesign_Draft` | `Gui.runCommand('PartDesign_Draft', 0)` | `modify.py` | `'draft'` |
| `PartDesign_LinearPattern` | `Gui.runCommand('PartDesign_LinearPattern', 0)` | `transform.py` | `'linearpattern'` |
| `PartDesign_Mirrored` | `Gui.runCommand('PartDesign_Mirrored', 0)` | `transform.py` | `'mirrored'` |
| `PartDesign_PolarPattern` | `Gui.runCommand('PartDesign_PolarPattern', 0)` | `transform.py` | `'polarpattern'` |
| `PartDesign_MultiTransform` | `Gui.runCommand('PartDesign_MultiTransform', 0)` | `transform.py` | `'multitransform'` |
| `PartDesign_MoveFeature` | `Gui.runCommand('PartDesign_MoveFeature', 0)` | `manage.py` | `'movefeature'` |
| `PartDesign_MoveFeatureInTree` | `Gui.runCommand('PartDesign_MoveFeatureInTree', 0)` | `manage.py` | `'movefeatureintree'` |
| `PartDesign_MoveTip` | `Gui.runCommand('PartDesign_MoveTip', 0)` | `manage.py` | `'movetip'` |
| `PartDesign_Preferences` | `Gui.runCommand('Std_DlgPreferences', 0)` | `manage.py` | `'preferences'` |
| `PartDesign_WizardShaft` | `Gui.runCommand('PartDesign_WizardShaft', 0)` | `manage.py` | `'wizardshaft'` |

### Bugs PartDesign

| # | Archivos | Problema | Corrección |
|---|---------|----------|------------|
| 1 | `subtractive.py` + `modify.py` | `'thickness'` duplicado — aparece en ambos; `subtractive` aplana antes que `modify` en `partdesign.py`, luego `modify` lo pisa | Eliminar `'thickness'` de `subtractive.py` (el ticket `PartDesign_Thickness` corresponde a `modify`) |
| 2 | `subtractive.py` + `modify.py` | `'boolean'` duplicado — mismo problema | Eliminar `'boolean'` de `modify.py` (pertenece a `subtractive`, es una operación booleana) |
| 3 | `subtractive.py` + `manage.py` | `'wizardshaft'` duplicado | Eliminar de `subtractive.py` |
| 4 | `transform.py` | `'scaled'` → `PartDesign_MultiTransform` — el ticket `PartDesign_Scaled` describe una sub-operación de MultiTransform, no un comando independiente; la clave es confusa | Evaluar si eliminar `'scaled'` o documentar la aclaración en `ayuda.py` |
| 5 | `additive.py` + `subtractive.py` | Ninguno tiene cabezal GPL — solo tienen el import y el dict sin header | Agregar cabezal GPL a ambos |

---

## Sketcher

### Estructura

```
Workbench/Sketcher/
├── sketcher.py              ← raíz, usa .update()
├── arc/arc.py
├── arcslot/arcslot.py
├── BSpline/bspline.py
├── bspline_tools/bspline_tools.py
├── circle/circle.py
├── constraints/
│   ├── constraints.py       ← constraints dimensionales (API Nivel 2)
│   ├── common.py            ← helpers: GetActiveSketch, RequireGeometry, etc.
│   ├── ayuda.py
│   └── geometric/
│       └── geometric.py     ← constraints geométricos (Gui.runCommand)
├── Ellipse/ellipse.py
├── external/external.py
├── heptagon/heptagon.py
├── hexagon/hexagon.py
├── line/line.py
├── oblong/oblong.py
├── point/point.py
├── Polygon/polygon.py
├── polyline/polyline.py
├── rectangle/rectangle.py
├── select/select.py
├── slot/slot.py
├── square/square.py
├── text/text.py
├── tools/tools.py
├── triangle/triangle.py
├── validate/validate.py
└── view/view.py
```

### Cobertura (97 tickets Sketcher)

**✅ Cubiertos correctamente**

| Ticket | Comando | Archivo | Clave |
|--------|---------|---------|-------|
| `ticket_NewSketch` | `Gui.runCommand('Sketcher_NewSketch', 0)` | `sketcher.py` | `'new'` |
| `ticket_EditSketch` / `Sketcher_EditSketch` | `Gui.runCommand('Sketcher_EditSketch', 0)` | `sketcher.py` | `'edit'` |
| `ticket_AttachSketch` / `Sketcher_MapSketch` | `Gui.runCommand('Sketcher_MapSketch', 0)` | `sketcher.py` | `'attach'` |
| `Sketcher_Grid` | `Gui.runCommand('Sketcher_Grid', 0)` | `sketcher.py` | `'grid'` |
| `ticket_StopOperation` | `Gui.runCommand('Sketcher_StopOperation', 0)` | `sketcher.py` | `'stop'` |
| `ticket_LeaveSketch` | `Gui.runCommand('Sketcher_LeaveSketch', 0)` | `sketcher.py` | `'leave'` |
| `ticket_CancelEditing` | `Gui.runCommand('Sketcher_StopEditing', 0)` | `sketcher.py` | `'cancelediting'` |
| `ticket_Carbon Copy` | `Gui.runCommand('Sketcher_CarbonCopy', 0)` | `sketcher.py` | `'carboncopy'` |
| `ticket_Copy Elements` | `Gui.runCommand('Sketcher_CopyClipboard', 0)` | `sketcher.py` | `'copyelements'` |
| `ticket_Cut Elements` | `Gui.runCommand('Sketcher_Cut', 0)` | `sketcher.py` | `'cutelements'` |
| `ticket_Paste Elements` | `Gui.runCommand('Sketcher_Paste', 0)` | `sketcher.py` | `'pasteelements'` |
| `ticket_Mirror` | `Gui.runCommand('Sketcher_Symmetry', 0)` | `sketcher.py` | `'mirror'` |
| `ticket_MirrorSketch` | `Gui.runCommand('Sketcher_MirrorSketch', 0)` | `sketcher.py` | `'mirrorsketch'` |
| `ticket_Offset` | `Gui.runCommand('Sketcher_Offset', 0)` | `sketcher.py` | `'offset'` |
| `ticket_Move-Array Transform` | `Gui.runCommand('Sketcher_Translate', 0)` | `sketcher.py` | `'movearray'` |
| `ticket_Rotate-Polar Transform` | `Gui.runCommand('Sketcher_Rotate', 0)` | `sketcher.py` | `'rotatepolar'` |
| `ticket_Scale` | `Gui.runCommand('Sketcher_Scale', 0)` | `sketcher.py` | `'scale'` |
| `ticket_Trim Edge` | `Gui.runCommand('Sketcher_Trimming', 0)` | `sketcher.py` | `'trimedge'` |
| `ticket_Split Edge` | `Gui.runCommand('Sketcher_Split', 0)` | `sketcher.py` | `'splitedge'` |
| `ticket_Extend Edge` | `Gui.runCommand('Sketcher_Extend', 0)` | `sketcher.py` | `'extendedge'` |
| `ticket_Fillet` | `Gui.runCommand('Sketcher_CreateFillet', 0)` | `sketcher.py` | `'fillet'` |
| `ticket_Chamfer` | `Gui.runCommand('Sketcher_CreateChamfer', 0)` | `sketcher.py` | `'chamfer'` |
| `ticket_ToggleConstruction` / `Sketcher_ToggleConstruction` | `sketch.toggleConstruction(idx)` | `sketcher.py` | `'toggleconstruction'` |
| `ticket_ValidateSketch` / `Sketcher_ValidateSketch` | `Gui.runCommand('Sketcher_ValidateSketch', 0)` | `validate.py` | `'validate'` |
| `ticket_Delete All Constraints` | `Gui.runCommand('Sketcher_DeleteAllConstraints', 0)` | `tools.py` | `'deleteconstraints'` |
| `ticket_Delete All Geometry` | `Gui.runCommand('Sketcher_DeleteAllGeometry', 0)` | `tools.py` | `'deletegeometry'` |
| `ticket_MergeSketches` | `Gui.runCommand('Sketcher_MergeSketches', 0)` | `tools.py` | `'merge'` |
| `ticket_ReorientSketch` | `Gui.runCommand('Sketcher_ReorientSketch', 0)` | `tools.py` | `'reorient'` |
| `ticket_Remove Axes Alignment` | `Gui.runCommand('Sketcher_RemoveAxesAlignment', 0)` | `tools.py` | `'removeaxes'` |
| `ticket_Select Horizontal Axis` | `Gui.runCommand('Sketcher_SelectHorizontalAxis', 0)` | `select.py` | `'horizontal'` |
| `ticket_Select Vertical Axis` | `Gui.runCommand('Sketcher_SelectVerticalAxis', 0)` | `select.py` | `'vertical'` |
| `ticket_Select Origin` | `Gui.runCommand('Sketcher_SelectOrigin', 0)` | `select.py` | `'origin'` |
| `ticket_ViewSketch` | `Gui.runCommand('Sketcher_ViewSketch', 0)` | `view.py` | `'sketch'` |
| `ticket_ViewSection` | `Gui.runCommand('Sketcher_ViewSection', 0)` | `view.py` | `'section'` |
| `ticket_External Projection` | `Gui.runCommand('Sketcher_Projection', 0)` | `external.py` | `'projection'` |
| `Sketcher_CreateLine` | `Gui.runCommand('Sketcher_CreateLine', 0)` | `line/line.py` | `'line'` |
| `Sketcher_CreatePoint` | `Gui.runCommand('Sketcher_CreatePoint', 0)` | `point/point.py` | `'point'` |
| `Sketcher_CreatePolyline` | `Gui.runCommand('Sketcher_CreatePolyline', 0)` | `polyline/polyline.py` | `'polyline'` |
| `Sketcher_CreateRectangle` / `Sketcher_CreateRectangle_Center` | ambos cubiertos | `rectangle/rectangle.py` | `'center'`, `'corner'` |
| `Sketcher_CreateSquare` | `Gui.runCommand('Sketcher_CreateSquare', 0)` | `square/square.py` | `'square'` |
| `Sketcher_CreateTriangle` | `Gui.runCommand('Sketcher_CreateTriangle', 0)` | `triangle/triangle.py` | `'triangle'` |
| `Sketcher_CreateCircle` / `Sketcher_Create3PointCircle` | ambos cubiertos | `circle/circle.py` | `'center'`, `'points'` |
| `Sketcher_CreateArc` / `Sketcher_Create3PointArc` | ambos cubiertos | `arc/arc.py` | `'center'`, `'points'` |
| `Sketcher_CreateArcSlot` | `Gui.runCommand('Sketcher_CreateArcSlot', 0)` | `arcslot/arcslot.py` | `'arcends'`, `'flatends'` |
| `Sketcher_CreateOblong` | `Gui.runCommand('Sketcher_CreateOblong', 0)` | `oblong/oblong.py` | `'oblong'` |
| `Sketcher_CreateText` | `Gui.runCommand('Sketcher_CreateText', 0)` | `text/text.py` | `'text'` |
| `Sketcher_CreateHexagon` | `Gui.runCommand('Sketcher_CreateHexagon', 0)` | `hexagon/hexagon.py` | `'hexagon'` |
| `Sketcher_CreateHeptagon` | `Gui.runCommand('Sketcher_CreateHeptagon', 0)` | `heptagon/heptagon.py` | `'heptagon'` |
| `Sketcher_CreateSlot` | `Gui.runCommand('Sketcher_CreateSlot', 0)` | `slot/slot.py` | `'slot'` |
| `Sketcher_CreateEllipseByCenter` | `Gui.runCommand('Sketcher_CreateEllipseByCenter', 0)` | `Ellipse/ellipse.py` | `'center'` |
| `Sketcher_CreateEllipseBy3Points` | `Gui.runCommand('Sketcher_CreateEllipseBy3Points', 0)` | `Ellipse/ellipse.py` | `'3points'` |
| `Sketcher_CreateArcOfEllipse` | `Gui.runCommand('Sketcher_CreateArcOfEllipse', 0)` | `Ellipse/ellipse.py` | `'elliptic'` |
| `Sketcher_CreateArcOfHyperbola` | `Gui.runCommand('Sketcher_CreateArcOfHyperbola', 0)` | `Ellipse/ellipse.py` | `'hyperbolic'` |
| `Sketcher_CreateArcOfParabola` | `Gui.runCommand('Sketcher_CreateArcOfParabola', 0)` | `Ellipse/ellipse.py` | `'parabolic'` |
| `Sketcher_CreatePentagon` | `Gui.runCommand('Sketcher_CreatePentagon', 0)` | `Polygon/polygon.py` | `'pentagon'` |
| `Sketcher_CreateOctagon` | `Gui.runCommand('Sketcher_CreateOctagon', 0)` | `Polygon/polygon.py` | `'octagon'` |
| `Sketcher_CreateRegularPolygon` | `Gui.runCommand('Sketcher_CreateRegularPolygon', 0)` | `Polygon/polygon.py` | `'regular'` |
| `Sketcher_CreateBSpline` / `Sketcher_CreatePeriodicBSpline` | ambos cubiertos | `BSpline/bspline.py` | `'direct'`, `'periodic'` |
| `Sketcher_CreateBSplineByInterpolation` / `Sketcher_CreatePeriodicBSplineByInterpolation` | ambos cubiertos | `BSpline/bspline.py` | `'interpolation'`, `'periodicinterp'` |
| `Sketcher_BSplineConvertToNURBS` | `Gui.runCommand('Sketcher_BSplineConvertToNURBS', 0)` | `bspline_tools/bspline_tools.py` | `'tonurbs'` |
| `Sketcher_BSplineDecreaseDegree` | `Gui.runCommand('Sketcher_BSplineDecreaseDegree', 0)` | `bspline_tools/bspline_tools.py` | `'decrease'` |
| `Sketcher_BSplineIncreaseDegree` | `Gui.runCommand('Sketcher_BSplineIncreaseDegree', 0)` | `bspline_tools/bspline_tools.py` | `'increase'` |
| `Sketcher_BSplineInsertKnot` | `Gui.runCommand('Sketcher_BSplineInsertKnot', 0)` | `bspline_tools/bspline_tools.py` | `'knot'` |
| `Sketcher_BSplineJoinCurve` | `Gui.runCommand('Sketcher_BSplineJoinCurve', 0)` | `bspline_tools/bspline_tools.py` | `'join'` |
| `ticket_CoincidentConstraint` | `Gui.runCommand('Sketcher_ConstrainCoincident', 0)` | `geometric/geometric.py` | `'coincident'` |
| `ticket_CoincidentUnifiedConstraint` | `Gui.runCommand('Sketcher_ConstrainCoincidentUnified', 0)` | `geometric/geometric.py` | `'coincidentunified'` |
| `ticket_LockPositionConstraint` | `Gui.runCommand('Sketcher_ConstrainLock', 0)` | `geometric/geometric.py` | `'lock'` |
| `ticket_PointOnObjectConstraint` | `Gui.runCommand('Sketcher_ConstrainPointOnObject', 0)` | `geometric/geometric.py` | `'pointonobject'` |
| `ticket_HorizontalConstraint` | `Gui.runCommand('Sketcher_ConstrainHorizontal', 0)` | `geometric/geometric.py` | `'horizontal'` |
| `ticket_VerticalConstraint` | `Gui.runCommand('Sketcher_ConstrainVertical', 0)` | `geometric/geometric.py` | `'vertical'` |
| `ticket_HorizontalVerticalConstraint` | `Gui.runCommand('Sketcher_ConstrainHorVer', 0)` | `geometric/geometric.py` | `'horver'` |
| `ticket_ParallelConstraintConstraint` | `Gui.runCommand('Sketcher_ConstrainParallel', 0)` | `geometric/geometric.py` | `'parallel'` |
| `ticket_PerpendicularConstraint` | `Gui.runCommand('Sketcher_ConstrainPerpendicular', 0)` | `geometric/geometric.py` | `'perpendicular'` |
| `ticket_TangentCollinearConstraint` | `Gui.runCommand('Sketcher_ConstrainTangent', 0)` | `geometric/geometric.py` | `'tangent'` |
| `ticket_EqualConstraint` | `Gui.runCommand('Sketcher_ConstrainEqual', 0)` | `geometric/geometric.py` | `'equal'` |
| `ticket_SymmetricConstraint` | `Gui.runCommand('Sketcher_ConstrainSymmetric', 0)` | `geometric/geometric.py` | `'symmetric'` |
| `ticket_BlockConstraint` | `Gui.runCommand('Sketcher_ConstrainBlock', 0)` | `geometric/geometric.py` | `'block'` |
| `ticket_ToggleDrivingReferenceConstraint` | `Gui.runCommand('Sketcher_ToggleDrivingReference', 0)` | `geometric/geometric.py` | `'toggledriving'` |
| `ticket_ToggleConstraints` | `Gui.runCommand('Sketcher_ToggleConstraints', 0)` | `geometric/geometric.py` | `'toggleactive'` |
| `ticket_DimensionConstraint` | `Sketcher.Constraint('Distance', ...)` | `constraints/constraints.py` | `'dimension'` |
| `ticket_HorizontalDimensionConstraint` | `Sketcher.Constraint('DistanceX', ...)` | `constraints/constraints.py` | `'horizontal'` |
| `ticket_VerticalDimensionConstraint` | `Sketcher.Constraint('DistanceY', ...)` | `constraints/constraints.py` | `'vertical'` |
| `ticket_AngleDimensionConstraint` | `Sketcher.Constraint('Angle', ...)` | `constraints/constraints.py` | `'angle'` |
| `ticket_RadiusDimensionConstraint` | `Sketcher.Constraint('Radius', ...)` | `constraints/constraints.py` | `'radius'` |
| `ticket_DiameterDimensionConstraint` | `Sketcher.Constraint('Diameter', ...)` | `constraints/constraints.py` | `'diameter'` |
| `ticket_RadiusDiameterDimensionConstraint` | `Sketcher.Constraint('Diameter', ...)` | `constraints/constraints.py` | `'radiam'` |
| `ticket_DistanceDimensionConstraint` | `Sketcher.Constraint('Distance', ...)` | `constraints/constraints.py` | `'distance'` |

**❌ Tickets sin cobertura**

| Ticket | Comando | Nota |
|--------|---------|------|
| `ticket_RefractionConstraint` | `Sketcher.Constraint('SnellsLaw', ...)` | Falta en `geometric/geometric.py` — clave sugerida: `'refraction'` → `Gui.runCommand('Sketcher_ConstrainSnellsLaw', 0)` |

**⚠️ Tickets que son macros/utilitarios — no requieren entrada en diccionario**

| Ticket | Motivo |
|--------|--------|
| `ticket_Common.txt` | Define `common.py` — módulo auxiliar, no un comando de voz |
| `ticket_GroupConstraint.txt` | Es un ejemplo de encadenamiento de constraints, no un comando DAV |

**⚠️ Tickets con API alternativa**

| Ticket | Dict | Nota |
|--------|------|------|
| `ticket_External Intersection` | `external['intersection']` → `Sketcher_External` | Ticket dice `Sketcher_Intersection`; el dict usa `Sketcher_External` (comando anterior). En FreeCAD 1.1+ el nombre cambió a `Sketcher_Intersection` — **verificar versión objetivo** |

### Bugs Sketcher

| # | Archivo | Problema | Corrección |
|---|---------|----------|------------|
| 1 | `constraints/constraints.py` | `'horizontal'` y `'vertical'` colisionan con las mismas claves en `geometric/geometric.py` — al aplanar en `sketcher.py`, `constraints` aplana antes y `geometric` las pisa (o viceversa según orden) | Renombrar en `constraints.py`: `'hdim'`, `'vdim'` |
| 2 | `external/external.py` | `'intersection'` → `Sketcher_External` pero ticket dice `Sketcher_Intersection` (FreeCAD 1.1+) | Cambiar a `Sketcher_Intersection` si la versión objetivo es 1.1+ |
| 3 | `geometric/geometric.py` | Falta `'refraction'` → `Sketcher_ConstrainSnellsLaw` | Agregar entrada |

---

## TechDraw

### Estructura

```text
Workbench/TechDraw/
├── TechDrawWorkbench.py   ← raíz, usa .update() — todos los módulos importados ✅ (corregido 2026-06-03)
├── Views/
│   ├── Views.py           ← importado (7 comandos)  ✅
│   └── view.py            ← eliminado 2026-06-03 (era huérfano)
├── Dimensions/
│   ├── dimensions.py      ← importado (agrega 3 + sub-dicts)  ✅
│   ├── dimension/         ← 'dimension' → Gui.runCommand (Opción A) ✅
│   ├── length/            ← 'length' → API directa + selección activa (Opción B) ✅
│   ├── horizontal/        ← 'horizontal' → API directa + selección activa (Opción B) ✅
│   ├── extent/            ← 'extent' → API directa + selección activa (Opción B) ✅
│   ├── radius/            ← 'radius' → API directa + selección activa (Opción B) ✅
│   ├── diameter/          ← 'diameter' → API directa + selección activa (Opción B) ✅
│   └── angle/             ← 'angle', 'points' → API directa + selección activa (Opción B) ✅
├── AddLines/addLines.py   ← importado (5 comandos)  ✅
├── Symbols/
│   ├── Symbols.py         ← importado (3 comandos)  ✅
│   └── weld.py            ← eliminado 2026-06-03 (era duplicado)
├── Snaps/Snaps.py         ← importado (2 comandos)  ✅
├── Topology/Topology.py   ← importado (1 comando)   ✅
├── Page/Page.py           ← importado ✅ (corregido 2026-06-03)
├── Annotations/           ← importado ✅ (corregido 2026-06-03)
├── Hatching/              ← importado ✅ (corregido 2026-06-03)
├── AddVertices/           ← importado ✅ (corregido 2026-06-03)
├── OtherViews/            ← importado ✅ (corregido 2026-06-03)
└── Features/Features.py   ← importado ✅ (corregido 2026-06-03)
```

#### Nota de diseño — Dimensiones con API directa (Opción B)

Los sub-dicts de `Dimensions/` (excepto `dimension/`) usan **API Python directa** en lugar de `Gui.runCommand`. Funcionan si el documento tiene una página y vista con los nombres por defecto (`"Page"`, `"View"`), pero fallan si esos nombres son distintos.

La alternativa (Opción A) sería usar `Gui.runCommand('TechDraw_RadiusDimension', 0)` etc., que abre el diálogo nativo y deja la selección al usuario. Para el MVP la implementación actual es aceptable con la restricción de nombres hardcodeados.

### Cobertura

#### Cubiertos y activos (en TechDrawWorkbench.py)

| Ticket | Comando | Archivo | Clave |
|--------|---------|---------|-------|
| `TechDraw_View` | `Gui.runCommand('TechDraw_View', 0)` | `Views/Views.py` | `'view'` |
| `TechDraw_DetailView` | `Gui.runCommand('TechDraw_DetailView', 0)` | `Views/Views.py` | `'detailView'` |
| `TechDraw_BrokenView` | `Gui.runCommand('TechDraw_BrokenView', 0)` | `Views/Views.py` | `'brokenView'` |
| `TechDraw_ClipGroup` | `Gui.runCommand('TechDraw_ClipGroup', 0)` | `Views/Views.py` | `'clipGroup'` |
| `TechDraw_ComplexSection` | `Gui.runCommand('TechDraw_ComplexSection', 0)` | `Views/Views.py` | `'complexSection'` |
| `TechDraw_DraftView` | `Gui.runCommand('TechDraw_DraftView', 0)` | `Views/Views.py` | `'draft'` |
| `TechDraw_SpreadsheetView` | `Gui.runCommand('TechDraw_SpreadsheetView', 0)` | `Views/Views.py` | `'spreadsheet'` |
| `TechDraw_VerticalDimension` | `Gui.runCommand('TechDraw_VerticalDimension', 0)` | `Dimensions/dimensions.py` | `'vertical'` |
| `TechDraw_AreaDimension` | `Gui.runCommand('TechDraw_AreaDimension', 0)` | `Dimensions/dimensions.py` | `'area'` |
| `TechDraw_HoleShaftFit` | `Gui.runCommand('TechDraw_HoleShaftFit', 0)` | `Dimensions/dimensions.py` | `'fit'` |
| `TechDraw_LengthDimension` (API) | `_create_dimension()` | `Dimensions/dimension/dimension.py` | `'dimension'` |
| `TechDraw_LengthDimension` (API) | `_create_length()` | `Dimensions/length/length.py` | `'length'` |
| `TechDraw_HorizontalDimension` (API) | `_create_horizontal()` | `Dimensions/horizontal/horizontal.py` | `'horizontal'` |
| `TechDraw_ExtentGroup` (API) | `_create_extent()` | `Dimensions/extent/extent.py` | `'extent'` |
| `TechDraw_RadiusDimension` (API) | `_create_radius()` | `Dimensions/radius/radius.py` | `'radius'` |
| `TechDraw_DiameterDimension` (API) | `_create_diameter()` | `Dimensions/diameter/diameter.py` | `'diameter'` |
| `TechDraw_AngleDimension` (API) | `_create_angle()` | `Dimensions/angle/angle.py` | `'angle'` |
| `TechDraw_3PtAngleDimension` (API) | `_create_angle_3pt()` | `Dimensions/angle/angle.py` | `'points'` |
| `TechDraw_2LineCenterLine` | `Gui.runCommand('TechDraw_2LineCenterLine', 0)` | `AddLines/addLines.py` | `'twoLines'` |
| `TechDraw_2PointCenterLine` | `Gui.runCommand('TechDraw_2PointCenterLine', 0)` | `AddLines/addLines.py` | `'twoPoints'` |
| `TechDraw_2PointCosmeticLine` | `Gui.runCommand('TechDraw_2PointCosmeticLine', 0)` | `AddLines/addLines.py` | `'cosmetic'` |
| `TechDraw_DecorateLine` | `Gui.runCommand('TechDraw_DecorateLine', 0)` | `AddLines/addLines.py` | `'decorate'` |
| `TechDraw_FaceCenterLine` | `Gui.runCommand('TechDraw_FaceCenterLine', 0)` | `AddLines/addLines.py` | `'center'` |
| `TechDraw_WeldSymbol` | `Gui.runCommand('TechDraw_WeldSymbol', 0)` | `Symbols/Symbols.py` | `'weldSymbol'` |
| `TechDraw_RichTextAnnotation` | `Gui.runCommand('TechDraw_RichTextAnnotation', 0)` | `Symbols/Symbols.py` | `'richText'` |
| `TechDraw_SurfaceFinishSymbols` | `Gui.runCommand('TechDraw_SurfaceFinishSymbols', 0)` | `Symbols/Symbols.py` | `'finish'` |
| `TechDraw_Midpoints` | `Gui.runCommand('TechDraw_Midpoints', 0)` | `Snaps/Snaps.py` | `'midpoints'` |
| `TechDraw_Quadrants` | `Gui.runCommand('TechDraw_Quadrants', 0)` | `Snaps/Snaps.py` | `'quadrants'` |
| `TechDraw_ShowAll` | `Gui.runCommand('TechDraw_ShowAll', 0)` | `Topology/Topology.py` | `'showAll'` |

#### ✅ Módulos antes huérfanos, ahora importados en `TechDraw.py` (corregido)

Verificado 2026-06-25: `TechDraw.py` (no `TechDrawWorkbench.py`) importa los 12 submódulos.

| Módulo | Tickets cubiertos | Estado |
| ------ | ---------------- | ------ |
| `Page/Page.py` | `TechDraw_PageDefault`, `TechDraw_PageTemplate`, `TechDraw_RedrawPage`, `TechDraw_PrintAll`, `TechDraw_ExportPageDXF`, `TechDraw_ExportPageSVG` | ✅ importado |
| `Annotations/annotations.py` | `TechDraw_Annotation`, `TechDraw_AxoLengthDimension`, `TechDraw_Balloon` | ✅ importado |
| `Hatching/hatching.py` | `TechDraw_GeometricHatch` | ✅ importado |
| `AddVertices/addVertices.py` | `TechDraw_CosmeticVertex` | ✅ importado |
| `OtherViews/otherViews.py` | `TechDraw_ActiveView` | ✅ importado |
| `Features/Features.py` | `TechDraw_FillTemplateFields`, `TechDraw_Image`, `TechDraw_Symbol` | ✅ importado |
| `Symbols/weld.py` | `TechDraw_WeldSymbol` (duplicado) | ✅ eliminado — cubierto por `Symbols.py` |

### Bugs TechDraw

> Estado verificado el 2026-06-25 contra el código real (`TechDraw.py`).

| # | Archivo | Problema | Estado |
|---|---------|----------|--------|
| 1 | `TechDraw.py` | No importaba `Page`, `Annotations`, `Hatching`, `AddVertices`, `OtherViews`, `Features` | ✅ Corregido — los 12 submódulos importados |
| 2 | `Views/view.py` | Archivo huérfano | ✅ Resuelto — eliminado (queda `Views.py`) |
| 3 | `Symbols/weld.py` | Duplica `TechDraw_WeldSymbol` | ✅ Resuelto — eliminado |
| 4 | `Annotations/annotations.py` | `from .help import help` (inglés) | ⚠️ Parcial — existe `ayuda.py` pero **el `help.py` sigue presente** (leftover a eliminar) |
| 5 | `Hatching/hatching.py` | `from .help import help` | ⚠️ Parcial — `ayuda.py` existe pero `help.py` sigue presente |
| 6 | `AddVertices/addVertices.py` | `from .help import help` | ⚠️ Parcial — `ayuda.py` existe pero `help.py` sigue presente |
| 7 | `OtherViews/otherViews.py` | `from .help import help` | ⚠️ Parcial — `ayuda.py` existe pero `help.py` sigue presente |
| 8 | `Dimensions/dimensions.py` | Usa `dimensions['angle'] = angle` en vez de `.update(angle)` | ⚠️ **Pendiente** — sigue usando asignación directa |
| 9 | `Dimensions/dimension/dimension.py` | `"TechDraw::DrawDimLine"` — tipo inexistente en FreeCAD 1.x | ✅ Corregido — usa `Gui.runCommand('TechDraw_LengthDimension', 0)` |
| 10 | `Snaps/Snaps.py` | Sin clave `'help'` | ✅ Corregido — expone `'help': ayuda` |
| 11 | `Topology/Topology.py` | Sin clave `'help'` | ✅ Corregido — expone `'help': ayuda` |
| 12 | `Features/Features.py` | Sin clave `'help'` | ✅ Corregido — expone `'help': ayuda` |
| 13 | `Symbols/Symbols.py` | Claves camelCase `'weldSymbol'`, `'richText'` | ✅ Corregido — `'weldsymbol'`, `'richtext'`, `'finish'` |
| 14 | `AddLines/addLines.py` | Claves camelCase `'twoLines'`, `'twoPoints'` | ✅ Corregido — `'twolines'`, `'twopoints'` |
| 15 | `Views/Views.py` | Claves camelCase `'detailView'`, etc. | ✅ Corregido — `'detailview'`, `'brokenview'`, `'clipgroup'`, `'complexsection'` |
| 16 | `TechDraw.py` | Clave de ayuda raíz es `'ayuda'` (español) — inconsistente con `'help'` que usan los demás roots y CONTEXT.md | ⚠️ **Pendiente** (nuevo) — cambiar a `'help'` |
| 17 | `Topology/Topology.py` | Clave `'showAll'` usa camelCase | ⚠️ **Pendiente** (nuevo) — renombrar a `'showall'` |

### LineAttributes (sub-módulo TechDraw)

```text
LineAttributes/
├── LineAttributes.py   ← raíz
└── attributes/
    └── attributes.py
```

Los 2 tickets de LineAttributes corresponden al TechDraw Workbench (`TechDraw_Extension*`). Están cubiertos pero tienen un bug estructural.

#### Cubiertos

| Ticket                                  | Comando                                                       | Archivo                    | Clave      |
| --------------------------------------- | ------------------------------------------------------------- | -------------------------- | ---------- |
| `Ticket_ExtensionSelectLineAttributes`  | `Gui.runCommand('TechDraw_ExtensionSelectLineAttributes', 0)` | `attributes/attributes.py` | `'select'` |
| `Ticket_ExtensionChangeLineAttributes`  | `Gui.runCommand('TechDraw_ExtensionChangeLineAttributes', 0)` | `attributes/attributes.py` | `'change'` |

#### Bugs LineAttributes

| # | Archivo | Problema | Corrección |
| -- | ------- | -------- | ---------- |
| 16 | `LineAttributes.py` | Anida `attributes` como valor (`'attributes': attributes`) en lugar de aplanarlo — el usuario tendría que decir `'attributes'` antes de llegar a `'select'` o `'change'` | Cambiar a `LineAttributes.update(attributes)` |
| 17 | `LineAttributes.py` | No usa el patrón `.update()` — es un dict literal con subdict anidado | Convertir a `LineAttributes = {}; LineAttributes.update(attributes); LineAttributes.update({'ayuda': ayuda})` |
| 18 | `attributes/attributes.py` | Verificar existencia de `LineAttributes/ayuda.py` y `LineAttributes/attributes/ayuda.py` | Confirmar o crear los archivos de ayuda |

---

## Part

### Estructura

```text
Workbench/Part/
├── Part.py                       ← raíz, usa .update() — importa los 24 sub-dicts (clave de ayuda raíz: 'ayuda')
├── box/box.py                    ✅
├── circle/circle.py              ✅
├── cone/cone.py                  ✅
├── cube/cube.py                  ✅  ← duplicado semántico de box
├── cylinder/cylinder.py          ✅
├── ellipse/ellipse.py            ✅
├── line/line.py                  ✅
├── new_sketch/new_sketch.py      ✅
├── part_chamfer/part_chamfer.py  ✅
├── part_color_per_face/...       ✅
├── part_cross_sections/...       ✅
├── part_extrude/part_extrude.py  ✅
├── part_fillet/part_fillet.py    ✅
├── part_loft/part_loft.py        ✅
├── part_makeface/part_makeface.py ✅
├── part_mirror/part_mirror.py    ✅
├── part_offset/part_offset.py    ✅
├── part_offset2d/part_offset2d.py ✅
├── part_projection_on_surface/.. ✅
├── part_revolve/part_revolve.py  ✅
├── part_ruled_surface/...        ✅
├── part_scale/part_scale.py      ✅
├── part_section/part_section.py  ✅
└── part_sweep/part_sweep.py      ✅
```

### Cobertura (24 sub-dicts, todos activos)

> Actualizado 2026-06-03: los 16 `part_*` migrados a Opción B (API directa `doc.addObject`).

| Sub-dict | Claves expuestas | Comando / API | Estado |
|----------|-----------------|---------------|--------|
| `box` | `'box'` | `Part::Box` (API directa) | ✅ |
| `circle` | `'circle'` | `Part::Circle` (API directa) | ✅ |
| `cone` | `'cone'`, `'primitive cone'` | `Part::Cone` (API directa) | ✅ — clave con espacio pendiente (Bug 2) |
| `cube` | `'cube'` | `Part::Box` (API directa) | ✅ — duplicado semántico (Bug 1) |
| `cylinder` | `'cylinder'`, `'primitive cylinder'` | `Part::Cylinder` (API directa) | ✅ — clave con espacio pendiente (Bug 2) |
| `ellipse` | `'ellipse'` | `Part::Ellipse` (API directa) | ✅ |
| `line` | `'line'` | `Part::Line` (API directa) | ✅ |
| `new_sketch` | `'nuevo boceto'`, `'nuevo sketch'`, `'crear sketch'` | `Sketcher::SketchObject` | ✅ — claves en español con espacios (Bug 2); pertenece a Sketcher (Bug 3) |
| `part_chamfer` | `'chaflan'`, `'chaflán'`, `'biselar'` | `doc.addObject("Part::Chamfer")` + `.Base` + selección previa | ✅ Opción B |
| `part_color_per_face` | `'pintar cara'`, `'color por cara'`, `'colorear cara'` | valida selección → `Gui.runCommand('Part_ColorPerFace', 0)` | ✅ Híbrido (sin API de documento equivalente) |
| `part_cross_sections` | `'secciones transversales'`, `'cross sections'` | valida selección → `Gui.runCommand('Part_CrossSections', 0)` | ✅ Híbrido (sin API de documento equivalente) |
| `part_extrude` | `'extruir'`, `'extrude'`, `'extruir objeto'` | `doc.addObject("Part::Extrusion")` + `.Base`, `.Dir`, `.Solid` | ✅ Opción B — 10 mm en Z por defecto |
| `part_fillet` | `'redondear bordes'`, `'fillet'`, `'redondear'` | `doc.addObject("Part::Fillet")` + `.Base` | ✅ Opción B |
| `part_loft` | `'hacer loft'`, `'loft'`, `'unir perfiles'` | `doc.addObject("Part::Loft")` + `.Sections` (mín. 2 objetos) | ✅ Opción B |
| `part_makeface` | `'crear cara'`, `'make face'`, `'cara'` | `Part.makeFilledFace(wires)` → `Part::Feature` | ✅ Opción B |
| `part_mirror` | `'espejo'`, `'reflejar'`, `'mirror'` | `doc.addObject("Part::Mirroring")` + `.Source`, `.Normal`, `.Base` | ✅ Opción B — plano XY por defecto |
| `part_offset` | `'desfase'`, `'offset'`, `'ensanchar'`, `'encoger'` | `doc.addObject("Part::Offset3D")` + `.Source`, `.Value = 1.0` | ✅ Opción B |
| `part_offset2d` | `'contorno'`, `'borde'`, `'offset 2d'` | `doc.addObject("Part::Offset2D")` + `.Source`, `.Value = 1.0` | ✅ Opción B |
| `part_projection_on_surface` | `'proyectar dibujo'`, `'proyectar'`, `'projection'` | `doc.addObject("Part::ProjectionOnSurface")` + `.SupportObject` + `.addProjectedObject()` | ✅ Opción B (mín. 2 objetos) |
| `part_revolve` | `'revolucion'`, `'revolución'`, `'revolve'` | `doc.addObject("Part::Revolution")` + `.Source`, `.Axis`, `.Angle = 360` | ✅ Opción B — eje Z, 360° por defecto |
| `part_ruled_surface` | `'superficie reglada'`, `'unir curvas'`, `'ruled surface'` | `doc.addObject("Part::RuledSurface")` + `.Curve1`, `.Curve2` (2 objetos) | ✅ Opción B |
| `part_scale` | `'escalar'`, `'agrandar'`, `'reducir'`, `'scale'` | `doc.addObject("Part::Scale")` + `.Base`, `.Uniform = True`, `.UniformScale = 2.0` | ✅ Opción B — factor 2× por defecto |
| `part_section` | `'intersección'`, `'obtener sección'`, `'section'` | `doc.addObject("Part::Section")` + `.Base`, `.Tool` (2 objetos) | ✅ Opción B |
| `part_sweep` | `'barrer perfil'`, `'sweep'`, `'barrido'` | `doc.addObject("Part::Sweep")` + `.Sections`, `.Spine` (perfil + camino) | ✅ Opción B |

### Bugs Part

> Bugs 4–13 corregidos el 2026-06-03 al migrar los 16 `part_*` a Opción B. Bugs 1–3 pendientes.

| # | Archivo | Problema | Estado |
|---|---------|----------|--------|
| 1 | `cube/cube.py` | `_create_cube()` es duplicado semántico de `box.py` — ambos crean `Part::Box`; `'cube'` podría ser alias en `box.py` | ⚠️ Pendiente — evaluar si es alias necesario |
| 2 | `cone/cone.py`, `cylinder/cylinder.py`, `new_sketch/new_sketch.py`, `part_cross_sections/...` y otros | Claves con espacios (`'primitive cone'`, `'nuevo boceto'`, `'cross sections'`) incompatibles con tokens Vosk | ⚠️ Pendiente — renombrar a `'primitivecone'`, `'nuevoboceto'`, `'crosssections'` |
| 3 | `new_sketch/new_sketch.py` | Crea `Sketcher::SketchObject` desde Part — ya cubierto en Sketcher; comando correcto: `Gui.runCommand('Sketcher_NewSketch', 0)` | ⚠️ Pendiente — mover o eliminar |
| 4–13 | `part_chamfer`, `part_fillet`, `part_extrude`, `part_mirror`, `part_revolve`, `part_loft`, `part_sweep`, `part_ruled_surface`, `part_section`, `part_offset`, `part_offset2d`, `part_projection_on_surface`, `part_makeface`, `part_color_per_face`, `part_cross_sections`, `part_scale` | Bugs originales: `.Source`/`.Base` sin asignar, tipos inexistentes (`Part::Scaled`, `Part::Face`, `Part::Compound`), `doc.getSelection()` inexistente, `Std_SetAppearance` incorrecto | ✅ Corregidos 2026-06-03 — migrados a Opción B con API correcta |

---

## Resumen general de cobertura

> Actualizado 2026-06-25 tras contrastar con el código real.

| Módulo | Tickets | Cubiertos | Faltantes | Estado |
|--------|---------|-----------|-----------|--------|
| Assembly | 22 | 22 | 0 | ✅ Completo |
| DraftWork | 59 | 59 activos (todos importados) | 1 (`Draft_Line`) | ⚠️ Falta nomenclatura en `modification.py` |
| PartDesign | 36 | 36 | 0 | ✅ Completo (con duplicados) |
| Sketcher | 97 | 94 | 1 (`refraction`) + 2 no aplica | ⚠️ Casi completo |
| Part | 24 sub-dicts, todos activos | 24 | 0 | ⚠️ Funcional (Opción B); falta limpieza de claves |
| TechDraw | 44 activos (todos importados) | 44 | 0 | ⚠️ Funcional; falta limpieza menor (`'ayuda'` raíz, `'showAll'`, leftovers `help.py`) |
