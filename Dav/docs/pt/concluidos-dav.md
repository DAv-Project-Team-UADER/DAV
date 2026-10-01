# Concluídos — DAV

Contraparte de [`pendientes-dav.md`](pendientes-dav.md): o que **já está
resolvido**, qual era o problema e como foi fechado. Serve para não rediagnosticar
a mesma coisa duas vezes e para ver o avanço real sem ler o histórico do git.

Ordem: o mais recente em cima.

---

## «Mover» a vista para um ponto (2026-09-20)

`Dav/dic/moveview.py`: pede um ponto e centraliza a câmera nele sem mudar para onde
ela olha nem o zoom (a posição da câmera é deslocada ao longo do seu eixo de visão,
à distância de foco; usa pivy). Como a cota, pede **X, Y** (desenho plano,
ou sketch em edição, com seu `Placement`) ou **X, Y, Z** (modelo 3D) conforme
`measure.dimensionMode()`. Está nos 384 `TraduceTo*` de todos os contextos, em
es/en/pt (`MOVE_VIEW_PHRASES`), adicionado com `setdefault`: onde «mover» já tinha outro
significado (Explorer/Edit, Draft/modify, Sketcher) ganha o local e valem as variantes
«mover vista», «mover cámara», «centrar en»...

---

## «Medir» / «cota»: 2D ou 3D conforme o documento (2026-09-20)

`CreateDimension` (`Dav/dic/measure.py`, importado por 36 `TraduceTo*`) pedia sempre
seis valores. Agora decide a cada execução e pede **quatro** (X, Y de cada ponto) ou
**seis** (X, Y, Z):

1. sketch em edição → 2D, no plano do sketch (usa seu `Placement`);
2. o documento tem algum sólido → 3D;
3. sem sólidos e bancada Draft/Sketcher/TechDraw ativa → 2D;
4. qualquer outro caso → 3D.

Continua sendo o mesmo nome, então os dicionários não mudam. Funciona porque
o coletor e o validador leem `inspect.signature(função)` a cada execução:
`CreateDimension` é um objeto invocável com `__signature__` calculado na hora.
Além disso, todos os `TraduceTo*` de `Workbench` (es/en/pt) recebem as frases de
`MEASURE_PHRASES` (em `measure.py`) com `setdefault`: não sobrescrevem frases próprias do
contexto (p. ex. «cota» dentro de `constraints` continua sendo a do Sketcher). A
gramática do Vosk inclui apenas o contexto atual e a raiz, não os ancestrais, por
isso precisa estar em cada dicionário e não basta a busca para cima.

---

## Perguntar sobre o que se trabalha, modificar por voz e corrigir (2026-09-20)

Acompanhamento de uma auditoria a olho nu. Tudo em `Dav/dic/`, exceto dois prompts novos.

### 1. Comandos que dependiam de «seleção ou objeto ativo»

`pad_by_length`, `revolve_by_angle`, `pocket_by_length` e `groove_by_angle` usavam
`_SelectedOrActive`: depois de criar uma figura, o «ativo» é a figura, não um perfil
(mesma origem da falha de «agujero pasante»). Agora perguntam o desenho com
`askSketch`. Um desenho solto (sem corpo) em um corte já não cria um corpo vazio
novo: pergunta-se em qual corpo trabalhar (`_OwningBody`).

### 2. Modificar no Draft sem mouse (`DraftWork/_modify.py`)

`modify`, `modification`, `array` e `facebinder` lançavam o comando nativo, que
espera cliques. Agora cada um pergunta o objeto com o menu de voz e os dados com
janelas numéricas, e usa a API do Draft: clonar, rebaixar/promover, para sketch, mover,
rotacionar, escalar, espelhar, offset, arredondamento, unir, editar/esticar um ponto, inclinação,
dividir, estender/aparar, polilinha para curva, vista 2D, todas as matrizes
(circular, ortogonal, polar, por trajetória, por pontos, com e sem links) e
união de faces. O nativo ficou como `interactive_*`.

### 3. Corpo novo ou existente

As figuras aditivas perguntam «¿cuerpo nuevo?» (`YesNoInputPrompt`: «no» é uma
resposta, não cancelar). Com «no» abre-se o menu de corpos válidos e a figura é
somada a um existente; se não tocar o sólido, o FreeCAD a rejeita e ela é descartada com um
aviso. As subtrativas e os furos abrem sempre o menu de corpos válidos
(`chooseBody`; `isBody` descarta os de operação quebrada).

