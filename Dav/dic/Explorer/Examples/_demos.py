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

"""Pick a guided example by voice and play it frame by frame."""

from . import _arandela, _dado, _draft, _partdesign, _sketcher, _techdraw

# (clave, módulo). Cada módulo aporta TITLE (por idioma) y steps().
_EXAMPLES = (
    ("sketcher", _sketcher),
    ("draft", _draft),
    ("techdraw", _techdraw),
    ("partdesign", _partdesign),
    ("dado", _dado),
    ("arandela", _arandela),
)

_CHOOSE_TITLE = {
    "es": "DAV - Ejemplos",
    "en": "DAV - Examples",
    "pt": "DAV - Exemplos",
}
_CHOOSE_MESSAGE = {
    "es": "Elegí un ejemplo para aprender paso a paso",
    "en": "Pick an example to learn step by step",
    "pt": "Escolha um exemplo para aprender passo a passo",
}

# el reproductor es no modal: se guarda la referencia para que Qt no lo recolecte
_player = None


def _importPrompts() -> None:
    """Make ``InputPrompts`` importable, wherever the dictionary was loaded from."""
    try:
        import InputPrompts  # noqa: F401
    except ImportError:
        from Workbench.Sketcher.new_sketch.new_sketch import _ensure_input_prompts_on_path

        _ensure_input_prompts_on_path()


def _chooseExample(language: str):
    """Show the example picker and return the chosen module, or None."""
    from InputPrompts.ExampleChoiceInputPrompt import ExampleChoiceInputPrompt
    from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher
    from InputPrompts.PromptVoiceRouter import PromptVoiceRouter

    options = [(key, module.TITLE.get(language, module.TITLE["es"]), ()) for key, module in _EXAMPLES]
    prompt = ExampleChoiceInputPrompt(
        options,
        Title=_CHOOSE_TITLE.get(language, _CHOOSE_TITLE["es"]),
        Message=_CHOOSE_MESSAGE.get(language, _CHOOSE_MESSAGE["es"]),
    )
    # el vocabulario abierto confunde las palabras de navegación: se acota la gramática
    PlaneGrammarSwitcher.ActivateGrammar(prompt.GrammarPhrases(language))
    PromptVoiceRouter.SetActivePrompt(prompt)
    try:
        result = prompt.RequestValue()
    finally:
        PromptVoiceRouter.ClearActivePrompt(prompt)
        PlaneGrammarSwitcher.RestoreCadGrammar()
    if result is None or result.Cancelled or not result.Success:
        return None
    return dict(_EXAMPLES)[result.Value]


def _play(module, language: str) -> None:
    """Open the non-modal player for ``module`` and route the voice to it."""
    global _player
    from InputPrompts.GuidedExampleInputPrompt import GuidedExampleInputPrompt
    from InputPrompts.PromptVoiceRouter import PromptVoiceRouter

    try:
        import FreeCADGui as Gui

        parent = Gui.getMainWindow()
    except Exception:
        parent = None

    player = GuidedExampleInputPrompt(
        module.TITLE.get(language, module.TITLE["es"]), module.steps(), Parent=parent
    )
    player.finished.connect(lambda _code: PromptVoiceRouter.ClearActivePrompt(player))
    PromptVoiceRouter.SetActivePrompt(player)
    _player = player
    player.Show()


def startExample() -> None:
    """Let the user pick one of the six examples and start it.

    The picker moves with ``retroceder`` / ``avanzar`` and confirms with
    ``enviar``. The chosen example then shows one frame at a time: the user
    says what they would say to do the same in DAV (the path through the command
    tree and the values dictated in its dialogs) and, once all of it is heard,
    the action runs in FreeCAD.
    """
    _importPrompts()
    from InputPrompts.InputPromptI18n import ResolveLanguage

    language = ResolveLanguage()
    module = _chooseExample(language)
    if module is not None:
        _play(module, language)
