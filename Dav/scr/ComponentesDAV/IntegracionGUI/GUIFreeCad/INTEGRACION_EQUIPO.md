# GUIFreeCad + DAV-Luigi — Guía para el equipo

Esta guía explica cómo clonar, instalar y probar la integración **Preferencias DAV + voz CAD** sin modificar el código core de `PruebaIntegracion` del equipo.

## Arquitectura (resumen)

```
Micrófono único (GUIFreeCad)
        │
        ├─ Modo CAD      → diccionario PruebaIntegracion (archivo enviar, nuevo enviar, …)
        └─ Modo Preferencias → tema oscuro, aplicar, idioma, …
```

- **GUIFreeCad** (este repo): preferencias, motor de voz unificado, adaptador CAD, puente Qt.
- **DAV-Luigi** (repo del equipo, rama `Pruebas`): workbench FreeCAD + `PruebaIntegracion` + diccionario.
- **No hace falta** parchear `Comando.py`, `ExploradorVoz.py`, etc. La integración vive acá.

---

## Layout de carpetas en la PC

Hay **dos formas válidas** (el script y las rutas las detectan solas):

### Opción A — Un solo clone del equipo (recomendada para compañeros)

Todo el paquete de integración vive en **`luigiIntegracionV1/`**:

```
DAV-Luigi/                    ← un solo git clone
├── luigiIntegracionV1/
│   ├── GUIFreeCad/            ← preferencias + voz unificada
│   ├── iniciar_dav.ps1
│   └── iniciar_dav.bat
├── Dav/
├── PruebaIntegracion/
└── scripts/
```

### Opción B — Dos repos hermanos (desarrollo local)

```
Repositorio DAVFreeCad/
├── GUIFreeCad/
└── DAVFreecad-Pruebas/DAV-Luigi/
```

Variable opcional si la ruta no se detecta:

```text
DAV_GUI_FREECAD_ROOT=C:\ruta\completa\a\GUIFreeCad
```

---

## ¿Subir GUIFreeCad al repo del equipo?

**Sí, pero la carpeta entera `GUIFreeCad/`**, no un subconjunto de archivos.

| Enfoque | ¿Conviene? |
|---------|------------|
| Carpeta completa `DAV-Luigi/GUIFreeCad/` | **Sí** — un clone y listo |
| Git submodule apuntando a tu repo | **Sí** — historial separado, `git clone --recursive` |
| Copiar solo `integration/` o 5 `.py` | **No** — falta UI, i18n, modelos, `main.py`, etc. |

Cada integrante sigue ejecutando `python scripts/setup_models.py` dentro de `GUIFreeCad` (modelos Vosk no van al git).

### Cómo subirlo (para vos o un PR al equipo)

```powershell
# Desde tu GUIFreeCad, copiar al repo del equipo (sin .venv ni modelos)
robocopy "GUIFreeCad" "DAV-Luigi\GUIFreeCad" /E /XD .venv __pycache__ models /XF settings.json
cd DAV-Luigi
git add GUIFreeCad
git commit -m "Añadir GUIFreeCad (preferencias y motor de voz unificado)."
```

O con **submódulo** (más prolijo a largo plazo):

```powershell
cd DAV-Luigi
git submodule add <URL-de-tu-repo-GUIFreeCad> GUIFreeCad
```

---

## Requisitos

| Componente | Versión / nota |
|------------|----------------|
| Windows | Probado en Win 10/11 |
| FreeCAD | Ej. `L:\Programas\Freecad\bin\FreeCAD.exe` |
| Python 3.10+ | Para venv de GUIFreeCad y scripts |
| Micrófono | Permisos en Windows |
| Git | Clone del repo DAV-Luigi (con `GUIFreeCad/` incluido o submodule) |

---

## Instalación paso a paso

### 1. Clonar repositorio

**Si GUIFreeCad ya está dentro de DAV-Luigi** (opción A):

```powershell
git clone https://github.com/Elluis1/DAV-Luigi.git
cd DAV-Luigi
git checkout Pruebas
# Si usaron submodule:
git submodule update --init --recursive
```

**Si trabajás con dos repos** (opción B):

```powershell
mkdir "C:\ruta\Repositorio DAVFreeCad"
cd "C:\ruta\Repositorio DAVFreeCad"

git clone <URL-REPO-GUIFreeCad> GUIFreeCad
git clone https://github.com/Elluis1/DAV-Luigi.git "DAVFreecad-Pruebas\DAV-Luigi"
cd "DAVFreecad-Pruebas\DAV-Luigi"
git checkout Pruebas
```

### 2. Dependencias y modelos Vosk (GUIFreeCad)

