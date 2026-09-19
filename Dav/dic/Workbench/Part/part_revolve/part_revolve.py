

import FreeCAD as App
from FreeCAD import Vector
from ..._display import finishFeature
from ..._prompts import askNumber, askSketch
from .ayuda import ayuda


def _revolve() -> None:
    """Revolve a drawing chosen by voice around its own Y axis by a dictated angle."""
    doc = App.activeDocument()
    if doc is None:
        print("[part] Error: no active document.")
        return
    profile = askSketch(doc, "Revolución")
    if profile is None:
        print("[part] Revolution cancelled.")
        return
    angle = askNumber("Revolución", "Decí el ángulo de giro en grados (1 a 360)")
    if angle is None:
        print("[part] Revolution cancelled.")
        return
    if angle <= 0 or angle > 360:
        print(f"[part] Error: the angle must be between 0 and 360 (got {angle}).")
        return

    # Eje: el Y local del perfil (dentro de su plano), como hace PartDesign con
    # el eje V del boceto; girar alrededor de la normal daria una figura plana.
    rotation = profile.Placement.Rotation
    revolution = doc.addObject("Part::Revolution", "Revolve")
    revolution.Source = profile
    revolution.Axis = rotation.multVec(Vector(0, 1, 0))
    revolution.Base = profile.Placement.Base
    revolution.Angle = angle
    revolution.Solid = True
    finishFeature(doc, revolution, "revolution", hide=(profile,))


part_revolve = {
    'revolucion': _revolve,
    'revolución': _revolve,
    'revolve': _revolve,
    'help': ayuda,
}
