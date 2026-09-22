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

from .._display import showResult
from .._prompts import askObject, isPart
from ._connectors import askConnector

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
    "RackPinion": 9,
    "Screw": 10,
    "Gears": 11,
    "Belt": 12,
}


def _RegisterObject(Feature) -> None:
    """Show a created feature and register it in the DAV navigable object tree."""
    showResult(Feature)
    # las juntas no tienen geometria: no hay caras ni aristas que extraer
    if not hasattr(Feature, "Shape"):
        return
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


def _ChooseParts(Doc, Count: int):
    """Let the user pick Count assembly parts by voice ("avanzar"/"okey").

    Reemplaza a la seleccion con el mouse: cada pieza se elige en un dialogo
    propio, sin repetir una ya elegida.

    Args:
        Doc: Active FreeCAD document.
        Count: How many parts to choose (1 or 2).

    Returns:
        The chosen parts, or None when the user cancelled or there are none.
    """
    ordinals = ("primera", "segunda")
    parts = []
    for index in range(Count):
        message = "Elegí la pieza" if Count == 1 else f"Elegí la {ordinals[index]} pieza"
        chosen = askObject(
            Doc,
            "Ensamblaje",
            message,
            lambda obj: isPart(obj) and obj not in parts,
            "[DAV] Error: no hay piezas para ensamblar. Creá o insertá piezas primero.",
        )
        if chosen is None:
            return None
        parts.append(chosen)
    return parts


def _ChooseConnectors(Parts):
    """Let the user pick by voice the face where each of Parts is joined.

    Args:
        Parts: The parts to connect.

    Returns:
        One face name per part (``"Face3"``), or None when the user cancelled.
    """
    elements = []
    for part in Parts:
        element = askConnector(part, "Ensamblaje")
        if element is None:
            return None
        elements.append(element)
    return elements


def _CreateJoint(JointTypeName: str, Doc, Parts, Elements=None):
    """Build a joint feature of the given type between Parts.

    Args:
        JointTypeName: Key of ``_JOINT_TYPE_INDEX``.
        Doc: Active FreeCAD document.
        Parts: The two objects to connect.
        Elements: Face of each part where it is joined (``"Face3"``). When None the
            user is asked by voice, one dialog per part.

    Returns:
        The created joint feature, or None when it could not be built or the user cancelled.
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

    # se pregunta antes de crear la junta: si se cancela no queda una junta a medias
    if Elements is None:
        Elements = _ChooseConnectors(Parts)
        if Elements is None:
            print("[assembly] Cancelled: the place where each part joins is needed.")
            return None

    group = _JointGroup(assembly)
    feature = group.newObject("App::FeaturePython", f"{JointTypeName}Joint")
    JointObject.Joint(feature, _JOINT_TYPE_INDEX[JointTypeName])

    # setJointConnectors espera [objeto, [elemento, vertice]] por cada lado y calcula el marco de
    # la junta con eso. Con una cara se repite el nombre: el marco queda en el centro de la cara
    # (en el eje, si es un cilindro) y orientado como ella. Con un solo nombre la referencia
    # se descarta y el marco queda en el origen de la pieza.
    references = [[part, [element, element]] for part, element in zip(Parts, Elements)]
    try:
        feature.Proxy.setJointConnectors(feature, references)
    except Exception as error:
        print(f"[assembly] Error: could not connect the parts: {error}")
        return None

    return feature


# separación entre las piezas que se van insertando, en mm
_LINK_GAP = 10


def _InsertLink(Doc, Assembly, Part):
    """Add a link to Part inside Assembly, beside the parts already inserted.

    Args:
        Doc: Active FreeCAD document.
        Assembly: The assembly that receives the link.
        Part: The body or part to insert.

    Returns:
        The new ``App::Link``.
    """
    link = Assembly.newObject("App::Link", Part.Label)
    link.LinkedObject = Part
    link.Label = Part.Label
    Doc.recompute()
    placed = [obj for obj in Assembly.Group if obj.isDerivedFrom("App::Link") and obj is not link]
    if placed:
        # a la derecha de las ya insertadas, para que no se pisen
        shift = max(obj.Shape.BoundBox.XMax for obj in placed) + _LINK_GAP - link.Shape.BoundBox.XMin
        link.Placement = App.Placement(App.Vector(shift, 0, 0), App.Rotation())
        Doc.recompute()
    return link


def insert_link() -> None:
    """Insert a part into the assembly, choosing it from a voice list.

    Replaces FreeCAD's own "Insert component" dialog, which is used with the mouse. The
    part is placed beside the ones already inserted so they do not overlap; the joints
    then bring them together.

    Example::

        insert_link()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[assembly] Error: no active document.")
        return

    assembly = _ActiveAssembly(doc)
    if assembly is None:
        print("[assembly] Error: no assembly found. Say 'crear ensamblaje' first.")
        return

    part = askObject(
        doc,
        "Ensamblaje",
        "Elegí la pieza a insertar",
        lambda obj: isPart(obj) and not obj.isDerivedFrom("App::Link"),
        "[DAV] Error: no hay piezas para insertar. Creá una primero.",
    )
    if part is None:
        print("[assembly] Cancelled: a part is needed to insert.")
        return

    link = _InsertLink(doc, assembly, part)
    _RegisterObject(link)
    print(f"[assembly] Inserted '{part.Label}'")


