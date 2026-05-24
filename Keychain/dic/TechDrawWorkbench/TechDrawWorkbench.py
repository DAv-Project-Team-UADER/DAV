from .Views.view import views
from .Dimensions.dimensions import dimensions
from .AddLines.addLines import centerlines
from .Symbols.weld import symbols
from .ayuda import ayuda

techdraw_workbench = {
    'views': views,
    'dimensions': dimensions,
    'AddLines': centerlines,
    'Symbols': symbols,
    'help': ayuda
}