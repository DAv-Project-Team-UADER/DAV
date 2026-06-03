import FreeCADGui as Gui
from .file.file import file
from .edit.edit import edit
from .print.print_cmds import print_cmds
from .doc.doc import doc
from .view.view import view as view_cmds
from .ayuda import ayuda

explorer = {
    'file':       file,
    'edit':       edit,
    'print':      print_cmds,
    'doc':        doc,
    'view':       view_cmds,
    'refresh':    lambda: Gui.runCommand('Std_Refresh', 0),
    'screenshot': lambda: Gui.runCommand('Std_ViewScreenShot', 0),
    'textdoc':    lambda: Gui.runCommand('Std_TextDocument', 0),
    'help':       ayuda,
}
