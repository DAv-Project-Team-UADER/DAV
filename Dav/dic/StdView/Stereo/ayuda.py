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

# ayuda.py - StdView / Stereo

def ayuda():
    print("=== Stereo ===")
    print("  camerapos: Obtiene e imprime la configuración actual de la cámara de la vista 3D activa en  | Req: Una vista 3D activa dentro del entorno de FreeCAD.")
    print("  stereocolumns: Cambia la vista 3D activa al modo estéreo por columnas intercaladas, permitiendo | Req: Una vista 3D activa, hardware gráfico compatible, un monitor")
    print("  stereorows: Cambia la vista 3D activa al modo estéreo por filas intercaladas, permitiendo ge | Req: Una vista 3D activa, hardware gráfico compatible, un monitor")
    print("  stereooff: Desactiva cualquier modo de visualización estéreo activo en la vista 3D y restau | Req: Una vista 3D activa con algún modo estéreo habilitado.")
    print("  stereoquad: Cambia la vista 3D activa al modo estéreo Quad Buffer, permitiendo visualización | Req: Una vista 3D activa, una tarjeta gráfica compatible con Quad")
    print("  stereoanaglyph: Cambia la vista 3D activa al modo estéreo anaglifo rojo/cian, permitiendo visual | Req: Una vista 3D activa y el uso de gafas estéreo rojo/cian para")
