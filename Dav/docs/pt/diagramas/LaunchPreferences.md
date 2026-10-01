# LaunchPreferences

> **Arquivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/integration/launch_preferences.py`

Abre o **diálogo de Preferências do DAV** dentro do FreeCAD (ou avulso, em testes)
e, ao fechá-lo, aplica o que mudou: o tema, o painel acoplado e a voz. É o
callable que executa o comando «preferencias» do dicionário raiz.

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

    launch_preferences ..> freecad_host : dentro do FreeCAD?
    launch_preferences ..> PreferencesDialog : exibe como modal
    launch_preferences ..> apply_settings : paleta do visualizador de relatórios
    launch_preferences ..> DavDockSource : tema do painel
    launch_preferences ..> DavVoiceService : retoma a voz
```

## O que acontece ao abrir

```mermaid
flowchart TD
    A[open_preferences] --> B[ensure_gui_on_path]
    B --> C{sem pai e<br/>dentro do FreeCAD?}
    C -->|sim| D[usa a janela principal]
    C -->|não| E[sem pai]
    D --> F[PreferencesDialog.exec]
    E --> F
    F -->|settings_changed| G[aplica o tema ao app,<br/>ao painel e ao visualizador]
    F -->|fecha| H{dentro do<br/>FreeCAD?}
    H -->|sim| I[exibe o visualizador de relatórios<br/>retoma a voz CAD<br/>avisa no console]
    H -->|não| J[fim]
```

## Notas de design

- **É modal.** Ao fechá-lo, dentro do FreeCAD, chama-se `DavVoiceService.resume_cad_voice()`
  para que a voz volte a controlar o CAD.
- **As mudanças são aplicadas ao vivo** (`settings_changed`), sem reiniciar o FreeCAD.
- **Cada aplicação tem seu próprio `try`:** se o painel não existe ou a paleta falha, o
  restante ainda é aplicado.
- Pode ser aberto a partir da thread de voz com
  [`FreecadGuiBridge`](FreecadGuiBridge.md) (`request_open_preferences`).
- Veja também [`Preferences`](Preferences.md), que salva e persiste a configuração.
