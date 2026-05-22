from __future__ import annotations

from typing import Any, Dict, Optional, Iterable

from PruebaIntegracion.core.EnvoltorioFuncion import EnvoltorioFuncion


class NodoContexto:
	"""Nodo en la jerarquía de herramientas.

	- `elementos` mapea nombres reales -> EnvoltorioFuncion o NodoContexto
	- `traducciones` mapea palabra_hablada -> nombre_real
	- `parent` referencia al nodo padre (o None si es raíz)
	"""

	def __init__(self, nombre: str, parent: Optional[NodoContexto] = None):
		self.nombre = nombre
		self.parent = parent
		self.elementos: Dict[str, Any] = {}
		self.traducciones: Dict[str, str] = {}

	def agregar_funcion(self, clave: str, envoltorio: EnvoltorioFuncion) -> None:
		"""Agrega una función envuelta al nodo bajo la clave `clave`."""
		self.elementos[clave] = envoltorio

	def agregar_subcontexto(self, clave: str, nodo: "NodoContexto") -> None:
		"""Agrega un subcontexto (otro NodoContexto)."""
		nodo.parent = self
		self.elementos[clave] = nodo

	def agregar_traduccion(self, palabra_hablada: str, nombre_real: str) -> None:
		"""Añade una traducción local de palabra hablada -> nombre real."""
		self.traducciones[palabra_hablada] = nombre_real

	def obtener_nombre_real(self, palabra_hablada: str) -> Optional[str]:
		"""Busca la traducción en este nodo; si no existe devuelve None."""
		return self.traducciones.get(palabra_hablada)

	def obtener_todas_las_llaves(self) -> Iterable[str]:
		"""Devuelve todas las claves reales disponibles en este nodo (no traducciones)."""
		yield from self.elementos.keys()

	def obtener_hijo(self, clave: str) -> Optional["NodoContexto"]:
		"""Si `clave` corresponde a un subcontexto devuelve el NodoContexto, sino None."""
		val = self.elementos.get(clave)
		if isinstance(val, NodoContexto):
			return val
		return None

	def __repr__(self) -> str:
		return f"NodoContexto({self.nombre!r}, elementos={list(self.elementos.keys())})"

