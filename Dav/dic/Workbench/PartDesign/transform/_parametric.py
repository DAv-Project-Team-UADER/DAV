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

"""Parametric transform commands for Validator (numbers and objects)."""

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


def _SelectedFeature(Doc):
    """Return the feature to repeat: the selection, or the active object."""
    try:
        selection = Gui.Selection.getSelection()
    except Exception:
        selection = []
    if selection:
        return selection[0]
    return getattr(Doc, "ActiveObject", None)


def _OwningBody(Doc, Feature):
    """Return the body that owns Feature, or None when it belongs to none."""
    for obj in Doc.Objects:
        if obj.isDerivedFrom("PartDesign::Body") and Feature in obj.Group:
            return obj
    return None


def _AxisNamed(Doc, Name: str):
    """Return one of the document's base axes by attribute name."""
    return getattr(Doc, Name, None)


def _BuildTransform(TypeId: str, Label: str, Doc, Feature):
    """Create a transform feature repeating Feature.

    Args:
        TypeId: FreeCAD type, e.g. ``PartDesign::LinearPattern``.
        Label: Name used for the created object and log lines.
        Doc: Active FreeCAD document.
        Feature: The feature to repeat.

    Returns:
        The created transform feature.
    """
    transform = Doc.addObject(TypeId, Label)
    transform.Originals = [Feature]

    body = _OwningBody(Doc, Feature)
    if body is not None:
        body.addObject(transform)
    return transform


def linear_pattern(occurrences: int, length: float) -> None:
    """Repeat the selected feature along the X axis a dictated number of times.

    ``occurrences`` is an int, so it is collected with IntegerInputPrompt while
    the length uses FloatInputPrompt.

    ``length`` is the distance covered by the whole pattern, not the gap
    between copies: FreeCAD's default mode is "Extent", so five copies over
    80 mm land 20 mm apart. Use ``linear_pattern_by_spacing`` to dictate the
    gap instead.

    Args:
        occurrences: How many copies, counting the original. Must be 2 or more.
        length: Overall pattern length, in millimetres.

    Example::

        linear_pattern(5, 80)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[transform] Error: no active document.")
        return
    if occurrences < 2:
        print(f"[transform] Error: a pattern needs at least 2 copies (got {occurrences}).")
        return
    if length <= 0:
        print(f"[transform] Error: length must be greater than zero (got {length}).")
        return

    feature = _SelectedFeature(doc)
    if feature is None:
        print("[transform] Error: select the feature to repeat first.")
        return

    pattern = _BuildTransform("PartDesign::LinearPattern", "LinearPattern", doc, feature)
    pattern.Direction = (_AxisNamed(doc, "X_Axis"), [""])
    pattern.Length = length
    pattern.Occurrences = occurrences

    doc.recompute()
    _RegisterObject(pattern)
    print(f"[transform] Repeated '{feature.Name}' {occurrences} times over {length}")


def linear_pattern_by_spacing(occurrences: int, offset: float) -> None:
    """Repeat the selected feature along X with a dictated gap between copies.

    Args:
        occurrences: How many copies, counting the original. Must be 2 or more.
        offset: Distance between consecutive copies, in millimetres.

    Example::

        linear_pattern_by_spacing(5, 20)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[transform] Error: no active document.")
        return
    if occurrences < 2:
        print(f"[transform] Error: a pattern needs at least 2 copies (got {occurrences}).")
        return
    if offset <= 0:
        print(f"[transform] Error: spacing must be greater than zero (got {offset}).")
        return

    feature = _SelectedFeature(doc)
    if feature is None:
        print("[transform] Error: select the feature to repeat first.")
        return

    pattern = _BuildTransform("PartDesign::LinearPattern", "LinearPattern", doc, feature)
    pattern.Direction = (_AxisNamed(doc, "X_Axis"), [""])
    # Mode 1 = "Spacing"; con el default (Extent) FreeCAD deja Offset en solo
    # lectura y se queda con Length, ignorando la separacion dictada.
    pattern.Mode = 1
    pattern.Offset = offset
    pattern.Occurrences = occurrences

    doc.recompute()
    _RegisterObject(pattern)
    print(f"[transform] Repeated '{feature.Name}' {occurrences} times every {offset}")


def polar_pattern(occurrences: int, angle: float) -> None:
    """Repeat the selected feature around the Z axis over a dictated angle.

    Args:
        occurrences: How many copies, counting the original. Must be 2 or more.
        angle: Angle covered by the whole pattern, in degrees. Use 360 for a
            full turn.

    Example::

        polar_pattern(6, 360)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[transform] Error: no active document.")
        return
    if occurrences < 2:
        print(f"[transform] Error: a pattern needs at least 2 copies (got {occurrences}).")
        return
    if angle <= 0 or angle > 360:
        print(f"[transform] Error: angle must be between 0 and 360 (got {angle}).")
        return

    feature = _SelectedFeature(doc)
    if feature is None:
        print("[transform] Error: select the feature to repeat first.")
        return

    pattern = _BuildTransform("PartDesign::PolarPattern", "PolarPattern", doc, feature)
    pattern.Axis = (_AxisNamed(doc, "Z_Axis"), [""])
    pattern.Angle = angle
    pattern.Occurrences = occurrences

    doc.recompute()
    _RegisterObject(pattern)
    print(f"[transform] Repeated '{feature.Name}' {occurrences} times over {angle} degrees")


def scaled_by_factor(occurrences: int, factor: float) -> None:
    """Scale the selected feature by a dictated factor.

    Args:
        occurrences: How many scaled copies, counting the original. Use 2 for a
            single scaled copy.
        factor: Scale factor of the last copy. Greater than 1 grows, between 0
            and 1 shrinks.

    Example::

        scaled_by_factor(2, 2)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[transform] Error: no active document.")
        return
    if occurrences < 2:
        print(f"[transform] Error: scaling needs at least 2 copies (got {occurrences}).")
        return
    if factor <= 0:
        print(f"[transform] Error: factor must be greater than zero (got {factor}).")
        return

    feature = _SelectedFeature(doc)
    if feature is None:
        print("[transform] Error: select the feature to scale first.")
        return

    scaled = _BuildTransform("PartDesign::Scaled", "Scaled", doc, feature)
    scaled.Factor = factor
    scaled.Occurrences = occurrences

    doc.recompute()
    _RegisterObject(scaled)
    print(f"[transform] Scaled '{feature.Name}' by {factor}")
