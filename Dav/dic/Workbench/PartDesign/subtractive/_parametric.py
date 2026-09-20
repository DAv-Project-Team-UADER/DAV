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

"""Parametric subtractive commands for Validator (numbers and objects)."""

from __future__ import annotations

import FreeCAD as App
import FreeCADGui as Gui

from ..._display import showResult
from ..._prompts import askNumber, askSketch
from ...Sketcher.Geometry._sketch import shapeToSketchGeometry
from .._placement import chooseBody, placeAt


def _RegisterObject(Feature) -> None:
    """Show a created feature and register it in the DAV navigable object tree."""
    showResult(Feature)
    try:
        from createobjects import CreateObjects
    except ImportError:
        from selection.createobjects import CreateObjects
    CreateObjects(ObjectName=Feature.Name, Is3D=True).Execute()


def _SelectedOrActive(Doc):
    """Return the current selection, falling back to the active object."""
    try:
        selection = Gui.Selection.getSelection()
    except Exception:
        selection = []
    if selection:
        return selection[0]
    return getattr(Doc, "ActiveObject", None)


def _SketchFromShape(Doc, Source, Name: str):
    """Copy a flat Part shape's edges into a new Sketcher object.

    Same conversion used by the additive commands: PartDesign only cuts with a
    ``Sketcher::SketchObject`` profile, while the DAV geometry commands produce
    loose ``Part::Feature`` objects.

    Args:
        Doc: Active FreeCAD document.
        Source: Object whose ``Shape`` edges are copied.
        Name: Internal name for the new sketch.

    Returns:
        The created sketch, or None when Source carries no usable geometry.
    """
    shape = getattr(Source, "Shape", None)
    if shape is None or not shape.Edges:
        return None

    sketch = Doc.addObject("Sketcher::SketchObject", Name)
    geometry = shapeToSketchGeometry(shape)
    if not geometry:
        Doc.removeObject(sketch.Name)
        return None
    sketch.addGeometry(geometry, False)
    return sketch


def _ResolveProfile(Doc, Target):
    """Return a usable profile for Target, converting a Part shape if needed."""
    if Target is None:
        return None
    if Target.isDerivedFrom("Sketcher::SketchObject"):
        return Target
    return _SketchFromShape(Doc, Target, f"{Target.Name}Profile")


def _OwningBody(Doc, Profile):
    """Return the body that owns Profile, else the active body, else a new one."""
    for obj in Doc.Objects:
        if obj.isDerivedFrom("PartDesign::Body") and Profile in obj.Group:
            return obj
    try:
        body = Gui.activeView().getActiveObject("pdbody")
    except Exception:
        body = None
    if body is None:
        body = Doc.addObject("PartDesign::Body", "Body")
    body.addObject(Profile)
    return body


