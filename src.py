import json
import queue
import re
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

import numpy as np
import sounddevice as sd
from pyrnnoise import RNNoise
import vosk
import command_parser

DEFAULT_SAMPLE_RATE = 16000
RNNOISE_SR = 48000
CHUNK_DURATION_MS = 256
CHUNK_SIZE = int(DEFAULT_SAMPLE_RATE * CHUNK_DURATION_MS / 1000)
PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = PROJECT_DIR / "transcripcion.txt"
COMMANDS_LOG_FILE = PROJECT_DIR / "comandos_reconocidos.jsonl"
COMMAND_ROOT = PROJECT_DIR / "archovo"

COMMAND_FOLDER_MAP = {
    "abrir relevamiento sketcher workbench": COMMAND_ROOT
    / "Relevamiento Sketcher Workbenchv2_Alex_30-04-2026.zip",
    "abrir relevo draft": COMMAND_ROOT / "RelevoDraftv4_JoaquinPoggio_7-5-26",
    "abrir relevo explorer": COMMAND_ROOT / "Relevo_Explorer_v2_Jesus_Serra_2026-05-08",
}

MODEL_PATTERNS = {
    "chico": ["model-small-es", "vosk-model-small-es-*", "vosk-model-small-es*"],
    "grande": ["model-es", "vosk-model-es-*", "vosk-model-es*"],
}


def normalize_model_dir(path_str):
    """Si el zip creó carpeta duplicada, baja un nivel automáticamente."""
    path = Path(path_str)
    if not path.is_dir():
        return None

    current = path
    for _ in range(2):
        if (current / "am" / "final.mdl").is_file():
            return str(current)
        subdirs = [p for p in current.iterdir() if p.is_dir()]
        if len(subdirs) == 1:
            current = subdirs[0]
            continue
        break
    return None


def find_local_model(patterns):
    for pattern in patterns:
        for candidate in sorted(PROJECT_DIR.glob(pattern)):
            normalized = normalize_model_dir(str(candidate))
            if normalized:
                return normalized
    return None


def choose_model_path():
    available = {
        "chico": find_local_model(MODEL_PATTERNS["chico"]),
        "grande": find_local_model(MODEL_PATTERNS["grande"]),
    }

    options = []
    if available["chico"]:
        options.append(("1", "chico", available["chico"]))
    if available["grande"]:
        options.append(("2", "grande", available["grande"]))

    if not options:
        return None

    print("Modelos disponibles:")
    for option_id, label, path in options:
        print(f"{option_id}) Modelo {label}: {path}")

    valid_ids = {option_id for option_id, _label, _path in options}
    while True:
        choice = input("Elegí modelo (1 o 2): ").strip()
        if choice not in valid_ids:
            print("Opción inválida. Probá de nuevo.")
            continue
        for option_id, _label, path in options:
            if choice == option_id:
                return path


def resample_audio(audio: np.ndarray, source_rate: int, target_rate: int) -> np.ndarray:
    if source_rate == target_rate or audio.size == 0:
        return audio

    audio_float = audio.astype(np.float32)
    target_len = int(round(len(audio_float) * target_rate / source_rate))
    if target_len <= 0:
        return np.array([], dtype=np.int16)

    original_indices = np.arange(len(audio_float))
    target_indices = np.linspace(0, len(audio_float) - 1, target_len)
    resampled = np.interp(target_indices, original_indices, audio_float)
    return np.clip(resampled, -32768, 32767).astype(np.int16)


def denoise_chunk(denoiser: RNNoise, audio_16k: np.ndarray) -> np.ndarray:
    if audio_16k.size == 0:
        return audio_16k

    audio_48k = resample_audio(audio_16k, DEFAULT_SAMPLE_RATE, RNNOISE_SR)
    audio_48k = np.expand_dims(audio_48k, axis=0)
    denoised_frames = []

    for _speech_prob, denoised_frame in denoiser.denoise_chunk(audio_48k):
        denoised_frames.append(denoised_frame)

    if denoised_frames:
        audio_48k = np.concatenate(denoised_frames, axis=-1)

    return resample_audio(audio_48k[0], RNNOISE_SR, DEFAULT_SAMPLE_RATE)


def print_missing_models_help():
    print(
        "No encuentro modelos en la carpeta del proyecto.\n"
        "Necesitás al menos uno:\n"
        "- Chico: 'model-small-es' o 'vosk-model-small-es-*'\n"
        "- Grande: 'model-es' o 'vosk-model-es-*'"
    )


