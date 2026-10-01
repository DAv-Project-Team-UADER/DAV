# Agregar un diálogo de voz (prompt) y acotar su gramática

Un **prompt** es una ventana que hace una pregunta y se contesta hablando: un
número, una opción, un archivo, sí o no. Existe porque muchos diálogos nativos de
FreeCAD no se pueden manejar por voz, y porque algunos comandos necesitan valores
(«círculo» pide un radio).

Antes de escribir uno, mirá si ya hay uno que sirva: casi siempre alcanza con
**usar uno existente** (secciones 1 y 2). Escribir una clase nueva (sección 3) es el
último recurso.

---

## 1. Lo más simple: dejar que los parámetros se pidan solos

Si la función del diccionario **declara parámetros con tipo**, DAV los pide por voz
sin que escribas ningún diálogo. Lo hace
[`ParameterCollector`](../diagramas/ParameterCollector.md); el recorrido completo está
en [`FlujoComandoConParametros`](../diagramas/FlujoComandoConParametros.md).

```python
def makeCircle(radius: float) -> None:
    ...

draft = {'circle': makeCircle}
```

| Anotación | Prompt que se abre |
| --- | --- |
| `int` | número entero |
| `float` | número decimal |
| `str` | texto libre |
| cualquier otra / ninguna | selección de un objeto del documento |

Un parámetro **con valor por defecto no se pide**. Si la función no tiene parámetros
obligatorios no se abre nada.

---

## 2. Conversaciones a medida: los helpers de `Workbench/_prompts.py`

Cuando el comando necesita algo más que un valor suelto (elegir entre dos modos, un
objeto que cumpla una condición, una confirmación), usá los helpers. Ya registran el
prompt en el router, acotan la gramática y la restauran al terminar.

| Helper | Pregunta | Devuelve |
| --- | --- | --- |
| `askNumber(title, message)` | un número decimal | `float` o `None` |
| `askChoice(title, message, options)` | una opción entre pocas | la clave elegida o `None` |
| `askYesNo(title, message)` | sí / no | `True`, `False` o `None` |
| `askText(title, message)` | un texto deletreado | `str` o `None` |
| `askPlane()` | el plano base | `"XY"`, `"XZ"`, `"YZ"` o `None` |
| `askObject(doc, title, message, filter, emptyMessage)` | un objeto que cumpla `filter` | el objeto o `None` |
| `askSketch` / `askShape` / `askSolid` | atajos de `askObject` | el objeto o `None` |

**Todos devuelven `None` si el usuario cancela**: siempre comprobalo y salí sin hacer nada.

```python
from Workbench._prompts import askChoice, askNumber

mode = askChoice("Grabar", "Elegí el tipo", [
    ("emboss",  "Relieve",     ("relieve", "saliente")),
    ("engrave", "Perforación", ("perforación", "hundido")),
])
if mode is None:
    return
height = askNumber("Grabar", "Decí la altura en mm")
if height is None:
    return
```

Cada opción de `askChoice` es `(clave, texto que se ve, palabras que la eligen)`.

---

## 3. Una clase de prompt nueva

### Qué heredar

| Necesitás | Heredá de |
| --- | --- |
| Un valor libre (texto, número, objeto) | [`BaseInputPrompt`](../diagramas/BaseInputPrompt.md) |
| Un número dictado | [`NumericInputPrompt`](../diagramas/NumericInputPrompt.md): solo implementás `_ParseAccumulatedText` |
| Elegir entre pocas opciones con nombre | [`ChoiceInputPrompt`](../diagramas/ChoiceInputPrompt.md) |
| Elegir con otro vocabulario de navegación | subclase de `ChoiceInputPrompt` (ver [`ExampleChoiceInputPrompt`](../diagramas/ExampleChoiceInputPrompt.md)) |

### Esqueleto mínimo

```python
from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser

_COLORS = {"rojo": "red", "azul": "blue"}          # sin tildes


class ColorInputPrompt(BaseInputPrompt):
    """Prompt that picks a color by saying its name."""

    def GrammarPhrases(self, Language: str = "es") -> list[str]:
        """Return the words Vosk should listen for."""
        from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher

        return list(_COLORS) + PlaneGrammarSwitcher.PlanePhrases(Language)

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Accept a color name; cancelar aborts."""
        self.SetHeardText(Text)
        tokens = SpokenNumberParser.Tokenize(Text)   # normaliza tildes y mayúsculas
        if self._HasCancellation(tokens):
            return self.Cancel()
        for word, value in _COLORS.items():
            if word in tokens:
                return self.AcceptValue(value)
        self.SetStatus("No te entendí")
        return self.GetResult()
```

### Reglas

- **`ProcessFinalText` recibe la frase ya reconocida.** Comparala tokenizada con
  `SpokenNumberParser.Tokenize`, que quita tildes y pasa a minúsculas; escribí tus
  palabras **sin tildes**.
