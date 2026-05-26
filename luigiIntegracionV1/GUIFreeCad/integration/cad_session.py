"""Build PruebaIntegracion ExploradorVoz without modifying teammates' code."""

from __future__ import annotations

from pathlib import Path

from integration.dav_paths import ensure_dav_repo_on_path
from integration.freecad_gui_bridge import request_open_preferences
from integration.voice_aliases import apply_voice_aliases

LANG_TO_IDIOMA: dict[str, str] = {
    "en": "EN",
    "es": "ES",
    "pt": "ES",
}


def _open_preferences_voice(context_keys=None) -> None:
    request_open_preferences()


_open_preferences_voice.__name__ = "preferences"


def build_explorador_voz(
    model_path: str | Path,
    language: str = "es",
    *,
    debug: bool = False,
):
    ensure_dav_repo_on_path()
    from PruebaIntegracion.core.Comando import Command
    from PruebaIntegracion.core.EnvoltorioFuncion import EnvoltorioFuncion
    from PruebaIntegracion.core.ExploradorVoz import ExploradorVoz
    from PruebaIntegracion.core.Navegador import Navegador
    from PruebaIntegracion.main import construir_raiz_principal
    from PruebaIntegracion.modelo.VoskModel import VoskModel

    raiz = construir_raiz_principal()
    apply_voice_aliases(raiz, language)
    raiz.agregar_funcion("preferences", EnvoltorioFuncion(_open_preferences_voice))
    for spoken, real in (
        ("preferencias", "preferences"),
        ("configuracion", "preferences"),
        ("ajustes", "preferences"),
        ("opciones", "preferences"),
        ("preferences", "preferences"),
        ("settings", "preferences"),
    ):
        raiz.agregar_traduccion(spoken, real)

    navegador = Navegador(raiz)
    modelo_str = str(model_path)
    idioma = LANG_TO_IDIOMA.get(language, "ES")
    voice_model = VoskModel(modelo_str, debug=debug)
    command = Command(voice_model, debug=debug, modelo=modelo_str, idioma=idioma)
    return ExploradorVoz(voice_model, navegador, command=command, debug=debug)
