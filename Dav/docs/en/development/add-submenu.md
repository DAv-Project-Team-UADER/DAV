# Adding a submenu (a new folder) to the command tree

[Adding a command](add-command.md) explains how to add **one phrase** to a
context that already exists. This page covers the next case: creating **a new
context**, that is, a folder with its own commands that you enter by saying a
word ("archivo", "ejemplos"…).

The real example is `Dav/dic/Explorer/Examples/` (see [`Examples`](../diagrams/Examples.md)).

---

## What the folder must contain

```
Explorer/Examples/
├── __init__.py          # empty, but mandatory
├── Examples.py          # master dictionary: internal keys → callables
├── ayuda.py             # explains the level's commands
├── TraduceToEs.py       # spoken phrases in Spanish → the same callables
├── TraduceToEn.py       # ... in English
├── TraduceToPt.py       # ... in Portuguese
├── manual.svg           # icon for the 'manual' key
├── demos.svg            # icon for the 'demos' key
└── _manual.py, _demos.py  # command code (optional, leading underscore = internal use)
```

| Rule | Detail |
| --- | --- |
| **Folder, module and variable share the same name** | `Examples/Examples.py` defines `examples` (the variable is lowercase, like `explorer` in `Explorer/Explorer.py`) |
| **One folder = one level** | If a command has variants, those variants go in a child folder |
| **`ayuda.py` in every folder** | Its `ayuda` function goes in as the `'help'` key of the master dictionary |
| **Mandatory header** | All new files, see [conventions](conventions.md) |

---

## Step by step

### 1. Create the master dictionary

Internal keys are **a single English word**, without repeating the parent's context.

```python
# Examples/Examples.py
from .ayuda import ayuda
from ._demos import startExample
from ._manual import openManual

examples = {
    'manual': openManual,
    'demos':  startExample,
    'help':   ayuda,
}
```

### 2. Link it in the parent — **nested, never flattened**

```python
# Explorer/Explorer.py
from .Examples.Examples import examples

explorer.update({'examples': examples})   # CORRECT: 'examples' stays navigable
explorer.update(examples)                 # WRONG: flattens the leaves into the parent
```

Flattening breaks two things **silently**: keys repeated between leaves (`help`,
`create`…) overwrite each other and only the last one survives, and the folder
stops being a navigable node, so its `TraduceTo*.py` is never loaded. A test
checks this (`test_no_flattened_updates_in_dic`)

### 3. Write the three `TraduceTo*` files

Each one maps the **spoken phrases of that language** to the callables of the
master dictionary, by object (`examples['manual']`), without duplicating functions.

```python
# Examples/TraduceToEs.py
from .Examples import examples

TraduceToEs = {
    'manual':      examples['manual'],
    'referencia':  examples['manual'],
    'ejemplos':    examples['demos'],
    'ayuda':       examples['help'],
}
```

Notes:

- **The file name and the variable name match** (`TraduceToEs.py` defines `TraduceToEs`).
- At the root of `dic/` Portuguese is called `TraduceToPT.py`; in the subfolders,
  `TraduceToPt.py`. The `DictionaryLoader` accepts both spellings.
- Accent marks are optional: the engine compares without accents. The Vosk grammar
  does need the form found in the model's vocabulary.
- "subir" (go up), "enviar" (send), "cancelar" (cancel) and "dónde estoy" (where am I)
  are **not** defined here: they live in `Dav/dic/NavCommands/` and work in any context.
- The standard views (`StdView.StandardViews`) are appended at the end of several
  `TraduceTo*` files so the view can be changed from any context; copy that block
  from a sibling folder if you want the same.

### 4. Add the phrases to **enter** the folder in the parent's `TraduceTo*`

Without this the folder exists but nobody can reach it.

```python
# Explorer/TraduceToEs.py
'ejemplos':        explorer['examples'],
'quiero aprender': explorer['examples'],
'aprender':        explorer['examples'],
```

Repeat it in `TraduceToEn.py` and `TraduceToPt.py`, and check that the phrase does not
clash with another one already used in that context (a phrase repeated in the same
dictionary gets overwritten).

### 5. Add the icons — **they are looked up by key name**

The panel requests the SVG using the button's key: the `manual` key looks for `manual.svg`.
[`IconLocator`](../diagrams/IconLocator.md) indexes all the SVGs in `Dav/dic/` and
`InterfazDAV/Icons/` and compares them ignoring case, `_` and `-`.

| Situation | Result |
| --- | --- |
| Leaf with `<key>.svg` in any folder of `dic/` | Shows that icon |
| Leaf without an SVG | Button with the two-letter fallback (not an error) |
| **Two SVGs with the same name in different folders** | **They share an icon**: the first one found wins |
| Folder whose key matches the name of an existing SVG | The folder **inherits** that icon |

That is why key naming matters. In `Examples` the leaf is called `demos` and not
`examples`: since the folder is called `examples`, a leaf with the same name would
have given the folder an icon, and it was meant not to have one. Before settling on a
key, check whether an SVG with that name already exists:

```powershell
Get-ChildItem Dav\dic -Recurse -Filter "<key>.svg"
```

If the icon exists under another name, copy the SVG with the key's name (like
`manual.svg`, a copy of `File/open.svg`) or add an alias in `IconLocator._ALIASES`.

### 6. Update the help

Add the submenu to the parent's help (`Explorer/ayuda.py`) and describe the leaves in
the new folder's `ayuda.py`.

### 7. Verify

```powershell
cd Dav\scr\ComponentesDAV\IntegracionGUI\GUIFreeCad
$env:PYTHONPATH = "<path>\Dav"
python -m unittest tests.test_real_dictionaries
```

It checks that `base.py` imports cleanly, that no submenu is flattened and that the
folders are still navigable. **A single broken import in a deep leaf can leave the
`Browser` without any commands**, and the `DictionaryLoader` catches it and carries on,
so without this test you would not notice. To test your functions without opening the
interface, see [testing.md](testing.md).

---

## Checklist

- [ ] Folder with `__init__.py`, master dictionary, `ayuda.py` and the three `TraduceTo*` files.
- [ ] Linked **nested** in the parent's dictionary.
- [ ] Entry phrases added in the parent's three `TraduceTo*` files.
- [ ] Each leaf has its SVG named after the key (or the fallback icon was accepted).
- [ ] The folder's key does **not** match the name of any SVG of its leaves.
- [ ] `test_real_dictionaries` passes.
- [ ] Header in the new files and docstrings in English.
- [ ] Diagram in [`diagrams/`](../diagrams/README.md) if the folder brings new classes or flows.

---

Previous: [Adding a command](add-command.md) · Next: [Adding a voice dialog](add-prompt.md)