### 4. Cobertura

- **Figuras sem parâmetros**: elipsoide, cunha, hélice, loft e tubo, aditivos e
  subtrativos. A cunha é posta em pé (sua altura nasce em Y) e centrada em x, y, z;
  hélice, loft e tubo escolhem seus desenhos de uma lista.
- **Sketcher por voz** (`Sketcher/_edit.py`, `_elements.py`, `constraints/_voice.py`):
  aparar, dividir, estender, arredondamento, chanfro, simetria, mover e construção, e as
  restrições **geométricas**. O sketch é escolhido de uma lista e o elemento **por
  número** (ordem de desenho, a partir de 1; a mensagem do pedido o lista com seu tipo).
  **As cotas e «medir» não são tocadas**: `constraints.py`, a cota linear do Draft e
  os blocos MEASURE (`measure.py`) ficaram como estavam.
- **Corrigir por voz** (`Correction/`, conectado em `dic/TraduceTo*.py`, diz-se de
  qualquer contexto): «deshacer», «rehacer», «borrar último», «borrar objeto» e
  «borrar rotos». Apagar pede confirmação e não apaga o que outros objetos usam.
- **Idiomas**: ver `pendientes-dav.md` §5. O TechDraw já estava carregado; as falhas
  reais eram typos e maiúsculas em imports.

Pendente: rotacionar, escalar e fazer offset de elementos do sketch, e as restrições
`lock`, `horver` e `coincidentunified`, continuam usando o comando nativo.

---

## PartDesign: furos e figuras com posição (2026-09-20)

«agujero pasante» falhava com `No base set, no sketch support either` e
«agujero ciego» com `draw the hole centres in a sketch first`. Além disso nenhuma
figura perguntava onde ia.

### A causa real

- `hole_by_size` criava o `Hole` com `doc.addObject` (fora do Body) e lhe
  atribuía o perfil **antes** de colocá-lo no Body: o FreeCAD o rejeita.
- Tomava como perfil «o objeto ativo», que depois de «cubo» era o próprio cubo:
  convertia as 12 arestas da caixa em um sketch.
- Usava `DepthType = 1` achando que era «profundidade explícita». No FreeCAD 1.x
  `0 = Dimension` e `1 = ThroughAll`: o valor ditado era ignorado. O mesmo
  acontecia em `hole_choose_sketch` ("agujero" com sketch escolhido).

### O que mudou (`Dav/dic/Workbench/PartDesign/`)

- **Furos sem sketch prévio**: `hole_by_size(diametro, x, y, z)` e
  `blind_hole_by_size(diametro, profundidad, x, y, z)` desenham sozinhos o sketch
  (círculo em x, y sobre o plano z) dentro do Body do último sólido. `z` é
  a altura da face a partir da qual se fura; corta para -Z e, se assim não retira
  material, é invertido. Se tampouco retira material, é descartado e avisa-se.
- **Figuras centradas em (x, y, z)**: caixa, cilindro, esfera, cone, toro e
  prisma, aditivos e subtrativos (cone, toro e prisma subtrativos eram
  comandos nativos sem parâmetros). `_placement.py` prende a figura ao plano XY
  do Body com `AttachmentOffset`, deslocada meia medida onde a primitiva nasce
  com um canto ou a base na origem.
- **Com qual corpo se trabalha**: furos e cortes usam `chooseBody`: só são
  oferecidos corpos com um sólido válido (`isBody` em `_prompts.py` descarta os
  que têm a última operação quebrada). Com um só, usa-se direto; com vários
  pergunta-se por voz («avanzar» / «okey»). Antes cortava-se sempre sobre o
  último Body: se seu remate era um `Hole` quebrado, o corte falhava com
  `Cannot subtract primitive feature without base feature`.
- Um corte que não toca o sólido (ou não retira material) já não deixa uma feature
  inútil no modelo: é eliminado e avisa-se.

Pendente: elipsoide, cunha, hélice, loft e tubo continuam usando o comando nativo.

---

## Gramática do Vosk restrita ao contexto (2026-08-10)

Era o **§1** dos pendentes: o `KaldiRecognizer` era criado sem `SetGrammar`, então o Vosk
competia contra as **100.001 palavras** do modelo em cada frase em vez das ~12 do
contexto ativo. Daí «croquis» → «crockett» e o «traffic» que ninguém disse.

