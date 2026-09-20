# ModelManager

> **Archivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/core/model_manager.py`

Módulo de funciones (no una clase) que **verifica y descarga los modelos de Vosk**.
Cada idioma tiene un modelo *chico* (viene con el proyecto) y uno *grande* (se baja
a pedido). Decide qué carpeta usar según la preferencia de tamaño y qué hay en disco.

```mermaid
classDiagram
    class model_manager {
        <<módulo>>
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
        <<core/settings>>
        +Path MODELS_DIR
    }

    class DavVoiceService
    class voice_bootstrap {
        <<integration>>
    }

    class PreferencesDialog {
        <<ui/preferences_dialog>>
    }

    class Vosk {
        <<alphacephei.com>>
    }

    model_manager ..> settings : MODELS_DIR
    DavVoiceService ..> model_manager : get_active_model_path
    voice_bootstrap ..> model_manager : get_active_model_path
    PreferencesDialog ..> model_manager : verify_small_models y download_large_model
    model_manager ..> Vosk : descarga el .zip
```

## Catálogo

| Idioma | Modelo chico | Modelo grande |
| --- | --- | --- |
| `es` | `vosk-model-small-es-0.42` | `vosk-model-es-0.42` |
| `en` | `vosk-model-small-en-us-0.15` | `vosk-model-en-us-0.22` |
| `pt` | `vosk-model-small-pt-0.3` | `vosk-model-pt-fb-v0.1.1-20220516_2113` |

## Qué modelo se elige

```mermaid
flowchart TD
    A["get_active_model_path(idioma, tamaño)"] --> B{¿idioma<br/>en el catálogo?}
    B -->|no| N[None]
    B -->|sí| C{¿pidió grande<br/>y está instalado?}
    C -->|sí| L[modelo grande]
    C -->|no| D{¿está el<br/>chico?}
    D -->|sí| S[modelo chico]
    D -->|no| N
```

## Notas de diseño

- **Un modelo es válido si la carpeta tiene alguno de sus archivos característicos**
  (`am`, `graph`, `conf`, `ivector`, `final.mdl`, `Gr.fst`). Una carpeta vacía o a medio
  descargar no cuenta.
- **Pedir el grande sin tenerlo cae al chico**, así el reconocimiento nunca queda sin modelo
  si el chico está.
- **`download_large_model`** baja el `.zip`, lo descomprime en `MODELS_DIR`, borra el `.zip`
  y valida el resultado; si la carpeta extraída tiene otro nombre, la renombra. Informa el
  progreso con un `progress_callback(descargado, total)`.
- **El tamaño** lo da `settings.model_size` (preferencia del usuario).
- **La carpeta de modelos** sale de `core/settings.py` y respeta `DAV_MODELS_DIR`.
- Un modelo grande **no mejora** el reconocimiento de comandos: ver `pendientes-dav.md` §10.
