# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)

import FreeCAD as App
from .ayuda import ayuda
from ._parametric import create_arc_slot_rounded, create_arc_slot_flat
from selection.createobjects import CreateObjects


def create_arc_slot_rounded_with_objects(
    cx: float,
    cy: float,
    radius: float,
    angle_start: float,
    angle_end: float,
    width: float,
    label: str = "ArcSlot",
):
    create_arc_slot_rounded(
        cx=cx, cy=cy, radius=radius,
        angle_start=angle_start, angle_end=angle_end, width=width, label=label,
    )
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_arc_slot_flat_with_objects(
    cx: float,
    cy: float,
    radius: float,
    angle_start: float,
    angle_end: float,
    width: float,
    label: str = "ArcSlot",
):
    create_arc_slot_flat(
        cx=cx, cy=cy, radius=radius,
        angle_start=angle_start, angle_end=angle_end, width=width, label=label,
    )
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


arc_slot = {
    'arc_ends':  create_arc_slot_rounded_with_objects,
    'rounded':   create_arc_slot_rounded_with_objects,
    'flat_ends': create_arc_slot_flat_with_objects,
    'flat':      create_arc_slot_flat_with_objects,
    'help':      ayuda
}