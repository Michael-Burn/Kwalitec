"""Contrast helpers for accessible colour pairings (WCAG relative luminance)."""

from __future__ import annotations

import re

_HEX_RE = re.compile(r"^#([0-9A-Fa-f]{6})$")


def parse_hex(colour: str) -> tuple[int, int, int] | None:
    """Parse ``#RRGGBB`` into RGB; return None for non-solid colours."""
    match = _HEX_RE.match(colour.strip())
    if not match:
        return None
    raw = match.group(1)
    return int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16)


def _channel(value: int) -> float:
    s = value / 255.0
    if s <= 0.03928:
        return s / 12.92
    return ((s + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_colour: str) -> float | None:
    """WCAG relative luminance for a solid hex colour."""
    rgb = parse_hex(hex_colour)
    if rgb is None:
        return None
    r, g, b = rgb
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast_ratio(foreground: str, background: str) -> float | None:
    """Contrast ratio between two solid hex colours, or None if unparsable."""
    lf = relative_luminance(foreground)
    lb = relative_luminance(background)
    if lf is None or lb is None:
        return None
    lighter = max(lf, lb)
    darker = min(lf, lb)
    return (lighter + 0.05) / (darker + 0.05)


def meets_contrast(
    foreground: str,
    background: str,
    *,
    minimum: float = 4.5,
) -> bool:
    """Return True when the pair meets the minimum contrast ratio."""
    ratio = contrast_ratio(foreground, background)
    if ratio is None:
        return False
    return ratio >= minimum
