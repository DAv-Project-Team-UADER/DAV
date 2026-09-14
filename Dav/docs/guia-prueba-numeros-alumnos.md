# Guía de pruebas — Entrada numérica por voz

> Para alumnos: testear las funciones que reciben valores numéricos por voz y detectar errores.

---

## Preparación

1. Abrir FreeCAD con el proyecto DAV
2. Iniciar el motor de voz: menú DAV → "Iniciar voz DAV" (o desde consola: `from integration.voice_bootstrap import start_voice_engine; start_voice_engine()`)
3. Asegurarse de que el micrófono funcione
4. Tener un documento abierto en FreeCAD

---

## Funciones con parámetros numéricos

| # | Función | Ruta del diccionario | Parámetros numéricos requeridos | Idiomas |
|---|---------|---------------------|--------------------------------|---------|
| 1 | `create_by_points` | `Workbench/Sketcher/Geometry/line` | `x1: float`, `y1: float`, `x2: float`, `y2: float` (4 floats) | ES, PT |
| 2 | `pointatcoords` | `Workbench/DraftWork/pointplacement` | `x: float`, `y: float`, `z: float` (3 floats) | ES, EN, PT |
| 3 | `_create_line` | `Workbench/Part/line` | `x1: float`, `y1: float`, `z1: float`, `x2: float`, `y2: float`, `z2: float` (6 floats) | ES, EN, PT |
| 4 | `pad_sketch` | `Workbench/PartDesign/additive` | `length: float = 10.0` (tiene valor por defecto, no requiere input) | ES, EN, PT |

**Total: 13 parámetros float requeridos en 3 funciones navegables por voz.**

---

## Prueba 1 — Sketcher Line (create by points)

### Navegación por voz

Decir en este orden:

```
"workbench"
"sketcher"
"geometry"
"linea"
"linea por puntos"
```

### Valores a ingresar

Cuando se abra el primer prompt, decir el número y luego confirmar:

| Prompt | Decir | Confirmar con | Valor esperado |
|--------|-------|---------------|----------------|
| #1 (x1) | **"uno"** | **"enviar"** | 1.0 |
| #2 (y1) | **"dos"** | **"enviar"** | 2.0 |
| #3 (x2) | **"cinco"** | **"enviar"** | 5.0 |
| #4 (y2) | **"tres"** | **"enviar"** | 3.0 |

### Verificación

- Debería crearse una línea de **(1, 2)** a **(5, 3)** en el plano XY
- Verificar en FreeCAD: `App.ActiveDocument.Objects` debería mostrar un objeto nuevo

---

## Prueba 2 — Draft Point (pointatcoords)

### Navegación por voz

```
"workbench"
"draft"
"pointplacement"
"punto en coordenadas"
```

### Valores a ingresar

| Prompt | Decir | Confirmar con | Valor esperado |
|--------|-------|---------------|----------------|
| #1 (x) | **"tres"** | **"ok"** | 3.0 |
| #2 (y) | **"cuatro"** | **"ok"** | 4.0 |
| #3 (z) | **"cero"** | **"ok"** | 0.0 |

### Verificación

- Debería crearse un punto en las coordenadas **(3, 4, 0)**

---

## Prueba 3 — Part Line (_create_line)

### Navegación por voz

```
"workbench"
"part"
"linea"
"linea"
```

### Valores a ingresar

| Prompt | Decir | Confirmar con | Valor esperado |
|--------|-------|---------------|----------------|
| #1 (x1) | **"cero"** | **"enviar"** | 0.0 |
| #2 (y1) | **"cero"** | **"enviar"** | 0.0 |
| #3 (z1) | **"cero"** | **"enviar"** | 0.0 |
| #4 (x2) | **"diez"** | **"enviar"** | 10.0 |
| #5 (y2) | **"cinco"** | **"enviar"** | 5.0 |
| #6 (z2) | **"cero"** | **"enviar"** | 0.0 |

### Verificación

- Debería crearse una línea de **(0, 0, 0)** a **(10, 5, 0)**

---

## Casos especiales probar

Probar estos casos en cualquiera de las funciones anteriores:

