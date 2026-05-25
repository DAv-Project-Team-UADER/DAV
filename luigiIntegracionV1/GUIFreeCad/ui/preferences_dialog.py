"""Preferences dialog — click and voice configuration (FreeCAD style)."""

from __future__ import annotations

import os

from PySide6.QtCore import QObject, Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from core.i18n import clear_cache, tr
from core.model_manager import (
    download_large_model,
    has_large_model,
    has_small_model,
    verify_small_models,
)
from core.network_utils import has_internet
from core.settings import settings
from speech.voice_commands import VoiceCommandListener
from ui.download_dialog import DownloadDialog
from ui.lang_icons import apply_lang_flag
from ui.model_prompt_dialog import UnavailableModelDialog, UpdateModelDialog


class _VoiceBridge(QObject):
    """Routes voice callbacks from the audio thread to the Qt main thread."""

    command_received = Signal(str)
    text_heard = Signal(str, bool)  # text, is_final
    status_changed = Signal(str)
    audio_activity = Signal()


class PreferencesDialog(QDialog):
    settings_changed = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._lang = settings.language
        self._pending_model_size = settings.model_size
        self._voice: VoiceCommandListener | None = None
        self._voice_bridge = _VoiceBridge()
        qc = Qt.ConnectionType.QueuedConnection
        self._voice_bridge.command_received.connect(self._on_voice_command, qc)
        self._voice_bridge.text_heard.connect(self._on_text_heard, qc)
        self._voice_bridge.status_changed.connect(self._on_voice_status, qc)
        self._voice_bridge.audio_activity.connect(self._on_audio_activity, qc)
        self._audio_pulse = 0
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._tick_audio_pulse)
        self._restart_voice_timer = QTimer(self)
        self._restart_voice_timer.setSingleShot(True)
        self._restart_voice_timer.timeout.connect(self._restart_voice)
        self._update_dialog: UpdateModelDialog | None = None
        self._unavailable_dialog: UnavailableModelDialog | None = None

        self.setMinimumSize(480, 420)
        self._build_ui()
        self._load_from_settings()
        self.retranslate()
        self._start_voice()
        QTimer.singleShot(800, self._refresh_voice_badge)

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)

        # --- Language ---
        self._lang_group_box = QGroupBox(self)
        lang_layout = QVBoxLayout(self._lang_group_box)
        self._lang_buttons = QButtonGroup(self)
        self._rb_en = QRadioButton(self)
        self._rb_es = QRadioButton(self)
        self._rb_pt = QRadioButton(self)
        self._flag_en = QLabel(self)
        self._flag_es = QLabel(self)
        self._flag_pt = QLabel(self)
        for i, (rb, flag) in enumerate(
            (
                (self._rb_en, self._flag_en),
                (self._rb_es, self._flag_es),
                (self._rb_pt, self._flag_pt),
            )
        ):
            self._lang_buttons.addButton(rb, i)
            lang_layout.addWidget(self._lang_option_row(rb, flag))
            rb.toggled.connect(self._on_language_changed)

        # --- Model ---
        self._model_group_box = QGroupBox(self)
        model_layout = QVBoxLayout(self._model_group_box)
        self._model_buttons = QButtonGroup(self)
        self._rb_small = QRadioButton(self)
        self._rb_large = QRadioButton(self)
        self._model_buttons.addButton(self._rb_small, 0)
        self._model_buttons.addButton(self._rb_large, 1)
        model_layout.addWidget(self._rb_small)
        model_layout.addWidget(self._rb_large)
        self._rb_small.toggled.connect(self._on_model_toggled)
        self._rb_large.toggled.connect(self._on_model_toggled)

        # --- Theme ---
        self._theme_group_box = QGroupBox(self)
        theme_layout = QVBoxLayout(self._theme_group_box)
        self._theme_buttons = QButtonGroup(self)
        self._rb_light = QRadioButton(self)
        self._rb_dark = QRadioButton(self)
        self._theme_buttons.addButton(self._rb_light, 0)
        self._theme_buttons.addButton(self._rb_dark, 1)
        theme_layout.addWidget(self._rb_light)
        theme_layout.addWidget(self._rb_dark)

        # --- Startup ---
        self._startup_group_box = QGroupBox(self)
        startup_layout = QVBoxLayout(self._startup_group_box)
        self._chk_startup = QCheckBox(self)
        startup_layout.addWidget(self._chk_startup)

        root.addWidget(self._lang_group_box)
        root.addWidget(self._model_group_box)
        root.addWidget(self._theme_group_box)
        root.addWidget(self._startup_group_box)

        # Voice status
        self._voice_status_badge = QLabel(self)
        self._voice_status_badge.setObjectName("voiceStatus")
        self._voice_label = QLabel(self)
        self._voice_label.setWordWrap(True)
        self._voice_heard = QLabel(self)
        self._voice_heard.setWordWrap(True)
        self._voice_heard.setStyleSheet("color: #555555; font-size: 8pt;")
        self._voice_hint = QLabel(self)
        self._voice_hint.setWordWrap(True)
        root.addWidget(self._voice_status_badge)
        root.addWidget(self._voice_label)
        root.addWidget(self._voice_heard)
        root.addWidget(self._voice_hint)

        self._btn_toggle_voice = QPushButton(self)
        self._btn_toggle_voice.clicked.connect(self._toggle_voice)
        root.addWidget(self._btn_toggle_voice)

        # Buttons
        self._buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Apply,
            self,
        )
        self._buttons.accepted.connect(self._on_accept)
        self._buttons.rejected.connect(self.reject)
        self._buttons.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(
            self._apply
        )
        root.addWidget(self._buttons)

    def _lang_option_row(self, radio: QRadioButton, flag: QLabel) -> QWidget:
        row = QWidget(self)
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 4, 0)
        layout.setSpacing(8)
        layout.addWidget(radio, stretch=1)
        layout.addWidget(
            flag,
            stretch=0,
            alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
        )
        return row

    def _load_from_settings(self) -> None:
        lang_map = {"en": self._rb_en, "es": self._rb_es, "pt": self._rb_pt}
        lang_map.get(settings.language, self._rb_es).setChecked(True)
        if settings.model_size == "large":
            self._rb_large.setChecked(True)
        else:
            self._rb_small.setChecked(True)
        if settings.theme == "dark":
            self._rb_dark.setChecked(True)
        else:
            self._rb_light.setChecked(True)
        self._chk_startup.setChecked(settings.startup_enabled)
        self._pending_model_size = settings.model_size

    def retranslate(self) -> None:
        self.setWindowTitle(tr("preferences_title", self._lang))
        self._lang_group_box.setTitle(tr("section_language", self._lang))
        self._rb_en.setText(tr("lang_en", self._lang))
        self._rb_es.setText(tr("lang_es", self._lang))
        self._rb_pt.setText(tr("lang_pt", self._lang))
        apply_lang_flag(self._flag_en, "en")
        apply_lang_flag(self._flag_es, "es")
        apply_lang_flag(self._flag_pt, "pt")
        self._model_group_box.setTitle(tr("section_model", self._lang))
        self._rb_small.setText(tr("model_small", self._lang))
        self._rb_large.setText(tr("model_large", self._lang))
        self._theme_group_box.setTitle(tr("section_theme", self._lang))
        self._rb_light.setText(tr("theme_light", self._lang))
        self._rb_dark.setText(tr("theme_dark", self._lang))
        self._startup_group_box.setTitle(tr("section_startup", self._lang))
        self._chk_startup.setText(
            tr("startup_on", self._lang) if self._chk_startup.isChecked()
            else tr("startup_off", self._lang)
        )
        self._voice_hint.setText(tr("voice_hint", self._lang))
        self._refresh_voice_badge()
        self._buttons.button(QDialogButtonBox.StandardButton.Ok).setText(
            tr("btn_ok", self._lang)
        )
        self._buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(
            tr("btn_cancel", self._lang)
        )
        self._buttons.button(QDialogButtonBox.StandardButton.Apply).setText(
            tr("btn_apply", self._lang)
        )

    def _current_language(self) -> str:
        if self._rb_en.isChecked():
            return "en"
        if self._rb_pt.isChecked():
            return "pt"
        return "es"

    def _on_language_changed(self) -> None:
        new_lang = self._current_language()
        if new_lang == self._lang:
            return
        self._lang = new_lang
        clear_cache()
        self.retranslate()
        self._restart_voice_timer.start(450)

    def _on_model_toggled(self, checked: bool) -> None:
        if not checked:
            return
        if self._rb_large.isChecked():
            self._handle_large_model_selection()
        else:
            self._pending_model_size = "small"

    def _handle_large_model_selection(self) -> None:
        lang = self._current_language()

        if not has_small_model(lang):
            QMessageBox.warning(
                self,
                tr("preferences_title", self._lang),
                tr("small_model_missing", self._lang, lang=lang),
            )
            self._rb_small.setChecked(True)
            return

        if has_large_model(lang):
            self._pending_model_size = "large"
            return

        if not has_internet():
            self._unavailable_dialog = UnavailableModelDialog(self._lang, self)
            self._unavailable_dialog.finished.connect(self._on_unavailable_closed)
            self._unavailable_dialog.open()
            return

        self._show_update_prompt(lang)

    def _on_unavailable_closed(self) -> None:
        self._rb_small.setChecked(True)
        self._pending_model_size = "small"
        self._unavailable_dialog = None

    def _show_update_prompt(self, lang: str) -> None:
        if self._update_dialog is not None:
            self._update_dialog.close()
        self._update_dialog = UpdateModelDialog(self._lang, self)
        self._update_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._update_dialog.confirmed.connect(lambda: self._on_update_prompt_yes(lang))
        self._update_dialog.rejected_voice.connect(self._on_update_prompt_no)
        self._update_dialog.finished.connect(
            lambda _code: setattr(self, "_update_dialog", None)
        )
        self._update_dialog.open()

    def _on_update_prompt_yes(self, lang: str) -> None:
        if self._update_dialog is not None:
            self._update_dialog.close()
            self._update_dialog = None
        self._download_large(lang)
        if has_large_model(lang):
            self._pending_model_size = "large"
        else:
            self._rb_small.setChecked(True)
            self._pending_model_size = "small"

    def _on_update_prompt_no(self) -> None:
        self._rb_small.setChecked(True)
        self._pending_model_size = "small"
        if self._update_dialog is not None:
            self._update_dialog.close()
            self._update_dialog = None

    def _download_large(self, lang: str) -> None:
        dlg = DownloadDialog(tr("downloading_model", self._lang), self)
        dlg.show()
        from PySide6.QtWidgets import QApplication

        QApplication.processEvents()

        try:
            download_large_model(
                lang,
                progress_callback=lambda cur, tot: (
                    dlg.set_progress(cur, tot),
                    QApplication.processEvents(),
                ),
            )
            self._pending_model_size = "large"
        except Exception as exc:
            QMessageBox.critical(
                self,
                tr("preferences_title", self._lang),
                str(exc),
            )
            self._rb_small.setChecked(True)
            self._pending_model_size = "small"
        finally:
            dlg.close()

    def _apply(self) -> None:
        settings.language = self._current_language()
        settings.model_size = self._pending_model_size
        settings.theme = "dark" if self._rb_dark.isChecked() else "light"
        settings.startup_enabled = self._chk_startup.isChecked()
        settings.save()
        self.settings_changed.emit()

    def _on_accept(self) -> None:
        self._apply()
        self.accept()

    # --- Voice ---

    def _start_voice(self) -> None:
        self._voice_heard.setText("")
        self._voice = VoiceCommandListener(
            language=self._current_language(),
            on_command=self._voice_bridge.command_received.emit,
            on_text=self._voice_bridge.text_heard.emit,
            on_status=self._voice_bridge.status_changed.emit,
            on_audio=self._voice_bridge.audio_activity.emit,
        )
        self._voice.start()
        self._btn_toggle_voice.setText("⏸ " + tr("voice_pause", self._lang))
        self._voice_label.setText(tr("voice_starting", self._lang))

    def _restart_voice(self) -> None:
        self._start_voice()

    def _toggle_voice(self) -> None:
        if self._voice and self._voice.is_running():
            self._voice.pause()
            self._btn_toggle_voice.setText("▶ " + tr("voice_resume", self._lang))
            self._refresh_voice_badge()
        elif self._voice:
            self._voice.resume()
            self._btn_toggle_voice.setText("⏸ " + tr("voice_pause", self._lang))
            self._refresh_voice_badge()
        else:
            self._start_voice()

    def _refresh_voice_badge(self) -> None:
        if self._voice and self._voice.is_running():
            self._voice_status_badge.setText("🟢 " + tr("voice_active", self._lang))
            self._voice_status_badge.setStyleSheet("color: #1a7f37; font-weight: bold;")
            self._voice_label.setText(tr("voice_listening", self._lang))
        elif self._voice and self._voice.is_starting():
            self._voice_status_badge.setText("🟡 " + tr("voice_starting", self._lang))
            self._voice_status_badge.setStyleSheet("color: #9a6700; font-weight: bold;")
        else:
            self._voice_status_badge.setText("🔴 " + tr("voice_paused", self._lang))
            self._voice_status_badge.setStyleSheet("color: #cf222e; font-weight: bold;")
            self._voice_label.setText(tr("voice_paused_hint", self._lang))

    def _on_voice_status(self, status: str) -> None:
        if status == "active":
            self._refresh_voice_badge()
            return
        if status == "paused":
            self._refresh_voice_badge()
            return
        if status.startswith("unknown:"):
            heard = status.split(":", 1)[1]
            self._voice_heard.setText(tr("voice_unknown", self._lang, text=heard))
            return
        if status == "error:no_model":
            self._voice_status_badge.setText("⚠️ " + tr("voice_error_model", self._lang))
            self._voice_label.setText(
                tr("small_model_missing", self._lang, lang=self._current_language())
            )
            return
        if status.startswith("error:mic"):
            self._voice_status_badge.setText("⚠️ " + tr("voice_error_mic", self._lang))
            self._voice_label.setText(status.replace("error:mic:", ""))
            return
        if status.startswith("error:import:"):
            detail = status.split("error:import:", 1)[1]
            self._voice_status_badge.setText("⚠️ " + tr("voice_error", self._lang))
            self._voice_label.setText(
                detail
                + "\n\npip en Python de FreeCAD:\n"
                + '& "' + os.environ.get("DAV_FREECAD_PYTHON", "FreeCAD\\bin\\python.exe") + '" -m pip install sounddevice vosk'
            )
            return
        if status.startswith("error:"):
            self._voice_status_badge.setText("⚠️ " + tr("voice_error", self._lang))
            self._voice_label.setText(status.split(":", 2)[-1] if ":" in status else status)

    def _on_text_heard(self, text: str, is_final: bool) -> None:
        prefix = tr("voice_heard_final", self._lang) if is_final else tr("voice_heard_partial", self._lang)
        self._voice_heard.setText(f"{prefix}: «{text}»")

    def _on_audio_activity(self) -> None:
        self._audio_pulse = 8
        if not self._pulse_timer.isActive():
            self._pulse_timer.start(120)

    def _tick_audio_pulse(self) -> None:
        if self._audio_pulse > 0:
            self._audio_pulse -= 1
            bars = "▁▂▃▄▅▆▇█"[8 - self._audio_pulse : 8]
            if self._voice and self._voice.is_running():
                self._voice_label.setText(tr("voice_hearing_audio", self._lang) + " " + bars)
        else:
            self._pulse_timer.stop()
            if self._voice and self._voice.is_running():
                self._voice_label.setText(tr("voice_listening", self._lang))

    def _block_lang_signals(self, block: bool) -> None:
        for rb in (self._rb_en, self._rb_es, self._rb_pt):
            rb.blockSignals(block)

    def _apply_language(self, code: str) -> None:
        lang_map = {"en": self._rb_en, "es": self._rb_es, "pt": self._rb_pt}
        rb = lang_map.get(code)
        if rb is None or rb.isChecked():
            return
        self._block_lang_signals(True)
        rb.setChecked(True)
        self._block_lang_signals(False)
        new_lang = self._current_language()
        if new_lang != self._lang:
            self._lang = new_lang
            clear_cache()
            self.retranslate()
            self._restart_voice_timer.start(450)

    def _on_voice_command(self, command: str) -> None:
        """Runs on the Qt main thread (via _VoiceBridge signal)."""
        if command in ("yes", "no", "ok"):
            if self._update_dialog is not None and self._update_dialog.isVisible():
                if command == "yes":
                    self._update_dialog.trigger_yes()
                elif command == "no":
                    self._update_dialog.trigger_no()
                else:
                    self._update_dialog.trigger_yes()
                return
            if self._unavailable_dialog is not None and self._unavailable_dialog.isVisible():
                if command in ("ok", "yes"):
                    self._unavailable_dialog.accept()
                elif command == "no":
                    self._unavailable_dialog.reject()
                return

        labels = {
            "lang_en": tr("lang_en", self._lang),
            "lang_es": tr("lang_es", self._lang),
            "lang_pt": tr("lang_pt", self._lang),
            "model_small": tr("model_small", self._lang),
            "model_large": tr("model_large", self._lang),
            "theme_light": tr("theme_light", self._lang),
            "theme_dark": tr("theme_dark", self._lang),
            "startup_on": tr("startup_on", self._lang),
            "startup_off": tr("startup_off", self._lang),
            "yes": tr("btn_yes", self._lang),
            "no": tr("btn_no", self._lang),
            "apply": tr("btn_apply", self._lang),
            "ok": tr("btn_ok", self._lang),
        }
        self._voice_label.setText(f"✓ {labels.get(command, command)}")

        if command == "lang_en":
            self._apply_language("en")
        elif command == "lang_es":
            self._apply_language("es")
        elif command == "lang_pt":
            self._apply_language("pt")
        elif command == "model_small":
            self._rb_small.setChecked(True)
        elif command == "model_large":
            self._rb_large.setChecked(True)
        elif command == "theme_light":
            self._rb_light.setChecked(True)
        elif command == "theme_dark":
            self._rb_dark.setChecked(True)
        elif command == "startup_on":
            self._chk_startup.setChecked(True)
            self._chk_startup.setText(tr("startup_on", self._lang))
        elif command == "startup_off":
            self._chk_startup.setChecked(False)
            self._chk_startup.setText(tr("startup_off", self._lang))
        elif command == "apply":
            self._apply()
        elif command == "ok":
            self._on_accept()

    def closeEvent(self, event) -> None:
        self._pulse_timer.stop()
        self._restart_voice_timer.stop()
        if self._voice:
            self._voice.stop(wait=True, timeout=3.0)
            self._voice = None
        self._voice_bridge.blockSignals(True)
        super().closeEvent(event)
