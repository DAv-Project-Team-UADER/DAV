# NumericInputPrompt

> **Arquivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/InputPrompts/NumericInputPrompt.py`

Modelo (template) dos prompts que pedem **um número ditado**. Guarda o que o usuário
vai dizendo, mesmo que o faça em várias frases («cinco» … «coma» … «dos» … «okey»), e
só quando ouve uma palavra de confirmação o converte. As subclasses apenas
implementam **como converter** o texto acumulado.

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
    PromptVoiceRouter ..> NumericInputPrompt : consulta RequiresNumericGrammar
    PromptVoiceRouter ..> NumericGrammarSwitcher : troca a gramática
```

## Fluxo de uma frase

```mermaid
flowchart TD
    A[ProcessFinalText] --> B{palavra de<br/>cancelar?}
    B -->|sim| C[apaga o acumulado<br/>e cancela]
    B -->|não| D{palavra de<br/>confirmar?}
    D -->|não| E[soma a frase a<br/>_AccumulatedText]
    D -->|sim| F{há algo<br/>acumulado?}
    F -->|não| G[avisa: falta um valor]
    F -->|sim| H[_ParseAccumulatedText]
    H -->|ValueError| I[Fail: permite tentar de novo]
    H -->|número| J[AcceptValue]
```

## Notas de design

- **Padrão template method.** O fluxo acumular / confirmar / cancelar vive uma única vez aqui; um
  novo tipo numérico só sobrescreve `_ParseAccumulatedText`.
- **`RequiresNumericGrammar()` devolve `True`.** Assim o [`PromptVoiceRouter`](PromptVoiceRouter.md)
  troca a gramática do Vosk para as palavras de números **sem verificar tipos concretos**.
- A conversão de palavras em número (incluindo «coma», «menos» e dezenas) está em
  [`SpokenNumberParser`](SpokenNumberParser.md).
- Um erro de conversão (`ValueError`) usa `Fail`: o diálogo permanece aberto e o acumulado
  já foi descartado, então o usuário volta a ditar o número.
