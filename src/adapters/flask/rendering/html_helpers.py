"""HTML construction helpers for the Design System renderer.

Framework-light utilities for escaping, attributes, and element assembly.
No educational logic, persistence, or AI.
"""

from __future__ import annotations

from collections.abc import Mapping
from html import escape as _html_escape
from typing import Any


def escape(value: Any) -> str:
    """Escape a value for safe HTML text content."""
    if value is None:
        return ""
    return _html_escape(str(value), quote=True)


def escape_attr(value: Any) -> str:
    """Escape a value for use inside an HTML attribute."""
    if value is None:
        return ""
    return _html_escape(str(value), quote=True)


def join_classes(*parts: Any) -> str:
    """Join non-empty CSS class fragments with a single space."""
    tokens: list[str] = []
    for part in parts:
        if part is None:
            continue
        if isinstance(part, list | tuple):
            tokens.extend(str(item).strip() for item in part if item)
        else:
            text = str(part).strip()
            if text:
                tokens.append(text)
    return " ".join(tokens)


def format_attributes(attrs: Mapping[str, Any] | None) -> str:
    """Serialise an attribute mapping into an HTML attribute string.

    Boolean ``True`` emits a bare attribute name. ``False`` / ``None`` omit
    the attribute. All other values are escaped.
    """
    if not attrs:
        return ""
    chunks: list[str] = []
    for key, value in attrs.items():
        if value is None or value is False:
            continue
        name = str(key).strip()
        if not name:
            continue
        if value is True:
            chunks.append(name)
            continue
        chunks.append(f'{name}="{escape_attr(value)}"')
    return " ".join(chunks)


def open_tag(name: str, attrs: Mapping[str, Any] | None = None) -> str:
    """Build an opening HTML tag."""
    rendered = format_attributes(attrs)
    if rendered:
        return f"<{name} {rendered}>"
    return f"<{name}>"


def close_tag(name: str) -> str:
    """Build a closing HTML tag."""
    return f"</{name}>"


def void_tag(name: str, attrs: Mapping[str, Any] | None = None) -> str:
    """Build a void / self-closing HTML element."""
    rendered = format_attributes(attrs)
    if rendered:
        return f"<{name} {rendered}>"
    return f"<{name}>"


def element(
    name: str,
    *,
    attrs: Mapping[str, Any] | None = None,
    children: Any = "",
    void: bool = False,
) -> str:
    """Assemble a complete HTML element."""
    if void:
        return void_tag(name, attrs)
    inner = "" if children is None else str(children)
    return f"{open_tag(name, attrs)}{inner}{close_tag(name)}"


def css_block(selector: str, declarations: Mapping[str, str]) -> str:
    """Format a CSS rule block from a selector and declaration map."""
    if not declarations:
        return f"{selector} {{}}"
    body = "; ".join(f"{prop}: {value}" for prop, value in declarations.items())
    return f"{selector} {{ {body}; }}"
