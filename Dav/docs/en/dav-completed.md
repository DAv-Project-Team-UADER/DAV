# Completed — DAV

What is **already
resolved**, what the problem was and how it was closed. It serves to avoid
re-diagnosing the same thing twice and to see real progress without reading the
git history.

Order: most recent first.

---

## "Move" the view to a point (2026-09-20)

`Dav/dic/moveview.py`: asks for a point and centers the camera on it without
changing where it looks or the zoom (the camera position is shifted along its
viewing axis, at the focus distance; uses pivy). Like the dimension, it asks for
**X, Y** (flat drawing, or sketch being edited, with its `Placement`) or
**X, Y, Z** (3D model) depending on `measure.dimensionMode()`. It is in the 384
`TraduceTo*` files of all contexts, in es/en/pt (`MOVE_VIEW_PHRASES`), added with
`setdefault`: where "mover" already had another meaning (Explorer/Edit,
Draft/modify, Sketcher) the local one wins and the variants "mover vista",
"mover cámara", "centrar en"... apply.

---

## "Measure" / "dimension": 2D or 3D depending on the document (2026-09-20)

`CreateDimension` (`Dav/dic/measure.py`, imported by 36 `TraduceTo*`) always
asked for six values. Now it decides on each execution and asks for **four**
(X, Y of each point) or **six** (X, Y, Z):

1. sketch being edited → 2D, in the sketch's plane (uses its `Placement`);
2. the document has any solid → 3D;
3. no solids and Draft/Sketcher/TechDraw workbench active → 2D;
4. any other case → 3D.

It is still the same name, so the dictionaries do not change. It works because
the collector and the validator read `inspect.signature(function)` on each
execution: `CreateDimension` is a callable object with a `__signature__`
computed on the fly. In addition, all the `TraduceTo*` files under `Workbench`
(es/en/pt) receive the phrases from `MEASURE_PHRASES` (in `measure.py`) with
`setdefault`: they do not overwrite the context's own phrases (e.g. "cota"
inside `constraints` is still the Sketcher one). The Vosk grammar only includes
the current context and the root, not the ancestors, which is why it has to be
in every dictionary and the upward lookup is not enough.

---

## Ask what to work on, modify by voice and correct (2026-09-20)

Follow-up to an at-a-glance audit. Everything in `Dav/dic/` except two new
prompts.

### 1. Commands that depended on "selection or active object"

`pad_by_length`, `revolve_by_angle`, `pocket_by_length` and `groove_by_angle`
took `_SelectedOrActive`: after creating a shape, the "active" one is the shape,
not a profile (same origin as the "through hole" failure). Now they ask for the
sketch with `askSketch`. A loose sketch (without a body) in a cut no longer
creates a new empty body: it asks which body to work on (`_OwningBody`).

### 2. Modify in Draft without a mouse (`DraftWork/_modify.py`)

`modify`, `modification`, `array` and `facebinder` launched the native command,
which waits for clicks. Now each one asks for the object with the voice menu and
for the data with numeric windows, and uses the Draft API: clone, downgrade/upgrade,
to sketch, move, rotate, scale, mirror, offset, fillet, join, edit/stretch a point,
slope, split, extend/trim, polyline to curve, 2D view, all arrays (circular,
orthogonal, polar, by path, by points, with and without links) and face union.
The native ones remain as `interactive_*`.

### 3. New or existing body

Additive shapes ask "new body?" (`YesNoInputPrompt`: "no" is an answer, not a
cancel). With "no" the menu of valid bodies opens and the shape is added to an
existing one; if it does not touch the solid, FreeCAD rejects it and it is
discarded with a notice. Subtractive shapes and holes always open the menu of
valid bodies (`chooseBody`; `isBody` discards those with a broken operation).

### 4. Coverage

- **Shapes without parameters**: ellipsoid, wedge, helix, loft and pipe, additive
  and subtractive. The wedge is stood upright (its height is born along Y) and
  centered in x, y, z; helix, loft and pipe choose their sketches from a list.
- **Sketcher by voice** (`Sketcher/_edit.py`, `_elements.py`, `constraints/_voice.py`):
  trim, split, extend, fillet, chamfer, symmetry, move and construction, and the
  **geometric** constraints. The sketch is chosen from a list and the element **by
  number** (drawing order, from 1; the request message lists it with its type).
  **Dimensions and "measure" are not touched**: `constraints.py`, Draft's linear
  dimension and the MEASURE blocks (`measure.py`) were left as they were.
- **Correct by voice** (`Correction/`, hooked into `dic/TraduceTo*.py`, can be said
  from any context): "deshacer" (undo), "rehacer" (redo), "borrar último" (delete
  last), "borrar objeto" (delete object) and "borrar rotos" (delete broken ones).
  Deleting asks for confirmation and does not delete what other objects use.
