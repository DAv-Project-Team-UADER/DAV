# Plano: Árvore do FreeCAD como dados navegáveis (substituir imagem PNG)

> **Estado: CONCLUÍDO E SUPERADO** (verificado em 2026-08-18).
>
> As fases 1-3 foram cumpridas, mas **não pelo caminho que este plano descreve**.
> O plano propunha macro → `tree_data.json` → GUI com dois timers; a
> implementação final lê o FreeCAD **em processo** e é atualizada por eventos,
> sem arquivos intermediários nem polling. Os três arquivos que este documento
> pedia para modificar (`MainWindow.py`, `capture_tree.FCMacro`,
> `trigger_capture.py`) **já não existem**.
>
> O que vale hoje:
> - `InterfazDAV/DavPanel.py` → `SetTree()` pinta o `QTreeWidget`.
> - `integration/dav_dock_panel.py` → `PublishTree()` lê `doc.Objects`,
>   `_TreeDocumentObserver` atualiza diante de mudanças do documento.
> - O contrato de dados (`name`/`label`/`type`/`visible`/`parent`) **foi
>   mantido exatamente** do design abaixo.
>
> Da seção "Fora de escopo", o **destaque bidirecional já está
> feito** (`_TreeSelectionObserver` + `DavPanel.HighlightSelection`, 2026-08-18):
> o que é selecionado por voz é destacado no painel. Continuam pendentes
> navegar na árvore por voz ("seleccionar el tercero") e o sentido
> painel → FreeCAD (clique no painel que selecione no FreeCAD).
>
> É mantido como registro do design e do contrato de dados.

## Contexto

Hoje o painel **"Árbol de FreeCAD"** da GUI PySide6 (`Dav/scr/ComponentesDAV/InterfazDAV/MainWindow.py`)
não mostra a árvore real: mostra uma **imagem PNG** (`tree_capture.png`) que uma macro do FreeCAD
gera com `combo_view.grab()` e que a GUI atualiza a cada 2s. Isso cumpre o visual, mas **não é
navegável** — não há objetos, nem tipos, nem hierarquia como dados. O requisito do CLAUDE.md
("navegar objetos criados") pede dados reais.

**Objetivo:** que a macro envie a **estrutura de objetos** do documento ativo como **JSON**
(nome, tipo, label, visibilidade, hierarquia pai/filho) e que a GUI a pinte em um
**`QTreeWidget`**, substituindo por completo a captura de imagem. Sem comandos de voz ainda e
sem seleção bidirecional com o FreeCAD (fica como fase futura).

O fluxo de comunicação GUI↔FreeCAD já existe e é reutilizado: arquivo de sinal JSON +
`dav_paths.json` + macro com `QTimer`. Muda apenas **o que** é transportado (dados em vez de imagem)
e **como é pintado** (widget em vez de pixmap).

## Arquivos a modificar

### 1. `Dav/scr/ComponentesDAV/InterfazDAV/capture_tree.FCMacro`
Substituir `capture_tree()` (que faz `pixmap.grab()` / `save PNG`) por uma função que serialize
a árvore do documento ativo:
- Percorrer `App.ActiveDocument.Objects`.
- Para cada objeto: `Name`, `Label`, `TypeId`, visibilidade (`obj.ViewObject.Visibility` se houver GUI),
  e o grupo pai (`obj.getParentGroup()` se existir) para reconstruir a hierarquia.
- Escrever o resultado em um novo arquivo `tree_data.json` (caminho obtido de `dav_paths.json`,
  nova chave `tree_data_path`), e responder no `signal_file` com
  `{"status":"done","result":{"success":true}}` igual a hoje.
- Manter o `QTimer` de escuta e o padrão de sinal intactos.

### 2. `Dav/scr/ComponentesDAV/InterfazDAV/trigger_capture.py`
- Em `ensure_macro_installed()`: adicionar `tree_data_path` ao dict `paths` que é escrito em
  `dav_paths.json`.
