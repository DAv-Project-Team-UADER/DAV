# Guía de pruebas — PartDesign por voz

Cubre los comandos de PartDesign que aceptan **medidas dictadas**: crear sólidos,
extruir perfiles, cortarlos y darles acabado, sin abrir los diálogos de FreeCAD.

Todas las frases están tomadas de los diccionarios reales (`Dav/dic/`).

Para el flujo completo desde el dibujo 2D y para Assembly, ver
[guia-pruebas-3d-voz.md](../guias/guia-pruebas-3d-voz.md).

---

## Antes de empezar

- FreeCAD con el panel DAV, idioma **español**, documento nuevo abierto.
- Si te perdés: **`donde estoy`**. Para subir un nivel: **`subir`**.
- **Confirmar un valor**: `enter` · `enviar` · `aceptar` · `confirmar` · `ok`
- **Abortar un pop-up**: `cancelar`

### Números: 0–99 se dicen normal, de 100 en adelante se deletrean

Se pronuncian natural hasta 99: 0–30 directos, más las decenas (40, 50, 60, 70,
80, 90) y los compuestos (`treinta y cinco`).

De 100 en adelante hay que **deletrear**: `uno cero cero` da 100. Ver
[numeros-por-voz-limites-y-propuesta.md](../referencia/numeros-por-voz-limites-y-propuesta.md).

| Para decir | Decí |
|---|---|
| −20 | `menos veinte` |
| 12,5 | `doce coma cinco` |

### Cómo llegar

Todas las pruebas arrancan con:

```
banco de trabajo → diseño de pieza
```

Y desde ahí se entra a `aditivo`, `sustractivo` o `modificar`.

---

## Qué esperar de cada comando

| Categoría | Comando de voz | Prompts | Qué hace |
|---|---|---|---|
| Aditivo | `caja por medidas` | 3 | caja / cubo |
| Aditivo | `cilindro por medidas` | 2 | cilindro |
| Aditivo | `extruir por medida` | 1 | perfil → sólido |
| Aditivo | `revolucion por angulo` | 1 | perfil → revolución |
| Aditivo | `esfera por radio` | 1 | esfera |
| Aditivo | `cono por medidas` | 3 | cono / tronco |
| Aditivo | `toro por medidas` | 2 | toro |
| Aditivo | `prisma por medidas` | 3 | prisma regular |
| Sustractivo | `vaciado por medida` | 1 | hueco con forma del perfil |
| Sustractivo | `agujero por medidas` | 2 | agujero cilíndrico |
| Sustractivo | `ranura por angulo` | 1 | ranura por revolución |
| Sustractivo | `cortar caja por medidas` | 3 | resta una caja |
| Sustractivo | `cortar cilindro por medidas` | 2 | resta un cilindro |
| Sustractivo | `cortar esfera por radio` | 1 | resta una esfera |
| Modificar | `redondear por radio` | 1 | redondea todas las aristas |
| Modificar | `chaflan por medida` | 1 | achaflana todas las aristas |
| Modificar | `chaflan con angulo` | 2 | chaflán con ángulo propio |
| Modificar | `espesor por medida` | 1 | ahueca dejando pared |
| Transformar | `patron lineal por medida` | 2 | N copias en línea |
| Transformar | `repetir cada` | 2 | N copias con separación |
| Transformar | `patron circular por medida` | 2 | N copias en círculo |
| Transformar | `escalar por factor` | 2 | escala el sólido |

---

## Prueba 1 — Cubo

| Decí | Qué pasa |
|---|---|
| `banco de trabajo` → `diseño de pieza` → `aditivo` | |
| `caja por medidas` | abre el pop-up |
| `veinte enter` | largo |
| `veinte enter` | ancho |
| `veinte enter` | alto |

**Esperado**: `[additive] Created box 20 x 20 x 20`

> Empezá por acá: si falla, el problema es la navegación o los números, no los
> comandos.

---

## Prueba 2 — Cilindro

Desde `aditivo`:

| Decí | Qué pasa |
|---|---|
| `cilindro por medidas` | abre el pop-up |
| `diez enter` | radio |
| `cuarenta enter` | altura |

