# Avances — Módulo StdView

> Revisado: 2026-06-03 · Estado: ✅ Diccionarios listos

---

## Estructura de archivos

```
StdView/
├── StdView.py                  ← raíz, usa .update()
├── Appearance/Appearance.py
├── Camera/Camera.py
├── Clipping/Clipping.py
├── DrawStyles/DrawStyles.py
├── Material/Material.py
├── Overlay/Overlay.py
├── Panels/Panels.py
├── SavedViews/SavedViews.py
├── StandardViews/StandardViews.py
├── Stereo/Stereo.py
├── Toolbars/Toolbars.py
├── Tree/Tree.py
└── Visibility/Visibility.py
```

---

## Cobertura de tickets (99 tickets StdView)

### ✅ Cubiertos correctamente

| Ticket | Comando | Archivo | Clave |
|--------|---------|---------|-------|
| `StdOrthographicCamera` | `Gui.runCommand('Std_OrthographicCamera', 1)` | `Camera.py` | `'orthographic'` |
| `StdPerspectiveCamera` | `Gui.runCommand('Std_PerspectiveCamera', 1)` | `Camera.py` | `'perspective'` |
| `StdDrawStyleAsIs` | `Gui.runCommand('Std_DrawStyleAsIs', 0)` | `DrawStyles.py` | `'styleasis'` |
| `StdDrawStyleFlatLines` | `Gui.runCommand('Std_DrawStyleFlatLines', 0)` | `DrawStyles.py` | `'flatlines'` |
| `StdDrawStyleHiddenLine` | `Gui.runCommand('Std_DrawStyleHiddenLine', 0)` | `DrawStyles.py` | `'hiddenline'` |
| `StdDrawStyleNoShading` | `Gui.runCommand('Std_DrawStyleNoShading', 0)` | `DrawStyles.py` | `'noshading'` |
| `StdDrawStylePoints` | `Gui.runCommand('Std_DrawStylePoints', 0)` | `DrawStyles.py` | `'points'` |
| `StdDrawStyleShaded` | `Gui.runCommand('Std_DrawStyleShaded', 0)` | `DrawStyles.py` | `'shaded'` |
| `StdDrawStyleWireframe` | `Gui.runCommand('Std_DrawStyleWireframe', 0)` | `DrawStyles.py` | `'wireframe'` |
| `StdOverlayToggleBottom` | `Gui.runCommand('Std_OverlayToggleBottom', 0)` | `Overlay.py` | `'bottom'` |
| `StdOverlayToggleFloating` | `Gui.runCommand('Std_OverlayToggleFloating', 0)` | `Overlay.py` | `'float'` |
| `StdOverlayToggleLeft` | `Gui.runCommand('Std_OverlayToggleLeft', 0)` | `Overlay.py` | `'left'` |
| `StdOverlayToggleRight` | `Gui.runCommand('Std_OverlayToggleRight', 0)` | `Overlay.py` | `'right'` |
| `StdToggleOverlay` | `Gui.runCommand('Std_ToggleOverlay', 0)` | `Overlay.py` | `'toggle'` |
| `StdToggleAxisCross` | `Gui.runCommand('Std_AxisCross', 0)` | `Overlay.py` | `'axis'` |
| `StdToggleNavigationEditMode` | `Gui.runCommand('Std_ToggleNavigation', 0)` | `Overlay.py` | `'navigation'` |
| `StdDockedPanel` | `Gui.runCommand('Std_PanelView', 0)` | `Panels.py` | `'panel'` |
| `StdDocumentWindowDocked` | `Gui.runCommand('Std_DockView', 0)` | `Panels.py` | `'dock'` |
| `StdDocumentWindowFullscreen` | `Gui.runCommand('Std_ViewFullscreen', 0)` | `Panels.py` | `'fullscreen'` |
| `StdDocumentWindowUndocked` | `Gui.runCommand('Std_UndockView', 0)` | `Panels.py` | `'undock'` |
| `StdPanelDAGView` | `Gui.runCommand('Std_DAGView', 0)` | `Panels.py` | `'dagview'` |
| `StdPanelModel` | `Gui.runCommand('Std_ComboView', 0)` | `Panels.py` | `'comboview'` |
| `StdPanelSelectionView` | `Gui.runCommand('Std_SelectionView', 0)` | `Panels.py` | `'selectionview'` |
| `StdPanelTasks` | `Gui.runCommand('Std_TaskView', 0)` | `Panels.py` | `'tasks'` |
| `StdPanelsPropertyView` | `Gui.runCommand('Std_PropertyView', 0)` | `Panels.py` | `'properties'` |
| `StdPanelsPythonConsole` | `Gui.runCommand('Std_PythonConsole', 0)` | `Panels.py` | `'console'` |
| `StdPanelsReportView` | `Gui.runCommand('Std_ReportView', 0)` | `Panels.py` | `'report'` |
| `StdPanelsTreeView` | `Gui.runCommand('Std_TreeView', 0)` | `Panels.py` | `'treeview'` |
| `StdViewStatusBar` | `Gui.runCommand('Std_ViewStatusBar', 0)` | `Panels.py` | `'statusbar'` |
| `StdClearViews` | `Gui.runCommand('Std_ClearViews', 0)` | `SavedViews.py` | `'clear'` |
| `StdFreezeView` | `Gui.runCommand('Std_FreezeView', 0)` | `SavedViews.py` | `'freeze'` |
| `StdLoadViews` | `Gui.runCommand('Std_FreezeViewsRestore', 0)` | `SavedViews.py` | `'restore'` |
| `StdRecallWorkingView` | `Gui.runCommand('Std_RecallWorkingView', 0)` | `SavedViews.py` | `'recall'` |
| `StdRestoreView` | `Gui.runCommand('Std_RestoreView', 0)` | `SavedViews.py` | `'load'` |
| `StdSaveViews` | `Gui.runCommand('Std_FreezeViewsSave', 0)` | `SavedViews.py` | `'save'` |
| `StdStoreWorkingView` | `Gui.runCommand('Std_StoreWorkingView', 0)` | `SavedViews.py` | `'store'` |
| `StdViewBottom` | `Gui.runCommand('Std_ViewBottom', 0)` | `StandardViews.py` | `'bottom'` |
| `StdViewBoxZoom` | `Gui.runCommand('Std_ViewBoxZoom', 0)` | `StandardViews.py` | `'boxzoom'` |
| `StdViewCreate` | `Gui.runCommand('Std_ViewCreate', 0)` | `StandardViews.py` | `'newview'` |
| `StdViewDimetric` | `Gui.runCommand('Std_ViewDimetric', 0)` | `StandardViews.py` | `'dimetric'` |
| `StdViewFitAll` | `Gui.runCommand('Std_ViewFitAll', 0)` | `StandardViews.py` | `'fitall'` |
| `StdViewFitSelection` | `Gui.runCommand('Std_ViewFitSelection', 0)` | `StandardViews.py` | `'fitselection'` |
| `StdViewFront` | `Gui.runCommand('Std_ViewFront', 0)` | `StandardViews.py` | `'front'` |
| `StdViewFullscreen` | `Gui.runCommand('Std_ViewFullscreen', 0)` | `StandardViews.py` | `'fullscreen'` |
| `StdViewHome` | `Gui.runCommand('Std_ViewHome', 0)` | `StandardViews.py` | `'home'` |
| `StdViewIsometric` | `Gui.runCommand('Std_ViewIsometric', 0)` | `StandardViews.py` | `'isometric'` |
| `StdViewLeft` | `Gui.runCommand('Std_ViewLeft', 0)` | `StandardViews.py` | `'left'` |
| `StdViewRear` | `Gui.runCommand('Std_ViewRear', 0)` | `StandardViews.py` | `'rear'` |
| `StdViewRight` | `Gui.runCommand('Std_ViewRight', 0)` | `StandardViews.py` | `'right'` |
| `StdViewTop` | `Gui.runCommand('Std_ViewTop', 0)` | `StandardViews.py` | `'top'` |
| `StdViewTrimetric` | `Gui.runCommand('Std_ViewTrimetric', 0)` | `StandardViews.py` | `'trimetric'` |
| `StdViewZoomIn` | `Gui.runCommand('Std_ViewZoomIn', 0)` | `StandardViews.py` | `'zoomin'` |
| `StdViewZoomOut` | `Gui.runCommand('Std_ViewZoomOut', 0)` | `StandardViews.py` | `'zoomout'` |
| `StdViewIvIssueCamPos` | `Gui.runCommand('Std_ViewIvIssueCamPos', 0)` | `Stereo.py` | `'camerapos'` |
| `StdViewIvStereoInterleavedColumns` | `Gui.runCommand('Std_ViewIvStereoInterleavedColumns', 0)` | `Stereo.py` | `'stereocolumns'` |
| `StdViewIvStereoInterleavedRows` | `Gui.runCommand('Std_ViewIvStereoInterleavedRows', 0)` | `Stereo.py` | `'stereorows'` |
| `StdViewIvStereoOff` | `Gui.runCommand('Std_ViewIvStereoOff', 0)` | `Stereo.py` | `'stereooff'` |
| `StdViewIvStereoQuadBuff` | `Gui.runCommand('Std_ViewIvStereoQuadBuff', 0)` | `Stereo.py` | `'stereoquad'` |
| `StdViewIvStereoRedGreen` | `Gui.runCommand('Std_ViewIvStereoRedGreen', 0)` | `Stereo.py` | `'stereoanaglyph'` |
| `StdToolbarClipboard` | `Gui.runCommand('Std_ToolbarClipboard', 0)` | `Toolbars.py` | `'clipboard'` |
| `StdToolbarEdit` | `Gui.runCommand('Std_ToolbarEdit', 0)` | `Toolbars.py` | `'edit'` |
| `StdToolbarFile` | `Gui.runCommand('Std_ToolbarFile', 0)` | `Toolbars.py` | `'file'` |
| `StdToolbarHelp` | `Gui.runCommand('Std_ToolbarHelp', 0)` | `Toolbars.py` | `'toolbarshelp'` |
| `StdToolbarIndividualViews` | `Gui.runCommand('Std_ToolbarIndividualViews', 0)` | `Toolbars.py` | `'views'` |
| `StdToolbarLockToolbars` | `Gui.runCommand('Std_ToggleToolbarsLock', 0)` | `Toolbars.py` | `'lock'` |
| `StdToolbarMacro` | `Gui.runCommand('Std_ToolbarMacro', 0)` | `Toolbars.py` | `'macro'` |
| `StdToolbarStructure` | `Gui.runCommand('Std_ToolbarStructure', 0)` | `Toolbars.py` | `'structure'` |
| `StdToolbarView` | `Gui.runCommand('Std_ToolbarView', 0)` | `Toolbars.py` | `'view'` |
| `StdToolbarWorkbench` | `Gui.runCommand('Std_ToolbarWorkbench', 0)` | `Toolbars.py` | `'workbench'` |
| `StdTreeCollapseDocument` | `Gui.runCommand('Std_TreeCollapseDocument', 0)` | `Tree.py` | `'collapse'` |
| `StdTreePreSelection` | `Gui.runCommand('Std_TreePreSelection', 0)` | `Tree.py` | `'preselection'` |
| `StdTreeRecordSelection` | `Gui.runCommand('Std_TreeRecordSelection', 0)` | `Tree.py` | `'recordselection'` |
| `StdTreeSingleExpand` | `Gui.runCommand('Std_TreeSingleExpand', 0)` | `Tree.py` | `'singleexpand'` |
| `StdTreeSyncPlacement` | `Gui.runCommand('Std_TreeSyncPlacement', 0)` | `Tree.py` | `'syncplacement'` |
| `StdTreeSyncSelection` | `Gui.runCommand('Std_TreeSyncSelection', 0)` | `Tree.py` | `'syncselection'` |
| `StdTreeSyncView` | `Gui.runCommand('Std_TreeSyncView', 0)` | `Tree.py` | `'syncview'` |
| `StdHideAllObjects` | `Gui.runCommand('Std_HideObjects', 0)` | `Visibility.py` | `'hideobjects'` |
| `StdHideSelection` | `Gui.runCommand('Std_HideSelection', 0)` | `Visibility.py` | `'hide'` |
| `StdLinkSelectAllLinks` | `Gui.runCommand('Std_LinkSelectAllLinks', 0)` | `Visibility.py` | `'alllinks'` |
| `StdLinkSelectLinked` | `Gui.runCommand('Std_LinkSelectLinked', 0)` | `Visibility.py` | `'linked'` |
| `StdLinkSelectLinkedFinal` | `Gui.runCommand('Std_LinkSelectLinkedFinal', 0)` | `Visibility.py` | `'linkedfinal'` |
| `StdSelBack` | `Gui.runCommand('Std_SelBack', 0)` | `Visibility.py` | `'selback'` |
| `StdSelForward` | `Gui.runCommand('Std_SelForward', 0)` | `Visibility.py` | `'selforward'` |
| `StdSelectVisibleObjects` | `Gui.runCommand('Std_SelectVisibleObjects', 0)` | `Visibility.py` | `'selectvisible'` |
| `StdShowAllObjects` | `Gui.runCommand('Std_ShowObjects', 0)` | `Visibility.py` | `'showobjects'` |
| `StdShowSelection` | `Gui.runCommand('Std_ShowSelection', 0)` | `Visibility.py` | `'show'` |
| `StdToggleAllObjects` | `Gui.runCommand('Std_ToggleObjects', 0)` | `Visibility.py` | `'toggleall'` |
| `StdToggleSelectability` | `Gui.runCommand('Std_ToggleSelectability', 0)` | `Visibility.py` | `'selectability'` |
| `StdToggleTransparency` | `Gui.runCommand('Std_ToggleTransparency', 0)` | `Visibility.py` | `'transparency'` |
| `StdToggleVisibility` | `Gui.runCommand('Std_ToggleVisibility', 0)` | `Visibility.py` | `'toggle'` |
| `StdAlignToSelection` | `Gui.runCommand('Std_AlignToSelection', 0)` | `Visibility.py` | `'aligntoselection'` |
| `StdAppearance` | `Gui.runCommand('Std_SetAppearance', 0)` | `Appearance.py` | `'appearance'` |
| `StdAppearancePerFace` | `Gui.runCommand('Part_FaceColors', 0)` | `Appearance.py` | `'facecolors'` |
| `StdRandomColor` | `Gui.runCommand('Std_RandomColor', 0)` | `Appearance.py` | `'randomcolor'` |
| `StdTextureMapping` | `Gui.runCommand('Std_TextureMapping', 0)` | `Appearance.py` | `'texturemapping'` |
| `StdMaterial` | `Gui.runCommand('Std_SetMaterial', 0)` | `Material.py` | `'material'` |
| `StdClippingView` | `Gui.runCommand('Std_ToggleClipPlane', 0)` | `Clipping.py` | `'clipping'` |
| `StdSelBoundingBox` | `Gui.runCommand('Std_SelBoundingBox', 0)` | `Visibility.py` | `'boundingbox'` |

