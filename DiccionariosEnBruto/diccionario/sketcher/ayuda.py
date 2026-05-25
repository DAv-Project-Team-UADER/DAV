# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

def ayuda():
    print("=== Subgrupo PartDesign: sketcher ===")
    print("  'preferencias' : Abre las preferencias de PartDesign. | Req: FreeCAD con GUI activa")
    print("  'verificar'    : Verifica geometría de un sólido. | Req: Objeto con Shape pasado por parámetro")
    print("  NOTA: Los comandos EditSketch, MapSketch y ValidateSketch no se incluyen como lambdas")
    print("        porque requieren interactuar con el objeto sketch por parámetro. Ver documentación.")
