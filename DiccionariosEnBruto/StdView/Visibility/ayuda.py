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

# ayuda.py - StdView / Visibility

def ayuda():
    print("=== Visibility ===")
    print("  hideobjects: Oculta todos los objetos del documento activo. | Req: Un documento activo con objetos.")
    print("  hide: Oculta los objetos que están actualmente seleccionados. | Req: Tener objetos seleccionados y visibles.")
    print("  alllinks: Selecciona todos los objetos de tipo Link que apuntan al objeto actualmente sele | Req: Un objeto seleccionado que sea referenciado por uno o más Li")
    print("  linked: Selecciona el objeto vinculado (linked object) al que apunta el Link actualmente | Req: Un objeto de tipo App::Link seleccionado en la vista de árbo")
    print("  linkedfinal: Selecciona el objeto vinculado más profundo en una cadena de Links, es decir, el | Req: Un objeto de tipo App::Link seleccionado (puede ser un link ")
    print("  selback: Restaura la selección anterior en el historial de navegación de links, equivalen | Req: Haber navegado previamente entre documentos o links usando l")
    print("  boundingbox: Activa o desactiva el modo global de resaltado mediante bounding box para los ob | Req: Una vista 3D activa con objetos seleccionables.")
    print("  selforward: Avanza al siguiente elemento en el historial de navegación de links, equivalente | Req: Haber retrocedido previamente en el historial de navegación ")
    print("  selectvisible: Selecciona todos los objetos que están actualmente visibles en la vista 3D. | Req: Que haya objetos visibles en el documento activo.")
    print("  showobjects: Hace visibles todos los objetos del documento activo. | Req: Un documento activo con objetos (ocultos o visibles).")
    print("  show: Muestra los objetos que están actualmente seleccionados. | Req: Tener objetos seleccionados (incluso si están ocultos en la ")
    print("  toggleall: Alterna la visibilidad de todos los objetos en el documento. | Req: Un documento activo con objetos.")
    print("  selectability: Alterna la capacidad de selección (selectability) de los objetos elegidos. | Req: Objetos seleccionados en el árbol.")
    print("  transparency: Alterna la transparencia de los objetos seleccionados. | Req: Objetos seleccionados.")
    print("  toggle: Alterna la visibilidad de los objetos seleccionados. | Req: Tener uno o más objetos seleccionados en el árbol o en la vi")
