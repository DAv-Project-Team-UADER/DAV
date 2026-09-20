# SpellingInputPrompt

> **Archivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/InputPrompts/SpellingInputPrompt.py`

Diálogo de voz que arma un texto **letra por letra**. Lo usa el comando
`grabar` para pedir el texto a grabar (ver
[`manual-croquis-y-grabado-voz.md`](../manual-croquis-y-grabado-voz.md)). El
usuario dice el nombre de cada letra, dígitos, `espacio`, `borrar` y `okey`.

```mermaid
classDiagram
    class BaseInputPrompt {
        <<QDialog>>
        +ProcessFinalText(Text) PromptResult
        +ProcessPartialText(Text) void
        +AcceptValue(Value) PromptResult
        +Fail(Error) PromptResult
        +Cancel() PromptResult
        +SetHeardText(Text) void
        +SetStatus(Status) void
    }

    class SpellingInputPrompt {
        +dict LetterNames
        +dict PairNames
        +dict PairWords
        +dict SpaceWords
        +dict DeleteWords
        +set SpaceTokens
        +set DeleteTokens
        -str _Text
        -int _MaxLength
        -dict _Lookup

        +GrammarPhrases(Language)$ list
        +GetText() str
        +ProcessPartialText(Text) void
        +ProcessFinalText(Text) PromptResult
        -_Append(Char) void
        -_Refresh() void
        -_StatusText() str
    }

    class SpokenNumberParser {
        +dict DigitWords
        +set ConfirmationWords
        +set CancellationWords
        +Tokenize(Phrase)$ list
        +NormalizeText(Text)$ str
    }

    class PlaneGrammarSwitcher {
        +PlanePhrases(Language)$ list
        +ActivateGrammar(Phrases)$ void
        +RestoreCadGrammar()$ void
    }

    class PromptResult {
        +bool Success
        +Any Value
        +bool Cancelled
    }

    SpellingInputPrompt --|> BaseInputPrompt : hereda
    SpellingInputPrompt ..> SpokenNumberParser : tokeniza y lee dígitos
    SpellingInputPrompt ..> PlaneGrammarSwitcher : palabras de confirmar y cancelar
    SpellingInputPrompt ..> PromptResult : devuelve el texto en mayúsculas
```

## Responsabilidades

| Método | Qué hace |
| --- | --- |
| `ProcessFinalText(Text)` | Recorre las palabras de la frase: aplica letras, dígitos, `espacio` y `borrar`; corta en la primera palabra de confirmación (`okey`…) y acepta el texto. Una palabra de cancelación aborta todo |
| `GrammarPhrases(Language)` | Palabras que Vosk debe escuchar mientras se deletrea: nombres de letra del idioma, dígitos, `espacio`, `borrar`, confirmación y cancelación (sin `arriba`/`abajo`) |
| `GetText()` | Texto armado hasta ahora |
| `ProcessPartialText(Text)` | Ignora los parciales: una letra solo cuenta cuando llega el resultado final |

## Recorrido de una frase

```mermaid
sequenceDiagram
    participant U as Usuario
    participant V as DavVoiceService
    participant R as PromptVoiceRouter
    participant P as SpellingInputPrompt
    participant E as engraveText

    E->>P: askText(...) crea el prompt
    E->>V: ActivateGrammar(GrammarPhrases)
    E->>R: SetActivePrompt(prompt)
    U->>V: "d a v"
    V->>R: texto final
    R->>P: ProcessFinalText("d a v")
    P-->>U: muestra "DAV_"
    U->>V: "espacio uno dos"
    V->>R: texto final
    R->>P: ProcessFinalText(...)
    P-->>U: muestra "DAV 12_"
    U->>V: "okey"
    R->>P: ProcessFinalText("okey")
    P->>E: AcceptValue("DAV 12")
    E->>V: RestoreCadGrammar()
```

## Notas de diseño

- **Gramática acotada.** Con el vocabulario abierto de un modelo pequeño, las
  letras sueltas se confunden con cualquier palabra. Por eso, mientras el prompt
  está activo, Vosk solo escucha las palabras de `GrammarPhrases`.
- **Un idioma en la gramática, tres al parsear.** La gramática lista solo los
  nombres de letra del idioma activo, pero `_Lookup` junta los tres idiomas: si
  el usuario dice una letra en otro idioma, se entiende igual.
- **Las tablas solo tienen palabras que Vosk conoce.** Se comprobaron contra el
  vocabulario de los modelos pequeños. Lo que falta se dice de otra forma: en
  portugués `fê`, `n` y `duplo vê` (F, N y W); en español la `ñ` se acepta como
  `ñ` suelta o `eñe`, aunque el modelo pequeño solo conoce la primera.
- **Letras de dos palabras** (`doble uve`, `i griega`) se resuelven mirando la
  palabra siguiente antes de interpretar la primera; `i` sola es la letra I.
- **La Ñ se protege antes de normalizar.** `SpokenNumberParser.NormalizeText`
  quita las tildes y `ñ` quedaría como `n`, así que `eñe` y `ñ` se reemplazan por
  un marcador interno antes de tokenizar.
- **Letras sueltas.** Vosk a veces devuelve la letra pelada (`d`, `v`); se acepta
  cualquier carácter alfabético de una sola letra.
- **Solo dígitos sueltos.** Se usan las entradas de `DigitWords` de un carácter;
  `veinticuatro` o `diez` no se reconocen y se ignoran sin avisar.
- **Salida en mayúsculas**, con un máximo de 40 caracteres (`MaxLength`).
