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
    print("=== Array ===")
    print("clave  |  requerimientos")
    print("polar: crea una matriz polar distribuyendo copias de un objeto alrededor de un centro.  |  req: OBJ, number, number, vector[], bool")
    print("orthogonal: crea una matriz ortogonal de copias de un objeto en los ejes X, Y y Z.  |  req: OBJ, vector[], vector[], vector[], number, number, number, bool")
    print("path: distribuye copias de un objeto a lo largo de una trayectoria o curva.  |  req: OBJ, OBJ, number, vector[], [], bool, string, vector[], bool, vector[], bool")
    print("pathlink: distribuye enlaces de un objeto a lo largo de una trayectoria o curva.  |  req: OBJ, OBJ, number, vector[], [], bool, string, vector[], bool, vector[], bool")
    print("point: Distribuye copias de un objeto en posiciones definidas por puntos  |  req: OBJ, OBJ, [], bool")
    print("pointlink: Distribuye enlaces de un objeto en las posiciones definidas por un conjunto de puntos  |  req: OBJ, OBJ, [], bool")