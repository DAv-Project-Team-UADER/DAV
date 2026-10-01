# SpokenNumberParser

> **File:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/InputPrompts/SpokenNumberParser.py`

Converts **dictated phrases into numbers** ("veintiuno coma cinco" (twenty-one point five) → `21.5`) and provides
the text tools used by all the prompts: normalizing without accents,
tokenizing, and the confirm and cancel words. It is a class with only class
methods, with no per-instance state.

```mermaid
classDiagram
    class SpokenNumberParser {
        <<static>>
        +dict DigitWords
        +dict TensWords
        +set ConnectorWords
        +dict UnitWords
        +set DecimalWords
        +set NegativeWords
        +set ConfirmationWords
        +set CancellationWords
        +ParseInteger(Phrase)$ int
        +ParseFloat(Phrase)$ float
        +TryParseInteger(Phrase)$ int
        +TryParseFloat(Phrase)$ float
        +ParseNumberText(Phrase, AllowDecimal)$ str
        +Tokenize(Phrase)$ list
        +NormalizeText(Text)$ str
        -_MergeTensAndUnits(Tokens)$ list
        -_TokenToNumericText(Token)$ str
    }

    class NavActions {
        <<Dav dic NavCommands>>
        +send
        +cancel
    }

    class BaseInputPrompt
    class NumericInputPrompt
    class ParameterCollector

    BaseInputPrompt ..> SpokenNumberParser : confirm and cancel
    NumericInputPrompt ..> SpokenNumberParser : ParseInteger and ParseFloat
    ParameterCollector ..> SpokenNumberParser : simulated mode
    SpokenNumberParser ..> NavActions : extends confirm and cancel on load
```

## Responsibilities

| Method | What it does |
| --- | --- |
| `NormalizeText(Text)` | Lowercase, without accents or eñes; the comma becomes a decimal point |
| `Tokenize(Phrase)` | Normalizes and splits into words and numbers |
| `ParseNumberText(Phrase, AllowDecimal)` | Builds the number as text: digits, sign (`menos` (minus)) and decimal separator (`coma` (comma), `punto` (point)) |
| `ParseInteger` / `ParseFloat` | Convert to `int` / `float`; raise `ValueError` if the phrase is not a number |
| `TryParseInteger` / `TryParseFloat` | Same, but return `None` instead of raising |

## How a number is read

```mermaid
flowchart LR
    A["«veintiuno coma cinco»"] --> B[Tokenize]
    B --> C[_MergeTensAndUnits<br/>tens and units]
    C --> D{each word}
    D -->|confirm| E[stops]
    D -->|menos| F[sign]
    D -->|coma| G[decimal]
    D -->|digit| H[appends to the text]
    E --> I["'21.5'"]
    F --> I
    G --> I
    H --> I
    I --> J[int or float]
```

## Design notes

- **Three languages in a single table.** Words of any language are accepted at the
  same time; there is no need to know which language was dictated.
- **Confirm and cancel are extended when the module is imported.** `_LoadNavWordsFromDictionaries`
  adds the phrases from `NavCommands/TraduceTo*.py` that point to `send` and `cancel`. This way, a
  new synonym added to the dictionary works in all the prompts without touching code.
  If the dictionary is not available, the basic words written in the class remain.
- **`ConnectorWords`** ("y" / "e", i.e. "and") join tens and units: "treinta y cinco" (thirty-five).
- Limits and improvement proposal for numeric dictation:
  [`voice-numbers-limits-and-proposal.md`](../voice-numbers-limits-and-proposal.md).
