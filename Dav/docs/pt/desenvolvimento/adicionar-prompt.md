# Adicionar um diálogo de voz (prompt) e restringir sua gramática

Um **prompt** é uma janela que faz uma pergunta e é respondida falando: um
número, uma opção, um arquivo, sim ou não. Ele existe porque muitos diálogos nativos do
FreeCAD não podem ser controlados por voz, e porque alguns comandos precisam de valores
(«círculo» pede um raio).

Antes de escrever um, veja se já existe algum que sirva: quase sempre basta
**usar um existente** (seções 1 e 2). Escrever uma classe nova (seção 3) é o
último recurso.

---

## 1. O mais simples: deixar que os parâmetros sejam pedidos sozinhos

Se a função do dicionário **declara parâmetros com tipo**, o DAV os pede por voz
sem que você escreva nenhum diálogo. Quem faz isso é o
[`ParameterCollector`](../diagramas/ParameterCollector.md); o percurso completo está
em [`FluxoComandoComParametros`](../diagramas/FluxoComandoComParametros.md).

```python
def makeCircle(radius: float) -> None:
    ...

draft = {'circle': makeCircle}
```

| Anotação | Prompt que se abre |
| --- | --- |
| `int` | número inteiro |
| `float` | número decimal |
| `str` | texto livre |
| qualquer outra / nenhuma | seleção de um objeto do documento |

Um parâmetro **com valor padrão não é pedido**. Se a função não tem parâmetros
obrigatórios, nada é aberto.

---

## 2. Conversas sob medida: os helpers de `Workbench/_prompts.py`

Quando o comando precisa de algo mais que um valor solto (escolher entre dois modos, um
objeto que cumpra uma condição, uma confirmação), use os helpers. Eles já registram o
prompt no router, restringem a gramática e a restauram ao terminar.

| Helper | Pergunta | Retorna |
| --- | --- | --- |
| `askNumber(title, message)` | um número decimal | `float` ou `None` |
| `askChoice(title, message, options)` | uma opção entre poucas | a chave escolhida ou `None` |
| `askYesNo(title, message)` | sim / não | `True`, `False` ou `None` |
| `askText(title, message)` | um texto soletrado | `str` ou `None` |
| `askPlane()` | o plano base | `"XY"`, `"XZ"`, `"YZ"` ou `None` |
| `askObject(doc, title, message, filter, emptyMessage)` | um objeto que cumpra `filter` | o objeto ou `None` |
| `askSketch` / `askShape` / `askSolid` | atalhos de `askObject` | o objeto ou `None` |

**Todos retornam `None` se o usuário cancela**: sempre verifique isso e saia sem fazer nada.

```python
from Workbench._prompts import askChoice, askNumber

mode = askChoice("Grabar", "Elegí el tipo", [
    ("emboss",  "Relieve",     ("relieve", "saliente")),
    ("engrave", "Perforación", ("perforación", "hundido")),
])
if mode is None:
    return
height = askNumber("Grabar", "Decí la altura en mm")
if height is None:
    return
```

Cada opção de `askChoice` é `(chave, texto que se vê, palavras que a escolhem)`.

---

## 3. Uma classe de prompt nova

### O que herdar

| Você precisa de | Herde de |
| --- | --- |
| Um valor livre (texto, número, objeto) | [`BaseInputPrompt`](../diagramas/BaseInputPrompt.md) |
| Um número ditado | [`NumericInputPrompt`](../diagramas/NumericInputPrompt.md): você só implementa `_ParseAccumulatedText` |
| Escolher entre poucas opções com nome | [`ChoiceInputPrompt`](../diagramas/ChoiceInputPrompt.md) |
| Escolher com outro vocabulário de navegação | subclasse de `ChoiceInputPrompt` (veja [`ExampleChoiceInputPrompt`](../diagramas/ExampleChoiceInputPrompt.md)) |

### Esqueleto mínimo

```python
from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser

_COLORS = {"rojo": "red", "azul": "blue"}          # sem acentos


class ColorInputPrompt(BaseInputPrompt):
    """Prompt that picks a color by saying its name."""

    def GrammarPhrases(self, Language: str = "es") -> list[str]:
        """Return the words Vosk should listen for."""
        from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher

        return list(_COLORS) + PlaneGrammarSwitcher.PlanePhrases(Language)

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Accept a color name; cancelar aborts."""
        self.SetHeardText(Text)
        tokens = SpokenNumberParser.Tokenize(Text)   # normaliza acentos e maiúsculas
        if self._HasCancellation(tokens):
            return self.Cancel()
        for word, value in _COLORS.items():
            if word in tokens:
                return self.AcceptValue(value)
        self.SetStatus("No te entendí")
        return self.GetResult()
```

### Regras

- **`ProcessFinalText` recebe a frase já reconhecida.** Compare-a tokenizada com
  `SpokenNumberParser.Tokenize`, que remove acentos e passa para minúsculas; escreva suas
  palavras **sem acentos**.
