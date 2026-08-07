# Plan: Árbol de FreeCAD como datos navegables (reemplazar imagen PNG)

## Contexto

Hoy el panel **"Árbol de FreeCAD"** de la GUI PySide6 (`Dav/scr/ComponentesDAV/InterfazDAV/MainWindow.py`)
no muestra el árbol real: muestra una **imagen PNG** (`tree_capture.png`) que una macro de FreeCAD
genera con `combo_view.grab()` y la GUI refresca cada 2s. Eso cumple lo visual pero **no es
navegable** — no hay objetos, ni tipos, ni jerarquía como datos. El requisito del CLAUDE.md
("navegar objetos creados") pide datos reales.

**Objetivo:** que la macro envíe la **estructura de objetos** del documento activo como **JSON**
(nombre, tipo, label, visibilidad, jerarquía padre/hijo) y que la GUI la pinte en un
**`QTreeWidget`**, reemplazando por completo la captura de imagen. Sin comandos de voz todavía y
sin selección bidireccional con FreeCAD (queda como fase futura).

El flujo de comunicación GUI↔FreeCAD ya existe y se reutiliza: archivo de señal JSON +
`dav_paths.json` + macro con `QTimer`. Solo cambia **qué** se transporta (datos en vez de imagen)
y **cómo se pinta** (widget en vez de pixmap).

## Archivos a modificar

### 1. `Dav/scr/ComponentesDAV/InterfazDAV/capture_tree.FCMacro`
Reemplazar `capture_tree()` (que hace `pixmap.grab()` / `save PNG`) por una función que serialice
el árbol del documento activo:
- Recorrer `App.ActiveDocument.Objects`.
- Por cada objeto: `Name`, `Label`, `TypeId`, visibilidad (`obj.ViewObject.Visibility` si hay GUI),
  y el grupo padre (`obj.getParentGroup()` si existe) para reconstruir jerarquía.
- Escribir el resultado en un archivo nuevo `tree_data.json` (ruta tomada de `dav_paths.json`,
  key nueva `tree_data_path`), y responder en el `signal_file` con
  `{"status":"done","result":{"success":true}}` igual que hoy.
- Mantener el `QTimer` de escucha y el patrón de señal intactos.

### 2. `Dav/scr/ComponentesDAV/InterfazDAV/trigger_capture.py`
- En `ensure_macro_installed()`: agregar `tree_data_path` al dict `paths` que se escribe en
  `dav_paths.json`.
- Limpiar `tree_data.json` viejo al iniciar (igual que hoy se limpia `tree_capture.png`).
- `trigger_capture()` no cambia (sigue mandando la señal `{"command":"capture"}` y esperando
  `status:done`).

### 3. `Dav/scr/ComponentesDAV/InterfazDAV/MainWindow.py`
Reemplazar el panel de imagen por un árbol de datos:
- **UI** (`_SetupUi`, panel "Árbol de FreeCAD"): cambiar `self._TreeImageLabel = QLabel()` por
  `self._TreeWidget = QTreeWidget()` (importar `QTreeWidget`, `QTreeWidgetItem`). Estilizar con la
  paleta `self._T` como el resto.
- **Borrar** la lógica de imagen: `_ShowPlaceholderImage`, `_RefreshTreeImage`, el `_RefreshTimer`
  (2s), y la parte de `resizeEvent` que reescala el pixmap.
- **Nuevo** `_RefreshTreeData()`: leer `tree_data.json` (si cambió por mtime, igual patrón que el
  viejo `_LastImageMtime`), limpiar el `QTreeWidget` y reconstruir items desde el JSON
  (label + tipo, e indentación por jerarquía). Conectar a un `QTimer` (puede reusar el de 2s).
- `_AutoCapture()` (5s) se mantiene: dispara la señal a la macro; solo que ahora la macro produce
  datos en vez de PNG.
- Ajustar `SetColor` / `_UpdateStyles` para reestilizar el `QTreeWidget` en vez del label de imagen.
- Quitar referencias muertas a `tree_capture.png` en `_CheckMacroStatus` (cambiar a chequear
  `tree_data.json`).

## Formato `tree_data.json` (contrato GUI↔macro)
```json
{
  "document": "Unnamed",
  "objects": [
    {"name": "Box", "label": "Cubo", "type": "Part::Box", "visible": true, "parent": null},
    {"name": "Fusion", "label": "Fusión", "type": "Part::MultiFuse", "visible": true, "parent": null}
  ]
}
```
v1: lista plana con `parent` (None o Name del grupo). El `QTreeWidget` anida por `parent`; objetos
sin padre van a la raíz.

## Reutilización
- Mecanismo de señal/config ya existente (`signal_file`, `dav_paths.json`, `QTimer` en la macro)
  — no se reinventa, solo se le agrega `tree_data_path`.
- Patrón de detección de cambios por `mtime` (como `_LastImageMtime`) se reaplica para
  `tree_data.json`.
- Paleta y QSS (`self._T`, `_PanelQss`) para estilar el árbol consistente con la GUI.

## Verificación
1. **Sin FreeCAD (rápido):** crear a mano un `tree_data.json` de ejemplo en la carpeta de InterfazDAV
   y lanzar la GUI standalone (`python main.py --gui` desde PruebaIntegracion, o el entrypoint de
   InterfazDAV) → el panel debe mostrar los objetos del JSON en el árbol, no la imagen.
2. **Con FreeCAD (real):** abrir FreeCAD con `iniciar_dav.ps1`, ejecutar la macro `capture_tree`,
   crear un par de objetos (Box, etc.). En ≤5s el `QTreeWidget` de la GUI debe listar esos objetos
   con su tipo. Crear/borrar objetos en FreeCAD y verificar que el árbol de la GUI se actualiza.
3. **Regresión:** historial, voz, temas y preferencias siguen funcionando (no se tocó `VoiceWorker`
   ni `AddToHistory`).

## Fuera de alcance (fases futuras)
- Navegar el árbol por voz (siguiente/anterior/seleccionar N).
- Selección bidireccional (seleccionar por voz → resaltar en el árbol real de FreeCAD).
- Borrar la maqueta muerta `Dav/scr/PruebaIntegracion/hilos/GestorDeHilos.py` (Tkinter, no usada)
  — limpieza aparte si se quiere.
