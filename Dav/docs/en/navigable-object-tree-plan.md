# Plan: FreeCAD tree as navigable data (replace the PNG image)

> **Status: COMPLETED AND SUPERSEDED** (verified 2026-08-18).
>
> Phases 1-3 were fulfilled, but **not by the route this plan describes**.
> The plan proposed macro → `tree_data.json` → GUI with two timers; the final
> implementation reads FreeCAD **in-process** and refreshes on events, with no
> intermediate files or polling. The three files this document asked to modify
> (`MainWindow.py`, `capture_tree.FCMacro`, `trigger_capture.py`) **no longer
> exist**.
>
> What is current today:
> - `InterfazDAV/DavPanel.py` → `SetTree()` paints the `QTreeWidget`.
> - `integration/dav_dock_panel.py` → `PublishTree()` reads `doc.Objects`,
>   `_TreeDocumentObserver` refreshes on document changes.
> - The data contract (`name`/`label`/`type`/`visible`/`parent`) **was kept
>   as-is** from the design below.
>
> From the "Out of scope" section, **bidirectional highlighting is already
> done** (`_TreeSelectionObserver` + `DavPanel.HighlightSelection`, 2026-08-18):
> what is selected by voice is highlighted in the panel. Still pending are
> navigating the tree by voice ("select the third") and the panel → FreeCAD
> direction (a click in the panel that selects in FreeCAD).
>
> It is kept as a record of the design and of the data contract.

## Context

Today the **"FreeCAD Tree"** panel of the PySide6 GUI (`Dav/scr/ComponentesDAV/InterfazDAV/MainWindow.py`)
does not show the real tree: it shows a **PNG image** (`tree_capture.png`) that
a FreeCAD macro generates with `combo_view.grab()` and the GUI refreshes every
2s. That covers the visual side but is **not navigable** — there are no
objects, types, or hierarchy as data. The CLAUDE.md requirement ("navigate
created objects") asks for real data.

**Goal:** have the macro send the **object structure** of the active document
as **JSON** (name, type, label, visibility, parent/child hierarchy) and have the
GUI paint it in a **`QTreeWidget`**, completely replacing the image capture. No
voice commands yet and no bidirectional selection with FreeCAD (left as a future
phase).

The GUI↔FreeCAD communication flow already exists and is reused: JSON signal
file + `dav_paths.json` + macro with `QTimer`. Only **what** is transported
(data instead of an image) and **how it is painted** (widget instead of pixmap)
change.

## Files to modify

### 1. `Dav/scr/ComponentesDAV/InterfazDAV/capture_tree.FCMacro`
Replace `capture_tree()` (which does `pixmap.grab()` / `save PNG`) with a
function that serializes the active document's tree:
- Iterate over `App.ActiveDocument.Objects`.
- For each object: `Name`, `Label`, `TypeId`, visibility
  (`obj.ViewObject.Visibility` if there is a GUI), and the parent group
  (`obj.getParentGroup()` if it exists) to rebuild the hierarchy.
- Write the result to a new file `tree_data.json` (path taken from
  `dav_paths.json`, new key `tree_data_path`), and respond in the `signal_file`
  with `{"status":"done","result":{"success":true}}` just as today.
- Keep the listening `QTimer` and the signal pattern intact.

### 2. `Dav/scr/ComponentesDAV/InterfazDAV/trigger_capture.py`
- In `ensure_macro_installed()`: add `tree_data_path` to the `paths` dict
  written to `dav_paths.json`.
- Clean up the old `tree_data.json` at startup (just as `tree_capture.png` is
  cleaned today).
- `trigger_capture()` does not change (it still sends the
  `{"command":"capture"}` signal and waits for `status:done`).

### 3. `Dav/scr/ComponentesDAV/InterfazDAV/MainWindow.py`
Replace the image panel with a data tree:
- **UI** (`_SetupUi`, "FreeCAD Tree" panel): change
  `self._TreeImageLabel = QLabel()` to `self._TreeWidget = QTreeWidget()`
  (import `QTreeWidget`, `QTreeWidgetItem`). Style it with the `self._T`
  palette like the rest.
- **Delete** the image logic: `_ShowPlaceholderImage`, `_RefreshTreeImage`, the
  `_RefreshTimer` (2s), and the part of `resizeEvent` that rescales the pixmap.
- **New** `_RefreshTreeData()`: read `tree_data.json` (if it changed by mtime,
  same pattern as the old `_LastImageMtime`), clear the `QTreeWidget` and
  rebuild items from the JSON (label + type, and indentation by hierarchy).
  Connect it to a `QTimer` (it can reuse the 2s one).
- `_AutoCapture()` (5s) is kept: it triggers the signal to the macro; only now
  the macro produces data instead of a PNG.
- Adjust `SetColor` / `_UpdateStyles` to restyle the `QTreeWidget` instead of
  the image label.
- Remove dead references to `tree_capture.png` in `_CheckMacroStatus` (change
  it to check `tree_data.json`).

## `tree_data.json` format (GUI↔macro contract)
```json
{
  "document": "Unnamed",
  "objects": [
    {"name": "Box", "label": "Cubo", "type": "Part::Box", "visible": true, "parent": null},
    {"name": "Fusion", "label": "Fusión", "type": "Part::MultiFuse", "visible": true, "parent": null}
  ]
}
```
v1: flat list with `parent` (None or the group's Name). The `QTreeWidget` nests
by `parent`; objects without a parent go to the root.

## Reuse
- Existing signal/config mechanism (`signal_file`, `dav_paths.json`, `QTimer` in
  the macro) — not reinvented, only `tree_data_path` is added to it.
- The `mtime` change-detection pattern (like `_LastImageMtime`) is reapplied for
  `tree_data.json`.
- Palette and QSS (`self._T`, `_PanelQss`) to style the tree consistently with
  the GUI.

## Verification
1. **Without FreeCAD (quick):** manually create a sample `tree_data.json` in the
   InterfazDAV folder and launch the standalone GUI (`python main.py --gui` from
   PruebaIntegracion, or the InterfazDAV entrypoint) → the panel must show the
   JSON's objects in the tree, not the image.
2. **With FreeCAD (real):** open FreeCAD with `iniciar_dav.ps1`, run the
   `capture_tree` macro, create a couple of objects (Box, etc.). Within ≤5s the
   GUI's `QTreeWidget` must list those objects with their type. Create/delete
   objects in FreeCAD and verify that the GUI tree updates.
3. **Regression:** history, voice, themes and preferences keep working
   (`VoiceWorker` and `AddToHistory` were not touched).

## Out of scope (future phases)
- Navigate the tree by voice (next/previous/select N).
- Bidirectional selection (select by voice → highlight in FreeCAD's real tree).
- Delete the dead mock-up `Dav/scr/PruebaIntegracion/hilos/GestorDeHilos.py`
  (Tkinter, unused) — separate cleanup if desired.
