# PromptedCommandExecutor

> **File:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/InputPrompts/PromptedCommandExecutor.py`

The `Browser`'s **command executor**. It is passed in as `on_execute`, and every time
the `Browser` resolves a phrase to a function, it hands it over here. If the
function needs parameters it collects them by voice; if not, it calls it directly.

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
    PromptedCommandExecutor ..> Validator : validation before executing
    PromptedCommandExecutor ..> ContextEntry : reads Target
    PromptedCommandExecutor ..> PromptResult : LastResult
```

## Steps of `ExecuteEntry`

```mermaid
flowchart TD
    A[Entry from the Browser] --> B{is it a<br/>callable?}
    B -->|no| X[LastResult = Fail<br/>prints the error]
    B -->|yes| C[Collector.CollectForFunction]
    C --> D{result?}
    D -->|cancelled| Y[prints cancelled<br/>and does not execute]
    D -->|failed| Z[prints the error<br/>and does not execute]
    D -->|ok| E[Validator.ValidateRequirements]
    E -->|invalid| W[LastResult = Fail<br/>does not execute]
    E -->|valid| F[function with kwargs]
    F -->|exception| V[LastResult = Fail<br/>prints the error]
    F -->|ok| G[prints: command executed]
```

## Design notes

- **A function with no required parameters opens no dialog**: the collector
  returns `Ok({})` and it is called with `function()`.
- **Messages go to the FreeCAD console** (`App.Console.PrintMessage` / `PrintError`)
  and, if FreeCAD is not present (tests), to `print`.
- **The `Validator` is applied twice on purpose:** inside the collector and again right
  before executing, as a pre-check layer. If its integration fails because of an
  import problem, it only warns and executes with the values already collected.
- **`LastResult`** keeps the last result queryable, useful in tests.
- It is built in `integration/voice_bootstrap.py` with the language from the preferences.
