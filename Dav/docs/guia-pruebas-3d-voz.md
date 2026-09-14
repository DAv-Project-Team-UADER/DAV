# Guía de pruebas — de un cuadrado a un ensamblaje, por voz

Esta guía cubre lo agregado en los PR **#208**, **#209** y **#213**: crear
geometría dictando medidas, extruirla a 3D y unir piezas con juntas — todo sin
diálogos de FreeCAD.

Todas las frases de esta guía están tomadas de los diccionarios reales
(`Dav/dic/`). Ninguna es inventada.

---

## Antes de empezar

- Abrí FreeCAD con el panel DAV, idioma **español**.
- Tené un documento nuevo abierto.
- Si te perdés: decí **`donde estoy`** — lista el contexto actual y las
  opciones disponibles.
- Para subir un nivel: **`subir`** (también `volver`, `atras`).

**Confirmar un valor** (después de cada número):
`enter` · `enviar` · `aceptar` · `confirmar` · `ok`

**Abortar un pop-up**: `cancelar`

### Números: 0–99 se dicen normal, de 100 en adelante se deletrean

Se pronuncian natural hasta 99: 0–30 directos, más las decenas (40, 50, 60, 70,
80, 90) y los compuestos (`treinta y cinco`).

De 100 en adelante hay que **deletrear dígito por dígito**: `uno cero cero` da
100, `tres seis cero` da 360. Funciona, pero es incómodo — ver
[numeros-por-voz-limites-y-propuesta.md](numeros-por-voz-limites-y-propuesta.md).

Las pruebas de esta guía usan valores menores a 100 para que las frases suenen
naturales.

Otros modificadores:

| Para decir | Decí |
|---|---|
| −20 | `menos veinte` |
| 12,5 | `doce coma cinco` |

---

## Cómo reportar

Para cada prueba anotá:

1. **Qué dijiste** (la frase exacta).
2. **Qué salió en el Report View** — todos los comandos imprimen ahí, tanto el
   éxito como el error.
3. **Si el objeto apareció en el árbol** del panel DAV.

---

## Prueba 1 — Cubo directo

La más rápida. Confirma que la navegación, el pop-up y los números funcionan.

| Decí | Qué pasa |
|---|---|
| `banco de trabajo` | entra a los workbenches |
| `diseño de pieza` | entra a PartDesign |
| `aditivo` | entra a las operaciones aditivas |
| `caja por medidas` | **abre el pop-up** |
| `veinte enter` | largo |
| `veinte enter` | ancho |
| `veinte enter` | alto |

**Esperado**: un cubo de 20×20×20 y en el Report View:
`[additive] Created box 20 x 20 x 20`

> Si esta prueba falla, el problema es la navegación o el reconocimiento de
> números. No sigas con las demás hasta resolverlo.

---

## Prueba 2 — Cilindro

Desde `aditivo`:

| Decí | Qué pasa |
|---|---|
| `cilindro por medidas` | abre el pop-up |
| `diez enter` | radio |
| `cuarenta enter` | altura |

**Esperado**: cilindro r=10, h=40.

---

## Prueba 3 — El flujo completo: cuadrado → cubo

**Ésta es la prueba principal.** Cierra el camino 2D → 3D sin mouse.

### Paso A — dibujar el cuadrado

| Decí | Qué pasa |
|---|---|
| `banco de trabajo` | |
| `croquis` | entra a Sketcher |
| `geometria` | entra a las geometrías |
| `rectangulo` | entra al submenú rectángulo |
| `rectangulo por esquinas` | **abre el pop-up** |
| `cero enter` | x1 |
| `cero enter` | y1 |
| `veinte enter` | x2 |
| `veinte enter` | y2 |

**Esperado**: cuadrado de 20×20 y
`[geometry.rectangle] Created 'Rectangle' from (0,0) to (20,20)`

### Paso B — seleccionarlo

Hacé clic en el rectángulo (en el árbol de objetos o en la vista 3D).

> Este paso **todavía necesita mouse**. La selección por voz existe, pero es
> otro flujo.

### Paso C — extruirlo

| Decí | Qué pasa |
|---|---|
| `subir` (hasta el nivel de workbench) | |
| `diseño de pieza` | |
| `aditivo` | |
| `extruir por medida` | **abre el pop-up** |
| `treinta enter` | altura |

**Esperado**: el cuadrado se convierte en un prisma de 20×20×30 y
`[additive] Padded '...' by 30`

> **El paso más importante de probar.** Internamente el cuadrado (un
> `Part::Feature`) se convierte a croquis para poder extruirse. Esa conversión
> sólo se validó con stubs, nunca dentro de FreeCAD.

---

## Prueba 4 — Revolución

Con un perfil 2D seleccionado, desde `aditivo`:

| Decí | Qué pasa |
|---|---|
| `revolucion por angulo` | abre el pop-up |
| `noventa enter` | ángulo en grados |

**Esperado**: sólido de revolución de 90°.

---

## Prueba 5 — Otras geometrías 2D

Desde `croquis` → `geometria`:

