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

# ayuda.py - StdView / SavedViews

def ayuda():
    print("=== SavedViews ===")
    print("  clearviews: Elimina todas las frozen views almacenadas en la sesión actual de FreeCAD. | Req: Al menos una frozen view guardada previamente con Std_Freeze")
    print("  freeze: Guarda la configuración actual de la cámara de la vista 3D activa como una froze | Req: Una vista 3D activa dentro del entorno de FreeCAD.")
    print("  freezeviewsrestore: Carga frozen views previamente almacenadas en un archivo .cam, reemplazando las  | Req: Un archivo válido con extensión .cam que contenga frozen vie")
    print("  recallview: Recupera y restaura la configuración previamente almacenada de la cámara de la v | Req: Una vista 3D activa que tenga almacenada previamente una wor")
    print("  restoreview: Restaura una frozen view previamente almacenada, recuperando la orientación y co | Req: Al menos una frozen view guardada previamente con Std_Freeze")
    print("  freezeviewssave: Guarda todas las frozen views existentes en un archivo con extensión .cam para p | Req: Debe existir al menos una frozen view creada previamente med")
    print("  storeview: Guarda temporalmente la configuración actual de la cámara de la vista 3D activa, | Req: Una vista 3D activa dentro del entorno de FreeCAD. No requie")
