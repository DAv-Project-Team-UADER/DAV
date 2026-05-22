import os
import threading
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
from FlashOverlay import FlashOverlay
from HelpWindow import HelpWindow
from VoiceWorker import VoiceWorker

class MainWindow(QMainWindow):
    def __init__(self, color="light", lang="es"):
        super().__init__()
        self._PrintStartupInfo()
        self.setWindowTitle("Asistente de Voz - Control por Comandos")
        self.setMinimumSize(900, 650)
        self._HelpWindow = None

        self.SetColor(color)
        self.SetLanguage(lang)

        self._SetupUi()
        self._StartVoiceRecognition()

    @staticmethod
    def _PrintStartupInfo():
        BaseDir = os.path.dirname(os.path.abspath(__file__))
        ModelPath = os.path.join(BaseDir, "vosk-model-small-es-0.42")
        print("\n==============================")
        print("DAV - Diseño Asistido por Voz")
        print("==============================")
        print(f"Directorio del script : {BaseDir}")
        print(f"Directorio de trabajo : {os.getcwd()}")
        print(f"Ruta del modelo Vosk  : {ModelPath}")
        print(f"Modelo encontrado     : {os.path.exists(ModelPath)}")
        if os.path.exists(ModelPath):
            print(f"Contenido del modelo  : {os.listdir(ModelPath)}")
        else:
            print("ADVERTENCIA: no se encontro la carpeta del modelo")
        print("==============================\n")

    def SetColor(self, mode):
        self._T = LIGHT if mode == "light" else DARK
        if hasattr(self, '_TitleLabel'):
            self.setStyleSheet(f"QMainWindow {{ background-color: {self._T['bg']}; }}")
            self._UpdateStyles()

    def SetLanguage(self, lang):
        self._Texts = TEXTS.get(lang, TEXTS["es"])

    def _UpdateStyles(self):
        T = self._T
        self._TitleLabel.setStyleSheet(f"color: {T['black']};")
        self._StatusLabel.setStyleSheet(self._MicQss(T["green"]))
        self._ListenLabel.setStyleSheet(f"color: {T['black']};")
        self._CurrentText.setStyleSheet(self._PanelQss(FONT_MONO, T["dark_text"], 12, Weight=600))
        self._ModelLabel.setStyleSheet(f"color: {T['black']};")
        self._ModelPanel.setStyleSheet(self._PanelQss(FONT_SANS, T["black"], 10, Weight=500))
        self._HistLabel.setStyleSheet(f"color: {T['black']};")
        self._HistoryList.setStyleSheet(self._PanelQss(FONT_MONO, T["green"], 11, Weight=600))
        self._CmdsLabel.setStyleSheet(f"color: {T['black']};")
        for Btn in self._ToolButtons:
            Btn.setStyleSheet(self._BtnQss())
        self._HelpButton.setStyleSheet(self._BtnQss())
        self._PopulateModel()

    # ----------------------------------------------------------
    # UI
    # ----------------------------------------------------------

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

        LogoPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Logos", "color.svg")
        TitleRow = QHBoxLayout()
        TitleRow.setSpacing(10)
        TitleRow.addStretch()
        if os.path.exists(LogoPath):
            Logo = QSvgWidget(LogoPath)
            Logo.setFixedSize(40, 36)
            TitleRow.addWidget(Logo)
        self._TitleLabel = QLabel(L["title"])
        self._TitleLabel.setFont(QFont(FONT_SANS, 16, QFont.Bold))
        self._TitleLabel.setStyleSheet(f"color: {T['black']};")
        TitleRow.addWidget(self._TitleLabel)
        TitleRow.addStretch()
        TopLayout.addLayout(TitleRow)
        MainLayout.addWidget(TopWidget)

        self._StatusLabel = QLabel(L["mic_active"])
        self._StatusLabel.setFont(QFont(FONT_SANS, 13, QFont.DemiBold))
        self._StatusLabel.setAlignment(Qt.AlignCenter)
        self._StatusLabel.setFixedHeight(54)
        self._StatusLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._StatusLabel.setStyleSheet(self._MicQss(T["green"]))
        MainLayout.addWidget(self._StatusLabel)

        BottomWidget = QWidget()
        BottomLayout = QVBoxLayout(BottomWidget)
        BottomLayout.setSpacing(12)
        BottomLayout.setContentsMargins(40, 12, 40, 20)

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

        self._CmdsLabel = QLabel(L["section_cmds"])
        self._CmdsLabel.setFont(QFont(FONT_SANS, 12, QFont.DemiBold))
        self._CmdsLabel.setAlignment(Qt.AlignCenter)
        self._CmdsLabel.setStyleSheet(f"color: {T['black']};")
        BottomLayout.addWidget(self._CmdsLabel)

        ToolRow = QHBoxLayout()
        ToolRow.setSpacing(10)
        self._ToolButtons = []
        for i in range(12):
            Btn = QPushButton()
            Btn.setFixedSize(54, 54)
            Btn.setStyleSheet(self._BtnQss())
            ToolRow.addWidget(Btn)
            self._ToolButtons.append(Btn)
        BottomLayout.addLayout(ToolRow)

        self._HelpButton = QPushButton(L["help_btn"])
        self._HelpButton.setFont(QFont(FONT_SANS, 13, QFont.Bold))
        self._HelpButton.setFixedHeight(44)
        self._HelpButton.setMinimumWidth(200)
        self._HelpButton.setStyleSheet(self._BtnQss())
        self._HelpButton.clicked.connect(self.OpenHelpWindow)
        HelpRow = QHBoxLayout()
        HelpRow.addWidget(self._HelpButton, alignment=Qt.AlignCenter)
        BottomLayout.addLayout(HelpRow)

        MainLayout.addWidget(BottomWidget)
        self._PopulateModel()

        self._Flash = FlashOverlay(CentralWidget)
        self._Flash.setGeometry(CentralWidget.rect())

    def _TriggerFlash(self):
        self._Flash.setGeometry(self.centralWidget().rect())
        self._Flash.raise_()
        self._Flash.Trigger()

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

    def _HighlightModelPart(self, PartName):
        T = self._T
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

        Found = False
        Cursor = Doc.find(PartName)
        if not Cursor.isNull():
            Cursor.mergeCharFormat(HighFmt)
            self._ModelPanel.setTextCursor(Cursor)
            Found = True
        return Found

    def _MicQss(self, Color):
        T = self._T
        return f"""
            QLabel {{
                background-color: {T['mic']};
                border-top: 1.5px solid {T['mic_border']};
                border-bottom: 1.5px solid {T['mic_border']};
                border-left: none;
                border-right: none;
                padding: 8px;
                color: {Color};
                font-family: {FONT_SANS};
                font-size: 13px;
                font-weight: 700;
            }}
        """

    def _PanelQss(self, Font, Color, Size, Weight=500):
        T = self._T
        return f"""
            QTextEdit {{
                background-color: {T['panel']};
                color: {Color};
                border: 1.5px solid {T['panel_border']};
                border-radius: 0px;
                padding: 12px;
                font-family: {Font};
                font-size: {Size}px;
                font-weight: {Weight};
            }}
        """

    def _BtnQss(self):
        T = self._T
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 {T['btn_top']}, stop:1 {T['btn_bot']});
                border: 1.5px solid {T['btn_border']};
                border-radius: 8px;
                color: {T['black']};
                font-family: {FONT_SANS};
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 {T['btn_bot']}, stop:1 {T['btn_hover']});
                border: 1.5px solid {T['btn_border']};
            }}
            QPushButton:pressed {{
                background: {T['btn_hover']};
            }}
        """

    # ----------------------------------------------------------
    # Voz
    # ----------------------------------------------------------

    def _StartVoiceRecognition(self):
        BaseDir = os.path.dirname(os.path.abspath(__file__))
        ModelPath = os.path.join(BaseDir, "vosk-model-small-es-0.42")
        self.voice_worker = VoiceWorker(model_path=ModelPath)
        self.voice_thread = threading.Thread(target=self.voice_worker.run, daemon=True)
        self.voice_worker.partial_result.connect(self.UpdateCurrentText)
        self.voice_worker.final_result.connect(self.ProcessVoiceCommand)
        self.voice_worker.status_signal.connect(self.UpdateStatus)
        self.voice_thread.start()

    def UpdateStatus(self, msg):
        T = self._T
        L = self._Texts
        if msg == "active":
            self._StatusLabel.setText(L["mic_active"])
            self._StatusLabel.setStyleSheet(self._MicQss(T["green"]))
        elif msg.startswith("error:"):
            self._StatusLabel.setText(L["mic_error"])
            self._StatusLabel.setStyleSheet(self._MicQss(T["red"]))

    def UpdateCurrentText(self, text):
        self._CurrentText.setText(text)

    def ProcessVoiceCommand(self, command):
        command_lower = command.lower().strip()
        L = self._Texts
        self._CurrentText.setText(f"{L['detected']} {command}")

        if command_lower == "ayuda":
            self.OpenHelpWindow()
            self.AddToHistory(command)
            return
        if command_lower in ("cerrar ayuda", "cerrar ventana"):
            self.CloseHelpWindow()
            self.AddToHistory(command)
            return
        if command_lower == "minimizar":
            self.showMinimized()
            self.AddToHistory(command)
            return
        if command_lower == "maximizar":
            self.showMaximized() if not self.isMaximized() else self.showNormal()
            self.AddToHistory(command)
            return
        if command_lower in ("cerrar programa", "cerrar app", "salir"):
            self.AddToHistory(command)
            self.close()
            return
        if command_lower in ("subir", "arriba"):
            self.ScrollHistory(up=True)
            self.AddToHistory(command)
            return
        if command_lower in ("bajar", "abajo"):
            self.ScrollHistory(up=False)
            self.AddToHistory(command)
            return

        GoTo = L["go_to"]
        if command_lower.startswith(GoTo + " "):
            Target = command_lower[len(GoTo) + 1:].strip()
            ResolvedPart = MODEL_PARTS_ALIASES.get(Target)
            if ResolvedPart and self._HighlightModelPart(ResolvedPart):
                self.AddToHistory(command)
            else:
                self.AddToHistory(command, unknown=True)
            return

        if "linea" in command_lower:
            self.ExecuteCommand(command)
        elif "circulo" in command_lower:
            self.ExecuteCommand(command)
        elif "acercar" in command_lower:
            self.ExecuteCommand(command)
        elif "guardar" in command_lower:
            self.ExecuteCommand(command)
        elif "limpiar" in command_lower or "borrar" in command_lower:
            self.ExecuteCommand(command)
        else:
            self.AddToHistory(command, unknown=True)

    def ScrollHistory(self, up=True):
        Scrollbar = self._HistoryList.verticalScrollBar()
        Step = Scrollbar.singleStep() * 5
        Scrollbar.setValue(Scrollbar.value() + (-Step if up else Step))

    def ExecuteCommand(self, command):
        self.AddToHistory(command)
        if "limpiar" in command.lower() or "borrar" in command.lower():
            self._HistoryList.clear()

    def AddToHistory(self, text, unknown=False):
        T = self._T
        L = self._Texts
        Timestamp = datetime.now().strftime("%H:%M:%S")
        Color = T["red"] if unknown else T["green"]
        DisplayText = f"{L['unknown']}: {text}" if unknown else text.upper()
        Html = (
            f'<span style="color:{T["dark_text"]}; font-family:{FONT_MONO}; font-size:12px; font-weight:600;">'
            f'[{Timestamp}]&nbsp;</span>'
            f'<span style="color:{Color}; font-family:{FONT_MONO}; font-size:12px; font-weight:600;">'
            f'{DisplayText}</span>'
        )
        self._HistoryList.append(Html)
        Cursor = self._HistoryList.textCursor()
        Cursor.movePosition(QTextCursor.End)
        self._HistoryList.setTextCursor(Cursor)
        if not unknown:
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

    def closeEvent(self, event):
        if hasattr(self, 'voice_worker'):
            self.voice_worker.stop()
        if hasattr(self, 'voice_thread'):
            self.voice_thread.join(timeout=1)
        event.accept()