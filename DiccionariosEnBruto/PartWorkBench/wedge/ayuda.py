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
    print('  cuna / primitive wedge - Crea una cuña sólida paramétrica (Part::Wedge).')
    print('         Requiere: Xmin, Ymin, Zmin (float) — vértice inferior de la cara frontal.')
    print('                   Xmax, Ymax, Zmax (float) — vértice superior de la cara trasera.')
    print('                   X2min, Z2min     (float) — vértice inferior de la cara trasera.')
    print('                   X2max, Z2max     (float) — vértice superior de la cara trasera.')
    print('         Nota: Es el primitivo más complejo de configurar.')
    print('               Si la cara trasera es un punto o una arista, se obtienen formas piramidales o de cuña pura.')
    print('               Disponible desde Part -> Primitives.')
