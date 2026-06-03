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
    print("=== Context ===")
    print("clave  |  requerimientos")
    print("move: Mueve un objeto (como una operación o un croquis) desde su Cuerpo actual hacia otro Cuerpo distinto dentro del mismo documento.  |  req: Tener seleccionado el objeto que se desea mover en el árbol de tareas y que existan al menos dos Cuerpos (Bodies) en el archivo.")
    print("moveintree: Permite reordenar objetos (croquis, geometría de referencia o operaciones) dentro de un Cuerpo (Body)  |  req: Tener seleccionado en el árbol (Tree View) el objeto o los objetos que se desean mover.")
    print("movetip: Define una operación específica como la "Punta" (Tip) del Cuerpo (Body). Esto determina qué parte del historial de diseño es la activa y se muestra en la vista 3D.  |  req: Tener seleccionada una operación (como un Pad, Pocket o Fillet) dentro del árbol de un Cuerpo (Body) activo.")