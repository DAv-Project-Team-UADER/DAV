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

def ayuda():
    print("=== Archivos ===")
    print("  documento nuevo : Crea un documento vacío             | Req: ninguno")
    print("  abrir           : Abre un archivo existente           | Req: ninguno")
    print("  guardar         : Guarda el documento activo          | Req: documento activo")
    print("  guardar como    : Guarda con nuevo nombre (diálogo)   | Req: documento activo")
    print("  guardar copia   : Guarda una copia (diálogo)          | Req: documento activo")
    print("  revertir        : Descarta cambios y recarga del disco | Req: documento guardado")
    print("  combinar        : Une otro archivo al documento actual | Req: documento activo")
