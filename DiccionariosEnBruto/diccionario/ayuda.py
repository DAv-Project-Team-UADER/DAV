# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

from .primitivas.ayuda  import ayuda as _ayuda_primitivas
from .boceto.ayuda      import ayuda as _ayuda_boceto
from .herramientas.ayuda import ayuda as _ayuda_herramientas
from .modificadores.ayuda import ayuda as _ayuda_modificadores
from .patrones.ayuda    import ayuda as _ayuda_patrones
from .sketcher.ayuda    import ayuda as _ayuda_sketcher

def ayuda():
    print("=== Diccionario PartDesignWorkbench ===")
    _ayuda_primitivas()
    _ayuda_boceto()
    _ayuda_herramientas()
    _ayuda_modificadores()
    _ayuda_patrones()
    _ayuda_sketcher()
