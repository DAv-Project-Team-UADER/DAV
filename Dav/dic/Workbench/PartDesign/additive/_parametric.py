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

"""Parametric additive commands for Validator (numbers and objects)."""

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


def _SketchFromShape(Doc, Source, Name: str):
    """Copy a flat Part shape's edges into a new Sketcher object.

    PartDesign features need a ``Sketcher::SketchObject`` profile, but the DAV
    geometry commands produce loose ``Part::Feature`` objects. This rebuilds
    the outline as a sketch so shapes dictated by voice can be padded directly.

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
    """Return a padable profile for Target, converting a Part shape if needed."""
    if Target is None:
        return None
    if Target.isDerivedFrom("Sketcher::SketchObject"):
        return Target
    return _SketchFromShape(Doc, Target, f"{Target.Name}Profile")


def _SelectedOrActive(Doc):
    """Return the current selection, falling back to the active object."""
    try:
        selection = Gui.Selection.getSelection()
    except Exception:
        selection = []
    if selection:
        return selection[0]
    return getattr(Doc, "ActiveObject", None)


def pad_by_length(length: float) -> None:
    """Extrude the selected 2D profile by a dictated length.

    This is the voice path from a flat shape to a solid: draw a square with the
    Sketcher geometry commands, select it, and say the height. Unlike ``pad``,
    no FreeCAD dialog is opened -- the length comes from the prompt, so the
    whole flow runs without mouse or keyboard.

    A loose ``Part::Feature`` (what the DAV geometry commands create) is
    converted to a sketch first, since PartDesign only pads sketches.

    Args:
        length: Extrusion height, in millimetres. Must be greater than zero.

    Example::

        pad_by_length(30)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    if length <= 0:
        print(f"[additive] Error: length must be greater than zero (got {length}).")
        return

    target = _SelectedOrActive(doc)
    if target is None:
        print("[additive] Error: select a 2D profile to extrude first.")
        return

    profile = _ResolveProfile(doc, target)
    if profile is None:
        print(f"[additive] Error: '{getattr(target, 'Name', target)}' has no usable outline.")
        return

    # el perfil plano ya no aporta nada visual una vez que hay solido
    if target is not profile:
        target.Visibility = False

    _PadProfile(doc, profile, length)


def _BodyOf(doc, profile):
    """Return the Body that owns profile, else the active Body, else a new one."""
    body = profile.getParentGeoFeatureGroup()
    if body is not None and body.isDerivedFrom("PartDesign::Body"):
        return body
    try:
        import FreeCADGui as Gui

        body = Gui.activeView().getActiveObject("pdbody")
    except Exception:
        body = None
    if body is None:
        body = doc.addObject("PartDesign::Body", "Body")
    body.addObject(profile)
    return body


def _discard(doc, feature) -> None:
    """Remove a feature that failed to compute, so it does not break the model."""
    try:
        doc.removeObject(feature.Name)
        doc.recompute()
    except Exception:
        pass


def _revolveProfile(doc, profile, angle: float):
    """Revolve profile about its own vertical axis, inside its Body.

    Sin un eje de giro la Revolución queda inválida, así que se usa el eje
    vertical del boceto (``V_Axis``): el perfil se dibuja a un lado de ese eje,
    con x como radio e y a lo largo de la pieza.

    Args:
        doc: Active FreeCAD document.
        profile: Sketch holding the closed profile.
        angle: Sweep angle, in degrees (1 to 360).

    Returns:
        The ``PartDesign::Revolution`` feature, or None when it could not be
        built (for instance a profile that crosses the axis).
    """
    body = _BodyOf(doc, profile)
    revolution = body.newObject("PartDesign::Revolution", "Revolution")
    revolution.Profile = profile
    revolution.ReferenceAxis = (profile, ["V_Axis"])
    revolution.Angle = angle
    doc.recompute()

    if not revolution.isValid():
        _discard(doc, revolution)
        print(
            f"[additive] Error: could not revolve '{profile.Name}'. The profile must be "
            "a closed figure on one side of the sketch's vertical axis."
        )
        return None
    try:
        profile.Visibility = False
    except Exception:
        pass
    _RegisterObject(revolution)
    print(f"[additive] Revolved '{profile.Name}' by {angle} degrees")
    return revolution


def _PadProfile(doc, profile, length: float) -> None:
    """Pad profile by length inside its Body and register the result."""
    if profile.GeometryCount == 0:
        print(f"[additive] Error: el boceto '{profile.Name}' está vacío; dibujá una figura cerrada primero.")
        return
    body = _BodyOf(doc, profile)

    pad = body.newObject("PartDesign::Pad", "Pad")
    pad.Profile = profile
    pad.Length = length
    doc.recompute()

    if not pad.isValid():
        _discard(doc, pad)
        print(f"[additive] Error: could not pad '{profile.Name}' (is the sketch a closed profile?).")
        return

    try:
        profile.Visibility = False
    except Exception:
        pass
    _RegisterObject(pad)
    print(f"[additive] Padded '{profile.Name}' by {length}")


def pad_choose_sketch() -> None:
    """Extrude a sketch chosen by voice among the existing ones.

    Opens the DAV object selector restricted to sketches (say "next" to move
    to the following one, "okey" to pick it), then asks the height and pads
    the sketch inside its Body. No native FreeCAD dialog is involved.

    Example::

        pad_choose_sketch()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return

    sketch = askSketch(doc, "Extruir")
    if sketch is None:
        print("[additive] Extrusion cancelled.")
        return

    length = askNumber("Extruir", "Decí la altura de extrusión en mm")
    if length is None:
        print("[additive] Extrusion cancelled.")
        return
    if length <= 0:
        print(f"[additive] Error: length must be greater than zero (got {length}).")
        return

    profile = _ResolveProfile(doc, sketch)
    if profile is None:
        print(f"[additive] Error: '{sketch.Name}' has no usable outline.")
        return
    if profile is not sketch:
        sketch.Visibility = False
    _PadProfile(doc, profile, length)


def revolve_choose_sketch() -> None:
    """Revolve a sketch chosen by voice among the existing ones.

    Example::

        revolve_choose_sketch()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return

    sketch = askSketch(doc, "Revolución")
    if sketch is None:
        print("[additive] Revolution cancelled.")
        return

    angle = askNumber("Revolución", "Decí el ángulo de giro en grados (1 a 360)")
    if angle is None:
        print("[additive] Revolution cancelled.")
        return
    if angle <= 0 or angle > 360:
        print(f"[additive] Error: angle must be between 0 and 360 (got {angle}).")
        return

    profile = _ResolveProfile(doc, sketch)
    if profile is None:
        print(f"[additive] Error: '{sketch.Name}' has no usable outline.")
        return
    if profile is not sketch:
        sketch.Visibility = False
    if profile.GeometryCount == 0:
        print(f"[additive] Error: el boceto '{profile.Name}' está vacío; dibujá una figura primero.")
        return

    _revolveProfile(doc, profile, angle)


def box_by_size(length: float, width: float, height: float) -> None:
    """Create a box from three dictated dimensions.

    Skips the sketch entirely: useful when the goal is a plain cube and there
    is no profile to extrude. Say three equal values to get a cube.

    Args:
        length: Size along X, in millimetres.
        width: Size along Y, in millimetres.
        height: Size along Z, in millimetres.

    Example::

        box_by_size(20, 20, 20)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    if length <= 0 or width <= 0 or height <= 0:
        print("[additive] Error: every dimension must be greater than zero.")
        return

    body = doc.addObject("PartDesign::Body", "Body")
    box = doc.addObject("PartDesign::AdditiveBox", "Box")
    box.Length = length
    box.Width = width
    box.Height = height
    body.addObject(box)

    doc.recompute()
    _RegisterObject(box)
    print(f"[additive] Created box {length} x {width} x {height}")


def cylinder_by_size(radius: float, height: float) -> None:
    """Create a cylinder from a dictated radius and height.

    Args:
        radius: Base radius, in millimetres.
        height: Cylinder height, in millimetres.

    Example::

        cylinder_by_size(10, 40)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    if radius <= 0 or height <= 0:
        print("[additive] Error: radius and height must be greater than zero.")
        return

    body = doc.addObject("PartDesign::Body", "Body")
    cylinder = doc.addObject("PartDesign::AdditiveCylinder", "Cylinder")
    cylinder.Radius = radius
    cylinder.Height = height
    body.addObject(cylinder)

    doc.recompute()
    _RegisterObject(cylinder)
    print(f"[additive] Created cylinder radius {radius} height {height}")


