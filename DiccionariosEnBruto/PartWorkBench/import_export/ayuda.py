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


def ayuda():
    print('Comandos disponibles en este nivel:')
    print('  configuracion importacion exportacion / preferencias dxf / etc - Abre la ventana de preferencias de importación y exportación.')
    print('         Requiere: Tener cargado el workbench correspondiente según el formato a utilizar[cite: 72].')
    print('         Devuelve: Una interfaz de configuración para controlar parámetros de múltiples formatos CAD y BIM[cite: 74].')
    print('         Nota: Incluye opciones para DAE, DWG, DXF, IFC, IGES, STEP, SVG y VTK[cite: 75].')
    print('               Algunas preferencias dependen de módulos externos como pyCollada o IfcOpenShell[cite: 76].')
