# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David

def ayuda():
    print("=== Subgrupo TechDraw: Views ===")
    print("  'clip'       : Crea una ventana rectangular de recorte para ocultar geometrías excedentes. | Req: Página activa")
    print("  'complex'    : Inserta una vista de sección compleja basada en una línea de corte no recta. | Req: Vista y Sketch")
    print("  'detail'     : Inserta una vista de detalle circular que amplía una porción específica. | Req: Vista principal")
    print("  'projection' : Genera un grupo de proyecciones multicubeta tradicionales en simultáneo. | Req: Objeto 3D")
    print("  'shape'      : Proyecta un objeto 3D sobre un plano 2D en el espacio tridimensional. | Req: Objeto 3D")
    print("  'section'    : Inserta una vista de sección transversal recta para mostrar interiores. | Req: Vista principal")
    print("  'share'      : Permite clonar o compartir una vista generada hacia otra página. | Req: Múltiples páginas")
    print("  'view'       : Inserta una vista principal 2D de un objeto 3D seleccionado. | Req: Página y Objeto 3D")