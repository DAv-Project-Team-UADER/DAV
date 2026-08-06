# Pendientes DAV — hallazgos de sesión de auditoría de diccionarios y navegación por voz

## 1. Vosk reconoce con vocabulario abierto, no acotado al contexto

**Dónde:** `Dav/scr/ComponentesDAV/InterfazDAV/VoiceWorker.py:56`

```python
recognizer = vosk.KaldiRecognizer(model, 16000)
```

El `KaldiRecognizer` se crea sin gramática restringida (`SetGrammar`), así que Vosk compite contra todo el vocabulario del modelo español en cada frase, en vez de limitarse a los comandos válidos del contexto actual (`Browser.Context` ya tiene esa lista disponible en todo momento).

**Síntoma observado:** palabras cortas o poco frecuentes se transcriben mal — "croquis" salió como "crockett", apareció "traffic" sin que nadie lo dijera. Con el modelo pequeño (`vosk-model-small-es-0.42`, 39 MB) el efecto es más marcado que con el modelo grande.

**Arreglo sugerido:** pasarle a `KaldiRecognizer` una gramática JSON con las palabras/frases de `Browser.Context` (o `BaseContext` si aún no se descendió), actualizándola cada vez que cambia el contexto de navegación. Debería reducir bastante las transcripciones erráticas.

## 2. MainWindow.py (la GUI que se usa hoy) no usa el Browser real

**Dónde:** `Dav/scr/ComponentesDAV/InterfazDAV/MainWindow.py` (`_VoiceMap`, `_GroupMeta`, `_LoadGroupMeta`, `_LoadVoiceMap`)

Esta ventana tiene su propio motor de navegación por voz, separado de `navigation/browser.py` (`Browser.ProcessPhrase`, el que se audita y mantiene activamente). Lee de:

```
Dav/scr/ComponentesDAV/InterfazDAV/DiccionarioPrueba/
```

que es un diccionario de prueba chico (solo `explorer` con `file`/`edit`/`print`/`doc`), **no** el árbol completo `Dav/dic/` (Sketcher, Workbench, PartDesign, StdView, NavCommands, etc.).

**Consecuencia práctica:** todo lo arreglado en `Dav/dic/` (imports rotos, duplicados, `base.py` enlazado, `NavCommands` para "subir"/"contexto") no tiene ningún efecto en la GUI real que se está probando. Los logs de este motor tienen formato distinto (`[Voz]`, `[Btn]`, `No entendí: '...' no disponible en <grupo>`) al del `Browser` (`[DAV Browser]`, `[BrowserVoiceAdapter]`).

**Pendiente de decidir:** si `MainWindow.py` debe migrar a usar `Browser` (de `navigation/browser.py`) en vez de su propio `_VoiceMap`/`_GroupMeta`, o si son productos deliberadamente separados (uno de prueba rápida, otro el motor "serio") y hay que documentar cuál es cuál.

## 3. Palabras ambiguas entre workbenches (parcialmente resuelto)

`"dibujar"` (Sketcher) y `"dibujo"` (Draft) eran casi indistinguibles para el reconocimiento de voz — se sacó `"dibujo"`/`"dibujos"` de Draft en `Dav/dic/Workbench/TraduceToEs.py` (queda `"banco de dibujo"`, `"borrador"`, `"draftwork"`, `"draft"` como alternativas). Sketcher sigue teniendo `"dibujar"` como sinónimo — si se repite el problema, revisar si conviene sacarlo también y dejar solo `"croquis"`/`"banco de croquis"`.

También hay pares similares en el mismo archivo con nombres en inglés (`"sketcher"`, `"draft"`, `"partdesign"`, `"techdraw"`) — el modelo español los reconoce mal por no ser palabras españolas; siempre usar los sinónimos en español como forma principal.
