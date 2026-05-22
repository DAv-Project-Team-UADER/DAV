from __future__ import annotations

import unicodedata


_DIGITOS_ES = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"]
_DIGITOS_EN = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


class Idioma:
    """Tokens base para el idioma activo.

    Conserva tres listas internas principales:
    - numeros hablados, para convertirlos a digitos.
    - digitos, para el vocabulario activo luego de normalizar.
    - comandos, para enter/cancelar/enviar.
    """

    def __init__(self, modelo: str = "", idioma: str = "ES") -> None:
        self.modelo = modelo.strip()
        self.idioma = self._normalizar_idioma(idioma)

        if self.idioma == "EN":
            self._lista_numeros_hablados = list(_DIGITOS_EN)
            self._lista_comandos = ["enter", "cancel", "send"]
        else:
            self._lista_numeros_hablados = list(_DIGITOS_ES)
            self._lista_comandos = ["enter", "entrar", "cancelar", "enviar"]

        self._lista_digitos = [str(indice) for indice in range(10)]

    @staticmethod
    def _normalizar_idioma(idioma: str) -> str:
        texto = unicodedata.normalize("NFKD", idioma).encode("ASCII", "ignore").decode().upper().strip()
        if texto in {"EN", "INGLES", "ENGLISH"}:
            return "EN"
        return "ES"

    @property
    def lista_numeros_hablados(self) -> list[str]:
        return list(self._lista_numeros_hablados)

    @property
    def lista_digitos(self) -> list[str]:
        return list(self._lista_digitos)

    @property
    def lista_comandos(self) -> list[str]:
        return list(self._lista_comandos)

    @property
    def comando_enter(self) -> str:
        return "enter"

    @property
    def comando_cancelar(self) -> str:
        return "cancel" if self.idioma == "EN" else "cancelar"

    @property
    def comando_enviar(self) -> str:
        return "send" if self.idioma == "EN" else "enviar"

    @property
    def vocabulario_basico(self) -> list[str]:
        return list(dict.fromkeys(self._lista_digitos + self._lista_comandos))

    @property
    def mapa_numeros(self) -> dict[str, str]:
        return {numero: str(indice) for indice, numero in enumerate(self._lista_numeros_hablados)}

    def normalizar_texto(self, texto: str) -> str:
        texto_normalizado = (
            unicodedata.normalize("NFKD", texto)
            .encode("ASCII", "ignore")
            .decode()
            .lower()
        )
        mapa = self.mapa_numeros
        return " ".join(mapa.get(palabra, palabra) for palabra in texto_normalizado.split())
