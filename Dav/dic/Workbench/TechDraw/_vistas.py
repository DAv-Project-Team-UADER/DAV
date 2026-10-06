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

"""Build and adjust a TechDraw drawing by voice.

En TechDraw lo que sigue a «vista» se hacía con el mouse: elegir qué objeto va en la
vista, su dirección, escala y posición, el eje de simetría y las cotas. Acá cada paso
se pregunta por voz con los mismos cuadros que el resto de DAV; el objeto se elige de
la lista («avanzar») o deletreando su nombre («buscar por deletreo»), útil cuando el
documento tiene cientos de objetos.
"""

import FreeCAD as App

PAGE_TYPE = "TechDraw::DrawPage"
VIEW_TYPE = "TechDraw::DrawViewPart"

# Vistas normalizadas: (clave, nombre, dirección hacia el observador, dirección X de la hoja)
# y las palabras que la eligen en cada idioma. «Isométrica» es la de la guía de la tijera.
_DIRECTIONS = (
    # «arriba» y «abajo» no son palabras de elección: en el cuadro mueven la selección
    ("top", "Superior (planta)", (0, 0, 1), (1, 0, 0), {
        "es": ("superior", "planta"),
        "en": ("top", "plan"),
        "pt": ("superior", "planta"),
    }),
    ("front", "Frontal", (0, -1, 0), (1, 0, 0), {
        "es": ("frontal", "frente"),
        "en": ("front",),
        "pt": ("frontal", "frente"),
    }),
    ("right", "Derecha", (1, 0, 0), (0, 1, 0), {
        "es": ("derecha", "derecho"),
        "en": ("right",),
        "pt": ("direita", "direito"),
    }),
    ("left", "Izquierda", (-1, 0, 0), (0, -1, 0), {
        "es": ("izquierda", "izquierdo"),
        "en": ("left",),
        "pt": ("esquerda", "esquerdo"),
    }),
    ("rear", "Trasera", (0, 1, 0), (-1, 0, 0), {
        "es": ("trasera", "posterior"),
        "en": ("rear", "back"),
        "pt": ("traseira", "posterior"),
    }),
    ("bottom", "Inferior", (0, 0, -1), (1, 0, 0), {
        "es": ("inferior",),
        "en": ("bottom",),
        "pt": ("inferior",),
    }),
    ("iso", "Isométrica", (1, -1, 1), (1, 1, 0), {
        "es": ("isometrica", "iso"),
        "en": ("isometric", "iso"),
        "pt": ("isometrica", "iso"),
    }),
)

_ORIENTATIONS = (
    ("horizontal", "Horizontal", {"es": ("horizontal",), "en": ("horizontal",), "pt": ("horizontal",)}),
    ("vertical", "Vertical", {"es": ("vertical",), "en": ("vertical",), "pt": ("vertical",)}),
)

_AXIS_REFERENCES = (
    ("center", "Centro de la vista", {
        "es": ("centro", "centro de la vista"),
        "en": ("center", "view center"),
        "pt": ("centro", "centro da vista"),
    }),
    ("origin", "Origen del modelo", {
        "es": ("origen", "origen del modelo"),
        "en": ("origin", "model origin"),
        "pt": ("origem", "origem do modelo"),
    }),
)

_PROJECTIONS = (
    ("Third angle", "Tercer ángulo (ASME)", {
        "es": ("tercer angulo", "tercero", "asme"),
        "en": ("third angle", "third", "asme"),
        "pt": ("terceiro angulo", "terceiro", "asme"),
    }),
    ("First angle", "Primer ángulo (ISO)", {
        "es": ("primer angulo", "primero", "iso"),
        "en": ("first angle", "first", "iso"),
        "pt": ("primeiro angulo", "primeiro", "iso"),
    }),
)

# Margen del eje de simetría más allá de la figura, en mm de la hoja, y separación de las cotas.
_AXIS_MARGIN = 6.0
_DIMENSION_GAP = 12.0


def _prompts():
    """Return the shared voice dialogs (list of objects, numbers, choices...)."""
    try:
        from Workbench import _prompts as prompts
    except ImportError:
        from dic.Workbench import _prompts as prompts
    return prompts


def _language() -> str:
    _prompts()._ensure_input_prompts_on_path()
    from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher

    return PlaneGrammarSwitcher.CurrentLanguage()


