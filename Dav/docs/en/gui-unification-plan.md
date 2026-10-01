# Plan: unify the two GUIs (resolve §2 of pendientes-dav.md)

**Status:** stages 1 to 4 implemented; stage 5 remains.
**Date:** 2026-08-09
**Result:** summarized in [`dav-completed.md`](dav-completed.md).
**Immediate reason:** InterfazDAV does not open from FreeCAD because of a Qt
DLL conflict that **only exists because it runs as an external process**.
Patching it is possible; eliminating it by construction is better.

---

## 1. The real map (verified, not assumed)

The assumption that "there are two complete GUIs and one has to be chosen" **is
incorrect**. What there is:

| | `InterfazDAV/` | `IntegracionGUI/GUIFreeCad/` |
| --- | --- | --- |
| Window | `MainWindow.py` — **1011 lines** | `ui/main_window.py` — **138 lines** |
| What it is | the real working GUI | a **desktop launcher** |
| Where it runs | external process (Python 3.14 venv) | external process (venv) |
| Qt | its own PySide6 → **clashes with FreeCAD's** | its own PySide6 |
| Has | history, minimize, tree, context buttons | preferences, model downloads |

The fact that changes everything: **`ui/main_window.py` does not use the
`Browser`**. Its "Start Voice" button does a `subprocess.Popen` of…
`InterfazDAV/main.py` (`ui/main_window.py:121-138`). It is a launcher, not an
alternative.

### Where the Browser really lives

```
FreeCAD (process)
└── dav_commands.py / freecad_wb.py
    └── integration/voice_bootstrap.py  ← start_voice_engine()
        └── Browser(...)                ← the real engine, INSIDE FreeCAD
            └── BrowserVoiceAdapter
                └── writes context_state.json ─┐
                                                │  file bridge
InterfazDAV (external process)                  │
└── MainWindow._PollFreeCADState() ←────────────┘  polling 500 ms
```

The `Browser` **already runs inside FreeCAD**. Neither window has it: one
consumes it through files, the other does not even touch it.

> **Correction to the previous recommendation:** saying "migrate history and
> minimize to IntegracionGUI" was wrongly framed — `IntegracionGUI` is not the
> good GUI to move to, it is a 138-line launcher. The real migration is of
> `InterfazDAV` **into FreeCAD**, not to the other folder.

---

## 2. Why the Qt bug is structural

`InterfazDAV` runs in a venv with **PySide6 6.11.1**. FreeCAD 1.1 ships its own
Qt6 in `bin/` (`Qt6Core.dll`, `Qt6Widgets.dll`, …). When launched as a
subprocess it inherits from the parent:

- `PYTHONHOME` / `PYTHONPATH` → the venv loads FreeCAD's stdlib
  (`SRE module mismatch`)
- `QT_PLUGIN_PATH` and FreeCAD's `bin` in the `PATH` → PySide6 resolves
  FreeCAD's Qt6 instead of its own (`DLL load failed while importing QtWidgets`)

The environment can be sanitized (it was attempted: removing variables,
filtering the `PATH`, prepending the PySide6 folder, changing the `cwd`). But
each patch covers one known contamination route, and the ones that depend on
the parent process's in-memory state remain. **As long as there are two
different Qts in play, the problem can come back** with another version of
FreeCAD, of PySide6, or on another machine.

A widget inside FreeCAD uses **FreeCAD's Qt**. The conflict is not patched: it
ceases to exist.

---

## 3. Goal

Turn `InterfazDAV` into a **docked panel inside FreeCAD** (`QDockWidget`),
eliminating the external process and the file bridge.

```
BEFORE                               AFTER

FreeCAD ──► Browser                  FreeCAD ──► Browser
   │           │                        │           │
   │      context_state.json            │      direct Qt signal
   │      command_queue.txt             │           │
   │      voice_history.log             │           ▼
   ▼           │                        └──► DavPanel (QDockWidget)
InterfazDAV ◄──┘                                 history, tree,
(external process, own Qt)                       buttons, minimize
```

### What is eliminated

- The Qt conflict (by construction)
- `command_queue.txt`, `context_state.json`, `voice_status.json`,
  `voice_history.log` as a channel — and with them the pending items §2.d:
  `pop_command_queue()` losing commands, the 500 ms latency, state
  versioned by mistake
- The two polling `QTimer`s
- `_launch_interfaz_dav()`, `_clean_child_env()`, `_probe_pyside6()`,
  `_check_interfaz_started()` in `dav_commands.py`
- `run_interfaz.bat`, `trigger_capture.py`, `capture_tree.FCMacro`

### What is gained

- The GUI accesses the `Browser`, the document and the selection **in the same
  process**: no serialization, no latency, no lost commands
- The object tree comes straight from `App.ActiveDocument`, with no macro or
  `tree_data.json`
- Theme and language inherited from FreeCAD

---

## 4. Staged migration

Each stage leaves the repo working. There is no "big bang".

