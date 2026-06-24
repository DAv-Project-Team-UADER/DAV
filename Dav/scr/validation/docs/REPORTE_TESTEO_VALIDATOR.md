# Reporte de Testeo — Validator (DAV)

| Campo | Valor |
|-------|-------|
| **Módulo** | `validation/Validator` |
| **Rama** | `Pruebas` |
| **Fecha de Pruebas** | 21 de Junio de 2026 |
| **Integrante(s)** | Benjamín Ayala |

---

## Introducción

Este documento detalla el procedimiento y los resultados de las pruebas realizadas sobre el módulo **Validator** en el asistente de voz DAV para FreeCAD. Se probó la integración del validador de tipos y precondiciones de FreeCAD como interfaz previa a la ejecución de comandos.

---

## Casos de Prueba (CP)

### CP-01 — Documento activo + demo automática

* **Acción ejecutada:** 
  1. Se creó un nuevo documento activo `App.newDocument("PruebaValidator")`.
  2. Se ejecutó la demo automática con `RunValidatorPrueba()`.
* **Resultado esperado:**
  * Se crea `LineaDemo`.
  * La llamada `additive` reporta error por falta del croquis "Sketch".
  * El caso `NoExiste` reporta error esperado.
* **Captura:**
  `![CP-01](images/testeo_local/CP-01.png)`
* **Estado:** `[x] OK  [ ] FAIL`
* **Observaciones:** 
  Ejecución exitosa de la demo automática en la consola de FreeCAD mediante `RunValidatorPrueba()`. Se generó la geometría de línea de prueba y se validaron los errores de croquis inexistente.

---

### CP-02 — Geometry OK (`MiLinea`)

* **Acción ejecutada:**
  1. Se ejecutó `CallIfValid` con coordenadas numéricas válidas para `create_by_points` en el diccionario `geometry.line`.
* **Resultado esperado:**
  * El objeto `MiLinea` se crea con éxito y es visible en el árbol de vista de FreeCAD.
* **Captura:**
  `![CP-02](images/testeo_local/CP-02.png)`
* **Estado:** `[x] OK  [ ] FAIL`
* **Observaciones:** 
  Creación exitosa de la línea `MiLinea` mediante coordenadas decimales válidas. El objeto se visualiza correctamente en el visor 3D y figura en el árbol.

---

### CP-03 — Geometry ERROR (tipo incorrecto)

* **Acción ejecutada:**
  1. Se envió un valor de tipo texto (`"hola"`) al parámetro `x1` que requiere un valor de tipo numérico (`float`).
* **Resultado esperado:**
  * El validador detecta la incompatibilidad, cancela la ejecución para evitar que falle FreeCAD y muestra el mensaje de error de coerción en la consola. No se crea el objeto `Fail` en el árbol.
* **Captura:**
  `![CP-03](images/testeo_local/CP-03.png)`
* **Estado:** `[x] OK  [ ] FAIL`
* **Observaciones:** 
  El validador interceptó el tipo incorrecto de 'x1' ("hola" en lugar de flotante) e imprimió el error esperado: `No se pudo convertir 'x1' al tipo un número decimal.`. La creación fue bloqueada y no se generó ningún objeto en el árbol de FreeCAD.

---

### CP-04 — GetRequirements en tres idiomas (geometry)

* **Acción ejecutada:**
  1. Se consultó `GetRequirements` para español (`es`), inglés (`en`) y portugués (`pt`).
* **Resultado esperado:**
  * La consola imprime correctamente las descripciones de los tipos esperados para cada idioma (`Dato`, `Data`, `Dado`).
* **Captura:**
  `![CP-04](images/testeo_local/CP-04.png)`
* **Estado:** `[x] OK  [ ] FAIL`
* **Observaciones:** 
  Las solicitudes de requisitos de parámetros se listaron correctamente en español, inglés y portugués (ej. 'Dato1', 'Data1', 'Dado1'), demostrando la correcta localización del validador.

---

### CP-05 — Additive OK (con Sketch)

* **Acción ejecutada:**
  1. Se creó un croquis (`Sketch`) en el entorno de Sketcher.
  2. Se invocó la extrusión `pad_sketch` del diccionario `additive` con los parámetros correctos.
* **Resultado esperado:**
  * Se ejecuta el comando `Pad` correctamente y la consola confirma la acción.
* **Captura:**
  `![CP-05](images/testeo_local/CP-05.png)`
* **Estado:** `[x] OK  [ ] FAIL`
* **Observaciones:** 
  Se extruyó con éxito el Sketch (círculo) a un Pad de 25mm de alto usando `CallIfValid` sin reportar errores, confirmando el correcto funcionamiento en comandos que alteran el documento.

---

### CP-06 — Additive ERROR (objeto inexistente)

* **Acción ejecutada:**
  1. Se intentó extruir un croquis con nombre inexistente (`"NoExiste"`).
* **Resultado esperado:**
  * El validador detecta que el objeto no existe en el documento activo, cancela la ejecución del comando y muestra un error específico en la consola de FreeCAD.
* **Captura:**
  `![CP-06](images/testeo_local/CP-06.png)`
* **Estado:** `[x] OK  [ ] FAIL`
* **Observaciones:** 
  El validador interceptó el croquis inexistente 'NoExiste' y reportó correctamente: `El objeto 'NoExiste' no existe en el documento activo.`. La llamada no se ejecutó en FreeCAD, protegiendo al sistema de posibles crashes.

---

### CP-07 — Tests automáticos (opcional)

* **Acción ejecutada:**
  1. Ejecución del comando `python validation/run_tests.py` en la terminal del sistema.
* **Resultado esperado:**
  * Todas las 14 pruebas unitarias y de integración terminan de forma exitosa (`OK`).
* **Captura:**
  `![CP-07](images/testeo_local/CP-07.png)`
* **Estado:** `[x] OK  [ ] FAIL`
* **Observaciones:** 
  Las 14 pruebas automáticas de unidad e integración (ejecutadas con `run_tests.py`) pasaron exitosamente.

---

## Conclusión General

El módulo Validator cumple exitosamente con su propósito. Se comprobó la correcta validación de tipos básicos (enteros, decimales, textos) y precondiciones del documento activo (existencia de objetos) en tres idiomas diferentes (español, inglés y portugués). La integración en el asistente de voz de FreeCAD permite filtrar comandos con parámetros erróneos o inválidos antes de que sean enviados al motor de FreeCAD, previniendo fallos críticos en la GUI y mejorando la robustez y experiencia del usuario final.
