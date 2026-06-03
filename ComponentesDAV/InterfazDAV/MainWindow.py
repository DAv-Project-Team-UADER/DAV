# MainWindow.py
# Asistente de Voz con captura automática del árbol de FreeCAD (cada 5 segundos)

import os
import sys
import threading
import unicodedata
from datetime import datetime
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QTextCursor, QTextCharFormat, QBrush, QPixmap
from PySide6.QtSvgWidgets import QSvgWidget

_here = os.path.dirname(os.path.abspath(__file__))
_curr = _here
for _ in range(4):
    _parent = os.path.dirname(_curr)
    if _parent == _curr:
        break
    found = False
    for name in ("ComponentesDAV", "componentesDAV"):
        if os.path.isdir(os.path.join(_parent, name)):
            if _parent not in sys.path:
                sys.path.insert(0, _parent)
            try:
                if name not in sys.modules:
                    mod = __import__(name)
                    sys.modules[name] = mod
                other_name = "componentesDAV" if name == "ComponentesDAV" else "ComponentesDAV"
                if other_name not in sys.modules and name in sys.modules:
                    sys.modules[other_name] = sys.modules[name]
            except Exception:
                pass
            found = True
            break
    if found:
        break
    _curr = _parent

from componentesDAV.InterfazDAV.Paletas import LIGHT, DARK, FONT_SANS, FONT_MONO
from componentesDAV.InterfazDAV.Textos import TEXTS, MODEL_PARTS, MODEL_PARTS_ALIASES
from componentesDAV.InterfazDAV.HelpWindow import HelpWindow
from componentesDAV.InterfazDAV.VoiceWorker import VoiceWorker
from componentesDAV.InterfazDAV.FlashOverlay import FlashOverlay
from componentesDAV.Keychain.Keychain import Keychain


# ================================================================
# THEME DETECTION
# ================================================================

def _DetectFreeCADTheme() -> str:
    """
    Intenta detectar el tema de FreeCAD.
    Retorna 'dark' o 'light' (por defecto 'light').
    """
    try:
        import FreeCADGui as Gui
        # Verificar la paleta de colores de la aplicación Qt
        palette = Gui.getMainWindow().palette()
        # Si el color de fondo es oscuro, asumimos tema oscuro
        bg_color = palette.color(palette.ColorRole.Window)
        # Calcular luminancia: si es baja, es oscuro
        luminance = (0.299 * bg_color.red() + 0.587 * bg_color.green() + 0.114 * bg_color.blue()) / 255.0
        return "dark" if luminance < 0.5 else "light"
    except Exception:
        return "light"
# Importar trigger de captura (también instala la macro automáticamente)
import trigger_capture

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

_VALUE_TO_GROUP_KEY = {
    "file":               "file",
    "edit":               "edit",
    "print_cmds":         "print",
    "doc":                "doc",
    "ayuda":              "help",
    "Std_Refresh":        "refresh",
    "Std_ViewScreenShot": "screenshot",
    "Std_TextDocument":   "textdoc",
}

def _RawValueToGroupKey(RawValue: str):
    Stripped = RawValue.strip()
    if Stripped in _VALUE_TO_GROUP_KEY:
        return _VALUE_TO_GROUP_KEY[Stripped]
    for FcCmd, GroupKey in _VALUE_TO_GROUP_KEY.items():
        if FcCmd in Stripped:
            return GroupKey
    return None


# ================================================================
# BUTTON LEVEL
# ================================================================

LEVEL_ROOT  = "root"
LEVEL_GROUP = "group"


# ================================================================
# MAIN WINDOW
# ================================================================