- **Languages**: TechDraw was already loaded; the
  real failures were typos and capitalization in imports.

Pending: rotating, scaling and offsetting sketch elements, and the `lock`,
`horver` and `coincidentunified` constraints, still use the native command.

---

## PartDesign: holes and shapes with position (2026-09-20)

"agujero pasante" (through hole) failed with `No base set, no sketch support
either` and "agujero ciego" (blind hole) with `draw the hole centres in a sketch
first`. In addition, no shape asked where it went.

### The real cause

- `hole_by_size` created the `Hole` with `doc.addObject` (outside the Body) and
  assigned the profile to it **before** putting it into the Body: FreeCAD
  rejects that.
- It took "the active object" as the profile, which after "cubo" was the cube
  itself: it converted the 12 edges of the box into a sketch.
- It used `DepthType = 1` believing it was "explicit depth". In FreeCAD 1.x
  `0 = Dimension` and `1 = ThroughAll`: the dictated value was ignored. The same
  happened in `hole_choose_sketch` ("agujero" with a chosen sketch).

### What changed (`Dav/dic/Workbench/PartDesign/`)

- **Holes without a previous sketch**: `hole_by_size(diametro, x, y, z)` and
  `blind_hole_by_size(diametro, profundidad, x, y, z)` draw the sketch themselves
  (circle at x, y on the z plane) inside the last solid's Body. `z` is the height
  of the face from which it drills; it cuts toward -Z and, if that removes no
  material, it is reversed. If it removes no material either, it is discarded and
  a notice is given.
- **Shapes centered at (x, y, z)**: box, cylinder, sphere, cone, torus and prism,
  additive and subtractive (subtractive cone, torus and prism were native commands
  without parameters). `_placement.py` attaches the shape to the Body's XY plane
  with `AttachmentOffset`, shifted half a dimension where the primitive is born
  with a corner or its base at the origin.
- **Which body to work with**: holes and cuts use `chooseBody`: only bodies with a
  valid solid are offered (`isBody` in `_prompts.py` discards those whose last
  operation is broken). With only one it is used directly; with several it asks
  by voice ("avanzar" / "okey"). Before, it always cut on the last Body: if its
  tip was a broken `Hole`, the cut failed with
  `Cannot subtract primitive feature without base feature`.
- A cut that does not touch the solid (or removes no material) no longer leaves a
  useless feature in the model: it is removed and a notice is given.

Pending: ellipsoid, wedge, helix, loft and pipe still use the native command.

---

## Vosk grammar narrowed to the context (2026-08-10)

It was **§1** of the pending list: the `KaldiRecognizer` was created without
`SetGrammar`, so Vosk competed against the model's **100,001 words** on every
phrase instead of the ~12 of the active context. Hence "croquis" → "crockett"
and the "traffic" that nobody said.

Integrated from PR #176 by SoPerez1, plus the fixes from #178.
Full operation in
[`vosk-grammar-shortener.md`](vosk-grammar-shortener.md).

### The cause that was not in plain sight

The grammar by itself was not enough: it **brought down FreeCAD**. Vosk does not
accept having its grammar changed on a recognizer that has already processed
audio, and it fails with a C++ exception that no Python `except` catches.

```
SetGrm():recognizer.cc:235
"Can't add speaker model to already running recognizer"
```

Since the loop calls `SetGrammar` after processing audio, **every level change
was a crash attempt**. Verified against the `pt` model in separate processes:

| scenario | result |
| --- | --- |
| `SetGrammar` before audio | ok |
| `SetGrammar` after audio | ERROR → crash |
| `Reset()` + `SetGrammar` | ok |

`speech/voice_commands.py` already had `USE_GRAMMAR = False` with the note *"can
block all recognition on some models"*: someone had run into this before. That
variable **was read by nobody**, so it turned nothing off, and its diagnosis was
incorrect — it does not depend on the model, it always happens. It was removed.

### The microphone that "did not pick up"

Second symptom, same root. The log showed the two modes fighting over the
recognizer:

```
14:28:27  aplicando gramatica: 82 frases    ← preferences
14:28:27  aplicando gramatica: 54 frases    ← CAD
14:28:27  aplicando gramatica: 82 frases
```

Each application does a `Reset()`, which discards half-recognized audio, so no
phrase ever got to complete. The loop now drains the queue and keeps only the
last grammar.

### What was done

| Change | Effect |
| --- | --- |
| `Browser.GetSpokenPhrases()` | Grammar of the active level, derived from the dictionary |
| `Reset()` before `SetGrammar` | Closes the crash |
| Only the last grammar in the queue | Closes the dead microphone |
| `core/dav_log.py` | Log to file: without this none of the above was diagnosable |
| `enviar`/`cancelar` to `NavCommands/` | They were in three places in the code, already out of sync |

