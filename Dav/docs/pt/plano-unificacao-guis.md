# Plano: unificar as duas GUIs

**Estado:** etapas 1 a 4 implementadas; falta a 5.
**Data:** 2026-08-09
**Resultado:** resumido em [`concluidos-dav.md`](concluidos-dav.md).
**Motivo imediato:** a InterfazDAV não abre a partir do FreeCAD por um conflito de
DLLs do Qt que **só existe porque roda como processo externo**. Remendá-lo é
possível; eliminá-lo por construção é melhor.

---

## 1. O mapa real (verificado, não assumido)

A suposição de "há duas GUIs completas e é preciso escolher uma" **está incorreta**.
O que existe é:

| | `InterfazDAV/` | `IntegracionGUI/GUIFreeCad/` |
| --- | --- | --- |
| Janela | `MainWindow.py` — **1011 linhas** | `ui/main_window.py` — **138 linhas** |
| O que é | a GUI de trabalho real | um **launcher de desktop** |
| Onde roda | processo externo (venv Python 3.14) | processo externo (venv) |
| Qt | PySide6 próprio → **conflita com o do FreeCAD** | PySide6 próprio |
| Tem | histórico, minimizar, árvore, botões de contexto | preferências, download de modelos |

O dado que muda tudo: **`ui/main_window.py` não usa o `Browser`**. Seu botão
"Iniciar Voz" faz `subprocess.Popen` de… `InterfazDAV/main.py`
(`ui/main_window.py:121-138`). É um lançador, não uma alternativa.

### Onde o Browser realmente vive

```
FreeCAD (processo)
└── dav_commands.py / freecad_wb.py
    └── integration/voice_bootstrap.py  ← start_voice_engine()
        └── Browser(...)                ← o motor real, DENTRO do FreeCAD
            └── BrowserVoiceAdapter
                └── escreve context_state.json ─┐
                                                │  ponte por arquivos
InterfazDAV (processo externo)                  │
└── MainWindow._PollFreeCADState() ←────────────┘  polling 500 ms
```

O `Browser` **já roda dentro do FreeCAD**. Nenhuma das duas janelas o
tem: uma o consome por arquivos, a outra nem sequer o toca.

> **Correção à recomendação anterior:** dizer "migrar histórico e minimizar
> para a IntegracionGUI" estava mal colocado — a `IntegracionGUI` não é a GUI boa
> para a qual se mudar, é um launcher de 138 linhas. A migração real é da
> `InterfazDAV` **para dentro do FreeCAD**, não para a outra pasta.

---

## 2. Por que o bug do Qt é estrutural

A `InterfazDAV` roda em um venv com **PySide6 6.11.1**. O FreeCAD 1.1 traz seu próprio
Qt6 em `bin/` (`Qt6Core.dll`, `Qt6Widgets.dll`, …). Ao ser iniciada como subprocesso,
ela herda do pai:

- `PYTHONHOME` / `PYTHONPATH` → o venv carrega a stdlib do FreeCAD
  (`SRE module mismatch`)
- `QT_PLUGIN_PATH` e o `bin` do FreeCAD no `PATH` → o PySide6 resolve as Qt6
  do FreeCAD em vez das suas (`DLL load failed while importing QtWidgets`)

É possível sanear o ambiente (foi tentado: remover variáveis, filtrar o `PATH`,
antepor a pasta do PySide6, mudar o `cwd`). Mas cada remendo cobre uma
via de contaminação conhecida, e sobram as que dependem do estado em memória
do processo pai. **Enquanto houver dois Qt distintos em jogo, o problema pode
voltar** com outra versão do FreeCAD, do PySide6 ou em outra máquina.

Um widget dentro do FreeCAD usa **o Qt do FreeCAD**. O conflito não é
remendado: deixa de existir.

---

## 3. Objetivo

Converter a `InterfazDAV` em um **painel acoplado dentro do FreeCAD**
(`QDockWidget`), eliminando o processo externo e a ponte por arquivos.

