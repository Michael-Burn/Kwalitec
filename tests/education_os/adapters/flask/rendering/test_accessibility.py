"""Accessibility rendering tests for V4-003."""

from __future__ import annotations

from adapters.flask.rendering import AccessibilityRenderer, ComponentRenderer
from presentation.design_system import (
    ProgressBar,
    primary_button,
    secondary_button,
)
from presentation.design_system.colours import SemanticColour, colour
from presentation.design_system.components.base import AccessibilityContract


def test_accessibility_attributes_for_button(
    accessibility_renderer: AccessibilityRenderer,
) -> None:
    button = primary_button("Continue")
    attrs = accessibility_renderer.attributes(
        button.accessibility(),
        label=button.label,
    )
    assert attrs["role"] == "button"
    assert attrs["aria-label"] == "Continue"
    assert attrs["tabindex"] == "0"
    assert attrs["data-reduced-motion"] == "safe"


def test_disabled_button_removes_focus(
    accessibility_renderer: AccessibilityRenderer,
) -> None:
    button = secondary_button("Unavailable", disabled=True)
    attrs = accessibility_renderer.attributes(
        button.accessibility(),
        label=button.label,
        disabled=True,
    )
    assert attrs["aria-disabled"] == "true"
    assert attrs["tabindex"] == "-1"


def test_progressbar_attributes(
    accessibility_renderer: AccessibilityRenderer,
) -> None:
    bar = ProgressBar(label="Coverage", percent=70, value_text="70%")
    attrs = accessibility_renderer.attributes(
        bar.accessibility(),
        label=bar.label,
        valuenow=bar.percent,
        valuetext=bar.value_text,
    )
    assert attrs["role"] == "progressbar"
    assert attrs["aria-valuemin"] == "0"
    assert attrs["aria-valuemax"] == "100"
    assert attrs["aria-valuenow"] == "70"
    assert attrs["aria-valuetext"] == "70%"


def test_contrast_compliance_for_primary_button(
    accessibility_renderer: AccessibilityRenderer,
) -> None:
    button = primary_button("Go")
    assert accessibility_renderer.contrast_is_compliant(button.accessibility())


def test_focus_ring_token(accessibility_renderer: AccessibilityRenderer) -> None:
    assert accessibility_renderer.focus_ring_token() == "--focus-ring"
    assert colour(SemanticColour.FOCUS_RING).css_var == "--focus-ring"


def test_rendered_components_include_aria(
    component_renderer: ComponentRenderer,
) -> None:
    html = component_renderer.render_primary_button(primary_button("Start"))
    assert 'aria-label="Start"' in html
    assert 'role="button"' in html
    assert 'tabindex="0"' in html


def test_html_attributes_serialisation(
    accessibility_renderer: AccessibilityRenderer,
) -> None:
    contract = AccessibilityContract(
        role="status",
        label_required=True,
        keyboard_focusable=False,
    )
    rendered = accessibility_renderer.html_attributes(contract, label="Saved")
    assert 'role="status"' in rendered
    assert 'aria-label="Saved"' in rendered
