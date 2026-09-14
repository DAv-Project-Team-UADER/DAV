#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Localized strings and live language resolution for DAV input prompts.

The prompt windows must speak the same language selected in DAV options
(``core.preferences`` → ``SetLanguage``). The executor thread passes that
language to the collector, and here every prompt resolves it at construction
time so buttons, status lines and messages follow the configured language.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

_ES = "es"
_EN = "en"
_PT = "pt"


def _Normalize(value: Any) -> str:
    """Map any stored language value to es/en/pt, defaulting to es."""
    text = str(value or _ES).strip().lower()
    if "en" in text:
        return _EN
    if "pt" in text:
        return _PT
    return _ES


def ResolveLanguage() -> str:
    """Return the language configured in DAV options.

    Reads ``preferences.SetLanguage`` from GUIFreeCad (the same value the
    Browser and the object Tagger use). When that package cannot be imported
    the language is searched walking up to the folder that contains
    ``core/preferences.py``; the final fallback is Spanish.

    Returns:
        One of ``"es"``, ``"en"``, ``"pt"``.
    """
    try:
        from core.preferences import preferences

        return _Normalize(getattr(preferences.SetLanguage, "value", preferences.SetLanguage))
    except Exception:
        pass

    env = os.environ.get("DAV_GUI_FREECAD_ROOT", "").strip()
    candidates = (Path(env),) if env and Path(env).is_dir() else tuple(
        Path(__file__).resolve().parents
    )

    for gui_root in candidates:
        if not (gui_root / "core" / "preferences.py").is_file():
            continue
        gui_text = str(gui_root)
        if gui_text not in sys.path:
            sys.path.insert(0, gui_text)
        try:
            from core.preferences import preferences

            return _Normalize(
                getattr(preferences.SetLanguage, "value", preferences.SetLanguage)
            )
        except Exception:
            continue

    return _ES


_LABELS: dict[str, dict[str, str]] = {
    _EN: {
        "listening": "Listening...",
        "accepted": "Accepted",
        "cancelled": "Cancelled",
        "ok": "OK",
        "cancel": "Cancel",
        "value_not_empty": "Value cannot be empty.",
        "numeric_no_value": "No value to confirm. Say a number first.",
        "numeric_prompt": "Say a number, then say ok or send.",
        "string_waiting": "Waiting for enter or send...",
        "string_not_empty": "Text value cannot be empty.",
        "object_unavailable": "Object selection is not available: {error}",
        "object_no_doc": "No active FreeCAD document.",
        "object_no_objects": "The active FreeCAD document has no objects.",
        "object_browse_confirm": "Say next to browse objects, then enter or send to confirm.",
        "object_browse": "Say next to browse, or enter/send to confirm.",
        "object_select_error": "Could not select object: {error}",
        "object_selected": "Selected {name} ({current}/{total}).",
        "object_none": "No object is currently selected.",
        "param_title": "DAV Parameter {index}",
        "param_message": "Say the {kind} value for '{name}', then say enter or send.",
        "kind_float": "float",
        "kind_int": "integer",
        "kind_str": "text",
        "kind_object": "object",
    },
    _ES: {
        "listening": "Escuchando...",
        "accepted": "Aceptado",
        "cancelled": "Cancelado",
        "ok": "Aceptar",
        "cancel": "Cancelar",
        "value_not_empty": "El valor no puede estar vacío.",
        "numeric_no_value": "No hay un número para confirmar. Decí un número primero.",
        "numeric_prompt": "Decí un número y luego decí ok o enviar.",
        "string_waiting": "Esperando okey o enviar...",
        "string_not_empty": "El texto no puede estar vacío.",
        "object_unavailable": "La selección de objetos no está disponible: {error}",
        "object_no_doc": "No hay documento activo de FreeCAD.",
        "object_no_objects": "El documento activo de FreeCAD no tiene objetos.",
        "object_browse_confirm": "Decí siguiente para recorrer objetos, luego decí enviar para confirmar.",
        "object_browse": "Decí siguiente para recorrer, o decí enviar para confirmar.",
        "object_select_error": "No se pudo seleccionar el objeto: {error}",
        "object_selected": "Seleccionado {name} ({current}/{total}).",
        "object_none": "No hay ningún objeto seleccionado.",
        "param_title": "DAV Parámetro {index}",
        "param_message": "Decí el {kind} para '{name}' y luego decí enviar.",
        "kind_float": "número decimal",
        "kind_int": "número entero",
        "kind_str": "texto",
        "kind_object": "objeto del documento",
    },
    _PT: {
        "listening": "Ouvindo...",
        "accepted": "Aceito",
        "cancelled": "Cancelado",
        "ok": "OK",
        "cancel": "Cancelar",
        "value_not_empty": "O valor não pode estar vazio.",
        "numeric_no_value": "Não há número para confirmar. Diga um número primeiro.",
        "numeric_prompt": "Diga um número e depois diga ok ou enviar.",
        "string_waiting": "Aguardando enviar ou aceitar...",
        "string_not_empty": "O texto não pode estar vazio.",
        "object_unavailable": "A seleção de objetos não está disponível: {error}",
        "object_no_doc": "Não há documento ativo no FreeCAD.",
        "object_no_objects": "O documento ativo do FreeCAD não tem objetos.",
        "object_browse_confirm": "Diga próximo para percorrer objetos e depois diga enviar para confirmar.",
        "object_browse": "Diga próximo para percorrer, ou diga enviar para confirmar.",
        "object_select_error": "Não foi possível selecionar o objeto: {error}",
        "object_selected": "Selecionado {name} ({current}/{total}).",
        "object_none": "Nenhum objeto está selecionado.",
        "param_title": "DAV Parâmetro {index}",
        "param_message": "Diga o {kind} para '{name}' e depois diga enviar.",
        "kind_float": "número decimal",
        "kind_int": "número inteiro",
        "kind_str": "texto",
        "kind_object": "objeto do documento",
    },
}


def T(language: str, key: str, **kwargs: Any) -> str:
    """Return the localized string for ``key`` filling ``**kwargs``.

    Unsupported languages and missing keys fall back to Spanish and to the
    key itself respectively, so a translation gap never raises.
    """
    table = _LABELS.get(_Normalize(language), _LABELS[_ES])
    template = table.get(key, key)
    return template.format(**kwargs) if kwargs else template


def KindLabel(language: str, kind: str) -> str:
    """Return the localized label of a parameter kind (int/float/str/object)."""
    return T(language, f"kind_{kind}")