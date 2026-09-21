# LaunchPreferences

> **Archivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/integration/launch_preferences.py`

Abre el **diálogo de Preferencias de DAV** dentro de FreeCAD (o suelto, en pruebas)
y, al cerrarse, aplica lo que cambió: el tema, el panel acoplado y la voz. Es el
callable que ejecuta el comando «preferencias» del diccionario raíz.

```mermaid
classDiagram
    class launch_preferences {
        <<módulo>>
        +open_preferences(parent) void
        -_hint_after_preferences() void
    }

    class PreferencesDialog {
        <<ui preferences_dialog>>
        +Signal settings_changed
        +exec()
    }

    class freecad_host {
        <<módulo>>
        +in_freecad() bool
        +get_freecad_main_window()
        +get_qt_application()
        +ensure_gui_on_path()
    }

    class apply_settings {
        <<módulo>>
        +apply_report_palette(theme) void
    }

    class DavDockSource {
        +SetTheme(theme) void
    }

    class DavVoiceService {
        +resume_cad_voice() void
    }

    launch_preferences ..> freecad_host : ¿dentro de FreeCAD?
    launch_preferences ..> PreferencesDialog : lo muestra modal
    launch_preferences ..> apply_settings : paleta del visor de reportes
    launch_preferences ..> DavDockSource : tema del panel
    launch_preferences ..> DavVoiceService : reanuda la voz
```

## Qué pasa al abrir

```mermaid
flowchart TD
    A[open_preferences] --> B[ensure_gui_on_path]
    B --> C{¿sin padre y<br/>dentro de FreeCAD?}
    C -->|sí| D[usa la ventana principal]
    C -->|no| E[sin padre]
    D --> F[PreferencesDialog.exec]
    E --> F
    F -->|settings_changed| G[aplica tema a la app,<br/>al panel y al visor]
    F -->|se cierra| H{¿dentro de<br/>FreeCAD?}
    H -->|sí| I[muestra el visor de reportes<br/>reanuda la voz CAD<br/>avisa en consola]
    H -->|no| J[fin]
```

## Notas de diseño

- **Es modal.** Al cerrarlo, dentro de FreeCAD, se llama a `DavVoiceService.resume_cad_voice()`
  para que la voz vuelva a controlar CAD.
- **Los cambios se aplican en vivo** (`settings_changed`), sin reiniciar FreeCAD.
- **Cada aplicación está en su `try`:** si el panel no existe o falla la paleta, el
  resto igual se aplica.
- Puede abrirse desde el hilo de voz con
  [`FreecadGuiBridge`](FreecadGuiBridge.md) (`request_open_preferences`).
- Ver también [`Preferences`](Preferences.md), que guarda y persiste la configuración.
