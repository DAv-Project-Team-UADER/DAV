import threading
import unicodedata
from typing import Optional, Union

_SPOKEN_DIGITS: dict[str, str] = {
    "cero": "0", "uno": "1", "dos": "2", "tres": "3", "cuatro": "4",
    "cinco": "5", "seis": "6", "siete": "7", "ocho": "8", "nueve": "9",
}

_CMD_CANCEL = "cancelar"
_CMD_SEND   = "enviar"
_CMD_ENTER  = "enter"

class Command:
    VECTORS: tuple[tuple[str, ...], ...] = (
        (_CMD_CANCEL, _CMD_SEND, _CMD_ENTER, "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"),
        (_CMD_CANCEL, _CMD_SEND, "linea fina", "linea punteada", "linea normal", "linea gruesa"),
    )

    def __init__(self, voice_model) -> None:
        self._voice_model = voice_model
        self._result: Union[str, bool, None] = None
        self._done = threading.Event()

    @staticmethod
    def _normalize(text: str) -> str:
        without_accents = (
            unicodedata.normalize("NFKD", text)
            .encode("ASCII", "ignore")
            .decode()
            .lower()
        )
        return " ".join(_SPOKEN_DIGITS.get(w, w) for w in without_accents.split())

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

    def _listening_loop(self, vector_index: int) -> None:
        active_vector = self.VECTORS[vector_index]
        accumulated: list[str] = []
        last_token: Optional[str] = None

        while True:
            raw_phrase = self._voice_model.escuchar_una_palabra()
            if not raw_phrase:
                continue

            for token in self._extract_tokens(self._normalize(raw_phrase), active_vector):
                if token == _CMD_CANCEL:
                    self._result = False
                    self._done.set()
                    return
                if token == _CMD_SEND:
                    self._result = "".join(accumulated)
                    self._done.set()
                    return
                if token == _CMD_ENTER:
                    last_token = _CMD_ENTER  
                    continue
                if token == last_token:
                    continue
                accumulated.append(token)
                last_token = token

    def exclusive_listen(self, vector_index: int) -> Union[str, bool, None]:
        self._result = None
        self._done.clear()

        t = threading.Thread(target=self._listening_loop, args=(vector_index,), daemon=True)
        t.start()

        self._done.wait()
        return self._result

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
