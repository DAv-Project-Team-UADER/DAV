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
from .._placement import askTwoProfiles, bodyForAdditive, placeAt, sketchEdges


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


def pad_by_length(length: float) -> None:
    """Extrude a 2D profile chosen by voice by a dictated length.

    This is the voice path from a flat shape to a solid: draw a square with the
    Sketcher geometry commands, choose it from the list, and say the height. Unlike ``pad``,
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

    # se pregunta el dibujo: el objeto activo suele ser la última figura creada, no un perfil
    target = askSketch(doc, "Extruir")
    if target is None:
        print("[additive] Extrusion cancelled.")
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


def _RegisterAdditive(doc, feature) -> bool:
    """Register an additive figure, or discard it when it could not join the body.

    Al sumar una figura a un cuerpo existente, FreeCAD exige un único sólido:
    si no toca ni se superpone con el actual la operación falla.

    Returns:
        True when the figure is valid and registered.
    """
    if not feature.isValid():
        _discard(doc, feature)
        print(
            "[additive] Error: la figura no se pudo unir al cuerpo; tiene que tocar "
            "o superponerse con el sólido existente (o creá un cuerpo nuevo)."
        )
        return False
    _RegisterObject(feature)
    return True


def box_by_size(length: float, width: float, height: float, x: float, y: float, z: float) -> None:
    """Create a box from three dictated dimensions and the position of its centre.

    Skips the sketch entirely: useful when the goal is a plain cube and there
    is no profile to extrude. Say three equal values to get a cube.

    Args:
        length: Size along X, in millimetres.
        width: Size along Y, in millimetres.
        height: Size along Z, in millimetres.
        x: X of the box centre, in millimetres.
        y: Y of the box centre.
        z: Z of the box centre.

    Example::

        box_by_size(20, 20, 20, 0, 0, 10)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    if length <= 0 or width <= 0 or height <= 0:
        print("[additive] Error: every dimension must be greater than zero.")
        return

    body = bodyForAdditive(doc, "Nueva figura")
    if body is None:
        return
    box = doc.addObject("PartDesign::AdditiveBox", "Box")
    box.Length = length
    box.Width = width
    box.Height = height
    body.addObject(box)
    # la caja nace con una esquina en el origen: se corre media medida para centrarla
    placeAt(body, box, x - length / 2, y - width / 2, z - height / 2)

    doc.recompute()
    if _RegisterAdditive(doc, box):
        print(f"[additive] Created box {length} x {width} x {height}")


def cylinder_by_size(radius: float, height: float, x: float, y: float, z: float) -> None:
    """Create a cylinder from a dictated radius, height and centre position.

    Args:
        radius: Base radius, in millimetres.
        height: Cylinder height, in millimetres.
        x: X of the cylinder centre, in millimetres.
        y: Y of the cylinder centre.
        z: Z of the cylinder centre (halfway up its height).

    Example::

        cylinder_by_size(10, 40, 0, 0, 20)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    if radius <= 0 or height <= 0:
        print("[additive] Error: radius and height must be greater than zero.")
        return

    body = bodyForAdditive(doc, "Nueva figura")
    if body is None:
        return
    cylinder = doc.addObject("PartDesign::AdditiveCylinder", "Cylinder")
    cylinder.Radius = radius
    cylinder.Height = height
    body.addObject(cylinder)
    # la base nace en el origen: se baja media altura para centrarlo
    placeAt(body, cylinder, x, y, z - height / 2)

    doc.recompute()
    if _RegisterAdditive(doc, cylinder):
        print(f"[additive] Created cylinder radius {radius} height {height}")


def revolve_by_angle(angle: float) -> None:
    """Revolve a 2D profile chosen by voice by a dictated angle.

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

    # se pregunta el dibujo: el objeto activo suele ser la última figura creada, no un perfil
    target = askSketch(doc, "Revolución")
    if target is None:
        print("[additive] Revolution cancelled.")
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


def sphere_by_radius(radius: float, x: float, y: float, z: float) -> None:
    """Create a sphere from a dictated radius and centre position.

    Args:
        radius: Sphere radius, in millimetres.
        x: X of the sphere centre, in millimetres.
        y: Y of the sphere centre.
        z: Z of the sphere centre.

    Example::

        sphere_by_radius(15, 0, 0, 15)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    if radius <= 0:
        print(f"[additive] Error: radius must be greater than zero (got {radius}).")
        return

    body = bodyForAdditive(doc, "Nueva figura")
    if body is None:
        return
    sphere = doc.addObject("PartDesign::AdditiveSphere", "Sphere")
    sphere.Radius = radius
    body.addObject(sphere)
    placeAt(body, sphere, x, y, z)

    doc.recompute()
    if _RegisterAdditive(doc, sphere):
        print(f"[additive] Created sphere radius {radius}")


def cone_by_size(
    radius1: float, radius2: float, height: float, x: float, y: float, z: float
) -> None:
    """Create a cone from two dictated radii, a height and the centre position.

    Say a second radius of zero for a sharp tip, or two different radii for a
    truncated cone.

    Args:
        radius1: Bottom radius, in millimetres.
        radius2: Top radius, in millimetres. Zero gives a sharp tip.
        height: Cone height, in millimetres.
        x: X of the cone axis, in millimetres.
        y: Y of the cone axis.
        z: Z of the cone centre (halfway up its height).

    Example::

        cone_by_size(10, 0, 25, 0, 0, 12.5)
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

    body = bodyForAdditive(doc, "Nueva figura")
    if body is None:
        return
    cone = doc.addObject("PartDesign::AdditiveCone", "Cone")
    cone.Radius1 = radius1
    cone.Radius2 = radius2
    cone.Height = height
    body.addObject(cone)
    placeAt(body, cone, x, y, z - height / 2)

    doc.recompute()
    if _RegisterAdditive(doc, cone):
        print(f"[additive] Created cone radii {radius1}/{radius2} height {height}")


def torus_by_size(radius1: float, radius2: float, x: float, y: float, z: float) -> None:
    """Create a torus from a dictated ring radius, tube radius and centre position.

    Args:
        radius1: Ring radius (centre to tube centre), in millimetres.
        radius2: Tube radius, in millimetres. Must be smaller than radius1.
        x: X of the torus centre, in millimetres.
        y: Y of the torus centre.
        z: Z of the torus centre.

    Example::

        torus_by_size(20, 5, 0, 0, 5)
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

    body = bodyForAdditive(doc, "Nueva figura")
    if body is None:
        return
    torus = doc.addObject("PartDesign::AdditiveTorus", "Torus")
    torus.Radius1 = radius1
    torus.Radius2 = radius2
    body.addObject(torus)
    placeAt(body, torus, x, y, z)

    doc.recompute()
    if _RegisterAdditive(doc, torus):
        print(f"[additive] Created torus ring {radius1} tube {radius2}")


def prism_by_size(
    sides: int, circumradius: float, height: float, x: float, y: float, z: float
) -> None:
    """Create a prism from a dictated side count, radius, height and centre position.

    Args:
        sides: Number of sides of the base polygon. Must be 3 or more.
        circumradius: Centre-to-vertex radius of the base, in millimetres.
        height: Prism height, in millimetres.
        x: X of the prism axis, in millimetres.
        y: Y of the prism axis.
        z: Z of the prism centre (halfway up its height).

    Example::

        prism_by_size(6, 10, 30, 0, 0, 15)
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

    body = bodyForAdditive(doc, "Nueva figura")
    if body is None:
        return
    prism = doc.addObject("PartDesign::AdditivePrism", "Prism")
    prism.Polygon = sides
    prism.Circumradius = circumradius
    prism.Height = height
    body.addObject(prism)
    placeAt(body, prism, x, y, z - height / 2)

    doc.recompute()
    if _RegisterAdditive(doc, prism):
        print(f"[additive] Created prism of {sides} sides radius {circumradius} height {height}")