class MainWindow(QMainWindow):

    def __init__(self, color: str = None, lang: str = "es"):
        super().__init__()
        # Si no se especifica color, detectar el tema de FreeCAD
        if color is None:
            color = _DetectFreeCADTheme()
        
        self.setWindowTitle("Asistente de Voz - Control por Comandos")
        self.setMinimumSize(900, 650)

        self._HelpWindow   = None
        self._Level        = LEVEL_ROOT
        self._ActiveGroup  = None

        self._ToolButtons  = []
        self._GroupMeta    = {}
        self._VoiceMap     = {}

        # Variables para la imagen del árbol
        self._TreeImageLabel = None
        self._last_image_mtime = None
        self._macro_checked = False

        self.SetColor(color)
        self.SetLanguage(lang)
        self._SetupUi()
        self._StartVoiceRecognition()
        
        # Timer para auto-refrescar la imagen (cada 2 segundos)
        self._RefreshTimer = QTimer()
        self._RefreshTimer.timeout.connect(self._RefreshTreeImage)
        self._RefreshTimer.start(2000)
        
        # Timer para auto-capturar (cada 5 SEGUNDOS)
        self._CaptureTimer = QTimer()
        self._CaptureTimer.timeout.connect(self._AutoCapture)
        self._CaptureTimer.start(5000)
        
        # Verificar estado de la macro después de 3 segundos
        QTimer.singleShot(3000, self._CheckMacroStatus)
        self._StartSettingsWatcher()

    def SetColor(self, Mode: str):
        self._T = LIGHT if Mode == "light" else DARK
        self._CurrentTheme = Mode
        if hasattr(self, '_TitleLabel'):
            self.setStyleSheet(f"QMainWindow {{ background-color: {self._T['bg']}; }}")
            self._UpdateStyles()

    def SetLanguage(self, Lang: str):
        self._Texts       = TEXTS.get(Lang, TEXTS["es"])
        self._CurrentLang = Lang
        self._LoadVoiceMap()
        if hasattr(self, '_ToolRow'):
            self._RebuildButtons()
        if hasattr(self, '_ModelLabel'):
            self._ModelLabel.setText("Árbol de FreeCAD")
        if hasattr(self, '_ListenLabel'):
            L = self._Texts
            self._ListenLabel.setText(L["section_listen"])
            self._ModelLabel.setText(L["section_model"])
            self._HistLabel.setText(L["section_history"])

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
            ("configuraciones.svg",  "Preferencias de Interfaz"),
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
            
            if IconFile == "configuraciones.svg":
                Btn.clicked.connect(self._OpenPreferences)
            
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

        # ============================================================
        # PANEL DEL ÁRBOL DE FREECAD
        # ============================================================
        TreeCol = QVBoxLayout()
        TreeCol.setSpacing(4)
        
        self._ModelLabel = QLabel("Árbol de FreeCAD")
        self._ModelLabel.setFont(QFont(FONT_SANS, 12, QFont.DemiBold))
        self._ModelLabel.setStyleSheet(f"color: {T['black']};")
        TreeCol.addWidget(self._ModelLabel)
        
        self._TreeImageLabel = QLabel()
        self._TreeImageLabel.setAlignment(Qt.AlignCenter)
        self._TreeImageLabel.setMinimumHeight(160)
        self._TreeImageLabel.setScaledContents(False)
        self._ShowPlaceholderImage()
        TreeCol.addWidget(self._TreeImageLabel, stretch=1)
        
        PanelRow.addLayout(TreeCol, stretch=1)

        # ============================================================
        # PANEL DE HISTORIAL
        # ============================================================
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
        self._LoadVoiceMap()
        self._ShowRootButtons()

    def _ShowPlaceholderImage(self):
        if self._TreeImageLabel:
            placeholder_text = "🌳 Árbol de FreeCAD\n\n"
            placeholder_text += "📸 Captura automática cada 5 segundos\n\n"
            placeholder_text += "Requisitos:\n"
            placeholder_text += "1. FreeCAD ABIERTO\n"
            placeholder_text += "2. Macro 'capture_tree' ejecutándose\n"
            placeholder_text += "   (Macro → Macros → capture_tree → Ejecutar)\n\n"
            placeholder_text += "⏳ Esperando primera captura..."
            self._TreeImageLabel.setText(placeholder_text)
            self._TreeImageLabel.setStyleSheet(f"""
                background-color: {self._T['panel']};
                border: 1.5px solid {self._T['panel_border']};
                color: {self._T['dark_text']};
                font-family: {FONT_SANS};
                font-size: 11px;
                padding: 20px;
            """)

    def _CheckMacroStatus(self):
        """Verifica si la macro está respondiendo y muestra ayuda si es necesario"""
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tree_capture.png")
        
        if not os.path.exists(image_path) or os.path.getsize(image_path) == 0:
            self.AddToHistory("💡 Configuración necesaria para la captura del árbol:", System=True)
            self.AddToHistory("   1. Abre FreeCAD", System=True)
            self.AddToHistory("   2. Macro → Macros → capture_tree → Ejecutar", System=True)
            self.AddToHistory("   3. La macro se quedará ejecutándose en segundo plano", System=True)
            self.AddToHistory("   4. La imagen se actualizará automáticamente cada 5 segundos", System=True)
            self._TriggerFlash()

    def _AutoCapture(self):
        """Ejecuta captura automática cada 5 segundos (solo envía señal)"""
        try:
            success = trigger_capture.trigger_capture()
            if success:
                print("[OK] Captura automatica exitosa")
        except Exception as e:
            print(f"[ERROR] Error en captura: {e}")

    def _RefreshTreeImage(self):
        """Actualiza la imagen del árbol si cambió"""
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tree_capture.png")
        
        if os.path.exists(image_path) and os.path.getsize(image_path) > 0:
            current_mtime = os.path.getmtime(image_path)
            if self._last_image_mtime == current_mtime:
                return
            
            self._last_image_mtime = current_mtime
            
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                label_width = self._TreeImageLabel.width() - 20
                label_height = self._TreeImageLabel.height() - 20
                if label_width > 0 and label_height > 0:
                    scaled_pixmap = pixmap.scaled(
                        label_width,
                        label_height,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    self._TreeImageLabel.setPixmap(scaled_pixmap)
                else:
                    self._TreeImageLabel.setPixmap(pixmap)
                
                self._TreeImageLabel.setStyleSheet(f"""
                    background-color: {self._T['panel']};
                    border: 1.5px solid {self._T['panel_border']};
                    padding: 5px;
                """)

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
                        continue
                    Children.append({"key": ActionKey, "icon": ChildIcon})

            self._GroupMeta[GroupName] = {
                "icon":     GroupIconPath,
                "children": Children,
            }

    def _LoadVoiceMap(self):
        self._VoiceMap = {}
        LangFiles = {"es": "TraduceToEs.py", "en": "TraduceToEn.py", "pt": "TraduceToPt.py"}
        LangFile  = LangFiles.get(self._CurrentLang, "TraduceToEs.py")
        DicDir    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DiccionarioPrueba")
        TransPath = os.path.join(DicDir, LangFile)

        if not os.path.exists(TransPath):
            return

        KC     = Keychain(TransPath)
        Keys   = KC.GetKeys()
        Values = KC.GetValues()

        for Key, RawValue in zip(Keys, Values):
            GroupKey = _RawValueToGroupKey(RawValue)
            if GroupKey is not None:
                self._VoiceMap[_NormCmd(Key)] = GroupKey

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

    # ================================================================
    # Theme / Tree Image Update
    # ================================================================

    def ToggleTheme(self):
        if self._CurrentTheme == "light":
            self.SetColor("dark")
            self.AddToHistory("Modo oscuro", FromVoice=False)
        else:
            self.SetColor("light")
            self.AddToHistory("Modo claro", FromVoice=False)

    def _UpdateStyles(self):
        T = self._T
        self._TitleLabel.setStyleSheet(f"color: {T['black']};")
        self._StatusLabel.setStyleSheet(self._MicQss(T["dark_text"]))
        self._ListenLabel.setStyleSheet(f"color: {T['black']};")
        self._CurrentText.setStyleSheet(self._PanelQss(FONT_MONO, T["dark_text"], 12, Weight=600))
        
        self._ModelLabel.setStyleSheet(f"color: {T['black']};")
        if self._TreeImageLabel:
            if self._TreeImageLabel.pixmap():
                self._TreeImageLabel.setStyleSheet(f"""
                    background-color: {T['panel']};
                    border: 1.5px solid {T['panel_border']};
                    padding: 5px;
                """)
            else:
                self._TreeImageLabel.setStyleSheet(f"""
                    background-color: {T['panel']};
                    border: 1.5px solid {T['panel_border']};
                    color: {T['dark_text']};
                    font-family: {FONT_SANS};
                    font-size: 11px;
                    padding: 20px;
                """)
        
        self._HistLabel.setStyleSheet(f"color: {T['black']};")
        self._HistoryList.setStyleSheet(self._PanelQss(FONT_MONO, T["green"], 11, Weight=600))
        self._HelpButton.setStyleSheet(self._BtnQss())
        for Btn in getattr(self, '_TopBarButtons', []):
            Btn.setStyleSheet(self._BtnQss())
        if hasattr(self, '_ToolAreaLayout'):
            self._RebuildButtons()

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
        
        if not os.path.exists(ModelPath):
            print(f"[WARNING] ADVERTENCIA: Modelo Vosk no encontrado")
            return
        
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
            TargetGroup = None
            if CmdNorm in ((_NormCmd(G)) for G in self._GroupMeta):
                TargetGroup = next(G for G in self._GroupMeta if _NormCmd(G) == CmdNorm)
            elif CmdNorm in self._VoiceMap:
                Candidate = self._VoiceMap[CmdNorm]
                if Candidate in self._GroupMeta:
                    TargetGroup = Candidate

            if TargetGroup is not None:
                self._EnterGroup(TargetGroup)
                if self._GroupMeta[TargetGroup].get("children"):
                    self.AddToHistory(f"Menú: {TargetGroup}")
                else:
                    self.AddToHistory(TargetGroup)
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

    def AddToHistory(self, Text: str, Unknown: bool = False, FromVoice: bool = True, System: bool = False):
        T         = self._T
        L         = self._Texts
        Timestamp = datetime.now().strftime("%H:%M:%S")
        if System:
            Color   = T["dark_text"]
            Display = Text
        else:
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
        if not Unknown and not System:
            QTimer.singleShot(0, self._TriggerFlash)

    def _OpenPreferences(self):
        """Open the preferences dialog from GUIFreeCad."""
        try:
            import importlib.util
            import json
            
            CurrentDir = os.path.dirname(os.path.abspath(__file__))
            DavDir = os.path.dirname(CurrentDir)
            GUIFreeCadPath = os.path.join(DavDir, "IntegracionGUI", "GUIFreeCad")
            PreferenceDialogPath = os.path.join(GUIFreeCadPath, "ui", "preferences_dialog.py")
            SettingsPath = os.path.join(GUIFreeCadPath, "core", "settings.py")
            ConfigPath = os.path.join(GUIFreeCadPath, "config", "settings.json")
            
            if GUIFreeCadPath not in sys.path:
                sys.path.insert(0, GUIFreeCadPath)
            
            try:
                # Ensure config directory exists
                ConfigDir = os.path.dirname(ConfigPath)
                os.makedirs(ConfigDir, exist_ok=True)
                
                # Sincronizar el tema actual de MainWindow con settings.json
                # esto asegura que el diálogo de preferencias abra con el tema correcto
                try:
                    if os.path.exists(ConfigPath):
                        with open(ConfigPath, 'r', encoding='utf-8') as f:
                            settings_data = json.load(f)
                    else:
                        settings_data = {}
                    
                    # Actualizar settings.json con el tema actual
                    settings_data['theme'] = self._CurrentTheme
                    
                    with open(ConfigPath, 'w', encoding='utf-8') as f:
                        json.dump(settings_data, f, indent=2, ensure_ascii=False)
                except Exception as e:
                    print(f"[Warning] No se pudo sincronizar theme con settings.json: {e}")
                
                # Load settings module first
                spec_settings = importlib.util.spec_from_file_location("settings", SettingsPath)
                settings_module = importlib.util.module_from_spec(spec_settings)
                sys.modules["settings"] = settings_module
                spec_settings.loader.exec_module(settings_module)
                
                spec = importlib.util.spec_from_file_location("preferences_dialog", PreferenceDialogPath)
                prefs_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(prefs_module)
                PreferencesDialog = prefs_module.PreferencesDialog
                
                PrefsDialog = PreferencesDialog(self)
                
                # Reload settings para asegurar que se aplicó el sync
                settings_module.settings.load()
                
                # Verificar que el tema en el diálogo coincida con el de MainWindow
                if settings_module.settings.theme != self._CurrentTheme:
                    settings_module.settings.theme = self._CurrentTheme
                    settings_module.settings.save()
                settings = settings_module.settings
                if settings.theme == "dark":
                    self.SetColor("dark")
                else:
                    self.SetColor("light")
                
                PrefsDialog.settings_changed.connect(self._OnPreferencesChanged)
                PrefsDialog.exec()
            finally:
                if GUIFreeCadPath in sys.path:
                    sys.path.remove(GUIFreeCadPath)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo abrir las preferencias:\n{str(e)}"
            )

    def _OnPreferencesChanged(self):
        """Apply preferences from the shared settings.json."""
        try:
            import importlib.util
            
            CurrentDir = os.path.dirname(os.path.abspath(__file__))
            DavDir = os.path.dirname(CurrentDir)
            GUIFreeCadPath = os.path.join(DavDir, "IntegracionGUI", "GUIFreeCad")
            SettingsPath = os.path.join(GUIFreeCadPath, "core", "settings.py")
            
            if GUIFreeCadPath not in sys.path:
                sys.path.insert(0, GUIFreeCadPath)
            
            try:
                spec_settings = importlib.util.spec_from_file_location("settings_current", SettingsPath)
                settings_module = importlib.util.module_from_spec(spec_settings)
                spec_settings.loader.exec_module(settings_module)
                settings = settings_module.settings
                
                if settings.theme == "dark":
                    self.SetColor("dark")
                else:
                    self.SetColor("light")
                    
                self.AddToHistory("Preferencias actualizadas", FromVoice=False)
            finally:
                if GUIFreeCadPath in sys.path:
                    sys.path.remove(GUIFreeCadPath)
        except Exception as e:
            pass
            import json
            path = self._SettingsPath()
            if not os.path.exists(path):
                return
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            theme    = data.get("theme", self._CurrentTheme)
            language = data.get("language", "es")
            
            # Aplicar tema — solo si cambió
            if theme in ("dark", "light") and theme != self._CurrentTheme:
                self.SetColor(theme)
            
            # Aplicar idioma — solo si cambió
            if language in ("es", "en", "pt") and language != self._CurrentLang:
                self.SetLanguage(language)
            
            self.AddToHistory("Preferencias actualizadas", FromVoice=False)
        except Exception:
            pass

    def _SettingsPath(self) -> str:
        DavDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(DavDir, "IntegracionGUI", "GUIFreeCad", "config", "settings.json")

    def _StartSettingsWatcher(self):
        """Poll settings.json every second; apply if the file changed since last check."""
        self._settings_mtime = self._ReadSettingsMtime()
        self._settings_poll = QTimer(self)
        self._settings_poll.timeout.connect(self._PollSettings)
        self._settings_poll.start(1000)

    def _ReadSettingsMtime(self) -> float:
        try:
            return os.path.getmtime(self._SettingsPath())
        except OSError:
            return 0.0

    def _PollSettings(self):
        mtime = self._ReadSettingsMtime()
        if mtime != self._settings_mtime:
            self._settings_mtime = mtime
            self._OnPreferencesChanged()

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
        
        if hasattr(self, '_TreeImageLabel') and self._TreeImageLabel:
            current_pixmap = self._TreeImageLabel.pixmap()
            if current_pixmap and not current_pixmap.isNull():
                label_width = self._TreeImageLabel.width() - 20
                label_height = self._TreeImageLabel.height() - 20
                if label_width > 0 and label_height > 0:
                    scaled_pixmap = current_pixmap.scaled(
                        label_width,
                        label_height,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    self._TreeImageLabel.setPixmap(scaled_pixmap)

    def closeEvent(self, Event):
        if hasattr(self, 'voice_worker'):
            self.voice_worker.stop()
        if hasattr(self, 'voice_thread'):
            self.voice_thread.join(timeout=1)
        Event.accept()