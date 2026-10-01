# LaunchPreferences

> **File:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/integration/launch_preferences.py`

Opens the **DAV Preferences dialog** inside FreeCAD (or standalone, in tests)
and, when it closes, applies what changed: the theme, the docked panel and the
voice. It is the callable run by the "preferencias" (preferences) command of the root dictionary.

```mermaid
classDiagram
    class launch_preferences {
        <<module>>
        +open_preferences(parent) void
        -_hint_after_preferences() void
    }

    class PreferencesDialog {
        <<ui preferences_dialog>>
        +Signal settings_changed
        +exec()
    }

    class freecad_host {
        <<module>>
        +in_freecad() bool
        +get_freecad_main_window()
        +get_qt_application()
        +ensure_gui_on_path()
    }

    class apply_settings {
        <<module>>
        +apply_report_palette(theme) void
    }

    class DavDockSource {
        +SetTheme(theme) void
    }

    class DavVoiceService {
        +resume_cad_voice() void
    }

    launch_preferences ..> freecad_host : inside FreeCAD?
    launch_preferences ..> PreferencesDialog : shows it modally
    launch_preferences ..> apply_settings : report viewer palette
    launch_preferences ..> DavDockSource : panel theme
    launch_preferences ..> DavVoiceService : resumes the voice
```

## What happens on open

```mermaid
flowchart TD
    A[open_preferences] --> B[ensure_gui_on_path]
    B --> C{no parent and<br/>inside FreeCAD?}
    C -->|yes| D[uses the main window]
    C -->|no| E[no parent]
    D --> F[PreferencesDialog.exec]
    E --> F
    F -->|settings_changed| G[applies theme to the app,<br/>the panel and the viewer]
    F -->|closes| H{inside<br/>FreeCAD?}
    H -->|yes| I[shows the report viewer<br/>resumes the CAD voice<br/>notifies in the console]
    H -->|no| J[end]
```

## Design notes

- **It is modal.** When it is closed inside FreeCAD, `DavVoiceService.resume_cad_voice()`
  is called so the voice goes back to controlling CAD.
- **Changes are applied live** (`settings_changed`), without restarting FreeCAD.
- **Each application is in its own `try`:** if the panel does not exist or the palette
  fails, the rest is still applied.
- It can be opened from the voice thread with
  [`FreecadGuiBridge`](FreecadGuiBridge.md) (`request_open_preferences`).
- See also [`Preferences`](Preferences.md), which stores and persists the settings.
