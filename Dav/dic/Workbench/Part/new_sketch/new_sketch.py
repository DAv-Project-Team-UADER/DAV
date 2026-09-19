

import FreeCAD as App
from _lenient import LenientDict
from ..._display import enterSketcherContext
from ...Sketcher.new_sketch.new_sketch import _new_sketch as _create_on_plane
from .ayuda import ayuda


def _new_sketch() -> None:
    """Create a sketch on a plane chosen by voice and switch to the sketch tools.

    Uses the same DAV plane selector as the Sketcher workbench (arriba/abajo,
    okey/cancelar); the sketch is created on the chosen plane and edited.
    """
    _create_on_plane()
    enterSketcherContext()


new_sketch = {
    'new sketch': _new_sketch,
    'sketch': _new_sketch,
    'help': ayuda,
}

# Tolerante a claves aún no implementadas (no rompe el contexto entero).
new_sketch = LenientDict(new_sketch)