### Verification

Real voice session inside FreeCAD: the grammar follows navigation (54 at the
root → 93 in File → 199 in Sketcher), with no crashes or grammars overwriting
each other.

### What remains open

- **The grammar restricts the vocabulary, not the syntax.** Vosk can combine
  valid words into meaningless phrases ("extender oblongo"). They execute nothing,
  but with 199 active phrases there is more surface for noise.
- `settings.json` sometimes ends up in `pt` between sessions and it is not yet
  known what writes it. The log already records which phrase triggers each
  language change.

---

## DAV panel docked to FreeCAD (2026-08-09)

Complete GUI migration: from an external process to a `QDockWidget` inside
FreeCAD. Plan and stages in [`gui-unification-plan.md`](gui-unification-plan.md).

### The underlying problem

`InterfazDAV` **would not open**. It ran as a separate process with its own
PySide6 6.11.1 and inherited from FreeCAD the variables that point to its Qt 6.8.3:

```
ImportError: DLL load failed while importing QtWidgets
```

Patching was attempted three times (cleaning `PYTHONHOME`/`PYTHONPATH`/`QT_PLUGIN_PATH`,
filtering the `PATH`, changing the `cwd`) and none was enough: each patch covered
one known contamination route and the ones that depend on the parent process's
in-memory state remained.

**It was solved by construction, not by patch:** a widget inside FreeCAD uses
FreeCAD's Qt, so there are no two Qts to collide.

### What was done

| Stage | Result |
| --- | --- |
| 1 | `MainWindow.py` (1011 lines) split into `DavPanel` + `ContextView` + `IconLocator`, with no dependencies on FreeCAD or on files |
| 2 | Panel mounted as a dock, fed by the in-process `Browser`; file bridge eliminated in both directions |
| 3 | Object tree from `App.ActiveDocument` + `DocumentObserver`, no macro or polling |
| 4 | External window retired entirely, including `DiccionarioPrueba/` |
| 5 | Desktop launcher deleted: **a single GUI** remains, closes §2.b |

### Why there were "two GUIs" and why there is now one

They were not equivalent: `InterfazDAV/MainWindow.py` (1011 lines) was the
working one, and `IntegracionGUI/ui/main_window.py` (138) a *launcher* whose
voice button did a `Popen` of the other. They diverged through parallel
development, not by design.

Stage 5 was resolved the opposite way from what was planned: it was recommended
to keep the launcher as a desktop configurator, but its main button was already
broken (it launched the window deleted in stage 4) and it **did not provide the
model download** — that flow lives in `preferences_dialog.py`, accessible from the
DAV bar and the panel's ⚙ button. It only *warned* if a model was missing, a
warning that `voice_bootstrap` already gives.

### The file bridge, eliminated

| Before | Now |
| --- | --- |
| `export_context_state()` → JSON, read every 500 ms | `PublishContext()` directly |
| `command_queue.txt` + `QTimer` | `SendCommand()` → `procesar_frase_final` |
| `voice_history.log` by polling | `_publish_line()` at the moment |
| `tree_data.json` + macro + 2 timers | `App.ActiveDocument` + observer |

`voice_history.log` (persistent record) and `voice_status.json`
(`export_voice_status` is the single point of the engine's state, and from there
it is published to the panel) survive.

### Deleted, ~4900 lines

`main.py` · `run_interfaz.bat` · `VoiceWorker.py` · `MainWindow.py` ·
`trigger_capture.py` · `capture_tree.FCMacro` · `HelpWindow.py` ·
`DiccionarioPrueba/` · `DavPanelController` + `FileBridgeSource` · the 7 methods
of the external launcher in `dav_commands.py` · `_schedule_interfaz_dav_launch`

### A hard crash that appeared and was closed

Mounting the panel brought down all of FreeCAD (`0xC0000005`), with no trace in
the Python console. FreeCAD's log showed it: a Qt widget was being touched **from
the microphone thread**, which is an access violation, not an exception that an
`except` can catch.

Fixed by moving the publications inside `run_on_main_thread`, and with
`_on_gui_thread()` that blocks them if they were to arrive from another thread
anyway.

---

## GUI defects fixed (2026-08-09)