### ⚠️ Cubiertos con API alternativa (aceptable)

| Ticket | Script del ticket | Dict actual | Nota |
|--------|------------------|-------------|------|
| `StdViewZoomIn` | `view.zoomIn()` | `StandardViews['zoomin']` → `Gui.runCommand('Std_ViewZoomIn', 0)` | ✅ `runCommand` equivalente válido para MVP |
| `StdViewZoomOut` | `view.zoomOut()` | `StandardViews['zoomout']` → `Gui.runCommand('Std_ViewZoomOut', 0)` | ✅ `runCommand` equivalente válido para MVP |
| `StdWorkbench` | `Gui.activateWorkbench('NombreWorkbench')` | `toolbars['workbench']` → `Std_ToolbarWorkbench` | ⚠️ Semántica distinta: el ticket cambia el workbench activo; el dict muestra/oculta la toolbar de workbenches |
| Stereo Iv* | `view.setStereoType('...')` | `Stereo.py` usa `Gui.runCommand('Std_ViewIvStereo*')` | ✅ ambos métodos funcionan |
| Toolbars (9 tickets Qt) | Solo Qt — no hay `runCommand` directo | `Toolbars.py` usa `Gui.runCommand('Std_Toolbar*')` | ✅ aproximación aceptable para MVP |

---

## Notas de implementación

- Todos los subdiccionarios exponen `'help': ayuda` para ayuda contextual por voz.
- `Toolbars.py`: la clave para mostrar/ocultar la barra de ayuda de FreeCAD es `'toolbarshelp'` (no `'help'`, para evitar colisión con la función de ayuda del módulo).
- `Panels.py`: la variable exportada es `Panels` (mayúscula), consistente con el import en `StdView.py`.
- `Appearance.py`: la clave `'facecolors'` (todo minúsculas) respeta la convención del proyecto.
- `aligntoselection` está en `Visibility.py` (operación de selección de cámara, no una vista estándar).