def _options(table):
    """Turn a table of ``(key, name, {language: words})`` into ChoiceInputPrompt options."""
    language = _language()
    return [(row[0], row[1], row[-1].get(language, row[-1]["es"])) for row in table]


def _doc():
    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo.")
    return doc


# ---------------------------------------------------------------- elegir página, vista y objeto


def _pickPage(doc):
    """Return the page to draw on, or None (with a message)."""
    if not doc.findObjects(PAGE_TYPE):
        print("[DAV] Error: no hay ninguna página. Creala con «página» y «plantilla».")
        return None
    try:
        from .Page._page import _pickPage as pickPage
    except ImportError:
        from dic.Workbench.TechDraw.Page._page import _pickPage as pickPage
    page = pickPage(doc)
    if page is None:
        print("[DAV] Cancelado: no hay página elegida.")
    return page


def _selectedView(doc):
    try:
        import FreeCADGui as Gui

        for obj in Gui.Selection.getSelection(doc.Name):
            if obj.isDerivedFrom(VIEW_TYPE):
                return obj
    except Exception:
        pass
    return None


def _pickView(doc, title: str):
    """Return the view to adjust: the selected one, the only one, or the one chosen by voice."""
    views = doc.findObjects(VIEW_TYPE)
    if not views:
        print("[DAV] Error: no hay ninguna vista. Creala con «vista de objeto».")
        return None
    view = _selectedView(doc)
    if view is None and len(views) == 1:
        view = views[0]
    if view is None:
        view = _prompts().askObject(
            doc,
            title,
            "Elegí la vista",
            lambda obj: obj.isDerivedFrom(VIEW_TYPE),
            "[DAV] Error: no hay vistas para elegir.",
        )
    if view is None:
        print(f"[DAV] {title} cancelado: no hay vista elegida.")
    return view


def isViewSource(obj) -> bool:
    """True for what a view can show: a body, a part, an assembly or a loose shape.

    Lo que vive dentro de otro objeto (los vínculos de un ensamblaje, las operaciones de
    un cuerpo) no se ofrece: la vista siempre parte del contenedor.
    """
    if obj.isDerivedFrom("TechDraw::DrawView") or obj.isDerivedFrom(PAGE_TYPE):
        return False
    try:
        if obj.getParentGeoFeatureGroup() is not None:
            return False
    except Exception:
        pass
    if obj.isDerivedFrom("Assembly::AssemblyObject") or obj.isDerivedFrom("App::Part"):
        return True
    return _prompts().isShape(obj)


def _pickSource(doc, title: str):
    source = _prompts().askObject(
        doc,
        title,
        "Elegí el objeto de la vista",
        isViewSource,
        "[DAV] Error: no hay ningún objeto para mostrar en la vista.",
    )
    if source is None:
        print(f"[DAV] {title} cancelado: no hay objeto elegido.")
    return source


def _askDirection(title: str):
    """Ask the standard view direction by voice; returns its table row or None."""
    key = _prompts().askChoice(
        title,
        "¿Desde dónde se mira? frontal, superior, derecha, izquierda, trasera, inferior o isométrica",
        _options(_DIRECTIONS),
    )
    if key is None:
        print(f"[DAV] {title} cancelado.")
        return None
    return next(row for row in _DIRECTIONS if row[0] == key)


def _askPositive(title: str, message: str):
    value = _prompts().askNumber(title, message)
    if value is None:
        print(f"[DAV] {title} cancelado.")
        return None
    if value <= 0:
        print(f"[DAV] Error: la escala tiene que ser mayor que cero (dijiste {value:g}).")
        return None
    return value


def _vector(values):
    return App.Vector(*values)


def _scaleOf(view) -> float:
    """The scale a view is drawn with (the page's when the view follows the page)."""
    try:
        return float(view.getScale())
    except Exception:
        return float(view.Scale)


# ---------------------------------------------------------------- vistas


