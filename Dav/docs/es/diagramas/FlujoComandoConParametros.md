# Flujo de un comando con parámetros

Qué pasa desde que el usuario dice un comando que necesita valores (por ejemplo
«círculo», que pide radio) hasta que la función corre en FreeCAD. Reúne a
[`Browser`](Browser.md), [`PromptedCommandExecutor`](PromptedCommandExecutor.md),
[`ParameterCollector`](ParameterCollector.md), [`Validator`](Validator.md), los
diálogos de voz y [`PromptVoiceRouter`](PromptVoiceRouter.md).

## Secuencia

```mermaid
sequenceDiagram
    actor U as Usuario
    participant V as DavVoiceService<br/>(hilo del micrófono)
    participant A as BrowserVoiceAdapter
    participant B as Browser
    participant E as PromptedCommandExecutor
    participant C as ParameterCollector
    participant Va as Validator
    participant P as Prompt<br/>(Integer, Float, String u Object)
    participant R as PromptVoiceRouter
    participant F as Función del diccionario

    U->>V: «círculo enviar»
    V->>R: ProcessVoiceText(frase)
    R-->>V: False (no hay prompt activo)
    V->>A: procesar_frase_final
    A->>B: ProcessPhrase
    B->>E: on_execute(Entry)
    E->>C: CollectForFunction(función)
    C->>Va: _BuildSpecs(función)
    Va-->>C: RequirementSpec por parámetro

    loop cada parámetro obligatorio
        C->>P: crea el prompt según el tipo
        C->>R: SetActivePrompt(prompt)
        Note over R: si el prompt es numérico,<br/>cambia la gramática a números
        C->>P: RequestValue() (modal)
        U->>V: «cinco okey»
        V->>R: ProcessVoiceText(frase, Final)
        R->>P: ProcessFinalText (hilo principal)
        P-->>C: AcceptValue(5)
        C->>R: ClearActivePrompt(prompt)
    end

    C->>Va: ValidateRequirements(kwargs)
    Va-->>C: kwargs convertidos
    C-->>E: PromptResult.Ok(kwargs)
    E->>Va: ValidateRequirements (verificación previa)
    E->>F: función(**kwargs)
    F-->>U: el objeto aparece en FreeCAD
```

## Qué puede cortar el flujo

```mermaid
flowchart TD
    A[función con parámetros] --> B{¿algún parámetro<br/>cancelado?}
    B -->|sí| X[no se ejecuta nada]
    B -->|no| C{¿algún parámetro<br/>falló?}
    C -->|sí| Y[error en la consola<br/>no se ejecuta]
    C -->|no| D{¿pasa la<br/>validación?}
    D -->|no| Z[Validator imprime el error<br/>no se ejecuta]
    D -->|sí| E[se ejecuta la función]
    E -->|excepción| W[error en la consola]
```

## Puntos a tener en cuenta

- **Mientras un prompt está activo, el `Browser` no oye.** El router consume las frases
  (`ProcessVoiceText` devuelve `True`), y por eso el registro se libera siempre en un
  `finally`.
- **Los textos de los diálogos se resuelven con el idioma actual**, no con el de arranque
  (ver la propiedad `Language` de `ParameterCollector`).
- **Los tipos salen de la firma de la función.** Una anotación `int` abre un prompt
  numérico entero, `float` uno decimal, `str` uno de texto y cualquier otra cosa uno de
  selección de objetos. Los parámetros con valor por defecto **no se piden**.
- **Otros diálogos no pasan por acá.** Los comandos que arman su propia conversación
  (elegir un plano, abrir un archivo, un ejemplo guiado) abren directamente su prompt
  con los helpers de `Workbench/_prompts.py`; ver
  [`guia-contribuir-dav.md`](../guia-contribuir-dav.md).
- **Probar sin micrófono:** `ExecuteEntry(Entry, SimulatedFinalTexts=["cinco okey"])`.