def fixed_joint() -> None:
    """Lock the two chosen parts together with a fixed joint.

    Pick the two parts by voice ("avanzar"/"okey"); no FreeCAD dialog is opened.

    Example::

        fixed_joint()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[assembly] Error: no active document.")
        return

    parts = _ChooseParts(doc, 2)
    if parts is None:
        print("[assembly] Cancelled: two parts are needed to make the joint.")
        return

    joint = _CreateJoint("Fixed", doc, parts)
    if joint is None:
        return

    doc.recompute()
    _RegisterObject(joint)
    print(f"[assembly] Fixed '{parts[0].Name}' to '{parts[1].Name}'")


def revolute_joint() -> None:
    """Hinge the two chosen parts with a revolute joint.

    Example::

        revolute_joint()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[assembly] Error: no active document.")
        return

    parts = _ChooseParts(doc, 2)
    if parts is None:
        print("[assembly] Cancelled: two parts are needed to make the joint.")
        return

    joint = _CreateJoint("Revolute", doc, parts)
    if joint is None:
        return

    doc.recompute()
    _RegisterObject(joint)
    print(f"[assembly] Hinged '{parts[0].Name}' to '{parts[1].Name}'")


def slider_joint() -> None:
    """Let the two chosen parts slide along one axis.

    Example::

        slider_joint()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[assembly] Error: no active document.")
        return

    parts = _ChooseParts(doc, 2)
    if parts is None:
        print("[assembly] Cancelled: two parts are needed to make the joint.")
        return

    joint = _CreateJoint("Slider", doc, parts)
    if joint is None:
        return

    doc.recompute()
    _RegisterObject(joint)
    print(f"[assembly] Slider between '{parts[0].Name}' and '{parts[1].Name}'")


def distance_joint(distance: float) -> None:
    """Hold the two chosen parts a dictated distance apart.

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

    parts = _ChooseParts(doc, 2)
    if parts is None:
        print("[assembly] Cancelled: two parts are needed to make the joint.")
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
    """Hold the two chosen parts at a dictated angle.

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

    parts = _ChooseParts(doc, 2)
    if parts is None:
        print("[assembly] Cancelled: two parts are needed to make the joint.")
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
    """Ground the chosen part so the solver keeps it fixed in place.

    An assembly needs at least one grounded part; without it the solver has
    nothing to anchor the others to.

    Example::

        ground_part()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[assembly] Error: no active document.")
        return

    parts = _ChooseParts(doc, 1)
    if parts is None:
        print("[assembly] Cancelled: a part is needed to ground.")
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


def _SimpleJoint(JointTypeName: str, Verb: str) -> None:
    """Create a joint that needs no dictated value between two chosen parts.

    Args:
        JointTypeName: Key of ``_JOINT_TYPE_INDEX``.
        Verb: Past-tense verb used in the log line.
    """
    doc = App.activeDocument()
    if doc is None:
        print("[assembly] Error: no active document.")
        return

    parts = _ChooseParts(doc, 2)
    if parts is None:
        print("[assembly] Cancelled: two parts are needed to make the joint.")
        return

    joint = _CreateJoint(JointTypeName, doc, parts)
    if joint is None:
        return

    doc.recompute()
    _RegisterObject(joint)
    print(f"[assembly] {Verb} '{parts[0].Name}' and '{parts[1].Name}'")


