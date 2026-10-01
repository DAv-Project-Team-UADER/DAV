# How to test and validate

How to check that a change works **before** sending it for review. Different
layers depending on what you touched.

---

## 1. Purely technical test (fast, no FreeCAD)

For our own Python code (prompts, panels, modules), at least:

### Syntax

```bash
# Windows (PowerShell)
python -c "import ast; ast.parse(open(r'<file>', encoding='utf-8').read()); print('OK')"
```

### Import / smoke test with the development venv

The development venv (`IntegracionGUI/GUIFreeCad/.venv`) has PySide6. You can
import a module that does not require FreeCAD at import time (if it
imports `FreeCAD` at the top, use a deferred import inside the functions — the
pattern the prompts use).

### Prompt logic (without opening FreeCAD)

Prompts inherit `BaseInputPrompt` and their logic can be tested by calling
`ProcessFinalText("...")` directly with an offscreen `QApplication`:

```python
import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"
from InputPrompts.PlaneSelectionInputPrompt import PlaneSelectionInputPrompt
from PySide6.QtWidgets import QApplication
app = QApplication.instance() or QApplication([])

p = PlaneSelectionInputPrompt()
print(p.ProcessFinalText("abajo").Success)   # navigates
print(p.ProcessFinalText("okey").Value)       # confirms → plane value
```

It requires `GUIFreeCad` to be in `sys.path` (or configure the path).

### FreeCAD actions without opening the interface (`freecadcmd`)

To check that an **action** (creating a sketch, a solid, a TechDraw page)
really works, parsing the file is not enough: it has to be run in FreeCAD.
`freecadcmd` is FreeCAD **without a window**, with its Python and its modules (`Part`, `Sketcher`,
`Draft`, `TechDraw`), and it can be launched from the terminal. It works both for the dictionary
actions and for the prompts that use Qt (with `offscreen` mode).

| System | Executable |
| --- | --- |
| Windows | `C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe` |
| Linux | `freecadcmd` (or the one in the installation folder) |

**Template for a test script** (save it outside the repo, for example in the session's
temporary folder):

```python
import os, sys, traceback
os.environ["QT_QPA_PLATFORM"] = "offscreen"          # Qt without a screen

DAV = r"C:\path\to\repo\Dav"
sys.path[:0] = [
    DAV + r"\dic",                                   # to import Explorer.Examples...
    DAV + r"\scr\ComponentesDAV\IntegracionGUI\GUIFreeCad",   # to import InputPrompts
]

out = open("resultado.txt", "w")                     # see the note about the output
def log(*args):
    out.write(" ".join(str(a) for a in args) + "\n")
    out.flush()

try:
    import FreeCAD as App
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    App.newDocument("Prueba")
    from Explorer.Examples import _partdesign as ejemplo   # the module to test
    for paso in ejemplo.steps():
        paso.Action()                                # runs each action in order

    doc = App.ActiveDocument
    invalidos = [o.Name for o in doc.Objects if not o.isValid()]
    log("objetos:", len(doc.Objects), "invalidos:", invalidos)
except Exception:
    log(traceback.format_exc())
```

```powershell
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" prueba.py
Get-Content resultado.txt
```

What to look at and keep in mind:

- **Check `isValid()` of each object** after recomputing. An operation that fails does not
  raise an exception: it leaves the object in an invalid state (for example a hole that
  could not be created).
- **Write the results to a file.** The standard output of `freecadcmd` depends on
  how it is launched and often does not come back to the terminal; a file is always reliable.
- **Without an interface there is no 3D view.** `Gui.ActiveDocument`, `ViewFit` and the panels do not exist;
  the action code must tolerate that (see `fitView()` in `Explorer/Examples/_common.py`).
  Anything that depends on the view is tested inside FreeCAD with the interface.
- **The warning `2 entries found for module 'dav'`** means two copies of the module are
  installed and FreeCAD uses only one. When testing inside FreeCAD, verify that it is the copy
  you are editing.
- **Test the three languages** of a prompt by changing its language before dictating:
  `prompt._Language = "en"`.
- **Simulate the voice** by calling `prompt.ProcessFinalText("phrase")`: it returns the
  `PromptResult`, so you can check `Success`, `Value` and `Cancelled` without a microphone.
- **For a command with parameters**, `PromptedCommandExecutor.ExecuteEntry(entry, ["cinco okey"])`
  collects with simulated phrases, one per parameter.