- **Feche sempre por um caminho explícito:** `AcceptValue(valor)`, `Cancel()` ou `Fail(msg)`
  (deixa a janela aberta para tentar de novo). Não chame `accept()` nem `close()` diretamente.
- **Aceite cancelar sempre** com `_HasCancellation`, e confirmar com `_HasConfirmation`
  se o valor é ditado em várias frases.
- **Três idiomas.** Se você tem palavras próprias, defina-as por idioma (`es`, `en`, `pt`) como
  faz `YesNoInputPrompt`, e aceite as dos três ao mesmo tempo ao comparar.
- **Não importe `FreeCAD` no nível de módulo** em `InputPrompts/`: faça isso dentro das
  funções, assim o prompt pode ser testado sem FreeCAD.
- **Docstrings em inglês, cabeçalho obrigatório**, e um diagrama em `docs/es/diagramas/`.

---

## 4. Restringir a gramática do Vosk

Com o vocabulário aberto, o Vosk confunde as palavras curtas de navegação
(«abajo» por «trabajo»). Enquanto o prompt está aberto, dá-se ao Vosk **somente as
palavras que esse prompt entende**. Fundamento e limites:
[`encurtador-gramatica-vosk.md`](../encurtador-gramatica-vosk.md).

### O padrão (copie-o tal qual)

```python
from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher
from InputPrompts.PromptVoiceRouter import PromptVoiceRouter

prompt = ColorInputPrompt(Title="Color", Message="Decí el color")
PlaneGrammarSwitcher.ActivateGrammar(
    prompt.GrammarPhrases(PlaneGrammarSwitcher.CurrentLanguage())
)
PromptVoiceRouter.SetActivePrompt(prompt)
try:
    result = prompt.RequestValue()               # modal: retorna ao fechar
finally:
    PromptVoiceRouter.ClearActivePrompt(prompt)  # SEMPRE, ou o Browser fica surdo
    PlaneGrammarSwitcher.RestoreCadGrammar()     # volta a gramática de CAD

if result is None or result.Cancelled or not result.Success:
    return None
return result.Value
```

| Peça | Para quê |
| --- | --- |
| `GrammarPhrases(Language)` | Lista de palavras que o prompt aceita, **no idioma ativo** |
| [`PlaneGrammarSwitcher.ActivateGrammar`](../diagramas/PlaneGrammarSwitcher.md) | Dá essa lista ao Vosk |
| [`PromptVoiceRouter.SetActivePrompt`](../diagramas/PromptVoiceRouter.md) | Desvia o que é dito para o prompt em vez de para o `Browser` |
| `try` / `finally` | Garante soltar o router e restaurar a gramática mesmo que algo falhe |

### Quais palavras podem ser usadas

- **Somente palavras que estejam no vocabulário do modelo do Vosk.** As que não estão
  (nomes de arquivos, siglas raras) nunca são reconhecidas; por isso o navegador de
  arquivos percorre uma lista em vez de pedir o nome. Teste as palavras reais.
- **Inclua sempre confirmar e cancelar.** `PlaneGrammarSwitcher.PlanePhrases(idioma)` já
  traz arriba/abajo, confirmar e cancelar.
- **Se uma frase tem várias palavras**, adicione também cada palavra solta, para que
  possam ser ditas separadamente: `phrases.extend([frase, *frase.split()])`.
- **Prompts numéricos:** retorne `True` em `RequiresNumericGrammar()`; o router muda
  sozinho para a gramática de números e a restaura
  ([`NumericGrammarSwitcher`](../diagramas/NumericGrammarSwitcher.md)).

### Se o comando continua depois do diálogo (não modal)

`RequestValue()` bloqueia até a janela ser fechada. Se o usuário precisa
**ver o modelo enquanto responde** (como nos exemplos guiados), mostre-o com
`Show()`, que não bloqueia, e cuide de três coisas:

1. Guardar uma **referência** ao prompt (senão o Qt o coleta).
2. Soltar o router ao fechar: `prompt.finished.connect(lambda _c: PromptVoiceRouter.ClearActivePrompt(prompt))`.
3. Voltar a restringir a gramática cada vez que mudam as palavras esperadas, e
   restaurá-la em `done()`.

Modelo completo: [`GuidedExampleInputPrompt`](../diagramas/GuidedExampleInputPrompt.md).

---

## Checklist

- [ ] Já existe um prompt ou helper que faça o que preciso?
- [ ] Herda da classe base correta e fecha com `AcceptValue` / `Cancel` / `Fail`.
- [ ] Aceita cancelar e as palavras nos três idiomas.
- [ ] Gramática restringida com `ActivateGrammar` e restaurada em um `finally`.
- [ ] Router liberado em um `finally` (ou em `finished` se não for modal).
- [ ] Não importa `FreeCAD` no nível de módulo.
- [ ] Testado sem microfone (veja [testando.md](testando.md)) e com voz real.
- [ ] Diagrama em [`diagramas/`](../diagramas/README.md).

---

Anterior: [Adicionar um submenu](adicionar-submenu.md) · Próximo: [Como testar e validar](testando.md)
