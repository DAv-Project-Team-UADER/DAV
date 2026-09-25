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

"""Spanish spoken-word mapping for the DAV base dictionary."""

from Workbench.workbench import workbench as Workbench
from StdView.StdView import StdView
from Explorer.Explorer import explorer
from LineAttributes.LineAttributes import LineAttributes
from Selection.selection import selection
from Correction.Correction import correction
from measure import CreateDimension
from integration.dav_dock_panel import hide_dav_panel, show_dav_panel
from integration.launch_preferences import open_preferences

TraduceToEs = {
    # Explorer (archivo, edición, ventanas)
    "explorador":    explorer,
    "archivo":       explorer,
    "archivos":      explorer,
    "carpeta":       explorer,
    "carpetas":      explorer,
    "directorio":    explorer,
    "directorios":   explorer,
    "mesa de trabajo": Workbench,
    "mesa": Workbench,
    "banco de trabajo": Workbench,
    "trabajo": Workbench,
    "banco": Workbench,
    "taller": Workbench,
    "herramientas":   Workbench,
    "crear":   Workbench,

    # Line attributes (atributos de linea)
    "atributos de línea": LineAttributes,
    "atributos de linea": LineAttributes,
    "diálogo atributos de línea": LineAttributes,
    "dialogo atributos de linea": LineAttributes,
    "ventana atributos de línea": LineAttributes,
    "panel atributos de línea": LineAttributes,

    # Std View (vista estandar)
    # "estándar"/"visor" suelen fallar en Vosk (los oye como "vista estoy/por").
    # Preferir frases sin la palabra "vista" al inicio:
    "vista estándar": StdView,
    "vista estandar":  StdView,
    "vistas estándar": StdView,
    "vistas estandar":  StdView,
    "diálogo vista estándar": StdView,
    "ventana vista estándar": StdView,
    "visor": StdView,
    "vistas basicas": StdView,
    "vistas básicas": StdView,
    "vista basica": StdView,
    "vista básica": StdView,
    "vista del modelo": StdView,
    "vistas del modelo": StdView,
    "orientacion": StdView,
    "orientación": StdView,
    "control de vista": StdView,
    "stdview": StdView,

    # Workbench
    "banco de trabajo": Workbench,
    "bancos de trabajo": Workbench,
    "entorno de trabajo": Workbench,

    # Preferencias
    "seleccion":            selection,
    "selección":            selection,
    "seleccionar":          selection,
    "seleccion de objetos": selection,
    "selección de objetos": selection,
    "objetos":              selection,
    # Sinonimos sin parecido (difflib >= 0.82) con ninguna palabra de los
    # submenus: "seleccion"/"objetos" se confunden con "seccion"/"objeto"/
    # "deseleccionar" al hablar dentro de Part, TechDraw, Tree y PartDesign.
    "agarrar":              selection,
    "elegir":               selection,
    "lista de objetos":     selection,
    "preferencias":  open_preferences,
    "configuracion": open_preferences,
    "ajustes":       open_preferences,

    # Panel DAV
    "minimizar":  hide_dav_panel,
    "reducir":    hide_dav_panel,
    "disminuir":  hide_dav_panel,
    "maximizar":  show_dav_panel,
    "aumentar":   show_dav_panel,
    "agrandar":   show_dav_panel,

    # Correcciones (globales: se dicen desde cualquier contexto)
    "deshacer":                correction["undo"],
    "deshacer cambio":         correction["undo"],
    "deshacer ultimo":         correction["undo"],
    "rehacer":                 correction["redo"],
    "rehacer cambio":          correction["redo"],
    "borrar ultimo":           correction["deletelast"],
    "borrar último":           correction["deletelast"],
    "eliminar ultimo":         correction["deletelast"],
    "eliminar último":         correction["deletelast"],
    "quitar ultimo":           correction["deletelast"],
    "borrar el ultimo objeto": correction["deletelast"],
    "borrar objeto":           correction["deleteobject"],
    "eliminar objeto":         correction["deleteobject"],
    "quitar objeto":           correction["deleteobject"],
    "borrar rotos":            correction["deletebroken"],
    "eliminar rotos":          correction["deletebroken"],
    "limpiar rotos":           correction["deletebroken"],
    "limpiar errores":         correction["deletebroken"],
    "borrar objetos rotos":    correction["deletebroken"],
    "limpiar objetos rotos":   correction["deletebroken"],

    # Cota / medir (globales: la gramática de Vosk solo incluye la raíz y el
    # contexto actual, así que para oírlas en cualquier lado tienen que estar acá)
    "medir":           CreateDimension,
    "medir distancia": CreateDimension,
    "medida":          CreateDimension,
    "cota":            CreateDimension,
    "cotar":           CreateDimension,
    "acotar":          CreateDimension,
    "dimensionar":     CreateDimension,
}

# Vistas estándar (frontal, arriba, zoom...): en todos los contextos, raíz incluida
from dic.StdView.StandardViews.TraduceToEs import TraduceToEs as _StandardViewsPhrases
for _phrase, _target in _StandardViewsPhrases.items():
    TraduceToEs.setdefault(_phrase, _target)

# Mover la vista (centra la cámara en un punto)
from moveview import MoveView, MOVE_VIEW_PHRASES
for _phrase in MOVE_VIEW_PHRASES['es']:
    TraduceToEs.setdefault(_phrase, MoveView)