def normalize_command_text(text: str) -> str:
    cleaned = "".join(ch for ch in text.lower() if ch.isalnum() or ch.isspace())
    return " ".join(cleaned.split())


def fold_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def try_parse_sketch_line_length_mm(text: str):
    """Si la frase pide crear una línea con medida, devuelve longitud en mm; si no, None."""
    folded = fold_accents(text.lower())
    if not re.search(r"\b(linea|lineas)\b", folded):
        return None
    if not re.search(
        r"\b(crear|crea|dibujar|dibuja|agregar|agrega|poner|pone|pon|trazar|traza)\b",
        folded,
    ):
        return None
    match = re.search(
        r"(\d+(?:[.,]\d+)?)\s*(centimetros?|centimetro|cms?|milimetros?|milimetro|mms?)?",
        folded,
    )
    if not match:
        return None
    value = float(match.group(1).replace(",", "."))
    unit = (match.group(2) or "").lower()
    if "centi" in unit or unit.strip("s") in ("cm", "cms"):
        return value * 10.0
    if "mili" in unit or unit in ("mm", "mms"):
        return value
    return value


VOICE_PHRASES_FILE = PROJECT_DIR / "voice_phrases.json"


def load_voice_phrase_rules():
    """
    Carga frases → script desde voice_phrases.json.
    Cada entrada puede tener varias variantes en 'when'; se priorizan las más largas
    para que 'guardar como' gane sobre 'guardar'.
    """
    if not VOICE_PHRASES_FILE.is_file():
        return []
    try:
        with open(VOICE_PHRASES_FILE, encoding="utf-8") as handle:
            entries = json.load(handle)
    except (json.JSONDecodeError, OSError) as error:
        print(f"No se pudo leer voice_phrases.json: {error}", file=sys.stderr)
        return []
    flat = []
    for entry in entries:
        when = entry.get("when") or []
        if isinstance(when, str):
            when = [when]
        script = (entry.get("script") or "").strip()
        if not script:
            continue
        label = entry.get("label") or (when[0] if when else "comando")
        for phrase in when:
            key = normalize_command_text(fold_accents(phrase.lower()))
            if not key:
                continue
            flat.append((len(key), key, script, label))
    flat.sort(key=lambda item: -item[0])
    return flat


def match_voice_phrase_script(text: str, rules):
    if not rules:
        return None
    normalized = normalize_command_text(fold_accents(text.lower()))
    if not normalized:
        return None
    for _length, key, script, label in rules:
        if key in normalized:
            return script, label
    return None


