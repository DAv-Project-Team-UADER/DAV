# Cómo probar y validar

Cómo comprobar que un cambio anda **antes** de mandarlo a revisión. Distintas
capas según lo que tocaste.

---

## 1. Prueba puramente técnica (rápida, sin FreeCAD)

Para código Python propio (prompts, pants, módulos), al menos:

### Sintaxis

```bash
# Windows (PowerShell)
python -c "import ast; ast.parse(open(r'<archivo>', encoding='utf-8').read()); print('OK')"
```

### Import / smoke test con el venv de desarrollo

El venv de desarrollo (`IntegracionGUI/GUIFreeCad/.venv`) tiene PySide6. Se
puede importar un módulo que no requiera FreeCAD en tiempo de import (si
importa `FreeCAD` arriba, usá import diferido dentro de las funciones — patrón
que usan los prompts).

### Lógica de prompts (sin abrir FreeCAD)

Los prompts heredan `BaseInputPrompt` y su lógica se puede probar llamando
`ProcessFinalText("...")` directamente con un `QApplication` offscreen:

```python
import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"
from InputPrompts.PlaneSelectionInputPrompt import PlaneSelectionInputPrompt
from PySide6.QtWidgets import QApplication
app = QApplication.instance() or QApplication([])

p = PlaneSelectionInputPrompt()
print(p.ProcessFinalText("abajo").Success)   # navega
print(p.ProcessFinalText("okey").Value)       # confirma → valor del plano
```

Requiere que `GUIFreeCad` esté en `sys.path` (o configurar la ruta).

---

## 2. Prueba de diccionarios / navegación

- **Cargar el dict maestro** no debe romper: si una carpeta tiene un dict roto,
  el `DictionaryLoader` lo omite y sigue (no tumba el motor).
- Verificá que las **frases nuevas aparecen** como opciones del contexto: en el
  panel, tras navegar al contexto, la ayuda/describir contexto listará los
  comandos disponibles (implícito en `Browser.DescribeContext`).
- Probá cada frase en los tres idiomas si agregaste traducciones.

---

## 3. Prueba integrada en FreeCAD (la que vale)

Corré el motor de voz dentro de FreeCAD (ver [setup](setup.md)) y probá el
flujo real por voz. Las guías existentes detallan qué esperar:

| Guía | Cubre |
|---|---|
| [guia-pruebas-partdesign-voz.md](../guia-pruebas-partdesign-voz.md) | PartDesign por voz con medidas dictadas (sólidos, extrusión, cortes, acabados) |
| [guia-pruebas-3d-voz.md](../guia-pruebas-3d-voz.md) | Flujo completo desde dibujo 2D y Assembly |
| [guia-prueba-numeros-alumnos.md](../guia-prueba-numeros-alumnos.md) | Dictado de números (cómo decir medidas) |
| [manual-selection-voz.md](../manual-selection-voz.md) | Selección de objetos por voz |
| [manual-explorer-voz.md](../manual-explorer-voz.md) | Explorer por voz (archivos) |
| [informe_pruebas_draftwork.md](../informe_pruebas_draftwork.md) | Reporte de pruebas del workbench Draft |

### Consejos de prueba

- **`donde estoy`** para ubicarte; **`subir`** para subir de nivel.
- Confirmar pop-ups: `enter` · `enviar` · `aceptar` · `confirmar` · `ok`.
  Abortar: `cancelar`.
- Si un comando "no se escucha", pensá en la **gramática acotada**: algunos
  prompts (numéricos, selector de plano) limitan qué palabras acepta Vosk a
  propósito (ver [acortador-gramatica-vosk.md](../acortador-gramatica-vosk.md)).

---

## 4. Correr los tests del proyecto

Hay infraestructura de tests/validación en `Dav/scr/validation/`:

- `test_validator.py` — pruebas del `Validator`.
- `test_integration.py` — pruebas de integración (incluye
  `PromptedCommandExecutor`).
- `run_tests.py` — correr los tests de la carpeta.
- `prueba_validator.py` — helper de prueba/validación.

```bash
python Dav/scr/validation/run_tests.py
```

> El `Validator` se integra a la ejecución de comandos vía
> `PromptedCommandExecutor` (validación previa de parámetros). Si tu comando
> toma parámetros, añadí cobertura en estas pruebas cuando corresponda.

---

## Checklist rápido antes de mandar el PR

- [ ] Sintaxis OK (AST parse) en archivos modificados/nuevos.
- [ ] No se aplanan subcontextos (`.update(sub_dict)`).
- [ ] Archivos nuevos con cabezal obligatorio.
- [ ] Docstrings en inglés para clases/métodos públicos.
- [ ] Frases probadas en los idiomas que toquen.
- [ ] Flujo real por voz probado en FreeCAD (si se puede).
- [ ] Actualizada la guía/doc si cambiaste una convención o un comportamiento.