| Figura | Decí | Valores de ejemplo |
|---|---|---|
| Círculo | `circulo` → `circulo por centro` | `cero` / `cero` / `veinticinco` |
| Arco | `arco` → `arco por centro` | `cero` / `cero` / `veinticinco` / `cero` / `noventa` |
| Elipse | `elipse` → `elipse por centro` | `cero` / `cero` / `cuarenta` / `veinte` |
| Polígono | `poligono` → `poligono por lados` | `seis` / `cero` / `cero` / `veinticinco` |
| Línea | `linea` → `linea por puntos` | `cero` / `cero` / `treinta` / `treinta` |

---

## Prueba 6 — Ensamblaje con juntas

| Decí | Qué pasa |
|---|---|
| `banco de trabajo` | |
| `ensamblaje` | entra a Assembly |
| `crear ensamblaje` | crea el ensamblaje |
| `insertar pieza` | inserta una pieza (repetir para tener dos) |

Con **una pieza** seleccionada:

| Decí | Esperado |
|---|---|
| `anclar pieza` | `[assembly] Grounded '...'` |

Con **dos piezas** seleccionadas:

| Decí | Luego | Esperado |
|---|---|---|
| `junta por distancia` | `veinticinco enter` | `Held '...' and '...' 25 apart` |
| `junta por angulo` | `noventa enter` | `Held '...' and '...' at 90 degrees` |
| `ensamble fijo` | — | `Fixed '...' to '...'` |
| `bisagra` | — | `Hinged '...' to '...'` |
| `junta deslizante` | — | `Slider between '...' and '...'` |

**Juntas sin medidas** (dos piezas seleccionadas):

| Decí | Qué hace |
|---|---|
| `rotula` | libre en cualquier rotación |
| `junta cilindrica` | gira y desliza sobre un eje |
| `junta paralela` | mantiene las piezas paralelas |
| `junta perpendicular` | mantiene las piezas en ángulo recto |

**Juntas de transmisión** (dos piezas seleccionadas, piden radios):

| Decí | Luego | Qué hace |
|---|---|---|
| `junta de engranajes` | `veinte` / `diez` | engrana con esa relación |
| `junta de correa` | `treinta` / `quince` | poleas unidas por correa |
| `junta de tornillo` | `cinco` | avance de rosca |
| `junta de cremallera` | `diez` | cremallera y piñón |

Para verificar que el solver corre: `resolver ensamblaje`.

> Seleccionar las piezas todavía necesita mouse; las juntas en sí ya no.

---

## Prueba 7 — Que los errores avisen

Estas rutas están implementadas pero **no se probaron dentro de FreeCAD**.
Confirmá que el mensaje sale en el Report View:

| Prueba | Cómo | Mensaje esperado |
|---|---|---|
| Radio cero | `circulo por centro` → `cero`/`cero`/`cero` | `radius must be greater than zero` |
| Polígono imposible | `poligono por lados` → `dos` | `a polygon needs at least 3 sides` |
| Caja con lado cero | `caja por medidas` → `veinte`/`cero`/`veinte` | `every dimension must be greater than zero` |
| Junta sin selección | `ensamble fijo` sin seleccionar nada | `select two parts to join first` |
| Cancelar | en cualquier pop-up decí `cancelar` | `Command cancelled by user` |
| Negativos | `menos veinte enter` | acepta −20 |
| Decimales | `doce coma cinco enter` | acepta 12,5 |

---

## Prueba 8 — El bug del árbol de objetos

Verifica una corrección puntual: antes, las elipses y polígonos creados por voz
**no aparecían en el árbol** del panel DAV.

1. Creá una **elipse** (prueba 5).
2. Creá un **polígono**.
3. Mirá el árbol de objetos del panel DAV.

**Esperado**: ambos figuran en el árbol. Si no aparecen, el arreglo no funcionó.

---

## Prueba 9 — Los otros idiomas

Tres módulos tenían diccionarios que fallaban en silencio: el loader aísla el
módulo roto y sigue con mapa vacío, así que las frases simplemente no
respondían, sin ningún error visible.

Cambiá el idioma del panel y probá que respondan:

| Idioma | Frase | Debería |
|---|---|---|
| Inglés | `box by size` | abrir el pop-up de la caja |
| Inglés | `line by points` | abrir el pop-up de la línea |
| Portugués | `caixa por medidas` | abrir el pop-up de la caja |
| Portugués | `junta fixa` | crear una junta fija |

Las de PartDesign en inglés y **todo Assembly en portugués** estaban caídos
antes de estos cambios.

---

## Dónde es más probable que falle

Nada de esto se ejecutó dentro de FreeCAD: se validó con stubs, que confirman
el ruteo de las frases, la matemática y que los valores dictados llegan a las
propiedades correctas — pero no la interacción con FreeCAD vivo.

Los tres puntos de mayor riesgo:

1. **Paso C de la prueba 3** — la conversión de cuadrado a croquis.
   `addGeometry` con curvas reales puede comportarse distinto que con el stub.
2. **Las juntas de la prueba 6** — se usa `Vertex1` de cada pieza como punto de
   anclaje por defecto; con formas complejas puede no ser el punto esperado.
3. **La cadena de navegación completa** — que
   `banco de trabajo` → `diseño de pieza` → `aditivo` funcione de corrido con
   el reconocimiento de voz real, no sólo en el diccionario.
