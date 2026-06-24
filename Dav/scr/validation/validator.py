# Copyright (C) 2026 El Equipo del Proyecto DAV
# Copyright (C) 2026 The DAV Project Team
# Universidad Autónoma de Entre Ríos (UADER)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Validate user data before calling dictionary functions (FreeCAD console)."""

from __future__ import annotations

import inspect
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

try:
    import FreeCAD as App
except ImportError:
    App = None  # type: ignore[assignment,misc]


class LanguageCode(Enum):
    En = "en"
    Es = "es"
    PT = "pt"

    @classmethod
    def FromInput(cls, value: str | "LanguageCode") -> "LanguageCode":
        if isinstance(value, LanguageCode):
            return value
        normalized = (value or "es").strip().lower()
        for item in cls:
            if item.value == normalized or item.name.lower() == normalized:
                return item
        return cls.Es


ParamKind = str  # "int" | "float" | "str" | "object"


@dataclass(frozen=True)
class RequirementSpec:
    index: int
    name: str
    kind: ParamKind
    required: bool


_I18N: dict[LanguageCode, dict[str, str]] = {
    LanguageCode.Es: {
        "dato": "Dato",
        "expects": "se espera",
        "int": "un entero",
        "float": "un número decimal",
        "str": "un texto",
        "object": "un objeto del documento",
        "none": "sin parámetros",
        "missing": "Falta el parámetro obligatorio '{name}'.",
        "wrong_type": "El parámetro '{name}' debe ser {expected}, pero se recibió {received}.",
        "object_not_found": "El objeto '{name}' no existe en el documento activo.",
        "no_document": "No hay documento activo para resolver objetos.",
        "not_callable": "La función del diccionario no es callable.",
        "coerce_fail": "No se pudo convertir '{name}' al tipo {expected}.",
    },
    LanguageCode.En: {
        "dato": "Data",
        "expects": "expected",
        "int": "an integer",
        "float": "a decimal number",
        "str": "a string",
        "object": "a document object",
        "none": "no parameters",
        "missing": "Required parameter '{name}' is missing.",
        "wrong_type": "Parameter '{name}' must be {expected}, but got {received}.",
        "object_not_found": "Object '{name}' was not found in the active document.",
        "no_document": "No active document to resolve objects.",
        "not_callable": "Dictionary function is not callable.",
        "coerce_fail": "Could not convert '{name}' to {expected}.",
    },
    LanguageCode.PT: {
        "dato": "Dado",
        "expects": "espera-se",
        "int": "um inteiro",
        "float": "um número decimal",
        "str": "um texto",
        "object": "um objeto do documento",
        "none": "sem parâmetros",
        "missing": "Falta o parâmetro obrigatório '{name}'.",
        "wrong_type": "O parâmetro '{name}' deve ser {expected}, mas foi recebido {received}.",
        "object_not_found": "O objeto '{name}' não existe no documento ativo.",
        "no_document": "Não há documento ativo para resolver objetos.",
        "not_callable": "A função do dicionário não é callable.",
        "coerce_fail": "Não foi possível converter '{name}' para {expected}.",
    },
}


def _Text(language: LanguageCode, key: str) -> str:
    return _I18N.get(language, _I18N[LanguageCode.Es])[key]


def _IsFreeCADObject(value: Any) -> bool:
    return value is not None and hasattr(value, "Name") and hasattr(value, "Document")


def _KindFromAnnotation(annotation: Any) -> ParamKind | None:
    if annotation is inspect.Parameter.empty:
        return None
    if annotation is int:
        return "int"
    if annotation is float:
        return "float"
    if annotation is str:
        return "str"
    if annotation is object:
        return "object"
    name = getattr(annotation, "__name__", str(annotation)).lower()
    if name in ("int", "float", "str", "object"):
        return name  # type: ignore[return-value]
    return "object"


def _KindLabel(language: LanguageCode, kind: ParamKind) -> str:
    return _Text(language, kind)


