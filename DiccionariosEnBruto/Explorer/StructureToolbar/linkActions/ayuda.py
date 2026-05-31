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
    print("Comandos disponibles en Link Actions:")
    print("  make link     - Crea un enlace al objeto seleccionado.")
    print("  relative link - Crea un sub-enlace relativo al subelemento seleccionado (cara, arista, vértice) dentro de un objeto, en lugar de enlazar el objeto completo.")
    print("  import link   - Importa el objeto enlazado seleccionado desde su documento externo al documento activo, convirtiendo el enlace externo en una copia local.")
    print("  import all links - Importa todos los objetos enlazados desde documentos externos al documento activo en una sola operación.")
    print("  replace link  - Reemplaza el objeto seleccionado en su contenedor padre por un enlace al mismo objeto, convirtiendo la copia directa en una referencia.")
    print("  help     - Muestra esta ayuda")