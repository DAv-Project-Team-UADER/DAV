import FreeCADGui as Gui
import ayuda

TraduceToPT = {
   'novo':    lambda: Gui.runCommand('Std_New', 0),
   'abrir':   lambda: Gui.runCommand('Std_Open', 0),
   'fechar':  lambda: Gui.runCommand('Std_CloseActiveWindow', 0),
   'salvar':   lambda: Gui.runCommand('Std_Save', 0),
   'salvar como': lambda: Gui.runCommand('Std_SaveAs', 0),
    'ajuda': ayuda,
    'Assistência': ayuda,   # sinónimo adicional
}
#file = {
 #   'new':    lambda: Gui.runCommand('Std_New', 0),
 #   'open':   lambda: Gui.runCommand('Std_Open', 0),
  #  'close':  lambda: Gui.runCommand('Std_CloseActiveWindow', 0),
  #  'save':   lambda: Gui.runCommand('Std_Save', 0),
  #  'saveas': lambda: Gui.runCommand('Std_SaveAs', 0),
  #  'help':   ayuda,
#}
