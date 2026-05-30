#  Copyright (C) 2026 The DAV Project Team-                                 |#  Copyright (C) 2026 El Equipo del Proyecto DAV
#  Universidad Autónoma de Entre Ríos (UADER)                               |#  Universidad Autónoma de Entre Ríos (UADER)
#  Directed by Gerard Guillermo and Gallo Fabricio David                    |#  Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#                                                                           |#
#  This program is free software: you can redistribute it and/or modify     |#  Este programa es software libre: usted puede redistribuirlo y/o modificarlo
#  it under the terms of the GNU General Public License as published by     |#  bajo los términos de la Licencia Pública General GNU tal como fue publicada 
#  the Free Software Foundation, in GLPv3 version  of the License           |#  por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#                                                                           |#
#  This program is distributed in the hope that it will be useful,          |#  Este programa se distribuye con la esperanza de que sea útil,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           |#  pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            |#  MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
#  GNU General Public License for more details.                             |#  Licencia Pública General GNU para más detalles.
#                                                                           |#
#  You should have received a copy of the GNU General Public License        |#  Deberías haber recibido una copia de la Licencia Pública General GNU
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.   |#  junto con este programa. Si no es así, consulte <https://www.gnu.org/licenses/>.

import os
import threading
import unicodedata
from datetime import datetime
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QTextCursor, QTextCharFormat, QBrush
from PySide6.QtSvgWidgets import QSvgWidget

from Paletas import LIGHT, DARK, FONT_SANS, FONT_MONO
from Textos import TEXTS, MODEL_PARTS, MODEL_PARTS_ALIASES
from HelpWindow import HelpWindow
from VoiceWorker import VoiceWorker
from FlashOverlay import FlashOverlay
from Keychain import Keychain

# ================================================================
# HELPERS
# ================================================================

def _StripAccents(Text):
    return ''.join(
        C for C in unicodedata.normalize('NFD', Text)
        if unicodedata.category(C) != 'Mn'
    )

def _NormCmd(Text):
    return _StripAccents(Text.lower().strip())

# ================================================================
# BUTTON LEVEL — controls which set of buttons is currently shown
# ================================================================

LEVEL_ROOT  = "root"
LEVEL_GROUP = "group"


# ================================================================
# MAIN WINDOW
# ================================================================

