# Adding a voice dialog (prompt) and restricting its grammar

A **prompt** is a window that asks a question and is answered by speaking: a
number, an option, a file, yes or no. It exists because many native FreeCAD
dialogs cannot be driven by voice, and because some commands need values
("círculo" asks for a radius).

Before writing one, check whether one already fits: most of the time it is enough
to **use an existing one** (sections 1 and 2). Writing a new class (section 3) is
the last resort.

---

## 1. The simplest way: let the parameters ask for themselves

If the dictionary function **declares typed parameters**, DAV asks for them by voice
without you writing any dialog. This is done by
[`ParameterCollector`](../diagrams/ParameterCollector.md); the full walkthrough is in
[`CommandWithParametersFlow`](../diagrams/CommandWithParametersFlow.md).

```python
def makeCircle(radius: float) -> None:
    ...

draft = {'circle': makeCircle}
```

| Annotation | Prompt that opens |
| --- | --- |
| `int` | integer number |
| `float` | decimal number |
| `str` | free text |
| any other / none | selection of an object in the document |

A parameter **with a default value is not asked for**. If the function has no required
parameters, nothing opens.

---

## 2. Custom conversations: the helpers in `Workbench/_prompts.py`

When the command needs more than a single value (choosing between two modes, an
object that meets a condition, a confirmation), use the helpers. They already register
the prompt in the router, restrict the grammar and restore it when finished.

| Helper | Asks | Returns |
| --- | --- | --- |
| `askNumber(title, message)` | a decimal number | `float` or `None` |
| `askChoice(title, message, options)` | one option among a few | the chosen key or `None` |
| `askYesNo(title, message)` | yes / no | `True`, `False` or `None` |
| `askText(title, message)` | a spelled-out text | `str` or `None` |
| `askPlane()` | the base plane | `"XY"`, `"XZ"`, `"YZ"` or `None` |
| `askObject(doc, title, message, filter, emptyMessage)` | an object that meets `filter` | the object or `None` |
| `askSketch` / `askShape` / `askSolid` | shortcuts for `askObject` | the object or `None` |

**All of them return `None` if the user cancels**: always check it and exit without doing anything.

```python
from Workbench._prompts import askChoice, askNumber

mode = askChoice("Grabar", "Elegí el tipo", [
    ("emboss",  "Relieve",     ("relieve", "saliente")),
    ("engrave", "Perforación", ("perforación", "hundido")),
])
if mode is None:
    return
height = askNumber("Grabar", "Decí la altura en mm")
if height is None:
    return
```

Each `askChoice` option is `(key, displayed text, words that select it)`. The texts
and words in the example are the Spanish ones shown to and said by the user
("Grabar" = Engrave, "Relieve" = Emboss, "Perforación" = Cut-in).

---

## 3. A new prompt class

### What to inherit from

| You need | Inherit from |
| --- | --- |
| A free value (text, number, object) | [`BaseInputPrompt`](../diagrams/BaseInputPrompt.md) |
| A dictated number | [`NumericInputPrompt`](../diagrams/NumericInputPrompt.md): you only implement `_ParseAccumulatedText` |
| Choosing among a few named options | [`ChoiceInputPrompt`](../diagrams/ChoiceInputPrompt.md) |
| Choosing with a different navigation vocabulary | subclass of `ChoiceInputPrompt` (see [`ExampleChoiceInputPrompt`](../diagrams/ExampleChoiceInputPrompt.md)) |

### Minimal skeleton

```python
from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser

_COLORS = {"rojo": "red", "azul": "blue"}          # no accent marks


class ColorInputPrompt(BaseInputPrompt):
    """Prompt that picks a color by saying its name."""

    def GrammarPhrases(self, Language: str = "es") -> list[str]:
        """Return the words Vosk should listen for."""
        from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher

        return list(_COLORS) + PlaneGrammarSwitcher.PlanePhrases(Language)

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Accept a color name; cancelar aborts."""
        self.SetHeardText(Text)
        tokens = SpokenNumberParser.Tokenize(Text)   # normalizes accents and case
        if self._HasCancellation(tokens):
            return self.Cancel()
        for word, value in _COLORS.items():
            if word in tokens:
                return self.AcceptValue(value)
        self.SetStatus("No te entendí")   # "I didn't understand you"
        return self.GetResult()
```

### Rules

- **`ProcessFinalText` receives the phrase already recognized.** Compare it tokenized with
  `SpokenNumberParser.Tokenize`, which strips accent marks and lowercases; write your
  words **without accent marks**.
