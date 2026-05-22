from __future__ import annotations

import importlib
import importlib.util
import inspect
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, Iterable

from PruebaIntegracion.core.EnvoltorioFuncion import EnvoltorioFuncion
from PruebaIntegracion.core.NodoContexto import NodoContexto


class CargadorConTraducciones:
	"""Carga la jerarquía de `dic/` a partir de módulos Python y traducciones.

	Convenciones:
	- Cada carpeta representa un `NodoContexto`.
	- Los módulos semánticos pueden exponer un diccionario raíz con el mismo
	  nombre que el archivo para modelar un diccionario de comandos.
	- Los archivos `TraduceTo*.py` pueden exponer `TRADUCCIONES` como dict.
	- Los demás `.py` se inspeccionan y solo se cargan callables con `_param_specs`.
	"""

	def __init__(self, directorio_dic: str | Path | None = None) -> None:
		self._raiz_paquete = Path(__file__).resolve().parent.parent
		if directorio_dic is not None:
			self.directorios_fuente = (Path(directorio_dic),)
		else:
			directorios: list[Path] = []
			diccionario = self._raiz_paquete / "diccionario"
			if diccionario.exists():
				directorios.append(diccionario)
			directorios.append(self._raiz_paquete / "dic")
			self.directorios_fuente = tuple(directorios)
		self.directorio_dic = self.directorios_fuente[0] if self.directorios_fuente else self._raiz_paquete / "dic"

	def cargar(self) -> Dict[str, NodoContexto]:
		roots: Dict[str, NodoContexto] = {}
		for fuente in self.directorios_fuente:
			if not fuente.exists():
				continue
			for child in sorted(fuente.iterdir(), key=lambda p: p.name.lower()):
				if child.is_dir() and not child.name.startswith("_"):
					roots[child.name] = self._cargar_directorio(child, parent=None)
				elif child.suffix.lower() == ".py" and child.name != "__init__.py" and not child.name.startswith("_"):
					nodo = self._cargar_modulo_raiz(child)
					if nodo is not None:
						roots[nodo.nombre] = nodo
		return roots

	def _cargar_directorio(self, directorio: Path, parent: NodoContexto | None) -> NodoContexto:
		nodo = NodoContexto(directorio.name, parent=parent)

		for archivo in sorted(directorio.iterdir(), key=lambda p: p.name.lower()):
			if archivo.is_dir() and not archivo.name.startswith("_"):
				subnodo = self._cargar_directorio(archivo, parent=nodo)
				nodo.agregar_subcontexto(archivo.name, subnodo)
				continue

			if archivo.suffix.lower() != ".py" or archivo.name == "__init__.py":
				continue

			if self._cargar_estructura_semantica(archivo, nodo):
				continue

			if archivo.name.lower().startswith("traduceto"):
				self._cargar_traducciones(archivo, nodo)
			else:
				self._cargar_funciones(archivo, nodo)

		return nodo

	def _cargar_modulo_raiz(self, archivo: Path) -> NodoContexto | None:
		modulo = self._importar_modulo(archivo)
		if modulo is None:
			return None

		estructura = self._extraer_estructura_semantica(modulo, archivo.stem)
		if estructura is None:
			return None

		nodo = NodoContexto(archivo.stem)
		self._cargar_desde_diccionario(nodo, estructura)
		return nodo

	def _cargar_estructura_semantica(self, archivo: Path, nodo: NodoContexto) -> bool:
		modulo = self._importar_modulo(archivo)
		if modulo is None:
			return False

		estructura = self._extraer_estructura_semantica(modulo, archivo.stem)
		if estructura is None:
			return False

		self._cargar_desde_diccionario(nodo, estructura)
		return True

	def _extraer_estructura_semantica(self, modulo: ModuleType, nombre_esperado: str) -> dict[str, Any] | None:
		candidato = getattr(modulo, nombre_esperado, None)
		if isinstance(candidato, dict):
			return candidato

		for nombre, objeto in vars(modulo).items():
			if nombre.startswith("_"):
				continue
			if isinstance(objeto, dict):
				return objeto

		return None

	def _cargar_desde_diccionario(self, nodo: NodoContexto, estructura: dict[str, Any]) -> None:
		for clave, valor in estructura.items():
			if isinstance(valor, dict):
				subnodo = NodoContexto(clave, parent=nodo)
				self._cargar_desde_diccionario(subnodo, valor)
				nodo.agregar_subcontexto(clave, subnodo)
				nodo.agregar_traduccion(clave.strip().lower(), clave)
				continue

			if isinstance(valor, EnvoltorioFuncion):
				nodo.agregar_funcion(clave, valor)
				nodo.agregar_traduccion(clave.strip().lower(), clave)
				continue

			if callable(valor):
				nodo.agregar_funcion(clave, EnvoltorioFuncion(valor))
				nodo.agregar_traduccion(clave.strip().lower(), clave)
				continue

			if isinstance(valor, str):
				nodo.agregar_traduccion(clave.strip().lower(), valor.strip())

	def _cargar_traducciones(self, archivo: Path, nodo: NodoContexto) -> None:
		modulo = self._importar_modulo(archivo)
		if modulo is None:
			return

		traducciones = getattr(modulo, "TRADUCCIONES", None)
		if isinstance(traducciones, dict):
			for palabra_hablada, nombre_real in traducciones.items():
				if isinstance(palabra_hablada, str) and isinstance(nombre_real, str):
					nodo.agregar_traduccion(palabra_hablada.strip().lower(), nombre_real.strip())

	def _cargar_funciones(self, archivo: Path, nodo: NodoContexto) -> None:
		modulo = self._importar_modulo(archivo)
		if modulo is None:
			return

		for nombre, objeto in inspect.getmembers(modulo):
			if nombre.startswith("_"):
				continue
			if callable(objeto) and hasattr(objeto, "_param_specs"):
				envoltorio = EnvoltorioFuncion(objeto)
				nodo.agregar_funcion(nombre, envoltorio)

	def _importar_modulo(self, archivo: Path) -> ModuleType | None:
		ruta_resuelta = archivo.resolve()
		try:
			relativa_paquete = ruta_resuelta.relative_to(self._raiz_paquete.resolve())
		except ValueError:
			relativa_paquete = None

		if relativa_paquete is not None:
			nombre_modulo = ".".join((self._raiz_paquete.name, *relativa_paquete.with_suffix("").parts))
			try:
				return importlib.import_module(nombre_modulo)
			except Exception:
				pass

		nombre_unico = f"PruebaIntegracion.dic_{archivo.stem}_{abs(hash(str(ruta_resuelta)))}"
		spec = importlib.util.spec_from_file_location(nombre_unico, ruta_resuelta)
		if spec is None or spec.loader is None:
			raise ImportError(f"No se pudo importar el archivo {archivo}")

		modulo = importlib.util.module_from_spec(spec)
		try:
			spec.loader.exec_module(modulo)
		except Exception:
			return None
		return modulo

