# DAV — Installation Guide (Linux)

**DAV (Voice-Assisted Design, "Diseño Asistido por Voz")** is a program that lets you control **FreeCAD** with your voice. Instead of clicking, you say commands like _"vista frontal"_ (front view) or _"crear boceto"_ (create sketch) and DAV runs them for you.

DAV is not a separate program: it **runs inside FreeCAD**, as one more module. That is why you install FreeCAD first, and then add DAV.

---

## Choose your path

There are two ways to install DAV on Linux, depending on what you need to do:

| If you want to… | Follow this path |
| :--- | :--- |
| **Just use DAV** without touching code | [Path A → End user](#path-a--end-user) |
| **Work on the project's code** | [Path B → Developers](#path-b--developers) |

---

## What you need on either path

| You need | What for |
| :--- | :--- |
| **FreeCAD 1.1.4 (AppImage)** | It is the base program. [Download the AppImage](https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage) and save it in your **Downloads** folder (or **Descargas**). |
| **Microphone** | To use the voice commands. |
| **Internet** | Only the first time: DAV downloads the Vosk voice model (≈ 40 MB) and dependencies. |
| **Python 3.10+** | It usually comes installed by default on modern Linux distributions (Ubuntu, Mint, Fedora). To create DAV's environment you also need the `python3-venv` package (`sudo apt install python3 python3-venv python3-pip`). |

> You **do not need** to download voice models manually. DAV takes care of all that automatically the first time you open it.

---

## Path A — End user

For those who **just want to use DAV**, without opening the code or using the terminal. It is a single executable file.

### Step 1 — Download FreeCAD
1. [Download FreeCAD 1.1.4 (AppImage for Linux)](https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage).
2. If you prefer another version, all of them are at <https://www.freecad.org/downloads.php> (always use the **1.x** series in `.AppImage` format).
3. Save the file exactly in your personal **Downloads** folder (or **Descargas** if your system is in Spanish).
4. **IMPORTANT:** Without the FreeCAD AppImage downloaded, DAV cannot open.

### Step 2 — Get the DAV installer
Download the file **`DAV_Installer_1.0-Linux`**.

### Step 3 — Give it execute permission
For security, Linux does not immediately run files downloaded from the internet with a double click. You have to authorize it:
1. **Right-click** `DAV_Installer_1.0-Linux`.
2. Select **Properties**.
3. Go to the **Permissions** tab.
4. Check the box **"Allow executing file as program"** (or similar).
5. Close the window.

### Step 4 — Run the installer
**Double-click** `DAV_Installer_1.0-Linux` and select **Run**.
*(If double-clicking does not work in your environment, you can open the terminal in that folder and type `./DAV_Installer_1.0-Linux`).*

The program will automatically do the following:
1. Copy the DAV files to your FreeCAD modules folder (`~/.local/share/FreeCAD/v1-1/Mod/`).
2. Install the voice dependencies and download the Spanish model.
3. **Open FreeCAD** with the DAV panel integrated.

> **Note:** The first time it may take a few minutes because of the voice model download.

### Step 5 — Start using DAV!
When FreeCAD opens, you will see the **DAV panel** with the microphone button. Say **"vista frontal"** (front view) to try it.

To open it again in the future, simply run the `DAV_Installer_1.0-Linux` file again (it will detect that it is already installed and open FreeCAD directly).

---

## Path B — Developers

For **team members** who need access to the source code, to modify it and test changes in real time.

### 1. Install the prerequisites
* Make sure you have **Git** installed (`sudo apt install git`).
* Have **Python 3.10+** with venv and pip: `sudo apt install python3 python3-venv python3-pip`.
* [Download the **FreeCAD 1.1.4 AppImage**](https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage) and leave it in your `~/Descargas/` folder.

### 2. Clone the repository
Open a terminal and run:
```bash
git clone https://github.com/DAv-Project-Team-UADER/DAV.git
cd DAV
```

### 3. Run the installer
Inside the project folder you just cloned, run the installer:
```bash
chmod +x LinuxInstaller.sh iniciar_dav.sh
./LinuxInstaller.sh
```

The installer sets everything up automatically, with no manual steps:
1. Creates the virtual environment (`GUIFreeCad/.venv`) and installs the voice dependencies (`PySide6`, `Vosk`, `sounddevice`, …).
2. Downloads the Vosk voice models into `Dav/models/` (if they are already there, it does not download them again).
3. Creates a symbolic link from your source code to `~/.local/share/FreeCAD/v1-1/Mod/DAV`.
4. Creates the shortcuts: `ejecutar.desktop` in the project folder, a **DAV** entry in the applications menu and, the first time, `DAV_V1.desktop` on the Desktop.

### 4. Open DAV
Double-click the **DAV** shortcut (or run `./iniciar_dav.sh` in the terminal). The script looks for the FreeCAD AppImage in your Downloads folder using a universal path (`$HOME`) and launches FreeCAD with your code loaded. Any change you save in the Python code will be reflected when FreeCAD is restarted.

Useful `iniciar_dav.sh` options:
```bash
./iniciar_dav.sh /path/to/FreeCAD.AppImage   # use a specific FreeCAD
./iniciar_dav.sh --install-only              # only prepare the environment, without opening FreeCAD
./iniciar_dav.sh --skip-models               # do not download the voice models
```

---

## Common problems

| Problem | Solution |
| :--- | :--- |
| **"Permission denied" when double-clicking** | You missed Step 3 of Path A. Right-click the file > Properties > Permissions > Allow executing as a program. |
| **"FreeCAD not found"** | Check that the FreeCAD file ends in `.AppImage` and is directly in the `Descargas` (or `Downloads`) folder. |
| **"Could not create GUIFreeCad/.venv"** | The virtual environment package is missing. Run `sudo apt install python3-venv python3-pip` and run the installer again. |
| **The microphone does not respond / Vosk error** | Audio dependencies may be missing on Linux. Open a terminal and run `sudo apt install libportaudio2 portaudio19-dev python3-pyaudio`. |
| **The first time takes a long time** | This is normal, it is downloading the voice model in the background. |
