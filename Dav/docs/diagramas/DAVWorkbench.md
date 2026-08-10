# DAVWorkbench y comandos

> **Archivos:**
> `Dav/scr/ComponentesDAV/Dav/InitGui.py`
> `Dav/scr/ComponentesDAV/Dav/scr/gui/dav_commands.py`
> `Dav/scr/ComponentesDAV/Dav/scr/gui/freecad_wb.py`

El workbench que FreeCAD carga al arrancar. Registra los comandos de la barra
DAV y levanta el motor de voz.

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

    DAVWorkbench --|> Gui_Workbench : hereda
    DAVWorkbench ..> freecad_wb : setup_workbench
    freecad_wb ..> dav_commands : register_commands
    dav_commands ..> DAV_StartVoiceCommand : registra
    dav_commands ..> DAV_StopVoiceCommand : registra
    dav_commands ..> DAV_ShowPanelCommand : registra
    dav_commands ..> DAV_OpenPreferencesCommand : registra
    DAV_StartVoiceCommand ..> voice_bootstrap : start_voice_engine
    DAV_StopVoiceCommand ..> voice_bootstrap : stop_voice_engine
    DAV_ShowPanelCommand ..> voice_bootstrap : show_dock_panel
```

## El arranque

```mermaid
sequenceDiagram
    participant F as FreeCAD
    participant W as DAVWorkbench
    participant V as voice_bootstrap
    participant S as DavVoiceService

    F->>W: Initialize()
    W->>W: setup_workbench()
    W->>W: register_commands()
    Note over W: arranque diferido ~1,5 s<br/>para no bloquear la UI
    W->>V: start_voice_engine()
    V->>V: resuelve Dav/dic y el modelo
    V->>S: start_cad(adapter)
    S->>S: abre micrófono en hilo aparte
```

## Notas de diseño

- **Hay varios puntos que llaman `start_voice_engine`** (el comando de la barra,
  el workbench al activarse, `freecad_voice_setup`): el log muestra unas cuatro
  llamadas por arranque. No se pisan —están separadas en el tiempo y las frena
  `is_cad_engine_loaded()`— así que solo la primera abre micrófono. Por eso el
  arranque se loguea a nivel `debug`.
- Los mensajes `[DAV]` van a la pestaña **Informe** de FreeCAD, no a la consola
  Python. El log de verdad está en `config/dav.log`.
