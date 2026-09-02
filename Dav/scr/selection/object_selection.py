#  Copyright (C) 2026 The DAV Project Team-                                 |#  Copyright (C) 2026 El Equipo del Proyecto DAV
#  Universidad Autónoma de Entre Ríos (UADER)                               |#  Universidad Autónoma de Entre Ríos (UADER)
#  Directed by Gerard Guillermo and Gallo Fabricio David                    |#  Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#                                                                           |#
#  This program is free software: you can redistribute it and/or modify     |#  Este programa es software libre: usted puede redistribuirlo y/o modificarlo
#  it under the terms of the GNU General Public License as published by     |#  bajo los términos de la Licencia Pública General GNU tal como fue publicada 
#  the Free Software Foundation, in GLPv3 version  of the License           |#  por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#                                                                           |#
#  This program is distributed in the hope that it will be useful,          |#  Este programa se distribuye con la esperanza de que sea útil,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           |#  pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            |#  MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
#  GNU General Public License for more details.                             |#  Licencia Pública General GNU para más detalles.
#                                                                           |#
#  You should have received a copy of the GNU General Public License        |#  Deberías haber recibido una copia de la Licencia Pública General GNU
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.   |#  junto con este programa. Si no es así, consulte <https://www.gnu.org/licenses/>.

import re
import unicodedata

import FreeCAD as App
import FreeCADGui as Gui

