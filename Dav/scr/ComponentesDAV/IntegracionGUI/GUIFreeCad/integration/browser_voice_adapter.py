"""
BrowserVoiceAdapter: connects Vosk spoken phrases to the new Browser navigation engine.
"""

from __future__ import annotations

import io
import sys
import unicodedata
from typing import Any

from navigation.browser import Browser
from integration.voice_history import append_voice_history


def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return " ".join(stripped.lower().split())


_SEND_WORDS = {"enviar", "send"}
_CANCEL_WORDS = {"cancelar", "cancel"}


class _CapturedOutput:
    """Captura lo que un comando escribe con ``print`` mientras corre.

    Los diccionarios imprimen su salida a stdout (988 llamadas repartidas en
    123 archivos), que en FreeCAD termina en el Report View y no en el panel
    DAV. Capturarlo aca permite reenviarlo sin tocar cada comando.

    Restaura ``sys.stdout`` incluso si el comando lanza, para no dejar la
    salida secuestrada.

    Example::

        with _CapturedOutput() as captured:
            browser.ProcessPhrase(token)
        for line in captured.Lines():
            panel.AddToHistory(line)
    """

    def __init__(self) -> None:
        self._buffer = io.StringIO()
        self._previous = None

    def __enter__(self) -> "_CapturedOutput":
        self._previous = sys.stdout
        sys.stdout = self._buffer
        return self

    def __exit__(self, *_exc) -> bool:
        sys.stdout = self._previous
        return False

    def Lines(self) -> list[str]:
        """Lineas capturadas, sin las vacias."""
        return [line for line in self._buffer.getvalue().splitlines() if line.strip()]


class BrowserVoiceAdapter:
    """Adapter to feed the raw phrase directly to the Browser's ProcessPhrase."""

    def __init__(self, browser: Browser) -> None:
        self._browser = browser
        self._stop_requested = False

    @property
    def explorador(self) -> Any:
        return None

    def request_stop(self) -> None:
        self._stop_requested = True

    def procesar_frase_final(self, raw_phrase: str) -> None:
        if self._stop_requested or not raw_phrase:
            return

        normalized = _normalize(raw_phrase)
        print(f"[BrowserVoiceAdapter] Received phrase: '{raw_phrase}'")
        append_voice_history(f"[DAV] Voz: {raw_phrase}")
        # OJO: aca estamos en el hilo del microfono. Tocar un widget Qt desde
        # aca es access violation (crash duro, no excepcion de Python), por eso
        # todo lo que llegue a la GUI va dentro de run_on_main_thread mas abajo.

        token = self._extract_token(normalized)
        if token is None:
            return
        if token is False:
            print("[DAV Browser] Cancelled.")
            return

        # Acciones que cambian de nivel: tras ellas mostramos el contexto.
        _NAV_ACTIONS = {"descend", "back", "base_jump"}

        def _run() -> None:
            # Ya en el hilo principal: recien aca se puede tocar la GUI.
            self._publish_line(f"[DAV] Voz: {raw_phrase}", recognized=raw_phrase)

            # Los comandos del diccionario (los ayuda.py sobre todo) escriben
            # su salida con print: son 988 llamadas en 123 archivos, asi que en
            # vez de tocarlas una por una se captura el stdout mientras corre
            # el comando y se vuelca al panel. Sin esto la ayuda aparecia solo
            # en el Report View de FreeCAD.
            with _CapturedOutput() as captured:
                result = self._browser.ProcessPhrase(token)

            for line in captured.Lines():
                print(line)
                self._publish_line(line)

            if result.Success:
                print(f"[DAV Browser] Success ({result.Action}): {result.Message}")
                append_voice_history(f"[DAV] OK ({result.Action}): {result.Message}")
                self._publish_line(f"[DAV] OK ({result.Action}): {result.Message}")
                if result.Action in _NAV_ACTIONS:
                    described = self._browser.DescribeContext()
                    print(described)
                    append_voice_history(described)
                    for line in described.splitlines():
                        self._publish_line(line)
            else:
                print(f"[DAV Browser] Ignored: {result.Message}")
                append_voice_history(f"[DAV] Ignorado: {result.Message}")
                self._publish_line(f"[DAV] Ignorado: {result.Message}", unknown=True)
            self._export_state()

        try:
            from integration.freecad_gui_bridge import run_on_main_thread
            run_on_main_thread(_run)
        except ImportError:
            _run()

    def _export_state(self) -> None:
        """Refresca el panel con el contexto activo.

        Antes serializaba el contexto a context_state.json para que lo leyera
        la ventana externa por polling. Esa ventana ya no existe (etapa 4) y
        nadie leia el archivo, asi que solo se publica al panel acoplado.
        """
        self._publish_to_dock()

    @staticmethod
    def _on_gui_thread() -> bool:
        """True si estamos en el hilo de la GUI.

        Tocar un widget Qt desde otro hilo es access violation: crashea el
        proceso entero sin pasar por ningun except de Python. Se comprueba
        antes de publicar en vez de confiar en el llamador.
        """
        try:
            from PySide6.QtCore import QCoreApplication, QThread
        except ImportError:
            return False
        app = QCoreApplication.instance()
        if app is None:
            return False
        return QThread.currentThread() is app.thread()

    @classmethod
    def _publish_line(cls, line: str, *, recognized: str = "", unknown: bool = False) -> None:
        """Manda una linea de historial al panel acoplado, si esta montado."""
        if not cls._on_gui_thread():
            return
        try:
            from integration.dav_dock_panel import get_source
        except ImportError:
            return
        source = get_source()
        if source is None:
            return
        if recognized:
            source.PublishRecognized(recognized)
        source.PublishHistory(line, unknown)

    @classmethod
    def _publish_to_dock(cls) -> None:
        """Refresca el panel acoplado, si esta montado."""
        if not cls._on_gui_thread():
            return
        try:
            from integration.dav_dock_panel import get_source
        except ImportError:
            return
        source = get_source()
        if source is not None:
            source.PublishContext()
            source.PublishTree()

    @staticmethod
    def _extract_token(normalized: str):
        """Return command token, False for cancel, None to ignore."""
        for word in _CANCEL_WORDS:
            if normalized == word or normalized.endswith(" " + word):
                return False
        for word in _SEND_WORDS:
            if normalized.endswith(" " + word):
                token = normalized[: -(len(word) + 1)].strip()
                return token or None
            if normalized == word:
                return None
        return normalized or None
