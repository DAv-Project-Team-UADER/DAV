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
# SPDX-License-Identifier: GPL-3.0-or-later

"""DAV visual style for the 3D view: white background, graph-paper grid and a clean look for solids.

Entry points, all safe to call outside FreeCAD (they do nothing there):

- :func:`aplicarFondoBlanco` paints the 3D view background white.
- :func:`aplicarRejilla` gives Draft and Sketcher the same 2 mm grid.
- :func:`aplicarVistaDav` applies the three view-wide settings: background, grid and line width.
- :func:`aplicarEstiloDav` gives one object the DAV look (light-gray solid, dark edges).
- :func:`instalarEstiloDav` applies the view settings and keeps the look on every new solid.

The voice command ``AplicarEstilo`` (``Operations/EspecialOperations.py``) uses
:func:`aplicarVistaDav` and :func:`aplicarEstiloDav`; the dock panel calls
:func:`instalarEstiloDav` when it is mounted.
"""

from __future__ import annotations

try:
    import FreeCAD
    import FreeCADGui
except ImportError:  # fuera de FreeCAD (pruebas, documentación)
    FreeCAD = None
    FreeCADGui = None

# colores como (r, g, b) entre 0 y 1, el formato de ViewObject
FONDO = (1.0, 1.0, 1.0)
SOLIDO = (0.80, 0.82, 0.85)
ARISTA = (0.15, 0.15, 0.15)
ANCHO_LINEA = 2.0

# Papel cuadriculado de Draft y Sketcher: 2 x 2 mm en #D4C7C5 sobre el fondo blanco.
REJILLA = (0xD4 / 255, 0xC7 / 255, 0xC5 / 255)
PASO_REJILLA = "2 mm"

_VIEW_PARAMS = "User parameter:BaseApp/Preferences/View"
_DRAFT_PARAMS = "User parameter:BaseApp/Preferences/Mod/Draft"
_SKETCHER_PARAMS = "User parameter:BaseApp/Preferences/Mod/Sketcher/General"
# Los objetos de origen no son piezas: no se les cambia el aspecto.
_IGNORADOS = ("App::Origin", "App::Line", "App::Plane")

_observer = None


def _empaquetar(color: tuple[float, float, float], alfa: int = 255) -> int:
    """Pack an (r, g, b) colour into the unsigned RGBA integer FreeCAD stores in its parameters."""
    r, g, b = (round(canal * 255) for canal in color)
    return (r << 24) | (g << 16) | (b << 8) | alfa


def aplicarFondoBlanco() -> None:
    """Make the 3D view background plain white, now and for the next sessions."""
    if FreeCAD is None:
        return
    params = FreeCAD.ParamGet(_VIEW_PARAMS)
    fondo = _empaquetar(FONDO)
    params.SetBool("Simple", True)
    params.SetBool("Gradient", False)
    params.SetUnsigned("BackgroundColor", fondo)
    params.SetUnsigned("BackgroundColor2", fondo)
    params.SetUnsigned("BackgroundColor3", fondo)
    params.SetUnsigned("BackgroundColor4", fondo)
    # la vista abierta no relee las preferencias sola: se le pide el color directo si puede
    try:
        vista = FreeCADGui.ActiveDocument.ActiveView
        vista.setBackgroundColor(*FONDO)
    except Exception:  # noqa: BLE001 - sin vista activa o versión sin ese método
        pass


