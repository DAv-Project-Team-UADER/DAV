# Fluxo de um comando com parâmetros

O que acontece desde que o usuário diz um comando que precisa de valores (por exemplo
«círculo», que pede raio) até que a função rode no FreeCAD. Reúne
[`Browser`](Browser.md), [`PromptedCommandExecutor`](PromptedCommandExecutor.md),
[`ParameterCollector`](ParameterCollector.md), [`Validator`](Validator.md), os
diálogos de voz e [`PromptVoiceRouter`](PromptVoiceRouter.md).

## Sequência

```mermaid
sequenceDiagram
    actor U as Usuário
    participant V as DavVoiceService<br/>(thread do microfone)
    participant A as BrowserVoiceAdapter
    participant B as Browser
    participant E as PromptedCommandExecutor
    participant C as ParameterCollector
    participant Va as Validator
    participant P as Prompt<br/>(Integer, Float, String ou Object)
    participant R as PromptVoiceRouter
    participant F as Função do dicionário

    U->>V: «círculo enviar»
    V->>R: ProcessVoiceText(frase)
    R-->>V: False (não há prompt ativo)
    V->>A: procesar_frase_final
    A->>B: ProcessPhrase
    B->>E: on_execute(Entry)
    E->>C: CollectForFunction(função)
    C->>Va: _BuildSpecs(função)
    Va-->>C: RequirementSpec por parâmetro

    loop cada parâmetro obrigatório
        C->>P: cria o prompt conforme o tipo
        C->>R: SetActivePrompt(prompt)
        Note over R: se o prompt é numérico,<br/>troca a gramática para números
        C->>P: RequestValue() (modal)
        U->>V: «cinco okey»
        V->>R: ProcessVoiceText(frase, Final)
        R->>P: ProcessFinalText (thread principal)
        P-->>C: AcceptValue(5)
        C->>R: ClearActivePrompt(prompt)
    end

    C->>Va: ValidateRequirements(kwargs)
    Va-->>C: kwargs convertidos
    C-->>E: PromptResult.Ok(kwargs)
    E->>Va: ValidateRequirements (verificação prévia)
    E->>F: função(**kwargs)
    F-->>U: o objeto aparece no FreeCAD
```

## O que pode cortar o fluxo

```mermaid
flowchart TD
    A[função com parâmetros] --> B{algum parâmetro<br/>cancelado?}
    B -->|sim| X[nada é executado]
    B -->|não| C{algum parâmetro<br/>falhou?}
    C -->|sim| Y[erro no console<br/>não é executado]
    C -->|não| D{passa na<br/>validação?}
    D -->|não| Z[Validator imprime o erro<br/>não é executado]
    D -->|sim| E[a função é executada]
    E -->|exceção| W[erro no console]
```

## Pontos a ter em conta

- **Enquanto um prompt está ativo, o `Browser` não ouve.** O router consome as frases
  (`ProcessVoiceText` devolve `True`), e por isso o registro é sempre liberado em um
  `finally`.
- **Os textos dos diálogos são resolvidos com o idioma atual**, não com o da inicialização
  (ver a propriedade `Language` de `ParameterCollector`).
- **Os tipos saem da assinatura da função.** Uma anotação `int` abre um prompt
  numérico inteiro, `float` um decimal, `str` um de texto e qualquer outra coisa um de
  seleção de objetos. Os parâmetros com valor padrão **não são pedidos**.
- **Outros diálogos não passam por aqui.** Os comandos que montam sua própria conversa
  (escolher um plano, abrir um arquivo, um exemplo guiado) abrem diretamente seu prompt
  com os helpers de `Workbench/_prompts.py`; ver
  [`guia-contribuir-dav.md`](../guia-desenvolvimento-dav.md).
- **Testar sem microfone:** `ExecuteEntry(Entry, SimulatedFinalTexts=["cinco okey"])`.
