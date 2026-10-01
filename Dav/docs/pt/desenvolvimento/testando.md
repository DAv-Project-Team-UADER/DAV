# Como testar e validar

Como verificar que uma mudança funciona **antes** de enviá-la para revisão. Camadas
diferentes conforme o que você alterou.

---

## 1. Teste puramente técnico (rápido, sem FreeCAD)

Para código Python próprio (prompts, painéis, módulos), ao menos:

### Sintaxe

```bash
# Windows (PowerShell)
python -c "import ast; ast.parse(open(r'<archivo>', encoding='utf-8').read()); print('OK')"
```

### Import / smoke test com o venv de desenvolvimento

O venv de desenvolvimento (`IntegracionGUI/GUIFreeCad/.venv`) tem PySide6. É
possível importar um módulo que não exija FreeCAD em tempo de import (se
importa `FreeCAD` no topo, use import adiado dentro das funções — padrão
que os prompts usam).

### Lógica de prompts (sem abrir o FreeCAD)

Os prompts herdam `BaseInputPrompt` e sua lógica pode ser testada chamando
`ProcessFinalText("...")` diretamente com um `QApplication` offscreen:

```python
import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"
from InputPrompts.PlaneSelectionInputPrompt import PlaneSelectionInputPrompt
from PySide6.QtWidgets import QApplication
app = QApplication.instance() or QApplication([])

p = PlaneSelectionInputPrompt()
print(p.ProcessFinalText("abajo").Success)   # navega
print(p.ProcessFinalText("okey").Value)       # confirma → valor do plano
```

Requer que `GUIFreeCad` esteja no `sys.path` (ou configurar o caminho).

### Ações do FreeCAD sem abrir a interface (`freecadcmd`)

Para verificar que uma **ação** (criar um esboço, um sólido, uma folha do TechDraw)
funciona de verdade, não basta fazer o parse do arquivo: é preciso rodá-la no FreeCAD.
`freecadcmd` é o FreeCAD **sem janela**, com seu Python e seus módulos (`Part`, `Sketcher`,
`Draft`, `TechDraw`), e pode ser lançado pelo terminal. Serve tanto para as ações
dos dicionários quanto para os prompts que usam Qt (com o modo `offscreen`).

| Sistema | Executável |
| --- | --- |
| Windows | `C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe` |
| Linux | `freecadcmd` (ou o da pasta de instalação) |

**Modelo de um script de teste** (guarde-o fora do repositório, por exemplo na pasta
temporária da sessão):

```python
import os, sys, traceback
os.environ["QT_QPA_PLATFORM"] = "offscreen"          # Qt sem tela

DAV = r"C:\ruta\al\repo\Dav"
sys.path[:0] = [
    DAV + r"\dic",                                   # para importar Explorer.Examples...
    DAV + r"\scr\ComponentesDAV\IntegracionGUI\GUIFreeCad",   # para importar InputPrompts
]

out = open("resultado.txt", "w")                     # veja a nota sobre a saída
def log(*args):
    out.write(" ".join(str(a) for a in args) + "\n")
    out.flush()

try:
    import FreeCAD as App
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    App.newDocument("Prueba")
    from Explorer.Examples import _partdesign as ejemplo   # o módulo a testar
    for paso in ejemplo.steps():
        paso.Action()                                # roda cada ação em ordem

    doc = App.ActiveDocument
    invalidos = [o.Name for o in doc.Objects if not o.isValid()]
    log("objetos:", len(doc.Objects), "invalidos:", invalidos)
except Exception:
    log(traceback.format_exc())
```

```powershell
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" prueba.py
Get-Content resultado.txt
```

O que observar e levar em conta:

- **Verifique `isValid()` de cada objeto** depois de recalcular. Uma operação que falha
  não lança exceção: deixa o objeto em estado inválido (por exemplo um furo que não
  pôde ser criado).
- **Escreva os resultados em um arquivo.** A saída padrão do `freecadcmd` depende de
  como ele é lançado e muitas vezes não volta ao terminal; um arquivo é sempre confiável.
- **Sem interface não há vista 3D.** `Gui.ActiveDocument`, `ViewFit` e os painéis não existem;
  o código das ações deve tolerar isso (veja `fitView()` em `Explorer/Examples/_common.py`).
  O que depender da vista é testado dentro do FreeCAD com a interface.
- **O aviso `2 entries found for module 'dav'`** significa que há duas cópias do módulo
  instaladas e o FreeCAD usa apenas uma. Ao testar dentro do FreeCAD, verifique que seja a cópia
  que você está editando.
- **Teste os três idiomas** de um prompt mudando seu idioma antes de ditar:
  `prompt._Language = "en"`.
- **Simule a voz** chamando `prompt.ProcessFinalText("frase")`: devolve o
  `PromptResult`, assim você pode verificar `Success`, `Value` e `Cancelled` sem microfone.
- **Para um comando com parâmetros**, `PromptedCommandExecutor.ExecuteEntry(entrada, ["cinco okey"])`
  coleta com frases simuladas, uma por parâmetro.

