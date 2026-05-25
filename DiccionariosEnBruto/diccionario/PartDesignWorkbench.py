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

from .primitivas.primitivas    import primitivas
from .boceto.boceto            import boceto
from .herramientas.herramientas import herramientas
from .modificadores.modificadores import modificadores
from .patrones.patrones        import patrones
from .sketcher.sketcher        import sketcher
from .ayuda                    import ayuda

partdesignworkbench = {}
partdesignworkbench.update(primitivas)
partdesignworkbench.update(boceto)
partdesignworkbench.update(herramientas)
partdesignworkbench.update(modificadores)
partdesignworkbench.update(patrones)
partdesignworkbench.update(sketcher)
partdesignworkbench['help'] = ayuda