| Symptom | Real cause |
| --- | --- |
| Buttons with two letters instead of an icon | The key and the file differed in case/separators (`lineattributes` vs `LineAttributes.svg`); and `pieza`/`circulo`/`stdview` have an icon with a different name → normalization + alias table |
| Icons of uneven sizes | The embedded `QSvgWidget` drew according to each SVG's `viewBox` → `setIcon`/`setIconSize` |
| "Microphone inactive" with voice active | `PublishStatus` existed but nobody called it |
| The window stayed always on top, without minimizing | A floating `QDockWidget` is `Qt.Tool` by default → real window flags, reapplied in `topLevelChanged` |
| The panel stretched when entering large contexts | The buttons went in a single row; `Part` has 47 entries (~3000 px) → grid with horizontal scroll and fixed height |
| The "volver" (back) button did nothing | `NavCommands/` only had `TraduceToEs.py`; in other languages **zero** navigation commands were loaded |
| Help came out in the Report View, not in the panel | Commands write with `print()` (988 calls in 123 files) → stdout is captured during execution |
| `Cannot find icon` in the bar | `Std_DlgCustomize` is a command identifier, not an icon name |
| `part` and `circle` appeared at the root | The `TraduceTo*` files added two destinations that `base.py` does not define; `circulo` is also a leaf that draws, not a category |

---

## Voice model analysis (2026-08-09)

**Counterfactual finding:** a larger Vosk model does **not** improve command
recognition.

- The small model already loads 100,001 words and DAV uses 745 (0.75%). The
  median per context is 12 phrases: a factor of ~8,000×.
- 66 of those 745 (8.9%) are **out of vocabulary** and impossible to emit:
  `chaflán`, `extruir`, `biselar`, `isométrica`, `polilínea`. This is the core of
  the CAD vocabulary, and enlarging the model does not add them.
- The overkill is in the language model (`Gr.fst`), not in the acoustic one. A
  restricted grammar replaces the former and keeps the latter.

> **The benchmark is missing** for the hit rate before presenting it as an
> experimental result. The experiment design is in §10.f.

---

## Vocabulary cleanup (2026-08-08)

**89 → 66 out-of-vocabulary words (11.5% → 8.9%).** When cross-checking the tree
against the model, 89 words appeared that the recognizer cannot emit, but they
were not all the same problem: only one category was a model limitation, the rest
was dictionary debt (internal keys that remained as spoken phrases, anglicisms
without a synonym, typos).

---

## Dictionary and navigation fixes (2026-06 / 2026-08)

- **Nested subcontexts, never flattened** — `explorer.update({'file': file})`
  and not `explorer.update(file)`. Flattening collided repeated keys between
  leaves and left the folder out of the navigable tree.
- **`NavCommands/`** — the navigation words (subir, contexto) live in the
  dictionary like any other command, not hardcoded in `browser.py`.
- **Broken imports** that brought down the loading of Base and Sketcher.
- **Accent normalization** unified into a single function.
- **`IsSameTarget`** as a public alias of `_SameTarget`: whoever walks `Context`
  from outside needs to deduplicate just like the `Browser`.

## Selection highlighting in the panel tree (2026-08-18)

**Problem.** When saying `"seleccion"` → `"siguiente"`, the object was selected
in FreeCAD but the DAV panel tree did not highlight it. The same with the objects
created by `CreateObjects`: they appeared in the tree, but you could not see which
one was active. You had to look at FreeCAD's native tree to know.

**Real cause.** Nothing was missing in the tree or in `ObjectSelection`: both
worked fine separately. `ObjectSelection.MonoSelection()` calls
`Gui.Selection.addSelection(Obj)` and its work ends there — **nobody told the
panel**. The `_TreeDocumentObserver` that already existed listens to changes in
the *document* (create/delete/recompute), and selecting does not change the
document, so it never fired. The observer for the other channel was missing.

**Solution.**

- `DavPanel.HighlightSelection(Names)` — walks the `_treeItems` map (which
  `SetTree` now stores) and marks the selected ones, with `scrollToItem` to the
  first. The widget still does not import FreeCAD: it receives a list of names.
- `BrowserPanelSource.PublishSelection()` — reads `Gui.Selection.getSelection()`
  and hands it to the panel.
- `_TreeSelectionObserver` — registered with `Gui.Selection.addObserver()`,
  same pattern as `_TreeDocumentObserver`: all the slots land in a
  `_Refresh` with `try/except`, because an exception here would propagate into
  FreeCAD's selection handling.

**Non-obvious detail.** `HighlightSelection` wraps the loop in
`blockSignals(True/False)`: `setSelected()` emits `itemSelectionChanged`, and
when the reverse direction is implemented (click in the panel → select in
FreeCAD) that would feed back in an infinite loop. Blocking now avoids the bug
before it exists.

The panel → FreeCAD direction and navigating the tree by voice
("seleccionar el tercero", i.e. "select the third") remain pending. See
`navigable-object-tree-plan.md`.

---

## How to add to this document

When closing a pending item: move it here with **what the problem was** and
**what turned out to be the real cause**, not only what was changed. Several
times the apparent cause and the real one were different (the icons were not
missing, the name did not match; the help button did work, its output went
elsewhere), and that is precisely the information that avoids repeating the
diagnosis.
