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
    print('Comandos disponibles en este nivel:')
    print('  cube - Crea una caja solida rectangular parametrica (Part::Box) con dimensiones por defecto 10x10x10.')
    print('         Requiere: Length (float) — longitud en X. Default: 10 mm.')
    print('                   Width  (float) — anchura en Y. Default: 10 mm.')
    print('                   Height (float) — altura en Z. Default: 10 mm.')
    print('         Nota: El objeto subyacente es Part::Box.')
    print('               Disponible desde Part -> Primitives -> Cube.')