def ellipsoid_by_size(
    radiusX: float, radiusY: float, radiusZ: float, x: float, y: float, z: float
) -> None:
    """Create an ellipsoid from its three semi-axes and its centre position.

    Args:
        radiusX: Semi-axis along X, in millimetres.
        radiusY: Semi-axis along Y.
        radiusZ: Semi-axis along Z.
        x: X of the centre, in millimetres.
        y: Y of the centre.
        z: Z of the centre.

    Example::

        ellipsoid_by_size(20, 10, 5, 0, 0, 5)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    if radiusX <= 0 or radiusY <= 0 or radiusZ <= 0:
        print("[additive] Error: the three radii must be greater than zero.")
        return

    body = bodyForAdditive(doc, "Nueva figura")
    if body is None:
        return
    ellipsoid = doc.addObject("PartDesign::AdditiveEllipsoid", "Ellipsoid")
    # Radius1 es el semieje local en Z, Radius2 en X y Radius3 en Y
    ellipsoid.Radius1 = radiusZ
    ellipsoid.Radius2 = radiusX
    ellipsoid.Radius3 = radiusY
    body.addObject(ellipsoid)
    placeAt(body, ellipsoid, x, y, z)

    doc.recompute()
    if _RegisterAdditive(doc, ellipsoid):
        print(f"[additive] Created ellipsoid {radiusX} x {radiusY} x {radiusZ}")


def wedge_by_size(
    length: float, depth: float, height: float, topLength: float, topDepth: float,
    x: float, y: float, z: float,
) -> None:
    """Create a wedge (a box whose top face is smaller) from its sizes and centre.

    Args:
        length: Base size along X, in millimetres.
        depth: Base size along Y.
        height: Height along Z.
        topLength: Top face size along X (zero gives a ridge).
        topDepth: Top face size along Y (zero gives a ridge).
        x: X of the centre, in millimetres.
        y: Y of the centre.
        z: Z of the centre (halfway up its height).

    Example::

        wedge_by_size(20, 20, 10, 10, 10, 0, 0, 5)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    if length <= 0 or depth <= 0 or height <= 0:
        print("[additive] Error: base sizes and height must be greater than zero.")
        return
    if topLength < 0 or topDepth < 0 or topLength > length or topDepth > depth:
        print("[additive] Error: the top face cannot be negative or larger than the base.")
        return

    body = bodyForAdditive(doc, "Nueva figura")
    if body is None:
        return
    wedge = doc.addObject("PartDesign::AdditiveWedge", "Wedge")
    # en FreeCAD la base es X-Z y la altura va en Y: se define así y luego se
    # pone de pie (giro de 90 grados sobre X) para que la altura sea Z
    wedge.Xmin, wedge.Xmax = 0, length
    wedge.Zmin, wedge.Zmax = 0, depth
    wedge.Ymin, wedge.Ymax = 0, height
    wedge.X2min, wedge.X2max = (length - topLength) / 2, (length + topLength) / 2
    wedge.Z2min, wedge.Z2max = (depth - topDepth) / 2, (depth + topDepth) / 2
    body.addObject(wedge)
    # el centro local (L/2, H/2, D/2) queda en (L/2, -D/2, H/2) tras el giro
    placeAt(
        body, wedge, x - length / 2, y + depth / 2, z - height / 2,
        App.Rotation(App.Vector(1, 0, 0), 90),
    )

    doc.recompute()
    if _RegisterAdditive(doc, wedge):
        print(f"[additive] Created wedge {length} x {depth} x {height}")


