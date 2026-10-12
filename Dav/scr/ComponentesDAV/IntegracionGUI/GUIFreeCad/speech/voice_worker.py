"""Micrófono + Vosk en un proceso aparte (usado en Linux).

Por qué existe: dentro de FreeCAD (AppImage) cargar PortAudio y libvosk.so puede
tumbar el proceso entero con una caída nativa (segfault / "Illegal instruction"),
y esa caída no se puede atrapar desde Python. Corriendo esto en un proceso
hijo, si algo se cae se cae el hijo: FreeCAD sigue vivo y solo avisa del error.

Protocolo (texto, una línea por mensaje):

* hijo -> DAV por stdout, cada mensaje con el prefijo ``@DAV `` y un JSON:
  ``{"t": "ready"}`` · ``{"t": "text", "text": str, "final": bool}`` ·
  ``{"t": "audio"}`` · ``{"t": "error", "kind": "import|model|mic", "msg": str}``.
  Cualquier otra línea (los logs de Kaldi, por ejemplo) se ignora.
* DAV -> hijo por stdin: ``{"cmd": "grammar", "json": str}`` y ``{"cmd": "stop"}``.
  Si stdin se cierra (FreeCAD murió) el hijo termina solo.

Solo usa la biblioteca estándar, ``sounddevice`` y ``vosk``: se ejecuta con el
Python del .venv de GUIFreeCad, no con el de FreeCAD.

Uso: ``python voice_worker.py <ruta_modelo> [sample_rate]``
"""

from __future__ import annotations

import json
import queue
import sys
import threading
import time

_PREFIX = "@DAV "


def _send(message: dict) -> None:
    sys.stdout.write(_PREFIX + json.dumps(message, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _read_commands(commands: "queue.Queue[dict]", stop: threading.Event) -> None:
    """Lee comandos de stdin hasta que se cierre (FreeCAD terminó) o pidan parar."""
    for line in sys.stdin:
        try:
            command = json.loads(line)
        except ValueError:
            continue
        if command.get("cmd") == "stop":
            break
        commands.put(command)
    stop.set()


def main() -> int:
    if len(sys.argv) < 2:
        _send({"t": "error", "kind": "model", "msg": "falta la ruta del modelo"})
        return 2
    model_path = sys.argv[1]
    sample_rate = int(sys.argv[2]) if len(sys.argv) > 2 else 16000

    try:
        import sounddevice as sd
        from vosk import KaldiRecognizer, Model, SetLogLevel
    except Exception as exc:  # noqa: BLE001 - ImportError u OSError (libreria ausente)
        _send({"t": "error", "kind": "import", "msg": str(exc)})
        return 3

    try:
        SetLogLevel(-1)
    except Exception:  # noqa: BLE001 - solo baja el ruido de Kaldi
        pass

    try:
        model = Model(model_path)
        recognizer = KaldiRecognizer(model, sample_rate)
    except Exception as exc:  # noqa: BLE001
        _send({"t": "error", "kind": "model", "msg": str(exc)})
        return 4

    stop = threading.Event()
    commands: "queue.Queue[dict]" = queue.Queue()
    threading.Thread(
        target=_read_commands, args=(commands, stop), name="cmd-reader", daemon=True
    ).start()

    audio_q: "queue.Queue[bytes]" = queue.Queue()
    heard_audio = threading.Event()

    def callback(indata, frames, time_info, status) -> None:
        try:
            audio_q.put(bytes(indata), block=False)
        except Exception:  # noqa: BLE001
            return
        heard_audio.set()

    try:
        # Sin micrófono (típico de una VM sin audio) se informa en vez de abrir
        # un stream que podría colgar PortAudio.
        devices = sd.query_devices()
        input_ids = [
            i for i, d in enumerate(devices) if d.get("max_input_channels", 0) > 0
        ]
        if not input_ids:
            raise RuntimeError("No hay ningún micrófono disponible")
        device = None  # el predeterminado del sistema
        default_in = sd.default.device[0]
        if default_in is None or default_in < 0:
            device = input_ids[0]

        stream = sd.RawInputStream(
            samplerate=sample_rate,
            blocksize=4000,
            dtype="int16",
            channels=1,
            device=device,
            callback=callback,
        )
    except Exception as exc:  # noqa: BLE001
        _send({"t": "error", "kind": "mic", "msg": str(exc)})
        return 5

    applied_grammar = None
    last_pulse = 0.0
    with stream:
        _send({"t": "ready"})
        while not stop.is_set():
            # Solo interesa la última gramática; y Vosk aborta el proceso si se
            # le cambia la gramática a un recognizer que ya procesó audio, por
            # eso se hace Reset() antes (igual que en dav_voice_service.py).
            grammar = None
            while True:
                try:
                    command = commands.get_nowait()
                except queue.Empty:
                    break
                if command.get("cmd") == "grammar":
                    grammar = command.get("json")
            if grammar and grammar != applied_grammar:
                try:
                    recognizer.Reset()
                    recognizer.SetGrammar(grammar)
                except Exception as exc:  # noqa: BLE001
                    sys.stderr.write(f"fallo SetGrammar: {exc}\n")
                applied_grammar = grammar

            if heard_audio.is_set():
                now = time.monotonic()
                if now - last_pulse >= 0.1:
                    heard_audio.clear()
                    last_pulse = now
                    _send({"t": "audio"})

            try:
                data = audio_q.get(timeout=0.5)
            except queue.Empty:
                continue
            if recognizer.AcceptWaveform(data):
                text = json.loads(recognizer.Result()).get("text", "")
                _send({"t": "text", "text": text, "final": True})
            else:
                text = json.loads(recognizer.PartialResult()).get("partial", "")
                _send({"t": "text", "text": text, "final": False})
    return 0


if __name__ == "__main__":
    sys.exit(main())
