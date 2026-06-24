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

import argparse
import os
import sys
import threading
from pathlib import Path
from typing import Iterable

from PruebaIntegracion.core.LoaderWithTranslations import LoaderWithTranslations
from PruebaIntegracion.core.Command import Command
from PruebaIntegracion.core.FunctionWrapper import FunctionWrapper
from PruebaIntegracion.core.VoiceExplorer import VoiceExplorer
from PruebaIntegracion.core.Navigator import Navigator
from PruebaIntegracion.core.ContextNode import ContextNode
from PruebaIntegracion.core.ParamSpec import ParamSpec
from PruebaIntegracion.gui_adapter import load_modelo_gui


class DemoVoiceModel:
    """Minimal model to run the flow without a microphone or Vosk."""

    def __init__(self, phrases: Iterable[str] | None = None, debug: bool = False) -> None:
        self._phrases = list(phrases or [])
        self._index = 0
        self._debug = debug

    def listen_for_one_word(self) -> str:
        if self._index < len(self._phrases):
            text = self._phrases[self._index]
            self._index += 1
            if self._debug:
                print(f"[demo] emit phrase {self._index}/{len(self._phrases)}: {text}")
            else:
                print(f"[demo] {text}")
            return text
        if self._debug:
            print("[demo] no phrases available")
        return ""


def _create_demo_function(name: str):
    def demo_function(value: float, context_keys=None):
        print(f"{name} executed with value={value} context_keys={context_keys}")
        return {"name": name, "value": value, "context_keys": context_keys}

    demo_function.__name__ = name
    demo_function._param_specs = (ParamSpec("value", float),)
    return demo_function


def build_main_root() -> ContextNode:
    loader = LoaderWithTranslations()
    roots = loader.load()

    if roots:
        root = ContextNode("DAVCore")
        for name, node in roots.items():
            root.add_subcontext(name, node)
        return root

    root = ContextNode("DAVCore")
    demo = ContextNode("Demo")
    demo.add_function("crear_punto", FunctionWrapper(_create_demo_function("crear_punto")))
    demo.add_translation("crear punto", "crear_punto")
    root.add_subcontext("Demo", demo)
    root.add_translation("demo", "Demo")
    return root


def build_voice_model(args: argparse.Namespace):
    if args.demo:
        return DemoVoiceModel(args.script or ["demo send", "crear punto send", "1"], debug=args.debug)

    model_path = Path(args.model)
    if not model_path.exists():
        raise FileNotFoundError(f"Vosk model not found at '{model_path}'")
    from PruebaIntegracion.modelo.VoskModel import VoskModel
    return VoskModel(str(model_path), debug=args.debug)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PruebaIntegracion startup")
    parser.add_argument("--model", default=os.environ.get("PRUEBAINTEGRACION_MODEL_PATH", r"MODELO\vosk-model-small-es-0.42"))
    parser.add_argument("--language", default=os.environ.get("PRUEBAINTEGRACION_LANGUAGE", "ES"), help="Base language for numbers and control commands")
    parser.add_argument("--demo", action="store_true", help="Run with a simulated console voice model")
    parser.add_argument("--gui", action="store_true", help="Use the GUI model as the voice source")
    parser.add_argument("--script", nargs="*", help="Phrases used by demo mode, in order")
    parser.add_argument("--max-iter", type=int, default=3, help="Maximum loop iterations in demo mode")
    parser.add_argument("--debug", action="store_true", help="Print detailed voice flow traces")
    return parser.parse_args()


def _run_gui_loop(explorer: VoiceExplorer, debug: bool) -> None:
    if debug:
        print("[gui] starting explorer loop in dedicated thread")
    explorer.command_loop()


def main() -> None:
    args = parse_args()

    if args.debug:
        print("[main] starting PruebaIntegracion")
        print(f"[main] demo={args.demo} model={args.model} max_iter={args.max_iter}")

    root = build_main_root()

    if args.debug:
        print(f"[main] root built: {root.name} with children {list(root.elements.keys())}")

    navigator = Navigator(root)

    print("Navigator created with root:", navigator.get_current_context().name)

    if args.gui:
        if args.demo and args.debug:
            print("[main] --gui overrides --demo; using GUI as voice source")
        MainWindow, VoiceCommandAdapter = load_modelo_gui()
        from PySide6.QtWidgets import QApplication

        app = QApplication(sys.argv)
        window = MainWindow()
        voice_adapter = VoiceCommandAdapter()
        window.voice_worker.final_result.connect(voice_adapter.receive_gui_phrase)
        voice_model = voice_adapter
        if args.debug:
            print("[main] voice_model=VoiceCommandAdapter (GUI)")
        command = Command(voice_model, debug=args.debug, model=args.model, language=args.language)
        explorer = VoiceExplorer(voice_model, navigator, command=command, debug=args.debug)
        threading.Thread(target=_run_gui_loop, args=(explorer, args.debug), daemon=True).start()
        window.show()
        sys.exit(app.exec())

    voice_model = build_voice_model(args)
    if args.debug:
        print(f"[main] voice_model={voice_model.__class__.__name__}")

    command = Command(voice_model, debug=args.debug, model=args.model, language=args.language)
    explorer = VoiceExplorer(voice_model, navigator, command=command, debug=args.debug)
    if args.debug:
        print("[main] explorer initialized, entering loop")

    explorer.command_loop(max_iterations=args.max_iter if args.demo else None)


if __name__ == "__main__":
    main()