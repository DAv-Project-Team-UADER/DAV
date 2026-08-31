#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Switches the active Vosk grammar in and out of plane-selection mode.

El selector de plano (``PlaneSelectionInputPrompt``) solo necesita que Vosk
escuche un puñado de palabras (arriba/abajo/okey/cancelar). Sin esto, el
modelo abierto confunde "abajo" con "trabajo" y otros falsos positivos del
vocabulario completo. Al activarse se acota la gramática a esas frases, y al
cerrarse se restaura la gramática del contexto CAD.
"""

from __future__ import annotations


# Frases mínimas por idioma para navegar el selector de plano. Se mantienen
# deliberadamente chicas (es el punto de acotar): arriba/abajo para mover el
# eje, okey para confirmar y cancelar para salir.
_PLANE_PHRASES: dict[str, list[str]] = {
    "es": ["arriba", "abajo", "okey", "ok", "aceptar", "cancelar"],
    "en": ["up", "down", "okey", "ok", "accept", "cancel"],
    "pt": ["cima", "abaixo", "okey", "ok", "aceitar", "cancelar"],
}


class PlaneGrammarSwitcher:
    """Restricts Vosk grammar to the sketch plane selection words."""

    @staticmethod
    def PlanePhrases(Language: str = "es") -> list[str]:
        """Return the plane-selection phrases for ``Language`` ("es"/"en"/"pt")."""
        return list(_PLANE_PHRASES.get(Language, _PLANE_PHRASES["es"]))

    @staticmethod
    def ActivatePlaneGrammar() -> None:
        """Restrict the Vosk grammar to the plane-selection words."""
        try:
            from core.settings import settings
            from speech.dav_voice_service import DavVoiceService

            DavVoiceService.get().set_grammar(
                PlaneGrammarSwitcher.PlanePhrases(settings.language)
            )
        except Exception:
            # Sin gramática acotada el reconocimiento sigue andando, solo con
            # el vocabulario abierto: se nota, no se derriba el selector.
            pass

    @staticmethod
    def RestoreCadGrammar() -> None:
        """Restore the Vosk grammar for the active Browser context."""
        try:
            from InputPrompts.NumericGrammarSwitcher import NumericGrammarSwitcher

            NumericGrammarSwitcher.RestoreCadGrammar()
        except Exception:
            pass
