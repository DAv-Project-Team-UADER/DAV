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

from .linkActions import link

TraduceToEs = {
    # MakeLink
    "crear enlace":     link["makelink"],
    "nuevo enlace":     link["makelink"],
    "generar enlace":   link["makelink"],
    "hacer enlace":     link["makelink"],

    # RelativeLink
    "enlace relativo":  link["relativelink"],
    "vincular relativo":link["relativelink"],
    "adjuntar relativo":link["relativelink"],
    "referencia relativa": link["relativelink"],

    # ImportLink
    "importar enlace":  link["importlink"],
    "traer enlace":     link["importlink"],
    "cargar enlace":    link["importlink"],
    "añadir enlace":    link["importlink"],

    # ImportAllLinks
    "importar todos":   link["importalllinks"],
    "cargar todos":     link["importalllinks"],
    "traer todos los enlaces": link["importalllinks"],
    "añadir todos los enlaces": link["importalllinks"],

    # ReplaceLink
    "reemplazar enlace": link["replacelink"],
    "sustituir enlace":  link["replacelink"],
    "cambiar enlace":    link["replacelink"],
    "modificar enlace":  link["replacelink"],

    # LinkGroups
    "grupo de enlaces":  link["linkgroups"],
    "conjunto de enlaces": link["linkgroups"],
    "colección de enlaces": link["linkgroups"],
    "agrupación de enlaces": link["linkgroups"],

    # Help
    "ayuda":            link["help"],
    "información":      link["help"],
    "opciones":         link["help"]
}
