# Adicionar um submenu (uma pasta nova) à árvore de comandos

[Adicionar um comando](adicionar-comando.md) explica como adicionar **uma frase** a um
contexto que já existe. Esta página cobre o caso seguinte: criar **um contexto
novo**, ou seja, uma pasta com seus próprios comandos que se entra dizendo uma
palavra («archivo», «ejemplos»…).

O exemplo real é `Dav/dic/Explorer/Examples/` (veja [`Examples`](../diagramas/Examples.md)).

---

## O que a pasta precisa ter

```
Explorer/Examples/
├── __init__.py          # vazio, mas obrigatório
├── Examples.py          # dicionário mestre: chaves internas → callables
├── ayuda.py             # explica os comandos do nível
├── TraduceToEs.py       # frases faladas em espanhol → os mesmos callables
├── TraduceToEn.py       # ... em inglês
├── TraduceToPt.py       # ... em português
├── manual.svg           # ícone da chave 'manual'
├── demos.svg            # ícone da chave 'demos'
└── _manual.py, _demos.py  # código dos comandos (opcional, o sublinhado = uso interno)
```

| Regra | Detalhe |
| --- | --- |
| **Pasta, módulo e variável têm o mesmo nome** | `Examples/Examples.py` define `examples` (a variável vai em minúscula, como `explorer` em `Explorer/Explorer.py`) |
| **Uma pasta = um nível** | Se um comando tem variantes, essas variantes vão em uma pasta filha |
| **`ayuda.py` em cada pasta** | Sua função `ayuda` vai como chave `'help'` do dicionário mestre |
| **Cabeçalho obrigatório** | Todos os arquivos novos, veja [convenções](convencoes.md) |

---

## Passo a passo

### 1. Crie o dicionário mestre

As chaves internas são **uma palavra em inglês**, sem repetir o contexto do pai.

```python
# Examples/Examples.py
from .ayuda import ayuda
from ._demos import startExample
from ._manual import openManual

examples = {
    'manual': openManual,
    'demos':  startExample,
    'help':   ayuda,
}
```

### 2. Vincule-o ao pai — **aninhado, nunca achatado**

```python
# Explorer/Explorer.py
from .Examples.Examples import examples

explorer.update({'examples': examples})   # CORRETO: 'examples' continua navegável
explorer.update(examples)                 # INCORRETO: achata as folhas no pai
```

Achatar quebra duas coisas **sem avisar**: as chaves repetidas entre folhas (`help`,
`create`…) se sobrescrevem e só sobrevive a última, e a pasta deixa de ser um nó
navegável, de modo que seu `TraduceTo*.py` nunca é carregado. Há um teste que
controla isso (`test_no_flattened_updates_in_dic`).

### 3. Escreva os três `TraduceTo*`

Cada um mapeia as **frases faladas daquele idioma** para os callables do dicionário
mestre, por objeto (`examples['manual']`), sem duplicar funções.

```python
# Examples/TraduceToEs.py
from .Examples import examples

TraduceToEs = {
    'manual':      examples['manual'],
    'referencia':  examples['manual'],
    'ejemplos':    examples['demos'],
    'ayuda':       examples['help'],
}
```

Notas:

- **O nome do arquivo e o da variável coincidem** (`TraduceToEs.py` define `TraduceToEs`).
- Na raiz de `dic/` o português se chama `TraduceToPT.py`; nas subpastas,
  `TraduceToPt.py`. O `DictionaryLoader` aceita as duas grafias.
- Os acentos são opcionais: o motor compara sem acentos. A gramática do Vosk sim
  precisa da forma do vocabulário do modelo.
- «subir», «enviar», «cancelar» e «dónde estoy» **não** são definidos aqui: vivem em
  `Dav/dic/NavCommands/` e valem em qualquer contexto.
- As vistas padrão (`StdView.StandardViews`) são anexadas ao final de vários
  `TraduceTo*` para poder mudar a vista de qualquer contexto; copie esse bloco
  de uma pasta irmã se quiser o mesmo.

### 4. Adicione as frases para **entrar** no `TraduceTo*` do pai

Sem isso a pasta existe, mas ninguém consegue chegar a ela.

```python
# Explorer/TraduceToEs.py
'ejemplos':        explorer['examples'],
'quiero aprender': explorer['examples'],
'aprender':        explorer['examples'],
```

Repita em `TraduceToEn.py` e `TraduceToPt.py`, e verifique que a frase não colida com
outra já usada nesse contexto (uma frase repetida em um mesmo dicionário se sobrescreve).

### 5. Coloque os ícones — **são buscados pelo nome da chave**

O painel pede o SVG com a chave do botão: a chave `manual` busca `manual.svg`.
O [`IconLocator`](../diagramas/IconLocator.md) indexa todos os SVG de `Dav/dic/` e
`InterfazDAV/Icons/` e compara sem maiúsculas nem `_` `-`.

| Situação | Resultado |
| --- | --- |
| Folha com `<chave>.svg` em qualquer pasta de `dic/` | Mostra esse ícone |
| Folha sem SVG | Botão com o fallback de duas letras (não é um erro) |
| **Dois SVG com o mesmo nome em pastas diferentes** | **Compartilham ícone**: vence o primeiro que for encontrado |
| Pasta cuja chave coincide com o nome de um SVG existente | A pasta **herda** esse ícone |

Por isso importa como as chaves são nomeadas. Em `Examples` a folha se chama `demos` e não
`examples`: como a pasta se chama `examples`, uma folha com o mesmo nome teria
dado ícone à pasta, e pediu-se que ela não tivesse. Antes de fixar uma chave, procure se
já existe um SVG com esse nome:

```powershell
Get-ChildItem Dav\dic -Recurse -Filter "<clave>.svg"
```

Se o ícone existe com outro nome, copie o SVG com o nome da chave (como
`manual.svg`, cópia de `File/open.svg`) ou adicione um alias em `IconLocator._ALIASES`.

### 6. Atualize a ajuda

Adicione o submenu à ajuda do pai (`Explorer/ayuda.py`) e descreva as folhas em
`ayuda.py` da pasta nova.

### 7. Verifique

```powershell
cd Dav\scr\ComponentesDAV\IntegracionGUI\GUIFreeCad
$env:PYTHONPATH = "<ruta>\Dav"
python -m unittest tests.test_real_dictionaries
```

Verifica que `base.py` importa limpo, que nenhum submenu está achatado e que as
pastas continuam navegáveis. **Um único import quebrado em uma folha profunda pode
deixar o `Browser` sem nenhum comando**, e o `DictionaryLoader` o captura e segue,
então sem este teste você não percebe. Para testar suas funções sem abrir a interface,
veja [testando.md](testando.md).

---

## Checklist

- [ ] Pasta com `__init__.py`, dicionário mestre, `ayuda.py` e os três `TraduceTo*`.
- [ ] Vinculada de forma **aninhada** no dicionário do pai.
- [ ] Frases de entrada adicionadas nos três `TraduceTo*` do pai.
- [ ] Cada folha tem seu SVG com o nome da chave (ou o ícone de fallback foi aceito).
- [ ] A chave da pasta **não** coincide com o nome de nenhum SVG de suas folhas.
- [ ] `test_real_dictionaries` passa.
- [ ] Cabeçalho nos arquivos novos e docstrings em inglês.
- [ ] Diagrama em [`diagramas/`](../diagramas/README.md) se a pasta traz classes ou fluxos novos.

---

Anterior: [Adicionar um comando](adicionar-comando.md) · Próximo: [Adicionar um diálogo de voz](adicionar-prompt.md)
