# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

def ayuda():
    print("=== Subgrupo PartDesign: boceto ===")
    print("  'extrusion'  : Extruye un boceto cerrado (Pad). | Req: Body activo + Sketch cerrado preexistente")
    print("  'revolucion' : Revoluciona un boceto alrededor del eje Y del Body. | Req: Body activo + Sketch preexistente")
    print("  'helice'     : Barre un perfil en trayectoria helicoidal. | Req: Body activo + Sketch cerrado")
    print("  'loft'       : Transición suave entre ≥2 bocetos. | Req: Body activo + mínimo 2 Sketches cerrados")
    print("  'tubo'       : Barre un perfil a lo largo de una trayectoria. | Req: Body activo + Sketch perfil + Sketch trayectoria")
    print("  NOTA: Estas operaciones usan scripting API. El boceto DEBE existir antes de ejecutar.")
