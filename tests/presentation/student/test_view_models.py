"""View model formatting tests — presentation only."""

from __future__ import annotations

import pytest

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.history_snapshot import (
    CompletedSessionSnapshot,
    HistorySnapshot,
    ReadinessPointSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.application.student_experience.dto.journey_snapshot import (
    JourneySnapshot,
    JourneyTopicSnapshot,
)
from app.application.student_experience.dto.profile_snapshot import (
    ProfileSnapshot,
    StudyPreferencesSnapshot,
)
from app.application.student_experience.dto.revision_snapshot import (
    RevisionOptionSnapshot,
    RevisionSnapshot,
)
from app.presentation.student.view_models import (
    contains_forbidden_term,
    format_benefit,
    format_minutes,
    format_readiness_percent,
    history_vm,
    home_vm,
    journey_card_vm,
    journey_vm,
    profile_vm,
    revision_vm,
    shell_vm,
)


@pytest.mark.parametrize(
    ("minutes", "expected"),
    [
        (None, ""),
        (0, "Less than a minute"),
        (1, "1 minute"),
        (25, "25 minutes"),
        (60, "1 hour"),
        (90, "1 hour 30 min"),
        (120, "2 hours"),
    ],
)
def test_format_minutes(minutes, expected):
    assert format_minutes(minutes) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, ""),
        (0.0, "0%"),
        (0.62, "62%"),
        (1.0, "100%"),
        (75.0, "75%"),
    ],
)
def test_format_readiness_percent(value, expected):
    assert format_readiness_percent(value) == expected


@pytest.mark.parametrize(
    ("delta", "fallback", "expected"),
    [
        (None, "", ""),
        (0.03, "", "About 3% readiness gain"),
        (None, "Custom benefit", "Custom benefit"),
        (3.0, "", "About 3% readiness gain"),
    ],
)
def test_format_benefit(delta, fallback, expected):
    assert format_benefit(delta, fallback=fallback) == expected


def test_home_vm_primary_cta():
    snap = HomeSnapshot(
        student_id="s1",
        greeting="Hello",
        recommendation_title="Revise equity",
        has_recommendation=True,
        can_start_session=True,
        estimated_study_minutes=25,
        expected_readiness_improvement=0.03,
        exam_readiness=0.62,
        exam_countdown_days=10,
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
    history = HistorySnapshot(
        student_id="s1",
        completed_sessions=(
            CompletedSessionSnapshot("s1", "Revision session", "2026-07-22", 30),
        ),
        readiness_progression=(
            ReadinessPointSnapshot("2026-06-01", 0.4),
            ReadinessPointSnapshot("2026-07-01", 0.6),
        ),
        session_count=1,
    )
    journey = JourneySnapshot(
        student_id="s1",
        current_topic=JourneyTopicSnapshot("t2", "Probability", "Current"),
        upcoming_topics=(JourneyTopicSnapshot("t3", "Checkpoint", "Upcoming"),),
        progress_percent=40,
        estimated_completion_label="8 weeks",
        completed_count=1,
        upcoming_count=1,
    )
    vm = home_vm(snap, journey=journey, history=history)
    assert vm.primary_cta_enabled is True
    assert vm.recommendation.has_recommendation is True
    assert vm.countdown.has_countdown is True
    assert vm.readiness.readiness_percent_label == "62%"
    assert "25" in vm.estimated_study_label
    assert "Revision session" in vm.journey_story
    assert "improving" in vm.readiness.trend_label.lower()
    assert "High educational return" in vm.coach_insight
    assert any(m.title == "Checkpoint" for m in vm.milestones)
    assert any(a.label == "Open Schedule" for a in vm.quick_actions)


def test_journey_vm_progress():
    snap = JourneySnapshot(
        student_id="s1",
        current_topic=JourneyTopicSnapshot("t2", "Current", "Current"),
        completed_topics=(JourneyTopicSnapshot("t1", "Done", "Completed"),),
        upcoming_topics=(JourneyTopicSnapshot("t3", "Next", "Upcoming"),),
        progress_percent=40,
        estimated_completion_label="8 weeks",
        completed_count=1,
        upcoming_count=1,
    )
    vm = journey_vm(snap)
    assert vm.progress_percent == 40
    assert vm.current is not None
    assert vm.upcoming[0].title == "Next"
    card = journey_card_vm(snap)
    assert card.next_topic_title == "Next"
    assert card.has_journey is True


def test_revision_vm_alternatives():
    snap = RevisionSnapshot(
        student_id="s1",
        primary=RevisionOptionSnapshot(
            option_id="r1",
            topic_title="Primary",
            priority_label="high",
            estimated_study_minutes=20,
            expected_benefit="Benefit",
            is_primary=True,
        ),
        alternatives=(
            RevisionOptionSnapshot(
                option_id="r2",
                topic_title="Alt",
                priority_label="medium",
                estimated_study_minutes=15,
            ),
        ),
        has_revision=True,
        option_count=2,
    )
    vm = revision_vm(snap)
    assert vm.primary_cta_enabled is True
    assert len(vm.alternatives) == 1


def test_history_vm_trend():
    snap = HistorySnapshot(
        student_id="s1",
        completed_sessions=(
            CompletedSessionSnapshot("s1", "Topic", "2026-07-01", 30),
        ),
        total_study_minutes=30,
        readiness_progression=(
            ReadinessPointSnapshot("2026-06-01", 0.4),
            ReadinessPointSnapshot("2026-07-01", 0.6),
        ),
        session_count=1,
    )
    vm = history_vm(snap)
    assert "improving" in vm.readiness_trend_label.lower()
    assert vm.sessions[0].duration_label == "30 minutes"


def test_profile_vm_days():
    snap = ProfileSnapshot(
        student_id="s1",
        display_name="Alex",
        examination_label="CPA",
        preferences=StudyPreferencesSnapshot(
            preferred_session_minutes=45,
            preferred_study_days=("Mon", "Wed"),
        ),
    )
    vm = profile_vm(snap)
    assert "Mon" in vm.preferences_days_label
    assert vm.display_name == "Alex"


def test_shell_vm_navigation():
    shell = shell_vm(active_surface="home", page_title="Home")
    assert shell.active_surface == "home"
    assert len(shell.navigation) == 5
    assert sum(1 for n in shell.navigation if n.active) == 1


@pytest.mark.parametrize(
    ("text", "forbidden"),
    [
        ("Digital Twin score", True),
        ("Adaptive Decision Engine", True),
        ("Learning Orchestrator", True),
        ("Today's Recommendation", False),
        ("Exam Readiness", False),
    ],
)
def test_forbidden_terms(text, forbidden):
    assert contains_forbidden_term(text) is forbidden
