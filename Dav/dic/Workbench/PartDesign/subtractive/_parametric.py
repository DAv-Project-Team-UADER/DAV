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


def _RegisterObject(Feature) -> None:
    """Register a created feature in the DAV navigable object tree."""
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
    for edge in shape.Edges:
        try:
            sketch.addGeometry(edge.Curve, False)
        except Exception as error:
            # una arista no convertible no invalida el resto del perfil
            print(f"[subtractive] Skipped an edge while building the sketch: {error}")
    return sketch


def _ResolveProfile(Doc, Target):
    """Return a usable profile for Target, converting a Part shape if needed."""
    if Target is None:
        return None
    if Target.isDerivedFrom("Sketcher::SketchObject"):
        return Target
    return _SketchFromShape(Doc, Target, f"{Target.Name}Profile")


def _OwningBody(Doc, Profile):
    """Return the body that owns Profile, or a new one when there is none."""
    for obj in Doc.Objects:
        if obj.isDerivedFrom("PartDesign::Body") and Profile in obj.Group:
            return obj
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
