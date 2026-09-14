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
