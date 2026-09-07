# Instalador Windows de DAV — Documentación técnica

Esta documentación explica **cómo se construye el instalador** de DAV para Windows, cómo
funciona por dentro y cómo regenerarlo. Está pensada para integrantes del equipo que quieran
mantener el instalador.

> Si lo que buscás es **instalar DAV**, no leas esto: usá la
> [Guía de instalación](../../../../docs/guia-instalacion.md) (Camino A o B).

---

## 1. Qué es el instalador

`DAV_Installer_1.0.exe` es un **auto-extraíble de IExpress** (herramienta que viene con
Windows, no hay que instalar nada). Al ejecutarlo:

1. Extrae en una carpeta temporal tres archivos:
   - `payload.zip` — todo el código de DAV comprimido.
   - `bootstrap.cmd` — disparador de Windows.
   - `bootstrap.ps1` — el instalador real (descomprime y arranca).
2. Ejecuta el bootstrap.
3. El bootstrap instala DAV y abre FreeCAD.

El instalador **no incluye** FreeCAD (se descarga aparte), ni los modelos de voz (se
descargan en la primera ejecución), ni los entornos virtuales.

---

## 2. Cómo funciona por dentro

```
DAV_Installer_1.0.exe  (IExpress)
   │ extrae a %TEMP%
   ▼
bootstrap.cmd
   │  powershell -file bootstrap.ps1
   ▼
bootstrap.ps1
   │  Expand-Archive payload.zip → %USERPROFILE%\DAV
   ▼
iniciar_dav.bat  (del repo instalado)
   │
   ▼
iniciar_dav.ps1
   │  1. crea GUIFreeCad\.venv (Python del sistema)
   │  2. pip install -r requirements.txt  (PySide6, Vosk, sounddevice, …)
   │  3. descarga modelos Vosk → Dav\models\ (solo la primera vez)
   │  4. enlaza el workbench DAV en el Mod de FreeCAD (junction)
   │  5. abre FreeCAD con el panel DAV
   ▼
FreeCAD + DAV listos
```

### Por qué el código viaja dentro de un zip

**IExpress aplana el árbol de archivos** al empaquetar: no conserva subcarpetas. Si se le
pasaran los archivos sueltos, el instalador quedaría un desorden plano.

Por eso el repo completo se comprime primero en **`payload.zip`** (que sí conserva la
estructura de carpetas) y IExpress envuelve **ese único archivo** más los dos bootstrap.

### Por qué los bootstraps son archivos aparte

- `AppLaunched` (lo que IExpress ejecuta) tiene un **límite de longitud**; un comando largo
  inline falla. Por eso apunta a algo corto: `cmd.exe /c bootstrap.cmd`.
- `bootstrap.cmd` solo invoca a `bootstrap.ps1` (que hace el trabajo), separando el disparo
  de Windows de la lógica de PowerShell.

---

## 3. Archivos involucrados

