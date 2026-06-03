#  Copyright (C) 2026 The DAV Project Team-                                 |#  Copyright (C) 2026 El Equipo del Proyecto DAV
#  Universidad Autónoma de Entre Ríos (UADER)                               |#  Universidad Autónoma de Entre Ríos (UADER)
#  Directed by Gerard Guillermo and Gallo Fabricio David                    |#  Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#                                                                           |#
#  This program is free software: you can redistribute it and/or modify     |#  Este programa es software libre: usted puede redistribuirlo y/o modificarlo
#  it under the terms of the GNU General Public License as published by     |#  bajo los términos de la Licencia Pública General GNU tal como fue publicada 
#  the Free Software Foundation, in GLPv3 version  of the License           |#  por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#                                                                           |#
#  This program is distributed in the hope that it will be useful,          |#  Este programa se distribuye con la esperanza de que sea útil,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           |#  pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            |#  MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
#  GNU General Public License for more details.                             |#  Licencia Pública General GNU para más detalles.
#                                                                           |#
#  You should have received a copy of the GNU General Public License        |#  Deberías haber recibido una copia de la Licencia Pública General GNU
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.   |#  junto con este programa. Si no es así, consulte <https://www.gnu.org/licenses/>.
from __future__ import annotations

import inspect
from collections.abc import Iterable
from typing import Any, Callable

from PruebaIntegracion.core.ParamSpec import ParamSpec, create_param_specs


class FunctionWrapper:
    """Wraps a real function and validates its arguments before executing it."""

    def __init__(self, function: Callable[..., Any], param_specs: Iterable[ParamSpec] | None = None):
        if not callable(function):
            raise TypeError("The wrapped function must be callable.")

        self.function = function
        self.name = getattr(function, "__name__", function.__class__.__name__)
        self.signature = inspect.signature(function)
        self.param_specs = create_param_specs(param_specs or getattr(function, "_param_specs", ()))
        self._param_order = self._extract_param_order()
        self._validate_param_specs_against_signature()

    def _extract_param_order(self) -> list[str]:
        order = []
        for name, parameter in self.signature.parameters.items():
            if parameter.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            ):
                order.append(name)
        return order

    def _validate_param_specs_against_signature(self) -> None:
        formal_names = set(self._param_order)
        for spec in self.param_specs:
            if spec.name not in formal_names and spec.name != "context_keys":
                raise ValueError(
                    f"The specification '{spec.name}' does not match the signature of '{self.name}'."
                )

    def get_param_order(self) -> list[str]:
        """Returns the parameter names in the original order of the signature."""
        return list(self._param_order)

    def execute(self, *args: Any, context_keys: Iterable[str] | None = None, **kwargs: Any) -> Any:
        """Validates arguments, injects context_keys if applicable, and executes the function."""
        try:
            bound = self.signature.bind_partial(*args, **kwargs)
        except TypeError as error:
            raise TypeError(f"Invalid arguments for '{self.name}': {error}") from error

        if "context_keys" in self.signature.parameters and "context_keys" not in bound.arguments:
            bound.arguments["context_keys"] = list(context_keys or [])

        missing = self._get_missing_required_parameters(bound.arguments)
        if missing:
            missing_list = ", ".join(missing)
            raise ValueError(f"Missing required parameters for '{self.name}': {missing_list}")

        self._validate_arguments(bound.arguments)
        return self.function(*bound.args, **bound.kwargs)

    def _get_missing_required_parameters(self, arguments: dict[str, Any]) -> list[str]:
        missing: list[str] = []
        for name, parameter in self.signature.parameters.items():
            if name == "context_keys":
                continue
            if parameter.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue
            if parameter.default is inspect._empty and name not in arguments:
                missing.append(name)
        return missing

    def _validate_arguments(self, arguments: dict[str, Any]) -> None:
        param_specs_by_name = {spec.name: spec for spec in self.param_specs}

        for name, value in arguments.items():
            spec = param_specs_by_name.get(name)
            if spec is not None:
                spec.validate(value, name)

    def __repr__(self) -> str:
        return f"FunctionWrapper(name={self.name!r}, param_specs={list(self.param_specs)!r})"
