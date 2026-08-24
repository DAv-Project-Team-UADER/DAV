# Diccionario Numbers — Entrada numérica por voz

> Implementación del recognition de números por voz para prompts paramétricos.

---

## Resumen

El sistema permite a Vosk reconocer números hablados (0-9, decimales, cifras compuestas) cuando FreeCAD pide un valor numérico al usuario. Se implementó:

1. **Diccionario `Dav/dic/Numbers/`** — palabras numéricas en español, inglés y portugués
2. **Gramática dinámica** — la gramática de Vosk cambia automáticamente al abrir/cerrar un prompt numérico
3. **Acumulación de texto** — permite decir un número y luego "ok" en frases separadas
4. **Fix del wrapper** — `create_by_points_with_objects` ahora reenvía parámetros

---

## Diagrama de flujo

```mermaid
sequenceDiagram
    participant U as Usuario (voz)
    participant V as Vosk
    participant D as DavVoiceService
    participant R as PromptVoiceRouter
    participant P as FloatInputPrompt
    participant S as SpokenNumberParser

    Note over V: Gramática CAD activa<br/>(comandos de navegación)

    U->>V: "create by points"
    V->>D: "create by points"
    D->>R: procesar_frase_final()
    R->>R: Browser.ProcessPhrase()
    R->>P: ParameterCollector crea prompt
    R->>D: SetActivePrompt(prompt)
    D->>V: set_grammar([cero, uno, ..., enviar, [unk]])
    Note over V: Gramática cambia a numérica

    U->>V: "cinco"
    V->>D: "cinco"
    D->>R: PromptVoiceRouter.ProcessVoiceText()
    R->>P: ProcessFinalText("cinco")
    P->>P: _AccumulatedText = "cinco"
    P-->>P: status: "Say a number, then say ok"

    U->>V: "ok"
    V->>D: "ok"
    D->>R: ProcessVoiceText()
    R->>P: ProcessFinalText("ok")
    P->>S: ParseFloat("cinco")
    S-->>P: 5.0
    P-->>P: AcceptValue(5.0)

    Note over V: Gramática vuelve a CAD
    D->>V: set_grammar(browser.GetSpokenPhrases())
```

---

## Diccionario Numbers

### Estructura de archivos

```
Dav/dic/Numbers/
├── __init__.py        # Paquete vacío
├── Numbers.py         # Sentinelas + get_numeric_grammar_phrases()
├── TraduceToEs.py     # Palabras en español
├── TraduceToEn.py     # Palabras en inglés
├── TraduceToPt.py     # Palabras en portugués
└── ayuda.py           # Texto de ayuda
```

### Sentinelas (`Numbers.py`)

Funciones sin-op que representan dígitos y separadores:

| Sentinelas | Valor |
|-----------|-------|
| `Zero`, `One`, ..., `Nine` | Dígitos 0-9 |
| `DecimalPoint`, `DecimalComma` | Separadores decimales |

### Traducciones

| Español | Inglés | Portugués | Sentinel |
|---------|--------|-----------|----------|
| cero | zero | zero | Zero |
| uno, un, una | one | um, uma | One |
| dos | two | dois, duas | Two |
| tres | three | três, tres | Three |
| cuatro | four | quatro | Four |
| cinco | five | cinco | Five |
| seis | six | seis | Six |
| siete | seven | sete | Seven |
| ocho | eight | oito | Eight |
| nueve | nine | nove | Nine |
| punto, decimal | point, decimal | ponto, decimal | DecimalPoint |
| coma | comma | vírgula, virgula | DecimalComma |

### `get_numeric_grammar_phrases()`

Construye la lista de frases para la gramática de Vosk durante input numérico:

1. Carga `TraduceToEs.py`, `TraduceToEn.py`, `TraduceToPt.py` via `importlib`
2. Agrega palabras de confirmación: `enviar`, `ok`, `send`, `enter`, etc.
3. Agrega palabras de cancelación: `cancelar`, `cancel`, etc.
4. Agrega `[unk]` (comodín de Vosk para ruido)

Total: **52 frases** en los 3 idiomas.

---

## Gramática dinámica

### Problema

Cuando un `IntegerInputPrompt` o `FloatInputPrompt` está activo, la gramática de Vosk solo contiene comandos de navegación. Palabras como "cinco" no están en la gramática, así que Vosk las descarta o las sustituye por palabras similares ("opciones").

### Solución

`PromptVoiceRouter` detecta prompts numéricos y cambia la gramática:

```
SetActivePrompt(prompt)
  → _IsNumericPrompt(prompt) = True
  → _ActivateNumericGrammar()
  → DavVoiceService.set_grammar(get_numeric_grammar_phrases())

ClearActivePrompt(prompt)
  → was_numeric = True
  → _RestoreCadGrammar()
  → DavVoiceService.set_grammar(browser.GetSpokenPhrases())
```

