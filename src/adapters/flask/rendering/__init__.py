"""Design System HTML/CSS renderer for the Flask adapter layer (V4-003).

Renders presentation Design System contracts into reusable HTML and CSS.
Presentation contracts remain the source of truth.

Forbidden: educational logic, persistence, AI.
"""

from __future__ import annotations

from adapters.flask.rendering.accessibility_renderer import AccessibilityRenderer
from adapters.flask.rendering.component_renderer import (
    COMPONENT_TEMPLATE_DIR,
    COMPONENT_TEMPLATES,
    TEMPLATES_DIR,
    ComponentRenderer,
)
from adapters.flask.rendering.html_helpers import (
    css_block,
    element,
    escape,
    escape_attr,
    format_attributes,
    join_classes,
)
from adapters.flask.rendering.style_renderer import StyleRenderer
from adapters.flask.rendering.token_renderer import TokenRenderer

__all__ = [
    "COMPONENT_TEMPLATES",
    "COMPONENT_TEMPLATE_DIR",
    "TEMPLATES_DIR",
    "AccessibilityRenderer",
    "ComponentRenderer",
    "StyleRenderer",
    "TokenRenderer",
    "css_block",
    "element",
    "escape",
    "escape_attr",
    "format_attributes",
    "join_classes",
]
