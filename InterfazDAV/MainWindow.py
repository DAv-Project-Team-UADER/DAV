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
    QTextEdit, QPushButton, QLabel, QSizePolicy, QMenu
)
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QFont, QColor, QTextCursor, QTextCharFormat, QBrush, QIcon
from PySide6.QtSvgWidgets import QSvgWidget

from Paletas import LIGHT, DARK, FONT_SANS, FONT_MONO
from Textos import TEXTS, MODEL_PARTS, MODEL_PARTS_ALIASES
from HelpWindow import HelpWindow
from VoiceWorker import VoiceWorker


def quitar_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')


class MainWindow(QMainWindow):
    def __init__(self, color="light", lang="es"):
        super().__init__()
        self.setWindowTitle("Asistente de Voz - Control por Comandos")
        self.setMinimumSize(900, 650)
        self._HelpWindow = None
        self._buttons_map = {}
        self._current_menu = None  # Menú actualmente abierto
        self._current_theme = color

        self.SetColor(color)
        self.SetLanguage(lang)
        self._SetupUi()
        self._StartVoiceRecognition()

    def SetColor(self, mode):
        self._T = LIGHT if mode == "light" else DARK
        self._current_theme = mode
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
        self._ThemeButton.setStyleSheet(self._ThemeBtnQss())
        self._HelpButton.setStyleSheet(self._BtnQss())
        self._PopulateModel()

    def _FlashButton(self, btn):
        original_style = btn.styleSheet()
        flash_color = "#3A7BFF" if self._current_theme == "light" else "#5B8CDE"
        btn.setStyleSheet(f"QPushButton {{ background-color: {flash_color}; border: 2px solid {flash_color}; border-radius: 8px; }}")
        QTimer.singleShot(300, lambda: btn.setStyleSheet(original_style))

    def _ThemeBtnQss(self):
        T = self._T
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {T['btn_top']}, stop:1 {T['btn_bot']});
                border: 1.5px solid {T['btn_border']}; border-radius: 8px; color: {T['black']};
                font-family: {FONT_SANS}; font-size: 14px; font-weight: bold;
            }}
            QPushButton:hover {{ background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {T['btn_bot']}, stop:1 {T['btn_hover']}); border: 1.5px solid {T['btn_border']}; }}
            QPushButton:pressed {{ background: {T['btn_hover']}; }}
        """

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
        if os.path.exists(LogoPath):
            Logo = QSvgWidget(LogoPath)
            Logo.setFixedSize(40, 36)
            TitleRow.addWidget(Logo)
        self._TitleLabel = QLabel(L["title"])
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
        self._HelpButton = QPushButton("❓")
        self._HelpButton.setFont(QFont(FONT_SANS, 14, QFont.Bold))
        self._HelpButton.setFixedSize(40, 36)
        self._HelpButton.setToolTip("Ayuda")
        self._HelpButton.setStyleSheet(self._BtnQss())
        self._HelpButton.clicked.connect(self.OpenHelpWindow)
        TitleRow.addWidget(self._HelpButton)
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

        # ==================== BOTONES CON SUBMENUS ====================
        ToolRow = QHBoxLayout()
        ToolRow.setSpacing(10)
        self._ToolButtons = []
        self._buttons_map = {}

        menus_data = [
            ("Punto", "Sketcher_CreatePoint", "punto", []),
            ("Línea", "Sketcher_CreateLine", "linea", []),
            ("Arco", "Sketcher_CreateArc", "arco", [
                ("Arco (centro, radio)", "arco centro", "Sketcher_CreateArc"),
                ("Arco por 3 puntos", "arco por 3 puntos", "Sketcher_Create3PointArc"),
                ("Arco elíptico", "arco eliptico", "Sketcher_CreateArcOfEllipse"),
                ("Arco de hipérbola", "arco hiperbola", "Sketcher_CreateArcOfHyperbola"),
                ("Arco de parábola", "arco parabola", "Sketcher_CreateArcOfParabola"),
            ]),
            ("Círculo", "Sketcher_CreateCircle", "circulo", [
                ("Círculo (centro, radio)", "circulo centro", "Sketcher_CreateCircle"),
                ("Círculo por 3 puntos", "circulo por 3 puntos", "Sketcher_Create3PointCircle"),
                ("Elipse (centro)", "elipse centro", "Sketcher_CreateEllipseByCenter"),
                ("Elipse por 3 puntos", "elipse 3 puntos", "Sketcher_CreateEllipseBy3Points"),
            ]),
            ("Rectángulo", "Sketcher_CreateRectangle", "rectangulo", [
                ("Rectángulo por esquinas", "rectangulo esquinas", "Sketcher_CreateRectangle"),
                ("Rectángulo centrado", "rectangulo centrado", "Sketcher_CreateRectangle_Center"),
                ("Rectángulo redondeado", "rectangulo redondeado", "Sketcher_CreateOblong"),
            ]),
            ("Polígono", "Sketcher_CreateHexagon", "poligono", [
                ("Triángulo", "triangulo", "Sketcher_CreateTriangle"),
                ("Cuadrado", "cuadrado", "Sketcher_CreateSquare"),
                ("Pentágono", "pentagono", "Sketcher_CreatePentagon"),
                ("Hexágono", "hexagono", "Sketcher_CreateHexagon"),
                ("Heptágono", "heptagono", "Sketcher_CreateHeptagon"),
                ("Octágono", "octagono", "Sketcher_CreateOctagon"),
                ("Polígono regular...", "poligono regular", "Sketcher_CreateRegularPolygon"),
            ]),
            ("Ranura", "Sketcher_CreateSlot", "ranura", [
                ("Ranura recta", "ranura recta", "Sketcher_CreateSlot"),
                ("Ranura arqueada", "ranura arco", "Sketcher_CreateArcSlot"),
            ]),
            ("Curva", "Sketcher_CreateBSpline", "curva", [
                ("Curva por puntos de control", "curva por puntos", "Sketcher_CreateBSpline"),
                ("Curva cerrada", "curva cerrada", "Sketcher_CreatePeriodicBSpline"),
                ("Curva por nudos", "curva por nudos", "Sketcher_CreateBSplineByInterpolation"),
            ]),
        ]

        icons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Icons")

        for parent_text, icon_name, parent_cmd, children in menus_data:
            btn = QPushButton()
            btn.setFixedSize(54, 54)
            btn.setToolTip(parent_text)
            btn.parent_cmd = parent_cmd
            btn.parent_name = parent_text
            
            icon_path = os.path.join(icons_dir, icon_name + ".svg")
            if not os.path.exists(icon_path) and icon_name == "Sketcher_CreateSlot":
                icon_path = os.path.join(icons_dir, "Sketcher_CreateOblong.svg")
            
            if os.path.exists(icon_path):
                svg_widget = QSvgWidget(icon_path)
                svg_widget.setFixedSize(42, 42)
                btn.setLayout(QVBoxLayout())
                btn.layout().addWidget(svg_widget, alignment=Qt.AlignCenter)
                btn.layout().setContentsMargins(6, 6, 6, 6)
            else:
                btn.setText(parent_text[:3])
            
            btn.setStyleSheet(self._BtnQss())
            self._buttons_map[parent_cmd] = btn
            
            if children:
                menu = QMenu(self)
                menu.setStyleSheet(f"""
                    QMenu {{ background-color: {self._T['panel']}; border: 1px solid {self._T['panel_border']}; border-radius: 5px; padding: 5px; }}
                    QMenu::item {{ padding: 8px 25px 8px 10px; color: {self._T['black']}; font-family: {FONT_SANS}; font-size: 11px; }}
                    QMenu::item:selected {{ background-color: {self._T['highlight']}; }}
                """)
                
                for child_text, child_cmd, child_icon_name in children:
                    child_icon_path = os.path.join(icons_dir, child_icon_name + ".svg")
                    if os.path.exists(child_icon_path):
                        child_icon = QIcon(child_icon_path)
                        action = menu.addAction(child_icon, child_text)
                    else:
                        action = menu.addAction(child_text)
                    action.setData((parent_text, child_text, child_cmd))
                    action.triggered.connect(self._OnChildAction)
                
                btn.setMenu(menu)
                # Guardar referencia al menú en el botón
                btn.custom_menu = menu
            else:
                btn.clicked.connect(lambda checked, cmd=parent_cmd, name=parent_text: self._OnDirectAction(name))
            
            ToolRow.addWidget(btn)
            self._ToolButtons.append(btn)

        BottomLayout.addLayout(ToolRow)
        MainLayout.addWidget(BottomWidget)
        self._PopulateModel()

    def _OpenMenu(self, btn, menu_name):
        """Abre un menú y guarda la referencia global"""
        if btn and hasattr(btn, 'custom_menu'):
            self._current_menu = btn.custom_menu
            self.AddToHistory(f"Menú: {menu_name}")
            # Usar QTimer para evitar bloqueo
            QTimer.singleShot(10, lambda: btn.custom_menu.exec(btn.mapToGlobal(QPoint(0, btn.height()))))
            return True
        return False

    def _CloseCurrentMenu(self):
        """Cierra el menú actual si está abierto"""
        if self._current_menu:
            self._current_menu.close()
            self._current_menu = None
            return True
        return False

    def _OnChildAction(self):
        action = self.sender()
        if action and action.data():
            parent_name, child_name, child_cmd = action.data()
            self.AddToHistory(f"Menú {parent_name}: {child_name}")
            print(f"[MENU {parent_name.upper()}: {child_name}]")
            for btn in self._buttons_map.values():
                if btn.parent_name == parent_name:
                    self._FlashButton(btn)
                    break
            # Cerrar el menú después de seleccionar un hijo
            self._CloseCurrentMenu()

    def _OnDirectAction(self, command_name):
        self.AddToHistory(command_name)

    def ToggleTheme(self):
        if self._current_theme == "light":
            self.SetColor("dark")
            self._ThemeButton.setText("🌞")
            self._ThemeButton.setToolTip("Cambiar a modo claro")
            self.AddToHistory("Cambiar a modo oscuro")
        else:
            self.SetColor("light")
            self._ThemeButton.setText("🌙")
            self._ThemeButton.setToolTip("Cambiar a modo oscuro")
            self.AddToHistory("Cambiar a modo claro")

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
        Cursor = Doc.find(PartName)
        if not Cursor.isNull():
            Cursor.mergeCharFormat(HighFmt)
            self._ModelPanel.setTextCursor(Cursor)
            return True
        return False

    def _MicQss(self, Color):
        T = self._T
        return f"""
            QLabel {{ background-color: {T['mic']}; border-top: 1.5px solid {T['mic_border']}; border-bottom: 1.5px solid {T['mic_border']};
            border-left: none; border-right: none; padding: 8px; color: {Color}; font-family: {FONT_SANS}; font-size: 13px; font-weight: 700; }}
        """

    def _PanelQss(self, Font, Color, Size, Weight=500):
        T = self._T
        return f"""
            QTextEdit {{ background-color: {T['panel']}; color: {Color}; border: 1.5px solid {T['panel_border']}; border-radius: 0px;
            padding: 12px; font-family: {Font}; font-size: {Size}px; font-weight: {Weight}; }}
        """

    def _BtnQss(self):
        T = self._T
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {T['btn_top']}, stop:1 {T['btn_bot']});
                border: 1.5px solid {T['btn_border']}; border-radius: 8px; color: {T['black']};
                font-family: {FONT_SANS}; font-size: 10px; font-weight: bold;
            }}
            QPushButton:hover {{ background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {T['btn_bot']}, stop:1 {T['btn_hover']}); border: 1.5px solid {T['btn_border']}; }}
            QPushButton:pressed {{ background: {T['btn_hover']}; }}
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
        command_lower = quitar_acentos(command_lower)
        L = self._Texts
        self._CurrentText.setText(f"{L['detected']} {command}")

        # Comandos de control
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
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()
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

        # Cambio de tema
        if command_lower == "modo claro":
            if self._current_theme != "light":
                self.ToggleTheme()
            else:
                self.AddToHistory("Ya está en modo claro")
            return
        if command_lower == "modo oscuro":
            if self._current_theme != "dark":
                self.ToggleTheme()
            else:
                self.AddToHistory("Ya está en modo oscuro")
            return

        # Cerrar menú (ahora sí funciona)
        if command_lower in ("atras", "cerrar menu", "cerrar menú", "salir menu", "salir menú"):
            if self._CloseCurrentMenu():
                self.AddToHistory("Cerrar menú")
            else:
                self.AddToHistory("No hay menú abierto")
            return

        # Abrir menús con voz
        if command_lower == "arco":
            btn = self._buttons_map.get("arco")
            if btn:
                self._OpenMenu(btn, "Arco")
            return
        if command_lower == "circulo":
            btn = self._buttons_map.get("circulo")
            if btn:
                self._OpenMenu(btn, "Círculo")
            return
        if command_lower == "rectangulo":
            btn = self._buttons_map.get("rectangulo")
            if btn:
                self._OpenMenu(btn, "Rectángulo")
            return
        if command_lower == "poligono":
            btn = self._buttons_map.get("poligono")
            if btn:
                self._OpenMenu(btn, "Polígono")
            return
        if command_lower == "ranura":
            btn = self._buttons_map.get("ranura")
            if btn:
                self._OpenMenu(btn, "Ranura")
            return
        if command_lower == "curva":
            btn = self._buttons_map.get("curva")
            if btn:
                self._OpenMenu(btn, "Curva")
            return

        # Comandos directos
        if command_lower == "punto":
            btn = self._buttons_map.get("punto")
            if btn:
                self._FlashButton(btn)
            self.AddToHistory("Punto")
            return
        if command_lower == "linea":
            btn = self._buttons_map.get("linea")
            if btn:
                self._FlashButton(btn)
            self.AddToHistory("Línea")
            return

        # Comandos de hijos
        hijos_map = {
            "arco centro": ("Arco", "Arco (centro, radio)"),
            "arco por 3 puntos": ("Arco", "Arco por 3 puntos"),
            "arco por tres puntos": ("Arco", "Arco por 3 puntos"),
            "arco eliptico": ("Arco", "Arco elíptico"),
            "arco hiperbola": ("Arco", "Arco de hipérbola"),
            "arco parabola": ("Arco", "Arco de parábola"),
            "circulo centro": ("Círculo", "Círculo (centro, radio)"),
            "circulo por 3 puntos": ("Círculo", "Círculo por 3 puntos"),
            "circulo por tres puntos": ("Círculo", "Círculo por 3 puntos"),
            "elipse centro": ("Círculo", "Elipse (centro)"),
            "elipse por 3 puntos": ("Círculo", "Elipse por 3 puntos"),
            "elipse por tres puntos": ("Círculo", "Elipse por 3 puntos"),
            "rectangulo esquinas": ("Rectángulo", "Rectángulo por esquinas"),
            "rectangulo centrado": ("Rectángulo", "Rectángulo centrado"),
            "rectangulo redondeado": ("Rectángulo", "Rectángulo redondeado"),
            "ranura recta": ("Ranura", "Ranura recta"),
            "ranura arco": ("Ranura", "Ranura arqueada"),
            "triangulo": ("Polígono", "Triángulo"),
            "cuadrado": ("Polígono", "Cuadrado"),
            "pentagono": ("Polígono", "Pentágono"),
            "hexagono": ("Polígono", "Hexágono"),
            "heptagono": ("Polígono", "Heptágono"),
            "octagono": ("Polígono", "Octágono"),
            "poligono regular": ("Polígono", "Polígono regular..."),
            "curva por puntos": ("Curva", "Curva por puntos de control"),
            "curva cerrada": ("Curva", "Curva cerrada"),
            "curva por nudos": ("Curva", "Curva por nudos"),
        }

        for palabra, (parent_name, child_display) in hijos_map.items():
            if palabra in command_lower:
                self.AddToHistory(f"Menú {parent_name}: {child_display}")
                for btn in self._buttons_map.values():
                    if btn.parent_name == parent_name:
                        self._FlashButton(btn)
                        break
                self._CloseCurrentMenu()  # Cerrar menú si estaba abierto
                return

        # Navegación en modelo
        GoTo = L["go_to"]
        if command_lower.startswith(GoTo + " "):
            Target = command_lower[len(GoTo) + 1:].strip()
            ResolvedPart = MODEL_PARTS_ALIASES.get(Target)
            if ResolvedPart and self._HighlightModelPart(ResolvedPart):
                self.AddToHistory(command)
            else:
                self.AddToHistory(command, unknown=True)
            return

        self.AddToHistory(command, unknown=True)

    def ScrollHistory(self, up=True):
        Scrollbar = self._HistoryList.verticalScrollBar()
        Step = Scrollbar.singleStep() * 5
        if up:
            Scrollbar.setValue(Scrollbar.value() - Step)
        else:
            Scrollbar.setValue(Scrollbar.value() + Step)

    def AddToHistory(self, text, unknown=False, from_voice=True):
        T = self._T
        L = self._Texts
        Timestamp = datetime.now().strftime("%H:%M:%S")
        Color = T["red"] if unknown else T["green"]
        source = "Voz" if from_voice else "Boton"
        if unknown:
            DisplayText = f"{L['unknown']}: {text}"
        else:
            DisplayText = f"[{source}] {text.upper()}"
        Html = f'<span style="color:{T["dark_text"]}; font-family:{FONT_MONO}; font-size:12px; font-weight:600;">[{Timestamp}]&nbsp;</span><span style="color:{Color}; font-family:{FONT_MONO}; font-size:12px; font-weight:600;">{DisplayText}</span>'
        self._HistoryList.append(Html)
        Cursor = self._HistoryList.textCursor()
        Cursor.movePosition(QTextCursor.End)
        self._HistoryList.setTextCursor(Cursor)

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

    def closeEvent(self, event):
        if hasattr(self, 'voice_worker'):
            self.voice_worker.stop()
        if hasattr(self, 'voice_thread'):
            self.voice_thread.join(timeout=1)
        event.accept()