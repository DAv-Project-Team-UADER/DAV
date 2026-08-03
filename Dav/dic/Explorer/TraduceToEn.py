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

from .Explorer import explorer

TraduceToEn = {
    # Sub-contextos
    'file':                  explorer['file'],
    'files':                 explorer['file'],
    'folder':                explorer['file'],
    'folders':               explorer['file'],
    'sheets':                explorer['file'],
    'documents':             explorer['file'],
    'edit':                  explorer['edit'],
    'editing':               explorer['edit'],
    'modify':                explorer['edit'],
    'print':                 explorer['print'],
    'printing':              explorer['print'],
    'printer':               explorer['print'],
    'windows':               explorer['windows'],
    'window':                explorer['windows'],
    'expressions':           explorer['expressions'],
    'expression':            explorer['expressions'],
    'tools':                 explorer['tools'],
    'tool':                  explorer['tools'],
    'utilities':             explorer['tools'],
    'structure':             explorer['structure'],
    'structure toolbar':     explorer['structure'],
    'structure bar':         explorer['structure'],

    # Callables directos
    'refresh':               explorer['refresh'],
    'reload':                explorer['refresh'],
    'update':                explorer['refresh'],
    'screenshot':            explorer['screenshot'],
    'photo':                 explorer['screenshot'],
    'take photo':            explorer['screenshot'],
    'capture':               explorer['screenshot'],
    'save screen':           explorer['screenshot'],
    'screen capture':        explorer['screenshot'],
    'text document':         explorer['textdoc'],
    'textdoc':               explorer['textdoc'],
    'text file':             explorer['textdoc'],
    'document':              explorer['textdoc'],
    'unlink':                explorer['unlink'],
    'remove link':           explorer['unlink'],
    'detach link':           explorer['unlink'],
    'freeze':                explorer['freeze'],
    'lock':                  explorer['freeze'],
    'immobilize':            explorer['freeze'],
    'all instances':         explorer['allinstances'],
    'select all instances':  explorer['allinstances'],
    'allinstances':          explorer['allinstances'],
    'variable set':          explorer['variableset'],
    'variables':             explorer['variableset'],
    'var set':               explorer['variableset'],
    'variableset':           explorer['variableset'],

    "help":                 explorer['help'],
    "info":                 explorer['help'],
    "options":              explorer['help'],
}
