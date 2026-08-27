#!/bin/bash

# Colores para la terminal
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Iniciando DAV en Ubuntu ===${NC}"

# Ruta de módulos de FreeCAD 1.1 en Linux
MOD_DIR="$HOME/.local/share/FreeCAD/v1-1/Mod"
mkdir -p "$MOD_DIR"

# Ruta a la subcarpeta donde vive el InitGui.py
WORKBENCH_PATH="$(pwd)/Dav/scr/ComponentesDAV/Dav"

if [ -f "$WORKBENCH_PATH/InitGui.py" ]; then
    echo "¡InitGui.py encontrado correctamente!"
else
    echo -e "${YELLOW}Advertencia: No se ve el InitGui.py en la ruta esperada.${NC}"
fi

echo "Vinculando Workbench desde: $WORKBENCH_PATH"

# Creación del enlace simbólico apuntando a la subcarpeta final
ln -sfn "$WORKBENCH_PATH" "$MOD_DIR/DAV"
echo -e "${GREEN}Enlace creado exitosamente en: $MOD_DIR/DAV${NC}"

# Iniciar tu AppImage de FreeCAD
echo -e "${GREEN}¡Iniciando FreeCAD!${NC}"
"$HOME/Descargas/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage"