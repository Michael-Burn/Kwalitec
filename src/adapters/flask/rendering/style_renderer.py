"""StyleRenderer — StyleContract → CSS declarations.

Maps presentation style contracts onto CSS custom-property references.
Never invents colours, spacing, or type outside the Design System.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from adapters.flask.rendering.html_helpers import escape_attr
from presentation.design_system.colours import BrandColour, SemanticColour, colour
from presentation.design_system.components.base import StyleContract
from presentation.design_system.elevation import ElevationToken, elevation
from presentation.design_system.motion import MotionToken, motion
from presentation.design_system.radius import RadiusToken, radius
from presentation.design_system.spacing import SpacingToken, space
from presentation.design_system.typography import TypeRole, type_style


class StyleRenderer:
    """Render ``StyleContract`` values as CSS declaration maps / inline styles."""

    def declarations(self, style: StyleContract) -> dict[str, str]:
        """Build CSS property → value map using Design System CSS variables."""
        decls: dict[str, str] = {}
        if style.background is not None:
            decls["background-color"] = self._css_var(style.background)
        if style.foreground is not None:
            decls["color"] = self._css_var(style.foreground)
        if style.border is not None:
            decls["border-color"] = self._css_var(style.border)
            decls.setdefault("border-style", "solid")
            decls.setdefault("border-width", "1px")
        if style.typography is not None:
            decls.update(self._typography(style.typography))
        if style.padding_x is not None:
            decls["padding-inline"] = self._space_var(style.padding_x)
        if style.padding_y is not None:
            decls["padding-block"] = self._space_var(style.padding_y)
        if style.gap is not None:
            decls["gap"] = self._space_var(style.gap)
        if style.radius is not None:
            decls["border-radius"] = self._radius_var(style.radius)
        if style.elevation is not None:
            decls["box-shadow"] = self._elevation_var(style.elevation)
        if style.motion is not None:
            decls["transition"] = self._motion_var(style.motion)
        for key, value in style.extras:
            decls[self._extra_property(key)] = self._resolve_extra(value)
        return decls

    def inline_style(self, style: StyleContract) -> str:
        """Serialise a style contract as an inline ``style`` attribute value."""
        decls = self.declarations(style)
        return "; ".join(f"{prop}: {value}" for prop, value in decls.items())

    def style_attribute(self, style: StyleContract) -> dict[str, str]:
        """Return ``{"style": "..."}`` when the contract has declarations."""
        rendered = self.inline_style(style)
        if not rendered:
            return {}
        return {"style": rendered}

    def class_names(self, *parts: Any) -> str:
        """Join component class names (presentation-only helpers)."""
        tokens: list[str] = []
        for part in parts:
            if not part:
                continue
            tokens.append(str(part).strip())
        return " ".join(token for token in tokens if token)

    def component_stylesheet(self, class_name: str, style: StyleContract) -> str:
        """Emit a CSS rule for a component class from its style contract."""
        decls = self.declarations(style)
        if not decls:
            return f".{class_name} {{}}"
        body = "; ".join(f"{prop}: {value}" for prop, value in decls.items())
        return f".{escape_attr(class_name)} {{ {body}; }}"

    def _typography(self, role: TypeRole) -> dict[str, str]:
        style = type_style(role)
        return {
            "font-family": style.family,
            "font-size": f"var({style.css_var_size})",
            "font-weight": f"var({style.css_var_weight})",
            "line-height": str(style.line_height),
            "letter-spacing": style.letter_spacing,
        }

    def _css_var(self, token: SemanticColour | BrandColour | Enum) -> str:
        if isinstance(token, SemanticColour | BrandColour):
            return f"var({colour(token).css_var})"
        if isinstance(token, Enum):
            return f"var(--{token.value})"
        return str(token)

    def _space_var(self, token: SpacingToken) -> str:
        return f"var({space(token).css_var})"

    def _radius_var(self, token: RadiusToken) -> str:
        return f"var({radius(token).css_var})"

    def _elevation_var(self, token: ElevationToken) -> str:
        return f"var({elevation(token).css_var})"

    def _motion_var(self, token: MotionToken) -> str:
        return f"var({motion(token).css_var})"

    def _extra_property(self, key: str) -> str:
        mapping = {
            "hover_background": "--ds-hover-background",
            "track_height": "height",
            "size": "width",
            "orientation": "--ds-orientation",
            "variant": "--ds-variant",
        }
        return mapping.get(key, f"--ds-{key.replace('_', '-')}")

    def _resolve_extra(self, value: str) -> str:
        try:
            semantic = SemanticColour(value)
            return f"var({colour(semantic).css_var})"
        except ValueError:
            pass
        try:
            spacing = SpacingToken(value)
            return f"var({space(spacing).css_var})"
        except ValueError:
            pass
        return value