- **Always close through an explicit path:** `AcceptValue(value)`, `Cancel()` or `Fail(msg)`
  (leaves the window open to retry). Do not call `accept()` or `close()` directly.
- **Always accept cancel** with `_HasCancellation`, and confirm with `_HasConfirmation`
  if the value is dictated over several phrases.
- **Three languages.** If you have words of your own, define them per language (`es`, `en`, `pt`) as
  `YesNoInputPrompt` does, and accept those of all three at once when comparing.
- **Do not import `FreeCAD` at module level** in `InputPrompts/`: do it inside the
  functions, so the prompt can be tested without FreeCAD.
- **Docstrings in English, mandatory header**, and a diagram in `docs/es/diagrams/`.

---

## 4. Restricting the Vosk grammar

With an open vocabulary, Vosk confuses short navigation words
("abajo" for "trabajo"). While the prompt is open, Vosk is given **only the
words that prompt understands**. Rationale and limits:
[`vosk-grammar-shortener.md`](../vosk-grammar-shortener.md).

### The pattern (copy it as is)

```python
from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher
from InputPrompts.PromptVoiceRouter import PromptVoiceRouter

prompt = ColorInputPrompt(Title="Color", Message="Decí el color")
PlaneGrammarSwitcher.ActivateGrammar(
    prompt.GrammarPhrases(PlaneGrammarSwitcher.CurrentLanguage())
)
PromptVoiceRouter.SetActivePrompt(prompt)
try:
    result = prompt.RequestValue()               # modal: returns when closed
finally:
    PromptVoiceRouter.ClearActivePrompt(prompt)  # ALWAYS, or the Browser stays deaf
    PlaneGrammarSwitcher.RestoreCadGrammar()     # the CAD grammar comes back

if result is None or result.Cancelled or not result.Success:
    return None
return result.Value
```

| Piece | Purpose |
| --- | --- |
| `GrammarPhrases(Language)` | List of words the prompt accepts, **in the active language** |
| [`PlaneGrammarSwitcher.ActivateGrammar`](../diagrams/PlaneGrammarSwitcher.md) | Gives that list to Vosk |
| [`PromptVoiceRouter.SetActivePrompt`](../diagrams/PromptVoiceRouter.md) | Diverts what is said to the prompt instead of the `Browser` |
| `try` / `finally` | Guarantees the router is released and the grammar restored even if something fails |

### Which words can be used

- **Only words that are in the Vosk model's vocabulary.** Words that are not
  (file names, odd acronyms) are never recognized; that is why the file browser
  walks through a list instead of asking for the name. Test the real words.
- **Always include confirm and cancel.** `PlaneGrammarSwitcher.PlanePhrases(language)` already
  brings up/down, confirm and cancel.
- **If a phrase has several words**, also add each single word, so they can be
  said separately: `phrases.extend([phrase, *phrase.split()])`.
- **Numeric prompts:** return `True` in `RequiresNumericGrammar()`; the router switches
  to the numbers grammar by itself and restores it
  ([`NumericGrammarSwitcher`](../diagrams/NumericGrammarSwitcher.md)).

### If the command continues after the dialog (non-modal)

`RequestValue()` blocks until the window is closed. If the user has to
**see the model while answering** (as in the guided examples), show it with
`Show()`, which does not block, and take care of three things:

1. Keep a **reference** to the prompt (otherwise Qt garbage-collects it).
2. Release the router on close: `prompt.finished.connect(lambda _c: PromptVoiceRouter.ClearActivePrompt(prompt))`.
3. Restrict the grammar again each time the expected words change, and
   restore it in `done()`.

Full model: [`GuidedExampleInputPrompt`](../diagrams/GuidedExampleInputPrompt.md).

---

## Checklist

- [ ] Does a prompt or helper already exist that does what I need?
- [ ] It inherits from the right base class and closes with `AcceptValue` / `Cancel` / `Fail`.
- [ ] It accepts cancel and the words in all three languages.
- [ ] Grammar restricted with `ActivateGrammar` and restored in a `finally`.
- [ ] Router released in a `finally` (or in `finished` if non-modal).
- [ ] Does not import `FreeCAD` at module level.
- [ ] Tested without a microphone (see [testing.md](testing.md)) and with real voice.
- [ ] Diagram in [`diagrams/`](../diagrams/README.md).

---

Previous: [Adding a submenu](add-submenu.md) · Next: [Testing and validating](testing.md)
