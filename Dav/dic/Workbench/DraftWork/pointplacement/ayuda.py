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
    print("=== Point Placement ===")
    print("clave  |  requerimientos")
    print("addpoint: Coloca un punto en el vértice actual del objeto seleccionado | req: un objeto seleccionado con un vértice seleccionado o con vértices")
    print("pointatvertex: Coloca un punto en un vértice específico por índice | req: index (int/índice de vértice)")
    print("midpoint: Coloca un punto en el punto medio de una arista | req: edge_index (int/índice de arista, por defecto 0)")
    print("pointatcoords: Coloca un punto en coordenadas absolutas X,Y,Z | req: x (float/coord X), y (float/coord Y), z (float/coord Z)")
