"""Static assets, templates, and documentation presence for Internal Alpha."""

from __future__ import annotations

from tests.operational.helpers import (
    REPO_ROOT,
    REQUIRED_STATIC_FILES,
    REQUIRED_TEMPLATES,
)


def test_required_static_files_exist():
    missing = [p for p in REQUIRED_STATIC_FILES if not (REPO_ROOT / p).is_file()]
    assert missing == []


def test_required_templates_exist():
    missing = [p for p in REQUIRED_TEMPLATES if not (REPO_ROOT / p).is_file()]
    assert missing == []


def test_session_and_founder_css_nonempty():
    for rel in REQUIRED_STATIC_FILES:
        path = REPO_ROOT / rel
        if path.suffix.lower() in {".woff", ".woff2", ".ttf", ".otf"}:
            assert path.stat().st_size > 1000, rel
            continue
        css = path.read_text(encoding="utf-8")
        assert len(css.strip()) > 50, rel


def test_templates_reference_css():
    session_base = (REPO_ROOT / "app/templates/session/base.html").read_text(
        encoding="utf-8"
    )
    assert "fonts.css" in session_base
    assert "tokens.css" in session_base
    assert "session.css" in session_base
    assert "@fontsource/inter" not in session_base
    student_base = (REPO_ROOT / "app/templates/student/base.html").read_text(
        encoding="utf-8"
    )
    assert "fonts.css" in student_base
    assert "@fontsource/inter" not in student_base
    layout_base = (REPO_ROOT / "app/templates/layouts/base.html").read_text(
        encoding="utf-8"
    )
    assert "fonts.css" in layout_base
    assert "tokens.css" in layout_base
    assert "@fontsource/inter" not in layout_base
    for name in ("dashboard.html", "workspace.html"):
        html = (
            REPO_ROOT / "app/templates/curriculum_studio" / name
        ).read_text(encoding="utf-8")
        assert "founder_dashboard.css" in html


def test_shared_tokens_define_ux001_scale():
    tokens = (REPO_ROOT / "app/static/css/tokens.css").read_text(encoding="utf-8")
    assert "--font-4xl: 2.5rem" in tokens
    assert "--font-base: 1rem" in tokens
    assert "--radius-lg: 1rem" in tokens
    assert "--radius-md: 0.75rem" in tokens
    assert ".skeleton" in tokens
    assert "kw-skeleton-pulse" in tokens
    brand = (REPO_ROOT / "app/static/css/brand.css").read_text(encoding="utf-8")
    assert "--status-warning: #A16207" in brand
    assert "--chart-gold" not in brand


def test_self_hosted_inter_fonts():
    fonts_css = (REPO_ROOT / "app/static/css/fonts.css").read_text(encoding="utf-8")
    assert 'font-family: "Inter"' in fonts_css
    assert "font-display: swap" in fonts_css
    assert "../fonts/inter/inter-latin-400-normal.woff2" in fonts_css
    for weight in (400, 500, 600, 700):
        path = (
            REPO_ROOT
            / f"app/static/fonts/inter/inter-latin-{weight}-normal.woff2"
        )
        assert path.is_file()
        assert path.stat().st_size > 1000


def test_svg_icons_use_ux001_sizes():
    """SVG element width/height must be 20, 24, or 32 (UX-001)."""
    import re

    forbidden = re.compile(
        r"<svg\b[^>]*\b(?:width|height)=\"(14|16|18|22|48)\"",
        re.IGNORECASE,
    )
    offenders: list[str] = []
    for path in (REPO_ROOT / "app").rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        for match in forbidden.finditer(text):
            offenders.append(f"{path.relative_to(REPO_ROOT)}:{match.group(0)[:80]}")
    assert offenders == [], "Off-spec SVG icon sizes:\n" + "\n".join(offenders)


def test_wsgi_and_render_start_command():
    assert (REPO_ROOT / "wsgi.py").is_file()
    text = (REPO_ROOT / "render.yaml").read_text(encoding="utf-8")
    assert "waitress-serve" in text
    assert "wsgi:app" in text


def test_alpha_ops_docs_present():
    docs = (
        "knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md",
        "knowledge/version2/ALPHA_WORKFLOW_VALIDATION.md",
        "knowledge/version2/ALPHA_READINESS_FOUNDER_UX.md",
        "knowledge/version2/V2_020_RETIREMENT_RUNBOOK.md",
        "knowledge/releases/V2_DEPLOY_IMPLEMENTATION_REPORT.md",
    )
    missing = [d for d in docs if not (REPO_ROOT / d).is_file()]
    assert missing == []


def test_core_v2_modules_present():
    assert (REPO_ROOT / "app/models/v2_aggregate.py").is_file()
    assert (REPO_ROOT / "app/application/config/v2_flags.py").is_file()
