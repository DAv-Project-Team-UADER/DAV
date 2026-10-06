# FreecadGuiBridge

> **File:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/integration/freecad_gui_bridge.py`

Bridge **from the microphone thread to Qt's main thread**. FreeCAD commands
(`Gui.runCommand`, creating objects, opening dialogs) can only be executed from the
interface thread, but speech is recognized on another one. The bridge receives a function
from any thread and queues it so that it runs on the main one.

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
        <<module functions>>
        +init_gui_bridge() FreecadGuiBridge
        +run_on_main_thread(fn) void
        +request_open_preferences() void
    }

    class PromptVoiceRouter
    class BrowserVoiceAdapter
    class launch_preferences

    FreecadGuiBridge --|> QObject
    bridge_api ..> FreecadGuiBridge : single instance
    PromptVoiceRouter ..> bridge_api : run_on_main_thread
    BrowserVoiceAdapter ..> bridge_api : runs the command on the main thread
    FreecadGuiBridge ..> launch_preferences : fallback when opening Preferences
```

## How it works

```mermaid
sequenceDiagram
    participant H as Microphone thread
    participant B as FreecadGuiBridge
    participant Q as Qt event queue
    participant M as Main thread

    H->>B: run_on_main_thread(fn)
    B->>Q: emits main_call_requested(fn)<br/>QueuedConnection
    Q->>M: delivers the signal
    M->>B: _run_main_call(fn)
    M->>M: fn()
    Note over M: if it fails, it prints the error to the<br/>FreeCAD console and carries on
```

## Responsibilities

| Element | What it does |
| --- | --- |
| `run_on_main_thread(fn)` | Queues `fn` on the main thread. It is safe to call from any thread |
| `request_open_preferences()` | Requests opening DAV's Preferences from the voice thread |
| `init_gui_bridge()` | Creates the bridge the first time and always returns the same one |
| `_run_main_call(fn)` | Runs the function; an error is reported but **does not bring down the interface thread** |
| `_open_preferences()` | Tries `Gui.runCommand("DAV_OpenPreferences")`; if that fails it uses [`launch_preferences`](LaunchPreferences.md) |

## Design notes

- **`QueuedConnection` is what switches threads.** With a direct connection the function
  would run on the emitting thread, not on Qt's.
- **Lazy single instance:** the `QObject` must be created on the main thread; that is why
  `init_gui_bridge()` is called when preparing the voice (`freecad_voice_setup.py`) and not from the voice thread.
- If `run_on_main_thread` is not available (outside FreeCAD), `PromptVoiceRouter` runs
  the function directly.
