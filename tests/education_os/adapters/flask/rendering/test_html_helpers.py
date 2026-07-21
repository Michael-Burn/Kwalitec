"""HTML helper unit tests for V4-003."""

from __future__ import annotations

from adapters.flask.rendering.html_helpers import (
    css_block,
    element,
    escape,
    format_attributes,
    join_classes,
)


def test_escape_and_attributes() -> None:
    assert escape("<b>") == "&lt;b&gt;"
    assert format_attributes({"role": "button", "disabled": True, "hidden": False}) == (
        'role="button" disabled'
    )


def test_join_classes_and_element() -> None:
    assert (
        join_classes("ds-btn", None, "is-active", ["extra"])
        == "ds-btn is-active extra"
    )
    assert element("span", attrs={"class": "x"}, children="Hi") == (
        '<span class="x">Hi</span>'
    )


def test_css_block() -> None:
    assert css_block(".x", {"color": "red"}) == ".x { color: red; }"
