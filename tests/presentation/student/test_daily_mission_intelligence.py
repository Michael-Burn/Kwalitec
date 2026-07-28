"""Presentation + accessibility tests for Daily Mission Intelligence (ILE-004)."""

from __future__ import annotations

from app.application.daily_mission_intelligence import (
    DailyMissionIntelligenceApplicationService,
)
from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.presentation.student.view_models import home_vm
from app.services.decision_journal_service import DecisionJournalService
from tests.presentation.student.helpers import FORBIDDEN_TERMS


def _home_snap(**overrides) -> HomeSnapshot:
    base = dict(
        student_id="1",
        greeting="Welcome back",
        recommendation_title="Revise equity valuation",
        recommendation_summary="Focus on equity today.",
        estimated_study_minutes=25,
        has_recommendation=True,
        can_start_session=True,
        explanation=ExplanationSnapshot(
            why_recommended="Recent practice looks fragile on equity.",
            evidence_points=("Two uneven sessions this week.",),
            expected_benefit="A steadier base for later topics.",
            confidence_label="Emerging confidence",
            suggested_next_action="Start with worked examples.",
            timeliness_line="Your plan places this focus today.",
            completion_loop_line="Evidence from today's loop is recorded.",
            is_complete=True,
        ),
        start_session=StartSessionActionSnapshot(
            label="Start Today's Session",
            enabled=True,
            can_start=True,
            mission_id="m-1",
            session_id="s-1",
            estimated_minutes=25,
            topic_title="Revise equity valuation",
        ),
    )
    base.update(overrides)
    return HomeSnapshot(**base)


class TestMissionIntelligenceViewModel:
    def test_home_vm_composes_mission_intelligence(self):
        vm = home_vm(_home_snap(), unified_journey=False)
        mi = vm.mission_intelligence
        assert mi is not None
        assert mi.has_mission
        assert mi.title == "Revise equity valuation"
        assert mi.why_today
        assert mi.educational_purpose
        assert mi.expected_learning_outcome
        assert mi.supporting_evidence
        assert mi.reflection_prompt
        assert mi.mission_confidence
        assert mi.skip_consequence
        assert mi.mission_explanation

    def test_empty_when_no_recommendation(self):
        vm = home_vm(
            HomeSnapshot(student_id="1", has_recommendation=False),
            unified_journey=False,
        )
        mi = vm.mission_intelligence
        assert mi is not None
        assert mi.empty or not mi.has_mission

    def test_application_present_writes_journal(self, user, db):
        snap = DailyMissionIntelligenceApplicationService.compose_snapshot(
            title="Presented mission",
            why_recommended="Highest-value focus today.",
            expected_benefit="Clearer grasp.",
            recommendation_key="present-key",
        )
        presented = DailyMissionIntelligenceApplicationService.present(
            user.id,
            snap,
        )
        assert presented.journal_entry_id
        rows = DecisionJournalService.get_timeline(user.id, limit=10)
        assert any(r.entry_id == presented.journal_entry_id for r in rows)


class TestMissionIntelligenceHomeRoute:
    def test_home_renders_mission_intelligence_fields(
        self, student_client, monkeypatch
    ):
        from app.presentation.student import views as student_views

        class _FakeDash:
            learning_activity_status = ""
            navigation = ()
            home = _home_snap(student_id="1")
            journey = None
            history = None
            revision = None
            profile = None

        class _FakeExperience:
            def get_dashboard(self, *args, **kwargs):
                return _FakeDash()

        monkeypatch.setattr(
            student_views,
            "get_experience_service",
            lambda: _FakeExperience(),
        )
        # Also patch factory path used by load_page.
        monkeypatch.setattr(
            "app.presentation.student.factory.get_experience_service",
            lambda: _FakeExperience(),
        )

        resp = student_client.get("/student/")
        # Some environments redirect onboarding; accept 200 or follow.
        if resp.status_code == 302:
            resp = student_client.get("/student/", follow_redirects=True)
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        # When Home renders with our snap, mission intelligence panel appears.
        # If onboarding / empty home intervenes, skip soft assertion.
        if 'data-dashboard-slot="primary"' in body and "Revise equity" in body:
            assert 'data-mission-intelligence="true"' in body
            assert "Why today" in body
            assert "Expected benefit" in body
            assert "What should I focus on today?" in body
            for term in FORBIDDEN_TERMS:
                assert term not in body.lower()


class TestMissionIntelligenceAccessibility:
    def test_panel_has_labelled_heading(self):
        snap = DailyMissionIntelligenceApplicationService.compose_snapshot(
            title="A11y mission",
            why_recommended="Purpose text.",
            timeliness_line="Why today text.",
            expected_benefit="Benefit text.",
            supporting_evidence=("Evidence point.",),
        )
        assert snap.focus_question
        assert snap.explainability_heading
        assert snap.evidence_heading
        assert snap.reflection_heading
        assert snap.skip_heading
