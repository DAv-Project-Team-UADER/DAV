from __future__ import annotations

import inspect
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from DAV.DiccionariosEnBruto.Workbench.Sketcher.runnerPydantic import sketcherActions
from DAV.DiccionariosEnBruto.Workbench.Sketcher.pydanticBuilder import buildModelForAction


def _payload_for_signature(sig: inspect.Signature) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}
    for name, param in sig.parameters.items():
        if param.kind not in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        ):
            continue

        if param.default is not inspect._empty:
            payload[name] = param.default
        else:
            payload[name] = None
    return payload


def testAllSketcherActionsValidateModelConstruction():
    """Verifica que se puede construir un modelo Pydantic para cada acción."""
    for actionKey, callableObj in sketcherActions.items():
        model = buildModelForAction(callableObj)
        assert model is not None, f"No se pudo construir modelo para '{actionKey}'"


def testAllSketcherActionsValidateEmptyPayloadOrDefaults():
    """Para acciones sin parámetros, payload vacío debe validar.
    Para acciones con parámetros, validamos con valores por defecto o None.
    """
    for actionKey, callableObj in sketcherActions.items():
        model = buildModelForAction(callableObj)
        sig = inspect.signature(callableObj)

        if len(model.model_fields) == 0:
            payload: Dict[str, Any] = {}
        else:
            payload = _payload_for_signature(sig)

        model.model_validate(payload)


def testActionsWithParamsRejectCompletelyEmptyPayload():
    """Acciones que tienen parámetros requeridos (sin default) deben rechazar
    un payload vacío con ValidationError.
    """
    for actionKey, callableObj in sketcherActions.items():
        sig = inspect.signature(callableObj)
        hasRequiredParams = any(
            p.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
            and p.default is inspect._empty
            for p in sig.parameters.values()
        )

        if not hasRequiredParams:
            continue

        model = buildModelForAction(callableObj)

        with pytest.raises(ValidationError, message=f"'{actionKey}' debería rechazar payload vacío"):
            model.model_validate({})


def testActionsWithParamsRejectWrongTypes():
    """Para _toggle_construction (la única acción con parámetros tipados),
    verifica que tipos completamente incorrectos son rechazados.

    Nota: como la mayoría de las acciones usan Any (sin anotaciones),
    este test se enfoca en callables con anotaciones explícitas.
    """
    for actionKey, callableObj in sketcherActions.items():
        sig = inspect.signature(callableObj)

        annotatedParams = [
            name
            for name, p in sig.parameters.items()
            if p.annotation is not inspect._empty
            and p.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ]

        if not annotatedParams:
            continue

        model = buildModelForAction(callableObj)

        bad_payload = {name: object() for name in annotatedParams}
        with pytest.raises(ValidationError):
            model.model_validate(bad_payload)

