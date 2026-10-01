# DavPanel

> **File:** `Dav/scr/ComponentesDAV/InterfazDAV/DavPanel.py`

The DAV GUI: a widget that lives inside FreeCAD as a `QDockWidget`. It shows
the navigation context, the command history and the document's object
tree.

It replaced `MainWindow.py` (1011 lines, external process) in the migration
documented in [`gui-unification-plan.md`](../gui-unification-plan.md).

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

    DavPanel --|> QWidget : inherits
    FlashOverlay --|> QWidget : inherits
    DavPanel "1" *-- "1" ContextView : context column
    DavPanel "1" *-- "1" FlashOverlay : visual feedback
    DavPanel ..> IconLocator : resolves icons
    DavPanel ..> Paletas : light/dark themes
    DavPanel ..> Textos : UI texts
```

## How it is fed

The panel **does not import FreeCAD or the `Browser`**: it receives data and emits signals.
What connects it is `integration/dav_dock_panel.py`.

```mermaid
flowchart LR
    B[Browser] --> A[BrowserVoiceAdapter]
    A --> D[dav_dock_panel]
    D -->|PublishContext| P[DavPanel]
    D -->|PublishHistory| P
    D -->|PublishTree| P
```

That separation is deliberate: it makes it possible to test the widget without starting FreeCAD.

## Design notes

- **Everything that enters the panel has to come from the GUI thread.** Touching a Qt
  widget from the microphone thread is an access violation. `BrowserVoiceAdapter`
  checks with `_on_gui_thread()` before publishing.
- Hiding/showing is provided by the `QDockWidget` that contains it, not by the panel: this
  covers the MVP's "minimize" requirement.
- The object tree is built from `App.ActiveDocument` with a
  `DocumentObserver`, with no macro or polling.
