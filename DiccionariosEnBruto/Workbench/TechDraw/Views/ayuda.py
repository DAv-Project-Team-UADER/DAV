# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

def ayuda():
    print("=== Subgrupo TechDraw: Views ===")
    print("  'view'           : Crea una vista 2D estándar a partir de un objeto 3D. | Req: Objeto 3D seleccionado y página activa")
    print("  'detailView'     : Amplía una zona específica o región de la vista. | Req: Vista activa y región seleccionada")
    print("  'brokenView'     : Acorta visualmente objetos largos mediante cortes. | Req: Vista base activa seleccionada")
    print("  'clipGroup'      : Agrupa múltiples vistas para aplicar recortes coordenados. | Req: Página activa y vistas seleccionadas")
    print("  'complexSection' : Genera vistas de sección y cortes complejos del modelo. | Req: Vista activa y elementos de corte")
    print("  'draft'          : Proyecta un objeto bidimensional (2D) del workbench Draft. | Req: Objeto planar de Draft seleccionado")
    print("  'spreadsheet'    : Renderiza e integra una tabla de Hoja de Cálculo en la hoja. | Req: Hoja de cálculo activa")