def helix_by_size(pitch: float, height: float) -> None:
    """Sweep a drawing chosen by voice along a helix around its vertical axis.

    The drawing (a closed profile beside the sketch's vertical axis) becomes
    a spring or thread.

    Args:
        pitch: Advance per turn, in millimetres.
        height: Total height of the helix, in millimetres.

    Example::

        helix_by_size(5, 30)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    if pitch <= 0 or height <= 0:
        print("[additive] Error: pitch and height must be greater than zero.")
        return

    chosen = askSketch(doc, "Hélice")
    if chosen is None:
        print("[additive] Helix cancelled.")
        return
    profile = _ResolveProfile(doc, chosen)
    if profile is None or profile.GeometryCount == 0:
        print(f"[additive] Error: '{chosen.Name}' has no usable outline.")
        return

    body = _BodyOf(doc, profile)
    helix = body.newObject("PartDesign::AdditiveHelix", "Helix")
    helix.Profile = profile
    helix.ReferenceAxis = (profile, ["V_Axis"])
    helix.Mode = "pitch-height-angle"
    helix.Pitch = pitch
    helix.Height = height
    doc.recompute()
    if not helix.isValid():
        _discard(doc, helix)
        print("[additive] Error: could not make the helix (the profile must be closed and not cross the vertical axis).")
        return
    profile.Visibility = False
    _RegisterObject(helix)
    print(f"[additive] Created helix pitch {pitch} height {height}")


def loft_choose_sketches() -> None:
    """Join two drawings chosen by voice with a smooth solid (loft).

    Example::

        loft_choose_sketches()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    chosen = askTwoProfiles(doc, "Loft", "Elegí el primer dibujo", "Elegí el segundo dibujo")
    if chosen is None:
        print("[additive] Loft cancelled.")
        return
    first, second = (_ResolveProfile(doc, item) for item in chosen)
    if first is None or second is None:
        print("[additive] Error: one of the drawings has no usable outline.")
        return

    body = _BodyOf(doc, first)
    if second.getParentGeoFeatureGroup() is None:
        body.addObject(second)
    elif second.getParentGeoFeatureGroup() is not body:
        print("[additive] Error: both drawings must belong to the same body.")
        return
    loft = body.newObject("PartDesign::AdditiveLoft", "Loft")
    loft.Profile = first
    loft.Sections = [second]
    doc.recompute()
    if not loft.isValid():
        _discard(doc, loft)
        print("[additive] Error: could not loft between those drawings (they must be closed profiles).")
        return
    first.Visibility = False
    second.Visibility = False
    _RegisterObject(loft)
    print(f"[additive] Created loft between '{first.Name}' and '{second.Name}'")


def pipe_choose_sketches() -> None:
    """Sweep a profile chosen by voice along a path chosen by voice (pipe).

    Example::

        pipe_choose_sketches()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[additive] Error: no active document.")
        return
    chosen = askTwoProfiles(doc, "Tubo", "Elegí el perfil que se recorre", "Elegí la trayectoria")
    if chosen is None:
        print("[additive] Pipe cancelled.")
        return
    profile, path = (_ResolveProfile(doc, item) for item in chosen)
    if profile is None or path is None:
        print("[additive] Error: one of the drawings has no usable outline.")
        return

    body = _BodyOf(doc, profile)
    if path.getParentGeoFeatureGroup() is None:
        body.addObject(path)
    elif path.getParentGeoFeatureGroup() is not body:
        print("[additive] Error: profile and path must belong to the same body.")
        return
    pipe = body.newObject("PartDesign::AdditivePipe", "Pipe")
    pipe.Profile = profile
    pipe.Spine = (path, sketchEdges(path))
    doc.recompute()
    if not pipe.isValid():
        _discard(doc, pipe)
        print("[additive] Error: could not make the pipe (the path must be connected and the profile closed).")
        return
    profile.Visibility = False
    path.Visibility = False
    _RegisterObject(pipe)
    print(f"[additive] Created pipe of '{profile.Name}' along '{path.Name}'")
