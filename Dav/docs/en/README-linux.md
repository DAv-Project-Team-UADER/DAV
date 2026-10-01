# Startup Script Documentation (`inicio_dav.sh`)

## Overview
This Bash script automates preparing the environment and launching FreeCAD for the custom **DAV** workbench. Its main job is to link your development code directly to FreeCAD's local files through a symbolic link and run the application automatically, adapting to any user's home directory.

---

## Prerequisites
* **Operating system:** Ubuntu / Linux.
* **FreeCAD location:** The script assumes the FreeCAD executable is stored in the default Spanish-language downloads folder of the user running it (`$HOME/Descargas/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage`).
* **Execution context:** The script **must** be run from the root directory of your project (the directory that contains the `Dav` folder), since it uses `$(pwd)` (Print Working Directory) to build the path.
* **Permissions:** The script needs execute permissions on the system.

---

## Usage

1. Open a terminal.
2. Navigate to the root directory where your project and this script are located:
   ```bash
   cd /path/to/your/project
   ```
3. Grant execute permission to the script (only needed the first time):
   ```bash
   chmod +x inicio_dav.sh
   ```
4. Run the script:
   ```bash
   ./inicio_dav.sh
   ```

---

## Step-by-Step Code Explanation

### 1. Environment Variables (Colors)
```bash
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'
```
Defines variables for printing colored messages in the terminal (green for successes, yellow for warnings, NC to reset to the default color).

### 2. FreeCAD Modules Directory (Mod)
```bash
MOD_DIR="$HOME/.local/share/FreeCAD/v1-1/Mod"
mkdir -p "$MOD_DIR"
```
Sets the path to the add-ons (Mods) folder specific to FreeCAD version 1.1 on Linux. The `mkdir -p` command creates the directory if it does not exist yet, avoiding errors.

### 3. Path Resolution and Validation
```bash
WORKBENCH_PATH="$(pwd)/Dav/scr/ComponentesDAV/Dav"

if [ -f "$WORKBENCH_PATH/InitGui.py" ]; then
    echo "¡InitGui.py encontrado correctamente!"
else
    echo -e "${YELLOW}Advertencia: No se ve el InitGui.py en la ruta esperada.${NC}"
fi
```
Takes the current path where you are running the script (`$(pwd)`) and appends the path to your Workbench's final subfolder.
Then it checks (`[ -f ... ]`) whether the critical file `InitGui.py` exists there. This is a safety barrier to warn you if you are running the script from the wrong folder.

### 4. Creating the Symbolic Link
```bash
ln -sfn "$WORKBENCH_PATH" "$MOD_DIR/DAV"
```
Creates a "shortcut" (symbolic link) from your source code to FreeCAD's `Mod` folder.
* `-s`: Creates a symbolic link (not a hard one).
* `-f`: Forces creation (overwrites if it already existed).
* `-n`: Treats the destination as a normal file (prevents nesting links if run multiple times).
* **Benefit:** Any change you save in your Python code will be reflected in FreeCAD the next time you start it, without copying or moving files manually.

### 5. Universal FreeCAD Launch
```bash
"$HOME/Descargas/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage"
```
Directly calls and runs the AppImage file. By using the `$HOME` environment variable instead of a hard-coded path, the script becomes universal: it will work for any user as long as they have the file in their "Descargas" (Downloads) folder.

---

## Possible Problems and Solutions (Troubleshooting)

| Problem | Probable cause | Solution |
| :--- | :--- | :--- |
| **"Advertencia: No se ve el InitGui.py..." (Warning: InitGui.py not found...)** | You are running the script from the wrong folder. | Use `cd` to go to your project's root folder before running `./inicio_dav.sh`. |
| **"Permiso denegado" (Permission denied)** | The script or the AppImage is not executable. | Run `chmod +x inicio_dav.sh` and `chmod +x "$HOME/Descargas/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage"`. |
| **"No existe el archivo o el directorio" (No such file or directory) when launching FreeCAD** | The user's system is in English (`Downloads` instead of `Descargas`) or the file has a different name/version. | Rename the downloads folder in the script or verify that the FreeCAD 1.1.3 file is exactly there. |
