"""UX-005 — Theme consistency & accessibility foundation contracts."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "app" / "static" / "css"


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_session_chrome_exists_without_reviving_legacy_session_css():
    chrome = CSS / "session" / "session_chrome.css"
    legacy = CSS / "session" / "session.css"
    assert chrome.is_file()
    assert not legacy.exists()
    text = chrome.read_text(encoding="utf-8")
    assert ".session-topbar" in text
    assert ".session-btn-primary" in text
    assert "var(--on-primary)" in text
    assert "var(--chrome-text" in text


def test_assessment_and_qc_load_session_chrome():
    assessment = _read("app/templates/student/assessment/base.html")
    qc = _read("app/templates/adaptive_assessment/base.html")
    assert "session/session_chrome.css" in assessment
    assert "session/session_chrome.css" in qc
    assert "session/session.css" not in assessment
    assert "session/session.css" not in qc


def test_tokens_define_ux005_semantic_aliases():
    tokens = _read("app/static/css/tokens.css")
    for name in (
        "--surface-primary",
        "--surface-secondary",
        "--surface-overlay",
        "--accent-primary",
        "--border-primary",
        "--chrome-text",
        "--chrome-text-muted",
        "--color-text-primary",
        "--session-primary",
        "--session-text",
        "--link",
    ):
        assert name in tokens, f"missing {name}"
    dark = tokens[tokens.index('[data-theme="dark"]') :]
    assert "--chrome-text:" in dark
    assert "--surface-overlay:" in dark


def test_console_active_nav_avoids_static_midnight_text():
    css = _read("app/founder/dashboard/static/css/founder_dashboard.css")
    assert ".console-nav-link.is-active" in css
    active = css.split(".console-nav-link.is-active{", 1)[1].split("}", 1)[0]
    assert "--brand-midnight" not in active
    assert "var(--primary)" in active


def test_student_timeline_and_nav_avoid_static_navy_text():
    css = _read("app/static/css/student/student.css")
    assert (
        ".student-timeline-item.is-current .student-timeline-title {\n"
        "  color: var(--primary);\n}"
    ) in css
    assert "color: var(--link, var(--primary));" in css
    assert (
        "color: var(--brand-navy);"
        not in css.split(".educational-timeline-nav__list a {", 1)[1].split("}", 1)[0]
    )


def test_topbar_notes_use_chrome_text_tokens():
    assessment = _read("app/static/css/assessment/assessment.css")
    qc = _read("app/static/css/adaptive_assessment/quick_check.css")
    assert "var(--chrome-text-muted" in assessment
    assert "var(--chrome-text-muted" in qc
    assert "color-mix(in srgb, #fff" not in assessment
    assert "color-mix(in srgb, #fff" not in qc


def test_primary_buttons_use_on_primary_token():
    student = _read("app/static/css/student/student.css")
    founder = _read("app/founder/dashboard/static/css/founder_dashboard.css")
    primary_block = student.split(".student-btn-primary {", 1)[1].split("}", 1)[0]
    assert "var(--on-primary)" in primary_block
    assert "color:#fff" not in primary_block.replace(" ", "")
    console_primary = founder.split(".console-btn--primary{", 1)[1].split("}", 1)[0]
    assert "var(--on-primary)" in console_primary
    assert "color:#fff" not in console_primary.replace(" ", "")
