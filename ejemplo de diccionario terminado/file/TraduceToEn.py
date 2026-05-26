import FreeCADGui as Gui

TraduceToEn = {
   'new':    lambda: Gui.runCommand('Std_New', 0),
   'open':   lambda: Gui.runCommand('Std_Open', 0),
   'close':  lambda: Gui.runCommand('Std_CloseActiveWindow', 0),
   'save':   lambda: Gui.runCommand('Std_Save', 0),
   'saveas': lambda: Gui.runCommand('Std_SaveAs', 0),
    'Help': ayuda,
    'Assistance': ayuda,   # sinónimo adicional
}
#file = {
 #   'new':    lambda: Gui.runCommand('Std_New', 0),
 #   'open':   lambda: Gui.runCommand('Std_Open', 0),
  #  'close':  lambda: Gui.runCommand('Std_CloseActiveWindow', 0),
  #  'save':   lambda: Gui.runCommand('Std_Save', 0),
  #  'saveas': lambda: Gui.runCommand('Std_SaveAs', 0),
  #  'help':   ayuda,
#}