class Validator:
    """
    Inspects dictionary callables and validates user-provided arguments.

    Supported FreeCAD types: int, float, str, object.
    """

    def GetRequirements(self, Language: str | LanguageCode, Function: Callable[..., Any]) -> str:
        """Print and return localized requirement lines (one per parameter)."""
        language = LanguageCode.FromInput(Language)
        specs = self._BuildSpecs(Function)
        if not specs:
            message = _Text(language, "none")
            print(message)
            return message

        lines: list[str] = []
        for spec in specs:
            lines.append(
                f"{_Text(language, 'dato')}{spec.index}: "
                f"{_Text(language, 'expects')} {_KindLabel(language, spec.kind)}"
            )
        text = "\n".join(lines)
        print(text)
        return text

    def ValidateRequirements(
        self,
        Language: str | LanguageCode,
        Function: Callable[..., Any],
        UserData: dict[str, Any] | list[Any] | tuple[Any, ...],
    ) -> tuple[bool, dict[str, Any] | None]:
        """
        Validate user data. On failure prints errors and returns (False, None).
        On success returns (True, kwargs ready to call Function).
        """
        language = LanguageCode.FromInput(Language)
        if not callable(Function):
            print(_Text(language, "not_callable"))
            return False, None

        specs = self._BuildSpecs(Function)
        provided = self._NormalizeUserData(UserData, specs)
        validated: dict[str, Any] = {}
        errors: list[str] = []

        for spec in specs:
            if spec.name not in provided:
                if spec.required:
                    errors.append(_Text(language, "missing").format(name=spec.name))
                continue

            converted, error = self._ConvertValue(
                spec.name,
                provided[spec.name],
                spec.kind,
                language,
            )
            if error:
                errors.append(error)
            else:
                validated[spec.name] = converted

        if errors:
            for message in errors:
                print(message)
            return False, None

        return True, validated

    def CallIfValid(
        self,
        Language: str | LanguageCode,
        Function: Callable[..., Any],
        UserData: dict[str, Any] | list[Any] | tuple[Any, ...],
    ) -> Any | None:
        """Validate and invoke Function(**kwargs). Returns None if validation fails."""
        ok, kwargs = self.ValidateRequirements(Language, Function, UserData)
        if not ok or kwargs is None:
            return None
        return Function(**kwargs)

    def _BuildSpecs(self, function: Callable[..., Any]) -> list[RequirementSpec]:
        specs: list[RequirementSpec] = []
        param_specs = getattr(function, "_param_specs", None)
        if param_specs:
            for index, spec in enumerate(param_specs, start=1):
                kind = self._KindFromParamSpec(spec)
                specs.append(
                    RequirementSpec(
                        index=index,
                        name=spec.name,
                        kind=kind,
                        required=getattr(spec, "required", True),
                    )
                )
            return specs

        try:
            signature = inspect.signature(function)
        except (TypeError, ValueError):
            return []

        index = 1
        for name, parameter in signature.parameters.items():
            if parameter.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue
            kind = _KindFromAnnotation(parameter.annotation) or "object"
            required = parameter.default is inspect.Parameter.empty
            specs.append(
                RequirementSpec(index=index, name=name, kind=kind, required=required)
            )
            index += 1
        return specs

    def _KindFromParamSpec(self, spec: Any) -> ParamKind:
        param_type = getattr(spec, "param_type", None) or getattr(spec, "tipo", None)
        if param_type is int:
            return "int"
        if param_type is float:
            return "float"
        if param_type is str:
            return "str"
        return "object"

    def _NormalizeUserData(
        self,
        user_data: dict[str, Any] | list[Any] | tuple[Any, ...],
        specs: list[RequirementSpec],
    ) -> dict[str, Any]:
        if isinstance(user_data, dict):
            return dict(user_data)

        values = list(user_data)
        ordered_names = [spec.name for spec in specs]
        return {
            name: values[index]
            for index, name in enumerate(ordered_names)
            if index < len(values)
        }

    def _ConvertValue(
        self,
        name: str,
        value: Any,
        kind: ParamKind,
        language: LanguageCode,
    ) -> tuple[Any | None, str | None]:
        expected = _KindLabel(language, kind)
        received = type(value).__name__

        if kind == "int":
            if isinstance(value, bool):
                return None, _Text(language, "wrong_type").format(
                    name=name, expected=expected, received=received
                )
            if isinstance(value, int):
                return value, None
            if isinstance(value, float) and value.is_integer():
                return int(value), None
            if isinstance(value, str):
                try:
                    return int(value.strip()), None
                except ValueError:
                    pass
            return None, _Text(language, "coerce_fail").format(name=name, expected=expected)

        if kind == "float":
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return float(value), None
            if isinstance(value, str):
                try:
                    return float(value.strip()), None
                except ValueError:
                    pass
            return None, _Text(language, "coerce_fail").format(name=name, expected=expected)

        if kind == "str":
            if isinstance(value, str):
                return value, None
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return str(value), None
            return None, _Text(language, "wrong_type").format(
                name=name, expected=expected, received=received
            )

        if _IsFreeCADObject(value):
            if self._ObjectExists(value):
                return value, None
            return None, _Text(language, "object_not_found").format(
                name=getattr(value, "Name", name)
            )

        if isinstance(value, str):
            resolved, error = self._ResolveObjectByName(value.strip(), language)
            if error:
                return None, error
            return resolved, None

        return None, _Text(language, "wrong_type").format(
            name=name, expected=expected, received=received
        )

    def _ResolveObjectByName(
        self,
        object_name: str,
        language: LanguageCode,
    ) -> tuple[Any | None, str | None]:
        if App is None:
            return object_name, None
        doc = App.activeDocument()
        if doc is None:
            return None, _Text(language, "no_document")
        obj = doc.getObject(object_name)
        if obj is None:
            return None, _Text(language, "object_not_found").format(name=object_name)
        return obj, None

    def _ObjectExists(self, obj: Any) -> bool:
        if App is None:
            return True
        doc = App.activeDocument()
        if doc is None:
            return False
        return doc.getObject(getattr(obj, "Name", "")) is not None
