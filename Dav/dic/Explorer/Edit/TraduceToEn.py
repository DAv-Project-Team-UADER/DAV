# Copyright (C) 2026 El Equipo del Proyecto DAV
# Copyright (C) 2026 The DAV Project Team
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
# SPDX-License-Identifier: GPL-3.0-or-later

from .Edit import edit

TraduceToEn = {
    # Comandos de Deshacer / Rehacer
    'undo':             edit['undo'],
    'revert':           edit['undo'],
    'go back':          edit['undo'],
    'redo':             edit['redo'],
    'step forward':     edit['redo'],
    
    # Comandos de Portapapeles y Selección
    'cut':              edit['cut'],
    'copy':             edit['copy'],
    'paste':            edit['paste'],
    'duplicate':        edit['duplicate'],
    'clone':            edit['duplicate'],
    'select all':       edit['selectall'],
    'grab all':         edit['selectall'],
    'delete':           edit['delete'],
    'remove':           edit['delete'],
    'erase':            edit['delete'],
    
    # Comandos de Transformación y Posicionamiento
    'placement':        edit['placement'],
    'position':         edit['placement'],
    'set position':     edit['placement'],
    'transform':        edit['transform'],
    'move':             edit['transform'],
    'align':            edit['align'],
    'alignment':        edit['align'],
    
    # Interfaz y Configuración
    'preferences':      edit['preferences'],
    'settings':         edit['preferences'],
    'properties':       edit['properties'],
    'details':          edit['properties'],
    'send to python':   edit['sendtopython'],
    'python console':   edit['sendtopython'],
    'edit mode':        edit['editmode'],
    'modify mode':      edit['editmode'],
    
    # Estandarización de Ayuda
    'help':             edit['help'],
    'info':             edit['help'],
    'options':          edit['help']
}