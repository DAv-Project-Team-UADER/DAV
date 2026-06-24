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

# ayuda.py - StdView / Overlay

def ayuda():
    print("=== Overlay ===")
    print("  overlaybottom: Alterna el modo overlay para todos los paneles acoplados en la parte inferior de | Req: Al menos un panel acoplado en la parte inferior de la interf")
    print("  overlayfloat: Alterna el modo flotante del panel overlay activo, permitiendo que se mueva libr | Req: Al menos un panel en modo overlay activo.")
    print("  overlayleft: Alterna el modo overlay para todos los paneles acoplados en el lado izquierdo de | Req: Al menos un panel acoplado en el lateral izquierdo de la int")
    print("  overlayright: Alterna el modo overlay para todos los paneles acoplados en el lado derecho de l | Req: Al menos un panel acoplado en el lateral derecho de la inter")
    print("  axiscross: Alterna la visualización de la cruz de ejes (X, Y, Z) en la vista 3D. | Req: Que haya una vista 3D activa.")
    print("  togglenavigation: Alterna entre el modo de navegación (para mover la cámara) y el modo de edición. | Req: Estar dentro de un entorno que soporte modo de edición.")
    print("  overlay: Alterna el modo overlay (transparente/superpuesto) de todos los paneles acoplabl | Req: Al menos un panel acoplable visible (Model, Tasks, Propertie")
