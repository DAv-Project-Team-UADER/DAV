from __future__ import annotations

import argparse
import os
import sys
import threading
from pathlib import Path
from typing import Iterable

from PruebaIntegracion.core.CargadorConTraducciones import CargadorConTraducciones
from PruebaIntegracion.core.Comando import Command
from PruebaIntegracion.core.EnvoltorioFuncion import EnvoltorioFuncion
from PruebaIntegracion.core.ExploradorVoz import ExploradorVoz
from PruebaIntegracion.core.Navegador import Navegador
from PruebaIntegracion.core.NodoContexto import NodoContexto
from PruebaIntegracion.core.ParamSpec import ParamSpec
from PruebaIntegracion.gui_adapter import load_modelo_gui


class DemoVoiceModel:
	"""Modelo mínimo para ejecutar el flujo sin micrófono ni Vosk."""

	def __init__(self, frases: Iterable[str] | None = None, debug: bool = False) -> None:
		self._frases = list(frases or [])
		self._indice = 0
		self._debug = debug

	def escuchar_una_palabra(self) -> str:
		if self._indice < len(self._frases):
			texto = self._frases[self._indice]
			self._indice += 1
			if self._debug:
				print(f"[demo] emitir frase {self._indice}/{len(self._frases)}: {texto}")
			else:
				print(f"[demo] {texto}")
			return texto
		if self._debug:
			print("[demo] sin frases disponibles")
		return ""


def _crear_funcion_demo(nombre: str):
	def funcion_demo(valor: float, context_keys=None):
		print(f"{nombre} ejecutada con valor={valor} context_keys={context_keys}")
		return {"nombre": nombre, "valor": valor, "context_keys": context_keys}

	funcion_demo.__name__ = nombre
	funcion_demo._param_specs = (ParamSpec("valor", float),)
	return funcion_demo


def construir_raiz_principal() -> NodoContexto:
	cargador = CargadorConTraducciones()
	roots = cargador.cargar()

	if roots:
		raiz = NodoContexto("DAVCore")
		for nombre, nodo in roots.items():
			raiz.agregar_subcontexto(nombre, nodo)
		return raiz

	raiz = NodoContexto("DAVCore")
	demo = NodoContexto("Demo")
	demo.agregar_funcion("crear_punto", EnvoltorioFuncion(_crear_funcion_demo("crear_punto")))
	demo.agregar_traduccion("crear punto", "crear_punto")
	raiz.agregar_subcontexto("Demo", demo)
	raiz.agregar_traduccion("demo", "Demo")
	return raiz


def construir_modelo_de_voz(args: argparse.Namespace):
	if args.demo:
		return DemoVoiceModel(args.script or ["demo enviar", "crear punto enviar", "1"], debug=args.debug)

	ruta_modelo = Path(args.modelo)
	if not ruta_modelo.exists():
		raise FileNotFoundError(f"No se encontró el modelo de Vosk en '{ruta_modelo}'")
	from PruebaIntegracion.modelo.VoskModel import VoskModel
	return VoskModel(str(ruta_modelo), debug=args.debug)


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Arranque de PruebaIntegracion")
	parser.add_argument("--modelo", default=os.environ.get("PRUEBAINTEGRACION_MODEL_PATH", r"MODELO\vosk-model-small-es-0.42"))
	parser.add_argument("--idioma", default=os.environ.get("PRUEBAINTEGRACION_LANGUAGE", "ES"), help="Idioma base para números y comandos de control")
	parser.add_argument("--demo", action="store_true", help="Ejecuta con un modelo de voz simulado por consola")
	parser.add_argument("--gui", action="store_true", help="Usa la GUI de MODELO como fuente de voz")
	parser.add_argument("--script", nargs="*", help="Frases usadas por el modo demo, en orden")
	parser.add_argument("--max-iter", type=int, default=3, help="Límite de iteraciones del bucle principal en modo demo")
	parser.add_argument("--debug", action="store_true", help="Imprime trazas detalladas del flujo de voz")
	return parser.parse_args()


def _run_gui_loop(explorador: ExploradorVoz, debug: bool) -> None:
	if debug:
		print("[gui] iniciando bucle de explorador en hilo dedicado")
	explorador.bucle_comando()


def main() -> None:
	args = parse_args()

	if args.debug:
		print("[main] iniciando PruebaIntegracion")
		print(f"[main] demo={args.demo} modelo={args.modelo} max_iter={args.max_iter}")

	raiz = construir_raiz_principal()

	if args.debug:
		print(f"[main] raiz construida: {raiz.nombre} con hijos {list(raiz.elementos.keys())}")

	navegador = Navegador(raiz)

	print("Se ejecuto navegador con raiz:", navegador.obtener_contexto_actual().nombre)

	if args.gui:
		if args.demo and args.debug:
			print("[main] --gui ignora --demo; usando GUI como fuente de voz")
		MainWindow, VoiceCommandAdapter = load_modelo_gui()
		from PySide6.QtWidgets import QApplication

		app = QApplication(sys.argv)
		window = MainWindow()
		voice_adapter = VoiceCommandAdapter()
		window.voice_worker.final_result.connect(voice_adapter.receive_gui_phrase)
		voice_model = voice_adapter
		if args.debug:
			print("[main] voice_model=VoiceCommandAdapter (GUI)")
		command = Command(voice_model, debug=args.debug, modelo=args.modelo, idioma=args.idioma)
		explorador = ExploradorVoz(voice_model, navegador, command=command, debug=args.debug)
		threading.Thread(target=_run_gui_loop, args=(explorador, args.debug), daemon=True).start()
		window.show()
		sys.exit(app.exec())

	voice_model = construir_modelo_de_voz(args)
	if args.debug:
		print(f"[main] voice_model={voice_model.__class__.__name__}")

	command = Command(voice_model, debug=args.debug, modelo=args.modelo, idioma=args.idioma)
	explorador = ExploradorVoz(voice_model, navegador, command=command, debug=args.debug)
	if args.debug:
		print("[main] explorador inicializado, entrando al bucle")

	explorador.bucle_comando(max_iterations=args.max_iter if args.demo else None)


if __name__ == "__main__":
	main()

