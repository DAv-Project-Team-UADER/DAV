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

"""Spanish spoken-word mapping for the Explorer context."""

from .Explorer import explorer

TraduceToEs = {
    # Sub-contextos
    'archivo':                          explorer['file'],
    'archivos':                         explorer['file'],
    'carpeta':                          explorer['file'],
    'carpetas':                         explorer['file'],
    'folios':                           explorer['file'],
    'editar':                           explorer['edit'],
    'edicion':                          explorer['edit'],
    'edición':                          explorer['edit'],
    'modificar':                        explorer['edit'],
    'alterar':                          explorer['edit'],
    'imprimir':                         explorer['print'],
    'generar pdf':                      explorer['print'],
    'exportar pdf':                     explorer['print'],
    'impresion':                        explorer['print'],
    'impresión':                        explorer['print'],
    'impresora':                        explorer['print'],
    'pdf':                              explorer['print'],
    'ventanas':                         explorer['windows'],
    'ventana':                          explorer['windows'],
    'expresiones':                      explorer['expressions'],
    'expresion':                        explorer['expressions'],
    'expresión':                        explorer['expressions'],
    'herramientas':                     explorer['tools'],
    'herramienta':                      explorer['tools'],
    'utilidades':                       explorer['tools'],
    'estructura':                       explorer['structure'],
    'barra de estructura':              explorer['structure'],
    'barra estructura':                 explorer['structure'],
    'barra de herramientas de estructura': explorer['structure'],
    
    # Callables directos
    'refrescar':                        explorer['refresh'],
    'recargar':                         explorer['refresh'],
    'actualizar':                       explorer['refresh'],
    'foto':                             explorer['screenshot'],
    'captura':                          explorer['screenshot'],
    'sacar foto':                       explorer['screenshot'],
    'guardar pantalla':                 explorer['screenshot'],
    'captura de pantalla':              explorer['screenshot'],
    'documento de texto':               explorer['textdoc'],
    'documento':                        explorer['textdoc'],
    'texto':                            explorer['textdoc'],
    'desvincular':                      explorer['unlink'],
    'quitar enlace':                    explorer['unlink'],
    'desenlazar':                       explorer['unlink'],
    'romper enlace':                    explorer['unlink'],
    'separar enlace':                   explorer['unlink'],
    'desasociar':                       explorer['unlink'],
    'desconectar':                      explorer['unlink'],
    'congelar':                         explorer['freeze'],
    'inmovilizar':                      explorer['freeze'],
    'bloquear':                         explorer['freeze'],
    'todas las instancias':             explorer['allinstances'],
    'seleccionar instancias':           explorer['allinstances'],
    'todas instancias':                 explorer['allinstances'],
    'conjunto de variables':            explorer['variableset'],
    'variables':                        explorer['variableset'],
    'set de variables':                 explorer['variableset'],

    'ayuda':                            explorer['help'],
    'información':                      explorer['help'],
    'opciones':                         explorer['help'],
}
