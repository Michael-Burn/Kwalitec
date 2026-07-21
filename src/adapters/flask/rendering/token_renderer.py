"""TokenRenderer — Design System tokens → CSS custom properties.

Exposes the presentation token catalogue as reusable CSS variables.
Presentation contracts remain the source of truth.
"""

from __future__ import annotations

from adapters.flask.rendering.html_helpers import css_block
from presentation.design_system import DesignTokens, get_tokens
from presentation.design_system.layout import BREAKPOINTS, CONTAINERS, GRIDS
from presentation.design_system.spacing import SPACING


class TokenRenderer:
    """Render design tokens into CSS custom-property declarations."""

    def __init__(self, tokens: DesignTokens | None = None) -> None:
        self._tokens = tokens or get_tokens()

    @property
    def tokens(self) -> DesignTokens:
        return self._tokens

    def css_variables(self) -> dict[str, str]:
        """Return flat CSS custom-property name → value mapping."""
        props = dict(self._tokens.css_custom_properties())
        for spec in CONTAINERS.values():
            if spec.max_width_rem is not None:
                props[spec.css_var] = spec.max_width_rem
            elif spec.max_width_px is not None:
                props[spec.css_var] = f"{spec.max_width_px}px"
            else:
                props[spec.css_var] = "100%"
        props["--ds-hover-lift"] = f"{self._tokens.hover_lift_px}px"
        props["--ds-press-scale"] = str(self._tokens.press_scale)
        props["--ds-disabled-opacity"] = str(self._tokens.disabled_opacity)
        props["--icon-stroke-width"] = str(self._tokens.icon_stroke_width)
        return props

    def root_stylesheet(self) -> str:
        """Emit a ``:root`` stylesheet block for all design tokens."""
        return css_block(":root", self.css_variables())

    def style_tag(self, *, include_responsive: bool = True) -> str:
        """Wrap token CSS in a ``<style>`` element for embedding."""
        parts = [self.root_stylesheet()]
        if include_responsive:
            parts.append(self.responsive_stylesheet())
            parts.append(self.reduced_motion_stylesheet())
        return f"<style data-ds-tokens>\n{chr(10).join(parts)}\n</style>"

    def responsive_stylesheet(self) -> str:
        """Emit responsive container / grid helpers from layout tokens."""
        rules: list[str] = [
            css_block(
                ".ds-container",
                {
                    "width": "100%",
                    "margin-inline": "auto",
                    "box-sizing": "border-box",
                },
            ),
            css_block(
                '.ds-container[data-width="narrow"]',
                {"max-width": "var(--container-narrow)"},
            ),
            css_block(
                '.ds-container[data-width="content"]',
                {"max-width": "var(--container-content)"},
            ),
            css_block(
                '.ds-container[data-width="wide"]',
                {"max-width": "var(--container-wide)"},
            ),
            css_block(
                '.ds-container[data-width="full"]',
                {"max-width": "var(--container-full)"},
            ),
        ]
        for breakpoint, grid in GRIDS.items():
            media = BREAKPOINTS[breakpoint].css_media
            gutter = SPACING[grid.gutter].css_var
            margin = SPACING[grid.margin].css_var
            rules.append(
                f"@media {media} {{\n"
                f"  .ds-grid {{ display: grid; "
                f"grid-template-columns: repeat({grid.columns}, minmax(0, 1fr)); "
                f"gap: var({gutter}); }}\n"
                f"  .ds-container {{ padding-inline: var({margin}); }}\n"
                f"}}"
            )
        return "\n".join(rules)

    def reduced_motion_stylesheet(self) -> str:
        """Honour ``prefers-reduced-motion`` for design-system surfaces."""
        return (
            "@media (prefers-reduced-motion: reduce) {\n"
            "  .ds-component, .ds-component * {\n"
            "    animation-duration: 0.01ms !important;\n"
            "    animation-iteration-count: 1 !important;\n"
            "    transition-duration: 0.01ms !important;\n"
            "    scroll-behavior: auto !important;\n"
            "  }\n"
            "}"
        )
