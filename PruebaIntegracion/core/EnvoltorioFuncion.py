from __future__ import annotations

import inspect
from collections.abc import Iterable
from typing import Any, Callable

from PruebaIntegracion.core.ParamSpec import ParamSpec, crear_param_specs


class EnvoltorioFuncion:
	"""Envuelve una funcion real y valida sus argumentos antes de ejecutarla."""

	def __init__(self, funcion: Callable[..., Any], param_specs: Iterable[ParamSpec] | None = None):
		if not callable(funcion):
			raise TypeError("La funcion envuelta debe ser callable.")

		self.funcion = funcion
		self.nombre = getattr(funcion, "__name__", funcion.__class__.__name__)
		self.firma = inspect.signature(funcion)
		self.param_specs = crear_param_specs(param_specs or getattr(funcion, "_param_specs", ()))
		self._orden_parametros = self._extraer_orden_parametros()
		self._validar_param_specs_contra_firma()

	def _extraer_orden_parametros(self) -> list[str]:
		orden = []
		for nombre, parametro in self.firma.parameters.items():
			if parametro.kind in (
				inspect.Parameter.POSITIONAL_ONLY,
				inspect.Parameter.POSITIONAL_OR_KEYWORD,
				inspect.Parameter.KEYWORD_ONLY,
			):
				orden.append(nombre)
		return orden

	def _validar_param_specs_contra_firma(self) -> None:
		nombres_formales = set(self._orden_parametros)
		for spec in self.param_specs:
			if spec.nombre not in nombres_formales and spec.nombre != "context_keys":
				raise ValueError(
					f"La especificacion '{spec.nombre}' no coincide con la firma de '{self.nombre}'."
				)

	def obtener_orden_parametros(self) -> list[str]:
		"""Devuelve los nombres de parametros en el orden original de la firma."""
		return list(self._orden_parametros)

	def ejecutar(self, *args: Any, context_keys: Iterable[str] | None = None, **kwargs: Any) -> Any:
		"""Valida argumentos, inyecta context_keys si aplica y ejecuta la funcion."""
		try:
			bound = self.firma.bind_partial(*args, **kwargs)
		except TypeError as error:
			raise TypeError(f"Argumentos invalidos para '{self.nombre}': {error}") from error

		if "context_keys" in self.firma.parameters and "context_keys" not in bound.arguments:
			bound.arguments["context_keys"] = list(context_keys or [])

		faltantes = self._obtener_parametros_requeridos_faltantes(bound.arguments)
		if faltantes:
			lista = ", ".join(faltantes)
			raise ValueError(f"Faltan parametros requeridos para '{self.nombre}': {lista}")

		self._validar_argumentos(bound.arguments)
		return self.funcion(*bound.args, **bound.kwargs)

	def _obtener_parametros_requeridos_faltantes(self, argumentos: dict[str, Any]) -> list[str]:
		faltantes: list[str] = []
		for nombre, parametro in self.firma.parameters.items():
			if nombre == "context_keys":
				continue
			if parametro.kind in (
				inspect.Parameter.VAR_POSITIONAL,
				inspect.Parameter.VAR_KEYWORD,
			):
				continue
			if parametro.default is inspect._empty and nombre not in argumentos:
				faltantes.append(nombre)
		return faltantes

	def _validar_argumentos(self, argumentos: dict[str, Any]) -> None:
		param_specs_por_nombre = {spec.nombre: spec for spec in self.param_specs}

		for nombre, valor in argumentos.items():
			spec = param_specs_por_nombre.get(nombre)
			if spec is not None:
				spec.validar(valor, nombre)

	def __repr__(self) -> str:
		return f"EnvoltorioFuncion(nombre={self.nombre!r}, param_specs={list(self.param_specs)!r})"
