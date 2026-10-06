# FreecadGuiBridge

> **Arquivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/integration/freecad_gui_bridge.py`

Ponte **da thread do microfone para a thread principal do Qt**. Os comandos do FreeCAD
(`Gui.runCommand`, criar objetos, abrir diálogos) só podem ser executados a partir da
thread da interface, mas a voz é reconhecida em outra. A ponte recebe uma função
de qualquer thread e a enfileira para que rode na principal.

```mermaid
classDiagram
    class QObject {
        <<Qt>>
    }

    class FreecadGuiBridge {
        +Signal open_preferences_requested
        +Signal main_call_requested
        -_run_main_call(fn) void
        -_open_preferences() void
    }

    class bridge_api {
        <<funções do módulo>>
        +init_gui_bridge() FreecadGuiBridge
        +run_on_main_thread(fn) void
        +request_open_preferences() void
    }

    class PromptVoiceRouter
    class BrowserVoiceAdapter
    class launch_preferences

    FreecadGuiBridge --|> QObject
    bridge_api ..> FreecadGuiBridge : instância única
    PromptVoiceRouter ..> bridge_api : run_on_main_thread
    BrowserVoiceAdapter ..> bridge_api : executa o comando na thread principal
    FreecadGuiBridge ..> launch_preferences : alternativa ao abrir Preferências
```

## Como funciona

```mermaid
sequenceDiagram
    participant H as Thread do microfone
    participant B as FreecadGuiBridge
    participant Q as Fila de eventos do Qt
    participant M as Thread principal

    H->>B: run_on_main_thread(fn)
    B->>Q: emite main_call_requested(fn)<br/>QueuedConnection
    Q->>M: entrega o sinal
    M->>B: _run_main_call(fn)
    M->>M: fn()
    Note over M: se falhar, imprime o erro no<br/>console do FreeCAD e segue
```

## Responsabilidades

| Elemento | O que faz |
| --- | --- |
| `run_on_main_thread(fn)` | Enfileira `fn` na thread principal. É seguro chamá-la de qualquer thread |
| `request_open_preferences()` | Pede para abrir as Preferências do DAV a partir da thread de voz |
| `init_gui_bridge()` | Cria a ponte na primeira vez e devolve sempre a mesma |
| `_run_main_call(fn)` | Executa a função; um erro é informado mas **não derruba a thread da interface** |
| `_open_preferences()` | Tenta `Gui.runCommand("DAV_OpenPreferences")`; se falhar usa [`launch_preferences`](LaunchPreferences.md) |

## Notas de design

- **`QueuedConnection` é o que troca de thread.** Com uma conexão direta a função
  rodaria na thread que emite, não na do Qt.
- **Instância única preguiçosa:** o `QObject` deve ser criado na thread principal; por isso
  `init_gui_bridge()` é chamado ao preparar a voz (`freecad_voice_setup.py`) e não a partir da thread de voz.
- Se `run_on_main_thread` não estiver disponível (fora do FreeCAD), `PromptVoiceRouter` executa
  a função diretamente.
