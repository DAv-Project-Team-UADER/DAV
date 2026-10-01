# NumericInputPrompt

> **Archivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/InputPrompts/NumericInputPrompt.py`

Plantilla de los prompts que piden **un número dictado**. Guarda lo que el usuario
va diciendo aunque lo haga en varias frases («cinco» … «coma» … «dos» … «okey») y
recién cuando oye una palabra de confirmación lo convierte. Las subclases solo
implementan **cómo convertir** el texto acumulado.

```mermaid
classDiagram
    class BaseInputPrompt {
        <<QDialog>>
        #str _AccumulatedText
        +RequiresNumericGrammar() bool
    }

    class NumericInputPrompt {
        <<plantilla>>
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
    PromptVoiceRouter ..> NumericInputPrompt : pregunta RequiresNumericGrammar
    PromptVoiceRouter ..> NumericGrammarSwitcher : cambia la gramática
```

## Flujo de una frase

```mermaid
flowchart TD
    A[ProcessFinalText] --> B{¿palabra de<br/>cancelar?}
    B -->|sí| C[borra lo acumulado<br/>y cancela]
    B -->|no| D{¿palabra de<br/>confirmar?}
    D -->|no| E[suma la frase a<br/>_AccumulatedText]
    D -->|sí| F{¿hay algo<br/>acumulado?}
    F -->|no| G[avisa: falta un valor]
    F -->|sí| H[_ParseAccumulatedText]
    H -->|ValueError| I[Fail: deja reintentar]
    H -->|número| J[AcceptValue]
```

## Notas de diseño

- **Patrón plantilla.** El flujo acumular / confirmar / cancelar vive una sola vez acá; un
  tipo numérico nuevo solo sobreescribe `_ParseAccumulatedText`.
- **`RequiresNumericGrammar()` devuelve `True`.** Así [`PromptVoiceRouter`](PromptVoiceRouter.md)
  cambia la gramática de Vosk a las palabras de números **sin comprobar tipos concretos**.
- La conversión de palabras a número (incluido «coma», «menos» y decenas) está en
  [`SpokenNumberParser`](SpokenNumberParser.md).
- Un error de conversión (`ValueError`) usa `Fail`: el diálogo queda abierto y lo acumulado
  ya se descartó, así que el usuario vuelve a dictar el número.
