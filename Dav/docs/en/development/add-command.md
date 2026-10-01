# Adding a voice command

The goal is that saying a **spoken phrase** runs a FreeCAD **action**. You get
that by editing the **command tree** (`Dav/dic/`), without touching the engine
(`Browser`).

Each folder in `Dav/dic/` is a **context level** and contains:

1. **A master dictionary** (`<name>.py`) — internal keys → callables.
2. **Per-language translations** (`TraduceToEs.py`, `TraduceToEn.py`,
   `TraduceToPT.py`) — spoken phrases → the same callables.

## Step by step

### 1. Find the context folder

For example, the Sketcher workbench commands live in
`Dav/dic/Workbench/Sketcher/`. If the command belongs to a submenu, it goes in
its child folder (e.g. `Sketcher/point/point.py`, `Sketcher/Geometry/geometry.py`).

### 2. Add the internal key to the master dictionary

Inside the master dict (e.g. `sketcher.py`), add the key and its callable:

```python
sketcher = {}
sketcher.update({
    'new': _new_sketch,     # own function that creates the sketch
    'edit': lambda: Gui.runCommand('Sketcher_EditSketch', 0),
    # ...
})
```

> If the action is a native FreeCAD command that does **not** open a dialog
> that can be controlled by voice, a `lambda: Gui.runCommand('FreeCAD_Command', 0)`
> is enough. If the native command opens its own dialog (like the plane
> selector of `Sketcher_NewSketch`), you must replace it with a DAV action of
> your own that uses a voice-controllable prompt (see the example below).

### 3. Add the spoken phrases in the `TraduceTo*.py` files

In the context's `TraduceToEs.py`, map the phrase(s) to the key:

```python
from .sketcher import sketcher

TraduceToEs = {
    "nuevo": sketcher["new"],
    "nuevo croquis": sketcher["new"],
    "crear croquis": sketcher["new"],
    # ...
}
```

> Adding synonyms is **only** a matter of editing these dictionaries: the
> engine does not need to be touched. The `DictionaryLoader` normalizes accents
> when comparing, so the variants with/without accent marks are optional but
> harmless.

### 4. (Optional) Update the folder's `ayuda.py`

Many contexts have an `ayuda.py` that prints the available commands.
Add the line for the new command so the help stays consistent.

### 5. Try it

Check that the phrase navigates and runs the action (see
[testing.md](testing.md)). Test in **all three languages** if you added
phrases in all three `TraduceTo` files.

---

## Real example: the voice plane selector when creating a sketch

Context: FreeCAD opens a native dialog (`Sketcher_NewSketch`) that is **not
controllable by voice**. The solution was a DAV action of our own that shows a
prompt navigable by voice.

**Files touched** (for reference):

- `Dav/scr/.../InputPrompts/PlaneSelectionInputPrompt.py` — the selection
  window: it cycles through `XY` / `XZ` / `YZ` with `arriba`/`abajo` (up/down)
  and confirms with `okey`/`cancelar` (okay/cancel) (inheriting `BaseInputPrompt`).
- `Dav/dic/Workbench/Sketcher/new_sketch/new_sketch.py` — the action: it shows
  the prompt, takes the chosen plane and creates the `Sketcher::SketchObject`
  with the same placement as the native command.
- `Dav/scr/.../InputPrompts/PlaneGrammarSwitcher.py` — restricts the Vosk
  grammar while the prompt is open to just `arriba/abajo/okey/cancelar`, so it
  does not confuse "abajo" with "trabajo".
- `Dav/dic/Workbench/Sketcher/sketcher.py` — `'new'` now points to
  `_new_sketch` instead of `Gui.runCommand('Sketcher_NewSketch', 0)`.
- `Dav/dic/Workbench/Sketcher/Geometry/geometry.py` — same for the geometry
  subcontext.
- `Dav/dic/Workbench/Sketcher/TraduceToEs.py` — new synonyms
  `nuevo boceto` / `crear boceto` / `boceto nuevo`.

**Points to copy from this example**:

- If the command opens a native dialog, **replace it** with a DAV prompt
  (inherit `BaseInputPrompt` and use `PromptVoiceRouter`).
- If the prompt needs Vosk to listen to only a small set of words, use a
  "grammar switcher" (the `NumericGrammarSwitcher` pattern) and restore the
  previous grammar when closing.
- Report the result of the action in the GUI (with `print`) so it shows up in
  the panel history.

---

## Rules to avoid breaking anything

- **Nested subcontexts**: `explorer.update({'file': file})`, never
  `explorer.update(file)`. See [conventions](conventions.md).
- The `TraduceTo*.py` files must import the master dict and link
  **by object/key**, not duplicate callables.
- Keep the **mandatory header** in every new file.
- Do not touch `browser.py` to add a command: the command goes in the dictionary.

---

Need a new folder? See [Adding a submenu](add-submenu.md). A voice dialog? See [Adding a voice dialog](add-prompt.md).

Next: [Adding a submenu](add-submenu.md)
