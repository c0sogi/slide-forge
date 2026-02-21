from .default import TEMPLATE_PATH, get_presentation
from .default.slide import (
    Color,
    VisualArea,
    add_bullet,
    add_content_box,
    add_line,
    add_section,
    add_shape,
    add_slide_title,
    add_spacer,
    create_cover_slide,
    create_slide,
    visual_area,
)

__version__ = "1.3.0"

__all__ = [
    "__version__",
    "Color",
    "VisualArea",
    "create_slide",
    "create_cover_slide",
    "add_slide_title",
    "add_content_box",
    "add_section",
    "add_bullet",
    "add_spacer",
    "add_shape",
    "add_line",
    "visual_area",
    "TEMPLATE_PATH",
    "get_presentation",
]
