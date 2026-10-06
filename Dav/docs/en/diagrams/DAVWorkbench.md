# DAVWorkbench and commands

> **Files:**
> `Dav/scr/ComponentesDAV/Dav/InitGui.py`
> `Dav/scr/ComponentesDAV/Dav/scr/gui/dav_commands.py`
> `Dav/scr/ComponentesDAV/Dav/scr/gui/freecad_wb.py`

The workbench that FreeCAD loads at startup. It registers the commands of the DAV
toolbar and starts the voice engine.

```mermaid
classDiagram
    class DAVWorkbench {
        +String MenuText
        +String ToolTip
        +Initialize() void
        +GetClassName() String
    }

    class DAV_StartVoiceCommand {
        +GetResources() dict
        +Activated() void
        +IsActive() bool
    }

    class DAV_StopVoiceCommand {
        +GetResources() dict
        +Activated() void
        +IsActive() bool
    }

    class DAV_ShowPanelCommand {
        +GetResources() dict
        +Activated() void
        +IsActive() bool
    }

    class DAV_OpenPreferencesCommand {
        +GetResources() dict
        +Activated() void
        +IsActive() bool
    }

    class freecad_wb {
        <<module>>
        +setup_workbench(workbench) void
        +apply_dav_toolbar(workbench) void
        +install_gui_integration() void
        -_auto_start_voice_if_needed() void
        -_schedule_settings_watcher() void
        -_schedule_report_view() void
    }

    class dav_commands {
        <<module>>
        +register_commands() void
        -_ensure_gui_path() Path
        -_dictionary_root() Path
    }

    class voice_bootstrap {
        <<module>>
        +start_voice_engine(debug) bool
        +stop_voice_engine(wait, timeout) void
        +is_voice_running() bool
        +show_dock_panel() bool
    }

    class Gui_Workbench {
        <<FreeCAD>>
    }

    DAVWorkbench --|> Gui_Workbench : inherits
    DAVWorkbench ..> freecad_wb : setup_workbench
    freecad_wb ..> dav_commands : register_commands
    dav_commands ..> DAV_StartVoiceCommand : registers
    dav_commands ..> DAV_StopVoiceCommand : registers
    dav_commands ..> DAV_ShowPanelCommand : registers
    dav_commands ..> DAV_OpenPreferencesCommand : registers
    DAV_StartVoiceCommand ..> voice_bootstrap : start_voice_engine
    DAV_StopVoiceCommand ..> voice_bootstrap : stop_voice_engine
    DAV_ShowPanelCommand ..> voice_bootstrap : show_dock_panel
```

## Startup

```mermaid
sequenceDiagram
    participant F as FreeCAD
    participant W as DAVWorkbench
    participant V as voice_bootstrap
    participant S as DavVoiceService

    F->>W: Initialize()
    W->>W: setup_workbench()
    W->>W: register_commands()
    Note over W: deferred start ~1.5 s<br/>so the UI is not blocked
    W->>V: start_voice_engine()
    V->>V: resolves Dav/dic and the model
    V->>S: start_cad(adapter)
    S->>S: opens microphone on a separate thread
```

## Design notes

- **Several places call `start_voice_engine`** (the toolbar command,
  the workbench when it is activated, `freecad_voice_setup`): the log shows about four
  calls per startup. They do not step on each other (they are separated in time and
  `is_cad_engine_loaded()` stops them), so only the first one opens the microphone. That is why
  startup is logged at `debug` level.
- The `[DAV]` messages go to FreeCAD's **Report view** tab, not to the Python
  console. The real log is in `config/dav.log`.
