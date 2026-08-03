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

TraduceToPT = {
    # Sub-contextos
    'arquivo':                          explorer['file'],
    'arquivos':                         explorer['file'],
    'pasta':                            explorer['file'],
    'pastas':                           explorer['file'],
    'folhas':                           explorer['file'],
    'ficheiro':                         explorer['file'],
    'ficheiros':                        explorer['file'],
    'editar':                           explorer['edit'],
    'edicao':                           explorer['edit'],
    'edição':                           explorer['edit'],
    'edisao':                           explorer['edit'],
    'modificar':                        explorer['edit'],
    'alterar':                          explorer['edit'],
    'imprimir':                         explorer['print'],
    'impressao':                        explorer['print'],
    'impressão':                        explorer['print'],
    'impressora':                       explorer['print'],
    'print':                            explorer['print'],
    'gerar pdf':                        explorer['print'],
    'exportar pdf':                     explorer['print'],  
    'vista':                             explorer['windows'],
    'vistas':                            explorer['windows'],
    'janelas':                          explorer['windows'],
    'janela':                           explorer['windows'],
    'expressoes':                       explorer['expressions'],
    'expressões':                       explorer['expressions'],
    'expressao':                        explorer['expressions'],
    'expressão':                        explorer['expressions'],
    'ferramentas':                      explorer['tools'],
    'ferramenta':                       explorer['tools'],
    'utilidades':                       explorer['tools'],
    'estrutura':                        explorer['structure'],
    'barra de estrutura':               explorer['structure'],
    'barra estrutura':                  explorer['structure'],
    'barra de ferramentas de estrutura': explorer['structure'],

    # Callables directos
    'atualizar':                        explorer['refresh'],
    'recarregar':                       explorer['refresh'],
    'refresh':                          explorer['refresh'],
    'renovar':                          explorer['refresh'],
    'atualizacao':                       explorer['refresh'],
    'atualização':                       explorer['refresh'],
    'captura':                          explorer['screenshot'],
    'foto':                             explorer['screenshot'],
    'tirar foto':                       explorer['screenshot'],
    'salvar tela':                      explorer['screenshot'],
    'captura de tela':                  explorer['screenshot'],
    'documento de texto':               explorer['textdoc'],
    'documento':                        explorer['textdoc'],
    'texto':                            explorer['textdoc'],
    'desvincular':                      explorer['unlink'],
    'remover link':                     explorer['unlink'],
    'desligar link':                    explorer['unlink'],
    'congelar':                         explorer['freeze'],
    'imobilizar':                       explorer['freeze'],
    'bloquear':                         explorer['freeze'],
    'todas as instancias':              explorer['allinstances'],
    'todas as instâncias':              explorer['allinstances'],
    'selecionar instancias':            explorer['allinstances'],
    'selecionar instâncias':            explorer['allinstances'],
    'conjunto de variaveis':            explorer['variableset'],
    'conjunto de variáveis':            explorer['variableset'],
    'variaveis':                        explorer['variableset'],
    'variáveis':                        explorer['variableset'],
    
    "ajuda":                            explorer['help'],
    "informação":                       explorer['help'],
    "opções":                           explorer['help'],
}
