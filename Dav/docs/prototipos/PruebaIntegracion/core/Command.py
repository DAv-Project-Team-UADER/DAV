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
import threading
import unicodedata
from typing import Iterable, Optional, Union

from PruebaIntegracion.core.Language import Language


class Command:
    """Clase de comando compatible con el diseño en `MODELO`.

    - Tiene `VECTORS` predefinidos (por índice).
    - `exclusive_listen` acepta tanto un `vector_index: int` como un iterable
      de tokens permitidos (`Iterable[str]`).
    """

    VECTORS: tuple[tuple[str, ...], ...] = (
        ("cancelar", "enviar", "enter", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"),
        ("cancelar", "enviar", "linea fina", "linea punteada", "linea normal", "linea gruesa"),
    )

    def __init__(self, voice_model, debug: bool = False, model: str = "", language: str = "ES") -> None:
        self._voice_model = voice_model
        self._debug = debug
        self._result: Union[str, bool, None] = None
        self._done = threading.Event()
        self.language = Language(model=model, language=language)
        self._cmd_cancel = self.language.cancel_command
        self._cmd_send = self.language.send_command
        self._cmd_enter = self.language.enter_command

    def _log(self, mensaje: str) -> None:
        if self._debug:
            print(f"[Command] {mensaje}")

    def _normalize(self, text: str) -> str:
        return self.language.normalize_text(text)

    @staticmethod
    def _extract_tokens(phrase: str, active_vector: tuple[str, ...]) -> list[str]:
        words = phrase.split()
        tokens: list[str] = []
        i = 0
        while i < len(words):
            if i + 1 < len(words):
                bigram = words[i] + " " + words[i + 1]
                if bigram in active_vector:
                    tokens.append(bigram)
                    i += 2
                    continue
            if words[i] in active_vector:
                tokens.append(words[i])
            i += 1
        return tokens

    def _listening_loop(self, active_vector: tuple[str, ...]) -> None:
        accumulated: list[str] = []
        last_token: Optional[str] = None

        self._log(f"iniciando escuchando con vector activo: {active_vector}")

        while True:
            # voice_model implementations use `listen_for_one_word` in English API
            raw_phrase = None
            # support both possible method names for compatibility
            if hasattr(self._voice_model, "listen_for_one_word"):
                raw_phrase = self._voice_model.listen_for_one_word()
            elif hasattr(self._voice_model, "escuchar_una_palabra"):
                raw_phrase = self._voice_model.escuchar_una_palabra()
            else:
                raise AttributeError("voice_model has no listen_for_one_word or escuchar_una_palabra method")
            if not raw_phrase:
                self._log("frase vacia recibida; esperando otra captura")
                continue

            self._log(f"frase cruda: {raw_phrase!r}")

            normalized = self._normalize(raw_phrase)
            tokens = self._extract_tokens(normalized, active_vector)
            self._log(f"frase normalizada: {normalized!r} -> tokens: {tokens}")

            for token in tokens:
                if token == self._cmd_cancel:
                    self._log("cancelar detectado")
                    self._result = False
                    self._done.set()
                    return
                if token == self._cmd_send:
                    self._log(f"enviar detectado; devolviendo acumulado={accumulated}")
                    self._result = "".join(accumulated)
                    self._done.set()
                    return
                if token == self._cmd_enter:
                    self._log("enter detectado")
                    last_token = self._cmd_enter
                    continue
                if token == last_token:
                    self._log(f"token repetido ignorado: {token!r}")
                    continue
                accumulated.append(token)
                self._log(f"token aceptado: {token!r}; acumulado={accumulated}")
                last_token = token

    def exclusive_listen(self, vector: Union[int, Iterable[str]]) -> Union[str, bool, None]:
        """Bloqueante: acepta `vector` como índice en `VECTORS` o como iterable de tokens."""
        if isinstance(vector, int):
            active_vector = self.VECTORS[vector]
        else:
            active_vector = tuple(vector)

        self._log(f"exclusive_listen llamado con vector={active_vector}")

        self._result = None
        self._done.clear()
        t = threading.Thread(target=self._listening_loop, args=(active_vector,), daemon=True)
        t.start()
        self._done.wait()
        self._log(f"exclusive_listen retorno={self._result!r}")
        return self._result

    ExclusiveListening = exclusive_listen

    def systematic_fill(self) -> None:
        pass

    def print_test(self, vector_index: int) -> None:
        print(f"\n--- RUNNING TEST (Vector {vector_index}) ---")
        res = self.exclusive_listen(vector_index)

        if res is False:
            print(">>> w = False")
        elif res is None:
            print(">>> w = null")
        else:
            print(f">>> w = '{res}'")