### Stage 0 — Provisional patch (optional)

Leave the `dav_commands.py` fixes (venv by path, environment sanitizing, startup
diagnostics) so that the GUI opens **while** the migration lasts. They are
deleted in stage 4.

> Pending decision: if stage 1 is done soon, this patch can be skipped.

### Stage 1 — Extract the panel

Split `MainWindow.py` (1011 lines) into:

- **`DavPanel.py`** — `QDockWidget` with all the widgets: history, tree,
  context buttons, overlay. **No** polling `QTimer`, no file reading, no
  `subprocess`.
- **`DavPanelController.py`** — the glue: receives the context from the
  `Browser` and updates the panel.

`MainWindow.py` remains as a thin wrapper so the standalone GUI can keep
running during the transition.

Rule: `DavPanel` **does not import FreeCAD**. It receives data, emits signals.
That way it can be tested without FreeCAD, just like `Browser`.

### Stage 2 — Mount the panel in FreeCAD

In `freecad_ui_setup.py` (which already knows how to do `Gui.getMainWindow()`):

```python
panel = DavPanel()
Gui.getMainWindow().addDockWidget(Qt.RightDockWidgetArea, panel)
```

Connect to the `Browser` through signals, replacing the bridge:

| Today (files, 500 ms) | After (signals, immediate) |
| --- | --- |
| `export_context_state()` → JSON | `browser.ContextChanged` → `panel.RenderContext()` |
| `command_queue.txt` → `pop_command_queue()` | `panel.CommandRequested` → `browser.ProcessPhrase()` |
| `append_voice_history()` → `.log` | `adapter.PhraseRecognized` → `panel.AddToHistory()` |

The `on_descend` callback that already exists in `Browser` (unused today) is the
natural hook for `ContextChanged`.

In this stage both routes coexist: the docked panel and the external window.
Behavior is compared.

> **Closed (2026-08-09).** The file bridge no longer exists in either
> direction:
>
> | Before | Now |
> | --- | --- |
> | `export_context_state()` → JSON | `PublishContext()` directly to the panel |
> | `command_queue.txt` + 500 ms `QTimer` | `SendCommand()` → `procesar_frase_final` |
> | `voice_history.log` read by polling | `_publish_line()` at the moment |
> | `tree_data.json` + macro | `App.ActiveDocument` + observer (stage 3) |
>
> Deleted, now without a consumer: `export_context_state`, `read_context_state`,
> `write_command_queue`, `pop_command_queue`, `read_voice_history_from`, the
> `QTimer` that polled the queue and the body of `_export_state`.
>
> `voice_history.log` and `voice_status.json` **are still written**: the first
> as a persistent record, the second because `export_voice_status` is the single
> point through which the engine's state passes and from there it is published
> to the panel.
>
> `on_descend` is still unused: the refresh goes through `PublishContext()` at
> the end of each phrase, which also covers commands that do not change level.

### Stage 3 — Native object tree

**Why it is separate from stage 2:** they are *two different bridges*, with
different files and different code. Stage 2 replaces the voice channel
(`context_state.json`, `command_queue.txt`, `voice_history.log`); the tree
travels by its own path:

```
InterfazDAV._AutoCapture()  ──► trigger_capture.py
                                    │
                                    ▼
                            capture_tree.FCMacro  (inside FreeCAD)
                                    │
                                    ▼
                            tree_data.json  ──► _RefreshTreeData() (QTimer)
```

Once stage 2 is finished, the tree **would still** read `tree_data.json` through
a macro: it does not fix itself. And conversely, if everything is bundled into
one stage and the tree gets complicated, it blocks a voice fix that was already
working.

Work: `_PopulateTree()` switches to reading `App.ActiveDocument.Objects`
directly (same contract: `name`, `label`, `type`, `visible`, `parent`).
`trigger_capture.py`, `capture_tree.FCMacro`, `_AutoCapture()`,
`_RefreshTreeData()`, `_LastTreeMtime` and the refresh `QTimer` are deleted —
the document notifies through its own signals instead of being polled every 5 s.

> **Done (2026-08-09) for the docked panel.** `BrowserPanelSource.PublishTree()`
> reads `App.ActiveDocument` in-process, and `_TreeDocumentObserver` (registered
> with `App.addDocumentObserver`) triggers it on creation, deletion, change,
> recompute, and active document change. The tree now also follows what is drawn
> with the mouse, not only what comes in by voice.
>
> **Still missing** is deleting the old path: `trigger_capture.py` and
> `capture_tree.FCMacro` remain in the repo because their only consumer is
> `MainWindow.py`, which is retired in stage 4. Deleting them now would break
> the external window while it is still the one in use.

### Stage 4 — Delete the scaffolding — DONE (2026-08-09)

