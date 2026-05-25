"""Main application window."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.i18n import tr
from core.model_manager import has_small_model, verify_small_models
from core.settings import settings
from ui.preferences_dialog import PreferencesDialog


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._lang = settings.language
        self._build_ui()
        self._check_models_on_startup()
        self.retranslate()

    def _build_ui(self) -> None:
        central = QWidget(self)
        layout = QVBoxLayout(central)

        header = QHBoxLayout()
        header.addStretch()
        self._btn_prefs = QPushButton(self)
        self._btn_prefs.setFixedSize(40, 40)
        self._btn_prefs.setToolTip(tr("menu_preferences", self._lang))
        self._btn_prefs.clicked.connect(self._open_preferences)
        header.addWidget(self._btn_prefs)
        layout.addLayout(header)

        self._welcome = QLabel(self)
        self._welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._welcome.setWordWrap(True)
        layout.addWidget(self._welcome)
        layout.addStretch()
        self.setCentralWidget(central)

        menubar = self.menuBar()
        self._menu_file = menubar.addMenu("")
        self._act_prefs = QAction(self)
        self._act_prefs.triggered.connect(self._open_preferences)
        self._menu_file.addAction(self._act_prefs)
        self._act_exit = QAction(self)
        self._act_exit.triggered.connect(self.close)
        self._menu_file.addAction(self._act_exit)

        self.statusBar().showMessage(tr("status_ready", self._lang))

    def retranslate(self) -> None:
        self._lang = settings.language
        self.setWindowTitle(tr("app_title", self._lang))
        self._menu_file.setTitle("Archivo" if self._lang == "es" else "Arquivo" if self._lang == "pt" else "File")
        self._act_prefs.setText(tr("menu_preferences", self._lang))
        self._btn_prefs.setText("\u2699")
        self._btn_prefs.setToolTip(tr("menu_preferences", self._lang))
        self._act_exit.setText(tr("menu_exit", self._lang))
        self._welcome.setText(tr("main_welcome", self._lang))
        size_key = (
            "status_model_large"
            if settings.model_size == "large"
            else "status_model_small"
        )
        self.statusBar().showMessage(tr(size_key, self._lang))

    def _check_models_on_startup(self) -> None:
        status = verify_small_models()
        missing = [lang for lang, ok in status.items() if not ok]
        if missing and not has_small_model(settings.language):
            QMessageBox.information(
                self,
                tr("app_title", self._lang),
                tr("small_model_missing", self._lang, lang=settings.language)
                + "\n\npython scripts/setup_models.py",
            )

    def _open_preferences(self) -> None:
        dlg = PreferencesDialog(self)
        dlg.settings_changed.connect(self._on_settings_changed)
        dlg.exec()

    def _on_settings_changed(self) -> None:
        from PySide6.QtWidgets import QApplication

        from ui.theme import apply_theme

        apply_theme(QApplication.instance(), settings.theme)
        self.retranslate()