def pocket_by_length(length: float) -> None:
    """Cut a pocket into the body using the selected profile and a dictated depth.

    The subtractive counterpart of ``pad_by_length``: instead of adding
    material it removes it, so a square on a face becomes a square hollow.

    Args:
        length: Cut depth, in millimetres. Must be greater than zero.

    Example::

        pocket_by_length(10)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if length <= 0:
        print(f"[subtractive] Error: length must be greater than zero (got {length}).")
        return

    target = _SelectedOrActive(doc)
    if target is None:
        print("[subtractive] Error: select a 2D profile to cut with first.")
        return

    profile = _ResolveProfile(doc, target)
    if profile is None:
        print(f"[subtractive] Error: '{getattr(target, 'Name', target)}' has no usable outline.")
        return

    body = _OwningBody(doc, profile)

    pocket = doc.addObject("PartDesign::Pocket", "Pocket")
    pocket.Profile = profile
    pocket.Length = length
    body.addObject(pocket)

    doc.recompute()
    _RegisterObject(pocket)
    print(f"[subtractive] Pocketed '{profile.Name}' by {length}")


def _discardHole(doc, *objects) -> None:
    """Remove the objects of a hole that did not work, so the model stays clean."""
    for obj in objects:
        try:
            doc.removeObject(obj.Name)
        except Exception:
            pass
    try:
        doc.recompute()
    except Exception:
        pass


def _drillHole(doc, label: str, diameter: float, depth, x: float, y: float, z: float) -> bool:
    """Drill a hole down from (x, y, z) into a solid chosen by voice, with no prior sketch.

    Se dibuja solo el boceto con un círculo en (x, y) sobre un plano a la altura
    z, dentro del Body, y sobre él se crea el agujero. El agujero corta en
    sentido -Z (hacia adentro de una cara superior): si así no saca material
    se invierte, para que también funcione desde una cara inferior.

    Args:
        doc: Active FreeCAD document.
        label: Name of the hole feature.
        diameter: Hole diameter, in millimetres.
        depth: Hole depth in millimetres, or None to drill through the whole solid.
        x: X of the hole axis, in millimetres.
        y: Y of the hole axis.
        z: Z of the plane where the hole starts.

    Returns:
        True when the hole removed material.
    """
    import Part

    body = chooseBody(doc, "Agujero")
    if body is None:
        return False

    before = body.Shape.Volume
    # el boceto y el agujero se crean dentro del Body: fuera de uno, FreeCAD
    # rechaza el perfil con "No base set, no sketch support either"
    sketch = body.newObject("Sketcher::SketchObject", f"{label}Sketch")
    sketch.Placement = App.Placement(App.Vector(0, 0, z), App.Rotation())
    sketch.addGeometry(
        Part.Circle(App.Vector(x, y, 0), App.Vector(0, 0, 1), diameter / 2), False
    )
    hole = body.newObject("PartDesign::Hole", label)
    hole.Profile = sketch
    # ThreadType 0 = sin rosca; DrillPoint 0 = fondo plano. DepthType en
    # FreeCAD 1.x: 0 = Dimension (usa Depth), 1 = ThroughAll (ignora Depth).
    hole.ThreadType = 0
    hole.DrillPoint = 0
    hole.Diameter = diameter
    if depth is None:
        hole.DepthType = 1
    else:
        hole.DepthType = 0
        hole.Depth = depth

    doc.recompute()
    if hole.isValid() and abs(body.Shape.Volume - before) < 1e-6:
        hole.Reversed = True
        doc.recompute()
    if not hole.isValid() or abs(body.Shape.Volume - before) < 1e-6:
        _discardHole(doc, hole, sketch)
        print(
            f"[subtractive] Error: the hole at ({x}, {y}, {z}) removed no material; "
            "check that the point is over the solid."
        )
        return False

    sketch.Visibility = False
    _RegisterObject(hole)
    return True


def hole_by_size(diameter: float, x: float, y: float, z: float) -> None:
    """Drill a through hole from a dictated point, without drawing a sketch first.

    The hole starts at height z and goes down (-Z) through the whole solid; if
    that removes nothing it is flipped to go up. Use the height of the face
    you want to drill from.

    Args:
        diameter: Hole diameter, in millimetres.
        x: X of the hole axis, in millimetres.
        y: Y of the hole axis.
        z: Z of the face where the hole starts.

    Example::

        hole_by_size(6, 10, 10, 20)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if diameter <= 0:
        print(f"[subtractive] Error: diameter must be greater than zero (got {diameter}).")
        return
    if _drillHole(doc, "Hole", diameter, None, x, y, z):
        print(f"[subtractive] Drilled a through hole of diameter {diameter} at ({x}, {y}, {z})")


