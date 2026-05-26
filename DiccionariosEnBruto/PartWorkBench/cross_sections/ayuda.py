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
    print('  secciones transversales - Crea múltiples secciones transversales a lo largo de un eje.')
    print('         Requiere: Tener un objeto base seleccionado en la vista 3D.')
    print('         Devuelve: Abre el panel de tareas para configurar el eje, cantidad y espaciado.')
    print('                   Al confirmar, genera un compuesto de perfiles (Cross sections).')
    print('         Nota: Herramienta de utilidad, muy usada para análisis de formas y diseño industrial.')
