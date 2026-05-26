# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

def ayuda():
    print("=== Subgrupo PartDesign: patrones ===")
    print("  'lineal'         : Patrón lineal de una Feature. | Req: Body activo + Feature seleccionada")
    print("  'espejo'         : Simetría especular de una Feature. | Req: Body activo + Feature seleccionada + plano ref")
    print("  'polar'          : Patrón polar/circular de una Feature. | Req: Body activo + Feature seleccionada")
    print("  'multitransform' : Combinación de múltiples transformaciones. | Req: Body activo + Feature seleccionada")
    print("  NOTA: PartDesign_Scaled se omite al no tener comando independiente (acceder vía Multi-Transform).")
