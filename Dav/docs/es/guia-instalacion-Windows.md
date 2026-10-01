# DAV — Guía de instalación

**DAV (Diseño Asistido por Voz)** es un programa que te permite manejar **FreeCAD** con la
voz. En lugar de hacer clic, decís comandos como _"vista frontal"_ o _"crear boceto"_ y DAV
los ejecuta por vos.

DAV no es un programa aparte: **corre por dentro de FreeCAD**, como un módulo más. Por eso
primero se instala FreeCAD, y después se agrega DAV.

---

## Elegí tu camino

Hay dos formas de instalar DAV, según lo que quieras hacer:

| Si querés…                                                | Seguí este camino                                                        |
| --------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Solo usar DAV** sin tocar código (Windows)              | [Camino A → usuario final](#camino-a--usuario-final-windows)             |
| **Trabajar con el código** del proyecto (Windows o Linux) | [Camino B → desarrolladores](#camino-b--desarrolladores-windows-y-linux) |

---

## Lo que necesitás en cualquiera de los dos caminos

| Necesitás        | Para qué                                                                                                                                                             |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FreeCAD 1.x**  | Es el programa que maneja DAV. Es **gratis** y está en <https://www.freecad.org/downloads.php>. DAV **no lo incluye**: hay que instalarlo antes.                     |
| **Micrófono**    | Para usar los comandos de voz.                                                                                                                                       |
| **Internet**     | Solo la primera vez: DAV descarga el modelo de voz Vosk (≈ 40 MB).                                                                                                   |
| **Python 3.10+** | Solo la primera vez: DAV lo usa para crear su entorno de voz. Si no lo tenés, instalalo desde <https://www.python.org/downloads/> marcando **"Add Python to PATH"**. |

> **No hace falta** descargar nada más: ni el código de FreeCAD, ni modelos de voz, ni
> editores. DAV se encarga de todo eso solo, la primera vez.

---

## Camino A — Usuario final (Windows)

Para quien **solo quiere usar DAV**, sin abrir el código. Es un solo archivo con doble clic.

### Paso 1 — Instalá FreeCAD

1. Entrá a <https://www.freecad.org/downloads.php>.
2. Bajá e instalá la versión **1.x** (Windows, 64 bits).
3. **IMPORTANTE:** DAV no trae FreeCAD adentro. Sin FreeCAD instalado, DAV no puede abrirse.

### Paso 2 — Bajá el instalador de DAV

Bajá el archivo **`DAV_Installer_1.0.exe`**.

### Paso 3 — Ejecutá el instalador

Hacé **doble clic** sobre `DAV_Installer_1.0.exe`.

**¿Windows dice "Windows protegió su equipo"?**
El instalador todavía no está firmado digitalmente (es normal). Para que corra:

1. Hacé clic en **"Más información"**.
2. Después en **"Ejecutar de todas formas"**.

### Paso 4 — Dejalo trabajar (mayormente solo)

Aparece una **ventana negra** (la consola) que va mostrando en verde los pasos que cumple:

1. Copia DAV a tu carpeta de usuario.
2. Crea el entorno de voz (instala lo que faltaba).
3. Descarga el modelo de voz **en español**.
4. **Abre FreeCAD** con el panel de DAV activo.

> La **primera vez puede tardar entre 5 y 15 minutos**: es la descarga de los modelos y las
> dependencias. No cierres la ventana negra. Las siguientes veces es casi instantáneo.

### Paso 5 — ¡A usar DAV!

Cuando FreeCAD se abra, vas a ver el **panel de DAV** (con el botón del micrófono).

Probá hablar: **"vista frontal"**. La vista debe cambiar. Eso es todo — ya estás usando DAV.

### Para volver a abrir DAV después

Hacé doble clic en: **`%USERPROFILE%\DAV\iniciar_dav.bat`**
(o volvé a ejecutar el instalador: se da cuenta de que ya está todo y solo abre FreeCAD).

---

## Camino B — Desarrolladores (Windows y Linux)

Para **compañeros del equipo** que quieren trabajar con el código de DAV y modificarlo.

### Windows — instalación desde el repositorio

#### 1. Instalá los prerrequisitos

- **Git** → <https://git-scm.com/downloads>
- **FreeCAD 1.x** → <https://www.freecad.org/downloads.php>
- **Python 3.10+** → <https://www.python.org/downloads/> (marcá **"Add Python to PATH"**)

#### 2. Cloná el repositorio

```bat
git clone https://github.com/DAv-Project-Team-UADER/DAV.git
cd DAV
```

#### 3. Abrí el launcher

Hacé **doble clic** en **`iniciar_dav.bat`** (o ejecutalo desde la terminal).

El launcher hace lo mismo que el instalador del Camino A, pero usando tu copia del código:

1. Detecta el Python del sistema y crea el entorno virtual local.
2. Instala las dependencias de voz (`PySide6`, `Vosk`, `sounddevice`, …).
3. Descarga los modelos de voz si faltan.
4. Encuentra tu `FreeCAD.exe` y enlaza el workbench DAV dentro de FreeCAD.
5. Abre FreeCAD con tu código cargado.

#### Opciones útiles del launcher

Si necesitás más control, convertilo en la terminal:

```powershell
# Probar con un FreeCAD específico
.\iniciar_dav.ps1 -FreeCADExe "C:\ruta\bin\FreeCAD.exe"

# Solo preparar el entorno, sin abrir FreeCAD
.\iniciar_dav.ps1 -InstallOnly

# Controlar la voz al arrancar
.\iniciar_dav.ps1 -StartVoice
.\iniciar_dav.ps1 -NoStartVoice
```

### Linux — instalación desde el repositorio

1. Bajá la AppImage de FreeCAD **1.1.3** a `~/Descargas/`.
2. Cloná el repositorio:

   ```bash
   git clone https://github.com/DAv-Project-Team-UADER/DAV.git
   cd DAV
   ```

3. Ejecutá el launcher de Linux:

   ```bash
   chmod +x iniciar_dav.sh
   ./iniciar_dav.sh
   ```

El script crea el enlace del workbench DAV en
`~/.local/share/FreeCAD/v1-1/Mod/DAV` y abre FreeCAD.

> Explicación paso a paso y solución de problemas de Linux: ver
> **`Dav/docs/README-linux.md`**.

---

## Problemas frecuentes (ambos caminos)

| Problema                            | Solución                                                                                                            |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Windows dice "protegió su equipo"   | Clic en **"Más información"** → **"Ejecutar de todas formas"** (es porque el instalador no está firmado aún).       |
| Dice "No se encontró FreeCAD.exe"   | FreeCAD no está instalado (o en otra ruta). Instalalo, o pasá la ruta con `-FreeCADExe` (Camino B).                 |
| Dice "No se encontró Python 3"      | Instalá Python 3.10+ marcando **"Add Python to PATH"**.                                                             |
| La primera vez tarda mucho          | Es normal: descarga los modelos de voz. No cierres la ventana.                                                      |
| El micrófono no responde en FreeCAD | Faltan librerías de voz en el Python de FreeCAD. Volvé a correr `iniciar_dav.bat` y dejala reinstalar dependencias. |

---

## Documentación relacionada

| Tema                                                                                                  | Dónde está                                          |
| ----------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Guía de Linux detallada                                                                               | `Dav/docs/README-linux.md`                          |
| **Documentación técnica del instalador** (cómo se generó el `.exe`, cómo funciona y cómo regenerarlo) | `Dav/scr/ComponentesDAV/scripts/iexpress/README.md` |
