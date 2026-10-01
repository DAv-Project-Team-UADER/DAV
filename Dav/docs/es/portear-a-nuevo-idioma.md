# Flujo de trabajo para portear DAV a un idioma nuevo (hipotético)

> Este documento es una **propuesta**: describe cómo se haría, con la arquitectura actual,
> para sumar un cuarto idioma (por ejemplo francés, `fr`) a los tres que hoy soporta DAV
> (español, inglés y portugués). No es un procedimiento probado de punta a punta.

Un idioma en DAV tiene cuatro piezas: el **modelo de reconocimiento** (Vosk), las **frases y
nombres** de cada comando (`TraduceTo*.py`), los **textos de la interfaz y de los diálogos**
y la **documentación** (incluido el manual PDF).

## 0. Decidir el alcance

- Código ISO 639-1 del idioma (`fr`) y si hay variante regional (`pt` vs `pt-br`).
- Confirmar que existe un modelo Vosk utilizable (paso 1). Sin modelo no hay voz: el resto
  sirve solo para la interfaz escrita.

## 1. Elegir el modelo de voz

1. Entrar a la página de modelos de Vosk: **<https://alphacephei.com/vosk/models>**.
2. Buscar el idioma. Conviene un par de modelos, como en los demás idiomas:
   - uno **chico** (decenas de MB, `vosk-model-small-<idioma>-…`), que viaja con el proyecto;
   - uno **grande** (cientos de MB a GB), que se descarga a pedido.
3. Revisar la licencia de cada modelo (casi todos son Apache 2.0, pero hay excepciones) y anotar
   la versión exacta.
4. Probarlo sin DAV con el ejemplo de Vosk (`vosk-transcriber` o un script de `KaldiRecognizer`) y
   confirmar que reconoce bien los números y los términos de CAD en ese idioma. La precisión con
   frases cortas y números decide si el idioma es viable.

## 2. Registrar el idioma en el código

| Dónde | Qué cambiar |
|---|---|
| [`core/language_code.py`](../../scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/core/language_code.py) | Agregar el miembro (`Fr = "fr"`) y su sufijo `TraduceToFr` en `TranslateModuleSuffix` / `AlternateTranslateSuffixes` |
| [`core/model_manager.py`](../../scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/core/model_manager.py) | Sumar `"fr": (chico, grande)` a `MODEL_CATALOG` |
| [`core/settings.py`](../../scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/core/settings.py) | Aceptar `"fr"` en la validación de la preferencia de idioma |
| [`InputPrompts/InputPromptI18n.py`](../../scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/InputPrompts/InputPromptI18n.py) | Reconocer `fr` al normalizar el código y devolverlo |
| `InputPrompts/SpokenNumberParser.py`, `PlaneGrammarSwitcher.py` | Números hablados y gramática de planos del nuevo idioma |
| Selector de idioma en Preferencias | Agregar la opción (ver [`Preferences`](diagramas/Preferences.md)) |

Buscar con `grep -rn "\"pt\"" Dav/scr` (y `'pt'`) para encontrar los lugares que enumeran los
idiomas y no se hayan listado arriba. Los tests existentes que recorren los tres idiomas fallarán
hasta que el nuevo esté completo: sirven como lista de pendientes.

## 3. Traducir los diccionarios de comandos

Cada carpeta de `Dav/dic/` tiene un `TraduceToEs.py`, `TraduceToEn.py` y `TraduceToPt.py`.

1. Crear `TraduceToFr.py` en **cada** carpeta (hoy son ~130), partiendo de la copia del
   inglés o del español. Un script que recorra el árbol y copie el archivo base acelera el paso.
2. Traducir las **frases habladas** y los nombres de los comandos. Criterios:
   - frases cortas, naturales y distintas entre sí (el modelo confunde las parecidas);
   - sin ambigüedad con números u otros comandos del mismo contexto;
   - validarlas contra el vocabulario del modelo elegido: una palabra fuera del vocabulario
     nunca se reconocerá (ver [`acortador-gramatica-vosk`](acortador-gramatica-vosk.md)).
3. Respetar la normalización de frases (`DictionaryLoader.NormalizeSpoken`: minúsculas, sin tildes).
4. Correr los tests de diccionarios reales para detectar claves faltantes o frases repetidas
   (ver [`probando`](desarrollo/probando.md)).

Las claves y la estructura de los diccionarios no cambian; solo se agregan archivos.

## 4. Traducir textos de interfaz y diálogos

- Los diálogos con parámetros (números, planos, sí/no, ejemplos guiados) tienen textos por idioma
  en sus clases de `InputPrompts/` y en los ejemplos de `dic/Explorer/Examples/`.
- Agregar la traducción en cada tupla o diccionario que hoy tiene `es`/`en`/`pt`.
- Revisar los títulos de los paneles y los mensajes de estado.

## 5. Documentación y manual PDF

1. Crear `Dav/docs/fr/` con los mismos archivos y nombres que `es/` y `en/` (la lista de
   archivos se obtiene con `find Dav/docs/es -type f`). Se puede partir de la traducción
   automática y revisarla; las frases que se dicen al modelo se dejan en el idioma del modelo.
2. Agregar el idioma a `Dav/docs/manual/`: una columna más en las tuplas de los `desc_*.py`
   y en `textos.py`, y el idioma en `IDIOMAS`/`IDX` de `build_manual.py` (ver
   [regenerar el manual PDF](regenerar-manual-pdf.md)).
3. Sumar un `README.fr.md` en la raíz, como los `README.es.md` y `README.pt.md`.
4. Actualizar el índice [`Dav/docs/README.md`](../README.md).

## 6. Verificación y entrega

- [ ] El modelo chico está en `Dav/models/` y el grande se descarga desde Preferencias.
- [ ] Cambiar el idioma en Preferencias carga la gramática y el modelo correctos.
- [ ] Todos los comandos tienen frase en el idioma nuevo (los tests de diccionarios pasan).
- [ ] Un hablante nativo recorre las guías de prueba (`guia-pruebas-*.md`) y anota las frases
      que no se reconocen.
- [ ] El manual PDF del idioma se genera sin avisos de comandos sin descripción.
- [ ] Se documentó la versión del modelo y su licencia.

## Sugerencia de ramas y PR

Seguir el [GitFlow del proyecto](gitflow-gitgraph.md) con una rama `feature/idioma-fr` y PR
pequeños: (1) registro del idioma y modelo, (2) diccionarios, (3) interfaz y diálogos,
(4) documentación y manual.