Integrado do PR #176 de SoPerez1, mais as correções do #178.
Funcionamento completo em
[`encurtador-gramatica-vosk.md`](encurtador-gramatica-vosk.md).

### A causa que não estava à vista

A gramática por si só não bastava: ela **derrubava o FreeCAD**. O Vosk não aceita que
se troque a gramática de um recognizer que já processou áudio, e falha com uma
exceção de C++ que nenhum `except` do Python captura.

```
SetGrm():recognizer.cc:235
"Can't add speaker model to already running recognizer"
```

Como o loop chama `SetGrammar` depois de processar áudio, **cada mudança de nível
era uma tentativa de crash**. Verificado contra o modelo `pt` em processos
separados:

| cenário | resultado |
| --- | --- |
| `SetGrammar` antes de áudio | ok |
| `SetGrammar` depois de áudio | ERRO → crash |
| `Reset()` + `SetGrammar` | ok |

`speech/voice_commands.py` já tinha `USE_GRAMMAR = False` com a nota *"can block
all recognition on some models"*: alguém já tinha esbarrado nisso antes. Essa
variável **ninguém a lia**, então não desligava nada, e seu diagnóstico estava
incorreto —não depende do modelo, acontece sempre—. Foi eliminada.

### O microfone que "não pegava"

Segundo sintoma, mesma raiz. O log mostrou os dois modos disputando o
recognizer:

```
14:28:27  aplicando gramatica: 82 frases    ← preferências
14:28:27  aplicando gramatica: 54 frases    ← CAD
14:28:27  aplicando gramatica: 82 frases
```

Cada aplicação faz `Reset()`, que descarta o áudio parcialmente reconhecido, então
nenhuma frase chegava a ser concluída. O loop agora drena a fila e fica apenas
com a última gramática.

### O que foi feito

| Mudança | Efeito |
| --- | --- |
| `Browser.GetSpokenPhrases()` | Gramática do nível ativo, derivada do dicionário |
| `Reset()` antes de `SetGrammar` | Fecha o crash |
| Só a última gramática da fila | Fecha o microfone morto |
| `core/dav_log.py` | Log em arquivo: sem isso nada do anterior era diagnosticável |
| `enviar`/`cancelar` para `NavCommands/` | Estavam em três lugares do código, já dessincronizados |

### Verificação

Sessão real por voz dentro do FreeCAD: a gramática acompanha a navegação (54 na
raiz → 93 em Arquivo → 199 em Sketcher), sem crashes nem gramáticas se atropelando.

### O que continua em aberto

- **A gramática restringe o vocabulário, não a sintaxe.** O Vosk pode combinar
  palavras válidas em frases sem sentido («extender oblongo»). Não executam nada,
  mas com 199 frases ativas há mais superfície para o ruído.
- `settings.json` às vezes fica em `pt` entre sessões e ainda não se sabe o que
  o escreve. O log já registra qual frase dispara cada mudança de idioma.

---

## Painel DAV acoplado ao FreeCAD (2026-08-09)

Migração completa da GUI: de processo externo para `QDockWidget` dentro do
FreeCAD. Plano e etapas em [`plano-unificacao-guis.md`](plano-unificacao-guis.md).

### O problema de fundo

A `InterfazDAV` **não abria**. Rodava como processo à parte com seu próprio
PySide6 6.11.1 e herdava do FreeCAD as variáveis que apontam para o seu Qt 6.8.3:

```
ImportError: DLL load failed while importing QtWidgets
```

Tentou-se remendar três vezes (limpar `PYTHONHOME`/`PYTHONPATH`/`QT_PLUGIN_PATH`,
filtrar o `PATH`, mudar o `cwd`) e nenhuma bastou: cada remendo tapava uma via
de contaminação conhecida e sobravam as que dependem do estado em memória do
processo pai.

**Resolveu-se por construção, não por remendo:** um widget dentro do FreeCAD usa
o Qt do FreeCAD, então não há dois Qt que colidam.

### O que foi feito

| Etapa | Resultado |
| --- | --- |
| 1 | `MainWindow.py` (1011 linhas) dividido em `DavPanel` + `ContextView` + `IconLocator`, sem dependências do FreeCAD nem de arquivos |
| 2 | Painel montado como dock, alimentado pelo `Browser` em processo; ponte por arquivos eliminada nas duas direções |
| 3 | Árvore de objetos a partir de `App.ActiveDocument` + `DocumentObserver`, sem macro nem polling |
| 4 | Janela externa retirada por completo, incluindo `DiccionarioPrueba/` |
| 5 | Launcher de desktop apagado: fica **uma única GUI**, fecha §2.b |

