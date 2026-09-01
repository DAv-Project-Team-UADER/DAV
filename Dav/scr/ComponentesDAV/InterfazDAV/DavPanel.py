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
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
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
    DockToggleRequested = Signal()

    #: Lado del boton y del icono, en px. El icono se deja bastante mas chico
    #: que el boton para que quede aire parejo alrededor de todos.
    BUTTON_SIZE = 54
    ICON_SIZE = 42

    #: Filas visibles antes de que la grilla empiece a scrollear.
    TOOL_AREA_MAX_ROWS = 3

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
        self._treeItems: dict[str, QTreeWidgetItem] = {}
        self._lastColumns = 0

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

        buttons = [self._MakeEntryButton(e) for e in self._context.Entries()]
        self._toolButtons.extend(buttons)
        if not self._context.IsRoot():
            buttons.append(self._MakeBackButton())

        # Se llena por columnas, no por filas: con scroll horizontal la altura
        # es la dimension fija (TOOL_AREA_MAX_ROWS) y el ancho es el que crece.
        rows = self._RowCount(len(buttons))
        self._lastColumns = rows
        for index, button in enumerate(buttons):
            self._toolAreaLayout.addWidget(button, index % rows, index // rows)

        # Volver al principio: viniendo de un contexto largo, el nuevo
        # aparecia desplazado.
        self._toolScroll.horizontalScrollBar().setValue(0)

    def _RowCount(self, Total: int) -> int:
        """Cuantas filas usar para repartir ``Total`` botones.

        Nunca mas de TOOL_AREA_MAX_ROWS, y con pocos botones se usan menos
        filas para no dejar una sola columna alta al costado.
        """
        if Total <= 0:
            return 1
        columns_that_fit = max(1, self._VisibleColumns())
        needed = -(-Total // columns_that_fit)  # ceil
        return max(1, min(self.TOOL_AREA_MAX_ROWS, needed))

    def _VisibleColumns(self) -> int:
        """Columnas que entran sin scroll, segun el ancho actual."""
        cell = self.BUTTON_SIZE + self._toolAreaLayout.spacing()
        available = max(self._toolScroll.viewport().width() - 24, cell)
        return max(1, available // cell)

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
        self._treeItems = {}
        if not Objects:
            tree.addTopLevelItem(QTreeWidgetItem(["(sin documento abierto)"]))
            return

        root = QTreeWidgetItem([DocumentName or "Documento"])
        tree.addTopLevelItem(root)

        items: dict[str, QTreeWidgetItem] = {}
        self._treeItems = items
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

    def HighlightSelection(self, Names: list[str]) -> None:
        """Mirror FreeCAD's current selection in the panel tree.

        Called by the selection observer so that objects picked by voice
        (``ObjectSelection.SelectNext``) light up here too, not only in
        FreeCAD's own tree. Names that are not in the tree are ignored.

        Args:
            Names: FreeCAD object ``Name`` values that are currently selected.
        """
        tree = self._treeWidget
        if tree is None:
            return

        Wanted = set(Names or [])
        Current = None
        # blockSignals: setSelected dispara itemSelectionChanged, y si el panel
        # llegara a reenviar eso a FreeCAD se realimentaria en bucle.
        tree.blockSignals(True)
        try:
            for name, item in self._treeItems.items():
                Selected = name in Wanted
                item.setSelected(Selected)
                if Selected and Current is None:
                    Current = item
        finally:
            tree.blockSignals(False)

        if Current is not None:
            tree.scrollToItem(Current)

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
        self._statusLabel.setFont(QFont(FONT_SANS, 13, QFont.Bold))
        self._statusLabel.setAlignment(Qt.AlignCenter)
        self._statusLabel.setFixedHeight(46)
        self._statusLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self._statusLabel)

        self._listenLabel = QLabel(texts["section_listen"])
        self._listenLabel.setFont(QFont(FONT_SANS, 12, QFont.Bold))
        layout.addWidget(self._listenLabel)

        self._currentText = QTextEdit()
        self._currentText.setFixedHeight(48)
        self._currentText.setFont(QFont(FONT_MONO, 12, QFont.Bold))
        self._currentText.setReadOnly(True)
        layout.addWidget(self._currentText)

        panels = QHBoxLayout()
        panels.setSpacing(16)
        panels.addLayout(self._BuildTreeColumn(), stretch=1)
        panels.addLayout(self._BuildHistoryColumn(), stretch=2)
        layout.addLayout(panels, stretch=1)

        # Grilla, no fila: hay contextos de 47 entradas (Part) contra 5 de la
        # raiz. En una sola fila el ancho pedido crecia con la cantidad y
        # estiraba la ventana. La grilla envuelve y el scroll acota la altura,
        # asi el panel mide siempre lo mismo entre en el contexto que entre.
        self._toolArea = QWidget()
        self._toolAreaLayout = QGridLayout(self._toolArea)
        self._toolAreaLayout.setSpacing(10)
        self._toolAreaLayout.setContentsMargins(10, 10, 10, 10)
        self._toolAreaLayout.setAlignment(Qt.AlignCenter)

        self._toolScroll = QScrollArea()
        self._toolScroll.setWidget(self._toolArea)
        self._toolScroll.setWidgetResizable(True)
        self._toolScroll.setFrameShape(QFrame.NoFrame)
        # Scroll horizontal: los botones se mantienen en filas de altura fija
        # y, si no entran a lo ancho, se corren en vez de empujar el borde de
        # la ventana. Asi el panel conserva el alto en cualquier contexto.
        self._toolScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._toolScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._toolScroll.setFixedHeight(
            self.TOOL_AREA_MAX_ROWS * (self.BUTTON_SIZE + 10) + 26
        )
        layout.addWidget(self._toolScroll)

        self._flash = FlashOverlay(self)
        self._flash.setGeometry(self.rect())

        self._ApplyStyles()

    def _BuildHeader(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(8)

        logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Logos", "color.svg")
        if os.path.exists(logo):
            widget = QSvgWidget(logo)
            widget.setFixedSize(40, 36)
            widget.setStyleSheet("background-color: transparent;")
            row.addWidget(widget)

        self._titleLabel = QLabel("DAV")
        self._titleLabel.setFont(QFont(FONT_SANS, 28, QFont.Bold))
        row.addWidget(self._titleLabel, stretch=1)

        self._dockButton = QPushButton("⧉")
        self._dockButton.setFixedSize(48, 44)
        self._dockButton.setFont(QFont(FONT_SANS, 28, QFont.Bold))
        self._dockButton.setToolTip("Separar de la ventana de FreeCAD")
        self._dockButton.clicked.connect(self.DockToggleRequested.emit)
        row.addWidget(self._dockButton)

        self._prefsButton = QPushButton("⚙")
        self._prefsButton.setFixedSize(48, 44)
        self._prefsButton.setFont(QFont(FONT_SANS, 28, QFont.Bold))
        self._prefsButton.setToolTip("Preferencias")
        self._prefsButton.clicked.connect(self.PreferencesRequested.emit)
        row.addWidget(self._prefsButton)

        self._helpButton = QPushButton("?")
        self._helpButton.setFixedSize(48, 44)
        self._helpButton.setFont(QFont(FONT_SANS, 28, QFont.Bold))
        self._helpButton.setToolTip("Información")
        self._helpButton.clicked.connect(self.HelpRequested.emit)
        row.addWidget(self._helpButton)

        return row

    def _BuildTreeColumn(self) -> QVBoxLayout:
        column = QVBoxLayout()
        column.setSpacing(4)

        self._modelLabel = QLabel(self._texts["section_model"])
        self._modelLabel.setFont(QFont(FONT_SANS, 12, QFont.Bold))
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
        self._histLabel.setFont(QFont(FONT_SANS, 12, QFont.Bold))
        column.addWidget(self._histLabel)

        self._historyList = QTextEdit()
        self._historyList.setFont(QFont(FONT_MONO, 11, QFont.Bold))
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

    # ================================================================
    # Estilos
    # ================================================================

    def _ApplyStyles(self) -> None:
        palette = self._palette
        self.setObjectName("DavPanel")
        self.setStyleSheet(
            f"QWidget#DavPanel {{ background-color: {palette['bg']} !important; }}"
            f"QWidget#DavPanel > * {{ background-color: transparent !important; }}"
            f"QScrollArea {{ background-color: transparent !important; border: none; }}"
            f"QScrollArea > QWidget {{ background-color: transparent !important; }}"
            f"QLabel {{ background-color: transparent !important; }}"
        )
        self._titleLabel.setStyleSheet(
            f"color: {palette['black']}; background-color: transparent !important;"
            f" font-size: 28pt; font-weight: bold;"
        )
        self._statusLabel.setStyleSheet(self._StatusQss())
        self._currentText.setStyleSheet(self._TextPanelQss(palette["dark_text"], 12))
        self._historyList.setStyleSheet(self._TextPanelQss(palette["green"], 11))

        for label in (self._listenLabel, self._histLabel, self._modelLabel):
            label.setStyleSheet(
                f"color: {palette['black']}; background-color: transparent !important;"
                f" font-size: 12pt; font-weight: bold;"
            )

        for button in (
            self._helpButton,
            self._prefsButton,
            self._dockButton,
        ):
            button.setStyleSheet(self._ButtonQss())

        if self._treeWidget is not None:
            self._treeWidget.setStyleSheet(self._TreeQss())

    def _StatusQss(self) -> str:
        palette = self._palette
        return (
            f"QLabel {{ background-color: transparent !important;"
            f" border-top: 1.5px solid {palette['mic_border']};"
            f" border-bottom: 1.5px solid {palette['mic_border']};"
            f" padding: 8px; color: {palette['dark_text']};"
            f" font-family: {FONT_SANS}; font-size: 13px; font-weight: 700; }}"
        )

    def _TextPanelQss(self, Colour: str, Size: int) -> str:
        palette = self._palette
        return (
            f"QTextEdit {{ background-color: {palette['panel']} !important; color: {Colour};"
            f" border: 1.5px solid {palette['panel_border']}; border-radius: 0px;"
            f" padding: 10px; font-family: {FONT_MONO}; font-size: {Size}px;"
            f" font-weight: 600; }}"
        )

    def _TreeQss(self) -> str:
        palette = self._palette
        return (
            f"QTreeWidget {{ background-color: {palette['panel']} !important;"
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
            f" stop:0 {palette['btn_top']}, stop:1 {palette['btn_bot']}) !important;"
            f" border: 1.5px solid {palette['btn_border']}; border-radius: 8px;"
            f" color: {palette['black']}; font-family: {FONT_SANS};"
            f" font-size: 10px; font-weight: bold; }}"
            f"QPushButton:hover {{ background: {palette['btn_hover']} !important; }}"
            f"QPushButton:pressed {{ background: {palette['btn_hover']} !important; }}"
        )

    def _BackButtonQss(self) -> str:
        palette = self._palette
        return (
            f"QPushButton {{"
            f" background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f" stop:0 {palette['highlight']}, stop:1 {palette['btn_bot']}) !important;"
            f" border: 1.5px solid {palette['btn_border']}; border-radius: 8px;"
            f" color: {palette['black']}; font-family: {FONT_SANS};"
            f" font-size: 18px; font-weight: bold; }}"
            f"QPushButton:hover {{ background: {palette['highlight']} !important; }}"
        )

    def resizeEvent(self, Event) -> None:  # noqa: N802 (API de Qt)
        super().resizeEvent(Event)
        self._flash.setGeometry(self.rect())
        # Al cambiar el ancho cambia cuantos botones entran por fila. Se
        # redibuja solo si el numero de columnas cambio, para no rehacer la
        # grilla en cada pixel del arrastre.
        if not self._context.IsEmpty():
            total = len(self._toolButtons) + (0 if self._context.IsRoot() else 1)
            if self._RowCount(total) != self._lastColumns:
                self.RenderContext(self._context)
