"""KWP-002 — Student Value Activation tests.

Commercial Loop Profile, Home/Session/Journey language, and learner-facing
scrub. Presentation packaging only — no SR-001A authority redesign.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.presentation.product_language import REJECTED_SYNONYMS
from app.presentation.session.messages import FLASH_SUCCESS, FLASH_WARNING
from tests.presentation.student.helpers import STUDENT_ROUTES, wire_experience
from tests.presentation.workflows.helpers import login_student, wire_session

STUDENT_TEMPLATES = Path("app/templates/student")
SESSION_TEMPLATES = Path("app/templates/session")

_LEARNER_FORBIDDEN = (
    "mission engine",
    "learning twin",
    "digital twin",
    "student twin",
    "building evidence",
    "educational evidence",
    "practice evidence",
    "overall mastery",
    "curriculum nodes",
    " nodes · ",
    "technical details",
)


@pytest.fixture
def student_client(app, client, ctx, user):
    wire_experience(app)
    wire_session(app)
    login_student(client)
    return client


# --- Commercial Loop Profile -------------------------------------------------


class TestCommercialLoopProfile:
    def test_commercial_loop_defaults_off(self):
        flags = resolve_v2_feature_flags(environ={})
        assert flags.SR_COMMERCIAL_LOOP is False
        assert flags.SR_SESSION_PRIMARY is False
        assert flags.SR_SESSION_SUBSTANCE is False
        assert flags.SR_SESSION_COMPLETION_PRODUCT is False
        assert flags.SR_EVIDENCE_GATE is False
        assert flags.SR_TWIN_DAILY_LOOP is False
        assert flags.SR_PROGRESS_SINGULARITY is False
        assert flags.SR_PILOT_MARK_COMPLETE is False

    def test_sole_runtime_inherits_commercial_loop_when_unset(self):
        """G1 production: sole runtime enables Start Session spine by default."""
        flags = resolve_v2_feature_flags(
            environ={"KWALITEC_V2_SOLE_RUNTIME": "1"}
        )
        assert flags.SOLE_RUNTIME is True
        assert flags.SR_COMMERCIAL_LOOP is True
        assert flags.SR_SESSION_PRIMARY is True
        assert flags.SR_SESSION_SUBSTANCE is True
        assert flags.SR_SESSION_COMPLETION_PRODUCT is True
        assert flags.SR_PILOT_MARK_COMPLETE is False

    def test_explicit_commercial_loop_off_wins_over_sole_runtime(self):
        flags = resolve_v2_feature_flags(
            environ={
                "KWALITEC_V2_SOLE_RUNTIME": "1",
                "KWALITEC_COMMERCIAL_LOOP": "0",
            }
        )
        assert flags.SOLE_RUNTIME is True
        assert flags.SR_COMMERCIAL_LOOP is False
        assert flags.SR_SESSION_PRIMARY is False

    def test_commercial_loop_enables_bundle(self):
        flags = resolve_v2_feature_flags(
            environ={"KWALITEC_COMMERCIAL_LOOP": "1"}
        )
        assert flags.SR_COMMERCIAL_LOOP is True
        assert flags.SR_SESSION_PRIMARY is True
        assert flags.SR_SESSION_SUBSTANCE is True
        assert flags.SR_SESSION_COMPLETION_PRODUCT is True
        assert flags.SR_EVIDENCE_GATE is True
        assert flags.SR_TWIN_DAILY_LOOP is True
        assert flags.SR_PROGRESS_SINGULARITY is True
        assert flags.SR_PILOT_MARK_COMPLETE is False

    def test_commercial_loop_alias(self):
        flags = resolve_v2_feature_flags(environ={"SR_COMMERCIAL_LOOP": "true"})
        assert flags.SR_COMMERCIAL_LOOP is True
        assert flags.SR_SESSION_PRIMARY is True

    def test_explicit_off_overrides_commercial_loop(self):
        flags = resolve_v2_feature_flags(
            environ={
                "KWALITEC_COMMERCIAL_LOOP": "1",
                "SR_SESSION_PRIMARY": "0",
                "SR_EVIDENCE_GATE": "false",
            }
        )
        assert flags.SR_COMMERCIAL_LOOP is True
        assert flags.SR_SESSION_PRIMARY is False
        assert flags.SR_EVIDENCE_GATE is False
        assert flags.SR_SESSION_SUBSTANCE is True

    def test_render_yaml_enables_commercial_loop(self):
        from tests.operational.helpers import render_env_map

        env = render_env_map()
        assert env.get("KWALITEC_COMMERCIAL_LOOP") == "1"


# --- Language Guide ----------------------------------------------------------


class TestLanguageGuideCompliance:
    def test_rejected_synonyms_include_kwp002_terms(self):
        for term in (
            "learning twin",
            "building evidence",
            "educational evidence",
            "practice evidence",
            "overall mastery",
            "mark mission complete",
        ):
            assert term in REJECTED_SYNONYMS

    def test_evidence_gate_flash_uses_outcome_language(self):
        msg = FLASH_WARNING["evidence_rejected"].lower()
        assert "educational evidence" not in msg
        assert "practice" in msg or "counting this topic" in msg

    def test_completion_flash_mentions_journey(self):
        msg = FLASH_SUCCESS["completed"].lower()
        assert "journey" in msg or "home" in msg

    @pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
    def test_student_routes_hide_kwp002_forbidden_terms(
        self, student_client, endpoint, path
    ):
        html = student_client.get(path).get_data(as_text=True).lower()
        for term in _LEARNER_FORBIDDEN:
            assert term not in html, f"{term!r} found on {path}"

    def test_student_templates_avoid_forbidden_phrases(self):
        for path in STUDENT_TEMPLATES.rglob("*.html"):
            text = path.read_text(encoding="utf-8").lower()
            for term in (
                "mission engine",
                "learning twin",
                "digital twin",
                "building evidence",
                "practice evidence",
                "overall mastery",
                " nodes · ",
                "curriculum nodes",
            ):
                assert term not in text, f"{term!r} in {path}"

    def test_session_templates_hide_technical_details(self):
        body = (SESSION_TEMPLATES / "partials" / "session_body.html").read_text(
            encoding="utf-8"
        ).lower()
        assert "technical details" not in body
        assert "session id" not in body


# --- Home / Journey / Session surfaces ---------------------------------------


class TestHomeActivation:
    def test_home_uses_todays_session_lexicon(self, student_client):
        html = student_client.get("/student/").get_data(as_text=True)
        assert (
            "Today's Mission" in html
            or "Today&#39;s Mission" in html
            or "ds-mission-hero" in html
            or "ds-empty-operational" in html
        )
        assert "Building evidence" not in html
        assert "Mark mission complete" not in html

    def test_home_keeps_decision_surface_not_session_detail(self):
        home = (STUDENT_TEMPLATES / "home.html").read_text(encoding="utf-8")
        assert "ds_mission_hero" in home or "ds-mission-hero" in home
        assert "explanation_card" not in home
        assert "readiness_card" not in home
        assert "Why this Session?" not in home


class TestJourneyActivation:
    def test_journey_shows_syllabus_progress(self, student_client):
        html = student_client.get("/student/journey").get_data(as_text=True)
        assert "Syllabus Progress" in html or "syllabus" in html.lower()
        assert "Overall mastery" not in html

    def test_journey_surfaces_insights_and_up_next(self):
        journey = (STUDENT_TEMPLATES / "journey.html").read_text(encoding="utf-8")
        assert "Learning Insights" in journey
        assert "Up Next" in journey
        assert "Needs Attention" in journey
        assert "Remaining Topics" in journey
        assert "Overall mastery" not in journey


class TestSessionActivation:
    def test_session_body_has_completion_moment_hooks(self):
        body = (SESSION_TEMPLATES / "partials" / "session_body.html").read_text(
            encoding="utf-8"
        )
        assert "data-completion-moment" in body
        assert "data-journey-update" in body
        assert "Learning Insights" in body
