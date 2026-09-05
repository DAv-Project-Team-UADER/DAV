# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.

import FreeCADGui as Gui
from .ayuda import ayuda

def run_cmd(cmd):
    try:
        Gui.activateWorkbench("TechDrawWorkbench")
        Gui.runCommand(cmd, 0)
    except Exception as e:
        print(f"[DAV] Error: {e}")

symbols = {
    'weldsymbol': lambda: run_cmd('TechDraw_WeldSymbol'),
    'richtext': lambda: run_cmd('TechDraw_RichTextAnnotation'),
    'finish': lambda: run_cmd('TechDraw_SurfaceFinishSymbols'),
    'help': ayuda
}