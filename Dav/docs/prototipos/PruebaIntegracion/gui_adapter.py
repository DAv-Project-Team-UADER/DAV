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
