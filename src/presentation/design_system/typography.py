"""Typography roles — Inter hierarchy (UX-001).

One family. Hierarchy from size and weight only.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class TypeStyle:
    """A typographic role resolved to concrete metrics."""

    family: str
    size_px: int
    size_rem: str
    weight: int
    line_height: float
    letter_spacing: str
    css_var_size: str
    css_var_weight: str


class TypeRole(str, Enum):
    """Named typography roles for V3 surfaces."""

    DISPLAY = "display"
    HEADING = "heading"
    SUBHEADING = "subheading"
    BODY = "body"
    CAPTION = "caption"
    MONOSPACE = "monospace"


FONT_FAMILY_SANS = '"Inter", system-ui, -apple-system, "Segoe UI", sans-serif'
FONT_FAMILY_MONO = '"SF Mono", "Fira Code", "Fira Mono", Menlo, Consolas, monospace'

TYPE_STYLES: Mapping[TypeRole, TypeStyle] = {
    TypeRole.DISPLAY: TypeStyle(
        family=FONT_FAMILY_SANS,
        size_px=40,
        size_rem="2.5rem",
        weight=600,
        line_height=1.2,
        letter_spacing="-0.02em",
        css_var_size="--font-4xl",
        css_var_weight="--font-weight-semibold",
    ),
    TypeRole.HEADING: TypeStyle(
        family=FONT_FAMILY_SANS,
        size_px=28,
        size_rem="1.75rem",
        weight=600,
        line_height=1.2,
        letter_spacing="-0.02em",
        css_var_size="--font-2xl",
        css_var_weight="--font-weight-semibold",
    ),
    TypeRole.SUBHEADING: TypeStyle(
        family=FONT_FAMILY_SANS,
        size_px=20,
        size_rem="1.25rem",
        weight=600,
        line_height=1.3,
        letter_spacing="-0.01em",
        css_var_size="--font-lg",
        css_var_weight="--font-weight-semibold",
    ),
    TypeRole.BODY: TypeStyle(
        family=FONT_FAMILY_SANS,
        size_px=16,
        size_rem="1rem",
        weight=400,
        line_height=1.5,
        letter_spacing="0",
        css_var_size="--font-base",
        css_var_weight="--font-weight-normal",
    ),
    TypeRole.CAPTION: TypeStyle(
        family=FONT_FAMILY_SANS,
        size_px=14,
        size_rem="0.875rem",
        weight=500,
        line_height=1.4,
        letter_spacing="0.02em",
        css_var_size="--font-sm",
        css_var_weight="--font-weight-medium",
    ),
    TypeRole.MONOSPACE: TypeStyle(
        family=FONT_FAMILY_MONO,
        size_px=14,
        size_rem="0.875rem",
        weight=400,
        line_height=1.5,
        letter_spacing="0",
        css_var_size="--font-sm",
        css_var_weight="--font-weight-normal",
    ),
}

# UX-001 canonical hierarchy sizes (px).
CANONICAL_TYPE_SIZES_PX: frozenset[int] = frozenset({40, 28, 20, 16, 14})


def type_style(role: TypeRole) -> TypeStyle:
    """Resolve a typography role."""
    return TYPE_STYLES[role]
