# Números por voz — qué se puede dictar hoy y cómo quitar el techo

Estado del reconocimiento numérico en los pop-ups de parámetros
(`SpokenNumberParser`), qué límite tiene realmente y qué haría falta para
sacarlo.

---

## Lo que se puede dictar hoy

Contra lo que se anotó en las primeras guías de prueba, **no hay un techo duro
de 99**. El parser concatena dígitos, así que cualquier número es dictable
deletreándolo:

| Se dice | Se obtiene |
|---|---|
| `veinticinco` | 25 |
| `treinta y cinco` | 35 |
| `cinco cero` | 50 |
| `nueve nueve` | 99 |
| **`uno cero cero`** | **100** |
| **`uno dos tres`** | **123** |
| `menos veinte` | −20 |
| `doce coma cinco` | 12,5 |

Verificado ejecutando `SpokenNumberParser.ParseInteger` sobre cada frase.

Lo que **sí** corta en 99 es la pronunciación *natural* de un número como
palabra compuesta: «ciento veinticinco» no se entiende, porque `cien` y las
centenas no están en el diccionario.

### La consecuencia práctica

Para valores de 0 a 99 se habla normal. Para 100 o más hay que **deletrear
dígito por dígito**, que funciona pero es antinatural — sobre todo en casos
como un patrón circular de 360°, donde `tres seis cero` es incómodo comparado
con «trescientos sesenta».

---

## Por qué pasa

`SpokenNumberParser.DigitWords` es un mapa plano de palabra → dígito, con 93
entradas que cubren 0–30 y las decenas (40, 50, 60, 70, 80, 90) en los tres
idiomas.

`_MergeTensAndUnits` arma los compuestos de dos palabras («treinta y cinco» →
35), pero **no hay noción de centena ni de multiplicador**: el parser junta
dígitos en una cadena de texto en vez de sumar valores posicionales.

```
"uno cero cero"  →  "1" + "0" + "0"  →  "100"   (concatenación, no suma)
```

Por eso deletrear funciona y pronunciar no.

---

## Las tres salidas posibles

### 1. Biblioteca externa

`text2num` o `number_parser` resuelven esto con soporte es/en/pt.

**No conviene.** El código corre en el **Python embebido de FreeCAD**, no en el
venv de desarrollo. El proyecto hoy no tiene dependencias externas más allá de
Vosk y PyAudio, y sumar uno más al intérprete embebido es frágil de instalar y
de sostener en las máquinas del equipo.

### 2. Algoritmo de composición posicional — recomendada

El español, como el inglés y el portugués, construye números de forma
**regular**: unidades, decenas, centenas y multiplicadores. No hay que
enumerar mil palabras, sino unas 30 más las reglas de combinación.

```
valor = suma de grupos, con multiplicadores que cierran cada grupo

"doscientos treinta y cinco"  →  200 + 30 + 5            =   235
"tres mil cuatrocientos"      →  (3 × 1000) + 400        =  3400
```

Palabras base necesarias:

| Grupo | Palabras |
|---|---|
| Unidades y 11–15 | `uno`…`quince` — **ya están** |
| Decenas | `veinte`…`noventa` — **ya están** |
| Centenas | `cien`, `ciento`, `doscientos`…`novecientos` — **faltan** |
| Multiplicadores | `mil`, `millón` — **faltan** |

Es decir: el diccionario ya tiene la mayor parte. Falta agregar centenas y
multiplicadores, y reemplazar `_MergeTensAndUnits` por un acumulador que sume
por posición en vez de concatenar texto.

Son unas 60 líneas, sin dependencias nuevas, y la misma estructura sirve para
los tres idiomas.

### 3. Ampliar el hardcodeo

Agregar `cien`, `doscientos`, etc. como entradas planas del mapa.

Rápido, pero no escala: para llegar a 1.000.000 harían falta miles de entradas,
y cada una infla la gramática de Vosk.

---

## El detalle que condiciona todo: la gramática de Vosk

**El parser no alcanza por sí solo.** La gramática de Vosk se acota al contexto
activo (ver [acortador-gramatica-vosk.md](acortador-gramatica-vosk.md)), y
durante un pop-up numérico se cambia a la lista que devuelve
`get_numeric_grammar_phrases()` en `Dav/dic/Numbers/Numbers.py`, vía
`NumericGrammarSwitcher.ActivateNumericGrammar()`.

Esa lista sale **del mismo diccionario** que alimenta al parser. O sea:

> Si «doscientos» no está en el diccionario numérico, Vosk **nunca va a
> transcribir esa palabra**, por más que el parser sepa interpretarla.

Es una buena noticia de diseño: parser y gramática comparten fuente, así que
agregar las palabras nuevas al diccionario las habilita en ambos lados a la
vez. Pero implica que el cambio **no es sólo del parser** — hay que verificar
que `get_numeric_grammar_phrases()` incluya las centenas y multiplicadores
nuevos.

---

## Recomendación

Encarar la **opción 2**, en este orden:

1. Agregar centenas y multiplicadores al diccionario `Numbers`, en los tres
   idiomas.
2. Confirmar que `get_numeric_grammar_phrases()` los devuelva (si arma la lista
   desde el mapa completo, sale gratis).
3. Reemplazar `_MergeTensAndUnits` por un acumulador posicional.
4. **Mantener el modo dígito-a-dígito**, que hoy funciona y puede haber gente
   usándolo: el acumulador debería reconocer ambas formas.

El punto 4 es el que más cuidado pide. Hoy `uno cero cero` da 100 por
concatenación; un acumulador posicional ingenuo lo interpretaría como
1 + 0 + 0 = 1. Hay que decidir explícitamente cómo convive cada modo antes de
tocar el parser.

---

## Impacto actual

Ningún comando está bloqueado —todo valor se puede deletrear— pero hay casos
donde se nota:

| Caso | Hoy | Con la propuesta |
|---|---|---|
| Patrón circular 360° | `tres seis cero` | `trescientos sesenta` |
| Cota de 150 mm | `uno cinco cero` | `ciento cincuenta` |
| Medidas 0–99 | ya es natural | igual |

Mientras tanto, las guías de prueba usan valores menores a 100 para que las
frases de ejemplo suenen naturales.