from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Tuple, Type


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo cargar el modulo: {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_modelo_gui() -> Tuple[Type[object], Type[object]]:
    """Carga dinamicamente la GUI de MODELO sin requerir paquete Python instalado.

    Retorna (MainWindow, VoiceCommandAdapter).
    """
    repo_root = Path(__file__).resolve().parents[1]
    gui_dir = repo_root / "MODELO" / "src" / "GUI"
    asistente_path = gui_dir / "asistente_voz.py"
    adapter_path = gui_dir / "voice_adapter.py"

    if not asistente_path.exists() or not adapter_path.exists():
        raise FileNotFoundError(
            "No se encontraron los archivos de GUI en MODELO/src/GUI."
        )

    asistente_mod = _load_module("modelo_gui_asistente", asistente_path)
    adapter_mod = _load_module("modelo_gui_adapter", adapter_path)

    return asistente_mod.MainWindow, adapter_mod.VoiceCommandAdapter
