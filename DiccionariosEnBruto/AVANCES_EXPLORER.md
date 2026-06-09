# Avances — Módulo Explorer

> Revisado: 2026-06-03 — Bugs #1–#8 corregidos

---

## Estructura de archivos

```
Explorer/
├── Explorer.py                  ← raíz, usa .update()
├── AdditionalTools/Additional.py
├── Edit/Edit.py
├── Expressions/Expressions.py
├── File/File.py
├── Print/Print.py
├── StructureToolbar/
│   ├── structure.py
│   └── linkActions/link.py
├── Tools/Tools.py
└── Windows/Windows.py
```

---

## Cobertura de tickets (59 tickets Explorer)

### ✅ Cubiertos correctamente

| Ticket | Comando | Archivo | Clave |
|--------|---------|---------|-------|
| `Std_New` | `FreeCAD.newDocument()` | `File.py` | `'new'` |
| `Std_Open` | `Gui.runCommand('Std_Open', 0)` | `File.py` | `'open'` |
| `Std_Save` | `FreeCAD.activeDocument().save()` | `File.py` | `'save'` |
| `Std_SaveAs` | `Gui.runCommand('Std_SaveAs', 0)` | `File.py` | `'saveas'` |
| `Std_SaveCopy` | `Gui.runCommand('Std_SaveCopy', 0)` | `File.py` | `'savecopy'` |
| `Std_Revert` | `Gui.runCommand('Std_Revert', 0)` | `File.py` | `'revert'` |
| `Std_Import` | `Gui.runCommand('Std_Import', 0)` | `File.py` | `'import'` |
| `Std_Export` | `Gui.runCommand('Std_Export', 0)` | `File.py` | `'export'` |
| `Std_RecentFiles` | `Gui.runCommand('Std_RecentFiles', 0)` | `File.py` | `'recent'` |
| `Std_ViewLoadImage` | `Gui.runCommand('Std_ViewLoadImage', 0)` | `File.py` | `'loadimage'` |
| `Std_MergeProjects` | `Gui.runCommand('Std_MergeProjects', 0)` | `File.py` | `'merge'` |
| `Std_Undo` | `Gui.runCommand('Std_Undo', 0)` | `Edit.py` | `'undo'` |
| `Std_Redo` | `Gui.runCommand('Std_Redo', 0)` | `Edit.py` | `'redo'` |
| `Std_Cut` | `Gui.runCommand('Std_Cut', 0)` | `Edit.py` | `'cut'` |
| `Std_Copy` | `Gui.runCommand('Std_Copy', 0)` | `Edit.py` | `'copy'` |
| `Std_Paste` | `Gui.runCommand('Std_Paste', 0)` | `Edit.py` | `'paste'` |
| `Std_DuplicateSelection` | `Gui.runCommand('Std_DuplicateSelection', 0)` | `Edit.py` | `'duplicate'` |
| `Std_SelectAll` | `Gui.runCommand('Std_SelectAll', 0)` | `Edit.py` | `'selectall'` |
| `Std_Delete` | `Gui.runCommand('Std_Delete', 0)` | `Edit.py` | `'delete'` |
| `Std_Placement` | `Gui.runCommand('Std_Placement', 0)` | `Edit.py` | `'placement'` |
| `Std_TransformManip` | `Gui.runCommand('Std_TransformManip', 0)` | `Edit.py` | `'transform'` |
| `Std_Alignment` | `Gui.runCommand('Std_Alignment', 0)` | `Edit.py` | `'align'` |
| `Std_DlgPreferences` | `Gui.runCommand('Std_DlgPreferences', 0)` | `Edit.py` | `'preferences'` |
| `Std_Properties` | `Gui.runCommand('Std_Properties', 0)` | `Edit.py` | `'properties'` |
| `Std_SendToPythonConsole` | `Gui.runCommand('Std_SendToPythonConsole', 0)` | `Edit.py` | `'sendtopython'` |
| `Std_UserEditMode` | `Gui.runCommand('Std_UserEditMode', 0)` | `Edit.py` | `'editmode'` |
| `Std_Print` | `Gui.runCommand('Std_Print', 0)` | `Print.py` | `'print'` |
| `Std_PrintPdf` | `Gui.runCommand('Std_PrintPdf', 0)` | `Print.py` | `'pdf'` |
| `Std_Expressions_CopyActiveDocument` | `Gui.runCommand('Std_Expressions_CopyActiveDocument', 0)` | `Expressions.py` | `'copyactdoc'` |
| `Std_Expressions_CopyAllDocuments` | `Gui.runCommand('Std_Expressions_CopyAllDocuments', 0)` | `Expressions.py` | `'copyalldoc'` |
| `Std_Expressions_CopySelected` | `Gui.runCommand('Std_Expressions_CopySelected', 0)` | `Expressions.py` | `'copyselected'` |
| `Std_Expressions_Paste` | `Gui.runCommand('Std_Expressions_Paste', 0)` | `Expressions.py` | `'pasteexpr'` |
| `Std_Measure` | `Gui.runCommand('Std_Measure', 0)` | `Tools.py` | `'measure'` |
| `Std_ClarifySelection` | `Gui.runCommand('Std_ClarifySelection', 0)` | `Tools.py` | `'clarifyselection'` |
| `Std_DemoMode` | `Gui.runCommand('Std_DemoMode', 0)` | `Tools.py` | `'demomode'` |
| `Std_DlgCustomize` | `Gui.runCommand('Std_DlgCustomize', 0)` | `Tools.py` | `'customize'` |
| `Std_DlgParameter` | `Gui.runCommand('Std_DlgParameter', 0)` | `Tools.py` | `'editparameters'` |
| `Std_ProjectUtil` | `Gui.runCommand('Std_ProjectUtil', 0)` | `Tools.py` | `'projectutil'` |
| `Std_Refresh` | `Gui.runCommand('Std_Refresh', 0)` | `Explorer.py` | `'refresh'` |
| `Std_ViewScreenShot` | `Gui.runCommand('Std_ViewScreenShot', 0)` | `Explorer.py` | `'screenshot'` |
| `Std_TextDocument` | `Gui.runCommand('Std_TextDocument', 0)` | `Explorer.py` | `'textdoc'` |
| `Std_LinkUnlink` | `Gui.runCommand('Std_LinkUnlink', 0)` | `Explorer.py` | `'unlink'` |
| `Std_ToggleFreeze` | `Gui.runCommand('Std_ToggleFreeze', 0)` | `Explorer.py` | `'freeze'` |
| `Std_TreeSelectAllInstances` | `Gui.runCommand('Std_TreeSelectAllInstances', 0)` | `Explorer.py` | `'allinstances'` |
| `Std_VarSet` | `Gui.runCommand('Std_VarSet', 0)` | `Explorer.py` | `'variableset'` |
| `Std_CloseActiveWindow` | `Gui.runCommand('Std_CloseActiveWindow', 0)` | `Windows.py` | `'close'` |
| `Std_CloseAllWindows` | `Gui.runCommand('Std_CloseAllWindows', 0)` | `Windows.py` | `'closeall'` |
| `Std_Quit` | `Gui.getMainWindow().close()` | `Windows.py` | `'quit'` |
| `Std_Group` | `Gui.runCommand('Std_Group', 0)` | `structure.py` | `'newgroup'` |
| `Std_Part` | `Gui.runCommand('Std_Part', 0)` | `structure.py` | `'part'` |
| `Std_LinkMake` | `Gui.runCommand('Std_LinkMake', 0)` | `link.py` | `'makelink'` |
| `Std_LinkMakeRelative` | `Gui.runCommand('Std_LinkMakeRelative', 0)` | `link.py` | `'relativelink'` |
| `Std_LinkImport` | `Gui.runCommand('Std_LinkImport', 0)` | `link.py` | `'importlink'` |
| `Std_LinkImportAll` | `Gui.runCommand('Std_LinkImportAll', 0)` | `link.py` | `'importalllinks'` |
| `Std_LinkReplace` | `Gui.runCommand('Std_LinkReplace', 0)` | `link.py` | `'replacelink'` |
| `Std_LinkMakeGroup` | `Gui.runCommand('Std_LinkMakeGroup', 0)` | `Additional.py` | `'linkgroups'` |

