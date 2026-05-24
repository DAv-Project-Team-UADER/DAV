# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David

def ayuda():
    print("=== Subgrupo TechDraw: Page ===")
    print("  'default'  : Inserta una página con la plantilla SVG predeterminada del sistema. | Req: Ninguno")
    print("  'template' : Crea una nueva página permitiendo especificar una plantilla personalizada. | Req: Archivo SVG")
    print("  'redraw'   : Fuerza la actualización de todo el documento y redibuja las páginas. | Req: Documento activo")
    print("  'print'    : Envía todas las páginas del documento a la impresora abriendo el diálogo. | Req: Página activa")
    print("  'dxf'      : Exporta la página especificada al formato de intercambio CAD DXF. | Req: Página seleccionada")
    print("  'svg'      : Exporta la página especificada a un archivo de imagen vectorial SVG. | Req: Página seleccionada")