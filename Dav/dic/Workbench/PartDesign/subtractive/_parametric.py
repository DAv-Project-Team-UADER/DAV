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


def hole_by_size(diameter: float, depth: float) -> None:
    """Drill a hole using the selected circular profile and dictated measures.

    Args:
        diameter: Hole diameter, in millimetres.
        depth: Hole depth, in millimetres.

    Example::

        hole_by_size(6, 25)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if diameter <= 0 or depth <= 0:
        print("[subtractive] Error: diameter and depth must be greater than zero.")
        return

    target = _SelectedOrActive(doc)
    if target is None:
        print("[subtractive] Error: select a circular profile to drill first.")
        return

    profile = _ResolveProfile(doc, target)
    if profile is None:
        print(f"[subtractive] Error: '{getattr(target, 'Name', target)}' has no usable outline.")
        return

    body = _OwningBody(doc, profile)

    hole = doc.addObject("PartDesign::Hole", "Hole")
    hole.Profile = profile
    # ThreadType 0 = sin rosca; DepthType 1 = profundidad explicita en Depth,
    # si se deja en 0 ("hasta el final") FreeCAD ignora el valor dictado.
    hole.ThreadType = 0
    hole.DepthType = 1
    hole.Diameter = diameter
    hole.Depth = depth
    body.addObject(hole)

    doc.recompute()
    _RegisterObject(hole)
    print(f"[subtractive] Drilled a hole of diameter {diameter} and depth {depth}")


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


def _pendingSketch(doc):
    """Return the sketch to drill: the selected/active one, else the newest unused one.

    Args:
        doc: Active FreeCAD document.

    Returns:
        A ``Sketcher::SketchObject`` with geometry, or None when there is none.
    """
    target = _SelectedOrActive(doc)
    if target is not None and target.isDerivedFrom("Sketcher::SketchObject"):
        return target
    for sketch in reversed(doc.Objects):
        if not sketch.isDerivedFrom("Sketcher::SketchObject") or sketch.GeometryCount == 0:
            continue
        # se descartan los que ya alimentan otra operacion (pad, agujero, etc.)
        used = [o for o in sketch.InList if o.isDerivedFrom("PartDesign::Feature")]
        if not used:
            return sketch
    return None


def _bodyOfSketch(doc, sketch):
    """Return the Body that must receive a feature built on ``sketch``, or None."""
    body = sketch.getParentGeoFeatureGroup()
    if body is not None and body.isDerivedFrom("PartDesign::Body"):
        return body
    try:
        body = Gui.activeView().getActiveObject("pdbody")
    except Exception:
        body = None
    if body is None:
        bodies = [o for o in doc.Objects if o.isDerivedFrom("PartDesign::Body")]
        body = bodies[-1] if bodies else None
    if body is not None:
        body.addObject(sketch)
    return body


def blind_hole_by_size(diameter: float, depth: float) -> None:
    """Drill a blind (non-through) hole at every circle of the sketch.

    The hole stops at the dictated depth and has a flat bottom. The sketch is
    the selected one or, failing that, the newest sketch not yet used; its
    circle centres say where each hole goes. If the hole would point out of
    the solid, its direction is flipped automatically.

    Args:
        diameter: Hole diameter, in millimetres.
        depth: Hole depth, in millimetres.

    Example::

        blind_hole_by_size(4, 2)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if diameter <= 0 or depth <= 0:
        print("[subtractive] Error: diameter and depth must be greater than zero.")
        return

    sketch = _pendingSketch(doc)
    if sketch is None:
        print("[subtractive] Error: draw the hole centres in a sketch first.")
        return
    body = _bodyOfSketch(doc, sketch)
    if body is None:
        print("[subtractive] Error: create a solid first; there is nothing to drill.")
        return

    # el agujero se crea dentro del Body antes de asignarle el perfil: fuera
    # de un Body, FreeCAD rechaza el perfil con "No base set"
    hole = body.newObject("PartDesign::Hole", "BlindHole")
    hole.Profile = sketch
    # ThreadType 0 = sin rosca. En FreeCAD 1.x DepthType es 0 = Dimension
    # (usa Depth) y 1 = ThroughAll (lo ignoraria); DrillPoint 0 = fondo plano.
    hole.ThreadType = 0
    hole.DepthType = 0
    hole.DrillPoint = 0
    hole.Diameter = diameter
    hole.Depth = depth

    before = body.Shape.Volume
    doc.recompute()
    if abs(body.Shape.Volume - before) < 1e-6:
        # el Hole corta en sentido contrario a la normal del boceto: si no
        # sacó material, apunta hacia afuera y se invierte
        hole.Reversed = True
        doc.recompute()
    if abs(body.Shape.Volume - before) < 1e-6:
        print("[subtractive] Warning: the hole removed no material; check the sketch position.")
        return

    sketch.Visibility = False
    _RegisterObject(hole)
    print(f"[subtractive] Drilled a blind hole of diameter {diameter} and depth {depth}")


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
    # ThreadType 0 = sin rosca; DepthType 1 = profundidad explicita en Depth,
    # si se deja en 0 ("hasta el final") FreeCAD ignora el valor dictado.
    hole.ThreadType = 0
    hole.DepthType = 1
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


