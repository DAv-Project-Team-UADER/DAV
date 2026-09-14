# Copyright (C) 2026 The DAV Project Team
# SPDX-License-Identifier: GPL-3.0-or-later

_active_help_box = None

def show_help_dialog(title: str, content: str):
    """Muestra la ayuda en consola y abre una ventana emergente en la interfaz si está disponible."""
    header = f"=== Ayuda: {title} ==="
    print(header)
    print(content)
    
    QtWidgets = None
    QtCore = None
    for mod_name in ("PySide", "PySide6", "PySide2"):
        try:
            mod = __import__(mod_name, fromlist=["QtWidgets", "QtCore", "QtGui"])
            QtWidgets = getattr(mod, "QtWidgets", None) or getattr(mod, "QtGui", None)
            QtCore = getattr(mod, "QtCore", None)
            if QtWidgets and hasattr(QtWidgets, "QMessageBox"):
                break
        except Exception:
            pass

    if QtWidgets and hasattr(QtWidgets, "QMessageBox"):
        def _open_box():
            global _active_help_box
            try:
                import FreeCADGui as Gui
                parent = Gui.getMainWindow() if hasattr(Gui, "getMainWindow") else None
                box = QtWidgets.QMessageBox(parent)
                box.setWindowTitle(f"DAV - Ayuda: {title}")
                box.setText(f"<h3>{title}</h3>")
                box.setInformativeText(content)
                icon_info = getattr(QtWidgets.QMessageBox, "Information", None) or getattr(QtWidgets.QMessageBox.Icon, "Information", None)
                if icon_info is not None:
                    box.setIcon(icon_info)
                btn_ok = getattr(QtWidgets.QMessageBox, "Ok", None) or getattr(QtWidgets.QMessageBox.StandardButton, "Ok", None)
                if btn_ok is not None:
                    box.setStandardButtons(btn_ok)
                box.show()
                box.raise_()
                box.activateWindow()
                _active_help_box = box
            except Exception as e:
                print(f"[DAV] Error mostrando ventana de ayuda: {e}")

        try:
            if QtCore and hasattr(QtCore, "QTimer"):
                QtCore.QTimer.singleShot(0, _open_box)
            else:
                _open_box()
        except Exception:
            _open_box()