```
ANTES                                DEPOIS

FreeCAD ──► Browser                  FreeCAD ──► Browser
   │           │                        │           │
   │      context_state.json            │      sinal Qt direto
   │      command_queue.txt             │           │
   │      voice_history.log             │           ▼
   ▼           │                        └──► DavPanel (QDockWidget)
InterfazDAV ◄──┘                                 histórico, árvore,
(processo externo, Qt próprio)                   botões, minimizar
```

### O que é eliminado

- O conflito de Qt (por construção)
- `command_queue.txt`, `context_state.json`, `voice_status.json`,
  `voice_history.log` como canal — e com eles os pendentes §2.d:
  `pop_command_queue()` perdendo comandos, a latência de 500 ms, o estado
  versionado por erro
- Os dois `QTimer` de polling
- `_launch_interfaz_dav()`, `_clean_child_env()`, `_probe_pyside6()`,
  `_check_interfaz_started()` em `dav_commands.py`
- `run_interfaz.bat`, `trigger_capture.py`, `capture_tree.FCMacro`

### O que se ganha

- A GUI acessa o `Browser`, o documento e a seleção **no mesmo
  processo**: sem serializar, sem latência, sem perda de comandos
- A árvore de objetos sai direto de `App.ActiveDocument`, sem macro nem
  `tree_data.json`
- Tema e idioma herdados do FreeCAD

---

## 4. Migração por etapas

Cada etapa deixa o repositório funcionando. Não há um "big bang".

### Etapa 0 — Remendo provisório (opcional)

Deixar as correções de `dav_commands.py` (venv por caminho, saneamento de ambiente,
diagnóstico de inicialização) para que a GUI abra **enquanto** durar a migração. São
apagadas na etapa 4.

> Decisão pendente: se a etapa 1 for feita logo, este remendo pode ser pulado.

### Etapa 1 — Extrair o painel

Separar `MainWindow.py` (1011 linhas) em:

- **`DavPanel.py`** — `QDockWidget` com todos os widgets: histórico, árvore,
  botões de contexto, overlay. **Sem** `QTimer` de polling, sem leitura de
  arquivos, sem `subprocess`.
- **`DavPanelController.py`** — a cola: recebe o contexto do `Browser` e
  atualiza o painel.

`MainWindow.py` fica como um wrapper fino para poder continuar rodando a GUI
solta durante a transição.

Regra: o `DavPanel` **não importa o FreeCAD**. Recebe dados, emite sinais. Assim
pode ser testado sem FreeCAD, igual ao `Browser`.

### Etapa 2 — Montar o painel no FreeCAD

Em `freecad_ui_setup.py` (que já sabe fazer `Gui.getMainWindow()`):

```python
panel = DavPanel()
Gui.getMainWindow().addDockWidget(Qt.RightDockWidgetArea, panel)
```

Conectar ao `Browser` por sinais, substituindo a ponte:

| Hoje (arquivos, 500 ms) | Depois (sinais, imediato) |
| --- | --- |
| `export_context_state()` → JSON | `browser.ContextChanged` → `panel.RenderContext()` |
| `command_queue.txt` → `pop_command_queue()` | `panel.CommandRequested` → `browser.ProcessPhrase()` |
| `append_voice_history()` → `.log` | `adapter.PhraseRecognized` → `panel.AddToHistory()` |

O callback `on_descend` que já existe no `Browser` (hoje sem uso) é o gancho
natural para `ContextChanged`.

Nesta etapa convivem as duas rotas: o painel acoplado e a janela externa. O
comportamento é comparado.

> **Encerrada (2026-08-09).** A ponte por arquivos já não existe em nenhuma
> direção:
>
> | Antes | Agora |
> | --- | --- |
> | `export_context_state()` → JSON | `PublishContext()` direto ao painel |
> | `command_queue.txt` + `QTimer` 500 ms | `SendCommand()` → `procesar_frase_final` |
> | `voice_history.log` lido por polling | `_publish_line()` no momento |
> | `tree_data.json` + macro | `App.ActiveDocument` + observador (etapa 3) |
>
> Foram apagados, já sem consumidor: `export_context_state`, `read_context_state`,
> `write_command_queue`, `pop_command_queue`, `read_voice_history_from`, o
> `QTimer` que consultava a fila e o corpo de `_export_state`.
>
> `voice_history.log` e `voice_status.json` **continuam sendo escritos**: o primeiro
> como registro persistente, o segundo porque `export_voice_status` é o ponto
> único por onde passa o estado do motor e dali é publicado ao painel.
>
> `on_descend` continua sem uso: a atualização vai por `PublishContext()` ao final
> de cada frase, o que cobre também os comandos que não mudam de nível.

