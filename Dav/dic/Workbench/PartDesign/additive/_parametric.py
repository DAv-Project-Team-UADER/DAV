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


def _RegisterObject(Feature) -> None:
    """Register a created feature in the DAV navigable object tree."""
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
    for edge in shape.Edges:
        try:
            sketch.addGeometry(edge.Curve, False)
        except Exception as error:
            # una arista no convertible no invalida el resto del perfil
            print(f"[additive] Skipped an edge while building the sketch: {error}")
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

    body = doc.addObject("PartDesign::Body", "Body")
    body.addObject(profile)

    pad = doc.addObject("PartDesign::Pad", "Pad")
    pad.Profile = profile
    pad.Length = length
    body.addObject(pad)

    # el perfil plano ya no aporta nada visual una vez que hay solido
    if target is not profile:
        target.Visibility = False

    doc.recompute()
    _RegisterObject(pad)
    print(f"[additive] Padded '{profile.Name}' by {length}")


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

    body = doc.addObject("PartDesign::Body", "Body")
    body.addObject(profile)

    revolution = doc.addObject("PartDesign::Revolution", "Revolution")
    revolution.Profile = profile
    revolution.Angle = angle
    body.addObject(revolution)

    if target is not profile:
        target.Visibility = False

    doc.recompute()
    _RegisterObject(revolution)
    print(f"[additive] Revolved '{profile.Name}' by {angle} degrees")


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
