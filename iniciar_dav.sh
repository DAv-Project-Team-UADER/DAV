#!/bin/bash

# Colores para la terminal
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

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