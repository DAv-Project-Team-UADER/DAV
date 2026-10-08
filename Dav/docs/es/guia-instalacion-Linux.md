# DAV — Guía de instalación (Linux)

**DAV (Diseño Asistido por Voz)** es un programa que te permite manejar **FreeCAD** con la voz. En lugar de hacer clic, decís comandos como _"vista frontal"_ o _"crear boceto"_ y DAV los ejecuta por vos.

DAV no es un programa aparte: **corre por dentro de FreeCAD**, como un módulo más. Por eso primero se instala FreeCAD, y después se agrega DAV.

---

## Elegí tu camino

Hay dos formas de instalar DAV en Linux, según lo que necesites hacer:

| Si querés… | Seguí este camino |
| :--- | :--- |
| **Solo usar DAV** sin tocar código | [Camino A → Usuario final](#camino-a--usuario-final) |
| **Trabajar con el código** del proyecto | [Camino B → Desarrolladores](#camino-b--desarrolladores) |

---

## Lo que necesitás en cualquiera de los dos caminos

| Necesitás | Para qué |
| :--- | :--- |
| **FreeCAD 1.1.4 (AppImage)** | Es el programa base. [Descargá el AppImage](https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage) y guardalo en tu carpeta de **Descargas** (o **Downloads**). |
| **Micrófono** | Para usar los comandos de voz. |
| **Internet** | Solo la primera vez: DAV descarga el modelo de voz Vosk (≈ 40 MB) y dependencias. |
| **Python 3.10+** | Generalmente ya viene instalado por defecto en distribuciones Linux modernas (Ubuntu, Mint, Fedora). Para crear el entorno de DAV también hace falta el paquete `python3-venv` (`sudo apt install python3 python3-venv python3-pip`). |

> **No hace falta** descargar modelos de voz manualmente. DAV se encarga de todo eso automáticamente la primera vez que lo abrís.

---

## Camino A — Usuario final 

Para quien **solo quiere usar DAV**, sin abrir el código ni usar la terminal. Es un solo archivo ejecutable.

### Paso 1 — Descargá FreeCAD
1. [Descargá FreeCAD 1.1.4 (AppImage para Linux)](https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage).
2. Si preferís otra versión, todas están en <https://www.freecad.org/downloads.php> (usá siempre la **1.x** en formato `.AppImage`).
3. Guardá el archivo exactamente en tu carpeta personal de **Descargas** (o **Downloads** si tu sistema está en inglés).
4. **IMPORTANTE:** Sin el AppImage de FreeCAD descargado, DAV no puede abrirse.

### Paso 2 — Bajá el instalador de DAV
Descargá el archivo **`DAV_Installer_1.0-Linux`**.

### Paso 3 — Dale permisos de ejecución
Por seguridad, Linux no ejecuta archivos descargados de internet con doble clic de inmediato. Hay que autorizarlo:
1. Hacé **clic derecho** sobre `DAV_Installer_1.0-Linux`.
2. Seleccioná **Propiedades**.
3. Andá a la pestaña **Permisos**.
4. Marcá la casilla **"Permitir ejecutar el archivo como un programa"** (o similar).
5. Cerrá la ventana.

### Paso 4 — Ejecutá el instalador
Hacé **doble clic** sobre `DAV_Installer_1.0-Linux` y seleccioná **Ejecutar**.
*(Si el doble clic no funciona en tu entorno, podés abrir la terminal en esa carpeta y escribir `./DAV_Installer_1.0-Linux`).*

El programa hará lo siguiente de forma automática:
1. Copia los archivos de DAV a tu carpeta de módulos de FreeCAD (`~/.local/share/FreeCAD/v1-1/Mod/`).
2. Instala las dependencias de voz y descarga el modelo en español.
3. **Abre FreeCAD** con el panel de DAV integrado.

> **Nota:** La primera vez puede tardar unos minutos por la descarga del modelo de voz.

### Paso 5 — ¡A usar DAV!
Cuando FreeCAD se abra, vas a ver el **panel de DAV** con el botón del micrófono. Decí **"vista frontal"** para probarlo. 

Para volver a abrirlo en el futuro, simplemente ejecutá nuevamente el archivo `DAV_Installer_1.0-Linux` (detectará que ya está instalado y abrirá FreeCAD directamente).

---

## Camino B — Desarrolladores 

Para **compañeros del equipo** que necesitan acceder al código fuente, modificarlo y probar los cambios en tiempo real.

### 1. Instalá los prerrequisitos
* Asegurate de tener **Git** instalado (`sudo apt install git`).
* Tener **Python 3.10+** con venv y pip: `sudo apt install python3 python3-venv python3-pip`.
* [Descargá el **AppImage de FreeCAD 1.1.4**](https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage) y dejalo en tu carpeta `~/Descargas/`.

### 2. Cloná el repositorio
Abrí una terminal y ejecutá:
```bash
git clone https://github.com/DAv-Project-Team-UADER/DAV.git
cd DAV
```

### 3. Ejecutá el instalador
Dentro de la carpeta del proyecto que acabás de clonar, ejecutá el instalador:
```bash
chmod +x LinuxInstaller.sh iniciar_dav.sh
./LinuxInstaller.sh
```

El instalador prepara todo de forma automática, sin pasos manuales:
1. Crea el entorno virtual (`GUIFreeCad/.venv`) e instala las dependencias de voz (`PySide6`, `Vosk`, `sounddevice`, …).
2. Descarga los modelos de voz Vosk en `Dav/models/` (si ya están, no los vuelve a descargar).
3. Crea un enlace simbólico de tu código fuente hacia `~/.local/share/FreeCAD/v1-1/Mod/DAV`.
4. Crea los accesos directos: `ejecutar.desktop` en la carpeta del proyecto, una entrada **DAV** en el menú de aplicaciones y, la primera vez, `DAV_V1.desktop` en el Escritorio.

### 4. Abrí DAV
Hacé doble clic en el acceso directo **DAV** (o ejecutá `./iniciar_dav.sh` en la terminal). El script busca la AppImage de FreeCAD en tu carpeta de Descargas, usando una ruta universal (`$HOME`), y lanza FreeCAD con tu código cargado. Cualquier cambio que guardes en el código de Python se reflejará al reiniciar FreeCAD.

Opciones útiles de `iniciar_dav.sh`:
```bash
./iniciar_dav.sh /ruta/a/FreeCAD.AppImage   # usar un FreeCAD específico
./iniciar_dav.sh --install-only             # solo preparar el entorno, sin abrir FreeCAD
./iniciar_dav.sh --skip-models              # no descargar los modelos de voz
```

---

## Problemas frecuentes 

| Problema | Solución |
| :--- | :--- |
| **"Permiso denegado" al hacer doble clic** | Te faltó el Paso 3 del Camino A. Clic derecho en el archivo > Propiedades > Permisos > Permitir ejecutar como programa. |
| **"No se encuentra FreeCAD"** | Verificá que el archivo de FreeCAD termine en `.AppImage` y esté directamente en la carpeta `Descargas` (o `Downloads`). |
| **"No se pudo crear GUIFreeCad/.venv"** | Falta el paquete de entornos virtuales. Ejecutá `sudo apt install python3-venv python3-pip` y volvé a correr el instalador. |
| **El micrófono no responde / Error de Vosk** | Es posible que falten dependencias de audio en Linux. Abrí una terminal y ejecutá `sudo apt install libportaudio2 portaudio19-dev python3-pyaudio`. |
| **La primera vez tarda mucho** | Es normal, está descargando el modelo de voz en segundo plano. |