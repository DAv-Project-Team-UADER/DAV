"""Start/stop the DAV voice engine (Browser + BrowserVoiceAdapter) from GUIFreeCad."""

from __future__ import annotations

import os
import traceback
from pathlib import Path

from integration.dav_paths import ensure_dav_repo_on_path, ensure_gui_on_path
from integration.voice_history import reset_voice_history, export_voice_status
from speech.dav_voice_service import DavVoiceService

# Hay tres puntos que arrancan la voz (el comando de la GUI, el workbench al
# activarse y freecad_voice_setup) y disparan casi a la vez: el log mostro
# cuatro start_voice_engine en dos segundos, y hasta seis.
#
# Todos corren en el hilo de Qt, uno detras de otro, asi que un Lock no sirve:
# cada llamada lo toma y lo suelta sin encontrarlo ocupado. Lo que hace falta es
# una guarda de reentrada, para que mientras el primer arranque esta a mitad de
# camino los demas salgan enseguida en vez de rehacer el trabajo.
_starting = False



def _active_adapter(svc):
    """Adapter del motor de voz en curso, o None si no hay ninguno.

    Se lee del servicio para poder montar el panel cuando la voz ya estaba
    activa, sin crear un segundo Browser ni reiniciar el microfono.
    """
    return getattr(svc, "_cad_adapter", None)


def _schedule_panel() -> None:
    """Abre el panel solo, poco despues de activarse la voz.

    Diferido para no montarlo en medio del arranque del motor, y siempre en el
    hilo de la GUI (un widget tocado desde otro hilo es access violation).

    Se puede desactivar con ``DAV_AUTO_PANEL=0`` si el panel diera problemas:
    la voz sigue funcionando y el panel se abre a mano desde la barra DAV.
    """
    if os.environ.get("DAV_AUTO_PANEL") == "0":
        return

    def _open() -> None:
        try:
            show_dock_panel()
        except Exception as exc:  # noqa: BLE001 - el panel no tumba la voz
            _print_message(f"[DAV] No se pudo abrir el panel: {exc}\n")

    try:
        from PySide6.QtCore import QTimer
        QTimer.singleShot(600, _open)
    except ImportError:
        _open()


def show_dock_panel() -> bool:
    """Muestra el panel DAV acoplado dentro de FreeCAD.

    Se invoca a mano desde la barra DAV, no en el arranque: usa el Qt de
    FreeCAD (sin el conflicto de DLLs del proceso externo), pero si algo suyo
    falla no debe dejar la aplicacion inusable.

    Requiere el motor de voz activo, porque el panel se alimenta del Browser
    en curso.

    Returns:
        True si el panel quedo montado.
    """
    svc = DavVoiceService.get()
    adapter = _active_adapter(svc)
    if adapter is None:
        _print_message(
            "[DAV] Primero activá la voz («Iniciar voz DAV»): el panel se "
            "alimenta del motor en curso.\n"
        )
        return False

    browser = getattr(adapter, "_browser", None)
    if browser is None:
        _print_message("[DAV] El motor de voz no expone un Browser.\n")
        return False

    try:
        from integration.dav_dock_panel import install_dock_panel
        return install_dock_panel(browser, adapter) is not None
    except Exception as exc:  # noqa: BLE001 - el panel no debe tumbar la voz
        _print_message(f"[DAV] No se pudo montar el panel acoplado: {exc}\n")
        return False


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
    """Arranca el motor de voz, ignorando los pedidos duplicados.

    Returns:
        True si la voz quedo andando (o ya estaba), False si fallo.
    """
    global _starting
    if _starting:
        # Otro arranque esta a mitad de camino: no rehacer el trabajo.
        return True
    _starting = True
    try:
        return _start_voice_engine(debug=debug)
    finally:
        _starting = False


def _start_voice_engine(*, debug: bool = False) -> bool:
    try:
        ensure_gui_on_path()
        ensure_dav_repo_on_path()
        from core.dav_log import get_logger, log_file_path, log_unhandled_thread_exceptions
        from core.model_manager import get_active_model_path
        from core.settings import settings

        log = get_logger("arranque")
        log_unhandled_thread_exceptions()
        log.info("iniciando motor de voz (debug=%s)", debug)
        _print_message(f"[DAV] Log: {log_file_path()}\n")

        settings.load()
        log.info(
            "settings: idioma=%s modelo=%s", settings.language, settings.model_size
        )
        model = get_active_model_path(settings.language, settings.model_size)
        if model is None:
            err_msg = (
                "[DAV] Sin modelo Vosk para idioma "
                f"'{settings.language}'. Configurá Preferencias DAV o ejecutá "
                "python scripts/setup_models.py en GUIFreeCad.\n"
            )
            _print_error(err_msg)
            export_voice_status("error", f"Sin modelo Vosk ({settings.language})")
            return False

        svc = DavVoiceService.get()
        if svc.is_cad_engine_loaded():
            _print_message("[DAV] El motor de voz ya está activo.\n")
            export_voice_status("active", "Voz activa")
            _schedule_panel()
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

        _schedule_panel()

        adapter._export_state()

        if not svc.start_cad(adapter):
            export_voice_status("error", "No se pudo iniciar micrófono")
            return False

        export_voice_status("active", "Voz activa")
        _print_message(
            "[DAV] Voz activa (motor unificado). Ejemplos: «preferencias enviar», "
            "«archivo enviar» → «nuevo enviar».\n"
        )
        return True
    except Exception:
        _print_error("[DAV] No se pudo iniciar la voz:\n")
        _print_error(traceback.format_exc())
        export_voice_status("error", "Error al iniciar motor de voz")
        return False


def stop_voice_engine(*, wait: bool = True, timeout: float = 4.0) -> None:
    svc = DavVoiceService.get()
    if not svc.is_cad_engine_loaded() and not svc.is_mic_running():
        _print_message("[DAV] El motor de voz no está activo.\n")
        export_voice_status("inactive", "Voz inactiva")
        return
    _print_message("[DAV] Deteniendo voz… (puede tardar un instante).\n")
    svc.stop(wait=wait, timeout=timeout)
    export_voice_status("inactive", "Voz inactiva")
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
