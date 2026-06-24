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