### Etapa 3 — Árvore de objetos nativa

**Por que vai separada da 2:** são *duas pontes distintas*, com arquivos
distintos e código distinto. A etapa 2 substitui o canal de voz
(`context_state.json`, `command_queue.txt`, `voice_history.log`); a árvore viaja
por seu próprio caminho:

```
InterfazDAV._AutoCapture()  ──► trigger_capture.py
                                    │
                                    ▼
                            capture_tree.FCMacro  (dentro do FreeCAD)
                                    │
                                    ▼
                            tree_data.json  ──► _RefreshTreeData() (QTimer)
```

Terminada a etapa 2, a árvore **continuaria** lendo `tree_data.json` por macro:
não se resolve sozinha. E ao contrário, se tudo for reunido em uma etapa e a árvore
se complicar, ela bloqueia uma correção de voz que já estava funcionando.

Trabalho: `_PopulateTree()` passa a ler `App.ActiveDocument.Objects` direto
(mesmo contrato: `name`, `label`, `type`, `visible`, `parent`). São apagados
`trigger_capture.py`, `capture_tree.FCMacro`, `_AutoCapture()`,
`_RefreshTreeData()`, `_LastTreeMtime` e o `QTimer` de atualização — o documento
avisa por seus próprios sinais em vez de ser consultado a cada 5 s.

> **Feito (2026-08-09) para o painel acoplado.** `BrowserPanelSource.PublishTree()`
> lê `App.ActiveDocument` em processo, e `_TreeDocumentObserver` (registrado com
> `App.addDocumentObserver`) o dispara diante de criação, exclusão, mudança,
> recompute e mudança de documento ativo. A árvore agora acompanha também o que é
> desenhado com o mouse, não só o que entra por voz.
>
> **Falta** apagar o caminho antigo: `trigger_capture.py` e `capture_tree.FCMacro`
> continuam no repositório porque seu único consumidor é `MainWindow.py`, que é
> retirado na etapa 4. Apagá-los agora quebraria a janela externa enquanto ainda
> é a que está em uso.

### Etapa 4 — Apagar o andaime — FEITO (2026-08-09)

Antes de apagar foi fechada a condição de entrada: os botões de **ajuda** e
**preferências** do painel emitiam sinais que ninguém conectava. Agora
o `BrowserPanelSource` os atende — preferências abre o diálogo do GUIFreeCad, e
a ajuda despeja `Browser.DescribeContext()` no histórico (os comandos válidos
*aqui e agora*, mais útil que o texto fixo da janela externa).

Apagado:

- `InterfazDAV/`: `main.py`, `run_interfaz.bat`, `VoiceWorker.py`,
  `MainWindow.py` (1011 linhas), `trigger_capture.py`, `capture_tree.FCMacro`,
  `HelpWindow.py` e **`DiccionarioPrueba/`** — fecha o §2 por completo
- `DavPanelController.py` + `FileBridgeSource`: eram a ponte por arquivos que
  esta etapa retira; sem janela externa ficaram sem consumidor
- `dav_commands.py`: `_launch_interfaz_dav`, `_check_interfaz_started`,
  `_clean_child_env`, `_probe_pyside6`, `_venv_python`, `_bring_interfaz_to_front`,
  `close_interfaz_dav` (~180 linhas). Com elas vai embora o conflito de Qt: já não
  se lança nenhum processo externo, então não há dois Qt que colidam.
- `freecad_wb.py`: `_schedule_interfaz_dav_launch()` e sua chamada na inicialização
- `IconLocator`: a raiz `DiccionarioPrueba` (ficam 467 ícones indexados)

