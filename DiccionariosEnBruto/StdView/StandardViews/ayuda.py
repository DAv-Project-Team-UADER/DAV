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
    print("  bottom: Orienta la cámara de la vista 3D hacia la cara inferior del modelo (vista desde abajo). | Req: Una vista 3D activa en el documento.")
    print("  boxzoom: Permite realizar zoom sobre un área rectangular específica seleccionada por el usuario. | Req: Una vista 3D activa y la selección manual de un área rectangular.")
    print("  newview: Crea una nueva ventana de vista 3D independiente para el documento activo. | Req: Un documento abierto en FreeCAD.")
    print("  dimetric: Orienta la cámara a una vista dimétrica del modelo, donde dos de los tres ejes forman ángulos iguales. | Req: Una vista 3D activa en el documento.")
    print("  fitall: Ajusta el zoom y la posición de la cámara para que todos los objetos visibles de la escena entren en pantalla. | Req: Una vista 3D activa con al menos un objeto visible en el documento.")
    print("  fitselection: Ajusta el zoom y la posición de la cámara para que solo los objetos seleccionados se enfoquen en pantalla. | Req: Una vista 3D activa y al menos un objeto seleccionado en el árbol.")
    print("  front: Orienta la cámara de la vista 3D hacia la cara frontal del modelo (vista desde el frente). | Req: Una vista 3D activa en el documento.")
    print("  fullscreen: Alterna la vista 3D activa entre modo pantalla completa y modo ventana normal. | Req: Una vista 3D activa en el documento.")
    print("  home: Restablece la vista 3D a la posición de cámara predeterminada (home), ajustando la rotación y el zoom inicial. | Req: Una vista 3D activa en el documento.")
    print("  isometric: Orienta la cámara a una vista isométrica del modelo, donde los tres ejes (X, Y, Z) se ven con igual deformación. | Req: Una vista 3D activa en el documento.")
    print("  left: Orienta la cámara de la vista 3D hacia la cara izquierda del modelo (vista desde la izquierda). | Req: Una vista 3D activa en el documento.")
    print("  rear: Orienta la cámara de la vista 3D hacia la cara trasera del modelo (vista desde el revés). | Req: Una vista 3D activa en el documento.")
    print("  right: Orienta la cámara de la vista 3D hacia la cara derecha del modelo (vista desde la derecha). | Req: Una vista 3D activa en el documento.")
    print("  top: Orienta la cámara de la vista 3D hacia la cara superior del modelo (vista desde arriba). | Req: Una vista 3D activa en el documento.")
    print("  trimetric: Orienta la cámara a una vista trimétrica del modelo, donde los tres ejes tienen ángulos y escalas distintas. | Req: Una vista 3D activa en el documento.")
    print("  zoomin: Acerca la cámara en la vista 3D activa, aumentando el nivel de zoom sobre el modelo. | Req: Una vista 3D activa dentro del entorno de FreeCAD.")
    print("  zoomout: Aleja la cámara en la vista 3D activa, disminuyendo el nivel de zoom sobre el modelo. | Req: Una vista 3D activa dentro del entorno de FreeCAD.")
    print("  clearviews: Elimina todas las vistas congeladas guardadas temporalmente en la sesión actual. | Req: Al menos una vista congelada con anterioridad.")
    print("  clippingview: Recorta temporalmente los objetos mediante planos de corte configurables para inspeccionar el interior. | Req: Objetos 3D visibles en la escena.")
    print("  drawstyleasis: Restablece y mantiene el modo de visualización y estilo de dibujo original individual de cada objeto. | Req: Una vista 3D activa con objetos.")
    print("  aligntoselection: Reorienta la cámara de la vista 3D de forma perpendicular a la superficie seleccionada. | Req: Una vista 3D activa y una cara o elemento seleccionado.")