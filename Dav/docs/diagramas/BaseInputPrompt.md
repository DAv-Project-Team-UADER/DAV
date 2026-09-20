# BaseInputPrompt

> **Archivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/InputPrompts/BaseInputPrompt.py`

Clase base de todos los diálogos de voz. Es un `QDialog` con un mensaje, una línea
de estado, el texto que se escuchó y los botones *Aceptar* / *Cancelar*. No sabe
qué se le pide al usuario: cada subclase decide qué hacer con lo que oye
(`ProcessFinalText`) y cuándo dar el valor por bueno (`AcceptValue`).

```mermaid
classDiagram
    class QDialog {
        <<Qt>>
    }

    class BaseInputPrompt {
        +Signal ResultReady
        #str _Language
        #PromptResult _Result
        #str _AccumulatedText
        +SetTitle(Title) void
        +SetMessage(Message) void
        +SetStatus(Status) void
        +SetHeardText(Text) void
        +GetCurrentText() str
        +GetResult() PromptResult
        +ProcessPartialText(Text) void
        +ProcessFinalText(Text) PromptResult
        +RequiresNumericGrammar() bool
        +AcceptValue(Value) PromptResult
        +Fail(Error) PromptResult
        +Cancel() PromptResult
        +Show() void
        +RequestValue() PromptResult
        +reject() void
        #_HasConfirmation(Tokens)$ bool
        #_HasCancellation(Tokens)$ bool
    }

    class PromptResult {
        <<dataclass, frozen>>
        +bool Success
        +Any Value
        +bool Cancelled
        +str Error
        +Pending()$ PromptResult
        +Ok(Value)$ PromptResult
        +Cancel()$ PromptResult
        +Fail(Error)$ PromptResult
    }

    class InputPromptI18n {
        <<módulo>>
        +ResolveLanguage() str
        +T(Language, Key) str
        +KindLabel(Language, Kind) str
    }

    class SpokenNumberParser {
        +set ConfirmationWords
        +set CancellationWords
    }

    BaseInputPrompt --|> QDialog
    BaseInputPrompt ..> PromptResult : guarda el resultado
    BaseInputPrompt ..> InputPromptI18n : textos por idioma
    BaseInputPrompt ..> SpokenNumberParser : palabras de confirmar y cancelar
```

## Responsabilidades

| Método | Qué hace |
| --- | --- |
| `ProcessFinalText(Text)` | Punto de extensión: la base solo muestra el texto. Las subclases lo reemplazan |
| `ProcessPartialText(Text)` | Muestra lo que se va reconociendo mientras el usuario habla |
| `AcceptValue(Value)` | Guarda `PromptResult.Ok`, emite `ResultReady` y cierra. Rechaza un texto vacío |
| `Fail(Error)` | Guarda el error y **deja el diálogo abierto** para reintentar |
| `Cancel()` | Guarda el resultado cancelado y cierra |
| `RequestValue()` | Lo muestra **modal** (`exec`) y devuelve el resultado al cerrarse |
| `Show()` | Lo muestra sin bloquear (lo usa [`GuidedExampleInputPrompt`](GuidedExampleInputPrompt.md)) |
| `RequiresNumericGrammar()` | `False` por defecto; los prompts numéricos devuelven `True` para que el router cambie la gramática |
| `reject()` | Cerrar la ventana cuenta como cancelar |

## Estados del resultado

```mermaid
stateDiagram-v2
    [*] --> Pending : se crea el prompt
    Pending --> Ok : AcceptValue
    Pending --> Failed : Fail
    Failed --> Pending : el usuario reintenta
    Failed --> Ok : AcceptValue
    Pending --> Cancelled : Cancel o cerrar la ventana
    Ok --> [*]
    Cancelled --> [*]
```

## Notas de diseño

- **Tema claro u oscuro.** `_IsDarkTheme()` lee la preferencia de tema de FreeCAD (su
  paleta de Qt sigue siendo clara con el tema oscuro) y solo si no dice nada mira la
  paleta. Texto negro sobre claro, rojo sobre oscuro.
- **El idioma se lee al crear el prompt** con `ResolveLanguage()`, la misma fuente que
  usan el `Browser` y el `Tagger`.
- **PySide6 primero, PySide2 de respaldo**, como el resto de la GUI.
- **Subclases:** [`FileSelectionInputPrompt`](FileSelectionInputPrompt.md),
  [`ObjectSelectionInputPrompt`](ObjectSelectionInputPrompt.md),
  [`NumericInputPrompt`](NumericInputPrompt.md), [`YesNoInputPrompt`](YesNoInputPrompt.md),
  [`ChoiceInputPrompt`](ChoiceInputPrompt.md), [`PlaneSelectionInputPrompt`](PlaneSelectionInputPrompt.md),
  [`SpellingInputPrompt`](SpellingInputPrompt.md), `StringInputPrompt` y
  [`GuidedExampleInputPrompt`](GuidedExampleInputPrompt.md).
