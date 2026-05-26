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
    print('  crear union de angulo / union de angulo / restriccion de angulo - Crea una restricción de ángulo entre dos entidades geométricas.')
    print('         Requiere: Workbench Assembly activo y un Ensamblaje activo.')
    print('                   Opcionalmente, dos entidades geométricas preseleccionadas (caras planas o aristas lineales).')
    print('         Devuelve: Abre el panel de tareas de uniones. Crea un objeto Angle bajo el contenedor Joints.')
    print('         Nota: Fuerza un ángulo específico entre dos piezas distintas del ensamblaje.')
