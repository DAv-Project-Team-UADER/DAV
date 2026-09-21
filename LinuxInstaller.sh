#!/bin/bash
# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

# Equivalente en Linux de crear_acceso_directo.ps1: crea "ejecutar.desktop"
# junto a este script, apuntando a iniciar_dav.sh y con el icono de DAV.
# Las rutas se calculan desde la ubicación del script, así que funciona
# en cualquier clon del repo. Correrlo una vez después de clonar.
#
# La primera vez (cuando "ejecutar.desktop" todavía no existe) también deja
# una copia en el Escritorio llamada "DAV_V1.desktop", con el mismo icono y
# destino. Las siguientes veces solo regenera "ejecutar.desktop": no pisa ni
# recrea la copia del Escritorio, por si el usuario la movió o la borró.

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LANZADOR="$RAIZ/iniciar_dav.sh"
ICONO="$RAIZ/Dav/scr/ComponentesDAV/Logos/color.png"
DESKTOP_FILE="$RAIZ/ejecutar.desktop"

if [ ! -f "$LANZADOR" ]; then
    echo -e "${RED}Error: No se encontró $LANZADOR${NC}"
    exit 1
fi
if [ ! -f "$ICONO" ]; then
    echo -e "${RED}Error: No se encontró el icono $ICONO${NC}"
    exit 1
fi

chmod +x "$LANZADOR"

ES_PRIMERA_VEZ=0
[ -e "$DESKTOP_FILE" ] || ES_PRIMERA_VEZ=1

# Los valores de Exec/Path/Icon con espacios van entre comillas dobles.
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=DAV
Comment=Inicia DAV
Exec="$LANZADOR"
Path=$RAIZ
Icon=$ICONO
Terminal=true
Categories=Graphics;Engineering;
EOF
chmod +x "$DESKTOP_FILE"

echo -e "${GREEN}Acceso directo creado:${NC} $DESKTOP_FILE"

if [ "$ES_PRIMERA_VEZ" -eq 1 ]; then
    # Respeta el nombre localizado del Escritorio (Desktop / Escritorio / ...)
    ESCRITORIO=""
    if command -v xdg-user-dir >/dev/null 2>&1; then
        ESCRITORIO="$(xdg-user-dir DESKTOP 2>/dev/null)"
    fi
    if [ -z "$ESCRITORIO" ] || [ ! -d "$ESCRITORIO" ]; then
        for d in "$HOME/Desktop" "$HOME/Escritorio"; do
            [ -d "$d" ] && ESCRITORIO="$d" && break
        done
    fi

    if [ -n "$ESCRITORIO" ] && [ -d "$ESCRITORIO" ]; then
        COPIA="$ESCRITORIO/DAV_V1.desktop"
        cp -f "$DESKTOP_FILE" "$COPIA"
        chmod +x "$COPIA"
        # GNOME exige marcar el lanzador como confiable para ejecutarlo
        if command -v gio >/dev/null 2>&1; then
            gio set "$COPIA" metadata::trusted true 2>/dev/null
        fi
        echo -e "${GREEN}Copia en el Escritorio:${NC} $COPIA"
    else
        echo "No se encontró la carpeta Escritorio; no se creó la copia."
    fi
fi
