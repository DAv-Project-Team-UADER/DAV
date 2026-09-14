# DavVoiceService

> **Archivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/speech/dav_voice_service.py`

Singleton que posee el micrófono y el recognizer de Vosk. Un solo hilo de audio
para todo DAV: lo comparten la navegación CAD y el diálogo de Preferencias, que
antes competían por el dispositivo.

```mermaid
classDiagram
    class DavVoiceService {
        <<singleton>>
        -DavVoiceService _instance$
        -String _mode
        -Thread _thread
        -Event _stop_event
        -Lock _lock
        -Queue _grammar_queue
        -Object _cad_adapter
        -_PreferencesCallbacks _prefs
        -bool _running
        -bool _mic_open
        -bool _accept_callbacks
        -String _language
        -String _model_size

        +get()$ DavVoiceService
        +set_grammar(phrases) void
        +start_cad(adapter) bool
        +attach_preferences(language, callbacks) bool
        +detach_preferences() void
        +resume_cad_voice() void
        +is_mic_running() bool
        +is_cad_engine_loaded() bool
        +preferences_listening() bool
        +stop(wait) void
        +request_cad_stop() void
        -_ensure_mic(language, model_size) bool
        -_listen_loop(model_path) void
        -_dispatch_text(text, final) void
        -_handle_preferences_text(text, final, prefs) void
        -_dispatch_to_active_prompt(text, final) bool
    }

    class _PreferencesCallbacks {
        <<dataclass>>
        +Callable on_command
        +Callable on_text
        +Callable on_status
        +Callable on_audio
        +String language
    }

    class KaldiRecognizer {
        <<Vosk>>
        +AcceptWaveform(data) bool
        +Reset() void
        +SetGrammar(json) void
    }

    DavVoiceService "1" o-- "0..1" _PreferencesCallbacks : modo preferences
    DavVoiceService "1" o-- "0..1" BrowserVoiceAdapter : modo cad
    DavVoiceService ..> KaldiRecognizer : posee en _listen_loop
```

## Los dos modos

```mermaid
stateDiagram-v2
    [*] --> idle
    idle --> cad : start_cad(adapter)
    cad --> preferences : attach_preferences()
    preferences --> cad : detach_preferences()
    preferences --> idle : detach sin adapter CAD
    cad --> idle : stop()
```

| Modo | Quién consume | Gramática |
| --- | --- | --- |
| `cad` | `BrowserVoiceAdapter` | Contexto de navegación activo |
| `preferences` | Diálogo de Preferencias | 81 frases de configuración |
| `idle` | Nadie | Micrófono cerrado |

## El hilo de audio

`_listen_loop` corre en un hilo aparte (`DAV-VoiceService`) para no bloquear la
UI de FreeCAD. En cada vuelta:

1. Drena `_grammar_queue` y se queda con la última gramática
2. Si cambió: `Reset()` + `SetGrammar()` — **siempre en este hilo**, nunca desde
   la GUI
3. `AcceptWaveform()` y despacha el texto según el modo

Detalle de por qué el `Reset()` es obligatorio (Vosk aborta el proceso sin él):
[`acortador-gramatica-vosk.md`](../acortador-gramatica-vosk.md).

## Notas de diseño

- **`_ensure_mic` reinicia el hilo si cambió el idioma o el tamaño del modelo**,
  porque el modelo se carga una sola vez al crear el recognizer.
- Los fallos del hilo quedan en `config/dav.log`: si el log corta sin la línea
  `hilo de voz terminado`, el proceso murió dentro del loop.
- `_dispatch_to_active_prompt` da prioridad a los `InputPrompts` abiertos sobre
  la navegación normal.
