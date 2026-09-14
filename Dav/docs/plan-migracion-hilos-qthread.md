# Plan — Migrar el hilo de voz de `InterfazDAV` a `QThread`

## Contexto

La GUI standalone `InterfazDAV` se cuelga "de a ratos". La causa raíz es cómo se
maneja el hilo de reconocimiento de voz:

- `VoiceWorker` es un `QObject` que **emite señales Qt** (`partial_result`,
  `final_result`, `status_signal`, `finished`) desde su método `run()`.
- Pero `run()` se corre dentro de un `threading.Thread` de Python plano, **no** de
  un `QThread` (ver `MainWindow._StartVoiceRecognition`). Al no haber un `QThread`
  asociado, la entrega de señales hacia los slots de la GUI queda en terreno
  frágil/no garantizado: es exactamente el tipo de cruce de hilos que produce
  cuelgues intermitentes y, eventualmente, crashes al tocar widgets desde el hilo
  equivocado.
- Además, `closeEvent` hace `self._VoiceThread.join(timeout=1)` en el hilo de la
  GUI → congela la ventana hasta 1 segundo al cerrar/minimizar.

**Objetivo:** migrar al patrón nativo de Qt (`QThread` + `moveToThread`), que
garantiza conexiones en cola (`QueuedConnection`) hacia el hilo de la GUI y un
cierre ordenado sin freeze. Cambio acotado: solo `InterfazDAV`, sin tocar
`DavVoiceService` ni el subsistema `GUIFreeCad`.

> Nota de diseño: `InterfazDAV` es una GUI **standalone** (su propio `main.py` +
> `QApplication`, sin FreeCAD). El motor robusto `DavVoiceService` existe pero está
> acoplado a `GUIFreeCad` (imports `from core...`, adapters, modos CAD/preferences).
> Adoptarlo acá sería un acople innecesario; por eso se corrige `VoiceWorker` en su
> propio patrón, manteniéndolo desacoplado.

## Archivos a modificar

1. `Dav/scr/ComponentesDAV/InterfazDAV/VoiceWorker.py`
2. `Dav/scr/ComponentesDAV/InterfazDAV/MainWindow.py`

## Cambios

### 1. `VoiceWorker.py` — preparar el worker para `moveToThread`

`VoiceWorker` ya es un `QObject` con las señales correctas; el `run()` y el `stop()`
sirven tal cual. Ajustes mínimos para que funcione como worker movido a un `QThread`:

- Mantener `run()` como slot de entrada (lo va a disparar `QThread.started`).
- Mantener la salida del bucle vía el flag `self.running` (que `stop()` baja). El
  bucle ya sale ordenadamente porque `audio_queue.get(timeout=0.5)` no bloquea
  indefinidamente.
- Asegurar que al final de `run()` se emita `finished` (ya se hace en el `finally`)
  — esa señal será la que dispare el `quit()` del `QThread`.

No hace falta reescribir la lógica de audio/Vosk: el patrón de cola
(`audio_callback` → `queue.Queue` → bucle) ya es thread-safe y se conserva.

### 2. `MainWindow.py` — usar `QThread` + `moveToThread`

**Imports:** agregar `QThread` a la importación de `PySide6.QtCore` (donde ya se
importan `Qt`, `QTimer`). Se puede quitar `import threading` si no se usa en otro
lado del archivo (verificar antes de borrarlo).

**`_StartVoiceRecognition` (~líneas 717-729):** reemplazar el `threading.Thread`
por el patrón Qt:

