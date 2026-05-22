from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


@dataclass(slots=True)
class ParamSpec:
	"""Especificacion de un parametro esperado por una funcion."""

	nombre: str
	tipo: type | tuple[type, ...] | None = None
	requerido: bool = True
	longitud_maxima: int | None = None
	valores_permitidos: tuple[Any, ...] = field(default_factory=tuple)

	def __post_init__(self) -> None:
		if not self.nombre or not isinstance(self.nombre, str):
			raise ValueError("El nombre del parametro debe ser una cadena no vacia.")

		if self.longitud_maxima is not None and self.longitud_maxima < 0:
			raise ValueError("La longitud maxima no puede ser negativa.")

		if not isinstance(self.valores_permitidos, tuple):
			self.valores_permitidos = tuple(self.valores_permitidos)

	def validar(self, valor: Any, nombre_argumento: str | None = None) -> Any:
		"""Valida un valor y devuelve el mismo valor si cumple las reglas."""
		etiqueta = nombre_argumento or self.nombre

		if valor is None:
			if self.requerido:
				raise ValueError(f"El parametro '{etiqueta}' es obligatorio.")
			return None

		if self.tipo is not None and not isinstance(valor, self.tipo):
			tipos_esperados = self._formatear_tipo_esperado()
			raise TypeError(
				f"El parametro '{etiqueta}' debe ser de tipo {tipos_esperados}, "
				f"pero recibio {type(valor).__name__}."
			)

		if isinstance(valor, str) and self.longitud_maxima is not None:
			if len(valor) > self.longitud_maxima:
				raise ValueError(
					f"El parametro '{etiqueta}' excede la longitud maxima de {self.longitud_maxima}."
				)

		if self.valores_permitidos and valor not in self.valores_permitidos:
			permitidos = ", ".join(repr(item) for item in self.valores_permitidos)
			raise ValueError(
				f"El parametro '{etiqueta}' debe ser uno de: {permitidos}."
			)

		return valor

	def _formatear_tipo_esperado(self) -> str:
		if self.tipo is None:
			return "cualquier tipo"
		if isinstance(self.tipo, tuple):
			return ", ".join(t.__name__ for t in self.tipo)
		return self.tipo.__name__


def crear_param_specs(parametros: Iterable[ParamSpec]) -> tuple[ParamSpec, ...]:
	"""Convierte una coleccion de especificaciones en una tupla inmutable."""
	return tuple(parametros)
