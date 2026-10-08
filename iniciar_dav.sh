#!/bin/bash

# Colores para la terminal
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Uso:
#   ./iniciar_dav.sh                      prepara el entorno y abre FreeCAD con DAV
#   ./iniciar_dav.sh /ruta/a/FreeCAD      igual, indicando el ejecutable de FreeCAD
#   ./iniciar_dav.sh --install-only       solo prepara (venv, deps, modelos, workbench)
#   ./iniciar_dav.sh --skip-models        no descarga los modelos Vosk
# El resto de los argumentos se pasan a FreeCAD.

INSTALL_ONLY=0
SKIP_MODELS=0
PASS_ARGS=()
for arg in "$@"; do
    case "$arg" in
        --install-only) INSTALL_ONLY=1 ;;
        --skip-models) SKIP_MODELS=1 ;;
        *) PASS_ARGS+=("$arg") ;;
    esac
done
set -- "${PASS_ARGS[@]}"

echo -e "${GREEN}=== Iniciando DAV en Linux / Ubuntu ===${NC}"

# 1. Manejo seguro de permisos (evitar ensuciar /root si se ejecuta con sudo)
if [ "$EUID" -eq 0 ] && [ -n "$SUDO_USER" ]; then
    echo -e "${YELLOW}Aviso: No es necesario ejecutar este script con sudo.${NC}"
    USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
    REAL_USER="$SUDO_USER"
else
    USER_HOME="$HOME"
    REAL_USER="$USER"
fi

# 2. Directorio base del repositorio (resuelto de forma dinámica)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKBENCH_PATH="$SCRIPT_DIR/Dav/scr/ComponentesDAV/Dav"

if [ ! -f "$WORKBENCH_PATH/InitGui.py" ]; then
    echo -e "${RED}Error: No se encontró InitGui.py en:${NC} $WORKBENCH_PATH"
    exit 1
fi
echo -e "¡InitGui.py encontrado en: ${BLUE}$WORKBENCH_PATH${NC}!"

# 2b. Preparar GUIFreeCad (venv, dependencias y modelos Vosk), igual que
# iniciar_dav.ps1 en Windows. Es idempotente: si ya está todo, no hace nada.
GUI_ROOT="$SCRIPT_DIR/Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad"
VENV_DIR="$GUI_ROOT/.venv"
VENV_PY="$VENV_DIR/bin/python"
REQ_FILE="$GUI_ROOT/requirements.txt"
SETUP_MODELS="$GUI_ROOT/scripts/setup_models.py"
DAV_MODELS_DEFAULT="$SCRIPT_DIR/Dav/models"

# Ejecuta como el usuario real aunque el script se haya lanzado con sudo,
# para no dejar el venv ni los modelos a nombre de root.
as_user() {
    if [ "$EUID" -eq 0 ] && [ -n "$SUDO_USER" ]; then
        sudo -u "$REAL_USER" "$@"
    else
        "$@"
    fi
}

# Paquetes del sistema que necesita DAV (Python, venv/pip y audio para el micrófono).
APT_PACKAGES=(python3 python3-venv python3-pip ca-certificates
    libportaudio2 portaudio19-dev python3-pyaudio
    libgl1 libegl1 libglib2.0-0 libdbus-1-3 libfontconfig1 libxkbcommon0 libxkbcommon-x11-0
    libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0
    libxcb-render-util0 libxcb-shape0 libxcb-xinerama0 libxcb-xkb1)

