from __future__ import annotations

import argparse
import json
import sys
import warnings
from typing import Any, Dict

from .pydanticBuilder import buildModelForAction
try:
    from .sketcher import sketcher as sketcherActions
except ModuleNotFoundError as exc:
    if exc.name and "FreeCADGui" in exc.name:
        warnings.warn(
            f"FreeCADGui no está disponible — sketcherActions cargado vacío. "
            f"Los tests correrán contra 0 acciones. (original error: {exc})",
            stacklevel=1,
        )
        sketcherActions = {}
    else:
        raise


def _parseArgs(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="runnerPydantic",
        description="Valida y opcionalmente ejecuta acciones del Sketcher usando Pydantic + inspect.",
    )
    parser.add_argument("action", help="Key de la acción dentro del diccionario `sketcher`")
    parser.add_argument(
        "--payload",
        default="{}",
        help="Objeto JSON con los argumentos a pasar a la acción (default: {})",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Si se pasa, ejecuta la acción luego de validar (requiere contexto FreeCAD GUI).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    ns = _parseArgs(sys.argv[1:] if argv is None else argv)

    actionKey: str = ns.action
    payloadRaw: str = ns.payload

    if len(sketcherActions) == 0:
        print(
            "[WARN] El diccionario de acciones está vacío. "
            "Probablemente FreeCADGui no está disponible en este entorno.",
            file=sys.stderr,
        )

    if actionKey not in sketcherActions:
        print(f"[ERROR] Acción desconocida: '{actionKey}'", file=sys.stderr)
        print(
            f"[INFO] Acciones disponibles (total={len(sketcherActions)}): "
            f"{sorted(sketcherActions.keys())}",
            file=sys.stderr,
        )
        return 2

    payload: Dict[str, Any]
    try:
        payload = json.loads(payloadRaw) if payloadRaw.strip() else {}
        if not isinstance(payload, dict):
            raise ValueError("El payload debe ser un objeto JSON (dict)")
    except Exception as exc:
        print(f"[ERROR] --payload JSON inválido: {exc}", file=sys.stderr)
        return 2

    actionCallable = sketcherActions[actionKey]
    model = buildModelForAction(actionCallable)

    try:
        validated = model.model_validate(payload)
    except Exception as exc:
        print(f"[FAIL] Validación fallida para la acción '{actionKey}': {exc}", file=sys.stderr)
        return 1

    validatedDict = validated.model_dump()
    print(f"[OK] Validación exitosa para '{actionKey}'. Payload: {validatedDict}")

    if not ns.execute:
        print("[INFO] --execute no fue pasado. No se ejecuta la acción.")
        return 0

    try:
        result = actionCallable(**validatedDict)
    except TypeError:
        result = actionCallable()

    print(f"[OK] Ejecución finalizada. Resultado: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())