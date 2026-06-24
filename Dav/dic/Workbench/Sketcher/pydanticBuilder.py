from __future__ import annotations

import inspect
from typing import Any, Callable, Dict, Optional, Tuple, Union, get_args, get_origin

try:
    from pydantic import BaseModel, Field, create_model
except Exception as exc:
    raise RuntimeError(
        "Pydantic is required for validation. Install it in your environment (e.g. `pip install pydantic`)."
    ) from exc


def _normalize_type(annotation: Any) -> Any:
    """Normalize type annotations to something Pydantic can understand."""
    if annotation is inspect._empty:
        return Any

    origin = get_origin(annotation)
    if origin is None:
        return annotation

    if origin is Union:
        args = get_args(annotation)
        if type(None) in args:
            non_none = [a for a in args if a is not type(None)]
            if len(non_none) == 1:
                return non_none[0]
            return annotation
    return annotation


def _extractParameters(func: Callable[..., Any]) -> Tuple[inspect.Signature, Dict[str, inspect.Parameter]]:
    sig = inspect.signature(func)
    params: Dict[str, inspect.Parameter] = {
        name: p
        for name, p in sig.parameters.items()
        if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    }
    return sig, params


def buildModelForAction(actionCallable: Callable[..., Any], *, modelName: Optional[str] = None) -> type[BaseModel]:
    """Create a dynamic Pydantic model for the given callable.

    Validation strategy:
    - Si el callable no tiene parámetros posicionales, el modelo espera payload vacío.
    - Si tiene parámetros, cada uno se convierte en un field.
    - Se usan las anotaciones de tipo cuando están presentes; sino los fields son `Any`.

    Nota: Muchas acciones de este proyecto son `lambda: Gui.runCommand(...)`
    (sin parámetros explícitos). Para esas, la validación Pydantic solo verifica
    que no se pasen inputs inesperados.
    """

    sig, params = _extractParameters(actionCallable)

    if modelName is None:
        safe = getattr(actionCallable, "__name__", "anonymous")
        modelName = f"ActionPayload_{safe}"

    fields: Dict[str, tuple[Any, Any]] = {}

    for name, param in params.items():
        ann = _normalize_type(param.annotation)

        if param.default is not inspect._empty:
            fields[name] = (ann, Field(default=param.default))
        else:
            fields[name] = (ann, ...)

    if len(fields) == 0:
        return create_model(modelName, __base__=BaseModel)

    return create_model(modelName, **fields)


def validatePayload(actionCallable: Callable[..., Any], payload: Dict[str, Any]) -> BaseModel:
    model = buildModelForAction(actionCallable)
    return model.model_validate(payload)


def getActionSignature(actionCallable: Callable[..., Any]) -> str:
    try:
        return str(inspect.signature(actionCallable))
    except Exception:
        return "<signature unavailable>"