### Por que eram "duas GUIs" e por que agora há uma

Não eram equivalentes: `InterfazDAV/MainWindow.py` (1011 linhas) era a de
trabalho, e `IntegracionGUI/ui/main_window.py` (138) um *launcher* cujo botão de
voz fazia `Popen` da outra. Divergiram por desenvolvimento paralelo, não por design.

A etapa 5 foi resolvida ao contrário do planejado: recomendava-se manter o
launcher como configurador de desktop, mas seu botão principal já estava quebrado
(lançava a janela apagada na etapa 4) e **não contribuía com o download de
modelos** —esse fluxo vive em `preferences_dialog.py`, acessível a partir da barra
DAV e do botão ⚙ do painel—. Só *avisava* se faltasse um modelo, aviso que
o `voice_bootstrap` já dá.

### A ponte por arquivos, eliminada

| Antes | Agora |
| --- | --- |
| `export_context_state()` → JSON, lido a cada 500 ms | `PublishContext()` direto |
| `command_queue.txt` + `QTimer` | `SendCommand()` → `procesar_frase_final` |
| `voice_history.log` por polling | `_publish_line()` no momento |
| `tree_data.json` + macro + 2 timers | `App.ActiveDocument` + observador |

Sobrevivem `voice_history.log` (registro persistente) e `voice_status.json`
(`export_voice_status` é o ponto único do estado do motor, e dali é
publicado ao painel).

### Apagado, ~4900 linhas

`main.py` · `run_interfaz.bat` · `VoiceWorker.py` · `MainWindow.py` ·
`trigger_capture.py` · `capture_tree.FCMacro` · `HelpWindow.py` ·
`DiccionarioPrueba/` · `DavPanelController` + `FileBridgeSource` · os 7 métodos
do lançador externo em `dav_commands.py` · `_schedule_interfaz_dav_launch`

### Um crash duro que apareceu e foi fechado

Montar o painel derrubava o FreeCAD inteiro (`0xC0000005`), sem rastro no console do
Python. O log do FreeCAD mostrou: tocava-se um widget Qt **a partir da thread do
microfone**, o que é access violation, não uma exceção que um `except` possa
capturar.

Corrigido movendo as publicações para dentro de `run_on_main_thread`, e com
`_on_gui_thread()` que as bloqueia se mesmo assim chegassem de outra thread.

---

## Defeitos da GUI corrigidos (2026-08-09)

| Sintoma | Causa real |
| --- | --- |
| Botões com duas letras em vez de ícone | A chave e o arquivo diferiam em maiúsculas/separadores (`lineattributes` vs `LineAttributes.svg`); e `pieza`/`circulo`/`stdview` têm ícone com outro nome → normalização + tabela de aliases |
| Ícones de tamanhos díspares | O `QSvgWidget` embutido desenhava conforme o `viewBox` de cada SVG → `setIcon`/`setIconSize` |
| "Micrófono inactivo" com a voz ativa | `PublishStatus` existia mas ninguém o chamava |
| A janela ficava sempre por cima, sem minimizar | Um `QDockWidget` flutuante é `Qt.Tool` por padrão → flags de janela real, reaplicadas em `topLevelChanged` |
| O painel esticava ao entrar em contextos grandes | Os botões iam em uma única linha; `Part` tem 47 entradas (~3000 px) → grade com scroll horizontal e altura fixa |
| O botão "voltar" não fazia nada | `NavCommands/` só tinha `TraduceToEs.py`; em outros idiomas carregavam-se **zero** comandos de navegação |
| A ajuda saía no Report View, não no painel | Os comandos escrevem com `print()` (988 chamadas em 123 arquivos) → captura-se o stdout durante a execução |
| `Cannot find icon` na barra | `Std_DlgCustomize` é um identificador de comando, não um nome de ícone |
| `part` e `circle` apareciam na raiz | Os `TraduceTo*` adicionavam dois destinos que `base.py` não define; `circulo` além disso é uma folha que desenha, não uma categoria |

---

## Análise do modelo de voz (2026-08-09)

**Achado contrafactual:** um modelo Vosk maior **não** melhora o
reconhecimento de comandos. Detalhe completo em `pendientes-dav.md` §10.

- O modelo pequeno já carrega 100.001 palavras e o DAV usa 745 (0,75 %). A mediana
  por contexto é de 12 frases: um fator de ~8.000×.