- Limpar o `tree_data.json` antigo ao iniciar (igual a hoje se limpa `tree_capture.png`).
- `trigger_capture()` não muda (continua enviando o sinal `{"command":"capture"}` e esperando
  `status:done`).

### 3. `Dav/scr/ComponentesDAV/InterfazDAV/MainWindow.py`
Substituir o painel de imagem por uma árvore de dados:
- **UI** (`_SetupUi`, painel "Árbol de FreeCAD"): trocar `self._TreeImageLabel = QLabel()` por
  `self._TreeWidget = QTreeWidget()` (importar `QTreeWidget`, `QTreeWidgetItem`). Estilizar com a
  paleta `self._T` como o resto.
- **Apagar** a lógica de imagem: `_ShowPlaceholderImage`, `_RefreshTreeImage`, o `_RefreshTimer`
  (2s), e a parte do `resizeEvent` que reescala o pixmap.
- **Novo** `_RefreshTreeData()`: ler `tree_data.json` (se mudou por mtime, mesmo padrão do
  antigo `_LastImageMtime`), limpar o `QTreeWidget` e reconstruir os itens a partir do JSON
  (label + tipo, e indentação por hierarquia). Conectar a um `QTimer` (pode reutilizar o de 2s).
- `_AutoCapture()` (5s) é mantido: dispara o sinal para a macro; só que agora a macro produz
  dados em vez de PNG.
- Ajustar `SetColor` / `_UpdateStyles` para reestilizar o `QTreeWidget` em vez do label de imagem.
- Remover referências mortas a `tree_capture.png` em `_CheckMacroStatus` (mudar para verificar
  `tree_data.json`).

## Formato `tree_data.json` (contrato GUI↔macro)
```json
{
  "document": "Unnamed",
  "objects": [
    {"name": "Box", "label": "Cubo", "type": "Part::Box", "visible": true, "parent": null},
    {"name": "Fusion", "label": "Fusión", "type": "Part::MultiFuse", "visible": true, "parent": null}
  ]
}
```
v1: lista plana com `parent` (None ou Name do grupo). O `QTreeWidget` aninha por `parent`; objetos
sem pai vão para a raiz.

## Reutilização
- Mecanismo de sinal/config já existente (`signal_file`, `dav_paths.json`, `QTimer` na macro)
  — não se reinventa, apenas se adiciona `tree_data_path`.
- Padrão de detecção de mudanças por `mtime` (como `_LastImageMtime`) é reaplicado para
  `tree_data.json`.
- Paleta e QSS (`self._T`, `_PanelQss`) para estilizar a árvore de forma consistente com a GUI.

## Verificação
1. **Sem FreeCAD (rápido):** criar à mão um `tree_data.json` de exemplo na pasta da InterfazDAV
   e iniciar a GUI standalone (`python main.py --gui` a partir de PruebaIntegracion, ou o entrypoint
   da InterfazDAV) → o painel deve mostrar os objetos do JSON na árvore, não a imagem.
2. **Com FreeCAD (real):** abrir o FreeCAD com `iniciar_dav.ps1`, executar a macro `capture_tree`,
   criar alguns objetos (Box, etc.). Em ≤5s o `QTreeWidget` da GUI deve listar esses objetos
   com o seu tipo. Criar/apagar objetos no FreeCAD e verificar que a árvore da GUI é atualizada.
3. **Regressão:** histórico, voz, temas e preferências continuam funcionando (não se mexeu em `VoiceWorker`
   nem em `AddToHistory`).

## Fora de escopo (fases futuras)
- Navegar na árvore por voz (próximo/anterior/selecionar N).
- Seleção bidirecional (selecionar por voz → destacar na árvore real do FreeCAD).
- Apagar a maquete morta `Dav/scr/PruebaIntegracion/hilos/GestorDeHilos.py` (Tkinter, não usada)
  — limpeza à parte, se desejado.
