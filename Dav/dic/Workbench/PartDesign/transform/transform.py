import FreeCADGui as Gui
from .ayuda import ayuda
from ._parametric import (
    linear_pattern,
    linear_pattern_by_spacing,
    polar_pattern,
    scaled_by_factor,
)

transform = {
    'linearpattern':  lambda: Gui.runCommand('PartDesign_LinearPattern', 0),
    'mirrored':       lambda: Gui.runCommand('PartDesign_Mirrored', 0),
    'polarpattern':   lambda: Gui.runCommand('PartDesign_PolarPattern', 0),
    'multitransform': lambda: Gui.runCommand('PartDesign_MultiTransform', 0),
    'scaled':         lambda: Gui.runCommand('PartDesign_Scaled', 0),
    'linear_pattern':            linear_pattern,
    'linear_pattern_by_spacing': linear_pattern_by_spacing,
    'polar_pattern':             polar_pattern,
    'scaled_by_factor':          scaled_by_factor,
    'help':           ayuda,
}
