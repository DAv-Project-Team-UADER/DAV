# Test guide — Numeric input by voice

> For students: test the functions that receive numeric values by voice and detect errors.

---

## Setup

1. Open FreeCAD with the DAV project
2. Start the voice engine: DAV menu → "Iniciar voz DAV" (Start DAV voice) (or from the console: `from integration.voice_bootstrap import start_voice_engine; start_voice_engine()`)
3. Make sure the microphone works
4. Have a document open in FreeCAD

---

## Functions with numeric parameters

| # | Function | Dictionary path | Required numeric parameters | Languages |
|---|---------|---------------------|--------------------------------|---------|
| 1 | `create_by_points` | `Workbench/Sketcher/Geometry/line` | `x1: float`, `y1: float`, `x2: float`, `y2: float` (4 floats) | ES, PT |
| 2 | `pointatcoords` | `Workbench/DraftWork/pointplacement` | `x: float`, `y: float`, `z: float` (3 floats) | ES, EN, PT |
| 3 | `_create_line` | `Workbench/Part/line` | `x1: float`, `y1: float`, `z1: float`, `x2: float`, `y2: float`, `z2: float` (6 floats) | ES, EN, PT |
| 4 | `pad_sketch` | `Workbench/PartDesign/additive` | `length: float = 10.0` (has a default value, requires no input) | ES, EN, PT |

**Total: 13 required float parameters in 3 voice-navigable functions.**

---

## Test 1 — Sketcher Line (create by points)

### Voice navigation

Say in this order:

```
"workbench"
"sketcher"
"geometry"
"linea"
"linea por puntos"
```

### Values to enter

When the first prompt opens, say the number and then confirm:

| Prompt | Say | Confirm with | Expected value |
|--------|-------|---------------|----------------|
| #1 (x1) | **"uno"** (one) | **"enviar"** (send) | 1.0 |
| #2 (y1) | **"dos"** (two) | **"enviar"** | 2.0 |
| #3 (x2) | **"cinco"** (five) | **"enviar"** | 5.0 |
| #4 (y2) | **"tres"** (three) | **"enviar"** | 3.0 |

### Verification

- A line from **(1, 2)** to **(5, 3)** should be created in the XY plane
- Verify in FreeCAD: `App.ActiveDocument.Objects` should show a new object

---

## Test 2 — Draft Point (pointatcoords)

### Voice navigation

```
"workbench"
"draft"
"pointplacement"
"punto en coordenadas"
```

### Values to enter

| Prompt | Say | Confirm with | Expected value |
|--------|-------|---------------|----------------|
| #1 (x) | **"tres"** (three) | **"ok"** | 3.0 |
| #2 (y) | **"cuatro"** (four) | **"ok"** | 4.0 |
| #3 (z) | **"cero"** (zero) | **"ok"** | 0.0 |

### Verification

- A point should be created at coordinates **(3, 4, 0)**

---

## Test 3 — Part Line (_create_line)

### Voice navigation

```
"workbench"
"part"
"linea"
"linea"
```

### Values to enter

| Prompt | Say | Confirm with | Expected value |
|--------|-------|---------------|----------------|
| #1 (x1) | **"cero"** (zero) | **"enviar"** | 0.0 |
| #2 (y1) | **"cero"** | **"enviar"** | 0.0 |
| #3 (z1) | **"cero"** | **"enviar"** | 0.0 |
| #4 (x2) | **"diez"** (ten) | **"enviar"** | 10.0 |
| #5 (y2) | **"cinco"** (five) | **"enviar"** | 5.0 |
| #6 (z2) | **"cero"** | **"enviar"** | 0.0 |

### Verification

- A line from **(0, 0, 0)** to **(10, 5, 0)** should be created

---

## Special cases to test

Try these cases in any of the functions above:

| # | Case | What to do | Expected result |
|---|------|-----------|--------------------|
| 1 | **Decimal with point** | Say "tres punto cinco" (three point five) → "enviar" | Accepts 3.5 |
| 2 | **Decimal with comma** | Say "dos coma ocho" (two comma eight) → "enviar" | Accepts 2.8 |
| 3 | **Confirm with "ok"** | Say "ocho" (eight) → "ok" | Accepts 8.0 |
| 4 | **Cancel** | Say "cancelar" | Closes the prompt without accepting a value |
| 5 | **Only "ok"** | Say "ok" without saying a number first | Shows "No value to confirm" |
| 6 | **Compound number (11-19)** | Say "trece" (thirteen) → "enviar" | Accepts 13.0 |
| 6b | **Tens alone (20-90)** | Say "cuarenta" (forty) → "enviar" | Accepts 40.0 |
| 6c | **Tens + unit** | Say "treinta y dos" (thirty-two) → "enviar" | Accepts 32.0 (also try without the "y": "treinta dos") |
| 6d | **Spanish contraction (21-29)** | Say "veintidós" (twenty-two) → "enviar" | Accepts 22.0 |
| 6e | **Digit by digit (fallback)** | Say "uno" "uno" (one one) → "enviar" | Accepts 11.0 (still works as an alternative) |
| 6f | **Out of range (100+)** | Say "seiscientos cincuenta" (six hundred fifty) → "enviar" | NOT supported (current range: 0-99). "seiscientos" is not in the dictionary and is silently ignored: it gives **50**, not an error. Report it if this is surprising in the test |
| 7 | **Two utterances** | Say "cinco" (five) → "ok" | Accepts 5.0 (accumulates + confirms) |

---

## What to Observe

For each test, observe and note:

1. **Did the prompt open?** — The pop-up window asking for a value appears
2. **Was the number recognized?** — The text field shows what you said
3. **Did the confirmation work?** — Saying "enviar" or "ok" accepts the value
4. **Did it move on to the next parameter?** — The prompt for the next float opens
5. **Did the function run?** — The object is created in FreeCAD
6. **Is the object correct?** — Correct coordinates and shape

---

## Report format

Fill in one row for each function tested:

```
Function: _______________________
Voice command: _______________________

Did the prompt open?          YES / NO
Numbers recognized:           _______________
Numbers NOT recognized:       _______________
Did the function run?         YES / NO
Was the object created correctly? YES / NO

Errors observed:
_________________________________________________
_________________________________________________
```

---

## Known errors — what to look for

| Error message | Probable cause | Severity |
|-----------------|----------------|-----------|
| `"Command not executed: Collected parameters failed validation"` | The wrapper does not forward parameters to the function | High |
| `"No se pudo convertir 'x1' al tipo un número decimal"` (could not convert 'x1' to the type decimal number) | The numeric grammar did not load; Vosk is not listening for numbers | High |
| The number is replaced by another word (e.g. "ocho" → "opciones") | The grammar did not switch to numeric mode | High |
| `"ok" does not confirm the number** | The prompt replaces the text instead of accumulating it | Medium |
| The prompt does not appear | The command is not voice-navigable | High |
| Vosk does not recognize the number in any language | The word is not in the numeric grammar | Medium |
| `"Value cannot be empty"` | Confirmed without entering a number | Low |
| The function runs but does not create an object | Error in the function's implementation | High |

---

## Tips

- **Speak clearly and slowly** — Vosk works better with clear diction
- **Wait for the prompt to appear** — Do not speak before the window is visible
- **Say the number and the confirmation separately** — First "cinco", wait, then "enviar"
- **If a number is not recognized, repeat it** — Sometimes Vosk fails because of noise
- **Try all 3 languages if possible** — Change the language from the DAV preferences
