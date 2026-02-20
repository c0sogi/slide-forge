from .default import TEMPLATE_PATH, get_presentation
from .default.slide import (
    add_bullet,
    add_content_box,
    add_section,
    add_slide_title,
    add_spacer,
    create_cover_slide,
    create_slide,
)

__all__ = [
    "create_slide",
    "create_cover_slide",
    "add_slide_title",
    "add_content_box",
    "add_section",
    "add_bullet",
    "add_spacer",
    "TEMPLATE_PATH",
    "get_presentation",
]
