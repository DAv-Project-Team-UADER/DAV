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
import queue
from PySide6.QtCore import QObject, Slot


class VoiceCommandAdapter(QObject):
  
    def __init__(self, parent=None):
        super().__init__(parent)
        self._phrase_queue: queue.Queue[str] = queue.Queue()
        self._active = True

    def connect_worker(self, voice_worker) -> None:
        voice_worker.final_result.connect(self._on_final_result)

    def disconnect_worker(self, voice_worker) -> None:
        try:
            voice_worker.final_result.disconnect(self._on_final_result)
        except RuntimeError:
            pass

    @Slot(str)
    def _on_final_result(self, text: str) -> None:
        if self._active and text.strip():
            self._phrase_queue.put(text.strip())

    @Slot(str)
    def receive_gui_phrase(self, text: str) -> None:
        self._on_final_result(text)

    def escuchar_una_palabra(self, timeout: float = 30.0) -> str:
        try:
            return self._phrase_queue.get(timeout=0.5)
        except queue.Empty:
            return None

    # Compatibility alias: provide English method name expected by other modules
    def listen_for_one_word(self, timeout: float = 30.0) -> str:
        return self.escuchar_una_palabra(timeout)

    def flush(self) -> None:
        while not self._phrase_queue.empty():
            try:
                self._phrase_queue.get_nowait()
            except queue.Empty:
                break

    def stop(self) -> None:
    
        self._active = False
        self._phrase_queue.put("") 