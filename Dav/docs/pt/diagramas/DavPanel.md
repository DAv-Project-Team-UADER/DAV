# DavPanel

> **Arquivo:** `Dav/scr/ComponentesDAV/InterfazDAV/DavPanel.py`

A GUI do DAV: um widget que vive dentro do FreeCAD como `QDockWidget`. Mostra
o contexto de navegação, o histórico de comandos e a árvore de objetos do
documento.

Substituiu `MainWindow.py` (1011 linhas, processo externo) na migração
documentada em [`plano-unificacao-guis.md`](../plano-unificacao-guis.md).

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

    DavPanel --|> QWidget : herda
    FlashOverlay --|> QWidget : herda
    DavPanel "1" *-- "1" ContextView : coluna de contexto
    DavPanel "1" *-- "1" FlashOverlay : feedback visual
    DavPanel ..> IconLocator : resolve ícones
    DavPanel ..> Paletas : temas claro/escuro
    DavPanel ..> Textos : textos da UI
```

## Como é alimentado

O painel **não importa o FreeCAD nem o `Browser`**: recebe dados e emite sinais.
Quem o conecta é `integration/dav_dock_panel.py`.

```mermaid
flowchart LR
    B[Browser] --> A[BrowserVoiceAdapter]
    A --> D[dav_dock_panel]
    D -->|PublishContext| P[DavPanel]
    D -->|PublishHistory| P
    D -->|PublishTree| P
```

Essa separação é proposital: permite testar o widget sem subir o FreeCAD.

## Notas de design

- **Tudo o que entra no painel tem que vir da thread da GUI.** Mexer em um
  widget Qt a partir da thread do microfone é access violation. `BrowserVoiceAdapter`
  verifica com `_on_gui_thread()` antes de publicar.
- Ocultar/mostrar é dado pelo `QDockWidget` que o contém, não pelo painel: isso
  cobre o requisito de «minimizar» do MVP.
- A árvore de objetos é montada a partir de `App.ActiveDocument` com um
  `DocumentObserver`, sem macro nem polling.