`Iniciar voz DAV` agora abre o painel acoplado em vez de lançar o processo
externo. `iniciar_dav.bat` não muda: nunca passou por `run_interfaz.bat`.

As entradas do `.gitignore` do circuito de captura são mantidas de propósito,
para não versionar os arquivos que ficaram em cópias de trabalho antigas.

### Etapa 5 — O que fazer com `ui/main_window.py` — FEITO (2026-08-09): (b)

Recomendava-se **(a)**, mantê-lo como configurador de desktop. Ao revisar
o estado real a recomendação não se sustentou e optou-se pela **(b)**, apagá-lo:

- **Sua função principal estava quebrada.** O botão "Iniciar Voz" —o elemento
  central, de 150×150 px— fazia `Popen` do `InterfazDAV/main.py`, retirado na
  etapa 4.
- **Não contribuía com o download de modelos.** Esse fluxo vive inteiro em
  `ui/preferences_dialog.py` (`_download_large` + `DownloadDialog` +
  `download_large_model`), que é aberto a partir da barra DAV e do botão ⚙ do
  painel. A `main_window` só *avisava* se faltasse um modelo, aviso que
  o `voice_bootstrap` já dá com a linha do `setup_models.py`.
- **Era o último resquício do modelo de dois processos**, o que mantinha viva a
  pergunta do §2.b.

Apagado: `ui/main_window.py` e `GUIFreeCad/main.py` (~180 linhas de wrapper).
Mantido: `ui/preferences_dialog.py`, `ui/download_dialog.py`,
`core/model_manager.py`, `scripts/setup_models.py`.

> **O que se perde:** baixar modelos com interface gráfica sem abrir o FreeCAD.
> Fica pela linha de comando (`python scripts/setup_models.py`). Se a via gráfica
> fizesse falta, é mais barato um comando na barra DAV que abra
> o `DownloadDialog` do que manter um app de desktop inteiro.

---

## 5. Riscos

| Risco | Mitigação |
| --- | --- |
| Um `QDockWidget` que dê crash derruba o FreeCAD inteiro | O painel não faz I/O nem trabalho pesado na thread de UI; o microfone já roda na sua thread |
| Mexe em código de várias pessoas (Tadeo, mica, Camila) | Etapas pequenas, PRs separados, `MainWindow.py` continua vivo até a etapa 4 |
| Perde-se o modo "janela solta" | O painel pode ser desacoplado (`setFloating(True)`): o comportamento é mantido sem processo à parte |
| 1011 linhas é bastante para dividir | A etapa 1 é só mover código, sem mudar comportamento; é feita e testada antes de tocar no FreeCAD |

---

## 6. Ordem de trabalho

As etapas são sequenciais e feitas de uma vez; não é preciso esperar ninguém
entre uma e outra. Cada uma fecha em um PR próprio para que seja revisável.

| Etapa | Escopo | Toca o FreeCAD | Toca código de outros |
| --- | --- | --- | --- |
| 1 | dividir `MainWindow.py` em `DavPanel` + controlador | não | sim (`MainWindow.py`) |
| 2 | montar o painel, sinais em vez de arquivos | sim | sim (ponte da mica) |
| 3 | árvore nativa | sim | sim (`capture_tree`) |
| 4 | apagar andaime | sim | sim |
| 5 | destino do launcher | não | não |

A 1 é a maior, mas a mais segura: é mover código, sem mudar
comportamento, e é testada rodando a janela solta como até agora.

**Avisar a equipe** antes da etapa 4: ali são apagados arquivos de Tadeo, mica
e Camila (`main.py`, `run_interfaz.bat`, `VoiceWorker.py`, `DiccionarioPrueba/`).
Até a 3 tudo é aditivo ou interno, e `MainWindow.py` continua funcionando.

### Decisões abertas

- **Etapa 0:** o remendo de `dav_commands.py` fica para que a GUI abra
  enquanto durar a migração, ou se pula direto para a 1? Se a 1 e a 2 saírem
  rápido, o remendo é trabalho jogado fora.
- **Etapa 5:** `ui/main_window.py` fica como configurador de desktop
  (recomendado) ou é absorvido pelo painel?

