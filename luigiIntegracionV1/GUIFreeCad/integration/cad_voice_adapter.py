"""Stream voice phrases into PruebaIntegracion without modifying their core classes."""

from __future__ import annotations

from typing import Any


class CadPhraseParser:
    """«comando enviar» parsing using Command helpers (no changes to Comando.py)."""

    def __init__(self, command) -> None:
        self._command = command
        self._accumulated: list[str] = []
        self._last_token: str | None = None
        self.last_raw_phrase = ""
        self.last_normalized = ""
        self.last_matched_tokens: list[str] = []

    def feed_phrase(self, raw_phrase: str, active_vector: tuple[str, ...]) -> str | bool | None:
        if not raw_phrase:
            return None

        cmd = self._command
        self.last_raw_phrase = raw_phrase
        normalized = cmd._normalize(raw_phrase)
        self.last_normalized = normalized
        tokens = cmd._extract_tokens(normalized, active_vector)
        self.last_matched_tokens = list(tokens)

        for token in tokens:
            if token == cmd._cmd_cancel:
                self._accumulated = []
                self._last_token = None
                return False
            if token == cmd._cmd_send:
                result = "".join(self._accumulated)
                self._accumulated = []
                self._last_token = None
                return result
            if token == cmd._cmd_enter:
                self._last_token = cmd._cmd_enter
                continue
            if token == self._last_token:
                continue
            self._accumulated.append(token)
            self._last_token = token
        return None


class CadStreamingAdapter:
    """Routes shared-mic final phrases to ExploradorVoz (read-only use of their API)."""

    def __init__(self, explorador) -> None:
        self._explorador = explorador
        self._parser = CadPhraseParser(explorador.command)
        self._stop_requested = False

    @property
    def explorador(self) -> Any:
        return self._explorador

    def request_stop(self) -> None:
        self._stop_requested = True

    def procesar_frase_final(self, raw_phrase: str) -> None:
        if self._stop_requested:
            return

        exp = self._explorador
        vocab = tuple(exp._vocabulario_navegacion())
        token = self._parser.feed_phrase(raw_phrase, vocab)

        if token is False:
            if not self._stop_requested:
                print("Cancelado por el usuario.")
            return
        if token is None:
            return
        if token == "":
            raw = self._parser.last_raw_phrase
            norm = self._parser.last_normalized
            matched = self._parser.last_matched_tokens
            print(f"[DAV] Escuché «{raw}» pero falta un comando antes de «enviar».")
            if norm and norm != raw:
                print(f"[DAV]   (normalizado: «{norm}», tokens: {matched or 'ninguno'})")
            print(
                "[DAV]   Decí el comando y «enviar» en la misma frase, "
                "p. ej. «archivo enviar» o «file enviar»."
            )
            muestra = sorted(
                v for v in vocab if v not in ("enviar", "cancelar", "enter", "entrar")
            )[:10]
            if muestra:
                print(f"[DAV]   Opciones en este menú: {', '.join(muestra)}")
            return

        self._procesar_token(token)

    def _procesar_token(self, token: str) -> None:
        exp = self._explorador
        print(f"Token escuchado: {token}")
        nombre_real = exp._obtener_nombre_real_ascendente(token)
        encontrado = exp.navegador.buscar_funcion_ascendente(nombre_real)
        if encontrado:
            nodo, envoltorio = encontrado
            print(f"Funcion detectada: {nombre_real} en nodo {nodo.nombre}")
            specs = getattr(envoltorio, "param_specs", ()) or ()
            if len(specs) == 0:
                self._ejecutar_sin_parametros(nombre_real)
                return
            exp.iniciar_parametros(envoltorio)
            exp.procesar_parametros()
            return

        from PruebaIntegracion.core.ContextNode import NodoContexto

        hijo = exp.navegador.contexto_actual.elementos.get(nombre_real)
        if isinstance(hijo, NodoContexto):
            exp.navegador.establecer_contexto(hijo)
            print(f"Cambiado contexto a: {hijo.nombre}")
            return

        print(f"Comando '{token}' no reconocido en este contexto.")

    def _ejecutar_sin_parametros(self, nombre_registro: str) -> None:
        """Run dictionary commands by registry key (new, open, …).

        ExploradorVoz uses EnvoltorioFuncion.nombre, which is '<lambda>' for the
        team's dictionary lambdas — so we call Navegador.llamar with the real key.
        FreeCAD GUI commands must run on the Qt main thread.
        """
        exp = self._explorador
        contexto = exp.navegador.contexto_actual.nombre

        def _run() -> None:
            try:
                resultado = exp.navegador.llamar(
                    nombre_registro,
                    context_keys=[contexto],
                )
                print(f"Ejecución exitosa: {resultado}")
            except Exception as exc:
                print(f"Error al ejecutar la función: {exc}")

        try:
            from integration.freecad_gui_bridge import run_on_main_thread

            run_on_main_thread(_run)
        except ImportError:
            _run()
