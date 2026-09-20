# GuidedExampleInputPrompt

> **Archivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/InputPrompts/GuidedExampleInputPrompt.py`

Reproductor de ejemplos guiados. Muestra **un cuadro por vez** con las palabras
que el usuario debe decir; cuando las dice todas, en orden, ejecuta la acción del
cuadro y pasa al siguiente. A diferencia del resto de los prompts es **no modal**:
el usuario ve cómo se arma la pieza en la vista 3D mientras sigue el ejemplo.

```mermaid
classDiagram
    class BaseInputPrompt {
        <<QDialog>>
        +ProcessFinalText(Text) PromptResult
        +AcceptValue(Value) PromptResult
        +Cancel() PromptResult
        +SetMessage(Message) void
        +SetStatus(Status) void
    }

    class GuidedExampleInputPrompt {
        -list _Steps
        -int _Viewing
        -int _Pending
        -int _Matched
        +Show() void
        +GrammarPhrases(Language) list
        +ProcessFinalText(Text) PromptResult
        +SkipStep() void
        +done(Code) void
        -_Consume(Text) bool
        -_RunPending() void
        -_View(Index) void
        -_Render() void
        -_ApplyGrammar() void
    }

    class ExampleStep {
        +Text
        +Say
        +Action
    }

    class PromptVoiceRouter {
        +SetActivePrompt(Prompt)$ void
        +ProcessVoiceText(Text, Final)$ bool
    }

    class PlaneGrammarSwitcher {
        +ActivateGrammar(Phrases)$ void
        +RestoreCadGrammar()$ void
    }

    class SpokenNumberParser {
        +Tokenize(Phrase)$ list
    }

    GuidedExampleInputPrompt --|> BaseInputPrompt : hereda
    GuidedExampleInputPrompt o-- "1..*" ExampleStep : cuadros
    GuidedExampleInputPrompt ..> PlaneGrammarSwitcher : acota y restaura la gramática
    GuidedExampleInputPrompt ..> SpokenNumberParser : tokeniza
    PromptVoiceRouter ..> GuidedExampleInputPrompt : entrega la frase
```

## Responsabilidades

| Método | Qué hace |
| --- | --- |
| `ProcessFinalText(Text)` | Cancelar cierra; en el cuadro pendiente compara las palabras o salta; *retroceder*/*avanzar* repasan cuadros; al terminar, *enviar* cierra |
| `_Consume(Text)` | Busca en la frase las palabras pendientes **en orden**; guarda el avance entre frases; al completarlas llama a `_RunPending` |
| `_RunPending()` | Ejecuta `Action`; si falla, el cuadro no avanza y se muestra el error |
| `SkipStep()` | Ejecuta el cuadro sin decir sus palabras (también es el botón de la ventana) |
| `GrammarPhrases(Language)` | Navegación, cancelar y las palabras del **cuadro actual** |
| `Show()` | Muestra la ventana abajo a la derecha del editor, sin bloquearlo |
| `done(Code)` | Restaura la gramática de CAD al cerrarse |

## Estado

```mermaid
stateDiagram-v2
    [*] --> Pendiente
    Pendiente --> Pendiente : dice una palabra (_Matched + 1)
    Pendiente --> Pendiente : la acción falla (_Matched = 0)
    Pendiente --> Pendiente : completa o salta, sigue otro cuadro
    Pendiente --> Terminado : último cuadro hecho
    Terminado --> [*] : enviar o cancelar
    Pendiente --> [*] : cancelar
```

- `_Pending`: primer cuadro sin hacer. `_Viewing`: el que se ve. Solo se puede
  volver a cuadros anteriores (`_Viewing ≤ _Pending`), nunca saltarse uno.
- `_Matched`: palabras ya dichas del cuadro pendiente.

## Notas de diseño

- **Las palabras se acumulan entre frases** dentro de un mismo cuadro, pero una
  palabra fuera de orden no cuenta.
- **La gramática se acota por cuadro:** Vosk solo escucha las palabras del cuadro
  actual y la navegación, lo que mejora el reconocimiento.
- **No modal:** por eso `startExample()` guarda la referencia del reproductor y
  registra la limpieza del router en `finished`.
- El botón *Aceptar* del prompt base pasa a ser *Saltar cuadro* y *Cancelar* pasa a *Cerrar*.