---

## 2. Dictionary / navigation test

- **Loading the master dict** must not break: if a folder has a broken dict,
  the `DictionaryLoader` skips it and carries on (it does not bring the engine down).
- Check that the **new phrases appear** as options of the context: in the
  panel, after navigating to the context, the help/describe context will list the
  available commands (implicit in `Browser.DescribeContext`).
- Test each phrase in the three languages if you added translations.
- **Run the guided-examples verification** if you touch the examples or the words of
  the tree they use. It replays, in es, en and pt, each phrase of each frame through a real `Browser`,
  runs the actions and reports which phrase does not resolve or which command it reaches. It needs
  FreeCAD, so it is launched with `freecadcmd`:

  ```powershell
  $tests = "Dav\scr\ComponentesDAV\IntegracionGUI\GUIFreeCad\tests"
  & "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" "$tests\verify_examples_paths.py"
  Get-Content "$tests\verify_examples_paths.txt"
  ```

  A phrase "resolving" is not enough: also look at which command each frame reaches (`->`
  in the report). That is how it was found, for example, that "cortar" said from *Sumar* reached
  "cotar" through a fuzzy match, and that from *Círculo* "crear" jumps to Workbench.
- **Run the real hierarchy test** after touching any dictionary. It needs
  the `Dav` folder on the `PYTHONPATH` (the `TraduceTo*` files import `dic.StdView...`); without
  that, two tests fail with `No module named 'dic'`, even if the tree is fine:

  ```powershell
  cd Dav\scr\ComponentesDAV\IntegracionGUI\GUIFreeCad
  $env:PYTHONPATH = "<path to the repo>\Dav"
  python -m unittest tests.test_real_dictionaries
  ```

  It checks that `base.py` imports cleanly, that no submenu is flattened and that the
  translations were not left empty. High priority: a single broken import in a deep
  leaf leaves the `Browser` without commands and the `DictionaryLoader` does not warn about it.

---

## 3. Integrated test in FreeCAD (the one that counts)

Run the voice engine inside FreeCAD (see [setup](setup.md)) and test the
real voice flow. The existing guides detail what to expect:

| Guide | Covers |
|---|---|
| [voice-partdesign-testing-guide.md](../voice-partdesign-testing-guide.md) | PartDesign by voice with dictated measurements (solids, extrusion, cuts, finishes) |
| [voice-3d-testing-guide.md](../voice-3d-testing-guide.md) | Complete flow from 2D drawing and Assembly |
| [student-number-test-guide.md](../student-number-test-guide.md) | Number dictation (how to say measurements) |
| [voice-selection-manual.md](../voice-selection-manual.md) | Object selection by voice |
| [voice-explorer-manual.md](../voice-explorer-manual.md) | Explorer by voice (files) |
| [draftwork-test-report.md](../draftwork-test-report.md) | Draft workbench test report |

### Testing tips

- **`donde estoy`** (where am I) to locate yourself; **`subir`** (go up) to go up a level.
- Confirm pop-ups: `enter` · `enviar` · `aceptar` · `confirmar` · `ok`.
  Abort: `cancelar`.
- If a command "can't be heard", think of the **restricted grammar**: some
  prompts (numeric, plane selector) deliberately limit which words Vosk accepts
  (see [vosk-grammar-shortener.md](../vosk-grammar-shortener.md)).

---

## 4. Run the project tests

There is test/validation infrastructure in `Dav/scr/validation/`:

- `test_validator.py` — `Validator` tests.
- `test_integration.py` — integration tests (includes
  `PromptedCommandExecutor`).
- `run_tests.py` — run the tests in the folder.
- `prueba_validator.py` — test/validation helper.

```bash
python Dav/scr/validation/run_tests.py
```

> The `Validator` is integrated into command execution via
> `PromptedCommandExecutor` (prior parameter validation). If your command
> takes parameters, add coverage in these tests where appropriate.

---

## Quick checklist before sending the PR

- [ ] Syntax OK (AST parse) in modified/new files.
- [ ] Subcontexts are not flattened (`.update(sub_dict)`).
- [ ] New files have the mandatory header.
- [ ] Docstrings in English for public classes/methods.
- [ ] Phrases tested in the languages involved.
- [ ] Real voice flow tested in FreeCAD (if possible).
- [ ] Guide/doc updated if you changed a convention or a behavior.
