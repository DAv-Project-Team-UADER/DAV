# Plano — Migrar a thread de voz da `InterfazDAV` para `QThread`

## Contexto

A GUI standalone `InterfazDAV` trava "de vez em quando". A causa raiz é como a
thread de reconhecimento de voz é tratada:

- `VoiceWorker` é um `QObject` que **emite sinais Qt** (`partial_result`,
  `final_result`, `status_signal`, `finished`) a partir do seu método `run()`.
- Mas `run()` é executado dentro de uma `threading.Thread` simples do Python, **não**
  de uma `QThread` (ver `MainWindow._StartVoiceRecognition`). Sem uma `QThread`
  associada, a entrega de sinais para os slots da GUI fica em terreno
  frágil/não garantido: é exatamente o tipo de cruzamento de threads que produz
  travamentos intermitentes e, eventualmente, crashes ao tocar widgets a partir da
  thread errada.
- Além disso, `closeEvent` faz `self._VoiceThread.join(timeout=1)` na thread da
  GUI → congela a janela por até 1 segundo ao fechar/minimizar.

**Objetivo:** migrar para o padrão nativo do Qt (`QThread` + `moveToThread`), que
garante conexões em fila (`QueuedConnection`) para a thread da GUI e um
encerramento ordenado sem freeze. Mudança restrita: somente `InterfazDAV`, sem tocar
em `DavVoiceService` nem no subsistema `GUIFreeCad`.

> Nota de design: `InterfazDAV` é uma GUI **standalone** (seu próprio `main.py` +
> `QApplication`, sem FreeCAD). O motor robusto `DavVoiceService` existe, mas está
> acoplado ao `GUIFreeCad` (imports `from core...`, adapters, modos CAD/preferences).
> Adotá-lo aqui seria um acoplamento desnecessário; por isso o `VoiceWorker` é corrigido
> no seu próprio padrão, mantendo-o desacoplado.

## Arquivos a modificar

1. `Dav/scr/ComponentesDAV/InterfazDAV/VoiceWorker.py`
2. `Dav/scr/ComponentesDAV/InterfazDAV/MainWindow.py`

## Mudanças

### 1. `VoiceWorker.py` — preparar o worker para `moveToThread`

`VoiceWorker` já é um `QObject` com os sinais corretos; o `run()` e o `stop()`
servem como estão. Ajustes mínimos para que funcione como worker movido para uma `QThread`:

- Manter `run()` como slot de entrada (será disparado por `QThread.started`).
- Manter a saída do laço via a flag `self.running` (que `stop()` abaixa). O
  laço já sai de forma ordenada porque `audio_queue.get(timeout=0.5)` não bloqueia
  indefinidamente.
- Garantir que no final de `run()` seja emitido `finished` (já é feito no `finally`)
  — esse sinal será o que dispara o `quit()` da `QThread`.

Não é preciso reescrever a lógica de áudio/Vosk: o padrão de fila
(`audio_callback` → `queue.Queue` → laço) já é thread-safe e é mantido.

### 2. `MainWindow.py` — usar `QThread` + `moveToThread`

**Imports:** adicionar `QThread` à importação de `PySide6.QtCore` (onde já são
importados `Qt`, `QTimer`). Pode-se remover `import threading` se não for usado em outro
ponto do arquivo (verificar antes de apagar).

**`_StartVoiceRecognition` (~linhas 717-729):** substituir a `threading.Thread`
pelo padrão Qt:

```python
def _StartVoiceRecognition(self):
    ModelPath = _ResolveModelPath("vosk-model-small-es-0.42")
    if not os.path.exists(ModelPath):
        print(f"[WARNING] ADVERTENCIA: Modelo Vosk no encontrado en {ModelPath}")
        return

    self._VoiceThread = QThread(self)
    self._VoiceWorker = VoiceWorker(model_path=ModelPath)
    self._VoiceWorker.moveToThread(self._VoiceThread)

    # Início do laço quando a thread inicia
    self._VoiceThread.started.connect(self._VoiceWorker.run)

    # Sinais worker -> slots da GUI (ficam em QueuedConnection automaticamente)
    self._VoiceWorker.partial_result.connect(self.UpdateCurrentText)
    self._VoiceWorker.final_result.connect(self.ProcessVoiceCommand)
    self._VoiceWorker.status_signal.connect(self.UpdateStatus)

    # Encerramento ordenado: ao terminar run(), parar a thread e limpar
    self._VoiceWorker.finished.connect(self._VoiceThread.quit)
    self._VoiceWorker.finished.connect(self._VoiceWorker.deleteLater)
    self._VoiceThread.finished.connect(self._VoiceThread.deleteLater)

    self._VoiceThread.start()
```

**`closeEvent` (~linhas 1037-1042):** substituir o `join(timeout=1)` bloqueante por
um desligamento não bloqueante baseado em Qt:

```python
def closeEvent(self, Event):
    if hasattr(self, '_VoiceWorker') and self._VoiceWorker is not None:
        self._VoiceWorker.stop()          # abaixa a flag running -> o laço sai
    if hasattr(self, '_VoiceThread') and self._VoiceThread is not None:
        self._VoiceThread.quit()
        self._VoiceThread.wait(1500)      # espera limitada da QThread (ms)
    Event.accept()
```

`QThread.wait(ms)` espera de forma controlada que a thread termine após `stop()`;
como o laço sai em ≤0,5 s (timeout da fila), não deveria haver freeze
perceptível. Se se preferir zero espera, pode-se omitir o `wait()` e confiar em
`deleteLater`, mas `wait(1500)` deixa o encerramento determinístico sem congelar.

## Por que isso corrige o sintoma

- Com `moveToThread` + `QThread`, as conexões sinal→slot entre o worker (na sua
  thread) e a `MainWindow` (thread da GUI) passam a ser `QueuedConnection` automaticamente:
  os slots `UpdateCurrentText` / `ProcessVoiceCommand` / `UpdateStatus` são executados
  **sempre na thread da GUI**, eliminando o cruzamento inseguro atual.
- O encerramento deixa de bloquear a thread da GUI com um `join` do Python; usa o ciclo
  de vida nativo da `QThread` (`quit` + `wait` limitado + `deleteLater`).

## Riscos / cuidados

- **`ProcessVoiceCommand` deve continuar leve.** Hoje é, mas chama
  `OpenHelpWindow()` e o ramo de preferências usa `PrefsDialog.exec()` (loop modal
  aninhado): não congela o Qt, mas pausa o processamento de voz enquanto o diálogo está
  aberto. E `_ExecuteChildAction` será o ponto onde no futuro entrarão operações
  pesadas do FreeCAD — essas **não** devem ser executadas inline neste slot. Fica fora
  do escopo desta correção, mas anotado para não reintroduzir travamentos.
- Verificar que `import threading` não seja usado em outra parte de `MainWindow.py`
  antes de removê-lo.
- Não reiniciar o reconhecimento duas vezes: confirmar onde hoje é chamado
  `_StartVoiceRecognition` para não criar duas threads.

## Verificação

1. Iniciar a GUI standalone:
   `python Dav/scr/ComponentesDAV/InterfazDAV/main.py`
2. Confirmar que o `_StatusLabel` passa a "mic activo" (verde) → o sinal
   `status_signal` chega corretamente à thread da GUI.
3. Falar comandos (`ayuda`, `minimizar`, navegação de grupos) e verificar que a
   UI responde de forma fluida e que o texto parcial/final é atualizado sem engasgos.
4. **Fechar a janela** e confirmar que o fechamento é imediato, sem o congelamento
   de ~1 s anterior.
5. Deixar o app escutando por um tempo e verificar que não aparecem os travamentos
   intermitentes nem crashes ao atualizar widgets.
