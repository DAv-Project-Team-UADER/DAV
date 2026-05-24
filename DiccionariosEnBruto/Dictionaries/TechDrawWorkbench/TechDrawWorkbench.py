from .Views.views import views
from .Dimensions.dimensions import dimensions
from .AddLines.addLines import add_lines
from .Annotations.annotations import annotations
from .AddVertices.addVertices import add_vertices
from .Hatching.hatching import hatching
from .OtherViews.otherViews import other_views
from .help import help

techdraw_workbench = {
    'views': views,
    'dimensions': dimensions,
    'add_lines': add_lines,
    'annotations': annotations,
    'add_vertices': add_vertices,
    'hatching': hatching,
    'other_views': other_views,
    'help': help
}
