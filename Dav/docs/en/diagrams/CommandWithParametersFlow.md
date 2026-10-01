# Flow of a command with parameters

What happens from the moment the user says a command that needs values (for example
"círculo" (circle), which asks for a radius) until the function runs in FreeCAD. It brings together
[`Browser`](Browser.md), [`PromptedCommandExecutor`](PromptedCommandExecutor.md),
[`ParameterCollector`](ParameterCollector.md), [`Validator`](Validator.md), the
voice dialogs and [`PromptVoiceRouter`](PromptVoiceRouter.md).

## Sequence

```mermaid
sequenceDiagram
    actor U as User
    participant V as DavVoiceService<br/>(microphone thread)
    participant A as BrowserVoiceAdapter
    participant B as Browser
    participant E as PromptedCommandExecutor
    participant C as ParameterCollector
    participant Va as Validator
    participant P as Prompt<br/>(Integer, Float, String or Object)
    participant R as PromptVoiceRouter
    participant F as Dictionary function

    U->>V: «círculo enviar»
    V->>R: ProcessVoiceText(phrase)
    R-->>V: False (no active prompt)
    V->>A: procesar_frase_final
    A->>B: ProcessPhrase
    B->>E: on_execute(Entry)
    E->>C: CollectForFunction(function)
    C->>Va: _BuildSpecs(function)
    Va-->>C: RequirementSpec per parameter

    loop each required parameter
        C->>P: creates the prompt according to the type
        C->>R: SetActivePrompt(prompt)
        Note over R: if the prompt is numeric,<br/>it switches the grammar to numbers
        C->>P: RequestValue() (modal)
        U->>V: «cinco okey»
        V->>R: ProcessVoiceText(phrase, Final)
        R->>P: ProcessFinalText (main thread)
        P-->>C: AcceptValue(5)
        C->>R: ClearActivePrompt(prompt)
    end

    C->>Va: ValidateRequirements(kwargs)
    Va-->>C: converted kwargs
    C-->>E: PromptResult.Ok(kwargs)
    E->>Va: ValidateRequirements (prior check)
    E->>F: function(**kwargs)
    F-->>U: the object appears in FreeCAD
```

(Spoken Spanish: «círculo enviar» = "circle send"; «cinco okey» = "five okay".)

## What can cut the flow short

```mermaid
flowchart TD
    A[function with parameters] --> B{any parameter<br/>cancelled?}
    B -->|yes| X[nothing is executed]
    B -->|no| C{any parameter<br/>failed?}
    C -->|yes| Y[error in the console<br/>not executed]
    C -->|no| D{does it pass<br/>validation?}
    D -->|no| Z[Validator prints the error<br/>not executed]
    D -->|yes| E[the function is executed]
    E -->|exception| W[error in the console]
```

## Points to keep in mind

- **While a prompt is active, the `Browser` does not listen.** The router consumes the phrases
  (`ProcessVoiceText` returns `True`), which is why the registration is always released in a
  `finally`.
- **The dialog texts are resolved with the current language**, not the startup one
  (see the `Language` property of `ParameterCollector`).
- **The types come from the function's signature.** An `int` annotation opens an integer
  numeric prompt, `float` a decimal one, `str` a text one and anything else an
  object-selection one. Parameters with a default value are **not asked for**.
- **Other dialogs do not go through here.** Commands that build their own conversation
  (choosing a plane, opening a file, a guided example) directly open their own prompt
  with the helpers in `Workbench/_prompts.py`; see
  [`guia-contribuir-dav.md`](../dav-development-guide.md).
- **Testing without a microphone:** `ExecuteEntry(Entry, SimulatedFinalTexts=["cinco okey"])`.