class ObjectSelection:
    def __init__(self):
        # Internal list of object names to iterate through
        self._ObjectNames = []
        # Current index inside the list
        self._CurrentIndex = 0
        # Index of the last actually selected object
        self._LastSelectedIndex = -1
        # Internal state of the boolean property
        self._SelectOther = False

    def MonoSelection(self, Obj):
        """Highlights a specific object and focuses it in the 3D view and the tree."""
        if not Obj:
            print("Error: The provided object is not valid.")
            return
            
        Gui.Selection.clearSelection()           # Clears previous selections
        Gui.Selection.addSelection(Obj)          # Makes the object glow (3D and Tree)
        try:
            Gui.Control.showInTree()                 # Focuses and scrolls the tree view to it
        except AttributeError:
            pass # Not available in FreeCAD 1.1+
        Gui.SendMsgToActiveView("ViewSelection") # Centers the 3D camera onto the object
        print(f"Successfully focused: '{Obj.Name}'")

    def VectorSelection(self, ListNames):
        """Initializes the list of object names and resets the counter."""
        if not isinstance(ListNames, list):
            print("Error: A list or vector of strings containing the names is required.")
            return
            
        self._ObjectNames = ListNames
        self._CurrentIndex = 0
        self._LastSelectedIndex = -1
        print(f"List loaded with {len(self._ObjectNames)} objects. Ready to iterate.")

    @property
    def SelectOther(self):
        """Allows reading the current state of the property."""
        return self._SelectOther

    def SelectNext(self):
        """Advances to the next object in the list (cyclic).

        If the list is empty, loads all objects from the active document first.
        """
        ActiveDoc = App.activeDocument()

        if not ActiveDoc:
            print("Error: There is no active document in FreeCAD.")
            return

        if not self._ObjectNames:
            ObjectNames = [Obj.Name for Obj in ActiveDoc.Objects]
            self.VectorSelection(ObjectNames)

        if not self._ObjectNames:
            print("Error: The document has no objects.")
            return

        CurrentName = self._ObjectNames[self._CurrentIndex]
        Obj = ActiveDoc.getObject(CurrentName)

        if Obj:
            print(f"\n[Next] Object {self._CurrentIndex + 1} of {len(self._ObjectNames)}")
            self.MonoSelection(Obj)
        else:
            print(f"Warning: The object '{CurrentName}' does not exist in the current document.")

        self._LastSelectedIndex = self._CurrentIndex
        self._CurrentIndex = (self._CurrentIndex + 1) % len(self._ObjectNames)

    def SelectPrevious(self):
        """Goes back to the previous object in the list (cyclic).

        If the list is empty, loads all objects from the active document first.
        """
        ActiveDoc = App.activeDocument()

        if not ActiveDoc:
            print("Error: There is no active document in FreeCAD.")
            return

        if not self._ObjectNames:
            ObjectNames = [Obj.Name for Obj in ActiveDoc.Objects]
            self.VectorSelection(ObjectNames)

        if not self._ObjectNames:
            print("Error: The document has no objects.")
            return

        if self._LastSelectedIndex >= 0:
            target = (self._LastSelectedIndex - 1) % len(self._ObjectNames)
        else:
            target = (self._CurrentIndex - 1) % len(self._ObjectNames)

        CurrentName = self._ObjectNames[target]
        Obj = ActiveDoc.getObject(CurrentName)

        if Obj:
            print(f"\n[Previous] Object {target + 1} of {len(self._ObjectNames)}")
            self.MonoSelection(Obj)
        else:
            print(f"Warning: The object '{CurrentName}' does not exist in the current document.")

        self._LastSelectedIndex = target
        self._CurrentIndex = (target + 1) % len(self._ObjectNames)

    def SelectAll(self):
        """Selects all objects in the active document."""
        ActiveDoc = App.activeDocument()

        if not ActiveDoc:
            print("Error: There is no active document in FreeCAD.")
            return

        Gui.Selection.clearSelection()

        for Obj in ActiveDoc.Objects:
            Gui.Selection.addSelection(Obj)

        print(f"Selected {len(ActiveDoc.Objects)} objects.")

    def DeselectAll(self):
        """Clears the current selection."""
        Gui.Selection.clearSelection()
        print("Selection cleared.")

    def SelectByLabel(self, Text):
        """Selects the object whose Label matches the dictated text.

        Matching is lenient: accents, case and spaces are ignored, so "mesa
        chica" matches a label of "Mesa Chica". Falls back to a prefix match
        when no exact match exists.

        Args:
            Text: Name dictated by the user.

        Returns:
            The matched object Name, or None when nothing matched.
        """
        ActiveDoc = App.activeDocument()

        if not ActiveDoc:
            print("Error: There is no active document in FreeCAD.")
            return None

        Wanted = self._NormalizeForMatch(Text)
        if not Wanted:
            print("Error: No name was dictated.")
            return None

        Exact = []
        Partial = []
        for Obj in ActiveDoc.Objects:
            Candidate = self._NormalizeForMatch(getattr(Obj, "Label", ""))
            if not Candidate:
                continue
            if Candidate == Wanted:
                Exact.append(Obj)
            elif Candidate.startswith(Wanted) or Wanted.startswith(Candidate):
                Partial.append(Obj)

        Matches = Exact or Partial
        if not Matches:
            print(f"Warning: No object matches the name '{Text}'.")
            return None

        if len(Matches) > 1:
            Names = ", ".join(Obj.Label for Obj in Matches)
            print(f"Warning: '{Text}' is ambiguous ({Names}). Using the first one.")

        Target = Matches[0]
        self.MonoSelection(Target)

        # Deja el cursor de recorrido sobre el objeto elegido, para que un
        # "siguiente" posterior continue desde aca y no desde el indice viejo.
        if Target.Name in self._ObjectNames:
            self._LastSelectedIndex = self._ObjectNames.index(Target.Name)
            self._CurrentIndex = (self._LastSelectedIndex + 1) % len(self._ObjectNames)

        return Target.Name

    @staticmethod
    def _NormalizeForMatch(Text):
        """Folds text for lenient matching (no accents, no case, no spaces)."""
        if not Text:
            return ""
        Folded = (
            unicodedata.normalize("NFKD", Text)
            .encode("ASCII", "ignore")
            .decode()
            .lower()
        )
        return re.sub(r"[^a-z0-9]", "", Folded)

    def GetCurrentObject(self):
        """Returns the name of the last selected object, or None."""
        if not self._ObjectNames or self._LastSelectedIndex < 0:
            return None

        return self._ObjectNames[self._LastSelectedIndex]

    def GetObjectCount(self):
        """Returns the number of objects in the current list."""
        return len(self._ObjectNames)

    @SelectOther.setter
    def SelectOther(self, Value):
        """Triggers automatically when the user writes 'Instance.SelectOther = True'."""
        if Value is True:
            self.SelectNext()
        else:
            self._SelectOther = Value
