# Regenerating the user manual (PDF)

`Manual_Usuario.pdf` (Spanish), `User_Manual.pdf` (English) and `Manual_do_Usuario.pdf` (Portuguese)
are in the **repository root** and are **not edited by hand**: they are built by
[`build_manual.py`](../manual/build_manual.py), which reads the real dictionaries in `Dav/dic/`
(groups, commands, phrases in each language and icons). That is why the manual does not go out of date
when a feature is added: it is enough to generate it again.

## Requirements

- Python 3 with **PyMuPDF** and **PySide6** (Qt is used to rasterize the SVG icons):

  ```
  pip install pymupdf PySide6
  ```

- FreeCAD does not need to be installed: `arbol.py` simulates FreeCAD and Qt when loading the tree.

## Generating the PDFs

From the repository root (it also works from any folder):

```
python Dav/docs/manual/build_manual.py              # all three languages
python Dav/docs/manual/build_manual.py es           # only one (es | en | pt)
python Dav/docs/manual/build_manual.py --salida C:/tmp   # another output folder
```

By default it writes the three PDFs in the repository root, overwriting the existing ones. When it finishes
it reports which commands were left **without a description** in the `desc_*.py` files.

## What is in `Dav/docs/manual/`

| File | What it contains |
|---|---|
| `arbol.py` | Loads the dictionary tree: groups, commands, phrases and SVG icons (same criterion as `IconLocator`) |
| `desc_*.py` | **What each command does**, in Spanish, English and Portuguese, and its requirement |
| `textos.py` | Fixed texts (introduction, navigation, examples, acknowledgments) and the reusable requirements |
| `build_manual.py` | Builds the HTML and lays it out as a PDF (index, bookmarks and table headers) |
| `img/` | Logo and screenshots of the guided examples |

## Adding a feature to the manual

1. Add it to the dictionary as usual (with its `TraduceTo*.py` and its `<key>.svg`).
2. In the `desc_*.py` of the corresponding workbench, add the entry
   `"path/key": ("Spanish", "English", "Portuguese"[, "requirement code"])`.
   The path is the one made of the dictionary keys (`workbench/partdesign/additive/pad`).
3. Run `build_manual.py` again and review the warning about commands without a description.
4. Commit the three regenerated PDFs together with the change.

The **groups** (submenus such as PartDesign's "agregar" (add)) come out on their own as a row with their icon and
the phrases to enter them; only their description is needed. A group without its own SVG uses the icon of its
first command; a command without an SVG can take that of its variant in `ICONO_PARIENTE`
(`build_manual.py`). The requirement codes (`doc`, `sel`, `bodysk`…) are in `textos.py`.

## Common problems

- **`ModuleNotFoundError: pymupdf` / `PySide6`**: install the packages above in the same
  Python used to run the script.
- **A command appears without a description or without an icon**: its entry in `desc_*.py` or its
  `<key>.svg` in the dictionary is missing.
- **The PDF does not change**: confirm that it was written to the expected folder (`--salida` option) and
  that the viewer does not have the file open (on Windows it blocks writing).
