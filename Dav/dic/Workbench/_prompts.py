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

"""Voice dialogs shared by the Part, PartDesign and Assembly commands.

Reemplazan a los dialogos nativos de FreeCAD (que no se controlan por voz):
elegir un dibujo o una pieza entre los existentes ("avanzar"/"okey"), pedir
un numero y elegir un plano.
"""

from __future__ import annotations

from .Sketcher.new_sketch.new_sketch import _ensure_input_prompts_on_path

# Objetos del origen de un Body/Part: tienen Shape pero no son "dibujos".
_ORIGIN_TYPES = ("App::Origin", "App::Line", "App::Plane", "App::Point")


def _requestPrompt(prompt):
    """Show prompt modally routing the voice to it; always releases the router."""
    from InputPrompts.PromptVoiceRouter import PromptVoiceRouter

    PromptVoiceRouter.SetActivePrompt(prompt)
    try:
        return prompt.RequestValue()
    finally:
        PromptVoiceRouter.ClearActivePrompt(prompt)


def _shapeOf(obj):
    """Return obj.Shape when it is a usable (non-null) shape, else None."""
    if obj.TypeId in _ORIGIN_TYPES:
        return None
    shape = getattr(obj, "Shape", None)
    if shape is None or shape.isNull():
        return None
    return shape


def isProfile(obj) -> bool:
    """True for a sketch with drawing or a loose flat shape (a DAV figure)."""
    if obj.isDerivedFrom("Sketcher::SketchObject"):
        return obj.GeometryCount > 0
    if obj.isDerivedFrom("PartDesign::Feature") or obj.isDerivedFrom("PartDesign::Body"):
        return False
    shape = _shapeOf(obj)
    return shape is not None and bool(shape.Edges) and not shape.Solids


def isSolid(obj) -> bool:
    """True for an object whose shape is a solid (a piece to modify)."""
    shape = _shapeOf(obj)
    return shape is not None and bool(shape.Solids)


def isBody(obj) -> bool:
    """True for a PartDesign body holding a valid solid (something to cut or drill).

    Un cuerpo cuya última operación quedó rota (por ejemplo un agujero que no
    se pudo crear) no sirve de base: no se ofrece.
    """
    if not obj.isDerivedFrom("PartDesign::Body"):
        return False
    tip = getattr(obj, "Tip", None)
    if tip is not None and not tip.isValid():
        return False
    return isSolid(obj)


def isPart(obj) -> bool:
    """True for an assembly component: part, body, link or solid piece."""
    if obj.TypeId in _ORIGIN_TYPES or obj.isDerivedFrom("Assembly::AssemblyObject"):
        return False
    if obj.isDerivedFrom("App::Part") or obj.isDerivedFrom("PartDesign::Body"):
        return True
    if obj.isDerivedFrom("App::Link"):
        return True
    # una caja dentro de una Part/Body ya se ofrece a traves de su contenedor
    return (
        isSolid(obj)
        and not obj.isDerivedFrom("PartDesign::Feature")
        and obj.getParentGeoFeatureGroup() is None
    )


def askObject(doc, title: str, message: str, objectFilter, emptyMessage: str):
    """Let the user browse the objects that pass objectFilter and pick one.

    Args:
        doc: Active FreeCAD document.
        title: Dialog title (the operation being prepared).
        message: What the user has to choose, shown in the dialog.
        objectFilter: Callable returning True for the objects to offer.
        emptyMessage: Printed when nothing passes the filter.

    Returns:
        The chosen object, or None when cancelled or there is nothing to offer.
    """
    _ensure_input_prompts_on_path()
    from InputPrompts.ObjectSelectionInputPrompt import ObjectSelectionInputPrompt

    if not any(objectFilter(obj) for obj in doc.Objects):
        print(emptyMessage)
        return None

    prompt = ObjectSelectionInputPrompt(
        Title=title,
        Message=f"{message}: 'avanzar' para cambiar, 'okey' para elegir",
        ReturnObject=True,
        ObjectFilter=objectFilter,
    )
    result = _requestPrompt(prompt)
    if result is None or result.Cancelled or not result.Success:
        return None
    return result.Value


def askSketch(doc, title: str):
    """Let the user pick a drawing (sketch with geometry or loose figure).

    Returns:
        The chosen sketch or loose shape, or None when cancelled or there are none.
    """
    return askObject(
        doc,
        title,
        "Elegí el dibujo",
        isProfile,
        "[DAV] Error: no hay ningún dibujo para usar. Dibujá algo primero "
        "(un boceto con figuras o una figura suelta).",
    )


def askSolid(doc, title: str, message: str = "Elegí la pieza"):
    """Let the user pick a solid piece; None when cancelled or there are none."""
    return askObject(
        doc, title, message, isSolid,
        "[DAV] Error: no hay ninguna pieza sólida. Creá una primero.",
    )


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


def askPlane():
    """Ask the base plane by voice.

    Returns:
        "XY", "XZ" or "YZ", or None when cancelled.
    """
    from .Sketcher.new_sketch.new_sketch import _ask_plane

    result = _ask_plane()
    if result is None or result.Cancelled or not result.Value:
        return None
    return str(result.Value).upper()


def _askWithGrammar(prompt, phrases):
    """Show prompt with the Vosk grammar narrowed to phrases, then restore it."""
    from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher

    PlaneGrammarSwitcher.ActivateGrammar(phrases)
    try:
        return _requestPrompt(prompt)
    finally:
        PlaneGrammarSwitcher.RestoreCadGrammar()


def askChoice(title: str, message: str, options):
    """Ask the user to pick one option by voice.

    Args:
        title: Dialog title.
        message: What the user has to choose.
        options: ``(key, label, spokenWords)`` triples; saying one of the
            spoken words picks the option, or arriba/abajo plus okey.

    Returns:
        The chosen key, or None when cancelled.

    Example::

        askChoice("Grabar", "Elegí el tipo", [
            ("emboss", "Relieve", ("relieve",)),
            ("engrave", "Perforación", ("perforacion", "hundido")),
        ])
    """
    _ensure_input_prompts_on_path()
    from InputPrompts.ChoiceInputPrompt import ChoiceInputPrompt
    from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher

    prompt = ChoiceInputPrompt(Options=list(options), Title=title, Message=message)
    phrases = prompt.GrammarPhrases(PlaneGrammarSwitcher.CurrentLanguage())
    result = _askWithGrammar(prompt, phrases)
    if result is None or result.Cancelled or not result.Success:
        return None
    return result.Value


def askText(title: str, message: str):
    """Ask a text spelled letter by letter, with "espacio" between words.

    Args:
        title: Dialog title.
        message: What the user has to spell.

    Returns:
        The text in upper case, or None when cancelled.
    """
    _ensure_input_prompts_on_path()
    from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher
    from InputPrompts.SpellingInputPrompt import SpellingInputPrompt

    prompt = SpellingInputPrompt(Title=title, Message=message)
    phrases = SpellingInputPrompt.GrammarPhrases(PlaneGrammarSwitcher.CurrentLanguage())
    result = _askWithGrammar(prompt, phrases)
    if result is None or result.Cancelled or not result.Success:
        return None
    return result.Value
