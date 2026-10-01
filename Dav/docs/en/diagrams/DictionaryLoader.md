# DictionaryLoader

> **File:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/navigation/dictionary_loader.py`

Loads the modules of `Dav/dic/` from disk: the base dictionary, the per-language
translations and the submenus. It isolates the `Browser` from the file system and from
import details.

```mermaid
classDiagram
    class DictionaryLoader {
        +Path DictionaryRoot
        +bool IsReady

        +LoadBaseModuleDict() dict
        +LoadModuleDictByName(module, attr) dict
        +LoadModuleDictForKey(folder, key) dict
        +LoadTranslateMap(folder, language) dict
        +LoadTranslateSpokenKeys(folder, language) list~String~
        +ResolveSubFolder(parent, key, target) Path
        +NormalizeSpoken(text)$ String
        -_ImportTranslateModule(folder, language) Module
        -_ImportFreshModule(name, path) Module
        -_FindChildByTargetIdentity(parent, target) Path
        -_FindChildCaseInsensitive(parent, name) Path
    }

    class LanguageCode {
        <<enumeration>>
        Es
        En
        PT
        +FromStorage(value)$ LanguageCode
    }

    DictionaryLoader ..> LanguageCode : selects TraduceTo*
    Browser "1" o-- "1" DictionaryLoader : uses
```

## Which files it looks for

```
Dav/dic/
├── base.py                 → LoadBaseModuleDict()
├── TraduceToEs.py          → LoadTranslateMap(root, Es)
├── NavCommands/
│   ├── NavActions.py       → LoadModuleDictByName("NavCommands.NavActions", "NavActions")
│   └── TraduceToEs.py      → LoadTranslateMap(NavCommands, Es)
└── explorer/
    ├── explorer.py         → base dictionary of the folder
    └── TraduceToEs.py      → LoadTranslateMap(explorer, Es)
```

One folder = one context level. Each has its base dictionary (internal
keys → FreeCAD callables) and its per-language translations (spoken phrases →
the same callables).

## Design notes

- **It tolerates a missing dictionary.** If the folder is missing or a module fails
  to import, it returns empty and leaves a message: the engine starts with empty
  contexts instead of breaking FreeCAD's startup.
- **`ResolveSubFolder` matches by the identity of the `Target`**, not by folder
  name: the name may differ from the internal key.
- `_ImportFreshModule` forces a reload so that a change in a dictionary is
  seen without restarting FreeCAD.
- Accent normalization lives here (`NormalizeSpoken`) and must be the same one
  used by `ContextEntry`.
