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
    print('  cone / primitive cone - Crea un cono solido parametrico.')
    print('         Requiere: Radius1 (float) — radio de la base inferior. Default: 2 mm.')
    print('                   Radius2 (float) — radio de la base superior. Default: 4 mm.')
    print('                                     Poner 0 para cono puro.')
    print('                   Height  (float) — altura. Default: 10 mm.')
    print('                   Angle   (float) — arco del perfil circular. Default: 360 grados.')
    print('         Nota: Si Angle < 360 el resultado es un segmento de cono.')
    print('               Disponible desde Part -> Primitives -> Cone.')