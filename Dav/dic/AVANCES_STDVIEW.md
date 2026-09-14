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
| `StdDrawStyleAsIs` | `Gui.runCommand('Std_DrawStyle', 0)` | `DrawStyles.py` | `'styleasis'` |
| `StdDrawStylePoints` | `Gui.runCommand('Std_DrawStyle', 1)` | `DrawStyles.py` | `'points'` |
| `StdDrawStyleWireframe` | `Gui.runCommand('Std_DrawStyle', 2)` | `DrawStyles.py` | `'wireframe'` |
| `StdDrawStyleHiddenLine` | `Gui.runCommand('Std_DrawStyle', 3)` | `DrawStyles.py` | `'hiddenline'` |
| `StdDrawStyleNoShading` | `Gui.runCommand('Std_DrawStyle', 4)` | `DrawStyles.py` | `'noshading'` |
| `StdDrawStyleShaded` | `Gui.runCommand('Std_DrawStyle', 5)` | `DrawStyles.py` | `'shaded'` |
| `StdDrawStyleFlatLines` | `Gui.runCommand('Std_DrawStyle', 6)` | `DrawStyles.py` | `'flatlines'` |
| `StdOverlayToggleBottom` | `Gui.runCommand('Std_DockOverlay', 11)` | `Overlay.py` | `'bottom'` |
| `StdOverlayToggleFloating` | `_toggle_floating()` (Qt `setFloating`) | `Overlay.py` | `'float'` |
| `StdOverlayToggleLeft` | `Gui.runCommand('Std_DockOverlay', 8)` | `Overlay.py` | `'left'` |
| `StdOverlayToggleRight` | `Gui.runCommand('Std_DockOverlay', 9)` | `Overlay.py` | `'right'` |
| `StdToggleOverlay` | `Gui.runCommand('Std_DockOverlay', 3)` | `Overlay.py` | `'toggle'` |
| `StdToggleAxisCross` | `Gui.runCommand('Std_AxisCross', 0)` | `Overlay.py` | `'axis'` |
| `StdToggleNavigationEditMode` | `Gui.runCommand('Std_ToggleNavigation', 0)` | `Overlay.py` | `'navigation'` |
| `StdDockedPanel` | `_toggle_panel(['DAV_Panel', 'Std_ComboView', ...])` | `Panels.py` | `'panel'` |
| `StdDocumentWindowDocked` | `_dock_window()` (`Std_ViewDockUndockFullscreen`, 0) | `Panels.py` | `'dock'` |
| `StdDocumentWindowFullscreen` | `_toggle_fullscreen()` (`Std_MainFullscreen` / Qt) | `Panels.py` | `'fullscreen'` |
| `StdDocumentWindowUndocked` | `_undock_window()` (`Std_ViewDockUndockFullscreen`, 1) | `Panels.py` | `'undock'` |
| `StdPanelDAGView` | `_toggle_panel(['Std_DAGView', ...])` | `Panels.py` | `'dagview'` |
| `StdPanelModel` | `_toggle_panel(['Std_ComboView', 'Model', ...])` | `Panels.py` | `'comboview'` |
| `StdPanelSelectionView` | `_toggle_panel(['Std_SelectionView', ...])` | `Panels.py` | `'selectionview'` |
| `StdPanelTasks` | `_toggle_panel(['Std_TaskView', ...])` | `Panels.py` | `'tasks'` |
| `StdPanelsPropertyView` | `_toggle_panel(['Std_PropertyView', ...])` | `Panels.py` | `'properties'` |
| `StdPanelsPythonConsole` | `_toggle_panel(['Std_PythonView', ...])` | `Panels.py` | `'console'` |
| `StdPanelsReportView` | `_toggle_panel(['Std_ReportView', ...])` | `Panels.py` | `'report'` |
| `StdPanelsTreeView` | `_toggle_panel(['Std_TreeView', ...])` | `Panels.py` | `'treeview'` |
| `StdViewStatusBar` | `_toggle_statusbar()` (Qt `statusBar`) | `Panels.py` | `'statusbar'` |
| `StdClearViews` | `Gui.runCommand('Std_FreezeViews', 4)` | `SavedViews.py` | `'clear'` |
| `StdFreezeView` | `Gui.runCommand('Std_FreezeViews', 3)` | `SavedViews.py` | `'freeze'` |
| `StdLoadViews` | `_restore_frozen_view()` (`Std_FreezeViews`, 6) | `SavedViews.py` | `'restore'` |
| `StdRecallWorkingView` | `Gui.runCommand('Std_RecallWorkingView', 0)` | `SavedViews.py` | `'recall'` |
| `StdRestoreView` | `Gui.runCommand('Std_FreezeViews', 1)` | `SavedViews.py` | `'load'` |
| `StdSaveViews` | `Gui.runCommand('Std_FreezeViews', 0)` | `SavedViews.py` | `'save'` |
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
| `StdToolbarClipboard` | `_toggle_toolbar(['Clipboard', ...])` | `Toolbars.py` | `'clipboard'` |
| `StdToolbarEdit` | `_toggle_toolbar(['Edit', ...])` | `Toolbars.py` | `'edit'` |
| `StdToolbarFile` | `_toggle_toolbar(['File', ...])` | `Toolbars.py` | `'file'` |
| `StdToolbarHelp` | `_toggle_toolbar(['Help', ...])` | `Toolbars.py` | `'toolbarshelp'` |
| `StdToolbarIndividualViews` | `_toggle_toolbar(['Individual Views', ...])` | `Toolbars.py` | `'views'` |
| `StdToolbarLockToolbars` | `_toggle_toolbar_lock()` (Qt `setMovable` / App param) | `Toolbars.py` | `'lock'` |
| `StdToolbarMacro` | `_toggle_toolbar(['Macro', ...])` | `Toolbars.py` | `'macro'` |
| `StdToolbarStructure` | `_toggle_toolbar(['Structure', ...])` | `Toolbars.py` | `'structure'` |
| `StdToolbarView` | `_toggle_toolbar(['View', ...])` | `Toolbars.py` | `'view'` |
| `StdToolbarWorkbench` | `_toggle_toolbar(['Workbench', ...])` | `Toolbars.py` | `'workbench'` |
| `StdTreeCollapseDocument` | `Gui.runCommand('Std_TreeCollapseDocument', 0)` | `Tree.py` | `'collapse'` |
| `StdTreePreSelection` | `Gui.runCommand('Std_TreePreSelection', 0)` | `Tree.py` | `'preselection'` |
| `StdTreeRecordSelection` | `Gui.runCommand('Std_TreeRecordSelection', 0)` | `Tree.py` | `'recordselection'` |
| `StdTreeSingleExpand` | `_single_expand()` (`Std_TreeSingleDocument` / `Std_TreeExpand`) | `Tree.py` | `'singleexpand'` |
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