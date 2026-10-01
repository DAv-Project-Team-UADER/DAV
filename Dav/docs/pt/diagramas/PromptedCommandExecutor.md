# PromptedCommandExecutor

> **Arquivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/InputPrompts/PromptedCommandExecutor.py`

O **executor de comandos** do `Browser`. É passado como `on_execute` e, toda vez
que o `Browser` resolve uma frase para uma função, ela é entregue aqui. Se a
função pede parâmetros, ele os coleta por voz; se não, chama-a diretamente.

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
    PromptedCommandExecutor ..> Validator : validação prévia à execução
    PromptedCommandExecutor ..> ContextEntry : lê Target
    PromptedCommandExecutor ..> PromptResult : LastResult
```

## Passos de `ExecuteEntry`

```mermaid
flowchart TD
    A[Entry do Browser] --> B{é um<br/>callable?}
    B -->|não| X[LastResult = Fail<br/>imprime o erro]
    B -->|sim| C[Collector.CollectForFunction]
    C --> D{resultado?}
    D -->|cancelado| Y[imprime cancelado<br/>e não executa]
    D -->|falhou| Z[imprime o erro<br/>e não executa]
    D -->|ok| E[Validator.ValidateRequirements]
    E -->|inválido| W[LastResult = Fail<br/>não executa]
    E -->|válido| F[function com kwargs]
    F -->|exceção| V[LastResult = Fail<br/>imprime o erro]
    F -->|ok| G[imprime: comando executado]
```

## Notas de design

- **Uma função sem parâmetros obrigatórios não abre nenhum diálogo**: o coletor
  devolve `Ok({})` e a função é chamada com `function()`.
- **As mensagens vão para o console do FreeCAD** (`App.Console.PrintMessage` / `PrintError`)
  e, se o FreeCAD não está presente (testes), para `print`.
- **O `Validator` é aplicado duas vezes de propósito:** dentro do coletor e novamente logo
  antes de executar, como camada de verificação prévia. Se a sua integração falhar por um
  problema de importação, apenas avisa e executa com os valores já coletados.
- **`LastResult`** deixa o último resultado consultável, útil em testes.
- É construído em `integration/voice_bootstrap.py` com o idioma das preferências.