Before deleting, the entry condition was closed: the panel's **help** and
**preferences** buttons emitted signals that nobody connected. Now
`BrowserPanelSource` handles them — preferences opens the GUIFreeCad dialog, and
help dumps `Browser.DescribeContext()` into the history (the valid commands
*here and now*, more useful than the external window's fixed text).

Deleted:

- `InterfazDAV/`: `main.py`, `run_interfaz.bat`, `VoiceWorker.py`,
  `MainWindow.py` (1011 lines), `trigger_capture.py`, `capture_tree.FCMacro`,
  `HelpWindow.py` and **`DiccionarioPrueba/`** — closes §2 entirely
- `DavPanelController.py` + `FileBridgeSource`: they were the file bridge that
  this stage retires; without the external window they were left without a
  consumer
- `dav_commands.py`: `_launch_interfaz_dav`, `_check_interfaz_started`,
  `_clean_child_env`, `_probe_pyside6`, `_venv_python`, `_bring_interfaz_to_front`,
  `close_interfaz_dav` (~180 lines). With them goes the Qt conflict: no external
  process is launched anymore, so there are no two Qts to collide.
- `freecad_wb.py`: `_schedule_interfaz_dav_launch()` and its call at startup
- `IconLocator`: the `DiccionarioPrueba` root (467 icons remain indexed)

`Iniciar voz DAV` now opens the docked panel instead of launching the external
process. `iniciar_dav.bat` does not change: it never went through
`run_interfaz.bat`.

The `.gitignore` entries for the capture circuit are kept on purpose, so as not
to version the files that were left in old working copies.

### Stage 5 — What to do with `ui/main_window.py` — DONE (2026-08-09): (b)

**(a)** was recommended: keep it as a desktop configurator. On reviewing the
real state the recommendation did not hold up and **(b)** was chosen: delete it:

- **Its main function was broken.** The "Start Voice" button — the central
  element, 150×150 px — did a `Popen` of `InterfazDAV/main.py`, retired in
  stage 4.
- **It did not provide the model download.** That flow lives entirely in
  `ui/preferences_dialog.py` (`_download_large` + `DownloadDialog` +
  `download_large_model`), which is opened from the DAV bar and from the ⚙
  button of the panel. `main_window` only *warned* if a model was missing, a
  warning that `voice_bootstrap` already gives with the `setup_models.py` line.
- **It was the last remnant of the two-process model**, which kept the question
  of §2.b alive.

Deleted: `ui/main_window.py` and `GUIFreeCad/main.py` (~180 lines of wrapper).
Kept: `ui/preferences_dialog.py`, `ui/download_dialog.py`,
`core/model_manager.py`, `scripts/setup_models.py`.

> **What is lost:** downloading models with a graphical interface without
> opening FreeCAD. It remains available via the command line
> (`python scripts/setup_models.py`). If the graphical route were needed, a
> command in the DAV bar that opens `DownloadDialog` is cheaper than maintaining
> an entire desktop app.

---

## 5. Risks

| Risk | Mitigation |
| --- | --- |
| A `QDockWidget` that crashes takes down all of FreeCAD | The panel does no I/O or heavy work on the UI thread; the microphone already runs in its own thread |
| It touches code from several people (Tadeo, mica, Camila) | Small stages, separate PRs, `MainWindow.py` stays alive until stage 4 |
| The "standalone window" mode is lost | The panel can be undocked (`setFloating(True)`): the behavior is kept without a separate process |
| 1011 lines is a lot to split | Stage 1 is just moving code, without changing behavior; it is done and tested before touching FreeCAD |

---

## 6. Work order

The stages are sequential and done back to back; there is no need to wait for
anyone between one and the next. Each one closes in its own PR so that it is
reviewable.

| Stage | Scope | Touches FreeCAD | Touches others' code |
| --- | --- | --- | --- |
| 1 | split `MainWindow.py` into `DavPanel` + controller | no | yes (`MainWindow.py`) |
| 2 | mount the panel, signals instead of files | yes | yes (mica's bridge) |
| 3 | native tree | yes | yes (`capture_tree`) |
| 4 | delete scaffolding | yes | yes |
| 5 | fate of the launcher | no | no |

Stage 1 is the biggest but the safest: it is moving code, without changing
behavior, and it is tested by running the standalone window as until now.

**Notify the team** before stage 4: that is where files by Tadeo, mica and
Camila are deleted (`main.py`, `run_interfaz.bat`, `VoiceWorker.py`,
`DiccionarioPrueba/`). Up to stage 3 everything is additive or internal, and
`MainWindow.py` keeps working.

### Open decisions

- **Stage 0:** is the `dav_commands.py` patch left in so the GUI opens while the
  migration lasts, or do we jump straight to 1? If 1 and 2 come out quickly, the
  patch is wasted work.
- **Stage 5:** does `ui/main_window.py` stay as a desktop configurator
  (recommended) or is it absorbed into the panel?

> Related: §2, §2.b and §2.e of `pendientes-dav.md` (the pending items this plan
> closes) and §9 (the map of the three voice engines).
