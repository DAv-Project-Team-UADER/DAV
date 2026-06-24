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

from dataclasses import dataclass, field
from typing import Any, Iterable


@dataclass(slots=True)
class ParamSpec:
    """Specification of a parameter expected by a function."""

    name: str
    param_type: type | tuple[type, ...] | None = None
    required: bool = True
    max_length: int | None = None
    allowed_values: tuple[Any, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.name or not isinstance(self.name, str):
            raise ValueError("The parameter name must be a non-empty string.")

        if self.max_length is not None and self.max_length < 0:
            raise ValueError("Maximum length cannot be negative.")

        if not isinstance(self.allowed_values, tuple):
            self.allowed_values = tuple(self.allowed_values)

    def validate(self, value: Any, argument_name: str | None = None) -> Any:
        """Validates a value and returns it if it meets the rules."""
        label = argument_name or self.name

        if value is None:
            if self.required:
                raise ValueError(f"The parameter '{label}' is required.")
            return None

        if self.param_type is not None and not isinstance(value, self.param_type):
            expected_types = self._format_expected_type()
            raise TypeError(
                f"The parameter '{label}' must be of type {expected_types}, "
                f"but received {type(value).__name__}."
            )

        if isinstance(value, str) and self.max_length is not None:
            if len(value) > self.max_length:
                raise ValueError(
                    f"The parameter '{label}' exceeds the maximum length of {self.max_length}."
                )

        if self.allowed_values and value not in self.allowed_values:
            allowed = ", ".join(repr(item) for item in self.allowed_values)
            raise ValueError(
                f"The parameter '{label}' must be one of: {allowed}."
            )

        return value

    def _format_expected_type(self) -> str:
        if self.param_type is None:
            return "any type"
        if isinstance(self.param_type, tuple):
            return ", ".join(t.__name__ for t in self.param_type)
        return self.param_type.__name__


def create_param_specs(parameters: Iterable[ParamSpec]) -> tuple[ParamSpec, ...]:
    """Converts a collection of specifications into an immutable tuple."""
    return tuple(parameters)
