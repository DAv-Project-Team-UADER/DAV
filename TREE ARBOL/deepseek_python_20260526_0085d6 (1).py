import FreeCADGui as Gui
from PySide2 import QtGui, QtCore

class TreeViewCapture:
    """
    Class to capture and save an image of FreeCAD's object tree view.
    """
    def __init__(self, SavePath="/tmp/freecad_tree.png"):
        # Path where the snapshot will be saved by default
        self.SavePath = SavePath
        # Reference to the QTreeView widget (found later)
        self.TreeView = None
        # QTimer for periodic captures
        self.Timer = QtCore.QTimer()
        # Connect the timer's timeout signal to the capture method
        self.Timer.timeout.connect(self.CaptureTree)
        # Try to locate the tree view widget right away
        self.__FindTreeView()

    def __FindTreeView(self):
        """Locates the QTreeView widget inside the main FreeCAD window."""
        MainWindow = Gui.getMainWindow()                     # Get the main application window
        if MainWindow:
            # Find the first child widget that is a QTreeView
            self.TreeView = MainWindow.findChild(QtGui.QTreeView)

    def CaptureTree(self, FileName=None):
        """
        Grabs the current appearance of the tree view and saves it as a PNG.
        If no filename is given, the default SavePath is used.
        Returns True if successful, False otherwise.
        """
        # If TreeView wasn't found before, try again now
        if not self.TreeView:
            self.__FindTreeView()
        # If still not found, notify and return failure
        if not self.TreeView:
            print("Could not find the object tree widget.")
            return False

        # Grab the current visual state of the tree view widget
        Snapshot = self.TreeView.grab()
        # Determine the output file path
        Path = FileName if FileName else self.SavePath
        # Save the image to disk
        Snapshot.save(Path, "PNG")
        print(f"Tree snapshot saved to {Path}")
        return True

    def CaptureTreePeriodic(self):
        """Starts automatic capture every 34 seconds."""
        self.Timer.start(34000)   # interval in milliseconds (34 * 1000)

    def StopPeriodic(self):
        """Stops the automatic periodic capture."""
        self.Timer.stop()


# =============================================================================
# EXAMPLE IMPLEMENTATION
# =============================================================================
# This section demonstrates how to use the TreeViewCapture class.
# To test it, copy the entire code into FreeCAD's Python console or run as a macro.

# # Create an instance of the class
# TreeCapture = TreeViewCapture(SavePath="/home/user/freecad_tree_snapshot.png")
# 
# # --- Single capture examples ---
# # Capture with default path
# TreeCapture.CaptureTree()
# 
# # Capture with custom filename
# TreeCapture.CaptureTree(FileName="/home/user/my_custom_tree.png")
# 
# # Capture and check if successful
# Success = TreeCapture.CaptureTree(FileName="/tmp/tree_test.png")
# if Success:
#     print("Capture completed successfully!")
# else:
#     print("Capture failed. Is FreeCAD's GUI running?")
# 
# # --- Periodic capture examples ---
# # Start automatic capture every 34 seconds
# TreeCapture.CaptureTreePeriodic()
# print("Periodic capture started. Snapshot taken every 34 seconds.")
# 
# # Let it run for a while, then stop
# # (In real usage, you'd call this from a button or menu action)
# # TreeCapture.StopPeriodic()
# # print("Periodic capture stopped.")
# 
# # --- Advanced: Using in a FreeCAD macro with a simple dialog ---
# # This creates a small window with buttons to control the capture
# 
# class CaptureControlDialog(QtGui.QDialog):
#     """Simple dialog to control tree view captures."""
#     def __init__(self, Parent=None):
#         super().__init__(Parent)
#         self.TreeCapture = TreeViewCapture()
#         self.InitUi()
#     
#     def InitUi(self):
#         """Set up the dialog interface."""
#         self.setWindowTitle("Tree View Capture Control")
#         self.setMinimumWidth(300)
#         
#         Layout = QtGui.QVBoxLayout()
#         
#         # Capture now button
#         CaptureBtn = QtGui.QPushButton("Capture Now")
#         CaptureBtn.clicked.connect(self.TreeCapture.CaptureTree)
#         Layout.addWidget(CaptureBtn)
#         
#         # Start periodic button
#         StartBtn = QtGui.QPushButton("Start Periodic (34s)")
#         StartBtn.clicked.connect(self.TreeCapture.CaptureTreePeriodic)
#         Layout.addWidget(StartBtn)
#         
#         # Stop periodic button
#         StopBtn = QtGui.QPushButton("Stop Periodic")
#         StopBtn.clicked.connect(self.TreeCapture.StopPeriodic)
#         Layout.addWidget(StopBtn)
#         
#         self.setLayout(Layout)
# 
# # To show the control dialog, uncomment the following lines:
# # Dialog = CaptureControlDialog()
# # Dialog.show()
#
# =============================================================================
# END OF EXAMPLE IMPLEMENTATION
# =============================================================================