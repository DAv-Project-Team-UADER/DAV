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

from ..._prompts import askChoice, askNumber, askObject


def _RegisterObject(Feature) -> None:
    """Register a created feature in the DAV navigable object tree."""
    try:
        from createobjects import CreateObjects
    except ImportError:
        from selection.createobjects import CreateObjects
    CreateObjects(ObjectName=Feature.Name, Is3D=True).Execute()


def _isRepeatable(obj) -> bool:
    """True for an operation that can be repeated: a PartDesign feature that is not a transform itself."""
    return (
        obj.isDerivedFrom("PartDesign::Feature")
        and not obj.isDerivedFrom("PartDesign::Transformed")
        and not obj.isDerivedFrom("PartDesign::Body")
    )


def _SelectedFeature(Doc):
    """Return the feature to repeat: the selection, else one chosen by voice from the list.

    Sin selección se abre la lista de operaciones («avanzar» / «buscar por deletreo» /
    «okey»); ya no se toma el objeto activo, que casi nunca era el que se quería.
    """
    try:
        selection = Gui.Selection.getSelection()
    except Exception:
        selection = []
    if selection:
        return selection[0]
    return askObject(
        Doc,
        "Transformación",
        "Elegí la operación a repetir",
        _isRepeatable,
        "[transform] Error: no hay ninguna operación para repetir. Creá una primero "
        "(por ejemplo un cilindro aditivo).",
    )


def _OwningBody(Doc, Feature):
    """Return the body that owns Feature, or None when it belongs to none."""
    for obj in Doc.Objects:
        if obj.isDerivedFrom("PartDesign::Body") and Feature in obj.Group:
            return obj
    return None


def _AxisNamed(Doc, Name: str):
    """Return one of the document's base axes by attribute name."""
    return getattr(Doc, Name, None)


def _OriginFeature(Doc, Feature, Role: str):
    """Return the origin axis or plane called Role (``"X_Axis"``, ``"XY_Plane"``...).

    Se busca en el origen del cuerpo de Feature (es el que acepta PartDesign) y, si no
    tiene, en el del documento.
    """
    body = _OwningBody(Doc, Feature)
    origin = getattr(body, "Origin", None) if body is not None else None
    for candidate in (origin, getattr(Doc, "Origin", None)):
        for item in getattr(candidate, "OriginFeatures", None) or []:
            if getattr(item, "Role", "") == Role:
                return item
    return _AxisNamed(Doc, Role)


def _askAxis(Title: str):
    """Ask by voice the axis (``"X_Axis"``, ``"Y_Axis"`` or ``"Z_Axis"``); None when cancelled."""
    return askChoice(Title, "Elegí el eje (arriba/abajo, okey)", [
        ("X_Axis", "Eje X", ("x", "equis", "eje x")),
        ("Y_Axis", "Eje Y", ("y", "ye", "eje y")),
        ("Z_Axis", "Eje Z", ("z", "zeta", "eje z")),
    ])


def _askPlane(Title: str):
    """Ask by voice the mirror plane (``"XY_Plane"``, ``"XZ_Plane"``, ``"YZ_Plane"``); None when cancelled."""
    return askChoice(Title, "Elegí el plano de simetría (arriba/abajo, okey)", [
        ("XY_Plane", "Plano XY", ("xy", "equis ye")),
        ("XZ_Plane", "Plano XZ", ("xz", "equis zeta")),
        ("YZ_Plane", "Plano YZ", ("yz", "ye zeta")),
    ])


def _askCopies(Title: str):
    """Ask by voice how many copies (2 or more); None when cancelled or not valid."""
    value = askNumber(Title, "Decí la cantidad de copias, contando el original")
    if value is None:
        return None
    copies = int(round(value))
    if copies < 2:
        print(f"[transform] Error: hacen falta al menos 2 copias (dijiste {copies}).")
        return None
    return copies


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


