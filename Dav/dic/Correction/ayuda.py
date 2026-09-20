# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.


def ayuda():
    """Print the correction commands available from any context."""
    print('Correcciones (se pueden decir desde cualquier contexto):')
    print('  deshacer        - Deshace el último cambio')
    print('  rehacer         - Rehace lo deshecho')
    print('  borrar ultimo   - Borra el último objeto creado (pide confirmación)')
    print('  borrar objeto   - Elegís un objeto de la lista y lo borra (pide confirmación)')
    print('  borrar rotos    - Borra todos los objetos que fallaron al recalcular (pide confirmación)')
