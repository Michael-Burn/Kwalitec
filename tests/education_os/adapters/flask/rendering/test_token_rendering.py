"""CSS token rendering tests for V4-003."""

from __future__ import annotations

from adapters.flask.rendering import StyleRenderer, TokenRenderer
from presentation.design_system import (
    MissionCard,
    get_tokens,
    primary_button,
)
from presentation.design_system.colours import SemanticColour
from presentation.design_system.components.base import StyleContract
from presentation.design_system.spacing import SpacingToken
from presentation.design_system.typography import TypeRole


def test_token_renderer_exposes_css_variables(token_renderer: TokenRenderer) -> None:
    props = token_renderer.css_variables()
    assert props["--primary"] == get_tokens().semantic_hex(SemanticColour.PRIMARY)
    assert "--space-lg" in props
    assert "--font-base" in props
    assert "--container-wide" in props
    assert props["--ds-disabled-opacity"] == str(get_tokens().disabled_opacity)


def test_root_stylesheet_contains_custom_properties(
    token_renderer: TokenRenderer,
) -> None:
    css = token_renderer.root_stylesheet()
    assert css.startswith(":root {")
    assert "--primary:" in css
    assert "--space-md:" in css
    assert "--radius-lg:" in css


def test_style_tag_includes_responsive_and_reduced_motion(
    token_renderer: TokenRenderer,
) -> None:
    tag = token_renderer.style_tag()
    assert tag.startswith("<style data-ds-tokens>")
    assert ".ds-container" in tag
    assert "@media" in tag
    assert "prefers-reduced-motion" in tag
    assert "grid-template-columns: repeat(4" in tag
    assert "grid-template-columns: repeat(12" in tag


def test_style_renderer_maps_contract_to_css_vars(
    style_renderer: StyleRenderer,
) -> None:
    style = StyleContract(
        background=SemanticColour.SURFACE,
        foreground=SemanticColour.TEXT,
        border=SemanticColour.BORDER_SUBTLE,
        typography=TypeRole.SUBHEADING,
        padding_x=SpacingToken.XL,
        padding_y=SpacingToken.XL,
        gap=SpacingToken.MD,
    )
    decls = style_renderer.declarations(style)
    assert decls["background-color"] == "var(--surface)"
    assert decls["color"] == "var(--text-primary)"
    assert decls["border-color"] == "var(--border-subtle)"
    assert decls["padding-inline"] == "var(--space-xl)"
    assert decls["gap"] == "var(--space-md)"
    assert "font-size" in decls
    assert decls["font-size"].startswith("var(")


def test_style_renderer_inline_style_for_button(
    style_renderer: StyleRenderer,
) -> None:
    button = primary_button("Go")
    inline = style_renderer.inline_style(button.style())
    assert "background-color: var(--primary)" in inline
    assert "color: var(--on-primary)" in inline


def test_style_renderer_honours_component_contract(
    style_renderer: StyleRenderer,
) -> None:
    card = MissionCard(title="Mission", body="Body")
    css = style_renderer.component_stylesheet("ds-mission-card", card.style())
    assert css.startswith(".ds-mission-card {")
    assert "var(--surface)" in css
