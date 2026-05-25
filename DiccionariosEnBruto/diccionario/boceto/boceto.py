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
# Fuentes: remito_PartDesign_Pad.txt, Revolution.txt, AdditiveHelix.txt,
#          AdditiveLoft.txt, AdditivePipe.txt
# Revisión: El campo <script nativo> de estos tickets contiene funciones Python
#   completas, que es el enfoque correcto para PartDesign (scripting API).
#   El campo <Requiere> listaba parámetros de función, no precondiciones GUI.
#   Las precondiciones reales (Body activo, boceto preexistente) quedan en ayuda.py.
#   Para AdditiveHelix y Revolution se vincula ReferenceAxis al origen del Body
#   para evitar errores "zero norm vector" y de perpendicularidad en FreeCAD ≥0.20.
# ─────────────────────────────────────────────────────────────────────────────

import FreeCAD as App
from .ayuda import ayuda


def _get_doc_and_body():
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument()
    body = doc.getObject('Body')
    if body is None:
        body = doc.addObject('PartDesign::Body', 'Body')
    return doc, body


def _extrusion(name, sketch_name, length=10.0):
    """PartDesign_Pad — Extrusión de boceto cerrado."""
    doc, body = _get_doc_and_body()
    sketch = doc.getObject(sketch_name)
    if sketch is None:
        raise ValueError(
            f"El boceto '{sketch_name}' no existe. "
            "Crea un boceto cerrado en el Body primero."
        )
    pad = doc.addObject('PartDesign::Pad', name)
    pad.Profile = sketch
    pad.Length  = length
    body.addObject(pad)
    doc.recompute()
    return pad


def _revolucion(name, sketch_name, angle=360.0):
    """PartDesign_Revolution — Revolución de boceto alrededor del eje Y del Body."""
    doc, body = _get_doc_and_body()
    sketch = doc.getObject(sketch_name)
    if sketch is None:
        raise ValueError(
            f"El boceto '{sketch_name}' no existe. "
            "Crea un boceto cerrado en el Body primero."
        )
    rev = doc.addObject('PartDesign::Revolution', name)
    rev.Profile = sketch
    rev.Angle   = angle
    # ReferenceAxis: eje Y del origen del Body (índice 1).
    # Evita el error de perpendicularidad en FreeCAD ≥ 0.21.
    rev.ReferenceAxis = (body.Origin.OriginFeatures[1], [''])
    body.addObject(rev)
    doc.recompute()
    return rev


def _helice(name, sketch_name, pitch=10.0, height=50.0):
    """PartDesign_AdditiveHelix — Barrido helicoidal de perfil (resortes, roscas).
    Vincula el eje al eje Z del origen del Body (evita 'zero norm vector').
    """
    doc, body = _get_doc_and_body()
    sketch = doc.getObject(sketch_name)
    if sketch is None:
        raise ValueError(
            f"El boceto '{sketch_name}' no existe. "
            "Crea un boceto cerrado en el Body primero."
        )
    helix = doc.addObject('PartDesign::AdditiveHelix', name)
    helix.Profile = sketch
    helix.Pitch   = pitch
    helix.Height  = height
    # ReferenceAxis: eje Z del origen del Body (índice 2).
    helix.ReferenceAxis = (body.Origin.OriginFeatures[2], [''])
    body.addObject(helix)
    doc.recompute()
    return helix


def _loft(name, sketch_names):
    """PartDesign_AdditiveLoft — Transición suave entre ≥2 bocetos."""
    if len(sketch_names) < 2:
        raise ValueError('AdditiveLoft requiere al menos 2 bocetos en sketch_names.')
    doc, body = _get_doc_and_body()
    profiles = []
    for s_name in sketch_names:
        s = doc.getObject(s_name)
        if s is None:
            raise ValueError(
                f"El boceto '{s_name}' no existe. "
                "Todos los bocetos deben existir antes de ejecutar."
            )
        profiles.append(s)
    loft = doc.addObject('PartDesign::AdditiveLoft', name)
    loft.Profile  = profiles[0]
    loft.Sections = profiles[1:]
    body.addObject(loft)
    doc.recompute()
    return loft


def _tubo(name, sketch_name, path_name):
    """PartDesign_AdditivePipe — Barrido de perfil a lo largo de trayectoria."""
    doc, body = _get_doc_and_body()
    profile = doc.getObject(sketch_name)
    spine   = doc.getObject(path_name)
    if profile is None:
        raise ValueError(
            f"El boceto de perfil '{sketch_name}' no existe. Créalo primero."
        )
    if spine is None:
        raise ValueError(
            f"El boceto de trayectoria '{path_name}' no existe. Créalo primero."
        )
    pipe = doc.addObject('PartDesign::AdditivePipe', name)
    pipe.Profile = profile
    pipe.Spine   = spine
    body.addObject(pipe)
    doc.recompute()
    return pipe


boceto = {
    'extrusion':  _extrusion,
    'revolucion': _revolucion,
    'helice':     _helice,
    'loft':       _loft,
    'tubo':       _tubo,
    'help':       ayuda,
}