- 66 dessas 745 (8,9 %) estão **fora do vocabulário** e são impossíveis de
  emitir: `chaflán`, `extruir`, `biselar`, `isométrica`, `polilínea`. É o
  núcleo do vocabulário CAD, e aumentar o modelo não as adiciona.
- O overkill está no modelo de linguagem (`Gr.fst`), não no acústico. Uma
  gramática restrita substitui o primeiro e conserva o segundo.

> **Falta o benchmark** de taxa de acerto antes de apresentá-lo como resultado
> experimental. O desenho do experimento está em §10.f.

---

## Limpeza de vocabulário (2026-08-08)

**89 → 66 palavras fora de vocabulário (11,5 % → 8,9 %).** Ao cruzar a árvore
com o modelo apareceram 89 palavras que o reconhecedor não pode emitir, mas
nem todas eram o mesmo problema: só uma categoria era limitação do modelo, o
resto era dívida do dicionário (chaves internas que ficaram como frase falada,
anglicismos sem sinônimo, typos). Detalhe em `pendientes-dav.md` §11.

---

## Correções de dicionários e navegação (2026-06 / 2026-08)

- **Subcontextos aninhados, nunca achatados** — `explorer.update({'file': file})`
  e não `explorer.update(file)`. Achatar colidia chaves repetidas entre folhas
  e deixava a pasta fora da árvore navegável. Convenção em
  `pendientes-dav.md` §4.
- **`NavCommands/`** — as palavras de navegação (subir, contexto) vivem no
  dicionário como qualquer outro comando, não hardcoded em `browser.py`.
- **Imports quebrados** que derrubavam o carregamento de Base e Sketcher.
- **Normalização de acentos** unificada em uma única função.
- **`IsSameTarget`** como alias público de `_SameTarget`: quem percorre `Context`
  de fora precisa deduplicar igual ao `Browser`.

## Destaque da seleção na árvore do painel (2026-08-18)

**Problema.** Ao dizer `"seleccion"` → `"siguiente"`, o objeto era selecionado
no FreeCAD mas a árvore do painel DAV não o destacava. O mesmo com os objetos
que `CreateObjects` cria: apareciam na árvore, mas não se via qual estava
ativo. Era preciso olhar a árvore nativa do FreeCAD para saber.

**Causa real.** Não faltava nada na árvore nem em `ObjectSelection`: os dois
funcionavam bem separadamente. `ObjectSelection.MonoSelection()` chama
`Gui.Selection.addSelection(Obj)` e aí termina seu trabalho — **ninguém avisava
o painel**. O `_TreeDocumentObserver` que já existia escuta mudanças do
*documento* (criar/apagar/recomputar), e selecionar não muda o documento,
então nunca era disparado. Faltava o observador do outro canal.

**Solução.**

- `DavPanel.HighlightSelection(Names)` — percorre o mapa `_treeItems` (que
  `SetTree` agora guarda) e marca os selecionados, com `scrollToItem` para o
  primeiro. O widget continua sem importar o FreeCAD: recebe uma lista de nomes.
- `BrowserPanelSource.PublishSelection()` — lê `Gui.Selection.getSelection()`
  e o passa ao painel.
- `_TreeSelectionObserver` — registrado com `Gui.Selection.addObserver()`,
  mesmo padrão do `_TreeDocumentObserver`: todos os slots caem em um
  `_Refresh` com `try/except`, porque uma exceção aqui se propagaria ao
  tratamento de seleção do FreeCAD.

**Detalhe não óbvio.** `HighlightSelection` envolve o laço em
`blockSignals(True/False)`: `setSelected()` emite `itemSelectionChanged`, e
quando o sentido inverso for implementado (clique no painel → selecionar no
FreeCAD) isso se realimentaria em laço infinito. Bloquear agora evita o bug
antes que ele exista.

Continuam pendentes o sentido painel → FreeCAD e navegar na árvore por voz
("seleccionar el tercero"). Ver `plano_arvore_de_objetos_navegavel.md`.

---

## Como adicionar a este documento

Ao fechar um pendente: movê-lo para cá com **qual era o problema** e **qual
acabou sendo a causa real**, não apenas o que foi mudado. Várias vezes a causa aparente e a
real foram diferentes (os ícones não faltavam, o nome não coincidia; o botão
de ajuda sim funcionava, sua saída ia para outro lugar), e esse é justamente o dado que
evita repetir o diagnóstico.
