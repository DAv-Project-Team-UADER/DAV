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

import sys
import os

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

sys.path.append(os.path.join(_here, '..', 'Keychain'))

from PySide6.QtWidgets import QApplication
from MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())