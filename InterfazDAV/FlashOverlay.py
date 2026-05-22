from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRect
from PySide6.QtGui import QPainter, QColor, QLinearGradient

class FlashOverlay(QWidget):
    def __init__(self, Parent):
        super().__init__(Parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAutoFillBackground(False)
        self._Progress = 0.0
        self._Direction = 1
        self.hide()

        self._Timer = QTimer(self)
        self._Timer.setInterval(16)
        self._Timer.timeout.connect(self._Step)

    def Trigger(self):
        self._Progress = 0.0
        self._Direction = 1
        self.setGeometry(self.parent().rect())
        self.show()
        self.raise_()
        self._Timer.start()

    def _Step(self):
        self._Progress += 0.05 * self._Direction
        if self._Direction == 1 and self._Progress >= 1.0:
            self._Progress = 1.0
            self._Direction = -1
        elif self._Direction == -1 and self._Progress <= 0.0:
            self._Progress = 0.0
            self._Timer.stop()
            self.hide()
        self.update()

    def paintEvent(self, Event):
        if self._Progress <= 0.0:
            return
        Painter = QPainter(self)
        W = self.width()
        H = self.height()

        FlashHeight = int(H * 0.45)
        Grad = QLinearGradient(0, H, 0, H - FlashHeight)

        FlashColor = QColor("#3A7BFF")
        FlashColor.setAlpha(int(255 * 0.65 * self._Progress))

        EdgeColor = QColor("#3A7BFF")
        EdgeColor.setAlpha(0)

        Grad.setColorAt(0.0, FlashColor)
        Grad.setColorAt(1.0, EdgeColor)

        Painter.fillRect(QRect(0, H - FlashHeight, W, FlashHeight), Grad)
        Painter.end()