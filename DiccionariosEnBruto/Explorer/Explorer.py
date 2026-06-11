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
from .StructureToolbar.structure        import structure
from .ayuda                             import ayuda

explorer = {}
explorer.update(file)
explorer.update(edit)
explorer.update(print_cmds)
explorer.update(windows)
explorer.update(expressions)
explorer.update(tools)
explorer.update(structure)
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