def revolve_by_angle(angle: float) -> None:
    """Revolve the selected 2D profile by a dictated angle.

    Args:
        angle: Sweep angle, in degrees. Must be between 0 and 360.

    Example::

        revolve_by_angle(180)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    if angle <= 0 or angle > 360:
        print(f"[additive] Error: angle must be between 0 and 360 (got {angle}).")
        return

    target = _SelectedOrActive(doc)
    if target is None:
        print("[additive] Error: select a 2D profile to revolve first.")
        return

    profile = _ResolveProfile(doc, target)
    if profile is None:
        print(f"[additive] Error: '{getattr(target, 'Name', target)}' has no usable outline.")
        return

    if _revolveProfile(doc, profile, angle) is not None and target is not profile:
        target.Visibility = False


def pad_sketch(sketch: object, length: float = 10.0) -> None:
    """Select a sketch and launch PartDesign Pad.

    Kept for the interactive path: this opens FreeCAD's own Pad dialog, so the
    height is typed rather than dictated. Use ``pad_by_length`` to stay on
    voice.

    Args:
        sketch: Sketch object to pad.
        length: Unused; the dialog owns the length. See ``pad_by_length``.
    """
    Gui.Selection.clearSelection()
    Gui.Selection.addSelection(sketch)
    Gui.runCommand("PartDesign_Pad", 0)
    print(f"[additive] Pad dialog opened on '{getattr(sketch, 'Name', sketch)}'")


def loft_profiles(profile_a: object, profile_b: object) -> None:
    """Select two profiles and launch additive loft."""
    Gui.Selection.clearSelection()
    Gui.Selection.addSelection(profile_a)
    Gui.Selection.addSelection(profile_b)
    Gui.runCommand("PartDesign_AdditiveLoft", 0)
    print(
        "[additive] Loft between "
        f"'{getattr(profile_a, 'Name', profile_a)}' and "
        f"'{getattr(profile_b, 'Name', profile_b)}'"
    )


def sphere_by_radius(radius: float) -> None:
    """Create a sphere from a dictated radius.

    Args:
        radius: Sphere radius, in millimetres.

    Example::

        sphere_by_radius(15)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    if radius <= 0:
        print(f"[additive] Error: radius must be greater than zero (got {radius}).")
        return

    body = doc.addObject("PartDesign::Body", "Body")
    sphere = doc.addObject("PartDesign::AdditiveSphere", "Sphere")
    sphere.Radius = radius
    body.addObject(sphere)

    doc.recompute()
    _RegisterObject(sphere)
    print(f"[additive] Created sphere radius {radius}")


def cone_by_size(radius1: float, radius2: float, height: float) -> None:
    """Create a cone from two dictated radii and a height.

    Say a second radius of zero for a sharp tip, or two different radii for a
    truncated cone.

    Args:
        radius1: Bottom radius, in millimetres.
        radius2: Top radius, in millimetres. Zero gives a sharp tip.
        height: Cone height, in millimetres.

    Example::

        cone_by_size(10, 0, 25)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    if radius1 < 0 or radius2 < 0:
        print("[additive] Error: radii cannot be negative.")
        return
    if radius1 == radius2:
        print("[additive] Error: the two radii must differ; use a cylinder instead.")
        return
    if height <= 0:
        print(f"[additive] Error: height must be greater than zero (got {height}).")
        return

    body = doc.addObject("PartDesign::Body", "Body")
    cone = doc.addObject("PartDesign::AdditiveCone", "Cone")
    cone.Radius1 = radius1
    cone.Radius2 = radius2
    cone.Height = height
    body.addObject(cone)

    doc.recompute()
    _RegisterObject(cone)
    print(f"[additive] Created cone radii {radius1}/{radius2} height {height}")


def torus_by_size(radius1: float, radius2: float) -> None:
    """Create a torus from a dictated ring radius and tube radius.

    Args:
        radius1: Ring radius (centre to tube centre), in millimetres.
        radius2: Tube radius, in millimetres. Must be smaller than radius1.

    Example::

        torus_by_size(20, 5)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    if radius1 <= 0 or radius2 <= 0:
        print("[additive] Error: both radii must be greater than zero.")
        return
    # con el tubo mas grueso que el anillo el toro se auto-interseca
    if radius2 >= radius1:
        print(
            f"[additive] Error: the tube radius ({radius2}) must be smaller "
            f"than the ring radius ({radius1})."
        )
        return

    body = doc.addObject("PartDesign::Body", "Body")
    torus = doc.addObject("PartDesign::AdditiveTorus", "Torus")
    torus.Radius1 = radius1
    torus.Radius2 = radius2
    body.addObject(torus)

    doc.recompute()
    _RegisterObject(torus)
    print(f"[additive] Created torus ring {radius1} tube {radius2}")


def prism_by_size(sides: int, circumradius: float, height: float) -> None:
    """Create a prism from a dictated side count, radius and height.

    Args:
        sides: Number of sides of the base polygon. Must be 3 or more.
        circumradius: Centre-to-vertex radius of the base, in millimetres.
        height: Prism height, in millimetres.

    Example::

        prism_by_size(6, 10, 30)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    if sides < 3:
        print(f"[additive] Error: a prism needs at least 3 sides (got {sides}).")
        return
    if circumradius <= 0 or height <= 0:
        print("[additive] Error: radius and height must be greater than zero.")
        return

    body = doc.addObject("PartDesign::Body", "Body")
    prism = doc.addObject("PartDesign::AdditivePrism", "Prism")
    prism.Polygon = sides
    prism.Circumradius = circumradius
    prism.Height = height
    body.addObject(prism)

    doc.recompute()
    _RegisterObject(prism)
    print(f"[additive] Created prism of {sides} sides radius {circumradius} height {height}")
