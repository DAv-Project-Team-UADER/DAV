# PromptedCommandExecutor

> **Archivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/InputPrompts/PromptedCommandExecutor.py`

El **ejecutor de comandos** del `Browser`. Se le pasa como `on_execute` y cada vez
que el `Browser` resuelve una frase a una función, se la entrega acá. Si la
función pide parámetros los recolecta por voz; si no, la llama directamente.

```mermaid
classDiagram
    class Browser {
        +ProcessPhrase(spoken) BrowserResult
    }

    class PromptedCommandExecutor {
        +ParameterCollector Collector
        +PromptResult LastResult
        +__call__(Entry) Any
        +ExecuteEntry(Entry, SimulatedFinalTexts) Any
        -_IsCallableEntry(Entry)$ bool
        -_GetEntryTarget(Entry)$ Callable
    }

    class ParameterCollector {
        +CollectForFunction(Function, Simulated) PromptResult
    }

    class Validator {
        +ValidateRequirements(Language, Function, UserData) tuple
    }

    class ContextEntry {
        +IsCallable() bool
        +Target
        +InternalKey
    }

    class PromptResult

    Browser ..> PromptedCommandExecutor : on_execute(Entry)
    PromptedCommandExecutor o-- ParameterCollector : Collector
    PromptedCommandExecutor ..> Validator : validación previa a ejecutar
    PromptedCommandExecutor ..> ContextEntry : lee Target
    PromptedCommandExecutor ..> PromptResult : LastResult
```

## Pasos de `ExecuteEntry`

```mermaid
flowchart TD
    A[Entry del Browser] --> B{¿es un<br/>callable?}
    B -->|no| X[LastResult = Fail<br/>imprime el error]
    B -->|sí| C[Collector.CollectForFunction]
    C --> D{¿resultado?}
    D -->|cancelado| Y[imprime cancelado<br/>y no ejecuta]
    D -->|falló| Z[imprime el error<br/>y no ejecuta]
    D -->|ok| E[Validator.ValidateRequirements]
    E -->|inválido| W[LastResult = Fail<br/>no ejecuta]
    E -->|válido| F[function con kwargs]
    F -->|excepción| V[LastResult = Fail<br/>imprime el error]
    F -->|ok| G[imprime: comando ejecutado]
```

## Notas de diseño

- **Una función sin parámetros obligatorios no abre ningún diálogo**: el colector
  devuelve `Ok({})` y se llama con `function()`.
- **Los mensajes van a la consola de FreeCAD** (`App.Console.PrintMessage` / `PrintError`)
  y, si FreeCAD no está (tests), a `print`.
- **El `Validator` se aplica dos veces a propósito:** dentro del colector y de nuevo justo
  antes de ejecutar, como capa de verificación previa. Si su integración falla por un
  problema de importación solo avisa y ejecuta con los valores ya recolectados.
- **`LastResult`** deja el último resultado consultable, útil en pruebas.
- Se construye en `integration/voice_bootstrap.py` con el idioma de las preferencias.
