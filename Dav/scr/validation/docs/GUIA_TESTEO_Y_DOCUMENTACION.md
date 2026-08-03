# Guía de testeo y documentación — Validator (DAV)

**Rama:** `Pruebas`  
**Módulo:** `validation/`  
**Entrega:** lunes  

El **código ya está implementado y probado** por el equipo de integración. Esta guía es para que ustedes **repitan las pruebas en FreeCAD**, saquen **capturas** y armen el **Word + ticket de testeo**.

No hace falta modificar código salvo que encuentren un bug (avisar con captura de consola).

---

## 1. Preparación

### 1.1 Obtener el código

```bash
git pull origin Pruebas
```

### 1.2 Abrir FreeCAD con DAV

Doble clic en **`iniciar_dav.bat`** (raíz del repo).

### 1.3 Abrir la consola Python

En FreeCAD: **Ver → Paneles → Consola de Python**.

### 1.4 Crear documento de prueba

Siempre empezar con un documento activo:

```python
import FreeCAD as App
App.newDocument("PruebaValidator")
```

> **Error común:** `no active document` → ejecutar el comando de arriba antes de probar.

---

## 2. Qué es Validator (para el Word)

Clase en `validation/validator.py` con dos métodos principales:

| Método | Función |
|--------|---------|
| **`GetRequirements(idioma, funcion)`** | Usa `inspect` sobre la función del diccionario. Imprime y devuelve líneas como `Dato1: se espera un número decimal` en **es / en / pt**. |
| **`ValidateRequirements(idioma, funcion, datos)`** | Verifica que los datos del usuario sean correctos. Si falla, imprime el error y **no** ejecuta la función. |

Tipos soportados (consigna): **int, float, str, object** (objeto del documento FreeCAD).

Función extra útil: **`CallIfValid(...)`** — valida y, si todo está bien, llama a la función.

---

## 3. Diccionarios de prueba

| Diccionario | Comando | Qué prueba |
|-------------|---------|------------|
| `geometry.line` | `create_by_points` | Números (float) y texto (str) |
| `additive` | `pad_sketch` | Objeto del documento (Sketch) + float |

Archivos en repo:

- `DiccionariosEnBruto/Workbench/Sketcher/Geometry/line/`
- `DiccionariosEnBruto/Workbench/PartDesign/additive/`

---

## 4. Pruebas en consola — paso a paso

### 4.1 Demo automática (captura general)

```python
from scr.gui.dav_commands import RunValidatorPrueba
RunValidatorPrueba()
```

**Resultado esperado:**

| Bloque | Esperado |
|--------|----------|
| geometry (es, en, pt) | `Created 'LineaDemo' from (0.0,0.0) to (100.0,50.0)` |
| additive (sin Sketch) | `El objeto 'Sketch' no existe en el documento activo` (o equivalente en en/pt) |
| caso `NoExiste` | Error de objeto no encontrado |

📸 **Capturar:** consola completa de esta demo.

---

### 4.2 Geometry — caso OK

```python
from validator import Validator
from dictionary_resolver import GetDictionaryFunction

v = Validator()
fn = GetDictionaryFunction("geometry.line", "create_by_points")

v.GetRequirements("es", fn)

v.CallIfValid("es", fn, {
    "x1": 0, "y1": 0, "x2": 100, "y2": 50, "label": "MiLinea"
})
```

**Esperado:**

- Consola: `[geometry.line] Created 'MiLinea' from (0.0,0.0) to (100.0,50.0)`
- Árbol del documento: objeto `MiLinea`

📸 **Capturar:** consola + árbol con `MiLinea`.

---

### 4.3 Geometry — caso ERROR (tipo incorrecto)

```python
v.CallIfValid("es", fn, {
    "x1": "hola", "y1": 0, "x2": 100, "y2": 50, "label": "Fail"
})
```

**Esperado:**

- Consola: `No se pudo convertir 'x1' al tipo un número decimal.`
- **No** debe crearse `Fail` en el árbol.

📸 **Capturar:** solo consola con el mensaje de error.

---

### 4.4 GetRequirements en tres idiomas

