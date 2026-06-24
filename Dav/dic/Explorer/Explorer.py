# Copyright (C) 2026 The DAV Project Team
# Universidad Autónoma de Entre Ríos (UADER)
# SPDX-License-Identifier: GPL-3.0-or-later

import FreeCADGui as Gui
from .File.File                         import file
from .Edit.Edit                         import edit
from .Print.Print                       import print_cmds
from .Windows.Windows                   import windows
from .Expressions.Expressions           import expressions
from .Tools.Tools                       import tools
from .StructureToolbar.StructureToolbar import structure
from .ayuda                             import ayuda

# Subcontextos anidados: el Browser navega por niveles y explorer/TraduceTo*.py
# espera explorer['file'], explorer['edit'], ... como submenús (no aplanados).
explorer = {}
explorer.update({'file':        file})
explorer.update({'edit':        edit})
explorer.update({'print':       print_cmds})
explorer.update({'windows':     windows})
explorer.update({'expressions': expressions})
explorer.update({'tools':       tools})
explorer.update({'structure':   structure})
# Callables directos al ras (sin subcontexto)
explorer.update({
    'refresh':      lambda: Gui.runCommand('Std_Refresh', 0),
    'screenshot':   lambda: Gui.runCommand('Std_ViewScreenShot', 0),
    'textdoc':      lambda: Gui.runCommand('Std_TextDocument', 0),
    'unlink':       lambda: Gui.runCommand('Std_LinkUnlink', 0),
    'freeze':       lambda: Gui.runCommand('Std_ToggleFreeze', 0),
    'allinstances': lambda: Gui.runCommand('Std_TreeSelectAllInstances', 0),
    'variableset':  lambda: Gui.runCommand('Std_VarSet', 0),
    'help':         ayuda,
})

