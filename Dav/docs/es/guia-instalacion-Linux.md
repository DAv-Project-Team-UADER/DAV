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
| **Conexión a Internet** | **Obligatoria durante la instalación** (la primera vez): se instalan paquetes del sistema y dependencias de Python, y se descarga el modelo de voz Vosk (≈ 40 MB). |
| **Contraseña de administrador (sudo)** | La primera vez, el instalador la pide **una sola vez** para instalar paquetes del sistema (audio, FUSE) y dar permisos de micrófono. Al escribirla no se ve nada en pantalla: es normal. |
| **Python 3.10+** | Generalmente ya viene instalado por defecto en distribuciones Linux modernas (Ubuntu, Mint, Fedora). Para crear el entorno de DAV también hace falta el paquete `python3-venv` (`sudo apt install python3 python3-venv python3-pip`). |

> **Importante:** sin conexión a Internet la instalación falla. Una vez instalado, DAV funciona sin conexión.

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

El instalador prepara todo de forma automática. **Te pide la contraseña de administrador (`sudo`) una sola vez**, porque algunos pasos instalan paquetes del sistema y dan permisos de audio:
1. Crea el entorno virtual (`GUIFreeCad/.venv`) e instala las dependencias de voz (`PySide6`, `Vosk`, `sounddevice`, …).
2. Descarga los modelos de voz Vosk en `Dav/models/` (si ya están, no los vuelve a descargar).
3. Crea un enlace simbólico de tu código fuente hacia `~/.local/share/FreeCAD/v1-1/Mod/DAV`.
4. Crea los accesos directos: `ejecutar.desktop` en la carpeta del proyecto, una entrada **DAV** en el menú de aplicaciones y `DAV_V1.desktop` en el Escritorio (si todavía no existe).
5. Instala los paquetes de audio del sistema (PortAudio, ALSA) y, si falta, `libfuse2`, que el AppImage de FreeCAD necesita para abrirse.
6. Instala las dependencias de voz (`sounddevice`, `vosk`) también para el Python de FreeCAD, en `GUIFreeCad/.freecad_deps`.
7. Agrega tu usuario al grupo `audio`, para que pueda usar el micrófono. Si lo agrega, **cerrá sesión y volvé a entrar una vez** para que tenga efecto.
8. Revisa tu equipo y te avisa, sin frenar la instalación, si no hay micrófono, si no hay uno por defecto o si la CPU no ofrece AVX (Vosk lo necesita).

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
| **El micrófono no responde / Error de Vosk** | Ejecutá `./iniciar_dav.sh` desde la terminal y mirá los avisos del paso del micrófono. Si el instalador te agregó al grupo `audio`, cerrá sesión y volvé a entrar. Si aun así falla, instalá a mano: `sudo apt install libportaudio2 portaudio19-dev python3-pyaudio`. |
| **"No se detectó ningún micrófono"** | DAV abre pero no puede escuchar. En una **máquina virtual** hay que habilitar el audio de entrada: en VMware, la tarjeta de sonido (*Sound Card*) de la VM conectada y el micrófono del equipo anfitrión disponible; en VirtualBox, *Configuración > Audio > Habilitar entrada de audio*. En una PC, conectá un micrófono y elegilo como entrada en los ajustes de sonido (`pavucontrol`). |
| **"La CPU no ofrece AVX" / `Illegal instruction`** | Vosk usa instrucciones AVX. En una máquina virtual, usá una versión de hardware reciente y activá la virtualización de CPU (podés comprobarlo con `grep -w avx /proc/cpuinfo`). DAV sigue abierto y muestra el error en el Informe de FreeCAD; sin AVX el reconocimiento de voz no puede funcionar. |
| **FreeCAD no abre o no pasa nada al lanzarlo (FUSE)** | El AppImage necesita `libfuse2`. El instalador intenta instalarla; si no puede, DAV ejecuta el AppImage sin FUSE (tarda más en abrir). A mano: `sudo apt install libfuse2` (en Ubuntu 24.04 se llama `libfuse2t64`). |
| **La primera vez tarda mucho** | Es normal, está descargando el modelo de voz en segundo plano. |

## Si algo falla: qué revisar y qué enviar

DAV guarda registros en `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/config/`:

| Archivo | Qué contiene |
| :--- | :--- |
| `dav.log` | Lo que hace DAV: arranque de la voz, errores y avisos. Es lo primero que hay que mirar. |
| `dav_fault.log` | Se crea si FreeCAD se cierra de golpe por una falla nativa; guarda en qué punto del código estaba. |

En Linux el reconocimiento de voz corre en un **proceso aparte**: si ese proceso se cae, FreeCAD sigue abierto y el motivo aparece en el Informe de FreeCAD y en `dav.log`.

Para reportar un problema, enviá:
1. Las últimas líneas de `dav.log` (y el contenido de `dav_fault.log`, si existe).
2. Lo que muestra la terminal al abrir con `./iniciar_dav.sh`.
3. Tu versión de Ubuntu/Lubuntu y si es una máquina virtual.
