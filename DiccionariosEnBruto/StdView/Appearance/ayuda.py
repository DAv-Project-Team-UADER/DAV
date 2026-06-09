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
    print("=== Subgrupo StdView: Appearance ===")
    print("  'appearance'     : Cambia propiedades visuales (color, transparencia) del objeto. | Req: Objeto seleccionado")
    print("  'facecolors'     : Establece propiedades de visualización en caras individuales. | Req: Cara seleccionada")
    print("  'randomcolor'    : Asigna un color aleatorio a los objetos seleccionados. | Req: Objeto seleccionado")
    print("  'texturemapping' : Abre el diálogo de mapeo de texturas para aplicar una imagen al objeto. | Req: Objeto seleccionado con geometría de cara")