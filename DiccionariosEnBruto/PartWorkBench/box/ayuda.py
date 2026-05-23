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
    print('  box - Crea una caja rectangular paramétrica (Part::Box) con dimensiones por defecto 10x10x10.')
    print('         Requiere: Length (float) — longitud en X.')
    print('                   Width  (float) — anchura en Y.')
    print('                   Height (float) — altura en Z.')
    print('         Nota: Equivalente al Cube de la barra Solids; accesible también desde el panel Primitives.')
    print('         El objeto creado es editable desde el panel de propiedades de FreeCAD.')