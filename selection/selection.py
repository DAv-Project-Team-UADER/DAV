import FreeCAD as App
import FreeCADGui as Gui

class ObjectSelection:
    def __init__(self):
        # Internal list of object names to iterate through
        self._ObjectNames = []
        # Current index inside the list
        self._CurrentIndex = 0
        # Internal state of the boolean property
        self._SelectOther = False

    def MonoSelection(self, Obj):
        """Highlights a specific object and focuses it in the 3D view and the tree."""
        if not Obj:
            print("Error: The provided object is not valid.")
            return
            
        Gui.Selection.clearSelection()           # Clears previous selections
        Gui.Selection.addSelection(Obj)          # Makes the object glow (3D and Tree)
        Gui.Control.showInTree()                 # Focuses and scrolls the tree view to it
        Gui.SendMsgToActiveView("ViewSelection") # Centers the 3D camera onto the object
        print(f"Successfully focused: '{Obj.Name}'")

    def VectorSelection(self, ListNames):
        """Initializes the list of object names and resets the counter."""
        if not isinstance(ListNames, list):
            print("Error: A list or vector of strings containing the names is required.")
            return
            
        self._ObjectNames = ListNames
        self._CurrentIndex = 0
        print(f"List loaded with {len(self._ObjectNames)} objects. Ready to iterate.")

    @property
    def SelectOther(self):
        """Allows reading the current state of the property."""
        return self._SelectOther

    @SelectOther.setter
    def SelectOther(self, Value):
        """Triggers automatically when the user writes 'Instance.SelectOther = True'."""
        if Value is True:
            if not self._ObjectNames:
                print("Error: The object list is empty. Load it first using VectorSelection.")
                self._SelectOther = False
                return

            CurrentName = self._ObjectNames[self._CurrentIndex]
            ActiveDoc = App.activeDocument()
            
            if ActiveDoc:
                Obj = ActiveDoc.getObject(CurrentName)
                if Obj:
                    print(f"\n[Advancing] Object {self._CurrentIndex + 1} of {len(self._ObjectNames)}")
                    self.MonoSelection(Obj)
                else:
                    print(f"Warning: The object '{CurrentName}' does not exist in the current document.")
            else:
                print("Error: There is no active document in FreeCAD.")

            self._CurrentIndex = (self._CurrentIndex + 1) % len(self._ObjectNames)
            self._SelectOther = False
        else:
            self._SelectOther = Value

# ==============================================================================
# HOW TO INVOKE THE CLASS USING ALL ACTIVE OBJECTS FROM THE DOCUMENT
# ==============================================================================
#
# # 1. Instantiate the class normally:
# SelectorInstance = ObjectSelection()
#
# # 2. Get the name list of ALL objects from the active document using a list comprehension:
# ActiveObjectNames = [Obj.Name for Obj in App.activeDocument().Objects]
#
# # 3. Pass that automatically generated vector to the VectorSelection method:
# SelectorInstance.VectorSelection(ActiveObjectNames)
#
# # 4. Now you can cyclically iterate through every single object in the tree with:
# SelectorInstance.SelectOther = True
# ==============================================================================
