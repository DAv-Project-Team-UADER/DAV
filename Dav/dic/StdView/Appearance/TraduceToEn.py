# Copyright (C) 2026 El Equipo del Proyecto DAV
# Copyright (C) 2026 The DAV Project Team
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
# SPDX-License-Identifier: GPL-3.0-or-later

from .Appearance import appearance
from .ayuda import ayuda
from DAV.DiccionariosEnBruto.StdView.Appearance import Appearance

TraduceToEn = {
    # Appearance
    'appearance':       appearance['appearance'],
    'look':             appearance['appearance'],
    'aspect':           appearance['appearance'],

    # facecolors
    'facecolor':        appearance['facecolor'],
    'background':       appearance['facecolor'],
    'Surface color':    appearance['facecolor'],
    'Part color':       appearance['facecolor'],

    # random colors
    'random color':         appearance['randomcolor'],
    'randomized color':     appearance['randomcolor'],
    'random shade':         appearance['randomcolor'],

    # texture mapping
    'texture mapping':      appearance['texturemapping'],
    'texture projection':   appearance['texturemapping'],
    'texture placement':    appearance['texturemapping'],

    # help
    'help':     Appearance['help'],
    'info':     Appearance['help'],
    'options':  Appearance['help'],

}
