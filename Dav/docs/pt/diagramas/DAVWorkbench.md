# DAVWorkbench e comandos

> **Arquivos:**
> `Dav/scr/ComponentesDAV/Dav/InitGui.py`
> `Dav/scr/ComponentesDAV/Dav/scr/gui/dav_commands.py`
> `Dav/scr/ComponentesDAV/Dav/scr/gui/freecad_wb.py`

O workbench que o FreeCAD carrega ao iniciar. Registra os comandos da barra
DAV e sobe o motor de voz.

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

    DAVWorkbench --|> Gui_Workbench : herda
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

## A inicialização

```mermaid
sequenceDiagram
    participant F as FreeCAD
    participant W as DAVWorkbench
    participant V as voice_bootstrap
    participant S as DavVoiceService

    F->>W: Initialize()
    W->>W: setup_workbench()
    W->>W: register_commands()
    Note over W: início adiado ~1,5 s<br/>para não bloquear a UI
    W->>V: start_voice_engine()
    V->>V: resolve Dav/dic e o modelo
    V->>S: start_cad(adapter)
    S->>S: abre o microfone em thread separada
```

## Notas de design

- **Há vários pontos que chamam `start_voice_engine`** (o comando da barra,
  o workbench ao ser ativado, `freecad_voice_setup`): o log mostra umas quatro
  chamadas por inicialização. Elas não se atropelam —estão separadas no tempo e são barradas por
  `is_cad_engine_loaded()`— então só a primeira abre o microfone. Por isso a
  inicialização é registrada em nível `debug`.
- As mensagens `[DAV]` vão para a aba **Relatório** do FreeCAD, não para o console
  Python. O log de verdade está em `config/dav.log`.