| Archivo                                                                                            | Rol                                               |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `scripts\build_iexpress_installer.ps1`                                                             | Generador: arma el payload, el SED y compila el exe. |
| `scripts\iexpress\bootstrap.ps1`                                                                   | Instalador real (descomprime + arranca).          |
| `scripts\iexpress\bootstrap.cmd`                                                                   | Disparador de la consola.                         |
| `scripts\iexpress\dav_installer.sed` *(generado, en `build\iexpress\pkg\`)*                        | Plantilla de opciones que lee IExpress.           |
| `build\iexpress\pkg\payload.zip` *(generado)*                                                      | Repo de DAV comprimido, sin excluidos.            |
| `build\iexpress\DAV_Installer_<versión>.exe` *(generado)*                                          | El instalador final.                              |

---

## 4. Cómo regenerar el instalador

El generador empaqueta el repo (excluyendo lo pesado), comprime el payload, copia los
bootstrap y compila con IExpress en modo silencioso.

```powershell
# Desde cualquier lado (detecta la raíz del repo solo)
cd Dav\scr\ComponentesDAV\scripts
.\build_iexpress_installer.ps1                # genera DAV_Installer_1.0.exe
.\build_iexpress_installer.ps1 -Version "1.1" # versiona la salida
```

Salida: `build\iexpress\DAV_Installer_<versión>.exe`.

Al regenerar, el payload **siempre incluye los `.md` y scripts actuales** — por eso, si
cambiás la guía o el código, alcanza con regenerar el exe para que la nueva versión viaje
en el instalador.

### Excluidos del payload

Se copia el repo con `robocopy /E` excluyendo:

- Carpetas: `.git`, `FREECAD`, `models`, `.venv`, `__pycache__`, `build`/`dist`/`out`.
- Tipos de archivo: `*.pyc`, `*.pyo`, `*.log`, `*.FCBak`, `*.lock`.

Los modelos y el entorno se recrean solos en la primera ejecución (la descarga es lo que
tarda los 5-15 min de la primera instalación).

---

## 5. Particularidades de IExpress (por qué el SED está como está)

- **No firma el exe** ⟶ Windows muestra "Windows protegió su equipo". Se documenta en la
  guía de usuario hasta que se firme con certificado.
- **SED en ASCII**: si el `.sed` se guarda en UTF-16/Unicode, IExpress lo rechaza.
- **AppLaunched corto**: `cmd.exe /c bootstrap.cmd` (por el límite de longitud).
- **`ShowInstallProgramWindow=2`**: muestra la consola del instalador al usuario.
- **Invocación silenciosa**: `iexpress /N /Q <nombre.sed>` con el directorio de trabajo en
  la carpeta del paquete. Como IExpress es una app GUI, hay que esperarla vía `cmd /c`
  para capturar su código de salida (ver `Invoke-IExpressBuild`).

### Esquema del SED

El SED usa el formato *wizard*: `[Options]` con placeholders `%…%`, los valores reales en
`[Strings]`, y las fuentes en `[SourceFiles]`/`[SourceFiles0]` mapeando archivos con
`%FILE<n>% =`. El extracto clave:

```
AppLaunched=cmd.exe /c bootstrap.cmd
FILE0="bootstrap.cmd"
FILE1="bootstrap.ps1"
FILE2="payload.zip"
[SourceFiles]
SourceFiles0=<pkg>\
[SourceFiles0]
%FILE0%=
%FILE1%=
%FILE2%=
```

---

## 6. Verificar un instalador recién generado

Pruebas rápidas por consola, sin instalar nada:

```powershell
# 1) El exe extrae los 3 archivos esperados (sin ejecutar la instalación)
$dir = "$env:TEMP\dav_probe"
New-Item -ItemType Directory -Force $dir | Out-Null
& ".\build\iexpress\DAV_Installer_1.0.exe" "/T:$dir" "/C"
Get-ChildItem $dir   # debe listar: bootstrap.cmd, bootstrap.ps1, payload.zip

# 2) El payload trae el código esperado y nada de lo excluido
powershell -Command "Add-Type -AssemblyName System.IO.Compression.FileSystem; $z=[System.IO.Compression.ZipFile]::OpenRead('$dir\payload.zip'); $z.Entries.FullName; $z.Dispose()"
```

Debe aparecer `Dav\dic\base.py`, `Dav\scr\ComponentesDAV\Dav\InitGui.py`, la guía
`Dav\docs\guia-instalacion.md`, y **no** debe aparecer `FREECAD\`, `.venv` ni `Dav\models\`.

---

## 7. Notas de mantenimiento

- **La guía de usuario y el README técnico viven en el repo** (no en `build/`): `build/`
  está en `.gitignore`, así que el `.exe` y el `payload.zip` **no se commitean**.
- Si se firman el exe, revisar también el mensaje de SmartScreen en la guía de usuario.
- Los archivos de este README (`build_iexpress_installer.ps1`, `bootstrap.*`) se siguen por
  git: estaban excluidos por `ComponentesDAV/` en `.gitignore`, y se habilitaron con las
  negaciones del final de ese archivo.