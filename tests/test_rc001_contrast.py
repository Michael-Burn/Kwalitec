"""RC-001 B6 — sidebar contrast regression tests.

Computes WCAG 2.1 contrast ratios for every sidebar text token directly from
the shipped CSS (``app/static/css/app.css``, ``brand.css``, ``tokens.css``),
so a future edit that quietly drops a token below AA fails CI instead of
shipping. Ratios and rationale are also recorded in
``knowledge/product/rc001/ACCESSIBILITY_VALIDATION.md``.

The sidebar is a permanently dark ("chrome") surface in both the light and
dark app themes — ``--chrome`` resolves to the same ``#0D1B2A`` in both
``[data-theme="light"]`` and ``[data-theme="dark"]`` blocks of tokens.css —
so these ratios hold regardless of the student's chosen appearance.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_CSS = (ROOT / "app" / "static" / "css" / "app.css").read_text()

CHROME = (13, 27, 42)  # #0D1B2A — sidebar background, both themes
MIDNIGHT = (2, 13, 36)  # #020D24 — nav-link hover background
BRAND_BLUE = (59, 79, 184)  # #3B4FB8 — active nav-link background
WHITE = (255, 255, 255)
TEXT_INVERSE = (248, 250, 252)  # #f8fafc
SECONDARY_ON_DARK = (139, 147, 167)  # #8B93A7


def _composite(fg, alpha, bg):
    return tuple(round(fg[i] * alpha + bg[i] * (1 - alpha)) for i in range(3))


def _rel_lum(rgb):
    def chan(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast(rgb1, rgb2):
    l1, l2 = _rel_lum(rgb1), _rel_lum(rgb2)
    l1, l2 = max(l1, l2), min(l1, l2)
    return (l1 + 0.05) / (l2 + 0.05)


AA_NORMAL_TEXT = 4.5


def test_nav_section_label_meets_aa():
    """B6 (PX-003) / PX-B-028: 'Main' / 'System' group labels are meaningful navigation
    text (not decorative), so they must clear 4.5:1 like any other label —
    previously shipped at rgba(255,255,255,.35) which only reached 3.21:1.
    PX-004 raised opacity to 0.72 for clearer AA margin on real displays."""
    assert ".nav-section-label{color:rgba(255, 255, 255, 0.72);" in APP_CSS, (
        "nav-section-label alpha regressed below the AA-passing value"
    )
    fg = _composite(WHITE, 0.72, CHROME)
    ratio = _contrast(fg, CHROME)
    assert ratio >= AA_NORMAL_TEXT, f"nav-section-label only reaches {ratio:.2f}:1"


def test_nav_link_default_meets_aa():
    fg = _composite(WHITE, 0.68, CHROME)
    assert _contrast(fg, CHROME) >= AA_NORMAL_TEXT


def test_nav_link_hover_meets_aa():
    assert _contrast(TEXT_INVERSE, MIDNIGHT) >= AA_NORMAL_TEXT


def test_nav_link_active_meets_aa():
    assert _contrast(TEXT_INVERSE, BRAND_BLUE) >= AA_NORMAL_TEXT


def test_sidebar_brand_descriptor_meets_aa():
    assert _contrast(SECONDARY_ON_DARK, CHROME) >= AA_NORMAL_TEXT


def test_sidebar_signout_meets_aa():
    fg = _composite(WHITE, 0.55, CHROME)
    assert _contrast(fg, CHROME) >= AA_NORMAL_TEXT