def viewFromObject() -> None:
    """Create a view of an object on a page, choosing everything by voice.

    Pregunta, en orden: el objeto (de la lista o deletreando su nombre), desde dónde se
    mira, la escala y la posición en la hoja.

    Example::

        viewFromObject()
    """
    title = "Vista de objeto"
    doc = _doc()
    if doc is None:
        return
    page = _pickPage(doc)
    if page is None:
        return
    source = _pickSource(doc, title)
    if source is None:
        return
    direction = _askDirection(title)
    if direction is None:
        return
    scale = _askPositive(title, "Decí la escala: uno = natural, cero coma cinco = mitad, dos = doble")
    if scale is None:
        return
    x = _prompts().askNumber(title, "Decí la posición X en la hoja, en mm desde la izquierda")
    if x is None:
        return
    y = _prompts().askNumber(title, "Decí la posición Y en la hoja, en mm desde abajo")
    if y is None:
        return
    try:
        doc.openTransaction("Create view")
        view = doc.addObject(VIEW_TYPE, "View")
        page.addView(view)
        view.Source = [source]
        view.Direction, view.XDirection = _vector(direction[2]), _vector(direction[3])
        view.ScaleType, view.Scale = "Custom", scale
        view.X, view.Y = x, y
        view.Label = f"Vista {direction[1].split(' ')[0].lower()} de {source.Label}"
        doc.commitTransaction()
        doc.recompute()
    except Exception as error:
        doc.abortTransaction()
        print(f"[DAV] Error: no se pudo crear la vista de '{source.Label}': {error}")
        return
    print(f"[DAV] Vista {direction[1].lower()} de '{source.Label}' a escala {scale:g} en ({x:g}, {y:g}).")


def setViewDirection() -> None:
    """Change from where a view looks (frontal, superior, isométrica...), by voice."""
    title = "Dirección de la vista"
    doc = _doc()
    view = _pickView(doc, title) if doc is not None else None
    if view is None:
        return
    direction = _askDirection(title)
    if direction is None:
        return
    view.Direction, view.XDirection = _vector(direction[2]), _vector(direction[3])
    doc.recompute()
    print(f"[DAV] '{view.Label}' ahora se mira desde {direction[1].lower()}.")


def setViewScale() -> None:
    """Change the scale of a view, by voice."""
    title = "Escala de la vista"
    doc = _doc()
    view = _pickView(doc, title) if doc is not None else None
    if view is None:
        return
    scale = _askPositive(title, "Decí la escala: uno = natural, cero coma cinco = mitad, dos = doble")
    if scale is None:
        return
    view.ScaleType, view.Scale = "Custom", scale
    doc.recompute()
    print(f"[DAV] '{view.Label}' a escala {scale:g}.")


def setViewPosition() -> None:
    """Move a view on the page, by voice (X and Y in mm)."""
    title = "Posición de la vista"
    doc = _doc()
    view = _pickView(doc, title) if doc is not None else None
    if view is None:
        return
    x = _prompts().askNumber(title, "Decí la posición X en la hoja, en mm desde la izquierda")
    if x is None:
        return
    y = _prompts().askNumber(title, "Decí la posición Y en la hoja, en mm desde abajo")
    if y is None:
        return
    view.X, view.Y = x, y
    doc.recompute()
    print(f"[DAV] '{view.Label}' en ({x:g}, {y:g}).")


def setProjection() -> None:
    """Choose first or third angle projection for a page, by voice."""
    title = "Tipo de proyección"
    doc = _doc()
    page = _pickPage(doc) if doc is not None else None
    if page is None:
        return
    projection = _prompts().askChoice(title, "¿Tercer ángulo (ASME) o primer ángulo (ISO)?", _options(_PROJECTIONS))
    if projection is None:
        print(f"[DAV] {title} cancelado.")
        return
    page.ProjectionType = projection
    doc.recompute()
    print(f"[DAV] '{page.Label}': proyección en {projection.lower()}.")


# ---------------------------------------------------------------- eje de simetría y cotas


def _ensureDrawn(view) -> None:
    """Show the page of ``view`` on screen: until then the view has no geometry to draw on."""
    import FreeCADGui as Gui

    doc = view.Document
    page = next((p for p in doc.findObjects(PAGE_TYPE) if view in p.Views), None)
    if page is None:
        return
    page.ViewObject.doubleClicked()
    for _ in range(2):
        for _ in range(20):
            Gui.updateGui()
        doc.recompute()


