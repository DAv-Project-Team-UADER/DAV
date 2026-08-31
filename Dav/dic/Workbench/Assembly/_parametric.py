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

"""Parametric assembly commands for Validator (numbers and objects)."""

from __future__ import annotations

import FreeCAD as App
import FreeCADGui as Gui

# Indice de cada tipo en Assembly.JointObject.JointTypes. Se pasa como segundo
# argumento a JointObject.Joint(feature, index), que es la forma en que los
# propios tests de FreeCAD crean juntas sin abrir el dialogo.
_JOINT_TYPE_INDEX = {
    "Fixed": 0,
    "Revolute": 1,
    "Cylindrical": 2,
    "Slider": 3,
    "Ball": 4,
    "Distance": 5,
    "Parallel": 6,
    "Perpendicular": 7,
    "Angle": 8,
}


def _RegisterObject(Feature) -> None:
    """Register a created feature in the DAV navigable object tree."""
    try:
        from createobjects import CreateObjects
    except ImportError:
        from selection.createobjects import CreateObjects
    CreateObjects(ObjectName=Feature.Name, Is3D=True).Execute()


def _ActiveAssembly(Doc):
    """Return the assembly to work on.

    ``UtilsAssembly.activeAssembly()`` only answers while the assembly is in
    edit mode, which is not a state the voice flow can rely on. This falls back
    to the single assembly in the document, so ``ensamble fijo`` works right
    after ``crear ensamblaje`` without extra clicks.

    Args:
        Doc: Active FreeCAD document.

    Returns:
        The assembly object, or None when there is none or the choice is
        ambiguous.
    """
    try:
        import UtilsAssembly

        active = UtilsAssembly.activeAssembly()
        if active is not None:
            return active
    except Exception:
        # sin el modulo o fuera de modo edicion seguimos por el documento
        pass

    assemblies = [
        obj for obj in Doc.Objects if obj.isDerivedFrom("Assembly::AssemblyObject")
    ]
    if not assemblies:
        return None
    if len(assemblies) > 1:
        print(
            f"[assembly] Error: {len(assemblies)} assemblies in the document; "
            "open the one to use so the command is unambiguous."
        )
        return None
    return assemblies[0]


def _JointGroup(Assembly):
    """Return the assembly's joint group, creating it when missing."""
    for obj in Assembly.Group:
        if obj.isDerivedFrom("Assembly::JointGroup"):
            return obj
    return Assembly.newObject("Assembly::JointGroup", "Joints")


def _SelectedParts(Count: int):
    """Return the first Count selected objects, or None when there are fewer."""
    try:
        selection = Gui.Selection.getSelection()
    except Exception:
        selection = []
    if len(selection) < Count:
        return None
    return selection[:Count]


def _CreateJoint(JointTypeName: str, Doc, Parts):
    """Build a joint feature of the given type between Parts.

    Args:
        JointTypeName: Key of ``_JOINT_TYPE_INDEX``.
        Doc: Active FreeCAD document.
        Parts: The two objects to connect.

    Returns:
        The created joint feature, or None when it could not be built.
    """
    assembly = _ActiveAssembly(Doc)
    if assembly is None:
        print("[assembly] Error: no assembly found. Say 'crear ensamblaje' first.")
        return None

    try:
        import JointObject
    except ImportError:
        print("[assembly] Error: the Assembly workbench is not available.")
        return None

    group = _JointGroup(assembly)
    feature = group.newObject("App::FeaturePython", f"{JointTypeName}Joint")
    JointObject.Joint(feature, _JOINT_TYPE_INDEX[JointTypeName])

    # setJointConnectors espera [objeto, [subelementos]] por cada lado; se usa
    # el primer vertice de cada pieza como punto de anclaje por defecto.
    references = [[part, ["Vertex1"]] for part in Parts]
    try:
        feature.Proxy.setJointConnectors(feature, references)
    except Exception as error:
        print(f"[assembly] Error: could not connect the parts: {error}")
        return None

    return feature