def parseVoiceCommand(transcription: str) -> dict:
    if not transcription or not isinstance(transcription, str):
        return {"success": False, "command": None, "parameters": None, "error": "Texto inválido."}

    text = transcription.lower().strip()
    
    # Mapeo de números hablados a dígitos (incluyendo errores acústicos comunes de Vosk)
    word_to_num = {
        "cero": "0", "uno": "1", "un": "1", "dos": "2", "tres": "3", 
        "cuatro": "4", "cuatroro": "4", "cinco": "5", "cincoco": "5", 
        "seis": "6", "seisis": "6", "siete": "7", "ocho": "8", "ochoho": "8", 
        "nueve": "9", "diez": "10", "once": "11", "doce": "12", "trece": "13", 
        "catorce": "14", "quince": "15", "veinte": "20", "treinta": "30"
    }
    for word, digit in word_to_num.items():
        text = re.sub(rf'\b{word}\b', digit, text)

    text = text.replace("menos ", "-")
    text = text.replace(",", ".")
    
    num_pattern = r'(-?\d+(?:\.\d+)?)'

    commands_config = [
        {
            "command": "create_3point_arc",
            "patterns": [
                rf'arco por tres puntos.*?{num_pattern}.*?{num_pattern}.*?{num_pattern}.*?{num_pattern}.*?{num_pattern}.*?{num_pattern}',
                rf'crear arco desde.*?{num_pattern}.*?{num_pattern}.*?pasando por.*?{num_pattern}.*?{num_pattern}.*?hasta.*?{num_pattern}.*?{num_pattern}'
            ],
            "extract": lambda g: {"x1": float(g[0]), "y1": float(g[1]), "x2": float(g[2]), "y2": float(g[3]), "x3": float(g[4]), "y3": float(g[5])}
        },
        {
            "command": "create_arc_of_ellipse",
            "patterns": [
                rf'arco de elipse.*?(?:en|centro).*?{num_pattern}.*?{num_pattern}.*?radio mayor.*?{num_pattern}.*?menor.*?{num_pattern}.*?de.*?{num_pattern}.*?a.*?{num_pattern}'
            ],
            "extract": lambda g: {"centro_x": float(g[0]), "centro_y": float(g[1]), "radio_mayor": float(g[2]), "radio_menor": float(g[3]), "inicio": float(g[4]), "fin": float(g[5])}
        },
        {
            "command": "create_arc_of_hyperbola",
            "patterns": [
                rf'arco de hip[eé]rbola.*?(?:en|centro).*?{num_pattern}.*?{num_pattern}.*?radios.*?{num_pattern}.*?y.*?{num_pattern}.*?desde.*?{num_pattern}.*?hasta.*?{num_pattern}'
            ],
            "extract": lambda g: {"centro_x": float(g[0]), "centro_y": float(g[1]), "radio_x": float(g[2]), "radio_y": float(g[3]), "inicio": float(g[4]), "fin": float(g[5])}
        },
        {
            "command": "create_arc_of_parabola",
            "patterns": [
                rf'arco de par[aá]bola.*?foco en.*?{num_pattern}.*?{num_pattern}.*?v[eé]rtice en.*?{num_pattern}.*?{num_pattern}.*?desde.*?{num_pattern}.*?hasta.*?{num_pattern}'
            ],
            "extract": lambda g: {"foco_x": float(g[0]), "foco_y": float(g[1]), "vertice_x": float(g[2]), "vertice_y": float(g[3]), "inicio": float(g[4]), "fin": float(g[5])}
        },
        {
            "command": "create_arc",
            "patterns": [
                rf'arco.*?(?:en|centro).*?{num_pattern}.*?{num_pattern}.*?radio.*?{num_pattern}.*?(?:desde|inicio).*?{num_pattern}.*?(?:a|hasta|fin).*?{num_pattern}'
            ],
            "extract": lambda g: {"centro_x": float(g[0]), "centro_y": float(g[1]), "radio": float(g[2]), "inicio": float(g[3]), "fin": float(g[4])}
        },
        {
            "command": "crear_circulo",
            "patterns": [
                rf'c[ií]rculo.*?(?:en|centro).*?{num_pattern}.*?{num_pattern}.*?radio.*?{num_pattern}'
            ],
            "extract": lambda g: {"centro_x": float(g[0]), "centro_y": float(g[1]), "radio": float(g[2])}
        },
        {
            "command": "create_line",
            "patterns": [
                rf'l[ií]nea desde.*?{num_pattern}.*?{num_pattern}.*?hasta.*?{num_pattern}.*?{num_pattern}',
                rf'l[ií]nea de.*?{num_pattern}.*?{num_pattern}.*?a.*?{num_pattern}.*?{num_pattern}'
            ],
            "extract": lambda g: {"x1": float(g[0]), "y1": float(g[1]), "x2": float(g[2]), "y2": float(g[3])}
        },
        {
            "command": "create_point",
            "patterns": [
                rf'punto.*?{num_pattern}.*?{num_pattern}'
            ],
            "extract": lambda g: {"x": float(g[0]), "y": float(g[1])}
        },
        {
            "command": "create_polyline",
            "patterns": [
                r'polil[ií]nea(.*)',
                r'crear polil[ií]nea(.*)'
            ],
            "extract": lambda g: {
                "puntos": [
                    (float(p[0]), float(p[1])) 
                    for p in zip(re.findall(num_pattern, g[0])[0::2], re.findall(num_pattern, g[0])[1::2])
                ]
            }
        },
        {
            "command": "toggle_grid",
            "patterns": [r'mostrar cuadr[ií]cula', r'ocultar cuadr[ií]cula', r'alternar grilla', r'ver grilla', r'quitar fondo'],
            "extract": lambda g: {}
        },
        {
            "command": "stop_operation",
            "patterns": [r'detener', r'cancelar', r'parar', r'dejar de dibujar', r'escape'],
            "extract": lambda g: {}
        },
        {
            "command": "doc.redo()",
            "patterns": [r'rehacer l[oó]gica'],
            "extract": lambda g: {}
        },
        {
            "command": "doc.undo()",
            "patterns": [r'deshacer l[oó]gica'],
            "extract": lambda g: {}
        },
        {
            "command": "Gui.runCommand('Std_CloseActiveWindow')",
            "patterns": [r'cerrar proyecto'],
            "extract": lambda g: {}
        },
        {
            "command": "Gui.runCommand('Std_New')",
            "patterns": [r'nuevo proyecto'],
            "extract": lambda g: {}
        },
        {
            "command": "Gui.runCommand('Std_PrintPdf')",
            "patterns": [r'imprimir pdf\s*(.*)'],
            "extract": lambda g: {"target": g[0].strip()} if g and g[0].strip() else {}
        },
        {
            "command": "Gui.runCommand('Std_Print')",
            "patterns": [r'imprimir\s*(.*)'],
            "extract": lambda g: {"target": g[0].strip()} if g and g[0].strip() else {}
        },
        {
            "command": "Gui.runCommand('Std_Copy')",
            "patterns": [r'copiar\s*(.*)'],
            "extract": lambda g: {"target": g[0].strip()} if g and g[0].strip() else {}
        },
        {
            "command": "Gui.runCommand('Std_Cut')",
            "patterns": [r'cortar\s*(.*)'],
            "extract": lambda g: {"target": g[0].strip()} if g and g[0].strip() else {}
        },
        {
            "command": "Gui.runCommand('Std_Delete')",
            "patterns": [r'borrar\s*(.*)', r'eliminar\s*(.*)'],
            "extract": lambda g: {"target": g[0].strip()} if g and g[0].strip() else {}
        },
        {
            "command": "Gui.runCommand('Std_Open')",
            "patterns": [r'abrir\s*(.*)'],
            "extract": lambda g: {"target": g[0].strip()} if g and g[0].strip() else {}
        },
        {
            "command": "Gui.runCommand('Std_Paste')",
            "patterns": [r'pegar\s*(.*)'],
            "extract": lambda g: {"target": g[0].strip()} if g and g[0].strip() else {}
        },
        {
            "command": "Gui.runCommand('Std_Redo')",
            "patterns": [rf'rehacer\s*{num_pattern}', r'rehacer'],
            "extract": lambda g: {"steps": int(float(g[0]))} if g else {}
        },
        {
            "command": "Gui.runCommand('Std_Refresh')",
            "patterns": [r'refrescar', r'actualizar'],
            "extract": lambda g: {}
        },
        {
            "command": "Gui.runCommand('Std_SaveAs')",
            "patterns": [r'guardar como\s*(.*)'],
            "extract": lambda g: {"target": g[0].strip()} if g and g[0].strip() else {}
        },
        {
            "command": "Gui.runCommand('Std_Save')",
            "patterns": [r'guardar'],
            "extract": lambda g: {}
        },
        {
            "command": "Gui.runCommand('Std_SelectAll')",
            "patterns": [r'seleccionar todo'],
            "extract": lambda g: {}
        },
        {
            "command": "Gui.runCommand('Std_TextDocument')",
            "patterns": [r'crear nota'],
            "extract": lambda g: {}
        },
        {
            "command": "Gui.runCommand('Std_Undo')",
            "patterns": [rf'deshacer\s*{num_pattern}', r'deshacer'],
            "extract": lambda g: {"steps": int(float(g[0]))} if g else {}
        },
        {
            "command": "Gui.runCommand('Std_ViewScreenShot')",
            "patterns": [r'captura de pantalla'],
            "extract": lambda g: {}
        }
    ]

    for config in commands_config:
        for pattern in config["patterns"]:
            match = re.search(pattern, text)
            if match:
                try:
                    params = config["extract"](match.groups())
                    if config["command"] == "create_polyline":
                        if len(params.get("puntos", [])) < 2:
                            return {"success": False, "command": config["command"], "parameters": None, "error": "Faltan parámetros"}
                    return {"success": True, "command": config["command"], "parameters": params, "error": None}
                except (ValueError, IndexError):
                    return {"success": False, "command": config["command"], "parameters": None, "error": "Faltan parámetros"}
                    
    return {"success": False, "command": None, "parameters": None, "error": "Comando no reconocido"}

