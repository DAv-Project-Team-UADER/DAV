# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.
# SPDX-License-Identifier: GPL-3.0-or-later

"""Ask the user to name a freshly created object, without ever blocking it."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

try:
    from .tagger import Tagger
except ImportError:
    from tagger import Tagger


_MESSAGES = {
    "es": "Diga el nombre del objeto y luego diga aceptar",
    "en": "Say the object name, then say enter",
    "pt": "Diga o nome do objeto e depois diga aceitar",
}

_TITLES = {
    "es": "DAV — Nombre del objeto",
    "en": "DAV — Object name",
    "pt": "DAV — Nome do objeto",
}

_SEARCH_MESSAGES = {
    "es": "Diga el nombre del objeto a seleccionar y luego diga aceptar",
    "en": "Say the name of the object to select, then say enter",
    "pt": "Diga o nome do objeto a selecionar e depois diga aceitar",
}

_SEARCH_TITLES = {
    "es": "DAV — Buscar objeto",
    "en": "DAV — Find object",
    "pt": "DAV — Procurar objeto",
}


def AskObjectName(Obj: Any, TaggerInstance: Tagger | None = None) -> str:
    """Prompt for a spoken name and apply it to Obj's Label.

    Never blocks object creation: if the prompt is unavailable, cancelled or
    fails, the Tagger's automatic name is applied instead.

    Args:
        Obj: The FreeCAD object just created.
        TaggerInstance: Optional Tagger to reuse (keeps counters consistent).

    Returns:
        The label that ended up applied to Obj.

    Example::

        box = doc.addObject("Part::Box", "Box")
        AskObjectName(box)   # -> "mesa"
    """
    if Obj is None:
        return ""

    tagger = TaggerInstance or Tagger(document=_DocumentOf(Obj))
    spoken = _RequestSpokenName()
    return tagger.ApplyCustomName(Obj, spoken, kind="object")


def _DocumentOf(Obj: Any):
    try:
        return Obj.Document
    except Exception:
        return None


def AskExistingObjectName() -> str:
    """Prompt for the name of an object that already exists in the document.

    Unlike naming a new object, this swaps the Vosk grammar to the document's
    labels so the recognizer can actually hear them.

    Returns:
        The dictated text, or '' when unavailable or cancelled.
    """
    return _RequestSpokenName(ForExistingObject=True)


def _RequestSpokenName(ForExistingObject: bool = False) -> str:
    """Open the string prompt and return the dictated text, or ''.

    Any failure degrades to '' so the caller falls back to the automatic name.
    """
    if not _HasRunningGuiApp():
        # Construir un QDialog sin QApplication aborta el proceso: Qt no lanza
        # una excepcion de Python, se lleva el interprete entero (igual que
        # SetGrammar de Vosk). Por eso se chequea antes y no con try/except.
        return ""

    try:
        _EnsureGuiRootOnPath()
        from InputPrompts.PromptVoiceRouter import PromptVoiceRouter

        if ForExistingObject:
            from InputPrompts.ObjectNameInputPrompt import (
                ObjectNameInputPrompt as PromptClass,
            )
        else:
            from InputPrompts.NewObjectNameInputPrompt import (
                NewObjectNameInputPrompt as PromptClass,
            )
    except Exception:
        # Sin GUI de DAV cargada (consola pelada, tests) no hay dictado posible.
        return ""

    language = _CurrentLanguage()
    titles = _SEARCH_TITLES if ForExistingObject else _TITLES
    messages = _SEARCH_MESSAGES if ForExistingObject else _MESSAGES
    if ForExistingObject:
        prompt = PromptClass(
            titles.get(language, titles["es"]),
            messages.get(language, messages["es"]),
        )
    else:
        prompt = PromptClass(
            titles.get(language, titles["es"]),
            messages.get(language, messages["es"]),
            Language=language,
        )

    PromptVoiceRouter.SetActivePrompt(prompt)
    try:
        result = prompt.RequestValue()
    except Exception:
        return ""
    finally:
        PromptVoiceRouter.ClearActivePrompt(prompt)

    if result is None or not getattr(result, "Success", False):
        return ""
    return str(getattr(result, "Value", "") or "")


def _HasRunningGuiApp() -> bool:
    """Return True only when a QApplication instance already exists.

    Inside FreeCAD this is always true. In a bare console or in tests it is
    false, and no dialog must be built: Qt aborts the whole interpreter when
    a widget is constructed without an application.
    """
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        try:
            from PySide2.QtWidgets import QApplication  # type: ignore[assignment]
        except ImportError:
            return False
    except Exception:
        return False

    try:
        return QApplication.instance() is not None
    except Exception:
        return False


def _CurrentLanguage() -> str:
    try:
        _EnsureGuiRootOnPath()
        from core.settings import settings

        return str(getattr(settings, "language", "es") or "es").strip().lower()[:2]
    except Exception:
        return "es"


def _EnsureGuiRootOnPath() -> None:
    """Put GUIFreeCad on sys.path so InputPrompts/core imports resolve."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "ComponentesDAV" / "IntegracionGUI" / "GUIFreeCad"
        if candidate.is_dir():
            text = str(candidate)
            if text not in sys.path:
                sys.path.insert(0, text)
            return
