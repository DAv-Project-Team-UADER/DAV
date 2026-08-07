"""Start/stop unified DAV voice from GUIFreeCad (no changes to PruebaIntegracion core)."""

from __future__ import annotations

import os
import traceback
from pathlib import Path

from integration.dav_paths import ensure_dav_repo_on_path, ensure_gui_on_path
from integration.voice_history import reset_voice_history, pop_command_queue
from speech.dav_voice_service import DavVoiceService

_command_timer = None

def _poll_command_queue(adapter):
    command = pop_command_queue()
    if command:
        adapter.procesar_frase_final(command)


def _resolve_dictionary_root() -> Path:
    """Localiza la carpeta de diccionarios respetando DAV_DICTIONARY_ROOT.

    Orden de resolución (igual criterio que dav_commands._dictionary_root):
      1. Variable de entorno DAV_DICTIONARY_ROOT (la setea el launcher).
      2. Candidatos relativos subiendo desde este archivo: layout DavCore
         (``Dav/dic``) y layout previo (``DiccionariosEnBruto``).

    Returns:
        Ruta a la carpeta de diccionarios; si no se encuentra ninguna,
        devuelve el mejor candidato del layout DavCore (DictionaryLoader
        tolera que no exista y arranca con contextos vacíos sin romper).
    """
    env = os.environ.get("DAV_DICTIONARY_ROOT", "").strip()
    if env:
        path = Path(env)
        if path.is_dir():
            return path.resolve()

    here = Path(__file__).resolve()
    for ancestor in here.parents:
        for candidate in (ancestor / "Dav" / "dic", ancestor / "DiccionariosEnBruto"):
            if _is_dictionary_dir(candidate):
                return candidate.resolve()

    # parents[5]=DAV-root con el nuevo layout (.../Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/integration)
    return here.parents[5] / "Dav" / "dic"


def _is_dictionary_dir(path: Path) -> bool:
    """True si la carpeta es un diccionario real (no un placeholder vacío).

    Evita confundir ``ComponentesDAV/Dav/dic`` (solo placeholder) con el
    ``Dav/dic`` real que contiene base.py y los TraduceTo*.py.
    """
    return (path / "base.py").is_file() or (path / "TraduceToEs.py").is_file()


def is_voice_running() -> bool:
    return DavVoiceService.get().is_cad_engine_loaded()


def start_voice_engine(*, debug: bool = False) -> bool:
    try:
        ensure_gui_on_path()
        ensure_dav_repo_on_path()
        from core.model_manager import get_active_model_path
        from core.settings import settings

        settings.load()
        model = get_active_model_path(settings.language, settings.model_size)
        if model is None:
            _print_error(
                "[DAV] Sin modelo Vosk para idioma "
                f"'{settings.language}'. Configurá Preferencias DAV o ejecutá "
                "python scripts/setup_models.py en GUIFreeCad.\n"
            )
            return False

        svc = DavVoiceService.get()
        if svc.is_cad_engine_loaded():
            _print_message("[DAV] El motor de voz ya está activo.\n")
            return True
        reset_voice_history()

        from core.language_code import LanguageCode
        from core.preferences import preferences
        from navigation.browser import Browser
        from integration.browser_voice_adapter import BrowserVoiceAdapter
        from InputPrompts.PromptedCommandExecutor import PromptedCommandExecutor

        preferences.SetLanguage = LanguageCode.FromStorage(settings.language)

        _dict_root = _resolve_dictionary_root()
        executor = PromptedCommandExecutor(Language=settings.language)
        browser = Browser(dictionary_root=_dict_root, prefs=preferences, on_execute=executor)
        adapter = BrowserVoiceAdapter(browser)
        
        adapter._export_state()
        
        if not svc.start_cad(adapter):
            return False

        global _command_timer
        if _command_timer is None:
            try:
                from PySide6.QtCore import QTimer
            except ImportError:
                from PySide2.QtCore import QTimer
            _command_timer = QTimer()
            _command_timer.timeout.connect(lambda: _poll_command_queue(adapter))
            _command_timer.start(500)

        _print_message(
            "[DAV] Voz activa (motor unificado). Ejemplos: «preferencias enviar», "
            "«archivo enviar» → «nuevo enviar».\n"
        )
        return True
    except Exception:
        _print_error("[DAV] No se pudo iniciar la voz:\n")
        _print_error(traceback.format_exc())
        return False


def stop_voice_engine(*, wait: bool = True, timeout: float = 4.0) -> None:
    global _command_timer
    if _command_timer is not None:
        _command_timer.stop()
        _command_timer = None
        
    svc = DavVoiceService.get()
    if not svc.is_cad_engine_loaded() and not svc.is_mic_running():
        _print_message("[DAV] El motor de voz no está activo.\n")
        return
    _print_message("[DAV] Deteniendo voz… (puede tardar un instante).\n")
    svc.stop(wait=wait, timeout=timeout)
    _print_message("[DAV] Motor de voz detenido.\n")


def _print_message(text: str) -> None:
    try:
        import FreeCAD as App

        App.Console.PrintMessage(text)
    except ImportError:
        print(text, end="")


def _print_error(text: str) -> None:
    try:
        import FreeCAD as App

        App.Console.PrintError(text)
    except ImportError:
        print(text, end="", file=__import__("sys").stderr)
