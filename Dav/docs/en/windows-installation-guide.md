# DAV — Installation Guide

**DAV (Voice-Assisted Design, "Diseño Asistido por Voz")** is a program that lets you control **FreeCAD** with your
voice. Instead of clicking, you say commands like _"vista frontal"_ (front view) or _"crear boceto"_ (create sketch) and DAV
runs them for you.

DAV is not a separate program: it **runs inside FreeCAD**, as one more module. That is why
you install FreeCAD first, and then add DAV.

---

## Choose your path

There are two ways to install DAV, depending on what you want to do:

| If you want to…                                           | Follow this path                                                         |
| --------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Just use DAV** without touching code (Windows)          | [Path A → end user](#path-a--end-user-windows)                    |
| **Work on the project's code** (Windows or Linux)         | [Path B → developers](#path-b--developers-windows-and-linux)        |

---

## What you need on either path

| You need         | What for                                                                                                                                                             |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FreeCAD 1.x**  | It is the program DAV controls. It is **free** and available at <https://www.freecad.org/downloads.php>. DAV **does not include it**: you must install it first.     |
| **Microphone**   | To use the voice commands.                                                                                                                                           |
| **Internet**     | Only the first time: DAV downloads the Vosk voice model (≈ 40 MB).                                                                                                   |
| **Python 3.10+** | Only the first time: DAV uses it to create its voice environment. If you do not have it, install it from <https://www.python.org/downloads/> checking **"Add Python to PATH"**. |

> You **do not need** to download anything else: no FreeCAD source code, no voice models, no
> editors. DAV takes care of all of that by itself, the first time.

---

## Path A — End user (Windows)

For those who **just want to use DAV**, without opening the code. It is a single file with a double click.

### Step 1 — Install FreeCAD

1. Go to <https://www.freecad.org/downloads.php>.
2. Download and install the **1.x** version (Windows, 64-bit).
3. **IMPORTANT:** DAV does not bundle FreeCAD. Without FreeCAD installed, DAV cannot open.

### Step 2 — Get the DAV installer

Download the file **`DAV_Installer_1.0.exe`**.

### Step 3 — Run the installer

**Double-click** `DAV_Installer_1.0.exe`.

**Does Windows say "Windows protected your PC"?**
The installer is not digitally signed yet (this is normal). To let it run:

1. Click **"More info"**.
2. Then **"Run anyway"**.

### Step 4 — Let it work (mostly on its own)

A **black window** (the console) appears and shows in green the steps it carries out:

1. Copies DAV to your user folder.
2. Creates the voice environment (installs whatever was missing).
3. Downloads the **Spanish** voice model.
4. **Opens FreeCAD** with the DAV panel active.

> The **first time it can take between 5 and 15 minutes**: it is the download of the models and
> dependencies. Do not close the black window. The following times it is almost instant.

### Step 5 — Start using DAV!

When FreeCAD opens, you will see the **DAV panel** (with the microphone button).

Try speaking: **"vista frontal"** (front view). The view should change. That is all — you are now using DAV.

### To open DAV again later

Double-click: **`%USERPROFILE%\DAV\iniciar_dav.bat`**
(or run the installer again: it notices that everything is already in place and just opens FreeCAD).

---

## Path B — Developers (Windows and Linux)

For **team members** who want to work with DAV's code and modify it.

### Windows — installation from the repository

#### 1. Install the prerequisites

- **Git** → <https://git-scm.com/downloads>
- **FreeCAD 1.x** → <https://www.freecad.org/downloads.php>
- **Python 3.10+** → <https://www.python.org/downloads/> (check **"Add Python to PATH"**)

#### 2. Clone the repository

```bat
git clone https://github.com/DAv-Project-Team-UADER/DAV.git
cd DAV
```

#### 3. Open the launcher

**Double-click** **`iniciar_dav.bat`** (or run it from the terminal).

The launcher does the same as the Path A installer, but using your copy of the code:

1. Detects the system Python and creates the local virtual environment.
2. Installs the voice dependencies (`PySide6`, `Vosk`, `sounddevice`, …).
3. Downloads the voice models if they are missing.
4. Finds your `FreeCAD.exe` and links the DAV workbench inside FreeCAD.
5. Opens FreeCAD with your code loaded.

#### Useful launcher options

If you need more control, run it from the terminal:

```powershell
# Try with a specific FreeCAD
.\iniciar_dav.ps1 -FreeCADExe "C:\path\bin\FreeCAD.exe"

# Only prepare the environment, without opening FreeCAD
.\iniciar_dav.ps1 -InstallOnly

# Control voice at startup
.\iniciar_dav.ps1 -StartVoice
.\iniciar_dav.ps1 -NoStartVoice
```

### Linux — installation from the repository

1. Download the FreeCAD **1.1.3** AppImage to `~/Descargas/`.
2. Clone the repository:

   ```bash
   git clone https://github.com/DAv-Project-Team-UADER/DAV.git
   cd DAV
   ```

3. Run the Linux launcher:

   ```bash
   chmod +x iniciar_dav.sh
   ./iniciar_dav.sh
   ```

The script creates the link to the DAV workbench in
`~/.local/share/FreeCAD/v1-1/Mod/DAV` and opens FreeCAD.

> Step-by-step explanation and Linux troubleshooting: see
> **`Dav/docs/es/README-linux.md`** (English version: `Dav/docs/en/README-linux.md`).

---

## Common problems (both paths)

| Problem                             | Solution                                                                                                            |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Windows says "protected your PC"    | Click **"More info"** → **"Run anyway"** (this is because the installer is not signed yet).                         |
| It says "FreeCAD.exe not found"     | FreeCAD is not installed (or is in another path). Install it, or pass the path with `-FreeCADExe` (Path B).         |
| It says "Python 3 not found"        | Install Python 3.10+ checking **"Add Python to PATH"**.                                                             |
| The first time takes a long time    | This is normal: it is downloading the voice models. Do not close the window.                                        |
| The microphone does not respond in FreeCAD | Voice libraries are missing in FreeCAD's Python. Run `iniciar_dav.bat` again and let it reinstall dependencies. |

---

## Related documentation

| Topic                                                                                                 | Where it is                                         |
| ----------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Detailed Linux guide                                                                                  | `Dav/docs/es/README-linux.md`                          |
| **Technical documentation of the installer** (how the `.exe` was generated, how it works and how to regenerate it) | `Dav/scr/ComponentesDAV/scripts/iexpress/README.md` |
