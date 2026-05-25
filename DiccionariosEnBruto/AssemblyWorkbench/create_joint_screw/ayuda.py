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
    print('  crear union helicoidal / husillo / tornillo de avance - Crea una unión helicoidal (screw joint).')
    print('         Requiere: Workbench Assembly y Ensamblaje activos.')
    print('                   REQUISITO OBLIGATORIO: Debe existir previamente un Slider joint y un Revolute joint.')
    print('         Devuelve: Abre el panel de tareas para configurar el paso (pitch). Crea un objeto Screw bajo Joints.')
    print('         Nota: Simula un tornillo de avance, acoplando la traslación de un componente con la rotación del otro.')
