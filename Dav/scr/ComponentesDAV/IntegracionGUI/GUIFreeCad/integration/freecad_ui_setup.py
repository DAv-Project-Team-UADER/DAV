"""FreeCAD main window size and Report view (Informe) for DAV sessions."""

from __future__ import annotations

import os

_APPLIED = False

DEFAULT_MAIN_WIDTH = 1024
DEFAULT_MAIN_HEIGHT = 800


def _qt_widgets():
    try:
        from PySide6.QtWidgets import QApplication, QDockWidget, QMainWindow, QTabWidget
    except ImportError:
        from PySide2.QtWidgets import (  # type: ignore[no-redef]
            QApplication,
            QDockWidget,
            QMainWindow,
            QTabWidget,
        )
    return QApplication, QDockWidget, QMainWindow, QTabWidget


def _find_dock(main_window, dock_id: str):
    _, QDockWidget, _, _ = _qt_widgets()
    for dock in main_window.findChildren(QDockWidget):
        if dock.objectName() == dock_id:
            return dock
        action = dock.toggleViewAction()
        if action is None:
            continue
        data = action.data()
        if data == dock_id or str(data) == dock_id:
            return dock
    return None


def _select_tab_for_dock(dock) -> None:
    if dock is None:
        return
    _, _, _, QTabWidget = _qt_widgets()
    parent = dock.parentWidget()
    while parent is not None:
        if isinstance(parent, QTabWidget):
            index = parent.indexOf(dock)
            if index >= 0:
                parent.setCurrentIndex(index)
            return
        parent = parent.parentWidget()


def ensure_main_window_size(
    *,
    min_width: int = DEFAULT_MAIN_WIDTH,
    min_height: int = DEFAULT_MAIN_HEIGHT,
) -> None:
    try:
        import FreeCADGui as Gui
    except ImportError:
        return

    QApplication, _, QMainWindow, _ = _qt_widgets()
    main_window = Gui.getMainWindow()
    if main_window is None or not isinstance(main_window, QMainWindow):
        return

    if main_window.width() < min_width or main_window.height() < min_height:
        main_window.resize(
            max(main_window.width(), min_width),
            max(main_window.height(), min_height),
        )

    screen = main_window.screen() or QApplication.primaryScreen()
    if screen is not None:
        available = screen.availableGeometry()
        if main_window.width() > available.width() or main_window.height() > available.height():
            main_window.resize(
                min(main_window.width(), available.width()),
                min(main_window.height(), available.height()),
            )
        frame = main_window.frameGeometry()
        if not available.contains(frame):
            main_window.move(
                max(available.left(), min(frame.left(), available.right() - frame.width())),
                max(available.top(), min(frame.top(), available.bottom() - frame.height())),
            )


def show_report_view_instead_of_python(*, persist_prefs: bool = True) -> None:
    """Show Informe / Report view; hide Python console in the bottom panel."""
    try:
        import FreeCAD as App
        import FreeCADGui as Gui
    except ImportError:
        return

    if persist_prefs:
        pref = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows")
        pref.SetBool("Std_ReportView", True)
        pref.SetBool("Std_PythonView", False)

    main_window = Gui.getMainWindow()
    if main_window is None:
        return

    report = _find_dock(main_window, "Std_ReportView")
    python = _find_dock(main_window, "Std_PythonView")

    if python is not None:
        python.hide()

    if report is not None:
        report.show()
        report.raise_()
        _select_tab_for_dock(report)
        return

    try:
        Gui.runCommand("Std_ReportView", 0)
    except Exception:
        pass


def apply_dav_freecad_ui(*, force: bool = False) -> None:
    """Resize main window and prefer Report view when DAV starts FreeCAD."""
    global _APPLIED
    if _APPLIED and not force:
        return
    if os.environ.get("DAV_AUTOLOAD_WORKBENCH") != "1" and not force:
        return

    ensure_main_window_size()
    show_report_view_instead_of_python()
    _APPLIED = True
