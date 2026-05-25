# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

def ayuda():
    print("=== Subgrupo PartDesign: primitivas ===")
    print("  'caja'      : Inserta un cubo/caja aditiva. | Req: Body activo (se crea si no existe)")
    print("  'cono'      : Inserta un cono aditivo (puede ser truncado). | Req: Body activo")
    print("  'cilindro'  : Inserta un cilindro aditivo. | Req: Body activo")
    print("  'elipsoide' : Inserta un elipsoide aditivo. | Req: Body activo")
    print("  'prisma'    : Inserta un prisma poligonal aditivo. | Req: Body activo")
    print("  'esfera'    : Inserta una esfera aditiva. | Req: Body activo")
    print("  'toroide'   : Inserta un toroide (dona) aditivo. | Req: Body activo")
    print("  'cuna'      : Inserta una cuña (wedge) aditiva. | Req: Body activo")
    print("  NOTA: Todas las primitivas usan scripting API. El Body se crea automáticamente si no existe.")