```powershell
cd "..\..\GUIFreeCad"
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python scripts/setup_models.py
```

Los modelos Vosk **no van al git** (`.gitignore`). Cada integrante debe ejecutar `setup_models.py` una vez.

### 3. Dependencias de voz en el Python de FreeCAD

```powershell
cd "..\DAVFreecad-Pruebas\DAV-Luigi\scripts"
.\check_freecad_deps.ps1 -FreeCADExe "L:\Programas\Freecad\bin\FreeCAD.exe" -Install
```

Instala `vosk` y `sounddevice` en el intérprete embebido de FreeCAD (no en el venv de GUIFreeCad).

### 4. Instalar workbench DAV en FreeCAD

```powershell
.\run_freecad_dav.ps1 -FreeCADExe "L:\Programas\Freecad\bin\FreeCAD.exe" -InstallOnly
```

Crea un junction `Mod\DAV` → `DAV-Luigi\Dav`. Requiere permisos de admin en el Mod del sistema; si falla, el script usa el Mod del usuario.

### 5. (Opcional) Verificar entorno

```powershell
.\verificar_pasos.ps1 -FreeCADExe "L:\Programas\Freecad\bin\FreeCAD.exe"
```

---

## Ejecutar FreeCAD con DAV

**Recomendado — un solo comando** (desde la raíz del repo, después de clonar):

```powershell
cd DAV-Luigi
git checkout Pruebas
.\iniciar_dav.ps1 -FreeCADExe "L:\Programas\Freecad\bin\FreeCAD.exe"
```

O desde `luigiIntegracionV1\` con el mismo script. Doble clic en `iniciar_dav.bat`.

**Alternativa manual** (solo el lanzador):

```powershell
cd "...\DAV-Luigi\scripts"
.\run_freecad_dav.ps1 -FreeCADExe "L:\Programas\Freecad\bin\FreeCAD.exe"
```

Al cargar el workbench **DAV**:

- Mensajes `[DAV]` → pestaña **Informe** (Ver → Informe), **no** la consola Python `>>>`.
- Barra **DAV**: Preferencias DAV, Iniciar voz DAV, Detener voz DAV.

---

## Uso de voz

### Activar

1. Clic en **Iniciar voz DAV**, o  
2. Preferencias DAV → activar **Arranque de voz al abrir FreeCAD** y reiniciar.

### Comandos CAD (diccionario del equipo)

Patrón: **`comando` + `enviar`** en la misma frase.

| Decís | Efecto |
|-------|--------|
| `archivo enviar` | Menú Archivo |
| `nuevo enviar` | Documento nuevo (después de entrar a Archivo, o con alias) |
| `editar enviar` | Menú Editar |
| `deshacer enviar` | Deshacer |
| `preferencias enviar` | Abre Preferencias DAV |
| `actualizar enviar` | Refrescar vista |

Alias en español (`archivo`, `nuevo`, `preferencias`, …): `integration/voice_aliases.py`.

**No existe** `dav enviar`.

### Comandos en Preferencias (solo con el diálogo abierto)

- `tema oscuro`, `tema claro`, `modelo pequeño`, `aplicar`, etc.

---

## Probar solo GUIFreeCad (sin FreeCAD)

```powershell
cd GUIFreeCad
.\.venv\Scripts\activate
python main.py
```

Útil para probar preferencias y voz standalone; **no** reemplaza la prueba en FreeCAD.

---

## Solución de problemas

| Problema | Qué hacer |
|----------|-----------|
| No aparece barra DAV / voz | `run_freecad_dav.ps1 -InstallOnly` y reiniciar FreeCAD |
| `ModuleNotFoundError: PruebaIntegracion` | Verificar layout de carpetas y `DAV_GUI_FREECAD_ROOT` |
| Sin reconocimiento | `setup_models.py` + permisos de micrófono |
| `import vosk` en FreeCAD | `check_freecad_deps.ps1 -Install` |
| Error Qt / hilo | Actualizar GUIFreeCad (comandos CAD van al hilo principal) |
| Micrófono muerto tras Preferencias | Detener/Iniciar voz o reiniciar FreeCAD; revisar versión reciente de GUIFreeCad |

---

## Qué commitea cada parte del repo

| Carpeta | Responsable | Contenido |
|---------|-------------|-----------|
| **GUIFreeCad/** | Equipo (GUI + integración) | Preferencias, motor de voz unificado, adaptador CAD |
| **Dav/, PruebaIntegracion/** | Equipo | Workbench FreeCAD, diccionario CAD, scripts de arranque |

Contacto integración: revisar `integration/` y `speech/dav_voice_service.py` en GUIFreeCad.