def command_record_signature(record: dict):
    if record.get("kind") == "parsed_command":
        params = record.get("parameters") or {}
        return ("parsed_command", record.get("label"), str(params))
    if record.get("kind") == "sketch_line":
        return ("sketch_line", round(record["length_mm"], 4))
    if record.get("kind") == "dynamic_command":
        return ("dynamic_command", record.get("label"), tuple(record.get("args", [])))
    return ("phrase_command", record.get("label"), record.get("script", ""))


def collect_command_records(text: str, phrase_rules, dynamic_rules=None) -> list:
    """Interpreta texto (parcial o final) y devuelve 0..n comandos con parámetros."""
    found = []
    
    parsed = parseVoiceCommand(text)
    if parsed.get("success"):
        found.append({
            "kind": "parsed_command",
            "label": parsed["command"],
            "parameters": parsed["parameters"]
        })
        return found

    length_mm = try_parse_sketch_line_length_mm(text)
    if length_mm is not None and length_mm > 0:
        found.append(
            {
                "kind": "sketch_line",
                "length_mm": length_mm,
                "axis": "x",
                "from_origin": True,
            }
        )
    
    # Try dynamic rules first
    if dynamic_rules:
        normalized_text = command_parser.fold_accents(text.lower())
        for rule in dynamic_rules:
            for regex in rule['regexes']:
                match = regex.search(normalized_text)
                if match:
                    args = list(match.groups())
                    script_with_args = command_parser.inject_args_to_script(rule['script_template'], args)
                    found.append({
                        "kind": "dynamic_command",
                        "label": rule['name'],
                        "script": script_with_args,
                        "args": args
                    })
                    return found

    hit = match_voice_phrase_script(text, phrase_rules)
    if hit:
        script, label = hit
        found.append({"kind": "phrase_command", "label": label, "script": script})
    return found