def _CutPrimitive(TypeId: str, Label: str, Doc):
    """Create a subtractive primitive inside the body being edited.

    Args:
        TypeId: FreeCAD type, e.g. ``PartDesign::SubtractiveBox``.
        Label: Name used for the created object.
        Doc: Active FreeCAD document.

    Returns:
        The created feature, or None when there is no body to cut from.
    """
    bodies = [obj for obj in Doc.Objects if obj.isDerivedFrom("PartDesign::Body")]
    if not bodies:
        print("[subtractive] Error: create a solid first; there is nothing to cut from.")
        return None

    # se corta del ultimo cuerpo creado, que es el que el usuario acaba de
    # construir por voz
    body = bodies[-1]
    feature = Doc.addObject(TypeId, Label)
    body.addObject(feature)
    return feature


def cut_box_by_size(length: float, width: float, height: float) -> None:
    """Cut a box-shaped pocket out of the current solid.

    Args:
        length: Size along X, in millimetres.
        width: Size along Y, in millimetres.
        height: Size along Z, in millimetres.

    Example::

        cut_box_by_size(10, 10, 20)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if length <= 0 or width <= 0 or height <= 0:
        print("[subtractive] Error: every dimension must be greater than zero.")
        return

    box = _CutPrimitive("PartDesign::SubtractiveBox", "CutBox", doc)
    if box is None:
        return
    box.Length = length
    box.Width = width
    box.Height = height

    doc.recompute()
    _RegisterObject(box)
    print(f"[subtractive] Cut a box {length} x {width} x {height}")


def cut_cylinder_by_size(radius: float, height: float) -> None:
    """Cut a cylindrical pocket out of the current solid.

    Args:
        radius: Cut radius, in millimetres.
        height: Cut height, in millimetres.

    Example::

        cut_cylinder_by_size(5, 20)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if radius <= 0 or height <= 0:
        print("[subtractive] Error: radius and height must be greater than zero.")
        return

    cylinder = _CutPrimitive("PartDesign::SubtractiveCylinder", "CutCylinder", doc)
    if cylinder is None:
        return
    cylinder.Radius = radius
    cylinder.Height = height

    doc.recompute()
    _RegisterObject(cylinder)
    print(f"[subtractive] Cut a cylinder radius {radius} height {height}")


def cut_sphere_by_radius(radius: float) -> None:
    """Cut a spherical pocket out of the current solid.

    Args:
        radius: Cut radius, in millimetres.

    Example::

        cut_sphere_by_radius(8)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[subtractive] Error: no active document.")
        return
    if radius <= 0:
        print(f"[subtractive] Error: radius must be greater than zero (got {radius}).")
        return

    sphere = _CutPrimitive("PartDesign::SubtractiveSphere", "CutSphere", doc)
    if sphere is None:
        return
    sphere.Radius = radius

    doc.recompute()
    _RegisterObject(sphere)
    print(f"[subtractive] Cut a sphere radius {radius}")