def fixed_joint() -> None:
    """Lock the two selected parts together with a fixed joint.

    Select two parts first, then say the command. No dialog is opened.

    Example::

        fixed_joint()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[assembly] Error: no active document.")
        return

    parts = _SelectedParts(2)
    if parts is None:
        print("[assembly] Error: select two parts to join first.")
        return

    joint = _CreateJoint("Fixed", doc, parts)
    if joint is None:
        return

    doc.recompute()
    _RegisterObject(joint)
    print(f"[assembly] Fixed '{parts[0].Name}' to '{parts[1].Name}'")


def revolute_joint() -> None:
    """Hinge the two selected parts with a revolute joint.

    Example::

        revolute_joint()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[assembly] Error: no active document.")
        return

    parts = _SelectedParts(2)
    if parts is None:
        print("[assembly] Error: select two parts to join first.")
        return

    joint = _CreateJoint("Revolute", doc, parts)
    if joint is None:
        return

    doc.recompute()
    _RegisterObject(joint)
    print(f"[assembly] Hinged '{parts[0].Name}' to '{parts[1].Name}'")


def slider_joint() -> None:
    """Let the two selected parts slide along one axis.

    Example::

        slider_joint()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[assembly] Error: no active document.")
        return

    parts = _SelectedParts(2)
    if parts is None:
        print("[assembly] Error: select two parts to join first.")
        return

    joint = _CreateJoint("Slider", doc, parts)
    if joint is None:
        return

    doc.recompute()
    _RegisterObject(joint)
    print(f"[assembly] Slider between '{parts[0].Name}' and '{parts[1].Name}'")


def distance_joint(distance: float) -> None:
    """Hold the two selected parts a dictated distance apart.

    This is the assembly counterpart of the parametric geometry commands: the
    gap comes from the voice prompt, so no dialog is opened.

    Args:
        distance: Gap between the parts, in millimetres.

    Example::

        distance_joint(25)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[assembly] Error: no active document.")
        return

    parts = _SelectedParts(2)
    if parts is None:
        print("[assembly] Error: select two parts to join first.")
        return

    joint = _CreateJoint("Distance", doc, parts)
    if joint is None:
        return

    joint.Distance = distance
    doc.recompute()
    _RegisterObject(joint)
    print(
        f"[assembly] Held '{parts[0].Name}' and '{parts[1].Name}' {distance} apart"
    )


def angle_joint(angle: float) -> None:
    """Hold the two selected parts at a dictated angle.

    Args:
        angle: Angle between the parts, in degrees. Must be between 0 and 360.

    Example::

        angle_joint(90)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[assembly] Error: no active document.")
        return
    if angle < 0 or angle > 360:
        print(f"[assembly] Error: angle must be between 0 and 360 (got {angle}).")
        return

    parts = _SelectedParts(2)
    if parts is None:
        print("[assembly] Error: select two parts to join first.")
        return

    joint = _CreateJoint("Angle", doc, parts)
    if joint is None:
        return

    joint.Angle = angle
    doc.recompute()
    _RegisterObject(joint)
    print(
        f"[assembly] Held '{parts[0].Name}' and '{parts[1].Name}' at {angle} degrees"
    )


def ground_part() -> None:
    """Ground the selected part so the solver keeps it fixed in place.

    An assembly needs at least one grounded part; without it the solver has
    nothing to anchor the others to.

    Example::

        ground_part()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[assembly] Error: no active document.")
        return

    parts = _SelectedParts(1)
    if parts is None:
        print("[assembly] Error: select the part to ground first.")
        return

    assembly = _ActiveAssembly(doc)
    if assembly is None:
        print("[assembly] Error: no assembly found. Say 'crear ensamblaje' first.")
        return

    try:
        import JointObject
    except ImportError:
        print("[assembly] Error: the Assembly workbench is not available.")
        return

    group = _JointGroup(assembly)
    feature = group.newObject("App::FeaturePython", "GroundedJoint")
    JointObject.GroundedJoint(feature, parts[0])

    doc.recompute()
    _RegisterObject(feature)
    print(f"[assembly] Grounded '{parts[0].Name}'")
