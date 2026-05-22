from __future__ import annotations

from typing import Optional, Tuple, Any

from PruebaIntegracion.core.NodoContexto import NodoContexto
from PruebaIntegracion.core.EnvoltorioFuncion import EnvoltorioFuncion


class Navegador:
	"""Gestiona el contexto actual y la búsqueda de funciones en la jerarquía."""

	def __init__(self, raiz: NodoContexto):
		if not isinstance(raiz, NodoContexto):
			raise TypeError("La raíz debe ser un NodoContexto")
		self.raiz = raiz
		self.contexto_actual: NodoContexto = raiz

	def establecer_contexto(self, nodo: NodoContexto) -> None:
		"""Establece `contexto_actual` a `nodo` (debe pertenecer al árbol)."""
		self.contexto_actual = nodo

	def navegar(self, ruta: str) -> Optional[NodoContexto]:
		"""Navega por una ruta separada por '-' (ej: 'Dibujo-Geometria').
		Si la ruta es válida devuelve el nodo final, sino None.
		"""
		partes = [p.strip() for p in ruta.split("-") if p.strip()]
		nodo = self.contexto_actual
		for parte in partes:
			hijo = nodo.obtener_hijo(parte)
			if hijo is None:
				return None
			nodo = hijo
		self.contexto_actual = nodo
		return nodo

	def buscar_funcion_ascendente(self, nombre_real: str) -> Optional[Tuple[NodoContexto, EnvoltorioFuncion]]:
		"""Busca `nombre_real` empezando en `contexto_actual` y subiendo a la raíz.
		Retorna una tupla (nodo_encontrado, envoltorio) o None si no existe.
		"""
		nodo = self.contexto_actual
		while nodo is not None:
			val = nodo.elementos.get(nombre_real)
			if isinstance(val, EnvoltorioFuncion):
				return nodo, val
			nodo = nodo.parent
		return None

	def llamar(self, nombre_real: str, *args: Any, context_keys: Optional[list[str]] = None, **kwargs: Any) -> Any:
		"""Busca y ejecuta la función `nombre_real`. Actualiza el contexto al nodo donde se encontró."""
		encontrado = self.buscar_funcion_ascendente(nombre_real)
		if not encontrado:
			raise LookupError(f"Funcion '{nombre_real}' no encontrada desde el contexto actual.")
		nodo, envoltorio = encontrado
		# Actualizamos el contexto al nodo donde se encontró la función
		self.contexto_actual = nodo
		return envoltorio.ejecutar(*args, context_keys=context_keys, **kwargs)

	def obtener_contexto_actual(self) -> NodoContexto:
		return self.contexto_actual

	def __repr__(self) -> str:
		return f"Navegador(contexto_actual={self.contexto_actual.nombre!r})"

