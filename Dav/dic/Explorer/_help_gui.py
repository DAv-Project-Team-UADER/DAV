# Copyright (C) 2026 The DAV Project Team
# SPDX-License-Identifier: GPL-3.0-or-later

def show_help_dialog(title: str, content: str):
    """Muestra la ayuda en consola y abre una ventana emergente en la interfaz si está disponible."""
    header = f"=== Ayuda: {title} ==="
    print(header)
    print(content)
    
    try:
        try:
            from PySide6.QtWidgets import QMessageBox
        except ImportError:
            try:
                from PySide2.QtWidgets import QMessageBox
            except ImportError:
                try:
                    from PySide.QtGui import QMessageBox
                except ImportError:
                    QMessageBox = None

        if QMessageBox:
            try:
                import FreeCADGui as Gui
                parent = Gui.getMainWindow() if hasattr(Gui, "getMainWindow") else None
            except Exception:
                parent = None
                
            box = QMessageBox(parent)
            box.setWindowTitle(f"DAV - Ayuda: {title}")
            box.setText(f"<b>Sección activa: {title}</b>")
            box.setInformativeText(content)
            box.setIcon(QMessageBox.Icon.Information)
            box.exec()
    except Exception:
        pass