def append_commands_jsonl(path: Path, records: list, source: str, raw_text: str):
    ts = time.time()
    ts_iso = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(ts))
    with open(path, "a", encoding="utf-8") as handle:
        for record in records:
            row = {
                **record,
                "source": source,
                "raw_text": raw_text,
                "ts": ts,
                "ts_iso": ts_iso,
            }
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def maybe_log_voice_commands(
    text: str, phrase_rules, dynamic_rules, commands_path: Path, log_state: dict, source: str
) -> bool:
    """
    Si el texto coincide con comandos configurados, los agrega al JSONL.
    En parciales evita repetir la misma detección en cada frame; en final
    no duplica si ya se registró el mismo paquete en el parcial del mismo enunciado.
    """
    text = (text or "").strip()
    if not text:
        if source == "partial":
            log_state["partial_bundle_sig"] = None
        return False
    records = collect_command_records(text, phrase_rules, dynamic_rules)
    if not records:
        return False
    bundle_sig = tuple(command_record_signature(rec) for rec in records)
    if source == "partial":
        if log_state.get("partial_bundle_sig") == bundle_sig:
            return True
        log_state["partial_bundle_sig"] = bundle_sig
    elif source == "final":
        if log_state.get("partial_bundle_sig") == bundle_sig:
            log_state["partial_bundle_sig"] = None
            return True
        log_state["partial_bundle_sig"] = None
    append_commands_jsonl(commands_path, records, source, text)
    for rec in records:
        if rec["kind"] == "sketch_line":
            print(
                f"[{source}] Comando: línea {rec['length_mm']:g} mm → {commands_path.name}",
                flush=True,
            )
        else:
            print(
                f"[{source}] Comando: {rec['label']} → {commands_path.name}",
                flush=True,
            )
    return True


def process_final_transcript(
    text: str, transcript_lines: list, phrase_rules, dynamic_rules, commands_path: Path, log_state: dict
) -> bool:
    """
    Procesa texto final de Vosk. 
    Se transcribe inmediatamente a archivo y luego se verifica si es comando.
    """
    print(f"Final: {text}")
    # Guardamos la transcripción inmediatamente
    with open(OUTPUT_FILE, "a", encoding="utf-8") as file_handle:
        file_handle.write(text + "\n")
        file_handle.flush()
        import os
        os.fsync(file_handle.fileno())

    command = match_command(text)
    if command:
        message = execute_command(command)
        if message:
            print(message)
        return True
    
    if maybe_log_voice_commands(text, phrase_rules, dynamic_rules, commands_path, log_state, "final"):
        return True
        
    return False


def match_command(text: str):
    normalized = normalize_command_text(text)
    if normalized in ("listar comandos", "mostrar comandos", "comandos"):
        return "list"
    if normalized in ("salir", "terminar", "cerrar"):
        return "exit"
    for command, path in COMMAND_FOLDER_MAP.items():
        if normalize_command_text(command) in normalized:
            return path
    return None