```python
def _StartVoiceRecognition(self):
    ModelPath = _ResolveModelPath("vosk-model-small-es-0.42")
    if not os.path.exists(ModelPath):
        print(f"[WARNING] ADVERTENCIA: Modelo Vosk no encontrado en {ModelPath}")
        return

    self._VoiceThread = QThread(self)
    self._VoiceWorker = VoiceWorker(model_path=ModelPath)
    self._VoiceWorker.moveToThread(self._VoiceThread)

    # Arranque del bucle cuando el hilo inicia
    self._VoiceThread.started.connect(self._VoiceWorker.run)

    # Señales worker -> slots GUI (quedan en QueuedConnection automáticamente)
    self._VoiceWorker.partial_result.connect(self.UpdateCurrentText)
    self._VoiceWorker.final_result.connect(self.ProcessVoiceCommand)
    self._VoiceWorker.status_signal.connect(self.UpdateStatus)

    # Cierre ordenado: al terminar run(), parar el hilo y limpiar
    self._VoiceWorker.finished.connect(self._VoiceThread.quit)
    self._VoiceWorker.finished.connect(self._VoiceWorker.deleteLater)
    self._VoiceThread.finished.connect(self._VoiceThread.deleteLater)

    self._VoiceThread.start()
```

**`closeEvent` (~líneas 1037-1042):** reemplazar el `join(timeout=1)` bloqueante por
un apagado no-bloqueante basado en Qt:

```python
def closeEvent(self, Event):
    if hasattr(self, '_VoiceWorker') and self._VoiceWorker is not None:
        self._VoiceWorker.stop()          # baja el flag running -> sale el bucle
    if hasattr(self, '_VoiceThread') and self._VoiceThread is not None:
        self._VoiceThread.quit()
        self._VoiceThread.wait(1500)      # espera acotada del QThread (ms)
    Event.accept()
```

`QThread.wait(ms)` espera de forma controlada a que el hilo termine tras `stop()`;
como el bucle sale en ≤0.5 s (timeout de la cola), no debería haber freeze
perceptible. Si se prefiere cero espera, se puede omitir `wait()` y confiar en
`deleteLater`, pero `wait(1500)` deja el cierre determinista sin congelar.

## Por qué esto arregla el síntoma

- Con `moveToThread` + `QThread`, las conexiones señal→slot entre el worker (en su
  hilo) y `MainWindow` (hilo GUI) pasan a ser `QueuedConnection` automáticamente:
  los slots `UpdateCurrentText` / `ProcessVoiceCommand` / `UpdateStatus` se ejecutan
  **siempre en el hilo de la GUI**, eliminando el cruce inseguro actual.
- El cierre deja de bloquear el hilo de la GUI con un `join` de Python; usa el ciclo
  de vida nativo de `QThread` (`quit` + `wait` acotado + `deleteLater`).

## Riesgos / cuidados

- **`ProcessVoiceCommand` debe seguir siendo liviano.** Hoy lo es, pero llama a
  `OpenHelpWindow()` y la rama de preferencias usa `PrefsDialog.exec()` (loop modal
  anidado): no congela Qt pero pausa el procesamiento de voz mientras el diálogo está
  abierto. Y `_ExecuteChildAction` será el punto donde a futuro entren operaciones
  pesadas de FreeCAD — esas **no** deben ejecutarse inline en este slot. Queda fuera
  del alcance de este fix, pero anotado para no reintroducir cuelgues.
- Verificar que `import threading` no se use en otra parte de `MainWindow.py` antes
  de eliminarlo.
- No reiniciar el reconocimiento dos veces: confirmar dónde se llama hoy a
  `_StartVoiceRecognition` para no crear dos hilos.

## Verificación

1. Arrancar la GUI standalone:
   `python Dav/scr/ComponentesDAV/InterfazDAV/main.py`
2. Confirmar que el `_StatusLabel` pasa a "mic activo" (verde) → la señal
   `status_signal` llega al hilo GUI correctamente.
3. Hablar comandos (`ayuda`, `minimizar`, navegación de grupos) y verificar que la
   UI responde fluida y que el texto parcial/final se actualiza sin tirones.
4. **Cerrar la ventana** y confirmar que el cierre es inmediato, sin el congelamiento
   de ~1 s previo.
5. Dejar la app escuchando un rato y verificar que no aparecen los cuelgues
   intermitentes ni crashes al actualizar widgets.
