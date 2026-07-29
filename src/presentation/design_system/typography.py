"""Typography roles — Inter hierarchy (DX-001 / DX-006A).

One family. Hierarchy from size and weight only.
Canonical product scale: 32 / 24 / 18 / 16 / 14 / 12.
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
    """Named typography roles for DX-006A surfaces.

    HEADING aliases PAGE; SUBHEADING aliases SECTION for legacy callers.
    """

    DISPLAY = "display"
    PAGE = "page"
    HEADING = "heading"
    SECTION = "section"
    SUBHEADING = "subheading"
    BODY = "body"
    SUPPORT = "support"
    CAPTION = "caption"
    MONOSPACE = "monospace"


FONT_FAMILY_SANS = '"Inter", system-ui, -apple-system, "Segoe UI", sans-serif'
FONT_FAMILY_MONO = '"SF Mono", "Fira Code", "Fira Mono", Menlo, Consolas, monospace'

TYPE_STYLES: Mapping[TypeRole, TypeStyle] = {
    TypeRole.DISPLAY: TypeStyle(
        family=FONT_FAMILY_SANS,
        size_px=32,
        size_rem="2rem",
        weight=600,
        line_height=1.2,
        letter_spacing="-0.02em",
        css_var_size="--font-display",
        css_var_weight="--font-weight-semibold",
    ),
    TypeRole.PAGE: TypeStyle(
        family=FONT_FAMILY_SANS,
        size_px=24,
        size_rem="1.5rem",
        weight=600,
        line_height=1.25,
        letter_spacing="-0.015em",
        css_var_size="--font-page",
        css_var_weight="--font-weight-semibold",
    ),
    TypeRole.HEADING: TypeStyle(
        family=FONT_FAMILY_SANS,
        size_px=24,
        size_rem="1.5rem",
        weight=600,
        line_height=1.25,
        letter_spacing="-0.015em",
        css_var_size="--font-page",
        css_var_weight="--font-weight-semibold",
    ),
    TypeRole.SECTION: TypeStyle(
        family=FONT_FAMILY_SANS,
        size_px=18,
        size_rem="1.125rem",
        weight=600,
        line_height=1.3,
        letter_spacing="-0.01em",
        css_var_size="--font-section",
        css_var_weight="--font-weight-semibold",
    ),
    TypeRole.SUBHEADING: TypeStyle(
        family=FONT_FAMILY_SANS,
        size_px=18,
        size_rem="1.125rem",
        weight=600,
        line_height=1.3,
        letter_spacing="-0.01em",
        css_var_size="--font-section",
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
    TypeRole.SUPPORT: TypeStyle(
        family=FONT_FAMILY_SANS,
        size_px=14,
        size_rem="0.875rem",
        weight=400,
        line_height=1.45,
        letter_spacing="0",
        css_var_size="--font-support",
        css_var_weight="--font-weight-normal",
    ),
    TypeRole.CAPTION: TypeStyle(
        family=FONT_FAMILY_SANS,
        size_px=12,
        size_rem="0.75rem",
        weight=500,
        line_height=1.4,
        letter_spacing="0.01em",
        css_var_size="--font-caption",
        css_var_weight="--font-weight-medium",
    ),
    TypeRole.MONOSPACE: TypeStyle(
        family=FONT_FAMILY_MONO,
        size_px=14,
        size_rem="0.875rem",
        weight=400,
        line_height=1.45,
        letter_spacing="0",
        css_var_size="--font-support",
        css_var_weight="--font-weight-normal",
    ),
}

# DX-001 / DX-006A canonical hierarchy sizes (px).
CANONICAL_TYPE_SIZES_PX: frozenset[int] = frozenset({32, 24, 18, 16, 14, 12})


def type_style(role: TypeRole) -> TypeStyle:
    """Resolve a typography role."""
    return TYPE_STYLES[role]