# Instala con apt los paquetes que falten. Es idempotente: si ya están todos, no hace nada.
ensure_system_packages() {
    if ! command -v apt-get >/dev/null 2>&1 || ! command -v dpkg >/dev/null 2>&1; then
        echo -e "  ${YELLOW}!!${NC}  apt no disponible: instala manualmente Python 3, venv, pip y PortAudio"
        return 0
    fi

    local missing=() pkg
    for pkg in "${APT_PACKAGES[@]}"; do
        dpkg -s "$pkg" >/dev/null 2>&1 || missing+=("$pkg")
    done

    if [ ${#missing[@]} -eq 0 ]; then
        echo -e "  ${GREEN}OK${NC}  Paquetes del sistema"
        return 0
    fi

    echo "  Instalando paquetes del sistema: ${missing[*]}"
    local sudo_cmd=""
    [ "$EUID" -ne 0 ] && sudo_cmd="sudo"
    $sudo_cmd apt-get update
    if ! $sudo_cmd apt-get install -y "${missing[@]}"; then
        # Algún paquete puede no existir en esta versión de la distro: reintentar uno a uno
        local failed=()
        for pkg in "${missing[@]}"; do
            $sudo_cmd apt-get install -y "$pkg" >/dev/null 2>&1 || failed+=("$pkg")
        done
        if [ ${#failed[@]} -gt 0 ]; then
            echo -e "${YELLOW}Aviso: no se pudieron instalar: ${failed[*]}${NC}"
            echo "  Manualmente: sudo apt install ${failed[*]}"
            return 0
        fi
    fi
    echo -e "  ${GREEN}OK${NC}  Paquetes del sistema instalados"
}

find_system_python() {
    local py
    for py in python3 python; do
        if command -v "$py" >/dev/null 2>&1 && "$py" -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
            command -v "$py"
            return 0
        fi
    done
    return 1
}

ensure_gui_venv() {
    if [ -x "$VENV_PY" ]; then
        echo -e "  ${GREEN}OK${NC}  Entorno virtual en GUIFreeCad/.venv"
        return 0
    fi

    local sys_py
    sys_py="$(find_system_python)" || {
        echo -e "${RED}Error: no se encontró Python 3.10 o superior.${NC}"
        echo "  Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
        return 1
    }

    echo "  Creando .venv en GUIFreeCad..."
    as_user "$sys_py" -m venv "$VENV_DIR"
    if [ ! -x "$VENV_PY" ]; then
        echo -e "${RED}Error: no se pudo crear GUIFreeCad/.venv.${NC}"
        echo "  Ubuntu/Debian: sudo apt install python3-venv python3-pip"
        return 1
    fi
    echo -e "  ${GREEN}OK${NC}  Entorno virtual creado"
}

ensure_gui_dependencies() {
    if as_user "$VENV_PY" -c "import PySide6, vosk, sounddevice" >/dev/null 2>&1; then
        echo -e "  ${GREEN}OK${NC}  Dependencias Python de GUIFreeCad"
        return 0
    fi

    echo "  Instalando requirements.txt..."
    as_user "$VENV_PY" -m pip install --upgrade pip >/dev/null 2>&1
    if ! as_user "$VENV_PY" -m pip install -r "$REQ_FILE"; then
        echo -e "${RED}Error: falló pip install en GUIFreeCad.${NC}"
        return 1
    fi
    echo -e "  ${GREEN}OK${NC}  Dependencias instaladas"
}

# Un modelo cuenta como presente si su carpeta existe y no está vacía.
model_present() {
    local dir
    for dir in "$DAV_MODELS_DEFAULT" "$GUI_ROOT/models"; do
        if [ -d "$dir/vosk-model-small-es-0.42" ] && [ -n "$(ls -A "$dir/vosk-model-small-es-0.42" 2>/dev/null)" ]; then
            echo "$dir/vosk-model-small-es-0.42"
            return 0
        fi
    done
    return 1
}

ensure_vosk_models() {
    if [ "$SKIP_MODELS" -eq 1 ]; then
        echo -e "  ${YELLOW}!!${NC}  Omitiendo descarga de modelos (--skip-models)"
        return 0
    fi

    local present
    if present="$(model_present)"; then
        echo -e "  ${GREEN}OK${NC}  Modelo Vosk ES presente: $present"
        return 0
    fi

    echo "  Descargando modelos Vosk (solo la primera vez, puede tardar)..."
    if ! as_user env DAV_MODELS_DIR="${DAV_MODELS_DIR:-$DAV_MODELS_DEFAULT}" "$VENV_PY" "$SETUP_MODELS"; then
        echo -e "${RED}Error: falló scripts/setup_models.py.${NC}"
        return 1
    fi
    echo -e "  ${GREEN}OK${NC}  Modelos Vosk listos"
}

if [ ! -d "$GUI_ROOT" ]; then
    echo -e "${RED}Error: No se encontró GUIFreeCad en:${NC} $GUI_ROOT"
    exit 1
fi

echo -e "\n${BLUE}== GUIFreeCad (venv, deps, modelos) ==${NC}"
ensure_system_packages
ensure_gui_venv || exit 1
ensure_gui_dependencies || exit 1
ensure_vosk_models || exit 1

# Variables que usa el workbench (las mismas que setea run_freecad_dav.ps1)
export DAV_GUI_FREECAD_ROOT="$GUI_ROOT"
export DAV_MODELS_DIR="${DAV_MODELS_DIR:-$DAV_MODELS_DEFAULT}"

# 3. Vincular Workbench en las rutas de módulos de FreeCAD
# A) Ruta estándar de FreeCAD en Linux (~/.local/share/FreeCAD/v1-1/Mod)
MOD_DIR_NATIVE="$USER_HOME/.local/share/FreeCAD/v1-1/Mod"
mkdir -p "$MOD_DIR_NATIVE"
ln -sfn "$WORKBENCH_PATH" "$MOD_DIR_NATIVE/DAV"
echo -e "${GREEN}Enlace creado/actualizado en:${NC} $MOD_DIR_NATIVE/DAV"

# B) Ruta de Flatpak (si FreeCAD está instalado vía Flatpak)
MOD_DIR_FLATPAK="$USER_HOME/.var/app/org.freecad.FreeCAD/data/FreeCAD/v1-1/Mod"
if [ -d "$USER_HOME/.var/app/org.freecad.FreeCAD" ]; then
    mkdir -p "$MOD_DIR_FLATPAK"
    ln -sfn "$WORKBENCH_PATH" "$MOD_DIR_FLATPAK/DAV"
    echo -e "${GREEN}Enlace Flatpak creado/actualizado en:${NC} $MOD_DIR_FLATPAK/DAV"
fi

# 4. Búsqueda y detección automática del ejecutable de FreeCAD
# (función para poder repetirla después de instalar FreeCAD)
detect_freecad() {
FREECAD_CMD=""

# Prioridad 1: Argumento por línea de comandos (ej: ./iniciar_dav.sh /ruta/a/freecad)
if [ -n "$1" ] && [ -e "$1" ]; then
    FREECAD_CMD="$1"
# Prioridad 2: Variable de entorno FREECAD_BIN
elif [ -n "$FREECAD_BIN" ] && [ -e "$FREECAD_BIN" ]; then
    FREECAD_CMD="$FREECAD_BIN"
else
    # Prioridad 3: Buscar AppImage en Downloads, Descargas, directorio actual o HOME
    for candidate in \
        "$USER_HOME"/Downloads/FreeCAD*.AppImage \
        "$USER_HOME"/Downloads/freecad*.AppImage \
        "$USER_HOME"/Descargas/FreeCAD*.AppImage \
        "$USER_HOME"/Descargas/freecad*.AppImage \
        "$SCRIPT_DIR"/FreeCAD*.AppImage \
        "$SCRIPT_DIR"/freecad*.AppImage \
        "$USER_HOME"/FreeCAD*.AppImage
    do
        if [ -f "$candidate" ]; then
            FREECAD_CMD="$candidate"
            break
        fi
    done

    # Prioridad 4: Comando freecad en el PATH del sistema
    if [ -z "$FREECAD_CMD" ]; then
        if command -v freecad >/dev/null 2>&1; then
            FREECAD_CMD="$(command -v freecad)"
        elif command -v FreeCAD >/dev/null 2>&1; then
            FREECAD_CMD="$(command -v FreeCAD)"
        fi
    fi

    # Prioridad 5: Versión Flatpak de FreeCAD
    if [ -z "$FREECAD_CMD" ]; then
        if command -v flatpak >/dev/null 2>&1 && flatpak info org.freecad.FreeCAD >/dev/null 2>&1; then
            FREECAD_CMD="flatpak run org.freecad.FreeCAD"
        fi
    fi
fi
}

# Pregunta (ventana emergente en inglés; si no hay entorno gráfico, en la
# terminal) si se quiere instalar FreeCAD. Devuelve 0 solo si el usuario acepta.
ask_install_freecad() {
    local title="FreeCAD not installed"
    local text="FreeCAD is not installed. Do you want to install it?\n\n(Requires internet access)"

    if [ -n "$DISPLAY$WAYLAND_DISPLAY" ]; then
        if command -v zenity >/dev/null 2>&1; then
            as_user zenity --question --title="$title" --text="$text" \
                --ok-label="Yes" --cancel-label="No" 2>/dev/null
            return $?
        elif command -v kdialog >/dev/null 2>&1; then
            as_user kdialog --title "$title" --yesno "$(echo -e "$text")" 2>/dev/null
            return $?
        fi
    fi

    # Sin diálogo gráfico disponible: preguntar por terminal
    if [ -t 0 ]; then
        echo -e "${YELLOW}$title.${NC}"
        read -r -p "$(echo -e "$text") [y/N] " answer
        case "$answer" in [yY]|[yY][eE][sS]) return 0 ;; esac
    fi
    return 1
}

install_freecad() {
    if ! command -v apt >/dev/null 2>&1; then
        echo -e "${RED}Error: apt no está disponible en este sistema.${NC}"
        echo "Instala FreeCAD manualmente (https://www.freecad.org/downloads.php)."
        return 1
    fi

    echo -e "${BLUE}Instalando FreeCAD (sudo apt update && sudo apt install -y freecad)...${NC}"
    if [ "$EUID" -eq 0 ]; then
        apt update && apt install -y freecad
    else
        sudo apt update && sudo apt install -y freecad
    fi
}

detect_freecad "$1"

if [ -z "$FREECAD_CMD" ]; then
    echo -e "${YELLOW}FreeCAD no está instalado.${NC}"
    if install_freecad; then
        hash -r
        detect_freecad "$1"
    else
        echo -e "${RED}Error: falló la instalación de FreeCAD.${NC}"
    fi
fi

if [ "$INSTALL_ONLY" -eq 1 ]; then
    if [ -z "$FREECAD_CMD" ]; then
        echo -e "${YELLOW}Aviso: FreeCAD sigue sin estar instalado; se volverá a preguntar al abrir DAV.${NC}"
    fi
    echo -e "${GREEN}Instalación lista (--install-only): no se inicia FreeCAD.${NC}"
    exit 0
fi

# 5. Validación final y ejecución
if [ -z "$FREECAD_CMD" ]; then
    echo -e "${RED}Error: No se pudo encontrar automáticamente el ejecutable de FreeCAD.${NC}"
    echo "Puedes iniciar pasando la ruta manualmente:"
    echo "  ./iniciar_dav.sh /ruta/a/FreeCAD.AppImage"
    echo "O guardar el AppImage en tu carpeta Downloads o Descargas."
    exit 1
fi

echo -e "${GREEN}¡Iniciando FreeCAD desde:${NC} $FREECAD_CMD"

# Si es un AppImage o ejecutable en disco, asegurar permisos de ejecución (chmod +x)
if [ -f "$FREECAD_CMD" ] && [ ! -x "$FREECAD_CMD" ]; then
    echo -e "${YELLOW}Asignando permisos de ejecución (chmod +x) a:${NC} $FREECAD_CMD"
    chmod +x "$FREECAD_CMD"
fi

# Si se corrió con sudo, degradar permisos para no ejecutar FreeCAD como root
if [ "$EUID" -eq 0 ] && [ -n "$SUDO_USER" ]; then
    sudo -u "$REAL_USER" $FREECAD_CMD "$@"
else
    exec $FREECAD_CMD "$@"
fi