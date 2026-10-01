# Getting started (setup)

Guide to bring up DAV and test the voice engine on a local machine.

> ⚠️ **The two interpreters.** The development venv
> (`IntegracionGUI/GUIFreeCad/.venv`) uses a newer Python than the Python
> embedded in FreeCAD. The code has to run on both: **scripts loaded inside
> FreeCAD use FreeCAD's interpreter, not the venv.**
> FreeCAD extensions must use **PySide6**, not PyQt, for build compatibility
> with the native framework.

## 1. Clone the repository

The contribution flow uses a **personal fork** + **Pull Request** (see
the full flow in `CLAUDE.md` and in `dav-development-guide.md` → GitFlow).

```bash
git clone https://github.com/<your-user>/DAV.git
cd DAV
```

If you want the central repository directly:

```bash
git clone https://github.com/DAv-Project-Team-UADER/DAV.git
```

## 2. Python dependencies (development venv)

The development environment lives in
`Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/.venv` with the dependencies
declared in `requirements.txt`:

```
PySide6>=6.6.0
vosk>=0.3.45
sounddevice>=0.4.6
numpy>=1.24.0
requests>=2.31.0
tqdm>=4.66.0
```

To recreate/install it:

```bash
cd Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad
python -m venv .venv
.venv\Scripts\activate          # Windows
# or: source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

> This venv is for **developing/testing the GUI widget and prompts** in
> isolation. To test voice **inside FreeCAD** the dependencies must be
> available to FreeCAD's interpreter (modules installed in the
> environment that runs FreeCAD).

## 3. Vosk voice models

The models live in `Dav/models/` (excluded from git — see
`Dav/models/README.md`):

| Model | Language |
|---|---|
| `vosk-model-small-es-0.42` | Spanish |
| `vosk-model-small-en-us-0.15` | English |
| `vosk-model-small-pt-0.3` | Portuguese |

There is no need to download them by hand: `core/model_manager.py` and
`ui/download_dialog.py` (in `IntegracionGUI/GUIFreeCad/`) download them if
they are missing. The script `scripts/setup_models.py` also exists.

> For higher accuracy in Spanish there is `vosk-model-es-0.42` (heavier), not
> included by default.

## 4. Run DAV inside FreeCAD

DAV starts inside FreeCAD's **Python console** (View → Panels →
Python console) or as a **macro**. `DAVCore` must be started the same way as
`FreeCADGuiInit.py`, that is, when the application starts.

General steps:

1. Open FreeCAD with a new document.
2. Open the **Python console**.
3. Load and run the voice engine startup (the bootstrap that mounts the
   `Browser` + microphone). See `integration/voice_bootstrap.py` and
   `InitGui.py` in `scr/.../Dav/` for the automatic startup with FreeCAD.
4. Set the language in **DAV Preferences** if it is not Spanish.

> The DAV panel is mounted as a `QDockWidget` inside FreeCAD via
> `integration/dav_dock_panel.py`. If it starts as a floating window, it can be
> docked to any edge.

## 5. Basic commands to verify the setup

With the engine active, try the Browser's own navigation phrases (they do not touch
anything in the document):

- **`donde estoy`** (where am I) — shows the current context.
- **`subir`** (go up) — goes up one level in the navigation tree.

And a real command, for example:

```
banco de trabajo → diseñador de piezas    (go to the PartDesign workbench)
```

The pop-up confirm/abort commands (shared by the prompts):

- **Confirm a value**: `enter` · `enviar` · `aceptar` · `confirmar` · `ok`
- **Abort a pop-up**: `cancelar`

## Ports / common problems

- **The microphone uses PyAudio/SoundDevice** — if the stream does not open, check
  that the device is available and not in use.
- **The model did not load** → confirm it exists in `Dav/models/<language>` or
  that `setup_models.py` downloaded it.
- **The grammar is restricted by context** — certain prompts (numeric, plane
  selection) deliberately limit which words Vosk listens for. If a
  command "is not understood", check whether an active prompt is restricting the
  grammar (see `vosk-grammar-shortener.md`).

---

Next: [Code conventions](conventions.md)
