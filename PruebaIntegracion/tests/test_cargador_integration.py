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
import os
import sys
from pathlib import Path

# Ensure the repo root is in sys.path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from PruebaIntegracion.core.LoaderWithTranslations import LoaderWithTranslations
from PruebaIntegracion.core.Navigator import Navigator


def test_loader_detects_demo_and_executes_function():
    """Test that the loader detects the demo folder and executes a function within it."""
    c = LoaderWithTranslations()
    roots = c.load()
    assert 'Demo' in roots, 'Demo folder not detected in dic/'
    demo = roots['Demo']
    assert 'crear_punto' in demo.elements, 'crear_punto not loaded'

    # The Navigator receives a root ContextNode; we use the loaded Demo node.
    nav = Navigator(demo)
    result = nav.call('crear_punto', 2.5, context_keys=['Demo'])
    assert isinstance(result, dict), 'Expected result to be a dict'
    assert result.get('value') == 2.5
