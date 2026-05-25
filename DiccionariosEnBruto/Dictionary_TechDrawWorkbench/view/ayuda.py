# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

def ayuda():
    print("=== Subgrupo TechDraw: view ===")
    print("  'draft'       : Inserta una vista de un objeto vectorial del modulo Draft. | Req: Objeto Draft seleccionado")
    print("  'spreadsheet' : Inserta una vista renderizada de una hoja de calculo. | Req: Objeto Spreadsheet en el arbol")
    print("  'text'        : Anade un bloque de anotacion con texto enriquecido. | Req: Pagina de TechDraw activa")
    print("  'hatch'       : Aplica un sombrado o patron de rayado a una cara. | Req: Cara cerrada seleccionada")
    print("  'show'        : Muestra u oculta los elementos invisibles del dibujo. | Req: Pagina de TechDraw activa")