### ⚠️ Cubiertos con API alternativa (aceptable)

| Ticket | Script del ticket | Dict actual | Nota |
|--------|------------------|-------------|------|
| `doc_undo` | `App.ActiveDocument.undo()` | `edit['undo']` → `Gui.runCommand('Std_Undo', 0)` | Hay ticket separado `Std_Undo` que cubre lo mismo por GUI |
| `doc_redo` | `App.ActiveDocument.redo()` | `edit['redo']` → `Gui.runCommand('Std_Redo', 0)` | Idem |
| `Std_Export` | `Part.export(seleccion, path)` | `file['export']` → `Gui.runCommand('Std_Export', 0)` | El ticket usa API para exportar con ruta fija; la GUI es preferible para MVP |

---

## Bugs corregidos ✅

| # | Archivo | Problema | Corrección aplicada |
|---|---------|----------|---------------------|
| 1 | `Tools/Tools.py` | `'clarify selection'` tiene espacio — viola convención (1 palabra) | → `'clarifyselection'` |
| 2 | `Tools/Tools.py` | `'proyectutil'` — typo, falta la "j" | → `'projectutil'` |
| 3 | `StructureToolbar/structure.py` | `'new Group'` y `'link actions'` tienen espacios en las claves | → `'newgroup'`, `'linkactions'` |
| 4 | `StructureToolbar/linkActions/link.py` | `'make link'`, `'relative link'`, `'import link'`, `'import all links'`, `'replace link'` — todas con espacios | → `'makelink'`, `'relativelink'`, `'importlink'`, `'importalllinks'`, `'replacelink'` |
| 5 | `Explorer.py` | `StructureToolbar/structure` y `AdditionalTools/Additional` no estaban importados — módulos huérfanos | Importados y agregados al `.update()` |
| 6 | `Edit.py` | `'screenshot'` y `'note'` duplicados respecto a `Explorer.py` | Eliminados de `Edit.py` |
| 7 | `Edit.py`, `Tools.py`, `Expressions.py` | Cabezal duplicado (dos líneas `Copyright`) | Unificado a un solo bloque GPL-3.0 |
| 8 | `Expressions.py` | `'paste'` colisionaba con `edit['paste']` al aplanar con `.update()` | → `'pasteexpr'` |

---

## Tickets sin cobertura

Ninguno. Todos los 59 tickets de Explorer tienen cobertura en algún archivo del módulo.

> **Nota:** `Std_Group`, `Std_Part` y los `Std_Link*` están en `StructureToolbar/` — bug #5 corregido, ya están importados y activos en `Explorer.py`.