class MainWindow(QMainWindow):

    def __init__(self, color: str = "light", lang: str = "es"):
        super().__init__()
        self.setWindowTitle("Asistente de Voz - Control por Comandos")
        self.setMinimumSize(900, 650)

        self._HelpWindow   = None
        self._Level        = LEVEL_ROOT
        self._ActiveGroup  = None

        self._ToolButtons  = []
        self._GroupMeta    = {}

        self.SetColor(color)
        self.SetLanguage(lang)
        self._SetupUi()
        self._StartVoiceRecognition()

    def SetColor(self, Mode: str):
        self._T = LIGHT if Mode == "light" else DARK
        self._CurrentTheme = Mode
        if hasattr(self, '_TitleLabel'):
            self.setStyleSheet(f"QMainWindow {{ background-color: {self._T['bg']}; }}")
            self._UpdateStyles()

    def SetLanguage(self, Lang: str):
        self._Texts       = TEXTS.get(Lang, TEXTS["es"])
        self._CurrentLang = Lang
        if hasattr(self, '_ToolRow'):
            self._RebuildButtons()

    def _MicQss(self, Color: str) -> str:
        T = self._T
        return (
            f"QLabel {{ background-color: {T['mic']};"
            f" border-top: 1.5px solid {T['mic_border']};"
            f" border-bottom: 1.5px solid {T['mic_border']};"
            f" border-left: none; border-right: none;"
            f" padding: 8px; color: {Color};"
            f" font-family: {FONT_SANS}; font-size: 13px; font-weight: 700; }}"
        )

    def _PanelQss(self, Font: str, Color: str, Size: int, Weight: int = 500) -> str:
        T = self._T
        return (
            f"QTextEdit {{ background-color: {T['panel']}; color: {Color};"
            f" border: 1.5px solid {T['panel_border']}; border-radius: 0px;"
            f" padding: 12px; font-family: {Font}; font-size: {Size}px;"
            f" font-weight: {Weight}; }}"
        )

    def _BtnQss(self) -> str:
        T = self._T
        return (
            f"QPushButton {{"
            f" background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f" stop:0 {T['btn_top']}, stop:1 {T['btn_bot']});"
            f" border: 1.5px solid {T['btn_border']}; border-radius: 8px;"
            f" color: {T['black']}; font-family: {FONT_SANS};"
            f" font-size: 10px; font-weight: bold; }}"
            f"QPushButton:hover {{"
            f" background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f" stop:0 {T['btn_bot']}, stop:1 {T['btn_hover']});"
            f" border: 1.5px solid {T['btn_border']}; }}"
            f"QPushButton:pressed {{ background: {T['btn_hover']}; }}"
        )

    def _BackBtnQss(self) -> str:
        T = self._T
        return (
            f"QPushButton {{"
            f" background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f" stop:0 {T['highlight']}, stop:1 {T['btn_bot']});"
            f" border: 1.5px solid {T['btn_border']}; border-radius: 8px;"
            f" color: {T['black']}; font-family: {FONT_SANS};"
            f" font-size: 18px; font-weight: bold; }}"
            f"QPushButton:hover {{"
            f" background: {T['highlight']};"
            f" border: 1.5px solid {T['btn_border']}; }}"
            f"QPushButton:pressed {{ background: {T['btn_hover']}; }}"
        )

    def _ThemeBtnQss(self) -> str:
        T = self._T
        return (
            f"QPushButton {{"
            f" background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f" stop:0 {T['btn_top']}, stop:1 {T['btn_bot']});"
            f" border: 1.5px solid {T['btn_border']}; border-radius: 8px;"
            f" color: {T['black']}; font-family: {FONT_SANS}; font-size: 14px; font-weight: bold; }}"
            f"QPushButton:hover {{"
            f" background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f" stop:0 {T['btn_bot']}, stop:1 {T['btn_hover']});"
            f" border: 1.5px solid {T['btn_border']}; }}"
            f"QPushButton:pressed {{ background: {T['btn_hover']}; }}"
        )

    def _FlashButton(self, Btn: QPushButton):
        OriginalStyle = Btn.styleSheet()
        FlashColor = "#3A7BFF" if self._CurrentTheme == "light" else "#5B8CDE"
        Btn.setStyleSheet(
            f"QPushButton {{ background-color: {FlashColor};"
            f" border: 2px solid {FlashColor}; border-radius: 8px; }}"
        )
        QTimer.singleShot(300, lambda: Btn.setStyleSheet(OriginalStyle))

    def _SetupUi(self):
        T = self._T
        L = self._Texts
        self.setStyleSheet(f"QMainWindow {{ background-color: {T['bg']}; }}")

        CentralWidget = QWidget()
        self.setCentralWidget(CentralWidget)
        MainLayout = QVBoxLayout(CentralWidget)
        MainLayout.setSpacing(0)
        MainLayout.setContentsMargins(0, 0, 0, 0)

        TopWidget = QWidget()
        TopLayout = QVBoxLayout(TopWidget)
        TopLayout.setSpacing(12)
        TopLayout.setContentsMargins(40, 20, 40, 12)

        BaseDir        = os.path.dirname(os.path.abspath(__file__))
        LogoPath       = os.path.join(BaseDir, "..", "Logos", "color.svg")
        SystemIconsDir = os.path.join(BaseDir, "icons", "system")

        TitleRow = QHBoxLayout()
        TitleRow.setSpacing(10)
        if os.path.exists(LogoPath):
            Logo = QSvgWidget(LogoPath)
            Logo.setFixedSize(40, 36)
            TitleRow.addWidget(Logo)

        self._TitleLabel = QLabel("DAV")
        self._TitleLabel.setFont(QFont(FONT_SANS, 16, QFont.Bold))
        self._TitleLabel.setStyleSheet(f"color: {T['black']};")
        TitleRow.addWidget(self._TitleLabel, stretch=1)

        self._ThemeButton = QPushButton("🌙")
        self._ThemeButton.setFont(QFont(FONT_SANS, 14, QFont.Bold))
        self._ThemeButton.setFixedSize(40, 36)
        self._ThemeButton.setToolTip("Cambiar a modo oscuro")
        self._ThemeButton.setStyleSheet(self._ThemeBtnQss())
        self._ThemeButton.clicked.connect(self.ToggleTheme)
        TitleRow.addWidget(self._ThemeButton)

        self._HelpButton = QPushButton()
        self._HelpButton.setFixedSize(40, 36)
        self._HelpButton.setToolTip("Información")
        self._HelpButton.setStyleSheet(self._BtnQss())
        self._HelpButton.clicked.connect(self.OpenHelpWindow)
        HelpIconPath = os.path.join(SystemIconsDir, "info.svg")
        if os.path.exists(HelpIconPath):
            HelpSvg = QSvgWidget(HelpIconPath)
            HelpSvg.setFixedSize(18, 18)
            InnerLayout = QVBoxLayout(self._HelpButton)
            InnerLayout.addWidget(HelpSvg, alignment=Qt.AlignCenter)
            InnerLayout.setContentsMargins(6, 6, 6, 6)
        else:
            self._HelpButton.setText("?")

        self._TopBarButtons = []
        ExtraIcons = [
            ("nuevo documento.svg",  "Nuevo documento"),
            ("abrir documento.svg",  "Abrir documento"),
            ("guardar como.svg",     "Guardar como"),
            ("imprimir.svg",         "Imprimir"),
            ("configuraciones.svg",  "Configuraciones"),
        ]
        for IconFile, Tooltip in ExtraIcons:
            Btn = QPushButton()
            Btn.setFixedSize(40, 36)
            Btn.setToolTip(Tooltip)
            Btn.setStyleSheet(self._BtnQss())
            IconPath = os.path.join(SystemIconsDir, IconFile)
            if os.path.exists(IconPath):
                Svg = QSvgWidget(IconPath)
                Svg.setFixedSize(18, 18)
                IL = QVBoxLayout(Btn)
                IL.addWidget(Svg, alignment=Qt.AlignCenter)
                IL.setContentsMargins(6, 6, 6, 6)
            else:
                Btn.setText("?")
            TitleRow.addWidget(Btn)
            self._TopBarButtons.append(Btn)

        TitleRow.addWidget(self._HelpButton)
        TopLayout.addLayout(TitleRow)
        MainLayout.addWidget(TopWidget)

        self._StatusLabel = QLabel("Esperando micrófono…")
        self._StatusLabel.setFont(QFont(FONT_SANS, 13, QFont.DemiBold))
        self._StatusLabel.setAlignment(Qt.AlignCenter)
        self._StatusLabel.setFixedHeight(54)
        self._StatusLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._StatusLabel.setStyleSheet(self._MicQss(T["dark_text"]))
        MainLayout.addWidget(self._StatusLabel)

        BottomWidget = QWidget()
        BottomLayout = QVBoxLayout(BottomWidget)
        BottomLayout.setSpacing(12)
        BottomLayout.setContentsMargins(40, 20, 40, 20)

        self._ListenLabel = QLabel(L["section_listen"])
        self._ListenLabel.setFont(QFont(FONT_SANS, 12, QFont.DemiBold))
        self._ListenLabel.setStyleSheet(f"color: {T['black']};")
        BottomLayout.addWidget(self._ListenLabel)

        self._CurrentText = QTextEdit()
        self._CurrentText.setFixedHeight(54)
        self._CurrentText.setFont(QFont(FONT_MONO, 12, QFont.DemiBold))
        self._CurrentText.setReadOnly(True)
        self._CurrentText.setStyleSheet(self._PanelQss(FONT_MONO, T["dark_text"], 12, Weight=600))
        BottomLayout.addWidget(self._CurrentText)

        PanelRow = QHBoxLayout()
        PanelRow.setSpacing(40)

        ModelCol = QVBoxLayout()
        ModelCol.setSpacing(4)
        self._ModelLabel = QLabel(L["section_model"])
        self._ModelLabel.setFont(QFont(FONT_SANS, 12, QFont.DemiBold))
        self._ModelLabel.setStyleSheet(f"color: {T['black']};")
        ModelCol.addWidget(self._ModelLabel)
        self._ModelPanel = QTextEdit()
        self._ModelPanel.setReadOnly(True)
        self._ModelPanel.setStyleSheet(self._PanelQss(FONT_SANS, T["black"], 10, Weight=500))
        self._ModelPanel.setMinimumHeight(160)
        ModelCol.addWidget(self._ModelPanel, stretch=1)
        PanelRow.addLayout(ModelCol, stretch=1)

        HistCol = QVBoxLayout()
        HistCol.setSpacing(4)
        self._HistLabel = QLabel(L["section_history"])
        self._HistLabel.setFont(QFont(FONT_SANS, 12, QFont.DemiBold))
        self._HistLabel.setStyleSheet(f"color: {T['black']};")
        HistCol.addWidget(self._HistLabel)
        self._HistoryList = QTextEdit()
        self._HistoryList.setFont(QFont(FONT_MONO, 11, QFont.DemiBold))
        self._HistoryList.setReadOnly(True)
        self._HistoryList.setStyleSheet(self._PanelQss(FONT_MONO, T["green"], 11, Weight=600))
        self._HistoryList.setMinimumHeight(160)
        HistCol.addWidget(self._HistoryList, stretch=1)
        PanelRow.addLayout(HistCol, stretch=2)

        BottomLayout.addLayout(PanelRow, stretch=1)

        self._ToolArea = QWidget()
        self._ToolAreaLayout = QHBoxLayout(self._ToolArea)
        self._ToolAreaLayout.setSpacing(25)
        self._ToolAreaLayout.setContentsMargins(40, 12, 40, 12)
        self._ToolAreaLayout.setAlignment(Qt.AlignHCenter)
        BottomLayout.addWidget(self._ToolArea)

        MainLayout.addWidget(BottomWidget)

        self._Flash = FlashOverlay(CentralWidget)
        self._Flash.setGeometry(CentralWidget.rect())

        self._LoadGroupMeta()
        self._PopulateModel()
        self._ShowRootButtons()

    def _LoadGroupMeta(self):
        self._GroupMeta = {}
        BaseDir = os.path.dirname(os.path.abspath(__file__))
        DicDir  = os.path.join(BaseDir, "DiccionarioPrueba")

        if not os.path.isdir(DicDir):
            return

        ExplorerPath = os.path.join(DicDir, "explorer.py")
        if not os.path.exists(ExplorerPath):
            return

        RootKeychain = Keychain(ExplorerPath)
        GroupNames   = [K for K in RootKeychain.GetKeys() if K != "doc"]

        for GroupName in GroupNames:
            GroupIconPath = os.path.join(DicDir, f"{GroupName}.svg")
            if not os.path.exists(GroupIconPath):
                continue  

            GroupFolder  = os.path.join(DicDir, GroupName)
            GroupDictPath = os.path.join(GroupFolder, f"{GroupName}.py")
            if not os.path.exists(GroupDictPath):
                GroupDictPath = os.path.join(GroupFolder, f"{GroupName}_cmds.py")

            Children = []
            if os.path.exists(GroupDictPath):
                ActionKeychain = Keychain(GroupDictPath)
                for ActionKey in ActionKeychain.GetKeys()[:12]:
                    ChildIcon = os.path.join(GroupFolder, f"{ActionKey.replace(' ', '_')}.svg")
                    if not os.path.exists(ChildIcon):
                        continue  # child without icon → not shown
                    Children.append({"key": ActionKey, "icon": ChildIcon})

            self._GroupMeta[GroupName] = {
                "icon":     GroupIconPath,
                "children": Children,
            }

    def _ClearToolArea(self):
        while self._ToolAreaLayout.count():
            Item = self._ToolAreaLayout.takeAt(0)
            Widget = Item.widget()
            if Widget:
                Widget.setParent(None)
                Widget.deleteLater()
        self._ToolButtons = []

    def _MakeSvgButton(self, IconPath: str, Tooltip: str, Size: int = 54) -> QPushButton:
        Btn = QPushButton()
        Btn.setFixedSize(Size, Size)
        Btn.setToolTip(Tooltip)
        Btn.setStyleSheet(self._BtnQss())
        Svg = QSvgWidget(IconPath)
        Svg.setFixedSize(Size - 12, Size - 12)
        Layout = QVBoxLayout(Btn)
        Layout.addWidget(Svg, alignment=Qt.AlignCenter)
        Layout.setContentsMargins(6, 6, 6, 6)
        return Btn

    def _ShowRootButtons(self):
        self._ClearToolArea()
        self._Level       = LEVEL_ROOT
        self._ActiveGroup = None

        for GroupName, Meta in self._GroupMeta.items():
            Btn = self._MakeSvgButton(Meta["icon"], GroupName)
            Btn.clicked.connect(lambda Checked=False, G=GroupName: self._EnterGroup(G))
            self._ToolButtons.append(Btn)
            self._ToolAreaLayout.addWidget(Btn)

    def _ShowGroupButtons(self, GroupName: str):
        self._ClearToolArea()
        self._Level       = LEVEL_GROUP
        self._ActiveGroup = GroupName

        Meta = self._GroupMeta.get(GroupName, {})
        Children = Meta.get("children", [])

        for Child in Children:
            Btn = self._MakeSvgButton(Child["icon"], Child["key"])
            Key = Child["key"]
            Btn.clicked.connect(lambda Checked=False, K=Key, G=GroupName: self._ExecuteChildAction(G, K))
            self._ToolButtons.append(Btn)
            self._ToolAreaLayout.addWidget(Btn)

        BackBtn = QPushButton("←")
        BackBtn.setFixedSize(54, 54)
        BackBtn.setToolTip("Volver")
        BackBtn.setStyleSheet(self._BackBtnQss())
        BackBtn.setFont(QFont(FONT_SANS, 18, QFont.Bold))
        BackBtn.clicked.connect(self.GoBack)
        self._ToolAreaLayout.addWidget(BackBtn)

    def _RebuildButtons(self):
        if self._Level == LEVEL_GROUP and self._ActiveGroup:
            self._ShowGroupButtons(self._ActiveGroup)
        else:
            self._ShowRootButtons()

    def _EnterGroup(self, GroupName: str):
        Meta     = self._GroupMeta.get(GroupName, {})
        Children = Meta.get("children", [])

        if not Children:
            self.AddToHistory(f"{GroupName}", FromVoice=False)
            self._TriggerFlash()
            return

        self.AddToHistory(f"Menú: {GroupName}", FromVoice=False)
        self._ShowGroupButtons(GroupName)
        self._TriggerFlash()

    def _ExecuteChildAction(self, GroupName: str, ActionKey: str):
        self.AddToHistory(f"{GroupName} → {ActionKey}", FromVoice=False)
        self._TriggerFlash()

    def GoBack(self):
        if self._Level == LEVEL_GROUP:
            PrevGroup = self._ActiveGroup
            self._ShowRootButtons()
            self.AddToHistory(f"Volver (desde {PrevGroup})", FromVoice=False)

    def ToggleTheme(self):
        if self._CurrentTheme == "light":
            self.SetColor("dark")
            self._ThemeButton.setText("🌞")
            self._ThemeButton.setToolTip("Cambiar a modo claro")
            self.AddToHistory("Modo oscuro", FromVoice=False)
        else:
            self.SetColor("light")
            self._ThemeButton.setText("🌙")
            self._ThemeButton.setToolTip("Cambiar a modo oscuro")
            self.AddToHistory("Modo claro", FromVoice=False)

    def _UpdateStyles(self):
        T = self._T
        self._TitleLabel.setStyleSheet(f"color: {T['black']};")
        self._StatusLabel.setStyleSheet(self._MicQss(T["dark_text"]))
        self._ListenLabel.setStyleSheet(f"color: {T['black']};")
        self._CurrentText.setStyleSheet(self._PanelQss(FONT_MONO, T["dark_text"], 12, Weight=600))
        self._ModelLabel.setStyleSheet(f"color: {T['black']};")
        self._ModelPanel.setStyleSheet(self._PanelQss(FONT_SANS, T["black"], 10, Weight=500))
        self._HistLabel.setStyleSheet(f"color: {T['black']};")
        self._HistoryList.setStyleSheet(self._PanelQss(FONT_MONO, T["green"], 11, Weight=600))
        self._ThemeButton.setStyleSheet(self._ThemeBtnQss())
        self._HelpButton.setStyleSheet(self._BtnQss())
        for Btn in getattr(self, '_TopBarButtons', []):
            Btn.setStyleSheet(self._BtnQss())
        if hasattr(self, '_ToolAreaLayout'):
            self._RebuildButtons()
        self._PopulateModel()

    def _PopulateModel(self):
        self._ModelPanel.clear()
        Cursor = self._ModelPanel.textCursor()
        Fmt = QTextCharFormat()
        Fmt.setFontWeight(QFont.Medium)
        Fmt.setFontFamily(FONT_SANS)
        Fmt.setFontPointSize(10)
        Fmt.setForeground(QBrush(QColor(self._T["black"])))
        for Part in MODEL_PARTS:
            Cursor.insertText(Part + "\n", Fmt)
        self._ModelPanel.setTextCursor(Cursor)

    def _HighlightModelPart(self, PartName: str) -> bool:
        T   = self._T
        Doc = self._ModelPanel.document()
        ClearFmt = QTextCharFormat()
        ClearFmt.setBackground(QBrush(QColor(T["panel"])))
        ClearFmt.setForeground(QBrush(QColor(T["black"])))
        AllCursor = QTextCursor(Doc)
        AllCursor.select(QTextCursor.Document)
        AllCursor.mergeCharFormat(ClearFmt)
        HighFmt = QTextCharFormat()
        HighFmt.setBackground(QBrush(QColor(T["highlight"])))
        HighFmt.setForeground(QBrush(QColor(T["black"])))
        Cursor = Doc.find(PartName)
        if not Cursor.isNull():
            Cursor.mergeCharFormat(HighFmt)
            self._ModelPanel.setTextCursor(Cursor)
            return True
        return False

    # ================================================================
    # Flash overlay
    # ================================================================

    def _TriggerFlash(self):
        self._Flash.setGeometry(self.centralWidget().rect())
        self._Flash.raise_()
        self._Flash.Trigger()

    # ================================================================
    # Voice
    # ================================================================

    def _StartVoiceRecognition(self):
        BaseDir   = os.path.dirname(os.path.abspath(__file__))
        ModelPath = os.path.join(BaseDir, "vosk-model-small-es-0.42")
        self.voice_worker = VoiceWorker(model_path=ModelPath)
        self.voice_thread = threading.Thread(target=self.voice_worker.run, daemon=True)
        self.voice_worker.partial_result.connect(self.UpdateCurrentText)
        self.voice_worker.final_result.connect(self.ProcessVoiceCommand)
        self.voice_worker.status_signal.connect(self.UpdateStatus)
        self.voice_thread.start()

    def UpdateStatus(self, Msg: str):
        T = self._T
        L = self._Texts
        if Msg == "active":
            self._StatusLabel.setText(L["mic_active"])
            self._StatusLabel.setStyleSheet(self._MicQss(T["green"]))
        elif Msg.startswith("error:"):
            self._StatusLabel.setText(L["mic_error"])
            self._StatusLabel.setStyleSheet(self._MicQss(T["red"]))

    def UpdateCurrentText(self, Text: str):
        self._CurrentText.setText(Text)

    def ProcessVoiceCommand(self, Command: str):
        CmdNorm = _NormCmd(Command)
        L       = self._Texts
        self._CurrentText.setText(f"{L['detected']} {Command}")

        if CmdNorm == "ayuda":
            self.OpenHelpWindow()
            self.AddToHistory(Command)
            return
        if CmdNorm in ("cerrar ayuda", "cerrar ventana"):
            self.CloseHelpWindow()
            self.AddToHistory(Command)
            return
        if CmdNorm == "minimizar":
            self.showMinimized()
            self.AddToHistory(Command)
            return
        if CmdNorm == "maximizar":
            self.showMaximized() if not self.isMaximized() else self.showNormal()
            self.AddToHistory(Command)
            return
        if CmdNorm in ("cerrar programa", "cerrar app", "salir"):
            self.AddToHistory(Command)
            self.close()
            return
        if CmdNorm in ("subir", "arriba"):
            self.ScrollHistory(Up=True)
            self.AddToHistory(Command)
            return
        if CmdNorm in ("bajar", "abajo"):
            self.ScrollHistory(Up=False)
            self.AddToHistory(Command)
            return
        if CmdNorm == "modo claro":
            if self._CurrentTheme != "light":
                self.ToggleTheme()
            return
        if CmdNorm == "modo oscuro":
            if self._CurrentTheme != "dark":
                self.ToggleTheme()
            return

        if CmdNorm in ("volver", "atras", "atrás", "cerrar menu", "cerrar menú"):
            if self._Level == LEVEL_GROUP:
                self.GoBack()
                self.AddToHistory("Volver")
            else:
                self.AddToHistory("Ya en nivel raíz", Unknown=True)
            return

        if self._Level == LEVEL_ROOT:
            for GroupName in self._GroupMeta:
                if _NormCmd(GroupName) == CmdNorm:
                    self._EnterGroup(GroupName)
                    if self._GroupMeta[GroupName].get("children"):
                        self.AddToHistory(f"Menú: {GroupName}")
                    else:
                        self.AddToHistory(GroupName)
                    return
            DicDir   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DiccionarioPrueba")
            LangFile = {"es": "TraduceToEs.py", "en": "TraduceToEn.py", "pt": "TraduceToPt.py"}.get(
                self._CurrentLang, "TraduceToEs.py"
            )
            TransPath = os.path.join(DicDir, LangFile)
            if os.path.exists(TransPath):
                KC   = Keychain(TransPath)
                Keys = KC.GetKeys()
                for Key in Keys:
                    if _NormCmd(Key) == CmdNorm:
                        Value = KC.GetValues()[Keys.index(Key)].strip("'\"")
                        if Value in self._GroupMeta:
                            self._EnterGroup(Value)
                            if self._GroupMeta[Value].get("children"):
                                self.AddToHistory(f"Menú: {Value}")
                            else:
                                self.AddToHistory(Value)
                            return

        elif self._Level == LEVEL_GROUP:
            Meta     = self._GroupMeta.get(self._ActiveGroup, {})
            Children = Meta.get("children", [])
            for Child in Children:
                if _NormCmd(Child["key"]) == CmdNorm:
                    self._ExecuteChildAction(self._ActiveGroup, Child["key"])
                    self.AddToHistory(f"{self._ActiveGroup} → {Child['key']}")
                    return
            self.AddToHistory(f"'{Command}' no disponible en {self._ActiveGroup}", Unknown=True)
            return

        self.AddToHistory(Command, Unknown=True)

    def ScrollHistory(self, Up: bool = True):
        Scrollbar = self._HistoryList.verticalScrollBar()
        Step = Scrollbar.singleStep() * 5
        Scrollbar.setValue(Scrollbar.value() + (-Step if Up else Step))

    def AddToHistory(self, Text: str, Unknown: bool = False, FromVoice: bool = True):
        T         = self._T
        L         = self._Texts
        Timestamp = datetime.now().strftime("%H:%M:%S")
        Color     = T["red"] if Unknown else T["green"]
        Source    = "Voz" if FromVoice else "Btn"
        Display   = f"{L['unknown']}: {Text}" if Unknown else f"[{Source}] {Text.upper()}"
        Html = (
            f'<span style="color:{T["dark_text"]}; font-family:{FONT_MONO};'
            f' font-size:12px; font-weight:600;">[{Timestamp}]&nbsp;</span>'
            f'<span style="color:{Color}; font-family:{FONT_MONO};'
            f' font-size:12px; font-weight:600;">{Display}</span>'
        )
        self._HistoryList.append(Html)
        Cursor = self._HistoryList.textCursor()
        Cursor.movePosition(QTextCursor.End)
        self._HistoryList.setTextCursor(Cursor)
        if not Unknown:
            QTimer.singleShot(0, self._TriggerFlash)

    def OpenHelpWindow(self):
        if self._HelpWindow is None:
            self._HelpWindow = HelpWindow(self._T, self._Texts, self)
            self._HelpWindow.finished.connect(self._OnHelpClosed)
        self._HelpWindow.show()
        self._HelpWindow.raise_()
        self._HelpWindow.activateWindow()

    def CloseHelpWindow(self):
        if self._HelpWindow and self._HelpWindow.isVisible():
            self._HelpWindow.close()

    def _OnHelpClosed(self):
        self._HelpWindow = None

    def resizeEvent(self, Event):
        super().resizeEvent(Event)
        if hasattr(self, '_Flash'):
            self._Flash.setGeometry(self.centralWidget().rect())

    def closeEvent(self, Event):
        if hasattr(self, 'voice_worker'):
            self.voice_worker.stop()
        if hasattr(self, 'voice_thread'):
            self.voice_thread.join(timeout=1)
        Event.accept()