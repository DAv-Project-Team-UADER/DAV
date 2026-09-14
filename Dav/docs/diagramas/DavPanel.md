# DavPanel

> **Archivo:** `Dav/scr/ComponentesDAV/InterfazDAV/DavPanel.py`

La GUI de DAV: un widget que vive dentro de FreeCAD como `QDockWidget`. Muestra
el contexto de navegación, el historial de comandos y el árbol de objetos del
documento.

Reemplazó a `MainWindow.py` (1011 líneas, proceso externo) en la migración
documentada en [`plan-unificacion-guis.md`](../plan-unificacion-guis.md).

```mermaid
classDiagram
    class DavPanel {
        -String _theme
        -String _lang
        -ContextView _context_view
        -FlashOverlay _flash
        -QListWidget _history
        -QTreeWidget _tree
        -QLabel _current_text
        -QLabel _status

        +RenderContext(data) void
        +AddToHistory(text, unknown, from_voice, system) void
        +SetCurrentText(text) void
        +SetStatus(msg) void
        +SetTree(nodes) void
        +SetTheme(mode) void
        +SetLanguage(lang) void
        +SetDockState(floating) void
        +Flash() void
        +resizeEvent(event) void
        -_BuildHistoryColumn() QWidget
        -_BuildContextColumn() QWidget
        -_BuildTreeColumn() QWidget
    }

    class ContextView {
        +Render(entries) void
    }

    class FlashOverlay {
        -float _Progress
        -QTimer _Timer
        +Trigger() void
        +paintEvent(event) void
    }

    class IconLocator {
        <<module>>
        +find_icon(name) Path
    }

    class QWidget {
        <<PySide6>>
    }

    DavPanel --|> QWidget : hereda
    FlashOverlay --|> QWidget : hereda
    DavPanel "1" *-- "1" ContextView : columna de contexto
    DavPanel "1" *-- "1" FlashOverlay : feedback visual
    DavPanel ..> IconLocator : resuelve iconos
    DavPanel ..> Paletas : temas claro/oscuro
    DavPanel ..> Textos : textos de la UI
```

## Cómo se alimenta

El panel **no importa FreeCAD ni el `Browser`**: recibe datos y emite señales.
Quien lo conecta es `integration/dav_dock_panel.py`.

```mermaid
flowchart LR
    B[Browser] --> A[BrowserVoiceAdapter]
    A --> D[dav_dock_panel]
    D -->|PublishContext| P[DavPanel]
    D -->|PublishHistory| P
    D -->|PublishTree| P
```

Esa separación es a propósito: permite testear el widget sin levantar FreeCAD.

## Notas de diseño

- **Todo lo que entra al panel tiene que venir del hilo de la GUI.** Tocar un
  widget Qt desde el hilo del micrófono es access violation. `BrowserVoiceAdapter`
  verifica con `_on_gui_thread()` antes de publicar.
- El ocultar/mostrar lo da el `QDockWidget` que lo contiene, no el panel: eso
  cubre el requisito de «minimizarse» del MVP.
- El árbol de objetos se arma desde `App.ActiveDocument` con un
  `DocumentObserver`, sin macro ni polling.
