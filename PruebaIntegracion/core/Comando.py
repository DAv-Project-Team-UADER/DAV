import threading
import unicodedata
from typing import Iterable, Optional, Union

_SPOKEN_DIGITS: dict[str, str] = {
    "cero": "0",
    "uno": "1",
    "dos": "2",
    "tres": "3",
    "cuatro": "4",
    "cinco": "5",
    "seis": "6",
    "siete": "7",
    "ocho": "8",
    "nueve": "9",
}

_CMD_CANCEL = "cancelar"
_CMD_SEND = "enviar"
_CMD_ENTER = "enter"


class Command:
    """Clase de comando compatible con el diseño en `MODELO`.

    - Tiene `VECTORS` predefinidos (por índice).
    - `exclusive_listen` acepta tanto un `vector_index: int` como un iterable
      de tokens permitidos (`Iterable[str]`).
    """

    VECTORS: tuple[tuple[str, ...], ...] = (
        (_CMD_CANCEL, _CMD_SEND, _CMD_ENTER, "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"),
        (_CMD_CANCEL, _CMD_SEND, "linea fina", "linea punteada", "linea normal", "linea gruesa"),
    )

    def __init__(self, voice_model, debug: bool = False) -> None:
        self._voice_model = voice_model
        self._debug = debug
        self._result: Union[str, bool, None] = None
        self._done = threading.Event()

    def _log(self, mensaje: str) -> None:
        if self._debug:
            print(f"[Command] {mensaje}")

    @staticmethod
    def _normalize(text: str) -> str:
        without_accents = (
            unicodedata.normalize("NFKD", text)
            .encode("ASCII", "ignore")
            .decode()
            .lower()
        )
        return " ".join(_SPOKEN_DIGITS.get(word, word) for word in without_accents.split())

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
            raw_phrase = self._voice_model.escuchar_una_palabra()
            if not raw_phrase:
                self._log("frase vacia recibida; esperando otra captura")
                continue

            self._log(f"frase cruda: {raw_phrase!r}")

            normalized = self._normalize(raw_phrase)
            tokens = self._extract_tokens(normalized, active_vector)
            self._log(f"frase normalizada: {normalized!r} -> tokens: {tokens}")

            for token in tokens:
                if token == _CMD_CANCEL:
                    self._log("cancelar detectado")
                    self._result = False
                    self._done.set()
                    return
                if token == _CMD_SEND:
                    self._log(f"enviar detectado; devolviendo acumulado={accumulated}")
                    self._result = "".join(accumulated)
                    self._done.set()
                    return
                if token == _CMD_ENTER:
                    self._log("enter detectado")
                    last_token = _CMD_ENTER
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

