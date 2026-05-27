import FreeCADGui as Gui
from .annotation_style_editor.annotation import annotation
from .arc.arc import arc
from .curve.curve import curve
from .circle.circle import circle
from .circular_array.array import array
from .modify.modify import modify
from .dimension.dimension import dimension
from .ellipse.ellipse import ellipse
from .facebinder.facebinder import facebinder
from .ayuda import ayuda

draft = {
    'annotation': annotation,
    'arc': arc,
    'curve': curve,
    'circle': circle,
    'array': array,
    'modify': modify,
    'dimension': dimension,
    'ellipse': ellipse,
    'facebinder': facebinder,
    'help': ayuda,
}