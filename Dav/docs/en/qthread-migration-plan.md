# Plan — Migrate the `InterfazDAV` voice thread to `QThread`

## Context

The standalone `InterfazDAV` GUI hangs "every now and then". The root cause is
how the voice recognition thread is handled:

- `VoiceWorker` is a `QObject` that **emits Qt signals** (`partial_result`,
  `final_result`, `status_signal`, `finished`) from its `run()` method.
- But `run()` is executed inside a plain Python `threading.Thread`, **not** a
  `QThread` (see `MainWindow._StartVoiceRecognition`). With no associated
  `QThread`, delivery of signals to the GUI slots is on fragile/unguaranteed
  ground: it is exactly the kind of thread crossing that produces intermittent
  hangs and, eventually, crashes when touching widgets from the wrong thread.
- In addition, `closeEvent` does `self._VoiceThread.join(timeout=1)` in the GUI
  thread → it freezes the window for up to 1 second on close/minimize.

**Goal:** migrate to Qt's native pattern (`QThread` + `moveToThread`), which
guarantees queued connections (`QueuedConnection`) to the GUI thread and an
orderly shutdown without freezing. Bounded change: only `InterfazDAV`, without
touching `DavVoiceService` or the `GUIFreeCad` subsystem.

> Design note: `InterfazDAV` is a **standalone** GUI (its own `main.py` +
> `QApplication`, no FreeCAD). The robust `DavVoiceService` engine exists but is
> coupled to `GUIFreeCad` (`from core...` imports, adapters, CAD/preferences
> modes). Adopting it here would be an unnecessary coupling; that is why
> `VoiceWorker` is fixed within its own pattern, keeping it decoupled.

## Files to modify

1. `Dav/scr/ComponentesDAV/InterfazDAV/VoiceWorker.py`
2. `Dav/scr/ComponentesDAV/InterfazDAV/MainWindow.py`

## Changes

### 1. `VoiceWorker.py` — prepare the worker for `moveToThread`

`VoiceWorker` is already a `QObject` with the right signals; `run()` and
`stop()` work as they are. Minimal adjustments so that it works as a worker
moved to a `QThread`:

- Keep `run()` as the entry slot (it will be triggered by `QThread.started`).
- Keep the loop exit via the `self.running` flag (which `stop()` lowers). The
  loop already exits in an orderly way because `audio_queue.get(timeout=0.5)`
  does not block indefinitely.
- Ensure that `finished` is emitted at the end of `run()` (already done in the
  `finally`) — that signal will be the one that triggers the `QThread`'s
  `quit()`.

There is no need to rewrite the audio/Vosk logic: the queue pattern
(`audio_callback` → `queue.Queue` → loop) is already thread-safe and is kept.

### 2. `MainWindow.py` — use `QThread` + `moveToThread`

**Imports:** add `QThread` to the `PySide6.QtCore` import (where `Qt` and
`QTimer` are already imported). `import threading` can be removed if it is not
used elsewhere in the file (verify before deleting it).

**`_StartVoiceRecognition` (~lines 717-729):** replace the `threading.Thread`
with the Qt pattern:

```python
def _StartVoiceRecognition(self):
    ModelPath = _ResolveModelPath("vosk-model-small-es-0.42")
    if not os.path.exists(ModelPath):
        print(f"[WARNING] ADVERTENCIA: Modelo Vosk no encontrado en {ModelPath}")
        return

    self._VoiceThread = QThread(self)
    self._VoiceWorker = VoiceWorker(model_path=ModelPath)
    self._VoiceWorker.moveToThread(self._VoiceThread)

    # Start the loop when the thread starts
    self._VoiceThread.started.connect(self._VoiceWorker.run)

    # Worker -> GUI slot signals (automatically become QueuedConnection)
    self._VoiceWorker.partial_result.connect(self.UpdateCurrentText)
    self._VoiceWorker.final_result.connect(self.ProcessVoiceCommand)
    self._VoiceWorker.status_signal.connect(self.UpdateStatus)

    # Orderly shutdown: when run() ends, stop the thread and clean up
    self._VoiceWorker.finished.connect(self._VoiceThread.quit)
    self._VoiceWorker.finished.connect(self._VoiceWorker.deleteLater)
    self._VoiceThread.finished.connect(self._VoiceThread.deleteLater)

    self._VoiceThread.start()
```

**`closeEvent` (~lines 1037-1042):** replace the blocking `join(timeout=1)` with
a non-blocking Qt-based shutdown:

```python
def closeEvent(self, Event):
    if hasattr(self, '_VoiceWorker') and self._VoiceWorker is not None:
        self._VoiceWorker.stop()          # lowers the running flag -> loop exits
    if hasattr(self, '_VoiceThread') and self._VoiceThread is not None:
        self._VoiceThread.quit()
        self._VoiceThread.wait(1500)      # bounded wait on the QThread (ms)
    Event.accept()
```

`QThread.wait(ms)` waits in a controlled way for the thread to finish after
`stop()`; since the loop exits in ≤0.5 s (queue timeout), there should be no
perceptible freeze. If zero wait is preferred, `wait()` can be omitted and
`deleteLater` relied upon, but `wait(1500)` makes the shutdown deterministic
without freezing.

## Why this fixes the symptom

- With `moveToThread` + `QThread`, signal→slot connections between the worker
  (in its thread) and `MainWindow` (GUI thread) automatically become
  `QueuedConnection`: the `UpdateCurrentText` / `ProcessVoiceCommand` /
  `UpdateStatus` slots **always run in the GUI thread**, eliminating the current
  unsafe crossing.
- Shutdown no longer blocks the GUI thread with a Python `join`; it uses the
  native `QThread` lifecycle (`quit` + bounded `wait` + `deleteLater`).

## Risks / care points

- **`ProcessVoiceCommand` must remain lightweight.** Today it is, but it calls
  `OpenHelpWindow()` and the preferences branch uses `PrefsDialog.exec()` (a
  nested modal loop): it does not freeze Qt but pauses voice processing while
  the dialog is open. And `_ExecuteChildAction` will be the point where heavy
  FreeCAD operations enter in the future — those must **not** be executed
  inline in this slot. This is outside the scope of this fix, but noted so as
  not to reintroduce hangs.
- Verify that `import threading` is not used elsewhere in `MainWindow.py`
  before removing it.
- Do not start recognition twice: confirm where `_StartVoiceRecognition` is
  called today so as not to create two threads.

## Verification

1. Launch the standalone GUI:
   `python Dav/scr/ComponentesDAV/InterfazDAV/main.py`
2. Confirm that `_StatusLabel` changes to "mic activo" (green) → the
   `status_signal` signal reaches the GUI thread correctly.
3. Speak commands (`ayuda`, `minimizar`, group navigation) and verify that the
   UI responds smoothly and that the partial/final text updates without
   stuttering.
4. **Close the window** and confirm that closing is immediate, without the
   previous ~1 s freeze.
5. Leave the app listening for a while and verify that the intermittent hangs
   or crashes when updating widgets do not appear.