**Esperado**: `[additive] Created cylinder radius 10 height 40`

---

## Prueba 3 — Redondear el cubo

Con el cubo de la prueba 1 **seleccionado** (clic en el árbol o la vista 3D):

| Decí | Qué pasa |
|---|---|
| `subir` → `modificar` | entra a los acabados |
| `redondear por radio` | abre el pop-up |
| `tres enter` | radio |

**Esperado**: todas las aristas redondeadas y
`[modify] Rounded '...' with radius 3`

> El radio debe ser **menor que la mitad del lado más chico** del sólido. Con un
> cubo de 20, un radio de 3 anda; uno de 15 falla al recalcular.

---

## Prueba 4 — Chaflán

Con un sólido seleccionado, desde `modificar`:

| Decí | Luego | Esperado |
|---|---|---|
| `chaflan por medida` | `dos enter` | chaflán de 2 mm a 45° |
| `chaflan con angulo` | `dos enter` / `treinta enter` | chaflán de 2 mm a 30° |

**Esperado**: `[modify] Chamfered '...' with size 2` (o `... at 30 degrees`).

---

## Prueba 5 — Ahuecar

Con un sólido seleccionado, desde `modificar`:

| Decí | Qué pasa |
|---|---|
| `espesor por medida` | abre el pop-up |
| `dos enter` | espesor de pared |

**Esperado**: `[modify] Hollowed '...' leaving 2 of wall`

---

## Prueba 6 — Cortar (sustractivo)

Estos comandos necesitan un **perfil 2D seleccionado**, igual que `extruir`.

Primero dibujá un cuadrado chico:

```
subir → croquis → geometria → rectangulo → rectangulo por esquinas
cero / cero / diez / diez
```

Seleccionalo, y desde `diseño de pieza` → `sustractivo`:

| Decí | Luego | Esperado |
|---|---|---|
| `vaciado por medida` | `diez enter` | `Pocketed '...' by 10` |
| `ranura por angulo` | `noventa enter` | `Grooved '...' by 90 degrees` |

Para el agujero, dibujá un círculo y seleccionalo:

| Decí | Luego | Esperado |
|---|---|---|
| `agujero por medidas` | `seis enter` / `veinticinco enter` | `Drilled a hole of diameter 6 and depth 25` |

---

## Prueba 7 — Flujo completo: cuadrado → cubo → redondeado

Encadena todo. Es la prueba que más valor tiene.

| Paso | Decí |
|---|---|
| 1 | `banco de trabajo` → `croquis` → `geometria` → `rectangulo` |
| 2 | `rectangulo por esquinas` → `cero`/`cero`/`veinte`/`veinte` |
| 3 | *(clic en el rectángulo para seleccionarlo)* |
| 4 | `subir` hasta workbench → `diseño de pieza` → `aditivo` |
| 5 | `extruir por medida` → `treinta enter` |
| 6 | *(clic en el sólido)* |
| 7 | `subir` → `modificar` → `redondear por radio` → `tres enter` |

**Esperado**: un prisma de 20×20×30 con las aristas redondeadas.

> Los pasos 3 y 6 **todavía necesitan mouse**. La selección por voz existe pero
> es otro flujo.

---

## Prueba 8 — Más primitivas

Desde `aditivo`, cada una abre su pop-up:

| Decí | Valores | Resultado |
|---|---|---|
| `esfera por radio` | `quince` | esfera r=15 |
| `cono por medidas` | `diez` / `cero` / `veinticinco` | cono con punta |
| `cono por medidas` | `diez` / `cinco` / `veinticinco` | tronco de cono |
| `toro por medidas` | `veinte` / `cinco` | toro (anillo 20, tubo 5) |
| `prisma por medidas` | `seis` / `diez` / `treinta` | prisma hexagonal |

> En el toro, el radio del tubo debe ser **menor** que el del anillo, o el
> comando avisa y no crea nada.

---

## Prueba 9 — Restar primitivas

Con un sólido ya creado, desde `sustractivo`:

| Decí | Valores | Resultado |
|---|---|---|
| `cortar caja por medidas` | `diez` / `diez` / `veinte` | resta una caja |
| `cortar cilindro por medidas` | `cinco` / `veinte` | resta un cilindro |
| `cortar esfera por radio` | `ocho` | resta una esfera |

Se restan del **último cuerpo creado**.

---

## Prueba 10 — Patrones y escalado

Con una operación seleccionada (por ejemplo el agujero de la prueba 6), desde
`transformar`:

| Decí | Valores | Resultado |
|---|---|---|
| `patron lineal por medida` | `cinco` / `ochenta` | 5 copias repartidas en 80 mm |
| `repetir cada` | `cinco` / `veinte` | 5 copias, una cada 20 mm |
| `patron circular por medida` | `seis` / `trescientos sesenta`* | 6 copias en círculo completo |
| `escalar por factor` | `dos` / `dos` | duplica el tamaño |

\* **Ojo**: 360 no se puede pronunciar como palabra; hay que deletrearlo:
`tres seis cero enter`. Funciona, pero es incómodo — está documentado en
[numeros-por-voz-limites-y-propuesta.md](../referencia/numeros-por-voz-limites-y-propuesta.md).

> La diferencia entre los dos patrones lineales: `patron lineal por medida`
> reparte las copias a lo largo del **total** dictado; `repetir cada` usa el
> valor como **separación entre copias**.

---

## Prueba 11 — Que los errores avisen

Implementadas pero **no probadas dentro de FreeCAD**. Confirmá que el mensaje
sale en el Report View:

| Prueba | Cómo | Mensaje esperado |
|---|---|---|
| Caja con lado cero | `caja por medidas` → `veinte`/`cero`/`veinte` | `every dimension must be greater than zero` |
| Radio negativo | `redondear por radio` → `menos uno` | `radius must be greater than zero` |
| Chaflán cero | `chaflan por medida` → `cero` | `size must be greater than zero` |
| Ángulo imposible | `chaflan con angulo` → `dos` / `doscientos` | `angle must be between 0 and 180` |
| Sin selección | `redondear por radio` sin seleccionar nada | `select the solid to round first` |
| Cancelar | `cancelar` en cualquier pop-up | `Command cancelled by user` |

---

## Prueba 12 — Los otros idiomas

PartDesign tenía tres carpetas con diccionarios que fallaban en silencio: el
loader aísla el módulo roto y sigue con mapa vacío, así que las frases
simplemente no respondían, sin error visible.

| Idioma | Frase | Debería |
|---|---|---|
| Inglés | `box by size` | abrir el pop-up de la caja |
| Inglés | `fillet by radius` | abrir el pop-up del redondeo |
| Portugués | `caixa por medidas` | abrir el pop-up de la caja |
| Portugués | `chanfro por medida` | abrir el pop-up del chaflán |

---

## Cómo reportar

Para cada prueba: **qué dijiste**, **qué salió en el Report View** y **si el
objeto apareció en el árbol** del panel DAV.

---

## Dónde es más probable que falle

Nada de esto se ejecutó dentro de FreeCAD: se validó con stubs, que confirman el
ruteo de las frases y que los valores dictados llegan a las propiedades
correctas (`Pad.Length`, `Fillet.Radius`, `Chamfer.Angle`…), pero no la
interacción con FreeCAD vivo.

Los puntos de mayor riesgo:

1. **Redondeo y chaflán** — se aplican a **todas las aristas** del sólido
   (`UseAllEdges`), porque elegir aristas sueltas por voz no es práctico. Si el
   radio o el tamaño es muy grande para la pieza, el recompute falla: es
   comportamiento de FreeCAD, no del comando, pero conviene ver qué mensaje
   aparece.
2. **Sustractivo** — el perfil se convierte de `Part::Feature` a croquis, igual
   que en `extruir`. Con curvas reales puede comportarse distinto que con el
   stub.
3. **`agujero por medidas`** — se fuerza `DepthType = 1` para que respete la
   profundidad dictada; vale confirmar que el agujero sale con la profundidad
   pedida y no pasante.
