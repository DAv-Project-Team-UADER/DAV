# Repository structure

The repository mixes two things: the **FreeCAD source code** (the base fork,
brought in whole) and the **DAV code of our own** (the voice layer). It is
important to know which half you are working in, because the license headers
and the rules are different.

```
DAV/
├── FREECAD/          # FreeCAD source code (base fork, do NOT touch this unless necessary)
│   ├── src/          #   FreeCAD Python and C++ modules
│   │   ├── App/      #   Application core (FreeCADInit.py)
│   │   ├── Gui/      #   Graphical interface (FreeCADGuiInit.py)
│   │   ├── Ext/freecad/  #   FreeCAD's own Python extensions
│   │   └── Mod/      #   Workbenches: Draft, Sketcher, Part, PartDesign,
│   │                 #     Assembly, TechDraw, etc.
│   └── CMakeLists.txt
├── Dav/              # ⭐ ALL of the DAV project's own code
│   ├── dic/          #   Voice command tree (see below)
│   ├── docs/         #   Documentation, plans, reports, regulations
│   ├── models/       #   Vosk models es/en/pt (excluded from git)
│   └── scr/          #   Python source code
│       ├── ComponentesDAV/
│       │   ├── IntegracionGUI/  # Browser engine (navigation/) + panel mounting
│       │   ├── InterfazDAV/     # DavPanel: the GUI widget (no FreeCAD)
│       │   ├── Keychain/        # Dictionary key reading
│       │   ├── Dav/             # InitGui.py — startup inside FreeCAD
│       │   ├── Logos/
│       │   └── scripts/
│       ├── PruebaIntegracion/
│       ├── selection/           # CreateObjects — sub-element extraction
│       └── validation/          # Validator — command validation rules
└── CLAUDE.md
```

## Where each thing lives

| What are you looking for? | Where is it? |
|---|---|
| Voice navigation engine (`Browser`) | `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/navigation/browser.py` |
| Voice command tree | `Dav/dic/` |
| Spoken phrase → command translation | `TraduceTo*.py` inside each folder of `Dav/dic/` |
| Dictionary key reading | `Dav/scr/ComponentesDAV/Keychain/` |
| GUI widget (panel) | `Dav/scr/ComponentesDAV/InterfazDAV/DavPanel.py` |
| Sub-element extraction (selection) | `Dav/scr/selection/` |
| Command validation | `Dav/scr/validation/` |
| Vosk models (not versioned) | `Dav/models/` |
| Project documentation | `Dav/docs/es/` (Spanish) and `Dav/docs/en/` (English) |

## The voice command tree (`Dav/dic/`)

Each **folder** of the tree is a **context level** and contains:

- A master dictionary: `<name>.py` with the **internal keys → FreeCAD callables**
  (e.g. `explorer.py`, `sketcher.py`).
- Per-language translations: `TraduceToEs.py`, `TraduceToEn.py`, `TraduceToPT.py`
  that map **spoken phrases → the same callables**.

`Dav/dic/base.py` is the entry point: it links the top-level modules
(`explorer`, `stdview`, `workbench`, `lineattributes`, `preferences`).

The engine that walks this tree at runtime is `Browser`
(`Dav/scr/.../GUIFreeCad/navigation/browser.py`) + `DictionaryLoader`
(`navigation/dictionary_loader.py`).

> ⚠️ Important: although a `DAVAgent` with `latentListening` historically
> existed, the real implementation uses `Browser.ProcessPhrase` +
> `DictionaryLoader`. If an old diagram shows you `DAVAgent`, it is the
> original conceptual design, not the current code.

## The GUI is a docked panel

The panel (`DavPanel`) is a `QDockWidget` that runs inside FreeCAD and is fed
by the `Browser` **in process** via
`Dav/scr/.../GUIFreeCad/integration/dav_dock_panel.py`. The widget does not import
FreeCAD: it is handed data and emits signals, so it can be tested separately.

`MainWindow.py`, its own voice engine (`_VoiceMap`/`_GroupMeta`) and
`DiccionarioPrueba/` no longer exist: they were removed when the panel was docked.
