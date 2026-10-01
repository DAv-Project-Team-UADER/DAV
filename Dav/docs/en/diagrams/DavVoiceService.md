# DavVoiceService

> **File:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/speech/dav_voice_service.py`

Singleton that owns the microphone and the Vosk recognizer. A single audio thread
for all of DAV: it is shared by CAD navigation and the Preferences dialog, which
used to compete for the device.

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

    DavVoiceService "1" o-- "0..1" _PreferencesCallbacks : preferences mode
    DavVoiceService "1" o-- "0..1" BrowserVoiceAdapter : cad mode
    DavVoiceService ..> KaldiRecognizer : owns in _listen_loop
```

## The two modes

```mermaid
stateDiagram-v2
    [*] --> idle
    idle --> cad : start_cad(adapter)
    cad --> preferences : attach_preferences()
    preferences --> cad : detach_preferences()
    preferences --> idle : detach without a CAD adapter
    cad --> idle : stop()
```

| Mode | Who consumes | Grammar |
| --- | --- | --- |
| `cad` | `BrowserVoiceAdapter` | Active navigation context |
| `preferences` | Preferences dialog | 81 configuration phrases |
| `idle` | Nobody | Microphone closed |

## The audio thread

`_listen_loop` runs on a separate thread (`DAV-VoiceService`) so as not to block
FreeCAD's UI. On each iteration:

1. It drains `_grammar_queue` and keeps only the latest grammar
2. If it changed: `Reset()` + `SetGrammar()` — **always on this thread**, never from
   the GUI
3. `AcceptWaveform()` and dispatches the text according to the mode

Details on why `Reset()` is mandatory (Vosk aborts the process without it):
[`vosk-grammar-shortener.md`](../vosk-grammar-shortener.md).

## Design notes

- **`_ensure_mic` restarts the thread if the language or the model size changed**,
  because the model is loaded only once, when the recognizer is created.
- Thread failures are recorded in `config/dav.log`: if the log stops without the line
  `hilo de voz terminado` (voice thread finished), the process died inside the loop.
- `_dispatch_to_active_prompt` gives priority to open `InputPrompts` over
  normal navigation.
