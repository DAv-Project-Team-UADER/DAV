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
    print("Comandos disponibles en Structure Toolbar:")
    print("  part       - Crea un nuevo contenedor de tipo Part, que puede contener otros objetos y organizar la estructura del proyecto.")
    print("  new Group   - Crea un nuevo grupo genérico, que puede contener otros objetos y organizar la estructura del proyecto sin las propiedades específicas de un Part.")
    print("  link actions - Muestra un submenú con comandos relacionados a la gestión de enlaces.")
    print("  help     - Muestra esta ayuda")