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

"""Parametric dress-up commands for Validator (numbers and objects)."""

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


def _SelectedSolid(Doc):
    """Return the solid to dress up: the selection, or the active object."""
    try:
        selection = Gui.Selection.getSelection()
    except Exception:
        selection = []
    if selection:
        return selection[0]
    return getattr(Doc, "ActiveObject", None)


def _OwningBody(Doc, Solid):
    """Return the body that owns Solid, or None when it belongs to none."""
    for obj in Doc.Objects:
        if obj.isDerivedFrom("PartDesign::Body") and Solid in obj.Group:
            return obj
    return None


def _ApplyDressUp(TypeId: str, Label: str, Doc, Solid):
    """Create a dress-up feature covering every edge of Solid.

    Picking individual edges by voice is impractical, so ``UseAllEdges`` is
    switched on and the base is set with an empty subelement list -- the
    combination FreeCAD's own tests use to dress a whole solid.

    Args:
        TypeId: FreeCAD type, e.g. ``PartDesign::Fillet``.
        Label: Name used for the created object and log lines.
        Doc: Active FreeCAD document.
        Solid: Object whose edges are dressed.

    Returns:
        The created feature, or None when it could not be built.
    """
    feature = Doc.addObject(TypeId, Label)
    feature.Base = (Solid, [""])
    feature.UseAllEdges = True

    body = _OwningBody(Doc, Solid)
    if body is not None:
        body.addObject(feature)
    return feature


def fillet_by_radius(radius: float) -> None:
    """Round every edge of the selected solid by a dictated radius.

    Args:
        radius: Fillet radius, in millimetres. Must be greater than zero and
            smaller than half the solid's smallest side, or the recompute
            fails.

    Example::

        fillet_by_radius(3)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[modify] Error: no active document.")
        return
    if radius <= 0:
        print(f"[modify] Error: radius must be greater than zero (got {radius}).")
        return

    solid = _SelectedSolid(doc)
    if solid is None:
        print("[modify] Error: select the solid to round first.")
        return

    fillet = _ApplyDressUp("PartDesign::Fillet", "Fillet", doc, solid)
    fillet.Radius = radius

    doc.recompute()
    _RegisterObject(fillet)
    print(f"[modify] Rounded '{solid.Name}' with radius {radius}")


def chamfer_by_size(size: float) -> None:
    """Chamfer every edge of the selected solid by a dictated size.

    The chamfer angle stays at FreeCAD's 45 degree default; use
    ``chamfer_by_size_and_angle`` to dictate it.

    Args:
        size: Chamfer size, in millimetres. Must be greater than zero.

    Example::

        chamfer_by_size(2)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[modify] Error: no active document.")
        return
    if size <= 0:
        print(f"[modify] Error: size must be greater than zero (got {size}).")
        return

    solid = _SelectedSolid(doc)
    if solid is None:
        print("[modify] Error: select the solid to chamfer first.")
        return

    chamfer = _ApplyDressUp("PartDesign::Chamfer", "Chamfer", doc, solid)
    chamfer.Size = size

    doc.recompute()
    _RegisterObject(chamfer)
    print(f"[modify] Chamfered '{solid.Name}' with size {size}")


def chamfer_by_size_and_angle(size: float, angle: float) -> None:
    """Chamfer every edge of the selected solid by a dictated size and angle.

    Args:
        size: Chamfer size, in millimetres.
        angle: Chamfer angle, in degrees. Must be between 0 and 180.

    Example::

        chamfer_by_size_and_angle(2, 30)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[modify] Error: no active document.")
        return
    if size <= 0:
        print(f"[modify] Error: size must be greater than zero (got {size}).")
        return
    if angle <= 0 or angle >= 180:
        print(f"[modify] Error: angle must be between 0 and 180 (got {angle}).")
        return

    solid = _SelectedSolid(doc)
    if solid is None:
        print("[modify] Error: select the solid to chamfer first.")
        return

    chamfer = _ApplyDressUp("PartDesign::Chamfer", "Chamfer", doc, solid)
    chamfer.Size = size
    # ChamferType 1 = "size and angle"; con el default (0) FreeCAD ignora Angle
    chamfer.ChamferType = 1
    chamfer.Angle = angle

    doc.recompute()
    _RegisterObject(chamfer)
    print(f"[modify] Chamfered '{solid.Name}' with size {size} at {angle} degrees")


def thickness_by_value(value: float) -> None:
    """Hollow the selected solid leaving a dictated wall thickness.

    Args:
        value: Wall thickness, in millimetres. Must be greater than zero.

    Example::

        thickness_by_value(2)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[modify] Error: no active document.")
        return
    if value <= 0:
        print(f"[modify] Error: thickness must be greater than zero (got {value}).")
        return

    solid = _SelectedSolid(doc)
    if solid is None:
        print("[modify] Error: select the solid to hollow first.")
        return

    thickness = _ApplyDressUp("PartDesign::Thickness", "Thickness", doc, solid)
    thickness.Value = value

    doc.recompute()
    _RegisterObject(thickness)
    print(f"[modify] Hollowed '{solid.Name}' leaving {value} of wall")