def groove_by_angle(angle: float) -> None:
    """Cut a groove by revolving the selected profile a dictated angle.

    Args:
        angle: Sweep angle, in degrees. Must be between 0 and 360.

    Example::

        groove_by_angle(90)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if angle <= 0 or angle > 360:
        print(f"[subtractive] Error: angle must be between 0 and 360 (got {angle}).")
        return

    target = _SelectedOrActive(doc)
    if target is None:
        print("[subtractive] Error: select a 2D profile to groove with first.")
        return

    profile = _ResolveProfile(doc, target)
    if profile is None:
        print(f"[subtractive] Error: '{getattr(target, 'Name', target)}' has no usable outline.")
        return

    body = _OwningBody(doc, profile)

    groove = doc.addObject("PartDesign::Groove", "Groove")
    groove.Profile = profile
    groove.Angle = angle
    body.addObject(groove)

    doc.recompute()
    _RegisterObject(groove)
    print(f"[subtractive] Grooved '{profile.Name}' by {angle} degrees")


def _finishFeature(doc, feature, profile) -> bool:
    """Recompute, verify the feature is valid and register it in the DAV tree."""
    doc.recompute()
    if not feature.isValid():
        try:
            doc.removeObject(feature.Name)
            doc.recompute()
        except Exception:
            pass
        print(f"[subtractive] Error: could not cut with '{profile.Name}' (needs a closed profile on the body).")
        return False
    try:
        profile.Visibility = False
    except Exception:
        pass
    _RegisterObject(feature)
    return True


def blind_hole_by_size(diameter: float, depth: float, x: float, y: float, z: float) -> None:
    """Drill a blind (non-through) hole from a dictated point, with no sketch first.

    The hole starts at height z, goes down (-Z) for the dictated depth and has
    a flat bottom. If that removes nothing it is flipped to go up.

    Args:
        diameter: Hole diameter, in millimetres.
        depth: Hole depth, in millimetres.
        x: X of the hole axis, in millimetres.
        y: Y of the hole axis.
        z: Z of the face where the hole starts.

    Example::

        blind_hole_by_size(4, 2, 10, 10, 20)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if diameter <= 0 or depth <= 0:
        print("[subtractive] Error: diameter and depth must be greater than zero.")
        return
    if _drillHole(doc, "BlindHole", diameter, depth, x, y, z):
        print(
            f"[subtractive] Drilled a blind hole of diameter {diameter} and depth {depth} "
            f"at ({x}, {y}, {z})"
        )


def _profileFor(doc, chosen):
    """Return a sketch for the chosen drawing (converting a loose shape), or None."""
    profile = _ResolveProfile(doc, chosen)
    if profile is None or profile.GeometryCount == 0:
        print(f"[subtractive] Error: '{chosen.Name}' has no usable outline.")
        return None
    if profile is not chosen:
        chosen.Visibility = False
    return profile


def pocket_choose_sketch() -> None:
    """Cut a pocket with a sketch chosen by voice and a dictated depth."""
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    sketch = askSketch(doc, "Vaciado")
    if sketch is None:
        print("[subtractive] Pocket cancelled.")
        return
    length = askNumber("Vaciado", "Decí la profundidad del vaciado en mm")
    if length is None:
        print("[subtractive] Pocket cancelled.")
        return
    if length <= 0:
        print(f"[subtractive] Error: depth must be greater than zero (got {length}).")
        return

    sketch = _profileFor(doc, sketch)
    if sketch is None:
        return
    body = _OwningBody(doc, sketch)
    pocket = body.newObject("PartDesign::Pocket", "Pocket")
    pocket.Profile = sketch
    pocket.Length = length
    if _finishFeature(doc, pocket, sketch):
        print(f"[subtractive] Pocketed '{sketch.Name}' by {length}")


