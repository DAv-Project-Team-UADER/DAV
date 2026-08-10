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

"""Pure DAV panel widget: renders voice state, emits user intent."""

from __future__ import annotations

import os
from datetime import datetime

from PySide6.QtCore import QSize, Qt, QTimer, Signal
from PySide6.QtGui import QBrush, QColor, QFont, QIcon, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtSvgWidgets import QSvgWidget

from ContextView import ContextView
from FlashOverlay import FlashOverlay
from IconLocator import IconLocator
from Paletas import DARK, FONT_MONO, FONT_SANS, LIGHT
from Textos import TEXTS


class DavPanel(QWidget):
    """DAV panel: context buttons, recognised text, history and object tree.

    Deliberately knows nothing about FreeCAD, the ``Browser`` or the file
    bridge. It is fed through ``RenderContext`` / ``AddToHistory`` / ``SetStatus``
    and reports user intent through signals, so the same widget works as a
    standalone window today and as a ``QDockWidget`` inside FreeCAD after the
    migration (see ``Dav/docs/plan-unificacion-guis.md``).

    Signals:
        CommandRequested(str): the user picked an entry; carries the spoken
            phrase, exactly as if it had been said out loud.
        HelpRequested(): the help button was pressed.
        PreferencesRequested(): the preferences button was pressed.
        ThemeToggled(str): theme switched; carries ``"light"`` or ``"dark"``.
        DockToggleRequested(): the user asked to detach the panel from the
            FreeCAD window, or to dock it back in. Whoever owns the dock
            decides what that means and calls ``SetDockState`` back.

    Example::

        panel = DavPanel()
        panel.CommandRequested.connect(browser.ProcessPhrase)
        panel.RenderContext(view)
    """

    CommandRequested = Signal(str)
    HelpRequested = Signal()
    PreferencesRequested = Signal()
    ThemeToggled = Signal(str)
    DockToggleRequested = Signal()

    def __init__(
        self,
        Parent: QWidget | None = None,
        Theme: str = "light",
        Lang: str = "es",
        Locator: IconLocator | None = None,
    ) -> None:
        super().__init__(Parent)
        self._locator = Locator or IconLocator()
        self._context = ContextView()
        self._toolButtons: list[QPushButton] = []
        self._treeWidget: QTreeWidget | None = None

        self._theme = Theme
        self._palette = LIGHT if Theme == "light" else DARK
        self._lang = Lang
        self._texts = TEXTS.get(Lang, TEXTS["es"])

        self._BuildUi()
        self.RenderContext(self._context)

    # ================================================================
    # API publica: entrada de datos
    # ================================================================

    def RenderContext(self, Context: ContextView) -> None:
        """Redraw the button area for the given context.

        Args:
            Context: snapshot of the active voice context.
        """
        self._context = Context or ContextView()
        self._ClearToolArea()

        if self._context.IsEmpty():
            self._ShowEmptyHint()
            return

        for entry in self._context.Entries():
            button = self._MakeEntryButton(entry)
            self._toolButtons.append(button)
            self._toolAreaLayout.addWidget(button)

        if not self._context.IsRoot():
            self._toolAreaLayout.addWidget(self._MakeBackButton())

    def AddToHistory(self, Text: str, FromVoice: bool = True, Unknown: bool = False) -> None:
        """Append a line to the history panel, colour-coded by origin.

        Args:
            Text: line to append.
            FromVoice: True when it came from speech, False for clicks.
            Unknown: True to mark it as an error / unrecognised command.
        """
        if not Text:
            return

        palette = self._palette
        colour = palette["red"] if Unknown else (
            palette["green"] if FromVoice else palette["dark_text"]
        )

        cursor = self._historyList.textCursor()
        cursor.movePosition(QTextCursor.End)
        fmt = QTextCharFormat()
        fmt.setForeground(QBrush(QColor(colour)))
        cursor.insertText(f"[{datetime.now():%H:%M:%S}] {Text}\n", fmt)
        self._historyList.setTextCursor(cursor)
        self._historyList.ensureCursorVisible()

    def SetCurrentText(self, Text: str) -> None:
        """Show the phrase currently being recognised."""
        self._currentText.setText(Text)

    def SetStatus(self, Status: str, Detail: str = "") -> None:
        """Update the microphone status banner.

        Args:
            Status: ``"active"``, ``"inactive"`` or ``"error"``.
            Detail: optional text shown instead of the default label.
        """
        labels = {
            "active": self._texts["mic_active"],
            "inactive": self._texts["mic_inactive"],
            "error": self._texts["mic_error"],
        }
        self._statusLabel.setText(Detail or labels.get(Status, Status))

    def SetTree(self, Objects: list[dict], DocumentName: str | None = None) -> None:
        """Rebuild the object tree.

        Args:
            Objects: dicts with ``name``, ``label``, ``type``, ``visible`` and
                optional ``parent``. Same contract the JSON bridge used, so the
                caller can switch to reading FreeCAD directly without touching
                this widget.
            DocumentName: shown as root item; a placeholder when None.
        """
        tree = self._treeWidget
        if tree is None:
            return

        tree.clear()
        if not Objects:
            tree.addTopLevelItem(QTreeWidgetItem(["(sin documento abierto)"]))
            return

        root = QTreeWidgetItem([DocumentName or "Documento"])
        tree.addTopLevelItem(root)

        items: dict[str, QTreeWidgetItem] = {}
        for obj in Objects:
            label = obj.get("label") or obj.get("name") or "?"
            if not obj.get("visible", True):
                label = f"{label}  (oculto)"
            items[obj.get("name", label)] = QTreeWidgetItem([label])

        for obj in Objects:
            item = items.get(obj.get("name", ""))
            if item is None:
                continue
            parent = items.get(obj.get("parent") or "")
            (parent or root).addChild(item)

        tree.expandAll()

    def SetTheme(self, Theme: str) -> None:
        """Switch between the light and dark palettes."""
        self._theme = Theme
        self._palette = LIGHT if Theme == "light" else DARK
        self._ApplyStyles()
        self.RenderContext(self._context)

    def SetLanguage(self, Lang: str) -> None:
        """Switch the interface language."""
        self._lang = Lang
        self._texts = TEXTS.get(Lang, TEXTS["es"])
        self._listenLabel.setText(self._texts["section_listen"])
        self._histLabel.setText(self._texts["section_history"])
        self._modelLabel.setText(self._texts["section_model"])

    def SetDockState(self, Floating: bool) -> None:
        """Reflect whether the panel is detached, on the dock/undock button.

        Called by whoever owns the dock, both after the button is pressed and
        when the user drags the title bar, so the icon never lies about the
        current state.

        Args:
            Floating: True when the panel is a separate window.
        """
        button = getattr(self, "_dockButton", None)
        if button is None:
            return
        button.setText("⧈" if Floating else "⧉")
        button.setToolTip(
            "Volver a unir a la ventana de FreeCAD" if Floating
            else "Separar de la ventana de FreeCAD"
        )

    def Flash(self) -> None:
        """Blink the overlay to acknowledge a recognised command."""
        self._flash.setGeometry(self.rect())
        self._flash.raise_()
        self._flash.Trigger()

    # ================================================================
    # Construccion de la UI
    # ================================================================

    def _BuildUi(self) -> None:
        palette = self._palette
        texts = self._texts

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 12, 16, 12)

        layout.addLayout(self._BuildHeader())

        self._statusLabel = QLabel(texts.get("status_idle", "Micrófono inactivo"))
        self._statusLabel.setFont(QFont(FONT_SANS, 13, QFont.DemiBold))
        self._statusLabel.setAlignment(Qt.AlignCenter)
        self._statusLabel.setFixedHeight(46)
        self._statusLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self._statusLabel)

        self._listenLabel = QLabel(texts["section_listen"])
        self._listenLabel.setFont(QFont(FONT_SANS, 12, QFont.DemiBold))
        layout.addWidget(self._listenLabel)

        self._currentText = QTextEdit()
        self._currentText.setFixedHeight(48)
        self._currentText.setFont(QFont(FONT_MONO, 12, QFont.DemiBold))
        self._currentText.setReadOnly(True)
        layout.addWidget(self._currentText)

        panels = QHBoxLayout()
        panels.setSpacing(16)
        panels.addLayout(self._BuildTreeColumn(), stretch=1)
        panels.addLayout(self._BuildHistoryColumn(), stretch=2)
        layout.addLayout(panels, stretch=1)

        self._toolArea = QWidget()
        self._toolAreaLayout = QHBoxLayout(self._toolArea)
        self._toolAreaLayout.setSpacing(10)
        # Margen inferior mayor: sin el, los botones quedan pegados al borde
        # de la ventana. AlignCenter (no solo horizontal) los centra tambien
        # en vertical dentro de la franja.
        self._toolAreaLayout.setContentsMargins(10, 10, 10, 14)
        self._toolAreaLayout.setAlignment(Qt.AlignCenter)
        self._toolArea.setFixedHeight(self.BUTTON_SIZE + 24)
        layout.addWidget(self._toolArea)

        self._flash = FlashOverlay(self)
        self._flash.setGeometry(self.rect())

        self._ApplyStyles()

    def _BuildHeader(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(8)

        logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Logos", "color.svg")
        if os.path.exists(logo):
            widget = QSvgWidget(logo)
            widget.setFixedSize(34, 30)
            row.addWidget(widget)

        self._titleLabel = QLabel("DAV")
        self._titleLabel.setFont(QFont(FONT_SANS, 15, QFont.Bold))
        row.addWidget(self._titleLabel, stretch=1)

        self._dockButton = QPushButton("⧉")
        self._dockButton.setFixedSize(36, 32)
        self._dockButton.setToolTip("Separar de la ventana de FreeCAD")
        self._dockButton.clicked.connect(self.DockToggleRequested.emit)
        row.addWidget(self._dockButton)

        self._themeButton = QPushButton("◐")
        self._themeButton.setFixedSize(36, 32)
        self._themeButton.setToolTip("Cambiar tema")
        self._themeButton.clicked.connect(self._OnThemeToggled)
        row.addWidget(self._themeButton)

        self._prefsButton = QPushButton("⚙")
        self._prefsButton.setFixedSize(36, 32)
        self._prefsButton.setToolTip("Preferencias")
        self._prefsButton.clicked.connect(self.PreferencesRequested.emit)
        row.addWidget(self._prefsButton)

        self._helpButton = QPushButton("?")
        self._helpButton.setFixedSize(36, 32)
        self._helpButton.setToolTip("Información")
        self._helpButton.clicked.connect(self.HelpRequested.emit)
        row.addWidget(self._helpButton)

        return row

    def _BuildTreeColumn(self) -> QVBoxLayout:
        column = QVBoxLayout()
        column.setSpacing(4)

        self._modelLabel = QLabel(self._texts["section_model"])
        self._modelLabel.setFont(QFont(FONT_SANS, 12, QFont.DemiBold))
        column.addWidget(self._modelLabel)

        self._treeWidget = QTreeWidget()
        self._treeWidget.setHeaderHidden(True)
        self._treeWidget.setMinimumHeight(150)
        column.addWidget(self._treeWidget, stretch=1)

        self.SetTree([])
        return column

    def _BuildHistoryColumn(self) -> QVBoxLayout:
        column = QVBoxLayout()
        column.setSpacing(4)

        self._histLabel = QLabel(self._texts["section_history"])
        self._histLabel.setFont(QFont(FONT_SANS, 12, QFont.DemiBold))
        column.addWidget(self._histLabel)

        self._historyList = QTextEdit()
        self._historyList.setFont(QFont(FONT_MONO, 11, QFont.DemiBold))
        self._historyList.setReadOnly(True)
        self._historyList.setMinimumHeight(150)
        column.addWidget(self._historyList, stretch=1)

        return column

    # ================================================================
    # Botones del contexto
    # ================================================================

    def _ClearToolArea(self) -> None:
        self._toolButtons.clear()
        while self._toolAreaLayout.count():
            item = self._toolAreaLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _ShowEmptyHint(self) -> None:
        hint = QLabel(self._texts["empty_context"])
        hint.setAlignment(Qt.AlignCenter)
        self._toolAreaLayout.addWidget(hint)

    #: Lado del boton y del icono, en px. El icono se deja bastante mas chico
    #: que el boton para que quede aire parejo alrededor de todos.
    BUTTON_SIZE = 54
    ICON_SIZE = 30

    def _MakeEntryButton(self, Entry) -> QPushButton:
        button = QPushButton()
        button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        button.setToolTip(Entry.Spoken)
        button.setStyleSheet(self._ButtonQss())

        icon = self._locator.Find(Entry.InternalKey)
        if icon:
            # setIcon en vez de un QSvgWidget embebido: Qt escala el SVG a un
            # cuadrado exacto respetando su relacion de aspecto, con lo cual
            # todos los botones quedan con el mismo tamaño visual. Con el
            # widget embebido cada SVG se dibujaba segun su propio viewBox y
            # unos se veian mas grandes que otros.
            button.setIcon(QIcon(icon))
            button.setIconSize(QSize(self.ICON_SIZE, self.ICON_SIZE))
        else:
            button.setText(Entry.Spoken[:2].capitalize())

        spoken = Entry.Spoken
        button.clicked.connect(lambda _checked=False, s=spoken: self._OnEntryClicked(s))
        return button

    def _MakeBackButton(self) -> QPushButton:
        button = QPushButton("←")
        button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        button.setToolTip("Volver")
        button.setFont(QFont(FONT_SANS, 18, QFont.Bold))
        button.setStyleSheet(self._BackButtonQss())
        button.clicked.connect(lambda: self._OnEntryClicked(self.BACK_PHRASE))
        return button

    #: Frase que el Browser interpreta como "subir un nivel" (Dav/dic/NavCommands).
    BACK_PHRASE = "subir"

    def _OnEntryClicked(self, Spoken: str) -> None:
        self.Flash()
        self.CommandRequested.emit(Spoken)

    def _OnThemeToggled(self) -> None:
        self.SetTheme("dark" if self._theme == "light" else "light")
        self.ThemeToggled.emit(self._theme)

    # ================================================================
    # Estilos
    # ================================================================

    def _ApplyStyles(self) -> None:
        palette = self._palette
        self.setStyleSheet(f"QWidget {{ background-color: {palette['bg']}; }}")
        self._titleLabel.setStyleSheet(f"color: {palette['black']};")
        self._statusLabel.setStyleSheet(self._StatusQss())
        self._currentText.setStyleSheet(self._TextPanelQss(palette["dark_text"], 12))
        self._historyList.setStyleSheet(self._TextPanelQss(palette["green"], 11))

        for label in (self._listenLabel, self._histLabel, self._modelLabel):
            label.setStyleSheet(f"color: {palette['black']};")

        for button in (
            self._helpButton,
            self._prefsButton,
            self._themeButton,
            self._dockButton,
        ):
            button.setStyleSheet(self._ButtonQss())

        if self._treeWidget is not None:
            self._treeWidget.setStyleSheet(self._TreeQss())

    def _StatusQss(self) -> str:
        palette = self._palette
        return (
            f"QLabel {{ background-color: {palette['mic']};"
            f" border-top: 1.5px solid {palette['mic_border']};"
            f" border-bottom: 1.5px solid {palette['mic_border']};"
            f" padding: 8px; color: {palette['dark_text']};"
            f" font-family: {FONT_SANS}; font-size: 13px; font-weight: 700; }}"
        )

    def _TextPanelQss(self, Colour: str, Size: int) -> str:
        palette = self._palette
        return (
            f"QTextEdit {{ background-color: {palette['panel']}; color: {Colour};"
            f" border: 1.5px solid {palette['panel_border']}; border-radius: 0px;"
            f" padding: 10px; font-family: {FONT_MONO}; font-size: {Size}px;"
            f" font-weight: 600; }}"
        )

    def _TreeQss(self) -> str:
        palette = self._palette
        return (
            f"QTreeWidget {{ background-color: {palette['panel']};"
            f" color: {palette['dark_text']};"
            f" border: 1.5px solid {palette['panel_border']};"
            f" padding: 6px; font-family: {FONT_MONO}; font-size: 11px; }}"
            f"QTreeWidget::item {{ padding: 2px; }}"
        )

    def _ButtonQss(self) -> str:
        palette = self._palette
        return (
            f"QPushButton {{"
            f" background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f" stop:0 {palette['btn_top']}, stop:1 {palette['btn_bot']});"
            f" border: 1.5px solid {palette['btn_border']}; border-radius: 8px;"
            f" color: {palette['black']}; font-family: {FONT_SANS};"
            f" font-size: 10px; font-weight: bold; }}"
            f"QPushButton:hover {{ background: {palette['btn_hover']}; }}"
            f"QPushButton:pressed {{ background: {palette['btn_hover']}; }}"
        )

    def _BackButtonQss(self) -> str:
        palette = self._palette
        return (
            f"QPushButton {{"
            f" background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f" stop:0 {palette['highlight']}, stop:1 {palette['btn_bot']});"
            f" border: 1.5px solid {palette['btn_border']}; border-radius: 8px;"
            f" color: {palette['black']}; font-family: {FONT_SANS};"
            f" font-size: 18px; font-weight: bold; }}"
            f"QPushButton:hover {{ background: {palette['highlight']}; }}"
        )

    def resizeEvent(self, Event) -> None:  # noqa: N802 (API de Qt)
        super().resizeEvent(Event)
        self._flash.setGeometry(self.rect())
