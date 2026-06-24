# Diagramas de Clases — Proyecto DAV

## Índice de Componentes
1. [Componente: Dav (Workbench FreeCAD)](#componente-dav)
2. [Componente: InterfazDAV (GUI de Asistente)](#componente-interfazdav)
3. [Componente: Keychain (Lector de Diccionarios)](#componente-keychain)
4. [Componente: IntegracionGUI (Puente FreeCAD)](#componente-integraciongui)
5. [Diagrama General — Relaciones entre Componentes](#diagrama-general)

---

## Componente: Dav
> **Ruta:** `ComponentesDAV/Dav/`  
> Workbench de FreeCAD que registra comandos de voz y lanza la interfaz.

```mermaid
classDiagram
    class DAVWorkbench {
        +String MenuText
        +String ToolTip
        +Initialize() void
        +GetClassName() String
    }

    class DAV_OpenPreferencesCommand {
        +GetResources() dict
        +Activated() void
        +IsActive() bool
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

    class freecad_wb {
        <<module>>
        +setup_workbench(workbench) void
        +setup_mod_path() String
        +apply_dav_toolbar(workbench) void
        +install_gui_integration() void
        -_schedule_autoload_workbench() void
        -_schedule_dav_ui_bootstrap() void
        -_schedule_toolbar_refresh() void
        -_schedule_report_view() void
        -_schedule_settings_watcher() void
        -_force_show_dav_toolbar() void
        -_auto_start_voice_if_needed() void
    }

    class dav_commands {
        <<module>>
        +register_commands() void
        -_dav_repo_root() Path
        -_guifreecad_root() Path
        -_ensure_gui_path() Path
        -_ensure_selection_path() Path
        -_ensure_validation_path() Path
        -_launch_interfaz_dav() void
        -_bring_interfaz_to_front() bool
        -_find_system_python() String
    }

    class Gui_Workbench {
        <<FreeCAD>>
    }

    DAVWorkbench --|> Gui_Workbench : hereda
    DAVWorkbench ..> freecad_wb : usa (setup_workbench)
    freecad_wb ..> dav_commands : usa (register_commands)
    freecad_wb ..> DAV_OpenPreferencesCommand : registra
    freecad_wb ..> DAV_StartVoiceCommand : registra
    freecad_wb ..> DAV_StopVoiceCommand : registra
    DAV_StartVoiceCommand ..> dav_commands : usa (_launch_interfaz_dav)
```

---

## Componente: InterfazDAV
> **Ruta:** `ComponentesDAV/InterfazDAV/`  
> Ventana principal del asistente de voz con reconocimiento Vosk.

```mermaid
classDiagram
    class MainWindow {
        -String _CurrentTheme
        -String _CurrentLang
        -String _Level
        -String _ActiveGroup
        -dict _GroupMeta
        -dict _VoiceMap
        -dict _Texts
        -dict _T
        -list _ToolButtons
        -list _TopBarButtons
        -HelpWindow _HelpWindow
        -VoiceWorker _VoiceWorker
        -Thread _VoiceThread
        -FlashOverlay _Flash
        -QTimer _RefreshTimer
        -QTimer _CaptureTimer
        -QTimer _settings_poll
        -QLabel _TreeImageLabel
        -float _LastImageMtime

        +__init__(color, lang) void
        +SetColor(Mode) void
        +SetLanguage(Lang) void
        +ProcessVoiceCommand(Command) void
        +UpdateStatus(Msg) void
        +UpdateCurrentText(Text) void
        +AddToHistory(Text, Unknown, FromVoice, System) void
        +GoBack() void
        +ToggleTheme() void
        +OpenHelpWindow() void
        +CloseHelpWindow() void
        +ScrollHistory(Up) void
        -_SetupUi() void
        -_LoadGroupMeta() void
        -_LoadVoiceMap() void
        -_ShowRootButtons() void
        -_ShowGroupButtons(GroupName) void
        -_RebuildButtons() void
        -_EnterGroup(GroupName) void
        -_ExecuteChildAction(GroupName, ActionKey) void
        -_MakeSvgButton(IconPath, Tooltip, Size) QPushButton
        -_StartVoiceRecognition() void
        -_AutoCapture() void
        -_RefreshTreeImage() void
        -_CheckMacroStatus() void
        -_OpenPreferences() void
        -_OnPreferencesChanged() void
        -_StartSettingsWatcher() void
        -_PollSettings() void
        -_TriggerFlash() void
        -_UpdateStyles() void
        -_FlashButton(Btn) void
    }

    class VoiceWorker {
        +Signal finished
        +Signal partial_result
        +Signal final_result
        +Signal status_signal
        -String model_path
        -bool running
        -Queue audio_queue

        +__init__(model_path) void
        +run() void
        +stop() void
        +audio_callback(indata, frames, time, status) void
    }

    class HelpWindow {
        +__init__(T, L, parent) void
    }

    class FlashOverlay {
        -float _Progress
        -int _Direction
        -QTimer _Timer

        +__init__(Parent) void
        +Trigger() void
        -_Step() void
        +paintEvent(Event) void
    }

    class Paletas {
        <<module>>
        +dict LIGHT
        +dict DARK
        +String FONT_SANS
        +String FONT_MONO
    }

    class Textos {
        <<module>>
        +dict TEXTS
        +dict MODEL_PARTS
        +dict MODEL_PARTS_ALIASES
    }

    class QMainWindow {
        <<PySide6>>
    }

    class QObject {
        <<PySide6>>
    }

    class QDialog {
        <<PySide6>>
    }

    class QWidget {
        <<PySide6>>
    }

    MainWindow --|> QMainWindow : hereda
    VoiceWorker --|> QObject : hereda
    HelpWindow --|> QDialog : hereda
    FlashOverlay --|> QWidget : hereda

    MainWindow "1" *-- "1" VoiceWorker : crea y posee
    MainWindow "1" *-- "1" FlashOverlay : crea y posee
    MainWindow "1" o-- "0..1" HelpWindow : abre bajo demanda
    MainWindow ..> Paletas : lee temas
    MainWindow ..> Textos : lee textos UI
```

---

## Componente: Keychain
> **Ruta:** `ComponentesDAV/Keychain/`  
> Parsea diccionarios `.py` sin ejecutarlos para extraer claves e iconos.

```mermaid
classDiagram
    class Keychain {
        +String FilePath
        -String _Content

        +__init__(FilePath) void
        +GetKeys() list
        +GetValues() list
        +GetIcons(base_dir) list
        +GetAllKeys() list
        -_extract_keys_from_literal(start_idx) list
        -_extract_values_from_literal(start_idx) list
        -_extract_keys_from_dict_call(start_idx) list
        -_extract_values_from_dict_call(start_idx) list
    }

    note for Keychain "Soporta dos formatos:\n{ 'key': value } (literal)\ndict(key=value) (constructor)"
```

---

## Componente: IntegracionGUI
> **Ruta:** `ComponentesDAV/IntegracionGUI/`  
> Puente entre el motor de voz y FreeCAD. Incluye operaciones especiales y preferencias.

```mermaid
classDiagram
    class EspecialOperations {
        <<module>>
        +Minimize(a, b) void
        +Maximize(a, b) void
        +Raise(a, b) void
        +Lower(a, b) void
        +RedoPrevious(a, b) void
        +UndoPrevious(a, b) void
        -_get_tree_view() QTreeView
    }

    class Settings {
        -dict _data
        +String language
        +String model_size
        +String theme
        +bool startup_enabled
        +bool auto_voice

        +__init__() void
        +load() void
        +save() void
    }

    class voice_bootstrap {
        <<module>>
        +start_voice_engine(debug) bool
        +stop_voice_engine() void
        +is_voice_running() bool
    }

    class apply_settings {
        <<module>>
        +apply_saved_settings() void
    }

    class launch_preferences {
        <<module>>
        +open_preferences() void
    }

    class DavVoiceService {
        <<singleton>>
        +get()$ DavVoiceService
        +start_cad(adapter) bool
        +stop_cad() void
        +is_cad_engine_loaded() bool
    }

    class freecad_gui_bridge {
        <<module>>
        +apply_dav_freecad_ui() void
    }

    voice_bootstrap ..> Settings : lee configuración
    voice_bootstrap ..> DavVoiceService : controla
    apply_settings ..> Settings : lee y aplica
    launch_preferences ..> Settings : lee/escribe
    EspecialOperations ..> FreeCADGui : llama runCommand
```

---
## Diagrama General
> Relaciones entre los 4 componentes principales del proyecto DAV.

```mermaid
classDiagram
    namespace Dav_Workbench {
        class DAVWorkbench
        class DAV_StartVoiceCommand
        class DAV_StopVoiceCommand
        class DAV_OpenPreferencesCommand
    }

    namespace InterfazDAV {
        class MainWindow
        class VoiceWorker
        class HelpWindow
        class FlashOverlay
    }

    namespace KeychainComp {
        class Keychain
    }

    namespace IntegracionGUI {
        class EspecialOperations
        class Settings
        class DavVoiceService
        class voice_bootstrap
    }

    DAV_StartVoiceCommand ..> MainWindow : lanza proceso
    DAV_StopVoiceCommand ..> voice_bootstrap : detiene motor
    DAV_OpenPreferencesCommand ..> Settings : abre preferencias
    DAV_StartVoiceCommand ..> voice_bootstrap : inicia motor

    MainWindow ..> Keychain : parsea diccionarios
    MainWindow ..> Settings : lee/escribe config
    MainWindow *-- VoiceWorker : crea y posee
    MainWindow *-- FlashOverlay : crea y posee
    MainWindow o-- HelpWindow : abre

    voice_bootstrap ..> DavVoiceService : usa singleton
    voice_bootstrap ..> EspecialOperations : registra comandos
```

