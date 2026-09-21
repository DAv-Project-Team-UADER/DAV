# Manual rápido — Explorer por voz

## Cómo funciona

DAV navega por **niveles**, como un menú. Decís una palabra para **entrar** a un
submenú, y otra para **ejecutar** un comando. Siempre estás parado en un
contexto, y solo se reconocen las palabras de ese contexto.

```
Base  →  explorador  →  archivo  →  guardar
         (entrar)       (entrar)    (ejecutar)
```

## Comandos de navegación (funcionan en cualquier contexto)

| Para | Decí |
| --- | --- |
| Subir un nivel | **subir**, volver, atrás, salir, regresar, retroceder |
| Ver dónde estás y qué podés decir | **contexto**, dónde estoy, qué puedo decir, opciones disponibles, ubicación |

> Si te perdés, decí **«contexto»** — lista los submenús y comandos disponibles
> en el nivel actual.

Estas palabras no están hardcodeadas: viven en `Dav/dic/NavCommands/`, así que
se pueden agregar sinónimos sin tocar `browser.py`.

## Entrar al Explorer

Desde Base, decí: **«explorador»**

## Submenús del Explorer

| Submenú | Palabras para entrar |
| --- | --- |
| Archivos | **archivo**, archivos, carpeta, carpetas, folios |
| Edición | **editar**, edición, modificar, alterar |
| Imprimir | **imprimir**, impresión, pdf, exportar pdf, generar pdf, impresora |
| Ventanas | **ventanas**, ventana |
| Expresiones | **expresiones**, expresión |
| Herramientas | **herramientas**, utilidades |
| Estructura | **estructura**, barra de estructura |
| Ejemplos | **ejemplos**, quiero aprender, aprender, tutoriales |

## Comandos directos (sin entrar a ningún submenú)

Estando en `explorador`, se ejecutan directo:

- **refrescar** / recargar / actualizar
- **captura** / foto / sacar foto / captura de pantalla / guardar pantalla
- **documento** / texto / documento de texto
- **desvincular** / desenlazar / quitar enlace
- **congelar** / bloquear / inmovilizar
- **variables** / conjunto de variables / set de variables
- **todas las instancias** / seleccionar instancias

## Comandos dentro de cada submenú

**archivo** → nuevo · abrir · guardar · guardar como · guardar copia ·
revertir · combinar · importar · exportar · recientes · cargar imagen

**proyecto** → abrir · guardar · exportar (sin diálogos nativos; ver más abajo)

**editar** → deshacer · rehacer · cortar · copiar · pegar · duplicar ·
seleccionar todo · eliminar · posición · transformar · alinear · preferencias ·
propiedades · enviar a python · modo edición

**imprimir** → imprimir · impresora · pdf

**ventanas** → cerrar · cerrar todo · salir

**expresiones** → copiar documento · copiar todo · copiar selección ·
pegar expresión

**herramientas** → medir · medir distancia · limpiar selección · modo demo ·
personalizar · editar parámetros · utilidades de proyecto

**estructura** → pieza · grupo · enlace

Todos los submenús aceptan además **ayuda** / información / opciones.

## Proyecto: abrir, guardar y exportar por voz

`archivo` usa los diálogos nativos de FreeCAD, que no se manejan por voz.
`proyecto` hace lo mismo con ventanas de voz (`Dav/dic/Explorer/Proyecto/`):

- **abrir** → recorre las carpetas: *siguiente* / *anterior* mueven la
  selección, *abrir* entra a la carpeta elegida, *subir* va a la carpeta
  padre, *okey* elige el archivo, *cancelar* sale. Empieza en la carpeta del
  documento activo o la última usada.
- **guardar** → si el documento ya tiene archivo, lo guarda ahí. Si es nuevo
  pregunta la carpeta (la sugerida u otra, elegida con el mismo navegador, donde
  *okey* elige la carpeta en la que estás) y el nombre (el sugerido o uno
  deletreado). Si el archivo existe pide *sobrescribir*.
