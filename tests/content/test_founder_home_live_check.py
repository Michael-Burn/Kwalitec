"""Regression tests for the founder Home live-rendering check.

The Wave 1 founder walk false-alarmed because it matched the literal
label ``Start Session`` and sampled the first 80 characters of page text
(navigation chrome, including Choose Exam). These tests lock the
corrected predicates.
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import founder_home_live_check as live_check  # noqa: E402

# Realistic Home: nav chrome first, then a startable mission whose CTA
# label is the current product copy, not the short "Start Session" string.
STARTABLE_HOME_HTML = """
<nav class="student-nav" data-student-nav>
  <ul class="student-nav-list">
    <li><a class="student-nav-link">Home</a></li>
    <li><a class="student-nav-link">Study</a></li>
    <li><a class="student-nav-link">Syllabus</a></li>
    <li><a class="student-nav-link">Revision</a></li>
    <li><a class="student-nav-link">History</a></li>
    <li><a class="student-nav-link">Stats</a></li>
    <li><a class="student-nav-link">Settings</a></li>
    <li><a class="student-nav-link">Choose Exam</a></li>
    <li><a class="student-nav-link">Help</a></li>
  </ul>
</nav>
<article data-home="decision-surface">
  <header>
    <h1>Good morning.</h1>
    <p>Ready for today's mission?</p>
  </header>
  <div data-workspace-section="todays-mission" class="ds-os-home__mission">
    <h2>Today's Mission</h2>
    <p>Name why actuarial data analysis exists</p>
  </div>
  <button
    type="submit"
    data-student-cta="primary"
    data-session-control="start"
    data-workspace-action="begin-session"
  >Start Today's Session<span aria-hidden="true">→</span></button>
</article>
"""

EMPTY_HOME_HTML = """
<nav class="student-nav">
  <a class="student-nav-link">Choose Exam</a>
</nav>
<article data-home="decision-surface">
  <section data-student-state="empty" data-sop-section="todays-session">
    <h2>Choose an exam</h2>
    <a data-student-cta="primary">Choose Exam</a>
  </section>
</article>
"""

RESUME_HOME_HTML = """
<article data-home="decision-surface">
  <div data-workspace-section="todays-mission" class="ds-os-home__mission">
    <h2>Today's Mission</h2>
  </div>
  <a data-student-cta="primary" data-session-control="resume">Continue</a>
</article>
"""


def _visible_text(html: str) -> str:
    stripped: list[str] = []
    in_tag = False
    for char in html:
        if char == "<":
            in_tag = True
            stripped.append(" ")
            continue
        if char == ">":
            in_tag = False
            continue
        if not in_tag:
            stripped.append(char)
    return " ".join("".join(stripped).split())


def test_startable_home_is_not_confused_with_nav_choose_exam() -> None:
    visible = _visible_text(STARTABLE_HOME_HTML)
    assert visible.startswith("Home Study")
    assert "Choose Exam" in visible[:80]
    assert "Start Session" not in visible
    assert "Start Today's Session" in visible

    result = live_check.evaluate_home_html(STARTABLE_HOME_HTML)
    assert result["startable"] is True
    assert result["can_enter_session"] is True
    assert result["status"] == "startable"
    assert result["session_control"] == "start"
    assert result["empty_state"] is False
    assert result["has_mission_hero"] is True
    assert result["has_home_surface"] is True
    assert any("Start Today's Session" in label for label in result["primary_labels"])


def test_empty_home_is_reported_as_not_startable() -> None:
    result = live_check.evaluate_home_html(EMPTY_HOME_HTML)
    assert result["startable"] is False
    assert result["can_enter_session"] is False
    assert result["status"] == "empty"
    assert result["empty_state"] is True
    assert result["session_control"] is None


def test_resume_home_is_enterable_without_start_control() -> None:
    result = live_check.evaluate_home_html(RESUME_HOME_HTML)
    assert result["startable"] is False
    assert result["can_enter_session"] is True
    assert result["status"] == "resumable"
    assert result["session_control"] == "resume"


def test_live_page_evaluator_does_not_use_legacy_false_alarm_predicates() -> None:
    import inspect

    source = inspect.getsource(live_check.evaluate_home_page)
    assert "Start Session" not in source
    assert "[:80]" not in source
    assert "STARTABLE_SELECTOR" in source
    assert "MISSION_HERO_SELECTOR" in source
    assert "EMPTY_STATE_SELECTOR" in source


class _FakeLocator:
    def __init__(self, nodes: list[SimpleNamespace]) -> None:
        self._nodes = nodes

    def count(self) -> int:
        return len(self._nodes)

    @property
    def first(self) -> SimpleNamespace:
        return self._nodes[0]

    def nth(self, index: int) -> SimpleNamespace:
        return self._nodes[index]


def test_evaluate_home_page_uses_data_attributes_not_body_prefix() -> None:
    hero = SimpleNamespace(
        inner_text=lambda: "Today's Mission\nName why actuarial data analysis exists"
    )
    primary = SimpleNamespace(inner_text=lambda: "Start Today's Session")
    page = SimpleNamespace(
        url="http://127.0.0.1:5001/student/",
        locator=lambda selector: {
            live_check.STARTABLE_SELECTOR: _FakeLocator([SimpleNamespace()]),
            live_check.RESUMABLE_SELECTOR: _FakeLocator([]),
            live_check.EMPTY_STATE_SELECTOR: _FakeLocator([]),
            live_check.MISSION_HERO_SELECTOR: _FakeLocator([hero]),
            live_check.HOME_SURFACE_SELECTOR: _FakeLocator([SimpleNamespace()]),
            live_check.PRIMARY_CTA_SELECTOR: _FakeLocator([primary]),
        }[selector],
    )
    result = live_check.evaluate_home_page(page)
    assert result["startable"] is True
    assert result["session_control"] == "start"
    assert "Today's Mission" in result["mission_hero_text"]
    assert result["url"].endswith("/student/")


def test_legacy_copy_match_would_miss_current_cta() -> None:
    """Document the Wave 1 false alarm: exact 'Start Session' misses Home."""
    html = STARTABLE_HOME_HTML
    assert "Start Today's Session" in html
    assert ">Start Session<" not in html
    assert html.count("data-session-control=\"start\"") == 1
    # The corrected evaluator still reports startable.
    assert live_check.evaluate_home_html(html)["startable"] is True
