import FreeCADGui as Gui
from .ayuda import ayuda
from ._parametric import (
    linear_pattern,
    linear_pattern_by_spacing,
    linear_pattern_voice,
    mirrored_voice,
    polar_pattern,
    polar_pattern_voice,
    scaled_by_factor,
    scaled_voice,
)

transform = {
    'linearpattern':  linear_pattern_voice,
    'mirrored':       mirrored_voice,
    'polarpattern':   polar_pattern_voice,
    'multitransform': lambda: Gui.runCommand('PartDesign_MultiTransform', 0),
    'scaled':         scaled_voice,
    'linear_pattern':            linear_pattern,
    'linear_pattern_by_spacing': linear_pattern_by_spacing,
    'polar_pattern':             polar_pattern,
    'scaled_by_factor':          scaled_by_factor,
    'help':           ayuda,
}
