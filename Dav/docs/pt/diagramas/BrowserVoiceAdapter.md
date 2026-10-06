# BrowserVoiceAdapter

> **Arquivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/integration/browser_voice_adapter.py`

Une o motor de voz com o `Browser`. Recebe a frase crua que o Vosk reconheceu,
a limpa, a manda navegar e publica o resultado no painel DAV.

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

    BrowserVoiceAdapter "1" o-- "1" Browser : navega
    BrowserVoiceAdapter ..> _CapturedOutput : captura o stdout dos comandos
    BrowserVoiceAdapter ..> DavVoiceService : enfileira gramática
    BrowserVoiceAdapter ..> DavPanel : publica histórico e contexto
```

## O fluxo de uma frase

```mermaid
sequenceDiagram
    participant V as DavVoiceService
    participant A as BrowserVoiceAdapter
    participant B as Browser
    participant P as DavPanel

    V->>A: procesar_frase_final("archivo nuevo enviar")
    A->>A: _extract_token() → "archivo nuevo"
    Note over A: thread do microfone:<br/>mexer no Qt aqui é access violation
    A->>A: run_on_main_thread(_run)
    Note over A: já na thread da GUI
    A->>B: ProcessPhrase("archivo nuevo")
    Note over A: captura o stdout do comando
    B-->>A: BrowserResult
    A->>P: PublishHistory / PublishContext
    A->>V: set_grammar(novas frases)
```

## Por que existe `_CapturedOutput`

Os comandos dos dicionários (os `ayuda.py` sobretudo) escrevem sua saída
com `print`: são **988 chamadas distribuídas em 123 arquivos**. No FreeCAD isso vai
para o Report View, não para o painel DAV.

Em vez de mexer em cada comando, captura-se `sys.stdout` enquanto o comando roda e
o conteúdo é despejado no painel. Restaura `sys.stdout` mesmo se o comando lançar uma exceção.

## Notas de design

- **`procesar_frase_final` roda na thread do microfone.** Mexer em um widget Qt
  a partir dali é access violation: derruba o processo sem passar por nenhum
  `except`. Por isso tudo o que chega à GUI vai dentro de
  `run_on_main_thread`, e `_on_gui_thread()` verifica antes de publicar.
- **`_SendWords()` / `_CancelWords()` saem do dicionário**
  (`Browser.GetNavWords`), não de constantes. As constantes `_SEND_WORDS` e
  `_CANCEL_WORDS` ficam apenas como alternativa caso `NavCommands` não carregue.
- `_extract_token` corta o `enviar` final de «archivo nuevo enviar» e devolve
  `False` se a frase terminar em uma palavra de cancelamento.
