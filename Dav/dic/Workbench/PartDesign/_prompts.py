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

"""Voice dialogs shared by the PartDesign commands (choose a sketch, dictate a value)."""

from __future__ import annotations

from ..Sketcher.new_sketch.new_sketch import _ensure_input_prompts_on_path


def _requestPrompt(prompt):
    """Show prompt modally routing the voice to it; always releases the router."""
    from InputPrompts.PromptVoiceRouter import PromptVoiceRouter

    PromptVoiceRouter.SetActivePrompt(prompt)
    try:
        return prompt.RequestValue()
    finally:
        PromptVoiceRouter.ClearActivePrompt(prompt)


def isProfile(obj) -> bool:
    """True for a sketch with drawing or a loose flat shape (a DAV figure)."""
    if obj.isDerivedFrom("Sketcher::SketchObject"):
        return obj.GeometryCount > 0
    if obj.TypeId != "Part::Feature":
        return False
    shape = getattr(obj, "Shape", None)
    return shape is not None and not shape.isNull() and bool(shape.Edges) and not shape.Solids


def askSketch(doc, title: str):
    """Let the user browse the existing drawings by voice and pick one.

    Args:
        doc: Active FreeCAD document.
        title: Dialog title (the operation being prepared).

    Returns:
        The chosen sketch or loose shape, or None when cancelled or there are none.
    """
    _ensure_input_prompts_on_path()
    from InputPrompts.ObjectSelectionInputPrompt import ObjectSelectionInputPrompt

    if not any(isProfile(obj) for obj in doc.Objects):
        print("[DAV] Error: no hay ningún dibujo para usar. Dibujá algo primero (un boceto con figuras o una figura suelta).")
        return None

    prompt = ObjectSelectionInputPrompt(
        Title=title,
        Message="Elegí el boceto: 'avanzar' para cambiar, 'okey' para elegir",
        ReturnObject=True,
        ObjectFilter=isProfile,
    )
    result = _requestPrompt(prompt)
    if result is None or result.Cancelled or not result.Success:
        return None
    return result.Value


def askNumber(title: str, message: str):
    """Ask a decimal number by voice.

    Args:
        title: Dialog title.
        message: What the user has to say, e.g. "Decí la altura en mm".

    Returns:
        The float, or None when cancelled.
    """
    _ensure_input_prompts_on_path()
    from InputPrompts.FloatInputPrompt import FloatInputPrompt

    result = _requestPrompt(FloatInputPrompt(Title=title, Message=message))
    if result is None or result.Cancelled or not result.Success:
        return None
    return result.Value
