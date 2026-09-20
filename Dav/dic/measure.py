#  Copyright (C) 2026 The DAV Project Team
#  Copyright (C) 2026 El Equipo del Proyecto DAV
#  Universidad Autónoma de Entre Ríos (UADER)
#  Directed by Gerard Guillermo and Gallo Fabricio David
#  Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, in GPLv3 version of the License
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Linear dimension ("cota", "medir") that adapts to the active document.

El mismo comando se dice desde muchos contextos. Según dónde se esté, pide
cuatro valores (X, Y de cada punto, dibujo plano) o seis (X, Y, Z de cada
punto, modelo 3D). Se decide cada vez que se ejecuta, así el usuario puede
cambiar de contexto sin que el comando quede fijo:

1. Hay un boceto en edición                       -> 2D, en el plano del boceto.
2. El documento tiene algún sólido                -> 3D.
3. Sin sólidos y un banco plano activo
   (Draft, Sketcher, TechDraw)                    -> 2D.
4. Cualquier otro caso (documento vacío o 3D)     -> 3D.
"""

import inspect

import Draft
import FreeCAD as App

try:
    import FreeCADGui as Gui
except ImportError:  # sin interfaz: se decide solo por el documento
    Gui = None

# Bancos de trabajo donde se dibuja en el plano.
_FLAT_WORKBENCHES = ("DraftWorkbench", "SketcherWorkbench", "TechDrawWorkbench")

# Distancia de la línea de cota respecto de los puntos medidos, en mm.
_OFFSET_DISTANCE = 10.0


def _sketchInEdit():
    """Return the sketch being edited, or None."""
    if Gui is None:
        return None
    try:
        view_object = Gui.ActiveDocument.getInEdit()
        obj = getattr(view_object, "Object", None)
        if obj is not None and obj.TypeId == "Sketcher::SketchObject":
            return obj
    except Exception:
        pass
    return None


def _hasSolids(doc) -> bool:
    """True when some object of the document holds a solid."""
    for obj in doc.Objects:
        shape = getattr(obj, "Shape", None)
        if shape is not None and not shape.isNull() and shape.Solids:
            return True
    return False


def _activeWorkbench() -> str:
    """Return the name of the active FreeCAD workbench, or an empty string."""
    if Gui is None:
        return ""
    try:
        return Gui.activeWorkbench().name()
    except Exception:
        return ""


def dimensionMode():
    """Decide whether the next dimension is flat (2D) or spatial (3D).

    Returns:
        ``("2D", sketch)`` with the sketch being edited (or None), or ``("3D", None)``.

    Example::

        mode, sketch = dimensionMode()
    """
    sketch = _sketchInEdit()
    if sketch is not None:
        return "2D", sketch
    doc = App.ActiveDocument
    if doc is not None and _hasSolids(doc):
        return "3D", None
    if _activeWorkbench() in _FLAT_WORKBENCHES:
        return "2D", None
    return "3D", None


def _createDimension(point1, point2, placement=None):
    """Create a Draft linear dimension between two points.

    Args:
        point1: First point, in the plane's own coordinates.
        point2: Second point, in the plane's own coordinates.
        placement: Optional ``App.Placement`` of the plane the points live on
            (the sketch's); None means the global axes.

    Returns:
        The dimension object, or None when both points coincide.
    """
    active_doc = App.ActiveDocument
    if active_doc is None:
        active_doc = App.newDocument()

    line_vector = point2.sub(point1)
    if line_vector.Length == 0:
        App.Console.PrintError("Error: Point 1 and Point 2 coincide.\n")
        return None

    # la línea de cota se desplaza perpendicular al segmento, dentro del plano
    normal_vector = App.Vector(-line_vector.y, line_vector.x, 0.0)
    if normal_vector.Length == 0:
        # segmento vertical (a lo largo de Z): un desplazamiento en Z caería sobre él
        normal_vector = App.Vector(1.0, 0.0, 0.0)
    normal_vector.normalize()
    dimension_point = point1.add(normal_vector.multiply(_OFFSET_DISTANCE))

    if placement is not None:
        point1 = placement.multVec(point1)
        point2 = placement.multVec(point2)
        dimension_point = placement.multVec(dimension_point)

    active_doc.openTransaction("Create Dimension")
    dim_obj = Draft.make_dimension(point1, point2, dimension_point)
    active_doc.commitTransaction()
    active_doc.recompute()
    App.Console.PrintMessage(f"Dimension successfully created between {point1} and {point2}.\n")
    return dim_obj


def _dimension3d(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int):
    """Linear dimension between Point1(x1, y1, z1) and Point2(x2, y2, z2)."""
    print("[DAV] Cota 3D: pide X, Y y Z de cada punto.")
    return _createDimension(
        App.Vector(float(x1), float(y1), float(z1)),
        App.Vector(float(x2), float(y2), float(z2)),
    )


def _dimension2d(x1: int, y1: int, x2: int, y2: int):
    """Linear dimension between Point1(x1, y1) and Point2(x2, y2) on the drawing plane."""
    _mode, sketch = dimensionMode()
    where = f"en el plano del boceto '{sketch.Name}'" if sketch is not None else "en el plano XY"
    print(f"[DAV] Cota 2D {where}: pide solo X e Y de cada punto.")
    return _createDimension(
        App.Vector(float(x1), float(y1), 0.0),
        App.Vector(float(x2), float(y2), 0.0),
        sketch.Placement if sketch is not None else None,
    )


class _CreateDimension:
    """Voice command that asks for 4 or 6 values depending on the document.

    El colector de parámetros y el validador leen la firma con
    ``inspect.signature`` cada vez que se ejecuta el comando; como acá la firma
    se calcula en ese momento, el mismo ``CreateDimension`` pide dos o tres
    coordenadas por punto sin que los diccionarios cambien.
    """

    __name__ = "CreateDimension"

    @property
    def __signature__(self):
        mode, _sketch = dimensionMode()
        return inspect.signature(_dimension2d if mode == "2D" else _dimension3d)

    def __call__(self, *args, **kwargs):
        # el modo lo marca lo que llegó (z1 / seis valores): así coincide con lo que se pidió
        is3d = "z1" in kwargs or len(args) == 6
        if not kwargs and not args:
            is3d = dimensionMode()[0] == "3D"
        return (_dimension3d if is3d else _dimension2d)(*args, **kwargs)


CreateDimension = _CreateDimension()


# Frases habladas de la cota / medir, por idioma. Cada TraduceTo de Workbench las
# agrega con setdefault (sin pisar frases propias del contexto) apuntando a CreateDimension.
MEASURE_PHRASES = {
    'es': (
        'medir',
        'medir distancia',
        'acotar',
        'dimensionar',
        'cotar',
        'distancia',
        'medida',
        'longitud',
        'separación',
        'separacion',
        'cota',
        'acotación',
        'acotacion',
        'dimensión',
        'dimension',
        'métrica',
        'metrica',
        'metro',
        'milímetro',
        'milimetro',
        'centímetro',
        'centimetro',
        'cinta',
        'flexómetro',
        'flexometro',
        'metro enrollable',
        'regla',
        'escalímetro',
        'escalimetro',
        'calibre',
        'pie de rey',
        'línea de cota',
        'linea de cota',
        'cota lineal',
        'acotación lineal',
        'acotacion lineal',
        'dimensionado',
        'micrómetro',
        'micrometro',
    ),
    'en': (
        'measure',
        'measure distance',
        'distance',
        'dimension',
        'dimensioning',
        'meter',
        'milimeter',
        'millimeter',
        'centimeter',
        'tape measure',
        'tape tool',
        'tape',
        'ruler',
    ),
    'pt': (
        'medir',
        'medida',
        'medir distancia',
        'medir distância',
        'distância',
        'distancia',
        'cotar',
        'dimensionar',
        'aferir',
        'mensurar',
        'calcular distância',
        'calcular distancia',
        'comprimento',
        'separação',
        'separacao',
        'afastamento',
        'extensão',
        'extensao',
        'cota',
        'cotagem',
        'acotação',
        'acotacao',
        'dimensão',
        'dimensao',
        'métrica',
        'metrica',
        'dimensionamento',
        'metro',
        'milímetro',
        'milimetro',
        'centímetro',
        'centimetro',
        'flexômetro',
        'flexometro',
        'metro enrolável',
        'metro enrolavel',
        'régua',
        'regua',
        'escalímetro',
        'escalimetro',
        'calibre',
        'paquímetro',
        'paquimetro',
        'micrômetro',
        'micrometro',
        'tolerância',
        'tolerancia',
        'desvio',
        'ajuste',
        'medição',
        'medicao',
        'mensuração',
        'mensuracao',
        'aferição',
        'afericao',
        'calibração',
        'calibracao',
        'verificação',
        'verificacao',
        'inspeção',
        'inspecao',
        'controle dimensional',
        'metrologia',
    ),
}
