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

"""Spanish spoken-word mapping for the DAV StdView dictionary folders."""

from .StdView import StdView

TraduceToEs = {
    "apariencia": StdView["appearance"],
    "aspecto": StdView["appearance"],
    "estilo visual": StdView["appearance"],

    "camara": StdView["camera"],
    "cámara": StdView["camera"],
    "vista de camara": StdView["camera"],
    "vista de cámara": StdView["camera"],

    "recorte": StdView["clipping"],
    "clip": StdView["clipping"],
    "plano de recorte": StdView["clipping"],

    "estilos de dibujo": StdView["drawstyles"],
    "estilos de visualizacion": StdView["drawstyles"],
    "estilos de visualización": StdView["drawstyles"],
    "modos de dibujo": StdView["drawstyles"],

    "material": StdView["material"],
    "materiales": StdView["material"],

    "superposicion": StdView["overlay"],
    "superposición": StdView["overlay"],
    "overlay": StdView["overlay"],
    "vista superpuesta": StdView["overlay"],

    "paneles": StdView["panels"],
    "panel": StdView["panels"],
    "paneles de vista": StdView["panels"],

    "vistas guardadas": StdView["savedviews"],
    "vista guardada": StdView["savedviews"],
    "vistas favoritas": StdView["savedviews"],

    "vistas estandar": StdView["standardviews"],
    "vistas estándar": StdView["standardviews"],
    "vista estandar": StdView["standardviews"],
    "vista estándar": StdView["standardviews"],
    "vistas basicas": StdView["standardviews"],
    "vistas básicas": StdView["standardviews"],

    "estereo": StdView["stereo"],
    "estéreo": StdView["stereo"],
    "vista estereo": StdView["stereo"],
    "vista estéreo": StdView["stereo"],

    "barras de herramientas": StdView["toolbars"],
    "barra de herramientas": StdView["toolbars"],

    "arbol": StdView["tree"],
    "árbol": StdView["tree"],
    "arbol del modelo": StdView["tree"],
    "árbol del modelo": StdView["tree"],
    "arbol de documento": StdView["tree"],
    "árbol de documento": StdView["tree"],

    "visibilidad": StdView["visibility"],
    "visible": StdView["visibility"],
    "mostrar ocultar": StdView["visibility"],

    "ayuda": StdView["help"],
    "información": StdView["help"],
    "opciones": StdView["help"],
}
