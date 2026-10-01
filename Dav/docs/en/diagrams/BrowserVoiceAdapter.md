# BrowserVoiceAdapter

> **File:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/integration/browser_voice_adapter.py`

Connects the voice engine to the `Browser`. It receives the raw phrase recognized by Vosk,
cleans it, sends it to navigate, and publishes the result in the DAV panel.

```mermaid
classDiagram
    class BrowserVoiceAdapter {
        -Browser _browser
        -bool _stop_requested

        +explorador() None
        +request_stop() void
        +procesar_frase_final(raw_phrase) void
        -_update_grammar() void
        -_SendWords() set~String~
        -_CancelWords() set~String~
        -_extract_token(normalized) String
        -_export_state() void
        -_publish_line(line, recognized, unknown)$ void
        -_publish_to_dock()$ void
        -_on_gui_thread()$ bool
    }

    class _CapturedOutput {
        -StringIO _buffer
        -TextIO _previous
        +Lines() list~String~
    }

    BrowserVoiceAdapter "1" o-- "1" Browser : navigates
    BrowserVoiceAdapter ..> _CapturedOutput : captures the commands' stdout
    BrowserVoiceAdapter ..> DavVoiceService : queues grammar
    BrowserVoiceAdapter ..> DavPanel : publishes history and context
```

## The flow of a phrase

```mermaid
sequenceDiagram
    participant V as DavVoiceService
    participant A as BrowserVoiceAdapter
    participant B as Browser
    participant P as DavPanel

    V->>A: procesar_frase_final("archivo nuevo enviar")
    A->>A: _extract_token() → "archivo nuevo"
    Note over A: microphone thread:<br/>touching Qt here is an access violation
    A->>A: run_on_main_thread(_run)
    Note over A: now on the GUI thread
    A->>B: ProcessPhrase("archivo nuevo")
    Note over A: captures the command's stdout
    B-->>A: BrowserResult
    A->>P: PublishHistory / PublishContext
    A->>V: set_grammar(new phrases)
```

(The phrase `"archivo nuevo enviar"` is spoken Spanish: "new file send".)

## Why `_CapturedOutput` exists

The dictionary commands (the `ayuda.py` files above all) write their output
with `print`: there are **988 calls spread across 123 files**. In FreeCAD that goes
to the Report View, not to the DAV panel.

Instead of touching every command, `sys.stdout` is captured while the command runs
and then dumped into the panel. It restores `sys.stdout` even if the command raises.

## Design notes

- **`procesar_frase_final` runs on the microphone thread.** Touching a Qt widget
  from there is an access violation: it crashes the process without going through any
  `except`. That is why everything that reaches the GUI goes inside
  `run_on_main_thread`, and `_on_gui_thread()` checks before publishing.
- **`_SendWords()` / `_CancelWords()` come from the dictionary**
  (`Browser.GetNavWords`), not from constants. The `_SEND_WORDS` and
  `_CANCEL_WORDS` constants remain only as a fallback in case `NavCommands` fails to load.
- `_extract_token` strips the trailing `enviar` ("send") from "archivo nuevo enviar" and returns
  `False` if the phrase ends in a cancel word.