def aplicarRejilla() -> None:
    """Give Draft and Sketcher the same 2 x 2 mm grid, in ``REJILLA`` and always visible."""
    if FreeCAD is None:
        return
    color = _empaquetar(REJILLA)

    draft = FreeCAD.ParamGet(_DRAFT_PARAMS)
    draft.SetBool("grid", True)
    draft.SetBool("alwaysShowGrid", True)
    draft.SetString("gridSpacing", PASO_REJILLA)
    draft.SetUnsigned("gridColor", color)
    # en Draft el parámetro es opacidad, no transparencia: 100 deja el color tal cual
    draft.SetInt("gridTransparency", 100)
    # sin borde, sin figura humana y sin ejes de colores: la cuadrícula queda pareja
    draft.SetBool("gridBorder", False)
    draft.SetBool("gridShowHuman", False)
    draft.SetBool("coloredGridAxes", False)

    sketcher = FreeCAD.ParamGet(_SKETCHER_PARAMS)
    sketcher.SetBool("ShowGrid", True)
    # con el paso automático la cuadrícula crece con el zoom y deja de medir 2 mm
    sketcher.SetBool("GridAuto", False)
    # el Sketcher guarda el paso como cantidad, en un subgrupo del mismo nombre
    sketcher.GetGroup("GridSize").SetString("GridSize", PASO_REJILLA)
    # una sola familia de líneas: todos los cuadros iguales, sin líneas maestras
    sketcher.SetInt("GridNumberSubdivision", 1)
    sketcher.SetUnsigned("GridLineColor", color)
    sketcher.SetUnsigned("GridDivLineColor", color)
    # 0xffff es la línea llena; el Sketcher trae las finas punteadas
    sketcher.SetInt("GridLinePattern", 0xFFFF)
    sketcher.SetInt("GridDivLinePattern", 0xFFFF)
    sketcher.SetInt("GridTransparency", 0)


def aplicarVistaDav() -> None:
    """Apply the DAV settings that belong to the view, not to one object."""
    if FreeCAD is None:
        return
    aplicarFondoBlanco()
    aplicarRejilla()
    # los objetos planos de Draft no pasan por aplicarEstiloDav (no tienen caras):
    # el ancho les llega por la preferencia global.
    FreeCAD.ParamGet(_VIEW_PARAMS).SetInt("DefaultShapeLineWidth", round(ANCHO_LINEA))


def aplicarEstiloDav(obj) -> bool:
    """Give ``obj`` the DAV look; return ``True`` when something was changed.

    Only solids and surfaces are restyled: sketches, planes, joints and any object without
    a shape keep their own appearance.

    Args:
        obj: a FreeCAD document object (``Part::Feature`` or a body/feature built on it).
    """
    if FreeCAD is None or obj is None or getattr(obj, "TypeId", "") in _IGNORADOS:
        return False
    vista = getattr(obj, "ViewObject", None)
    forma = getattr(obj, "Shape", None)
    if vista is None or forma is None or forma.isNull() or not (forma.Solids or forma.Faces):
        return False
    cambio = False
    for atributo, valor in (
        ("ShapeColor", SOLIDO),
        ("LineColor", ARISTA),
        ("LineWidth", ANCHO_LINEA),
    ):
        if hasattr(vista, atributo):
            setattr(vista, atributo, valor)
            cambio = True
    return cambio


class _EstiloObserver:
    """Document observer: styles each solid once, right after it gets its shape."""

    def __init__(self):
        # (documento, objeto) ya pintados: un recálculo posterior no pisa los colores del usuario
        self._pintados = set()

    def slotChangedObject(self, obj, prop):  # noqa: N802 - nombre fijo de FreeCAD
        # la forma se calcula después de crear el objeto; recién ahí hay algo que pintar
        if prop != "Shape":
            return
        clave = (obj.Document.Name, obj.Name)
        if clave in self._pintados:
            return
        try:
            if aplicarEstiloDav(obj):
                self._pintados.add(clave)
        except Exception as exc:  # noqa: BLE001 - un fallo de estilo no debe cortar el modelado
            print(f"[DAV] Estilo visual: {exc}")


def instalarEstiloDav() -> None:
    """Apply the view settings and style every solid created from now on.

    Calling it again does nothing.
    """
    global _observer
    if FreeCAD is None or _observer is not None:
        return
    aplicarVistaDav()
    _observer = _EstiloObserver()
    FreeCAD.addDocumentObserver(_observer)
