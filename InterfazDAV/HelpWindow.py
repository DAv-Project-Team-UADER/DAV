import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtSvgWidgets import QSvgWidget

from Paletas import FONT_SANS

class HelpWindow(QDialog):
    def __init__(self, T, L, parent=None):
        super().__init__(parent)
        self.setWindowTitle(L["help_title"])
        self.setMinimumSize(560, 540)
        self.setModal(False)

        self.setStyleSheet(
            f"QDialog {{ background-color: {T['panel']}; }}"
            f"QLabel {{ background: transparent; }}"
        )

        Layout = QVBoxLayout(self)
        Layout.setSpacing(14)
        Layout.setContentsMargins(30, 30, 30, 30)

        LogoPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Logos", "color.svg")
        TitleRow = QHBoxLayout()
        TitleRow.setSpacing(10)
        TitleRow.addStretch()
        if os.path.exists(LogoPath):
            Logo = QSvgWidget(LogoPath)
            Logo.setFixedSize(36, 32)
            TitleRow.addWidget(Logo)
        Title = QLabel(L["help_title"])
        Title.setFont(QFont(FONT_SANS, 15, QFont.Bold))
        Title.setStyleSheet(f"color: {T['black']};")
        TitleRow.addWidget(Title)
        TitleRow.addStretch()
        Layout.addLayout(TitleRow)

        Line = QFrame()
        Line.setFrameShape(QFrame.HLine)
        Line.setFixedHeight(2)
        Line.setStyleSheet(f"background-color: {T['panel_border']}; border: none;")
        Layout.addWidget(Line)

        HelpText = QLabel()
        HelpText.setFont(QFont(FONT_SANS, 10))
        HelpText.setWordWrap(True)
        HelpText.setStyleSheet(f"color: {T['dark_text']};")

        RawText = L["help_text"]
        Lines = RawText.split("\n")
        HtmlLines = []
        for i, Line_ in enumerate(Lines):
            if i == 0:
                Escaped = Line_.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                HtmlLines.append(f'<div align="center"><b>{Escaped}</b></div>')
            else:
                Escaped = Line_.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;")
                HtmlLines.append(Escaped)

        HelpText.setText("<br>".join(HtmlLines))
        HelpText.setTextFormat(Qt.RichText)
        Layout.addWidget(HelpText, stretch=1)

        CloseBtn = QPushButton(L["help_close"])
        CloseBtn.setFont(QFont(FONT_SANS, 12, QFont.Bold))
        CloseBtn.setFixedHeight(44)
        CloseBtn.setMinimumWidth(180)
        CloseBtn.setStyleSheet(f"""
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
            }}
            QPushButton:pressed {{
                background: {T['btn_hover']};
            }}
        """)
        CloseBtn.clicked.connect(self.close)
        Layout.addWidget(CloseBtn, alignment=Qt.AlignCenter)