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

from .circular_array import array

TraduceToPt = {
    "circular":              array["circular"],
    "matriz circular":       array["circular"],
    "arranjo circular":      array["circular"],
    "ligadura circular":      array["circular"],
    "rodando":                array["circular"],
    "rotando":                array["circular"],
    "ortogonal":             array["ortho"],
    "matriz ortogonal":      array["ortho"],
    "arranjo retangular":    array["ortho"],
    "ligadura ortogonal":    array["ortho"],
    "retangular":            array["ortho"],
    "cuadrado":               array["ortho"],
    "quadrado":               array["ortho"],
    "quadrais":                array["ortho"],
    
    "polar":                 array["polar"],
    "matriz polar":          array["polar"],
    
    "caminho":               array["path"],
    "matriz por caminho":    array["path"],
    "copiar no caminho":     array["path"],
    
    
    "ligadura por caminho": array["pathlink"],
    "ligação por caminho":  array["pathlink"],
    "pontos":                array["point"],
    "matriz por pontos":     array["point"],
    
    "ligação por pontos":    array["pointlink"],
    "ligadura por pontos":   array["pointlink"],
    "ajuda":             array["help"],
    "informação":       array["help"],
    "opções":            array["help"]
}