def _projectedBox(view):
    """Return ``(umin, umax, vmin, vmax)`` of the viewed object seen from the view, or None.

    Son coordenadas de la vista sin escala: u hacia la derecha de la hoja, v hacia arriba.
    """
    try:
        shape = view.Source[0].Shape
        box = shape.BoundBox
        if not box.isValid():
            return None
    except Exception:
        return None
    right = view.XDirection.normalize()
    up = view.Direction.cross(view.XDirection).normalize()
    corners = [
        App.Vector(x, y, z)
        for x in (box.XMin, box.XMax)
        for y in (box.YMin, box.YMax)
        for z in (box.ZMin, box.ZMax)
    ]
    us = [corner.dot(right) for corner in corners]
    vs = [corner.dot(up) for corner in corners]
    return min(us), max(us), min(vs), max(vs)


def symmetryAxis() -> None:
    """Draw a centre line on a view (the axis of symmetry), choosing it by voice.

    Pregunta la vista, si el eje es horizontal o vertical y por dónde pasa: por el
    centro de la vista o por el origen del modelo (el perno de una tijera, el eje de
    una pieza de revolución...).
    """
    title = "Eje de simetría"
    doc = _doc()
    view = _pickView(doc, title) if doc is not None else None
    if view is None:
        return
    prompts = _prompts()
    orientation = prompts.askChoice(title, "¿El eje es horizontal o vertical?", _options(_ORIENTATIONS))
    if orientation is None:
        print(f"[DAV] {title} cancelado.")
        return
    reference = prompts.askChoice(
        title, "¿Pasa por el centro de la vista o por el origen del modelo?", _options(_AXIS_REFERENCES)
    )
    if reference is None:
        print(f"[DAV] {title} cancelado.")
        return
    try:
        _ensureDrawn(view)
        centre = view.getGeometricCenter()
        box = _projectedBox(view)
        margin = _AXIS_MARGIN / _scaleOf(view)
        # las coordenadas de la línea se miden desde el centro de la caja de la vista
        pivotU = 0.0 if reference == "center" else -centre.x
        pivotV = 0.0 if reference == "center" else -centre.y
        if box is None:
            low, high = (-50.0, 50.0)
            ranges = ((low, high), (low, high))
        else:
            ranges = ((box[0] - centre.x, box[1] - centre.x), (box[2] - centre.y, box[3] - centre.y))
        if orientation == "horizontal":
            start = App.Vector(ranges[0][0] - margin, pivotV, 0)
            end = App.Vector(ranges[0][1] + margin, pivotV, 0)
        else:
            start = App.Vector(pivotU, ranges[1][0] - margin, 0)
            end = App.Vector(pivotU, ranges[1][1] + margin, 0)
        tag = view.makeCosmeticLine(start, end)
        doc.recompute()
    except Exception as error:
        print(f"[DAV] Error: no se pudo trazar el eje de simetría: {error}")
        return
    if not tag:
        print("[DAV] Error: FreeCAD no creó el eje. Abrí la página (doble clic en el árbol) y probá de nuevo.")
        return
    print(f"[DAV] Eje de simetría {orientation} en '{view.Label}'.")


def totalDimensions() -> None:
    """Add the overall length and height of a view as extent dimensions, by voice."""
    title = "Cotas totales"
    doc = _doc()
    view = _pickView(doc, title) if doc is not None else None
    if view is None:
        return
    try:
        import TechDraw

        _ensureDrawn(view)
        before = set(obj.Name for obj in doc.findObjects("TechDraw::DrawViewDimExtent"))
        TechDraw.makeExtentDim(view, [], 0)  # largo total
        TechDraw.makeExtentDim(view, [], 1)  # alto total
        created = [o for o in doc.findObjects("TechDraw::DrawViewDimExtent") if o.Name not in before]
        box = _projectedBox(view)
        if box is not None:
            # fuera de la figura: el largo debajo y el alto a la izquierda
            scale = _scaleOf(view)
            halfWidth, halfHeight = (box[1] - box[0]) * scale / 2, (box[3] - box[2]) * scale / 2
            for dim in created:
                if dim.Type == "DistanceX":
                    dim.X, dim.Y = 0, -(halfHeight + _DIMENSION_GAP)
                else:
                    dim.X, dim.Y = -(halfWidth + _DIMENSION_GAP), 0
        doc.recompute()
    except Exception as error:
        print(f"[DAV] Error: no se pudieron crear las cotas totales: {error}")
        return
    print(f"[DAV] Cotas totales (largo y alto) en '{view.Label}'.")
