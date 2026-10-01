# Puesta en marcha (setup)

Guía para levantar DAV y probar el motor de voz en una máquina local.

> ⚠️ **Los dos intérpretes.** El venv de desarrollo
> (`IntegracionGUI/GUIFreeCad/.venv`) usa Python más nuevo que el Python
> embebido de FreeCAD. El código tiene que correr en ambos: **los scripts que
> se cargan dentro de FreeCAD usan el intérprete de FreeCAD, no el venv.**
> Las extensiones de FreeCAD deben usar **PySide6**, no PyQt, por
> compatibilidad constructiva con el framework nativo.

## 1. Clonar el repositorio

El flujo de contribución se hace con **fork personal** + **Pull Request** (ver
el flujo completo en `CLAUDE.md` y en `guia-desarrollo-dav.md` → GitFlow).

```bash
git clone https://github.com/<tu-usuario>/DAV.git
cd DAV
```

Si querés el repositorio central directo:

```bash
git clone https://github.com/DAv-Project-Team-UADER/DAV.git
```

## 2. Dependencias Python (venv de desarrollo)

El entorno de desarrollo vive en
`Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/.venv` con las dependencias
declaradas en `requirements.txt`:

```
PySide6>=6.6.0
vosk>=0.3.45
sounddevice>=0.4.6
numpy>=1.24.0
requests>=2.31.0
tqdm>=4.66.0
```

Para recrearlo/instalarlo:

```bash
cd Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad
python -m venv .venv
.venv\Scripts\activate          # Windows
# o: source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

> Este venv sirve para **desarrollar/testear el widget de GUI y prompts** de
> forma aislada. Para probar la voz **dentro de FreeCAD** hay que tener las
> dependencias disponibles para el intérprete de FreeCAD (módulos instalados
> en el entorno que corre FreeCAD).

## 3. Modelos de voz Vosk

Los modelos viven en `Dav/models/` (excluidos de git — ver
`Dav/models/README.md`):

| Modelo | Idioma |
|---|---|
| `vosk-model-small-es-0.42` | Español |
| `vosk-model-small-en-us-0.15` | Inglés |
| `vosk-model-small-pt-0.3` | Portugués |

No hace falta descargarlos a mano: `core/model_manager.py` y
`ui/download_dialog.py` (en `IntegracionGUI/GUIFreeCad/`) los descargan si
faltan. También existe el script `scripts/setup_models.py`.

> Para mayor precisión en español existe `vosk-model-es-0.42` (más pesado), no
> incluido por defecto.

## 4. Correr DAV dentro de FreeCAD

DAV arranca dentro de la **consola Python** de FreeCAD (Vista → Paneles →
Consola de Python) o como **macro**. El `DAVCore` debe iniciarse igual que
`FreeCADGuiInit.py`, es decir al arrancar la aplicación.

Pasos generales:

1. Abrí FreeCAD con un documento nuevo.
2. Abrí la **Consola de Python**.
3. Cargá y ejecutá el arranque del motor de voz (el bootstrap que monta el
   `Browser` + micrófono). Ver `integration/voice_bootstrap.py` y el
   `InitGui.py` en `scr/.../Dav/` para el arranque automático con FreeCAD.
4. Configurá el idioma en **Preferencias DAV** si no es español.

> El panel DAV se monta como `QDockWidget` dentro de FreeCAD vía
> `integration/dav_dock_panel.py`. Si arranca como ventana flotante, se puede
> anclar a cualquier borde.

## 5. Comandos básicos para verificar el setup

Con el motor activo, probá frases de navegación del propio Browser (no tocan
nada del documento):

- **`donde estoy`** — muestra el contexto actual.
- **`subir`** — sube un nivel del árbol de navegación.

Y un comando real, por ejemplo:

```
banco de trabajo → diseñador de piezas    (ir al workbench PartDesign)
```

Los comandos de confirmación/aborto de pop-ups (compartidos por los prompts):

- **Confirmar un valor**: `enter` · `enviar` · `aceptar` · `confirmar` · `ok`
- **Abortar un pop-up**: `cancelar`

## Puertos / problemas comunes

- **El micrófono usa PyAudio/SoundDevice** — si no se abre el stream, revisá
  que el dispositivo esté disponible y desocupado.
- **No se cargó el modelo** → confirmá que exista en `Dav/models/<idioma>` o
  que `setup_models.py` lo haya descargado.
- **La gramática está acotada por contexto** — ciertos prompts (numéricos, de
  selección de plano) limitan qué palabras escucha Vosk a propósito. Si un
  comando "no se entiende", revisá si hay un prompt activo acotando la
  gramática (ver `acortador-gramatica-vosk.md`).

---

Siguiente: [Convenciones de código](convenciones.md)
