# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

"""Mounts the DAV panel as a dock inside FreeCAD, wired to the live Browser."""

from __future__ import annotations

import sys
from pathlib import Path

_DOCK_OBJECT_NAME = "DAV_Panel"
_dock = None
_source = None


def _ensure_interfaz_on_path() -> None:
    """Make ``InterfazDAV`` importable (it lives outside GUIFreeCad)."""
    here = Path(__file__).resolve()
    for ancestor in here.parents:
        candidate = ancestor / "InterfazDAV"
        if candidate.is_dir() and (candidate / "DavPanel.py").is_file():
            text = str(candidate)
            if text not in sys.path:
                sys.path.insert(0, text)
            return


class BrowserPanelSource:
    """Feeds a ``DavPanel`` from the in-process ``Browser``.

    Drop-in replacement for ``FileBridgeSource``: same role, no files, no
    polling. The panel pushes phrases in through ``SendCommand`` and the
    adapter pushes state back out through ``PublishContext`` — everything in
    the FreeCAD process, so a click is as immediate as a method call.

    Args:
        Browser_: the live ``Browser`` instance.
        Adapter: the ``BrowserVoiceAdapter`` driving it, so clicks go through
            the same path as speech (token extraction, history, main thread).
    """

    def __init__(self, Browser_, Adapter) -> None:
        self._browser = Browser_
        self._adapter = Adapter
        self._panel = None

    def Attach(self, Panel) -> None:
        """Bind to a panel and draw the current context immediately."""
        self._panel = Panel
        Panel.CommandRequested.connect(self.SendCommand)
        self.PublishContext()

    def SendCommand(self, Spoken: str) -> None:
        """Process a phrase picked in the UI as if it had been spoken."""
        self._adapter.procesar_frase_final(Spoken)

    def PublishHistory(self, Line: str, Unknown: bool = False) -> None:
        """Show a line in the panel history."""
        if self._panel is not None:
            self._panel.AddToHistory(Line, FromVoice=True, Unknown=Unknown)

    def PublishRecognized(self, Phrase: str) -> None:
        """Show the phrase currently recognised."""
        if self._panel is not None:
            self._panel.SetCurrentText(Phrase)

    def PublishStatus(self, Status: str, Detail: str = "") -> None:
        """Update the microphone status banner."""
        if self._panel is not None:
            self._panel.SetStatus(Status, Detail)

    def PublishContext(self) -> None:
        """Rebuild the panel buttons from the Browser's active context."""
        if self._panel is None:
            return

        from ContextView import ContextEntryView, ContextView

        submenus, commands, seen = [], [], []
        for entry in self._browser.Context:
            if any(self._browser.IsSameTarget(entry.Target, t) for t in seen):
                continue
            seen.append(entry.Target)
            view = ContextEntryView(entry.Spoken, entry.InternalKey, entry.IsSubContext())
            (submenus if entry.IsSubContext() else commands).append(view)

        self._panel.RenderContext(
            ContextView(self._browser.ContextPath, submenus, commands)
        )

    def PublishTree(self) -> None:
        """Refresh the object tree straight from the active document.

        Reads FreeCAD in-process, with no macro and no ``tree_data.json``.
        Full removal of that bridge is migration stage 3.
        """
        if self._panel is None:
            return
        try:
            import FreeCAD as App
        except ImportError:
            return

        doc = App.ActiveDocument
        if doc is None:
            self._panel.SetTree([])
            return

        objects = []
        for obj in doc.Objects:
            parents = getattr(obj, "InList", None) or []
            objects.append({
                "name": obj.Name,
                "label": getattr(obj, "Label", obj.Name),
                "type": obj.TypeId,
                "visible": bool(getattr(getattr(obj, "ViewObject", None), "Visibility", True)),
                "parent": parents[0].Name if parents else None,
            })
        self._panel.SetTree(objects, doc.Name)


def install_dock_panel(browser, adapter):
    """Create the DAV dock inside FreeCAD and wire it to the Browser.

    Idempotent: calling it again reuses the existing dock and just re-points
    it at the given browser.

    Args:
        browser: live ``Browser`` instance.
        adapter: ``BrowserVoiceAdapter`` driving it.

    Returns:
        The ``BrowserPanelSource`` bound to the panel, or None outside FreeCAD.
    """
    global _dock, _source

    try:
        import FreeCADGui as Gui
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import QDockWidget
    except ImportError:
        return None

    main_window = Gui.getMainWindow()
    if main_window is None:
        return None

    _ensure_interfaz_on_path()
    from DavPanel import DavPanel

    source = BrowserPanelSource(browser, adapter)

    existing = main_window.findChild(QDockWidget, _DOCK_OBJECT_NAME)
    if existing is not None:
        panel = existing.widget()
        _dock, _source = existing, source
        source.Attach(panel)
        source.PublishTree()
        existing.show()
        existing.raise_()
        return source

    panel = DavPanel(Theme=_detect_theme())
    dock = QDockWidget("DAV", main_window)
    dock.setObjectName(_DOCK_OBJECT_NAME)
    dock.setWidget(panel)
    # Se permite anclar en los cuatro bordes: si solo se habilitan dos, al
    # soltar la ventana flotante sobre un borde no permitido Qt no la re-ancla
    # y queda suelta sin forma de volver a unirla.
    dock.setAllowedAreas(Qt.AllDockWidgetAreas)
    # Movable + Floatable es lo que habilita el ciclo completo separar/volver
    # a unir (arrastrando la barra de titulo o con doble click sobre ella).
    dock.setFeatures(
        QDockWidget.DockWidgetMovable
        | QDockWidget.DockWidgetFloatable
        | QDockWidget.DockWidgetClosable
    )
    main_window.addDockWidget(Qt.RightDockWidgetArea, dock)

    source.Attach(panel)
    source.PublishTree()
    _wire_dock_toggle(dock, panel)

    _dock, _source = dock, source
    return source


def _wire_dock_toggle(dock, panel) -> None:
    """Conecta el boton separar/unir del panel con el estado del dock.

    Arrastrar la barra de titulo ya separa y vuelve a unir, pero es poco
    descubrible: el boton hace explicita la accion y refleja el estado actual.
    """
    def _toggle() -> None:
        floating = dock.isFloating()
        dock.setFloating(not floating)
        if floating:
            # Al re-anclar, Qt recuerda el area previa; si no hay, va a la derecha.
            dock.show()
            dock.raise_()
        _refresh()

    def _refresh(*_args) -> None:
        panel.SetDockState(dock.isFloating())

    if hasattr(panel, "DockToggleRequested"):
        panel.DockToggleRequested.connect(_toggle)
    dock.topLevelChanged.connect(_refresh)
    _refresh()


def get_source():
    """The source bound to the live dock, or None when it is not mounted."""
    return _source


def remove_dock_panel() -> None:
    """Remove the dock from FreeCAD, if present."""
    global _dock, _source
    if _dock is not None:
        _dock.setParent(None)
        _dock.deleteLater()
    _dock = _source = None


def _detect_theme() -> str:
    """Guess FreeCAD's theme from its window palette luminance."""
    try:
        import FreeCADGui as Gui

        palette = Gui.getMainWindow().palette()
        colour = palette.color(palette.ColorRole.Window)
        luminance = (
            0.299 * colour.red() + 0.587 * colour.green() + 0.114 * colour.blue()
        ) / 255.0
        return "dark" if luminance < 0.5 else "light"
    except Exception:
        return "light"
