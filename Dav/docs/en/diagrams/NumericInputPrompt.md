# NumericInputPrompt

> **File:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/InputPrompts/NumericInputPrompt.py`

Template for the prompts that ask for **a dictated number**. It stores what the user
says even when it is spread over several phrases ("cinco" (five) ... "coma" (point) ... "dos" (two) ... "okey") and
only converts it once it hears a confirmation word. Subclasses only
implement **how to convert** the accumulated text.

```mermaid
classDiagram
    class BaseInputPrompt {
        <<QDialog>>
        #str _AccumulatedText
        +RequiresNumericGrammar() bool
    }

    class NumericInputPrompt {
        <<template>>
        +RequiresNumericGrammar() bool
        +ProcessFinalText(Text) PromptResult
        #_ParseAccumulatedText(Text)* Any
    }

    class IntegerInputPrompt {
        #_ParseAccumulatedText(Text) int
    }

    class FloatInputPrompt {
        #_ParseAccumulatedText(Text) float
    }

    class SpokenNumberParser {
        +ParseInteger(Phrase)$ int
        +ParseFloat(Phrase)$ float
    }

    class NumericGrammarSwitcher {
        +ActivateNumericGrammar()$ void
        +RestoreCadGrammar()$ void
    }

    class PromptVoiceRouter {
        +SetActivePrompt(Prompt)$ void
    }

    NumericInputPrompt --|> BaseInputPrompt
    IntegerInputPrompt --|> NumericInputPrompt
    FloatInputPrompt --|> NumericInputPrompt
    IntegerInputPrompt ..> SpokenNumberParser : ParseInteger
    FloatInputPrompt ..> SpokenNumberParser : ParseFloat
    PromptVoiceRouter ..> NumericInputPrompt : asks RequiresNumericGrammar
    PromptVoiceRouter ..> NumericGrammarSwitcher : switches the grammar
```

## Flow of a phrase

```mermaid
flowchart TD
    A[ProcessFinalText] --> B{cancel<br/>word?}
    B -->|yes| C[clears what was accumulated<br/>and cancels]
    B -->|no| D{confirm<br/>word?}
    D -->|no| E[adds the phrase to<br/>_AccumulatedText]
    D -->|yes| F{anything<br/>accumulated?}
    F -->|no| G[warns: a value is missing]
    F -->|yes| H[_ParseAccumulatedText]
    H -->|ValueError| I[Fail: lets the user retry]
    H -->|number| J[AcceptValue]
```

## Design notes

- **Template pattern.** The accumulate / confirm / cancel flow lives here only once; a new
  numeric type just overrides `_ParseAccumulatedText`.
- **`RequiresNumericGrammar()` returns `True`.** This way [`PromptVoiceRouter`](PromptVoiceRouter.md)
  switches the Vosk grammar to the number words **without checking concrete types**.
- The conversion from words to number (including "coma" (point), "menos" (minus) and tens) is in
  [`SpokenNumberParser`](SpokenNumberParser.md).
- A conversion error (`ValueError`) uses `Fail`: the dialog stays open and what was accumulated
  has already been discarded, so the user dictates the number again.
