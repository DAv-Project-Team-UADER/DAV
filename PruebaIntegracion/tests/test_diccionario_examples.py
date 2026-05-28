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
def test_cargador_explorer_examples():
    from PruebaIntegracion.core.LoaderWithTranslations import LoaderWithTranslations
    from PruebaIntegracion.core.Navigator import Navegador

    c = CargadorConTraducciones()
    roots = c.cargar()
    assert 'ExplorerExamples' in roots

    nodo = roots['ExplorerExamples']
    # Debe exponer las funciones new y open
    assert 'new' in nodo.elementos
    assert 'open' in nodo.elementos

    nav = Navegador(nodo)
    # Llamar a new
    res = nav.llamar('new', 'prueba', context_keys=['ExplorerExamples'])
    assert isinstance(res, dict)
    assert res['action'] == 'new' and res['name'] == 'prueba'

    # Llamar a open
    res2 = nav.llamar('open', '/tmp/fichero', context_keys=['ExplorerExamples'])
    assert res2['action'] == 'open' and res2['path'] == '/tmp/fichero'
