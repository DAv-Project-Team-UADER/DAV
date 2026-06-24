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
from __future__ import annotations

import unicodedata


_DIGITS_ES = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"]
_DIGITS_EN = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


class Language:
    """Base tokens for the active language.

    Maintains three main internal lists:
    - spoken numbers, to convert them to digits.
    - digits, for the active vocabulary after normalization.
    - commands, for enter/cancel/send.
    """

    def __init__(self, model: str = "", language: str = "ES") -> None:
        self.model = model.strip()
        self.language = self._normalize_language(language)

        if self.language == "EN":
            self._spoken_numbers_list = list(_DIGITS_EN)
            self._command_list = ["enter", "cancel", "send"]
        else:
            self._spoken_numbers_list = list(_DIGITS_ES)
            self._command_list = ["enter", "entrar", "cancelar", "enviar"]

        self._digit_list = [str(index) for index in range(10)]

    @staticmethod
    def _normalize_language(language: str) -> str:
        text = unicodedata.normalize("NFKD", language).encode("ASCII", "ignore").decode().upper().strip()
        if text in {"EN", "INGLES", "ENGLISH"}:
            return "EN"
        return "ES"

    @property
    def spoken_numbers(self) -> list[str]:
        return list(self._spoken_numbers_list)

    @property
    def digits(self) -> list[str]:
        return list(self._digit_list)

    @property
    def commands(self) -> list[str]:
        return list(self._command_list)

    @property
    def enter_command(self) -> str:
        return "enter"

    @property
    def cancel_command(self) -> str:
        return "cancel" if self.language == "EN" else "cancelar"

    @property
    def send_command(self) -> str:
        return "send" if self.language == "EN" else "enviar"

    @property
    def basic_vocabulary(self) -> list[str]:
        return list(dict.fromkeys(self._digit_list + self._command_list))

    @property
    def number_map(self) -> dict[str, str]:
        return {number: str(index) for index, number in enumerate(self._spoken_numbers_list)}

    def normalize_text(self, text: str) -> str:
        """Normalizes text by removing diacritics and converting spoken number words to digits."""
        normalized_text = (
            unicodedata.normalize("NFKD", text)
            .encode("ASCII", "ignore")
            .decode()
            .lower()
        )
        mapping = self.number_map
        return " ".join(mapping.get(word, word) for word in normalized_text.split())