```python
v.GetRequirements("es", fn)
v.GetRequirements("en", fn)
v.GetRequirements("pt", fn)
```

**Esperado:**

- Español: `Dato1`, `Dato2`…
- Inglés: `Data1`, `Data2`…
- Portugués: `Dado1`, `Dado2`…

📸 **Capturar:** las tres salidas en consola.

---

### 4.5 Additive — crear Sketch primero

1. Workbench **Sketcher**.
2. Crear sketch (cualquier figura simple).
3. Cerrar sketch (Finish).
4. Verificar nombre en consola:

```python
import FreeCAD as App
[obj.Name for obj in App.ActiveDocument.Objects if "Sketch" in obj.TypeId]
```

Debería listar algo como `['Sketch']`.

---

### 4.6 Additive — caso OK

```python
fn2 = GetDictionaryFunction("additive", "pad_sketch")

v.GetRequirements("es", fn2)

v.CallIfValid("es", fn2, {"sketch": "Sketch", "length": 10})
```

> Si el sketch tiene otro nombre (ej. `Sketch001`), usar ese nombre.

**Esperado:**

- Consola: `[additive] Pad on 'Sketch' length=10.0`
- Sketch seleccionado; puede abrirse diálogo de PartDesign Pad.

📸 **Capturar:** consola + vista con sketch seleccionado.

---

### 4.7 Additive — caso ERROR (objeto inexistente)

```python
v.CallIfValid("es", fn2, {"sketch": "NoExiste", "length": 10})
```

**Esperado:**

- Consola: `El objeto 'NoExiste' no existe en el documento activo.`
- No debe ejecutar Pad.

📸 **Capturar:** consola con el error.

---

### 4.8 GetRequirements additive en en / pt (opcional)

```python
v.GetRequirements("en", fn2)
v.GetRequirements("pt", fn2)
```

---

## 5. Tests automáticos (sin FreeCAD)

Desde la carpeta del repo, en PowerShell o CMD:

```bash
python validation/run_tests.py
```

**Esperado:** `Ran 12 tests` y `OK`.

📸 **Capturar:** salida del terminal (opcional en el Word).

---

## 6. Qué incluir en el documento Word

1. **Carátula:** materia, integrantes, fecha, rama `Pruebas`.
2. **Introducción:** objetivo de Validator y métodos `GetRequirements` / `ValidateRequirements`.
3. **Tabla de requisitos** (ejemplo):

   | Idioma | Dato | Tipo esperado |
   |--------|------|---------------|
   | es | Dato1 (geometry x1) | número decimal |
   | es | Dato5 (geometry label) | texto |
   | es | Dato1 (additive sketch) | objeto del documento |

4. **Procedimiento:** pasos que siguieron (resumen de esta guía).
5. **Capturas** de cada caso (OK y error).
6. **Conclusión:** qué funcionó, observaciones, limitaciones conocidas.

---

## 7. Ticket de testeo

Completar el archivo **`validation/docs/TICKET_TESTEO_VALIDATOR.md`** (marcar OK/FAIL y pegar capturas o referencias).

Subir el Word (`.docx` o `.pdf`) a:

```
validation/docs/
```

y commitear en rama `Pruebas`.

---

## 8. División sugerida (equipo de 4)

| Persona | Tarea |
|---------|--------|
| 1 | Geometry: casos OK + error + capturas |
| 2 | Additive: Sketch + OK + error + capturas |
| 3 | Idiomas (es/en/pt) + `run_tests.py` |
| 4 | Redactar Word, completar ticket, subir al repo |

---

## 9. Problemas frecuentes

| Mensaje | Solución |
|---------|----------|
| `no active document` | `App.newDocument("PruebaValidator")` |
| `El objeto 'Sketch' no existe` | Crear sketch en Sketcher o usar el nombre correcto |
| `No se pudo convertir 'x1'` | Comportamiento correcto — documentar como prueba de error |
| `ModuleNotFoundError: validator` | Abrir FreeCAD con `iniciar_dav.bat`, no FreeCAD suelto |

---

## 10. Contacto

Ante dudas o bugs: avisar al responsable de integración con **captura de consola completa**.
