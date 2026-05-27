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

# ayuda.py - StdView / DrawStyles

def ayuda():
    print("=== DrawStyles ===")
    print("  styleasis: Mantiene el modo de visualización original configurado individualmente para cada | Req: Una vista 3D activa con objetos visibles.")
    print("  flatlines: Muestra los objetos con superficies iluminadas y aristas visibles simultáneament | Req: Una vista 3D activa con objetos visibles.")
    print("  hiddenline: Visualiza los objetos ocultando determinadas líneas y mostrando una representaci | Req: Una vista 3D activa con objetos visibles.")
    print("  noshading: Muestra vértices, aristas y caras utilizando colores sólidos sin aplicar sombrea | Req: Una vista 3D activa con objetos visibles.")
    print("  points: Muestra los objetos únicamente mediante vértices representados como puntos sólid | Req: Una vista 3D activa con objetos visibles.")
    print("  shaded: Muestra los objetos con superficies sombreadas e iluminación basada en la orient | Req: Una vista 3D activa con objetos visibles.")
    print("  wireframe: Muestra los objetos utilizando únicamente aristas y líneas de contorno, sin visu | Req: Una vista 3D activa con objetos visibles.")
