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

# ayuda.py - StdView / Appearance

def ayuda():
    print("=== Appearance ===")
    print("  align: Reorienta la cámara de la vista 3D para que quede alineada perpendicularmente a  | Req: Una vista 3D activa y una cara, arista o elemento selecciona")
    print("  appearance: Establece las propiedades de visualización (color, brillo, transparencia) de los | Req: Objetos seleccionados.")
    print("  partfacecolors: Establece las propiedades de visualización de caras individuales de un objeto, n | Req: Que el Workbench Part o PartDesign esté activo y haya un obj")
    print("  toggleclipplane: Recorta temporalmente los objetos en la vista 3D utilizando planos de corte. | Req: Objetos 3D visibles en la escena.")
    print("  setmaterial: Establece el material físico/visual de los objetos seleccionados. | Req: Objetos seleccionados y que el Workbench de Material (o Part")
    print("  randomcolor: Aplica un color difuso aleatorio a los objetos seleccionados. | Req: Objetos seleccionados.")
    print("  texture: Mapea temporalmente una textura sobre todos los objetos de la vista 3D. | Req: Objetos 3D visibles en la escena.")
