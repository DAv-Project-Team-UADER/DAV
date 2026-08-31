# Instructions and Project Rules for DAV Agents

## Mandatory Convention: Nested Subcontexts (Rule 4)

When assembling the master dictionary of any folder in `Dav/dic/`, every submenu MUST be added as a nested dictionary under its own dedicated key, NEVER merged directly via `.update(sub_dict)`:

### Correct Pattern (Reference: `Explorer/Explorer.py`)
```python
explorer.update({'file': file})
explorer.update({'edit': edit})
```

### Incorrect Pattern (Flattens child leaves into parent)
```python
# DO NOT DO THIS — flattens child leaves into parent
explorer.update(file)
explorer.update(edit)
```

### Why it Matters:
1. **Silent Key Collisions**: Multiple sub-dictionaries define common key names (`create`, `help`, `center`, `horizontal`). Using direct `.update(sub_dict)` causes later submenus to silently overwrite earlier keys.
2. **Orphaned Translations**: `DictionaryLoader` loads `TraduceTo*.py` for a folder ONLY when `Browser` descends to that folder as a frame. If a parent flattens the child, the folder is lost as a navigable node in the stack, and its translation file is never loaded even if correctly written.

### New Workbench / Submenu Checklist:
- Always nest sub-dictionaries using `parent_dict.update({'submenu_key': submenu_dict})`.
- Ensure the folder remains navigable so `Browser` can descend and `DictionaryLoader` reads its `TraduceTo*.py`.
- Run integration tests to verify AST adherence: `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/.venv/Scripts/python.exe -m unittest Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/tests/test_real_dictionaries.py`.