def hole_choose_sketch() -> None:
    """Drill a hole at a sketch chosen by voice, with dictated diameter and depth.

    The sketch must hold the circle(s) or point(s) where the hole goes.
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    sketch = askSketch(doc, "Agujero")
    if sketch is None:
        print("[subtractive] Hole cancelled.")
        return
    diameter = askNumber("Agujero", "Decí el diámetro del agujero en mm")
    if diameter is None:
        print("[subtractive] Hole cancelled.")
        return
    depth = askNumber("Agujero", "Decí la profundidad del agujero en mm")
    if depth is None:
        print("[subtractive] Hole cancelled.")
        return
    if diameter <= 0 or depth <= 0:
        print("[subtractive] Error: diameter and depth must be greater than zero.")
        return

    sketch = _profileFor(doc, sketch)
    if sketch is None:
        return
    body = _OwningBody(doc, sketch)
    hole = body.newObject("PartDesign::Hole", "Hole")
    hole.Profile = sketch
    # ThreadType 0 = sin rosca; DepthType 0 = Dimension (usa Depth). El valor 1
    # es ThroughAll y ignoraria la profundidad dictada.
    hole.ThreadType = 0
    hole.DepthType = 0
    hole.Diameter = diameter
    hole.Depth = depth
    if _finishFeature(doc, hole, sketch):
        print(f"[subtractive] Drilled a hole of diameter {diameter} and depth {depth}")


def groove_choose_sketch() -> None:
    """Cut a groove revolving a sketch chosen by voice by a dictated angle."""
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    sketch = askSketch(doc, "Ranura")
    if sketch is None:
        print("[subtractive] Groove cancelled.")
        return
    angle = askNumber("Ranura", "Decí el ángulo de giro en grados (1 a 360)")
    if angle is None:
        print("[subtractive] Groove cancelled.")
        return
    if angle <= 0 or angle > 360:
        print(f"[subtractive] Error: angle must be between 0 and 360 (got {angle}).")
        return

    sketch = _profileFor(doc, sketch)
    if sketch is None:
        return
    body = _OwningBody(doc, sketch)
    groove = body.newObject("PartDesign::Groove", "Groove")
    groove.Profile = sketch
    groove.Angle = angle
    if _finishFeature(doc, groove, sketch):
        print(f"[subtractive] Grooved '{sketch.Name}' by {angle} degrees")


def _cutPrimitive(doc, typeId: str, label: str, properties: dict, center, shift, text: str) -> None:
    """Cut a primitive out of a solid chosen by voice, centred on a dictated point.

    Args:
        doc: Active FreeCAD document.
        typeId: FreeCAD type, e.g. ``PartDesign::SubtractiveBox``.
        label: Name used for the created object.
        properties: Property values to set, e.g. ``{"Radius": 5}``.
        center: ``(x, y, z)`` where the centre of the figure goes.
        shift: ``(dx, dy, dz)`` from the primitive's own origin to its centre.
        text: Description printed on success.
    """
    body = chooseBody(doc, "Corte")
    if body is None:
        return

    before = body.Shape.Volume
    feature = doc.addObject(typeId, label)
    body.addObject(feature)
    for name, value in properties.items():
        setattr(feature, name, value)
    x, y, z = center
    placeAt(body, feature, x - shift[0], y - shift[1], z - shift[2])

    doc.recompute()
    if not feature.isValid() or abs(body.Shape.Volume - before) < 1e-6:
        _discardHole(doc, feature)
        print(
            f"[subtractive] Error: {text} at ({x}, {y}, {z}) removed no material; "
            "check that it overlaps the solid."
        )
        return
    _RegisterObject(feature)
    print(f"[subtractive] Cut {text} at ({x}, {y}, {z})")


def cut_box_by_size(
    length: float, width: float, height: float, x: float, y: float, z: float
) -> None:
    """Cut a box-shaped pocket out of the current solid, centred on a point.

    Args:
        length: Size along X, in millimetres.
        width: Size along Y, in millimetres.
        height: Size along Z, in millimetres.
        x: X of the box centre, in millimetres.
        y: Y of the box centre.
        z: Z of the box centre.

    Example::

        cut_box_by_size(10, 10, 20, 0, 0, 10)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if length <= 0 or width <= 0 or height <= 0:
        print("[subtractive] Error: every dimension must be greater than zero.")
        return
    _cutPrimitive(
        doc, "PartDesign::SubtractiveBox", "CutBox",
        {"Length": length, "Width": width, "Height": height},
        (x, y, z), (length / 2, width / 2, height / 2),
        f"a box {length} x {width} x {height}",
    )