---

## 2. Teste de dicionários / navegação

- **Carregar o dict mestre** não deve quebrar: se uma pasta tem um dict quebrado,
  o `DictionaryLoader` o omite e segue (não derruba o motor).
- Verifique que as **frases novas aparecem** como opções do contexto: no
  painel, após navegar até o contexto, a ajuda/descrever contexto listará os
  comandos disponíveis (implícito em `Browser.DescribeContext`).
- Teste cada frase nos três idiomas se você adicionou traduções.
- **Rode a verificação dos exemplos guiados** se mexer nos exemplos ou nas palavras da
  árvore que eles usam. Ela reproduz, em es, en e pt, cada frase de cada quadro por um `Browser` real,
  executa as ações e avisa qual frase não é resolvida ou a qual comando chega. Precisa do
  FreeCAD, então é lançada com `freecadcmd`:

  ```powershell
  $tests = "Dav\scr\ComponentesDAV\IntegracionGUI\GUIFreeCad\tests"
  & "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" "$tests\verify_examples_paths.py"
  Get-Content "$tests\verify_examples_paths.txt"
  ```

  Que uma frase «seja resolvida» não basta: veja também a qual comando chega cada quadro (`->`
  no relatório). Assim se descobriu, por exemplo, que «cortar» dito a partir de *Sumar* chegava a
  «cotar» por correspondência aproximada, e que a partir de *Círculo* «crear» salta para Workbench.
- **Rode o teste da hierarquia real** depois de mexer em qualquer dicionário. Precisa da
  pasta `Dav` no `PYTHONPATH` (os `TraduceTo*` importam `dic.StdView...`); sem
  isso falham dois testes por `No module named 'dic'`, mesmo que a árvore esteja bem:

  ```powershell
  cd Dav\scr\ComponentesDAV\IntegracionGUI\GUIFreeCad
  $env:PYTHONPATH = "<ruta al repo>\Dav"
  python -m unittest tests.test_real_dictionaries
  ```

  Verifica que `base.py` importa limpo, que nenhum submenu está achatado e que as
  traduções não ficaram vazias. Alta prioridade: um único import quebrado em uma folha
  profunda deixa o `Browser` sem comandos e o `DictionaryLoader` não avisa.

---

## 3. Teste integrado no FreeCAD (o que vale)

Rode o motor de voz dentro do FreeCAD (veja [setup](setup.md)) e teste o
fluxo real por voz. As guias existentes detalham o que esperar:

| Guia | Cobre |
|---|---|
| [guia-testes-partdesign-voz.md](../guia-testes-partdesign-voz.md) | PartDesign por voz com medidas ditadas (sólidos, extrusão, cortes, acabamentos) |
| [guia-testes-3d-voz.md](../guia-testes-3d-voz.md) | Fluxo completo a partir de desenho 2D e Assembly |
| [guia-teste-numeros-alunos.md](../guia-teste-numeros-alunos.md) | Ditado de números (como dizer medidas) |
| [manual-selecao-voz.md](../manual-selecao-voz.md) | Seleção de objetos por voz |
| [manual-explorer-voz.md](../manual-explorer-voz.md) | Explorer por voz (arquivos) |
| [relatorio_testes_draftwork.md](../relatorio_testes_draftwork.md) | Relatório de testes do workbench Draft |

### Dicas de teste

- **`donde estoy`** (onde estou) para se localizar; **`subir`** (subir) para subir de nível.
- Confirmar pop-ups: `enter` · `enviar` · `aceptar` · `confirmar` · `ok`.
  Abortar: `cancelar`.
- Se um comando "não é ouvido", pense na **gramática restrita**: alguns
  prompts (numéricos, seletor de plano) limitam de propósito quais palavras o Vosk aceita
  (veja [encurtador-gramatica-vosk.md](../encurtador-gramatica-vosk.md)).

---

## 4. Rodar os testes do projeto

Há infraestrutura de testes/validação em `Dav/scr/validation/`:

- `test_validator.py` — testes do `Validator`.
- `test_integration.py` — testes de integração (inclui
  `PromptedCommandExecutor`).
- `run_tests.py` — rodar os testes da pasta.
- `prueba_validator.py` — helper de teste/validação.

```bash
python Dav/scr/validation/run_tests.py
```

> O `Validator` é integrado à execução de comandos via
> `PromptedCommandExecutor` (validação prévia de parâmetros). Se o seu comando
> recebe parâmetros, adicione cobertura nestes testes quando couber.

---

## Checklist rápido antes de enviar o PR

- [ ] Sintaxe OK (AST parse) nos arquivos modificados/novos.
- [ ] Subcontextos não são achatados (`.update(sub_dict)`).
- [ ] Arquivos novos com cabeçalho obrigatório.
- [ ] Docstrings em inglês para classes/métodos públicos.
- [ ] Frases testadas nos idiomas afetados.
- [ ] Fluxo real por voz testado no FreeCAD (se possível).
- [ ] Guia/doc atualizada se você mudou uma convenção ou um comportamento.
