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

# ayuda.py - StdView / Panels

def ayuda():
    print("=== Panels ===")
    print("  panel: Muestra u oculta el panel acoplado activo, permitiendo gestionar la visibilidad  | Req: Un documento activo con al menos una vista de panel disponib")
    print("  dock: Acopla una vista 3D en la interfaz principal de FreeCAD. | Req: Que haya una vista 3D abierta y actualmente desacoplada.")
    print("  fullscreen: Alterna el modo de pantalla completa para una vista 3D. | Req: Que haya una vista 3D activa.")
    print("  undock: Desacopla una vista 3D de la interfaz principal de FreeCAD. | Req: Que haya una vista 3D activa y acoplada.")
    print("  dagview: Alterna la visibilidad de la vista de Grafo Acíclico Dirigido (DAG), que muestra | Req: FreeCAD abierto (Nota: este panel no está disponible o activ")
    print("  comboview: Alterna la visibilidad del panel 'Model', que combina la Vista de Árbol y la Vis | Req: FreeCAD abierto y configurado con el modo Tree/Property View")
    print("  selectionview: Alterna la visibilidad del panel de Vista de Selección, que lista los nombres ex | Req: FreeCAD abierto.")
    print("  tasks: Alterna la visibilidad del panel de Tareas, el cual muestra diálogos y opciones  | Req: FreeCAD abierto.")
    print("  properties: Alterna la visibilidad del panel de Vista de Propiedades, donde se editan los da | Req: FreeCAD abierto. Disponible como panel separado si el modo e")
    print("  console: Alterna la visibilidad de la Consola de Python integrada. | Req: FreeCAD abierto.")
    print("  report: Alterna la visibilidad de la Vista de Informe, donde FreeCAD imprime advertencia | Req: FreeCAD abierto.")
    print("  treeview: Alterna la visibilidad del panel de Vista de Árbol, que muestra la jerarquía de  | Req: FreeCAD abierto. Disponible como panel separado si el modo e")
    print("  statusbar: Alterna la visibilidad de la barra de estado en la parte inferior de la ventana  | Req: La ventana principal de FreeCAD abierta.")
    print("  appearance: Abre el panel de propiedades de apariencia gráfica (color, transparencia). | Req: Objetos seleccionados en el árbol.")
    print("  faceappearance: Abre el panel para cambiar el color de caras de forma independiente. | Req: Workbench Part o PartDesign activo y un objeto seleccionado.")