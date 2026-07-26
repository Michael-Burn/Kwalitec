"""Home rendering tests — Experience Feedback Loop (P2-MS008)."""

from __future__ import annotations

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.infrastructure.adapters.experience_feedback import (
    DEFAULT_SOURCE_DESCRIPTION,
    ExperienceFeedback,
    ExperienceFeedbackFact,
)
from app.presentation.student.view_models import home_vm


def _snap(**overrides) -> HomeSnapshot:
    base = dict(
        student_id="s1",
        greeting="Hello",
        recommendation_title="Revise equity",
        recommendation_summary="Focus on equity today",
        has_recommendation=True,
        can_start_session=True,
        estimated_study_minutes=25,
        expected_readiness_improvement=0.03,
        start_session=StartSessionActionSnapshot(
            label="Start Today's Session",
            enabled=True,
            can_start=True,
            mission_id="m1",
        ),
        explanation=ExplanationSnapshot(
            why_recommended="High educational return",
            expected_benefit="Strengthen readiness",
            confidence_label="Strong",
            is_complete=True,
        ),
    )
    base.update(overrides)
    return HomeSnapshot(**base)


def _feedback() -> ExperienceFeedback:
    source = DEFAULT_SOURCE_DESCRIPTION
    return ExperienceFeedback(
        feedback_id="expfb-home",
        reporting_period="this_week",
        completed_missions=2,
        completed_reflections=1,
        study_sessions=2,
        active_streak=3,
        generated_at="2026-07-25T12:00:00+00:00",
        facts=(
            ExperienceFeedbackFact(
                key="completed_missions",
                label="Missions completed this week",
                value=2,
                value_label="2 missions",
                source_description=source,
            ),
            ExperienceFeedbackFact(
                key="study_sessions",
                label="Study sessions completed",
                value=2,
                value_label="2 sessions",
                source_description=source,
            ),
            ExperienceFeedbackFact(
                key="completed_reflections",
                label="Reflection consistency",
                value=1,
                value_label="1 reflection",
                source_description=source,
            ),
            ExperienceFeedbackFact(
                key="active_streak",
                label="Current study streak",
                value=3,
                value_label="3 days",
                source_description=source,
            ),
        ),
        student_id="s1",
        evidence_summary_id="evfact-home",
        source_description=source,
    )


def test_home_shows_experience_feedback_when_unified_and_feedback_present():
    vm = home_vm(
        _snap(),
        unified_journey=True,
        experience_feedback=_feedback(),
    )
    assert vm.unified_journey_enabled is True
    assert vm.experience_feedback_enabled is True
    assert vm.experience_feedback_period_label == "This week"
    assert vm.experience_feedback_source == DEFAULT_SOURCE_DESCRIPTION
    assert len(vm.experience_feedback_facts) == 4
    assert vm.experience_feedback_facts[0].label == "Missions completed this week"
    assert all(
        fact.source_description == DEFAULT_SOURCE_DESCRIPTION
        for fact in vm.experience_feedback_facts
    )


def test_home_hides_feedback_when_unified_journey_off():
    vm = home_vm(
        _snap(),
        unified_journey=False,
        experience_feedback=_feedback(),
    )
    assert vm.experience_feedback_enabled is False
    assert vm.experience_feedback_facts == ()


def test_home_hides_feedback_when_none():
    vm = home_vm(_snap(), unified_journey=True, experience_feedback=None)
    assert vm.experience_feedback_enabled is False
    assert vm.experience_feedback_facts == ()


def test_home_feedback_does_not_change_mission_recommendation():
    """Feedback is display-only — mission/recommendation projections unchanged."""
    without = home_vm(_snap(), unified_journey=True, experience_feedback=None)
    with_fb = home_vm(
        _snap(),
        unified_journey=True,
        experience_feedback=_feedback(),
    )
    assert with_fb.primary_mission_title == without.primary_mission_title
    assert with_fb.why_it_matters == without.why_it_matters
    assert with_fb.recommendation.title == without.recommendation.title
    assert with_fb.recommendation.summary == without.recommendation.summary
    assert with_fb.primary_cta_enabled == without.primary_cta_enabled
    assert with_fb.mission_priority == without.mission_priority
