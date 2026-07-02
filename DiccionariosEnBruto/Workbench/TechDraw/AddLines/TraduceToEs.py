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

from .addLines import addLines

TraduceToEs = {
    # twolines
<<<<<<< HEAD
    "dos líneas":        addLines["twolines"],
    "línea central":     addLines["twolines"],    # sinonimo
    "eje central":       addLines["twolines"],    # sinonimo
    # twopoints
    "dos puntos":        addLines["twopoints"],
    "línea dos puntos":  addLines["twopoints"],   # sinonimo
    "eje dos puntos":    addLines["twopoints"],   # sinonimo
    # cosmetic
    "cosmetica":         addLines["cosmetic"],
    "línea cosmetica":   addLines["cosmetic"],    # sinonimo
    "línea auxiliar":    addLines["cosmetic"],    # sinonimo
    # decorate
    "decorar":           addLines["decorate"],
    "estilo línea":      addLines["decorate"],    # sinonimo
    "cambiar línea":     addLines["decorate"],    # sinonimo
    # center
    "centro":            addLines["center"],
    "centro cara":       addLines["center"],      # sinonimo
    "línea centro cara": addLines["center"],      # sinonimo
    # help
    "ayuda":             addLines["help"],
    "información":              addLines["help"],        # sinonimo
    "opciones":          addLines["help"],        # sinonimo
=======
    "dos lineas":        addLines["twolines"],
    "linea central":     addLines["twolines"],      
    "eje central":       addLines["twolines"],    

    # twopoints
    "dos puntos":        addLines["twopoints"],
    "linea dos puntos":  addLines["twopoints"],     
    "eje dos puntos":    addLines["twopoints"],  

    # cosmetic
    "cosmetica":         addLines["cosmetic"],
    "linea cosmetica":   addLines["cosmetic"],      
    "linea auxiliar":    addLines["cosmetic"],     

    # decorate
    "decorar":           addLines["decorate"],
    "estilo linea":      addLines["decorate"],      
    "cambiar linea":     addLines["decorate"],     

    # center
    "centro":            addLines["center"],
    "centro cara":       addLines["center"],        
    "linea centro cara": addLines["center"],        

    # help
    "ayuda":             addLines["help"],
    "información":              addLines["help"],          
    "opciones":          addLines["help"],          
>>>>>>> ab0008d5c571ed323a300c3168bedfe72882654d
}
