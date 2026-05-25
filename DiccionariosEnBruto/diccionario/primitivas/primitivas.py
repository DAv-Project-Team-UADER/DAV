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

# ─────────────────────────────────────────────────────────────────────────────
# Fuentes: tickets remito_PartDesign_Additive*.txt
# Revisión: el campo <script nativo> de los tickets contiene funciones Python
#   completas (con def/import) en lugar de Gui.runCommand, lo cual es correcto
#   para PartDesign: estos objetos se crean vía scripting API, no vía GUI cmd.
#   Las claves del motor de voz son los valores de <Palabras sugeridas>
#   normalizados: minúsculas, sin tildes, sin caracteres especiales.
# ─────────────────────────────────────────────────────────────────────────────

import FreeCAD as App
from .ayuda import ayuda


def _get_doc_and_body():
    """Devuelve (doc, body), creando ambos si no existen."""
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument()
    body = doc.getObject('Body')
    if body is None:
        body = doc.addObject('PartDesign::Body', 'Body')
    return doc, body


def _caja(name='Box', length=10.0, width=10.0, height=10.0):
    """PartDesign_AdditiveBox — Caja/cubo aditivo."""
    doc, body = _get_doc_and_body()
    box = doc.addObject('PartDesign::AdditiveBox', name)
    box.Length = length
    box.Width  = width
    box.Height = height
    body.addObject(box)
    doc.recompute()
    return box


def _cono(name='Cone', radius1=5.0, radius2=0.0, height=10.0):
    """PartDesign_AdditiveCone — Cono aditivo (truncado si radius2 > 0)."""
    doc, body = _get_doc_and_body()
    cone = doc.addObject('PartDesign::AdditiveCone', name)
    cone.Radius1 = radius1
    cone.Radius2 = radius2
    cone.Height  = height
    body.addObject(cone)
    doc.recompute()
    return cone


def _cilindro(name='Cylinder', radius=5.0, height=10.0):
    """PartDesign_AdditiveCylinder — Cilindro aditivo."""
    doc, body = _get_doc_and_body()
    cyl = doc.addObject('PartDesign::AdditiveCylinder', name)
    cyl.Radius = radius
    cyl.Height = height
    body.addObject(cyl)
    doc.recompute()
    return cyl


def _elipsoide(name='Ellipsoid', radius1=5.0, radius2=3.0, radius3=2.0):
    """PartDesign_AdditiveEllipsoid — Elipsoide aditivo."""
    doc, body = _get_doc_and_body()
    ell = doc.addObject('PartDesign::AdditiveEllipsoid', name)
    ell.Radius1 = radius1
    ell.Radius2 = radius2
    ell.Radius3 = radius3
    body.addObject(ell)
    doc.recompute()
    return ell


def _prisma(name='Prism', sides=6, radius=5.0, height=10.0):
    """PartDesign_AdditivePrism — Prisma poligonal regular aditivo."""
    doc, body = _get_doc_and_body()
    prism = doc.addObject('PartDesign::AdditivePrism', name)
    prism.Polygon      = sides
    prism.Circumradius = radius
    prism.Height       = height
    body.addObject(prism)
    doc.recompute()
    return prism


def _esfera(name='Sphere', radius=5.0):
    """PartDesign_AdditiveSphere — Esfera aditiva."""
    doc, body = _get_doc_and_body()
    sph = doc.addObject('PartDesign::AdditiveSphere', name)
    sph.Radius = radius
    body.addObject(sph)
    doc.recompute()
    return sph


def _toroide(name='Torus', radius1=10.0, radius2=2.0):
    """PartDesign_AdditiveTorus — Toroide (dona) aditivo.
    radius1 = radio mayor (centro del toro al centro del tubo).
    radius2 = radio menor (radio del tubo circular).
    """
    doc, body = _get_doc_and_body()
    tor = doc.addObject('PartDesign::AdditiveTorus', name)
    tor.Radius1 = radius1
    tor.Radius2 = radius2
    body.addObject(tor)
    doc.recompute()
    return tor


def _cuna(name='Wedge', xmin=0.0, ymin=0.0, zmin=0.0,
          xmax=10.0, ymax=10.0, zmax=10.0):
    """PartDesign_AdditiveWedge — Cuña aditiva definida por bounding box."""
    doc, body = _get_doc_and_body()
    wedge = doc.addObject('PartDesign::AdditiveWedge', name)
    wedge.Xmin = xmin
    wedge.Ymin = ymin
    wedge.Zmin = zmin
    wedge.Xmax = xmax
    wedge.Ymax = ymax
    wedge.Zmax = zmax
    body.addObject(wedge)
    doc.recompute()
    return wedge


primitivas = {
    'caja':      _caja,
    'cono':      _cono,
    'cilindro':  _cilindro,
    'elipsoide': _elipsoide,
    'prisma':    _prisma,
    'esfera':    _esfera,
    'toroide':   _toroide,
    'cuna':      _cuna,
    'help':      ayuda,
}
