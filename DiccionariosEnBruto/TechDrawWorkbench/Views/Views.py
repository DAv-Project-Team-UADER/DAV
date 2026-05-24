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
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

import FreeCADGui as Gui

# Diccionario del subgrupo Views (Vistas del modelo, proyecciones y cortes)
views = {
    'clip': lambda: Gui.runCommand('TechDraw_ClipGroup', 0),
    'complex': lambda: Gui.runCommand('TechDraw_ComplexSection', 0),
    'detail': lambda: Gui.runCommand('TechDraw_DetailView', 0),
    'projection': lambda: Gui.runCommand('TechDraw_ProjectionGroup', 0),
    'shape': lambda: Gui.runCommand('TechDraw_ProjectShape', 0),
    'section': lambda: Gui.runCommand('TechDraw_SectionView', 0),
    'share': lambda: Gui.runCommand('TechDraw_ShareView', 0),
    'view': lambda: Gui.runCommand('TechDraw_View', 0)
}