def execute_command(command):
    if command == "list":
        print("Comandos disponibles:")
        for command_name in COMMAND_FOLDER_MAP:
            print(f"- {command_name}")
        print("- listar comandos")
        print("- salir")
        print('- ejemplo: "crear una línea de veinte centímetros" → se guarda en comandos_reconocidos.jsonl')
        print("- más frases: editá voice_phrases.json (frases → script de referencia)")
        return "Listado mostrado."
    if command == "exit":
        raise KeyboardInterrupt
    if isinstance(command, Path):
        if not command.exists():
            return f"No se encontró la carpeta: {command}"
        subprocess.Popen(["explorer", str(command)], shell=False)
        return f"Abriendo carpeta: {command.name}"
    return None


def main():
    model_path = choose_model_path()
    if not model_path:
        print_missing_models_help()
        return

    print(f"Cargando modelo Vosk desde '{model_path}'...")
    try:
        model = vosk.Model(model_path)
    except Exception as error:
        print(f"No se pudo cargar el modelo: {error}")
        return

    recognizer = vosk.KaldiRecognizer(model, DEFAULT_SAMPLE_RATE)
    recognizer.SetWords(True)

    print("Cargando RNNoise...")
    try:
        denoiser = RNNoise(sample_rate=RNNOISE_SR)
    except Exception as error:
        print(f"No se pudo inicializar RNNoise: {error}")
        return

    audio_queue = queue.Queue()

    def audio_callback(indata, _frames, _time_info, status):
        if status:
            print(f"Error en callback: {status}", file=sys.stderr)
        audio_int16 = np.clip(indata[:, 0] * 32767, -32768, 32767).astype(np.int16)
        audio_queue.put(audio_int16.copy())

    transcript_lines = []

    phrase_rules = load_voice_phrase_rules()
    
    dynamic_dirs = [
        PROJECT_DIR / "RelevoDraftv4_JoaquinPoggio_7-5-26",
        PROJECT_DIR / "Relevo_Explorer_v2_Jesus_Serra_2026-05-08",
        PROJECT_DIR / "Relevamiento Sketcher Workbenchv2_Alex_30-04-2026.zip"
    ]
    dynamic_rules = command_parser.parse_commands_from_directories(dynamic_dirs)
    
    command_log_state = {"partial_bundle_sig": None}
    print(
        f"Comandos detectados (parciales y finales) → {COMMANDS_LOG_FILE.resolve()}"
    )
    if phrase_rules:
        print(f"Frases estáticas: {len(phrase_rules)} variantes.")
    if dynamic_rules:
        print(f"Comandos dinámicos desde .txt: {len(dynamic_rules)} reglas.")
    print("Iniciando captura de audio. Habla ahora…")
    try:
        with sd.InputStream(
            samplerate=DEFAULT_SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=CHUNK_SIZE,
            callback=audio_callback,
            latency="low",
        ):
            while True:
                audio_chunk = audio_queue.get()
                audio_clean = denoise_chunk(denoiser, audio_chunk)

                if recognizer.AcceptWaveform(audio_clean.tobytes()):
                    command_log_state["partial_bundle_sig"] = None
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        process_final_transcript(
                            text,
                            transcript_lines,
                            phrase_rules,
                            dynamic_rules,
                            COMMANDS_LOG_FILE,
                            command_log_state,
                        )
                else:
                    partial = json.loads(recognizer.PartialResult())
                    ptext = (partial.get("partial") or "").strip()
                    if ptext:
                        maybe_log_voice_commands(
                            ptext,
                            phrase_rules,
                            dynamic_rules,
                            COMMANDS_LOG_FILE,
                            command_log_state,
                            "partial",
                        )
                        print(f"Parcial: {ptext}", end="\r", flush=True)
                    else:
                        command_log_state["partial_bundle_sig"] = None
    except KeyboardInterrupt:
        print("\nPrograma finalizado.")
    except Exception as error:
        print(f"Error en captura de audio: {error}")
    finally:
        final_text = json.loads(recognizer.FinalResult()).get("text", "").strip()
        if final_text:
            process_final_transcript(
                final_text,
                transcript_lines,
                phrase_rules,
                dynamic_rules,
                COMMANDS_LOG_FILE,
                command_log_state,
            )
        print(f"Sesión finalizada. Las transcripciones fueron guardadas en: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()