def ball_joint() -> None:
    """Join the two chosen parts with a ball joint, free to rotate any way.

    Example::

        ball_joint()
    """
    _SimpleJoint("Ball", "Ball-jointed")


def cylindrical_joint() -> None:
    """Join the two chosen parts so one both slides and turns on an axis.

    Example::

        cylindrical_joint()
    """
    _SimpleJoint("Cylindrical", "Cylindrically joined")


def parallel_joint() -> None:
    """Keep the two chosen parts parallel to each other.

    Example::

        parallel_joint()
    """
    _SimpleJoint("Parallel", "Kept parallel")


def perpendicular_joint() -> None:
    """Keep the two chosen parts perpendicular to each other.

    Example::

        perpendicular_joint()
    """
    _SimpleJoint("Perpendicular", "Kept perpendicular")


def _RatioJoint(JointTypeName: str, Verb: str, Radius1: float, Radius2: float | None) -> None:
    """Create a joint whose motion ratio comes from one or two dictated radii.

    FreeCAD stores these in the generic ``Distance`` and ``Distance2``
    properties rather than in fields of their own: ``Distance`` holds the pitch
    radius (rack and pinion, screw, belt) or the first gear radius, and
    ``Distance2`` the second gear radius.

    Args:
        JointTypeName: Key of ``_JOINT_TYPE_INDEX``.
        Verb: Past-tense verb used in the log line.
        Radius1: First radius or pitch, in millimetres.
        Radius2: Second radius, or None when the joint uses only one.
    """
    doc = App.activeDocument()
    if doc is None:
        print("[assembly] Error: no active document.")
        return
    if Radius1 <= 0 or (Radius2 is not None and Radius2 <= 0):
        print("[assembly] Error: radii must be greater than zero.")
        return

    parts = _ChooseParts(doc, 2)
    if parts is None:
        print("[assembly] Cancelled: two parts are needed to make the joint.")
        return

    joint = _CreateJoint(JointTypeName, doc, parts)
    if joint is None:
        return

    joint.Distance = Radius1
    if Radius2 is not None:
        joint.Distance2 = Radius2

    doc.recompute()
    _RegisterObject(joint)
    sizes = f"{Radius1}" if Radius2 is None else f"{Radius1} and {Radius2}"
    print(f"[assembly] {Verb} '{parts[0].Name}' and '{parts[1].Name}' with {sizes}")


def gears_joint(radius1: float, radius2: float) -> None:
    """Mesh the two chosen parts as gears with dictated radii.

    The ratio between the radii sets how fast one gear turns relative to the
    other.

    Args:
        radius1: Radius of the first gear, in millimetres.
        radius2: Radius of the second gear, in millimetres.

    Example::

        gears_joint(20, 10)
    """
    _RatioJoint("Gears", "Meshed", radius1, radius2)


def belt_joint(radius1: float, radius2: float) -> None:
    """Link the two chosen parts with a belt between dictated pulley radii.

    Args:
        radius1: Radius of the first pulley, in millimetres.
        radius2: Radius of the second pulley, in millimetres.

    Example::

        belt_joint(30, 15)
    """
    _RatioJoint("Belt", "Belted", radius1, radius2)


def screw_joint(pitch: float) -> None:
    """Join the two chosen parts as a screw with a dictated pitch radius.

    Args:
        pitch: Pitch radius, in millimetres.

    Example::

        screw_joint(5)
    """
    _RatioJoint("Screw", "Screwed", pitch, None)


def rack_pinion_joint(pitch_radius: float) -> None:
    """Join the two chosen parts as rack and pinion with a dictated radius.

    Args:
        pitch_radius: Pitch radius of the pinion, in millimetres.

    Example::

        rack_pinion_joint(10)
    """
    _RatioJoint("RackPinion", "Rack-and-pinioned", pitch_radius, None)
