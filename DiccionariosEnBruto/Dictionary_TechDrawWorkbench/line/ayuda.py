# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

def ayuda():
    print("=== Subgrupo TechDraw: line ===")
    print("  'cosmetic'   : Traza una linea cosmetica auxiliar entre dos puntos. | Req: Dos vertices seleccionados")
    print("  'leader'     : Anade una linea de directriz indicadora con flecha. | Req: Vista de dibujo activa")
    print("  'midpoints'  : Anade puntos medios auxiliares en las aristas. | Req: Una o mas aristas seleccionadas")
    print("  'quadrants'  : Anade vertices cosmeticos en los cuadrantes. | Req: Arista circular seleccionada")
    print("  'surface'    : Inserta un simbolo normado de acabado superficial. | Req: Vista o cota seleccionada")