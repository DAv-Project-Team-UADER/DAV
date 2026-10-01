# Adicionar um comando por voz

O objetivo é que, ao dizer uma **frase falada**, seja executada uma **ação** do
FreeCAD. Isso é conseguido mexendo na **árvore de comandos** (`Dav/dic/`), sem
mexer no motor (`Browser`).

Cada pasta de `Dav/dic/` é um **nível de contexto** e tem:

1. **Um dicionário mestre** (`<nome>.py`) — chaves internas → callables.
2. **Traduções por idioma** (`TraduceToEs.py`, `TraduceToEn.py`,
   `TraduceToPT.py`) — frases faladas → os mesmos callables.

## Passo a passo

### 1. Localize a pasta do contexto

Por exemplo, os comandos do workbench Sketcher ficam em
`Dav/dic/Workbench/Sketcher/`. Se o comando corresponde a um submenu, ele vai na
sua pasta filha (ex.: `Sketcher/point/point.py`, `Sketcher/Geometry/geometry.py`).

### 2. Adicione a chave interna ao dicionário mestre

Dentro do dict mestre (ex.: `sketcher.py`), adicione a chave e seu callable:

```python
sketcher = {}
sketcher.update({
    'new': _new_sketch,     # função própria que cria o esboço
    'edit': lambda: Gui.runCommand('Sketcher_EditSketch', 0),
    # ...
})
```

> Se a ação é um comando nativo do FreeCAD que **não** abre um diálogo
> controlável por voz, um `lambda: Gui.runCommand('Comando_De_FreeCAD', 0)`
> basta. Se o comando nativo abre um diálogo próprio (como o seletor de
> plano de `Sketcher_NewSketch`), é preciso substituí-lo por uma ação própria do
> DAV com um prompt controlável por voz (veja o exemplo mais abaixo).

### 3. Adicione as frases faladas nos `TraduceTo*.py`

No `TraduceToEs.py` do contexto, mapeie a(s) frase(s) para a chave:

```python
from .sketcher import sketcher

TraduceToEs = {
    "nuevo": sketcher["new"],
    "nuevo croquis": sketcher["new"],
    "crear croquis": sketcher["new"],
    # ...
}
```

> Adicionar sinônimos é **somente** editar esses dicionários: não é preciso
> mexer no motor. O `DictionaryLoader` normaliza acentos ao comparar, então as
> variantes com/sem acento são opcionais, mas inofensivas.

### 4. (Opcional) Atualize o `ayuda.py` da pasta

Muitos contextos têm um `ayuda.py` que imprime os comandos disponíveis.
Adicione a linha do novo comando para que a ajuda fique consistente.

### 5. Teste

Verifique que a frase navega e executa a ação (veja
[testando.md](testando.md)). Teste nos **três idiomas** se você adicionou frases
nos três `TraduceTo`.

---

## Exemplo real: o seletor de plano por voz ao criar um esboço

Contexto: o FreeCAD abre um diálogo nativo (`Sketcher_NewSketch`) que **não é
controlável por voz**. A solução foi uma ação própria do DAV que mostra um
prompt navegável por voz.

**Arquivos alterados** (referência):

- `Dav/scr/.../InputPrompts/PlaneSelectionInputPrompt.py` — a janela de
  seleção: percorre `XY` / `XZ` / `YZ` com `arriba`/`abajo` (para cima/para baixo)
  e confirma com `okey`/`cancelar` (herdando `BaseInputPrompt`).
- `Dav/dic/Workbench/Sketcher/new_sketch/new_sketch.py` — a ação: mostra o
  prompt, pega o plano escolhido e cria o `Sketcher::SketchObject` com o
  mesmo placement que o comando nativo.
- `Dav/scr/.../InputPrompts/PlaneGrammarSwitcher.py` — restringe a gramática do
  Vosk enquanto o prompt está aberto a somente `arriba/abajo/okey/cancelar`,
  para que ele não confunda "abajo" com "trabajo".
- `Dav/dic/Workbench/Sketcher/sketcher.py` — `'new'` agora aponta para
  `_new_sketch` em vez de `Gui.runCommand('Sketcher_NewSketch', 0)`.
- `Dav/dic/Workbench/Sketcher/Geometry/geometry.py` — idem para o subcontexto
  de geometria.
- `Dav/dic/Workbench/Sketcher/TraduceToEs.py` — novos sinônimos
  `nuevo boceto` / `crear boceto` / `boceto nuevo`.

**Pontos a copiar deste exemplo**:

- Se o comando abre um diálogo nativo, **substitua-o** por um prompt DAV
  (herde `BaseInputPrompt` e use `PromptVoiceRouter`).
- Se o prompt precisa que o Vosk escute apenas um conjunto pequeno de palavras,
  use um "grammar switcher" (padrão `NumericGrammarSwitcher`) e restaure-o
  ao fechar.
- Avise na GUI (com `print`) o resultado da ação para que apareça no
  histórico do painel.

---

## Regras para não quebrar nada

- **Subcontextos aninhados**: `explorer.update({'file': file})`, nunca
  `explorer.update(file)`. Veja [convenções](convencoes.md) e
  `pendientes-dav.md` §4.
- Os `TraduceTo*.py` devem importar o dict mestre e vincular
  **por objeto/chave**, sem duplicar callables.
- Mantenha o **cabeçalho obrigatório** em cada arquivo novo.
- Não mexa em `browser.py` para adicionar um comando: o comando vai no dicionário.

---

Precisa de uma pasta nova? Veja [Adicionar um submenu](adicionar-submenu.md). Um diálogo de voz? Veja [Adicionar um diálogo de voz](adicionar-prompt.md).

Próximo: [Adicionar um submenu](adicionar-submenu.md)
