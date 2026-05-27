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

# ayuda.py - StdView / StandardViews

def ayuda():
    print("=== StandardViews ===")
    print("  bottom: Orienta la cámara de la vista 3D hacia la cara inferior del modelo (vista desde  | Req: Una vista 3D activa en el documento.")
    print("  boxzoom: Permite realizar zoom sobre un área rectangular específica seleccionada por el u | Req: Una vista 3D activa y la selección manual de un área rectang")
    print("  newview: Crea una nueva ventana de vista 3D independiente para el documento activo. | Req: Un documento abierto en FreeCAD.")
    print("  dimetric: Orienta la cámara a una vista dimétrica del modelo, donde dos de los tres ejes f | Req: Una vista 3D activa en el documento.")
    print("  fitall: Ajusta el zoom y la posición de la cámara para que todos los objetos visibles de | Req: Una vista 3D activa con al menos un objeto visible en el doc")
    print("  fitselection: Ajusta el zoom y la posición de la cámara para que solo los objetos seleccionado | Req: Una vista 3D activa y al menos un objeto seleccionado en el ")
    print("  front: Orienta la cámara de la vista 3D hacia la cara frontal del modelo (vista desde e | Req: Una vista 3D activa en el documento.")
    print("  fullscreen: Alterna la vista 3D activa entre modo pantalla completa y modo ventana normal. | Req: Una vista 3D activa en el documento.")
    print("  home: Restablece la vista 3D a la posición de cámara predeterminada (home), ajustando  | Req: Una vista 3D activa en el documento.")
    print("  isometric: Orienta la cámara a una vista isométrica del modelo, donde los tres ejes (X, Y,  | Req: Una vista 3D activa en el documento.")
    print("  left: Orienta la cámara de la vista 3D hacia la cara izquierda del modelo (vista desde | Req: Una vista 3D activa en el documento.")
    print("  rear: Orienta la cámara de la vista 3D hacia la cara trasera del modelo (vista desde e | Req: Una vista 3D activa en el documento.")
    print("  right: Orienta la cámara de la vista 3D hacia la cara derecha del modelo (vista desde e | Req: Una vista 3D activa en el documento.")
    print("  top: Orienta la cámara de la vista 3D hacia la cara superior del modelo (vista desde  | Req: Una vista 3D activa en el documento.")
    print("  trimetric: Orienta la cámara a una vista trimétrica del modelo, donde los tres ejes tienen  | Req: Una vista 3D activa en el documento.")
    print("  zoomin: Acerca la cámara en la vista 3D activa, aumentando el nivel de zoom sobre el mod | Req: Una vista 3D activa dentro del entorno de FreeCAD.")
    print("  zoomout: Aleja la cámara en la vista 3D activa, disminuyendo el nivel de zoom sobre el mo | Req: Una vista 3D activa dentro del entorno de FreeCAD.")
