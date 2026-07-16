"""RR-001C Student Terminology regression tests.

Founder observation (FC-001): Mission / Study Session wording was still mixed
on student-facing surfaces.

Canonical student object is "Study Session". The engineering name "Mission"
may remain internally (route names, CSS classes, ORM attributes, comments),
but must never appear as student-visible prose.

These tests guard the specific student-visible strings corrected in RR-001C so
the mixed wording cannot silently return. They read source files directly to
stay fast and deterministic (no DB / HTTP client required).
"""

from __future__ import annotations

from pathlib import Path

_APP = Path(__file__).resolve().parents[1] / "app"


def _read(relative: str) -> str:
    return (_APP / relative).read_text(encoding="utf-8")


class TestStudentVisibleTerminology:
    def test_wizard_step6_helper_uses_study_sessions(self):
        body = _read("templates/study_plan/wizard_step_6.html")
        assert "daily study sessions" in body
        assert "daily missions" not in body

    def test_analytics_empty_trend_uses_study_session(self):
        body = _read("templates/analytics/index.html")
        assert "Complete your first study session to see trends." in body
        assert "Complete your first mission to see trends." not in body

    def test_settings_export_description_uses_study_sessions(self):
        body = _read("templates/settings/index.html")
        assert "study plans, study sessions, study attempts" in body
        assert "study plans, missions, study attempts" not in body

    def test_mission_route_flash_uses_study_sessions(self):
        source = _read("mission/routes.py")
        assert "You can only review your own study sessions." in source
        assert "You can only review your own missions." not in source