def linear_pattern_voice() -> None:
    """Repeat an operation along an axis, choosing everything by voice.

    Pide la operación (si no hay selección), el eje, la cantidad de copias y el largo
    total del patrón. Reemplaza al diálogo nativo de PartDesign.

    Example::

        linear_pattern_voice()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[transform] Error: no active document.")
        return
    feature = _SelectedFeature(doc)
    if feature is None:
        return
    axis = _askAxis("Patrón lineal")
    copies = _askCopies("Patrón lineal") if axis else None
    length = askNumber("Patrón lineal", "Decí el largo total del patrón en mm") if copies else None
    if length is None:
        print("[transform] Patrón lineal cancelado.")
        return
    if length <= 0:
        print(f"[transform] Error: length must be greater than zero (got {length}).")
        return

    pattern = _BuildTransform("PartDesign::LinearPattern", "LinearPattern", doc, feature)
    pattern.Direction = (_OriginFeature(doc, feature, axis), [""])
    pattern.Length = length
    pattern.Occurrences = copies
    doc.recompute()
    _RegisterObject(pattern)
    print(f"[transform] Repeated '{feature.Name}' {copies} times over {length} along {axis}")


def polar_pattern_voice() -> None:
    """Repeat an operation around an axis, choosing everything by voice.

    Pide la operación (si no hay selección), el eje, la cantidad de copias y el ángulo.

    Example::

        polar_pattern_voice()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[transform] Error: no active document.")
        return
    feature = _SelectedFeature(doc)
    if feature is None:
        return
    axis = _askAxis("Patrón polar")
    copies = _askCopies("Patrón polar") if axis else None
    angle = askNumber("Patrón polar", "Decí el ángulo total en grados (360 es una vuelta)") if copies else None
    if angle is None:
        print("[transform] Patrón polar cancelado.")
        return
    if angle <= 0 or angle > 360:
        print(f"[transform] Error: angle must be between 0 and 360 (got {angle}).")
        return

    pattern = _BuildTransform("PartDesign::PolarPattern", "PolarPattern", doc, feature)
    pattern.Axis = (_OriginFeature(doc, feature, axis), [""])
    pattern.Angle = angle
    pattern.Occurrences = copies
    doc.recompute()
    _RegisterObject(pattern)
    print(f"[transform] Repeated '{feature.Name}' {copies} times over {angle} degrees around {axis}")


def mirrored_voice() -> None:
    """Mirror an operation across a base plane, choosing everything by voice.

    Pide la operación (si no hay selección) y el plano de simetría (XY, XZ o YZ).

    Example::

        mirrored_voice()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[transform] Error: no active document.")
        return
    feature = _SelectedFeature(doc)
    if feature is None:
        return
    plane = _askPlane("Simetría")
    if plane is None:
        print("[transform] Simetría cancelada.")
        return

    mirrored = _BuildTransform("PartDesign::Mirrored", "Mirrored", doc, feature)
    mirrored.MirrorPlane = (_OriginFeature(doc, feature, plane), [""])
    doc.recompute()
    _RegisterObject(mirrored)
    print(f"[transform] Mirrored '{feature.Name}' across {plane}")


def scaled_voice() -> None:
    """Scale an operation, choosing everything by voice.

    Pide la operación (si no hay selección), la cantidad de copias y el factor.

    Example::

        scaled_voice()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[transform] Error: no active document.")
        return
    feature = _SelectedFeature(doc)
    if feature is None:
        return
    copies = _askCopies("Escalado")
    factor = askNumber("Escalado", "Decí el factor de escala (2 duplica, 0 coma 5 reduce a la mitad)") if copies else None
    if factor is None:
        print("[transform] Escalado cancelado.")
        return
    if factor <= 0:
        print(f"[transform] Error: factor must be greater than zero (got {factor}).")
        return

    scaled = _BuildTransform("PartDesign::Scaled", "Scaled", doc, feature)
    scaled.Factor = factor
    scaled.Occurrences = copies
    doc.recompute()
    _RegisterObject(scaled)
    print(f"[transform] Scaled '{feature.Name}' by {factor}")
