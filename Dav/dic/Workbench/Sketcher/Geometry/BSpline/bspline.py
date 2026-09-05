# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)

import FreeCAD as App
from .ayuda import ayuda
from ._parametric import (
    create_bspline,
    create_bspline_interpolated,
    create_bspline_periodic,
    create_bspline_periodic_interpolated,
)
from selection.createobjects import CreateObjects


def create_bspline_with_objects(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float, label: str = "BSpline"):
    create_bspline(x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, x4=x4, y4=y4, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_bspline_interpolated_with_objects(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float, label: str = "BSplineInterp"):
    create_bspline_interpolated(x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, x4=x4, y4=y4, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_bspline_periodic_with_objects(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float, label: str = "BSplineClosed"):
    create_bspline_periodic(x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, x4=x4, y4=y4, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_bspline_periodic_interpolated_with_objects(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float, label: str = "BSplineClosedInterp"):
    create_bspline_periodic_interpolated(x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, x4=x4, y4=y4, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


bspline = {
    'create':         create_bspline_with_objects,
    'interpolation':  create_bspline_interpolated_with_objects,
    'periodic':       create_bspline_periodic_with_objects,
    'periodicinterp': create_bspline_periodic_interpolated_with_objects,
    'help':        ayuda,
}