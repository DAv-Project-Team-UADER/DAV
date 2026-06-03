import FreeCADGui as Gui
from .base.base import base
from .additive.additive import additive
from .subtractive.subtractive import subtractive
from .modify.modify import modify
from .transform.transform import transform
from .manage.manage import manage
from .ayuda import ayuda

partdesign = {
    'base':        base,
    'additive':    additive,
    'subtractive': subtractive,
    'modify':      modify,
    'transform':   transform,
    'manage':      manage,
    'help':        ayuda,
}