| # | Caso | Qué hacer | Resultado esperado |
|---|------|-----------|--------------------|
| 1 | **Decimal con punto** | Decir "tres punto cinco" → "enviar" | Acepta 3.5 |
| 2 | **Decimal con coma** | Decir "dos coma ocho" → "enviar" | Acepta 2.8 |
| 3 | **Confirmar con "ok"** | Decir "ocho" → "ok" | Acepta 8.0 |
| 4 | **Cancelar** | Decir "cancelar" | Cierra el prompt sin aceptar valor |
| 5 | **Solo "ok"** | Decir "ok" sin decir número antes | Muestra "No value to confirm" |
| 6 | **Número compuesto (11-19)** | Decir "trece" → "enviar" | Acepta 13.0 |
| 6b | **Decena sola (20-90)** | Decir "cuarenta" → "enviar" | Acepta 40.0 |
| 6c | **Decena + unidad** | Decir "treinta y dos" → "enviar" | Acepta 32.0 (probar también sin el "y": "treinta dos") |
| 6d | **Contracción española (21-29)** | Decir "veintidós" → "enviar" | Acepta 22.0 |
| 6e | **Dígito a dígito (respaldo)** | Decir "uno" "uno" → "enviar" | Acepta 11.0 (sigue funcionando como alternativa) |
| 6f | **Fuera de rango (100+)** | Decir "seiscientos cincuenta" → "enviar" | NO soportado (rango actual: 0-99). "seiscientos" no está en el diccionario y se ignora en silencio: da **50**, no un error. Reportar si esto sorprende en la prueba |
| 7 | **Dos utterances** | Decir "cinco" → "ok" | Acepta 5.0 (acumula + confirma) |

---

## QuéObservar

Para cada prueba, observar y anotar:

1. **¿El prompt se abrió?** — Aparece la ventana emergente pidiendo valor
2. **¿El número se reconoció?** — El campo de texto muestra lo que dijiste
3. **¿La confirmación funcionó?** — Al decir "enviar" o "ok" se acepta el valor
4. **¿Pasó al siguiente parámetro?** — Se abre el prompt para el siguiente float
5. **¿La función se ejecutó?** — Se crea el objeto en FreeCAD
6. **¿El objeto es correcto?** — Coordenadas y forma correctas

---

## Formato de reporte

Llenar una fila por cada función probada:

```
Función: _______________________
Comando de voz: _______________________

¿Se abrió el prompt?          SÍ / NO
Números reconocidos:          _______________
Números NO reconocidos:       _______________
¿Se ejecutó la función?       SÍ / NO
¿El objeto se creó correctamente? SÍ / NO

Errores observados:
_________________________________________________
_________________________________________________
```

---

## Errores conocidos — qué buscar

| Mensaje de error | Causa probable | Severidad |
|-----------------|----------------|-----------|
| `"Command not executed: Collected parameters failed validation"` | El wrapper no reenvía parámetros a la función | Alta |
| `"No se pudo convertir 'x1' al tipo un número decimal"` | La gramática numérica no se cargó; Vosk no escucha números | Alta |
| El número se reemplaza por otra palabra (ej: "ocho" → "opciones") | La gramática no cambió a modo numérico | Alta |
| `"ok" no confirma el número** | El prompt reemplaza el texto en vez de acumularlo | Media |
| El prompt no aparece | El comando no está navegável por voz | Alta |
| Vosk no reconoce el número en ningún idioma | La palabra no está en la gramática numérica | Media |
| `"Value cannot be empty"` | Se confirmó sin ingresar número | Baja |
| La función ejecuta pero no crea objeto | Error en la implementación de la función | Alta |

---

## Consejos

- **Hablar claro y pausado** — Vosk funciona mejor con dicción clara
- **Esperar a que aparezca el prompt** — No hablar antes de que la ventana esté visible
- **Decir número y confirmación por separado** — Primero "cinco", esperar, luego "enviar"
- **Si un número no se reconoce, repetirlo** — A veces Vosk falla por ruido
- **Probar con los 3 idiomas** si es posible — Cambiar idioma desde preferencias DAV
