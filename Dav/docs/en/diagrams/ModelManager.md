# ModelManager

> **File:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/core/model_manager.py`

A module of functions (not a class) that **verifies and downloads the Vosk models**.
Each language has a *small* model (shipped with the project) and a *large* one
(downloaded on demand). It decides which folder to use based on the size
preference and what is on disk.

```mermaid
classDiagram
    class model_manager {
        <<module>>
        +dict MODEL_CATALOG
        +str MODEL_BASE_URL
        +has_small_model(language) bool
        +has_large_model(language) bool
        +verify_small_models() dict
        +get_active_model_path(language, size) Path
        +download_large_model(language, progress_callback) Path
        -_model_path(folder_name) Path
        -_is_valid_model(path) bool
    }

    class settings {
        <<core settings>>
        +Path MODELS_DIR
    }

    class DavVoiceService
    class voice_bootstrap {
        <<integration>>
    }

    class PreferencesDialog {
        <<ui preferences_dialog>>
    }

    class Vosk {
        <<alphacephei com>>
    }

    model_manager ..> settings : MODELS_DIR
    DavVoiceService ..> model_manager : get_active_model_path
    voice_bootstrap ..> model_manager : get_active_model_path
    PreferencesDialog ..> model_manager : verify_small_models and download_large_model
    model_manager ..> Vosk : downloads the .zip
```

## Catalog

| Language | Small model | Large model |
| --- | --- | --- |
| `es` | `vosk-model-small-es-0.42` | `vosk-model-es-0.42` |
| `en` | `vosk-model-small-en-us-0.15` | `vosk-model-en-us-0.22` |
| `pt` | `vosk-model-small-pt-0.3` | `vosk-model-pt-fb-v0.1.1-20220516_2113` |

## Which model is chosen

```mermaid
flowchart TD
    A["get_active_model_path(language, size)"] --> B{language<br/>in the catalog?}
    B -->|no| N[None]
    B -->|yes| C{large requested<br/>and installed?}
    C -->|yes| L[large model]
    C -->|no| D{is the<br/>small one there?}
    D -->|yes| S[small model]
    D -->|no| N
```

## Design notes

- **A model is valid if its folder contains any of its characteristic files**
  (`am`, `graph`, `conf`, `ivector`, `final.mdl`, `Gr.fst`). An empty or half-downloaded
  folder does not count.
- **Requesting the large model without having it falls back to the small one**, so
  recognition is never left without a model as long as the small one is present.
- **`download_large_model`** downloads the `.zip`, extracts it into `MODELS_DIR`, deletes the `.zip`
  and validates the result; if the extracted folder has a different name, it renames it. It reports
  progress through a `progress_callback(downloaded, total)`.
- **The size** comes from `settings.model_size` (user preference).
- **The models folder** comes from `core/settings.py` and honors `DAV_MODELS_DIR`.
- A large model does **not** improve command recognition: see `pendientes-dav.md` §10.