def cut_cylinder_by_size(radius: float, height: float, x: float, y: float, z: float) -> None:
    """Cut a cylindrical pocket out of the current solid, centred on a point.

    Args:
        radius: Cut radius, in millimetres.
        height: Cut height, in millimetres.
        x: X of the cylinder axis, in millimetres.
        y: Y of the cylinder axis.
        z: Z of the cylinder centre (halfway up its height).

    Example::

        cut_cylinder_by_size(5, 20, 0, 0, 10)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if radius <= 0 or height <= 0:
        print("[subtractive] Error: radius and height must be greater than zero.")
        return
    _cutPrimitive(
        doc, "PartDesign::SubtractiveCylinder", "CutCylinder",
        {"Radius": radius, "Height": height},
        (x, y, z), (0, 0, height / 2),
        f"a cylinder radius {radius} height {height}",
    )


def cut_sphere_by_radius(radius: float, x: float, y: float, z: float) -> None:
    """Cut a spherical pocket out of the current solid, centred on a point.

    Args:
        radius: Cut radius, in millimetres.
        x: X of the sphere centre, in millimetres.
        y: Y of the sphere centre.
        z: Z of the sphere centre.

    Example::

        cut_sphere_by_radius(8, 0, 0, 10)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if radius <= 0:
        print(f"[subtractive] Error: radius must be greater than zero (got {radius}).")
        return
    _cutPrimitive(
        doc, "PartDesign::SubtractiveSphere", "CutSphere",
        {"Radius": radius}, (x, y, z), (0, 0, 0), f"a sphere radius {radius}",
    )


def cut_cone_by_size(
    radius1: float, radius2: float, height: float, x: float, y: float, z: float
) -> None:
    """Cut a conical pocket out of the current solid, centred on a point.

    Args:
        radius1: Bottom radius, in millimetres.
        radius2: Top radius, in millimetres. Zero gives a sharp tip.
        height: Cone height, in millimetres.
        x: X of the cone axis, in millimetres.
        y: Y of the cone axis.
        z: Z of the cone centre (halfway up its height).

    Example::

        cut_cone_by_size(10, 0, 25, 0, 0, 12.5)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if radius1 < 0 or radius2 < 0 or radius1 == radius2 or height <= 0:
        print("[subtractive] Error: radii must be zero or more and different, and height greater than zero.")
        return
    _cutPrimitive(
        doc, "PartDesign::SubtractiveCone", "CutCone",
        {"Radius1": radius1, "Radius2": radius2, "Height": height},
        (x, y, z), (0, 0, height / 2),
        f"a cone radii {radius1}/{radius2} height {height}",
    )


def cut_torus_by_size(radius1: float, radius2: float, x: float, y: float, z: float) -> None:
    """Cut a torus-shaped pocket out of the current solid, centred on a point.

    Args:
        radius1: Ring radius (centre to tube centre), in millimetres.
        radius2: Tube radius, in millimetres. Must be smaller than radius1.
        x: X of the torus centre, in millimetres.
        y: Y of the torus centre.
        z: Z of the torus centre.

    Example::

        cut_torus_by_size(20, 5, 0, 0, 10)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if radius1 <= 0 or radius2 <= 0 or radius2 >= radius1:
        print("[subtractive] Error: both radii must be greater than zero and the tube smaller than the ring.")
        return
    _cutPrimitive(
        doc, "PartDesign::SubtractiveTorus", "CutTorus",
        {"Radius1": radius1, "Radius2": radius2}, (x, y, z), (0, 0, 0),
        f"a torus ring {radius1} tube {radius2}",
    )


def cut_prism_by_size(
    sides: int, circumradius: float, height: float, x: float, y: float, z: float
) -> None:
    """Cut a prism-shaped pocket out of the current solid, centred on a point.

    Args:
        sides: Number of sides of the base polygon. Must be 3 or more.
        circumradius: Centre-to-vertex radius of the base, in millimetres.
        height: Prism height, in millimetres.
        x: X of the prism axis, in millimetres.
        y: Y of the prism axis.
        z: Z of the prism centre (halfway up its height).

    Example::

        cut_prism_by_size(6, 10, 30, 0, 0, 15)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if sides < 3 or circumradius <= 0 or height <= 0:
        print("[subtractive] Error: a prism needs 3 or more sides, and a radius and height above zero.")
        return
    _cutPrimitive(
        doc, "PartDesign::SubtractivePrism", "CutPrism",
        {"Polygon": sides, "Circumradius": circumradius, "Height": height},
        (x, y, z), (0, 0, height / 2),
        f"a prism of {sides} sides radius {circumradius} height {height}",
    )