### Import path

`Dav/dic/` no está en `sys.path` por defecto. La solución agrega la ruta dinámicamente:

```python
dic_root = str(Path(__file__).resolve().parent.parent)
if dic_root not in sys.path:
    sys.path.insert(0, dic_root)
```

---

## Acumulación de texto (fix del Bug 2)

### Problema

Cuando el usuario decía "cinco" (frase final) y luego "ok" (frase final), el prompt reemplazaba el texto. El parser veía solo "ok" (sin número) y no confirmaba.

### Solución

`FloatInputPrompt` e `IntegerInputPrompt` acumulan texto en `_AccumulatedText`:

- **Número sin confirmación** → se acumula: `"cinco"` → `"cinco"`
- **Confirmación con número acumulado** → se parsea el acumulado y se limpia
- **Confirmación sin número** → "No value to confirm. Say a number first."
- **Cancelación** → se limpia el acumulado y se cierra

```python
def ProcessFinalText(self, Text):
    tokens = SpokenNumberParser.Tokenize(Text)

    if self._HasCancellation(tokens):
        self._AccumulatedText = ""
        return self.Cancel()

    if self._HasConfirmation(tokens):
        if not self._AccumulatedText:
            self.SetStatus("No value to confirm.")
            return self.GetResult()
        parse_text = self._AccumulatedText
        self._AccumulatedText = ""
        value = SpokenNumberParser.ParseFloat(parse_text)
        return self.AcceptValue(value)

    self._AccumulatedText = (
        (self._AccumulatedText + " " + Text).strip()
        if self._AccumulatedText else Text
    )
    return self.GetResult()
```

---

## Fix del wrapper (line.py)

### Problema

`create_by_points_with_objects()` no declaraba parámetros, entonces `ParameterCollector` no pedía nada y llamaba a `create_by_points()` sin argumentos.

### Solución

El wrapper ahora firma los mismos parámetros que la función original:

```python
# Antes (bug)
def create_by_points_with_objects():
    create_by_points()  # ← falla: missing 4 args

# Después (fix)
def create_by_points_with_objects(x1: float, y1: float, x2: float, y2: float, label: str = "Segment"):
    create_by_points(x1=x1, y1=y1, x2=x2, y2=y2, label=label)
```

---

## Diagrama de clases

```mermaid
classDiagram
    direction TB

    class PromptVoiceRouter {
        +SetActivePrompt(Prompt)$ void
        +ClearActivePrompt(Prompt)$ void
        +ProcessVoiceText(Text, Final)$ bool
        -_ActivateNumericGrammar()$ void
        -_RestoreCadGrammar()$ void
    }

    class BaseInputPrompt {
        +_AccumulatedText: str
        +ProcessPartialText(Text) void
        +ProcessFinalText(Text) PromptResult
        +AcceptValue(Value) PromptResult
        +Cancel() PromptResult
    }

    class FloatInputPrompt {
        +ProcessFinalText(Text) PromptResult
    }

    class IntegerInputPrompt {
        +ProcessFinalText(Text) PromptResult
    }

    class SpokenNumberParser {
        +DigitWords: dict$
        +ParseFloat(Phrase) float$
        +ParseInteger(Phrase) int$
        +Tokenize(Phrase) list~str~$
    }

    class Numbers {
        +get_numeric_grammar_phrases() list~str~$
    }

    class DavVoiceService {
        +set_grammar(phrases) void
    }

    FloatInputPrompt --|> BaseInputPrompt
    IntegerInputPrompt --|> BaseInputPrompt
    FloatInputPrompt --> SpokenNumberParser : usa
    IntegerInputPrompt --> SpokenNumberParser : usa
    PromptVoiceRouter --> DavVoiceService : cambia gramática
    PromptVoiceRouter --> Numbers : carga frases numéricas
    PromptVoiceRouter --> BaseInputPrompt : registra prompt activo
```

---

## Archivos modificados

| Archivo | Cambio |
|---------|--------|
| `Dav/dic/Numbers/*` | **Nuevo** — diccionario completo (6 archivos) |
| `InputPrompts/PromptVoiceRouter.py` | Grammar switching numérico |
| `InputPrompts/BaseInputPrompt.py` | `_AccumulatedText` |
| `InputPrompts/FloatInputPrompt.py` | Acumulación de texto |
| `InputPrompts/IntegerInputPrompt.py` | Acumulación de texto |
| `integration/browser_voice_adapter.py` | `_ActiveAdapter` global |
| `Workbench/Sketcher/Geometry/line/line.py` | Wrapper con parámetros |