- **Cerrá siempre por un camino explícito:** `AcceptValue(valor)`, `Cancel()` o `Fail(msg)`
  (deja la ventana abierta para reintentar). No llames a `accept()` ni `close()` directo.
- **Aceptá cancelar siempre** con `_HasCancellation`, y confirmar con `_HasConfirmation`
  si el valor se dicta en varias frases.
- **Tres idiomas.** Si tenés palabras propias, definilas por idioma (`es`, `en`, `pt`) como
  hace `YesNoInputPrompt`, y aceptá las de los tres a la vez al comparar.
- **No importes `FreeCAD` a nivel de módulo** en `InputPrompts/`: hacelo dentro de las
  funciones, así el prompt se puede probar sin FreeCAD.
- **Docstrings en inglés, cabezal obligatorio**, y un diagrama en `docs/diagramas/`.

---

## 4. Acotar la gramática de Vosk

Con el vocabulario abierto, Vosk confunde las palabras cortas de navegación
(«abajo» por «trabajo»). Mientras el prompt está abierto se le da a Vosk **solo las
palabras que ese prompt entiende**. Fundamento y límites:
[`acortador-gramatica-vosk.md`](../acortador-gramatica-vosk.md).

### El patrón (copiarlo tal cual)

```python
from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher
from InputPrompts.PromptVoiceRouter import PromptVoiceRouter

prompt = ColorInputPrompt(Title="Color", Message="Decí el color")
PlaneGrammarSwitcher.ActivateGrammar(
    prompt.GrammarPhrases(PlaneGrammarSwitcher.CurrentLanguage())
)
PromptVoiceRouter.SetActivePrompt(prompt)
try:
    result = prompt.RequestValue()               # modal: devuelve al cerrarse
finally:
    PromptVoiceRouter.ClearActivePrompt(prompt)  # SIEMPRE, o el Browser queda sordo
    PlaneGrammarSwitcher.RestoreCadGrammar()     # vuelve la gramática de CAD

if result is None or result.Cancelled or not result.Success:
    return None
return result.Value
```

| Pieza | Para qué |
| --- | --- |
| `GrammarPhrases(Language)` | Lista de palabras que el prompt acepta, **en el idioma activo** |
| [`PlaneGrammarSwitcher.ActivateGrammar`](../diagramas/PlaneGrammarSwitcher.md) | Le da esa lista a Vosk |
| [`PromptVoiceRouter.SetActivePrompt`](../diagramas/PromptVoiceRouter.md) | Desvía lo que se dice al prompt en vez de al `Browser` |
| `try` / `finally` | Garantiza soltar el router y restaurar la gramática aunque falle algo |

### Qué palabras se pueden poner

- **Solo palabras que estén en el vocabulario del modelo de Vosk.** Las que no están
  (nombres de archivos, siglas raras) no se reconocen nunca; por eso el navegador de
  archivos recorre una lista en vez de pedir el nombre. Probá las palabras reales.
- **Incluí siempre confirmar y cancelar.** `PlaneGrammarSwitcher.PlanePhrases(idioma)` ya
  trae arriba/abajo, confirmar y cancelar.
- **Si una frase tiene varias palabras**, sumá también cada palabra suelta, para que se
  puedan decir por separado: `phrases.extend([frase, *frase.split()])`.
- **Prompts numéricos:** devolvé `True` en `RequiresNumericGrammar()`; el router cambia
  solo a la gramática de números y la restaura
  ([`NumericGrammarSwitcher`](../diagramas/NumericGrammarSwitcher.md)).

### Si el comando sigue después del diálogo (no modal)

`RequestValue()` bloquea hasta que se cierra la ventana. Si el usuario tiene que
**ver el modelo mientras contesta** (como en los ejemplos guiados), mostralo con
`Show()`, que no bloquea, y ocupate de tres cosas:

1. Guardar una **referencia** al prompt (si no, Qt lo recolecta).
2. Soltar el router al cerrarse: `prompt.finished.connect(lambda _c: PromptVoiceRouter.ClearActivePrompt(prompt))`.
3. Volver a acotar la gramática cada vez que cambian las palabras esperadas, y
   restaurarla en `done()`.

Modelo completo: [`GuidedExampleInputPrompt`](../diagramas/GuidedExampleInputPrompt.md).

---

## Checklist

- [ ] ¿Existe ya un prompt o helper que haga lo que necesito?
- [ ] Hereda de la clase base correcta y cierra con `AcceptValue` / `Cancel` / `Fail`.
- [ ] Acepta cancelar y las palabras en los tres idiomas.
- [ ] Gramática acotada con `ActivateGrammar` y restaurada en un `finally`.
- [ ] Router liberado en un `finally` (o en `finished` si no es modal).
- [ ] No importa `FreeCAD` a nivel de módulo.
- [ ] Probado sin micrófono (ver [probando.md](probando.md)) y con voz real.
- [ ] Diagrama en [`diagramas/`](../diagramas/README.md).

---

Anterior: [Agregar un submenú](agregar-submenu.md) · Siguiente: [Cómo probar y validar](probando.md)