- **exportar** → elige el formato (STEP, IGES, STL, OBJ, DXF; con
  *arriba*/*abajo* y *okey*), luego carpeta y nombre como en guardar. Exporta
  la selección o, si no hay, todo lo visible.

Los nombres de archivo no se pueden dictar (no están en el vocabulario de
Vosk): por eso se recorre la lista en lugar de decirlos.

## Ejemplos: aprender haciendo

Dentro de **ejemplos** (la carpeta no tiene ícono) hay dos opciones:

| Opción | Palabras | Qué hace |
| --- | --- | --- |
| Manual de usuario | **manual**, referencia | Abre el PDF en tu idioma: `Manual_Usuario.pdf` en español; `User_Manual.pdf` en inglés y también en portugués |
| Ejemplos | **ejemplos**, demostraciones, tutorial | Abre un selector con siete ejemplos guiados |

Ejemplos guiados:

| Ejemplo | Qué se hace | Medidas |
| --- | --- | --- |
| **Croquis** | Un círculo con restricción de radio | Cota en 2D |
| **Draft** | Rectángulo, círculo y polígono | Cota en 2D |
| **TechDraw** | Un círculo en una hoja con su rótulo | — |
| **PartDesign** | Un tornillo: vástago, punta, cabeza, chaflán y rosca | Cota en 3D y vista «tres de» |
| **Dado** | Un dado de 20 mm: la cara del 1 con un cilindro y las otras cinco con un boceto y un vaciado cada una | Cota en 3D, las seis vistas y «tres de» |
| **Arandela plana M6** | Un croquis con el agujero (Ø 6,4) y el borde (Ø 12), extruido 1,6 mm en PartDesign y puesto en una hoja de TechDraw con vista isométrica, vista del boceto y el texto «M6 arandela» | Restricción de diámetro y cota en 2D |
| **Bulón-tuerca** | Un bulón M6 de cabeza hexagonal (simplificado de la DIN 931) y su tuerca, hechos en PartDesign, insertados por voz en un ensamblaje, con el bulón anclado y una junta cilíndrica que lleva la tuerca al eje por las caras que se eligen | Ensamblaje con junta cilíndrica y vista «tres de» |

Los decimales se dictan con «punto» en los tres idiomas: «uno punto uno uno» es 1,11. En español «coma» vale igual («uno coma uno uno»). Los números de 0 a 99 se dicen naturales («treinta y dos»); de 100 en adelante, dígito por dígito («uno cero cero»).

El selector se maneja con **retroceder**, **avanzar** y **enviar**. Ya elegido el
ejemplo, aparece una ventana (no bloquea FreeCAD, así ves cómo se arma la pieza)
que muestra un **cuadro** por vez con **lo que dirías para hacerlo en DAV**: el camino
por los menús y, después, los valores que se dictan en los diálogos. Cuando lo decís
todo, en orden, la acción se ejecuta y pasa al cuadro siguiente.

Por ejemplo, para dibujar un círculo de radio 12 en un croquis:

```
banco → croquis → nuevo → enviar          (elige el plano XY)
geometría → círculo → círculo             (entra a Geometría y a Círculo, y lo crea)
cero → enviar → cero → enviar → doce → enviar     (centro X, centro Y y radio)
```

Cada palabra o frase del camino es un comando; cada valor se confirma con **enviar**.
Lo que se dicta depende del documento: por ejemplo, en el Dado, cuántas veces decir
**abajo** para llegar a una cara de la lista sale de las caras que tiene el sólido en ese
momento (la ventana agrupa las repeticiones: «abajo ×5»).

- **retroceder / avanzar**: repasar cuadros ya hechos.
- **saltar**: ejecuta el cuadro sin decir sus palabras (útil si el micrófono no lo reconoce).
- **cancelar**: cierra el ejemplo. Al terminar, **enviar** lo cierra.

Cada ejemplo son las funciones `steps()` de `Dav/dic/Explorer/Examples/_*.py`;
para agregar uno, crear un módulo con `TITLE` y `steps()` y sumarlo a `_EXAMPLES` en `_demos.py`.

Las palabras de cada cuadro se comprueban contra el árbol real, en los tres idiomas, con
`tests/verify_examples_paths.py` (ver [`probando.md`](desarrollo/probando.md)): si el
diccionario cambia y un ejemplo deja de coincidir, esa prueba lo marca.

## Ejemplos completos

Guardar el archivo:

```
"explorador" → "archivo" → "guardar"
```

Exportar a PDF:

```
"explorador" → "imprimir" → "pdf"
```

Deshacer un cambio:

```
"explorador" → "editar" → "deshacer"
```

Sacar una captura (comando directo, sin submenú):

```
"explorador" → "captura"
```

## Tips

- **No hace falta subir para cambiar de menú principal**: desde cualquier nivel
  se puede decir «banco de trabajo», «vista estándar», etc. y salta directo.
- **Los acentos no importan**: «impresión» e «impresion» se reconocen igual (el
  motor normaliza tildes y eñes antes de comparar).
- **Evitá las palabras en inglés** (`sketcher`, `draft`, `techdraw`): el modelo
  de voz es español y las reconoce mal. Usá siempre los sinónimos en castellano.
- Si una palabra no se entiende, probá un sinónimo de la lista — casi todos los
  comandos tienen dos o tres.

## De dónde sale este vocabulario

Todas las palabras de este manual salen de los diccionarios reales:

- `Dav/dic/Explorer/TraduceToEs.py` — submenús y comandos directos
- `Dav/dic/Explorer/<Submenú>/TraduceToEs.py` — comandos de cada submenú
- `Dav/dic/NavCommands/TraduceToEs.py` — subir / contexto

Si se agregan sinónimos ahí, este manual queda desactualizado: conviene
regenerarlo desde esos archivos.
