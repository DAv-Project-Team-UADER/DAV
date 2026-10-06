# DavVoiceService

> **Arquivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/speech/dav_voice_service.py`

Singleton que possui o microfone e o recognizer do Vosk. Uma única thread de áudio
para todo o DAV: compartilham-na a navegação CAD e o diálogo de Preferências, que
antes disputavam o dispositivo.

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
    DavVoiceService ..> KaldiRecognizer : possui em _listen_loop
```

## Os dois modos

```mermaid
stateDiagram-v2
    [*] --> idle
    idle --> cad : start_cad(adapter)
    cad --> preferences : attach_preferences()
    preferences --> cad : detach_preferences()
    preferences --> idle : detach sem adapter CAD
    cad --> idle : stop()
```

| Modo | Quem consome | Gramática |
| --- | --- | --- |
| `cad` | `BrowserVoiceAdapter` | Contexto de navegação ativo |
| `preferences` | Diálogo de Preferências | 81 frases de configuração |
| `idle` | Ninguém | Microfone fechado |

## A thread de áudio

`_listen_loop` roda em uma thread separada (`DAV-VoiceService`) para não bloquear a
UI do FreeCAD. A cada volta:

1. Drena `_grammar_queue` e fica com a última gramática
2. Se mudou: `Reset()` + `SetGrammar()` — **sempre nesta thread**, nunca a partir
   da GUI
3. `AcceptWaveform()` e despacha o texto conforme o modo

Detalhe de por que o `Reset()` é obrigatório (o Vosk aborta o processo sem ele):
[`encurtador-gramatica-vosk.md`](../encurtador-gramatica-vosk.md).

## Notas de design

- **`_ensure_mic` reinicia a thread se o idioma ou o tamanho do modelo mudou**,
  porque o modelo é carregado uma única vez ao criar o recognizer.
- As falhas da thread ficam em `config/dav.log`: se o log cortar sem a linha
  `hilo de voz terminado`, o processo morreu dentro do loop.
- `_dispatch_to_active_prompt` dá prioridade aos `InputPrompts` abertos sobre
  a navegação normal.
