"""Tests for Learning Session Runtime policies."""

from __future__ import annotations

from app.application.learning_session.policies.completion_policy import (
    CompletionPolicy,
)
from app.application.learning_session.policies.planning_policy import PlanningPolicy
from app.application.learning_session.policies.reflection_policy import (
    ReflectionPolicy,
)
from app.application.learning_session.policies.scheduling_policy import (
    NextAction,
    SchedulingPolicy,
)
from app.application.learning_session.runtime_phase import RuntimePhase
from app.domain.learning_journey.entities.journey_reflection import (
    JourneyReflection,
    ReflectionPosture,
)
from app.domain.learning_journey.entities.learning_objective import ObjectiveKind
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.session_state import SessionState
from tests.application.learning_session.helpers import (
    make_evidence,
    make_objective,
    make_session,
)


class TestPlanningPolicy:
    def test_default_activities_without_objectives(self):
        activities = PlanningPolicy.activities_for([])
        assert "focused_study" in activities

    def test_activities_for_understand(self):
        acts = PlanningPolicy.activities_for(
            [make_objective(kind=ObjectiveKind.UNDERSTAND)]
        )
        assert "read_core_notes" in acts

    def test_activities_for_apply(self):
        acts = PlanningPolicy.activities_for(
            [make_objective(kind=ObjectiveKind.APPLY)]
        )
        assert "worked_example" in acts

    def test_activities_for_analyse(self):
        acts = PlanningPolicy.activities_for(
            [make_objective(kind=ObjectiveKind.ANALYSE)]
        )
        assert "diagnose_errors" in acts

    def test_activities_for_review(self):
        acts = PlanningPolicy.activities_for(
            [make_objective(kind=ObjectiveKind.REVIEW)]
        )
        assert "spaced_review" in acts

    def test_activities_for_revise(self):
        acts = PlanningPolicy.activities_for(
            [make_objective(kind=ObjectiveKind.REVISE)]
        )
        assert "targeted_revision" in acts

    def test_activities_dedupe_across_objectives(self):
        acts = PlanningPolicy.activities_for(
            [
                make_objective("o1", kind=ObjectiveKind.UNDERSTAND),
                make_objective("o2", kind=ObjectiveKind.UNDERSTAND, sequence_index=1),
            ]
        )
        assert len(acts) == len(set(acts))

    def test_explicit_effort_override(self):
        effort = PlanningPolicy.estimate_effort(
            [make_objective()],
            explicit=EffortEstimate.EXTENSIVE,
        )
        assert effort == EffortEstimate.EXTENSIVE

    def test_default_effort_medium_without_objectives(self):
        assert PlanningPolicy.estimate_effort([]) == EffortEstimate.MEDIUM

    def test_revise_effort_is_high(self):
        effort = PlanningPolicy.estimate_effort(
            [make_objective(kind=ObjectiveKind.REVISE)]
        )
        assert effort == EffortEstimate.HIGH

    def test_review_effort_low(self):
        effort = PlanningPolicy.estimate_effort(
            [make_objective(kind=ObjectiveKind.REVIEW)],
            previous_evidence_count=2,
        )
        assert effort == EffortEstimate.LOW

    def test_review_without_evidence_bumps_to_medium(self):
        effort = PlanningPolicy.estimate_effort(
            [make_objective(kind=ObjectiveKind.REVIEW)],
            previous_evidence_count=0,
        )
        assert effort == EffortEstimate.MEDIUM

    def test_rationale_tags_include_no_mastery_claim(self):
        tags = PlanningPolicy.rationale_tags(
            topic_id="topic-a",
            objectives=[make_objective()],
            previous_evidence=[],
            estimated_effort=EffortEstimate.MEDIUM,
        )
        assert "no_mastery_claim" in tags
        assert "topic=topic-a" in tags

    def test_objective_ids_ordered(self):
        ids = PlanningPolicy.objective_ids(
            [
                make_objective("a"),
                make_objective("b", sequence_index=1),
            ]
        )
        assert ids == ("a", "b")


class TestReflectionPolicy:
    def test_required_on_completed_without_reflection(self):
        session = make_session(state=SessionState.COMPLETED)
        assert ReflectionPolicy.is_required(session)

    def test_not_required_when_active(self):
        session = make_session(state=SessionState.ACTIVE)
        assert not ReflectionPolicy.is_required(session)

    def test_satisfied_when_captured(self):
        reflection = JourneyReflection.create_captured(
            "r1",
            "sess-1",
            "journey-1",
            what_was_learned="x",
            uncertainty="y",
            captured_at=__import__("datetime").datetime(
                2026, 7, 18, tzinfo=__import__("datetime").UTC
            ),
        )
        session = make_session(state=SessionState.COMPLETED, reflection=reflection)
        assert ReflectionPolicy.is_satisfied(session)
        assert not ReflectionPolicy.is_required(session)

    def test_pending_not_satisfied(self):
        reflection = JourneyReflection.create_pending("r1", "sess-1", "journey-1")
        session = make_session(state=SessionState.COMPLETED, reflection=reflection)
        assert ReflectionPolicy.is_required(session)
        assert not ReflectionPolicy.is_satisfied(session)

    def test_may_defer_pending(self):
        reflection = JourneyReflection.create_pending("r1", "sess-1", "journey-1")
        session = make_session(state=SessionState.COMPLETED, reflection=reflection)
        assert ReflectionPolicy.may_defer(session)

    def test_may_not_defer_active(self):
        assert not ReflectionPolicy.may_defer(make_session(state=SessionState.ACTIVE))

    def test_may_capture_completed_without_reflection(self):
        assert ReflectionPolicy.may_capture(
            make_session(state=SessionState.COMPLETED)
        )

    def test_may_not_capture_active(self):
        assert not ReflectionPolicy.may_capture(
            make_session(state=SessionState.ACTIVE)
        )

    def test_required_fields(self):
        fields = ReflectionPolicy.required_fields()
        assert "summary" in fields
        assert "challenges" in fields
        assert "next_intention" in fields

    def test_validate_capture_missing_summary(self):
        blockers = ReflectionPolicy.validate_capture_content(
            summary="",
            challenges="hard",
        )
        assert "missing_summary" in blockers

    def test_validate_capture_missing_challenges(self):
        blockers = ReflectionPolicy.validate_capture_content(
            summary="ok",
            challenges="  ",
        )
        assert "missing_challenges" in blockers

    def test_validate_capture_ok(self):
        assert (
            ReflectionPolicy.validate_capture_content(
                summary="ok",
                challenges="hard",
                confidence="medium",
            )
            == ()
        )

    def test_deferred_not_final_satisfaction(self):
        reflection = JourneyReflection(
            reflection_id="r1",
            session_id="sess-1",
            journey_id="journey-1",
            posture=ReflectionPosture.DEFERRED_CAPTURE,
        )
        session = make_session(state=SessionState.COMPLETED, reflection=reflection)
        assert not ReflectionPolicy.is_satisfied(session)


class TestCompletionPolicy:
    def test_not_finished_blocks(self):
        result = CompletionPolicy.evaluate(make_session(state=SessionState.ACTIVE))
        assert not result.is_complete
        assert "session_not_finished" in result.blockers
        assert result.journey_complete is False

    def test_completed_without_reflection_blocked(self):
        result = CompletionPolicy.evaluate(
            make_session(state=SessionState.COMPLETED)
        )
        assert not result.is_complete
        assert "reflection_unsatisfied" in result.blockers
        assert result.journey_complete is False

    def test_abandoned_not_complete(self):
        result = CompletionPolicy.evaluate(
            make_session(state=SessionState.ABANDONED)
        )
        assert not result.is_complete
        assert result.journey_complete is False

    def test_skipped_not_complete(self):
        result = CompletionPolicy.evaluate(make_session(state=SessionState.SKIPPED))
        assert not result.is_complete

    def test_rejects_journey_completion(self):
        assert CompletionPolicy.rejects_journey_completion()
        assert CompletionPolicy.rejects_mastery_estimation()

    def test_captured_reflection_completes(self):
        from datetime import UTC, datetime

        reflection = JourneyReflection.create_captured(
            "r1",
            "sess-1",
            "journey-1",
            what_was_learned="x",
            uncertainty="y",
            captured_at=datetime(2026, 7, 18, tzinfo=UTC),
        )
        result = CompletionPolicy.evaluate(
            make_session(state=SessionState.COMPLETED, reflection=reflection)
        )
        assert result.is_complete
        assert result.journey_complete is False


class TestSchedulingPolicy:
    def test_archived_none(self):
        session = make_session(state=SessionState.COMPLETED)
        from app.application.learning_session.policies.completion_policy import (
            CompletionPolicy,
        )

        action = SchedulingPolicy.decide(
            session,
            phase=RuntimePhase.ARCHIVED,
            completion=CompletionPolicy.evaluate(session),
        )
        assert action == NextAction.NONE

    def test_completed_owes_reflect(self):
        session = make_session(state=SessionState.COMPLETED)
        action = SchedulingPolicy.decide(
            session,
            phase=RuntimePhase.COMPLETED,
            completion=CompletionPolicy.evaluate(session),
        )
        assert action == NextAction.REFLECT

    def test_active_continue(self):
        session = make_session(state=SessionState.ACTIVE, effort=EffortEstimate.LOW)
        action = SchedulingPolicy.decide(
            session,
            phase=RuntimePhase.ACTIVE,
            completion=CompletionPolicy.evaluate(session),
            actual_duration_minutes=10,
        )
        assert action == NextAction.CONTINUE

    def test_active_break_on_long_duration(self):
        session = make_session(state=SessionState.ACTIVE)
        assert SchedulingPolicy.should_recommend_break(
            session,
            actual_duration_minutes=50,
        )

    def test_ready_start(self):
        session = make_session(state=SessionState.NOT_STARTED)
        action = SchedulingPolicy.decide(
            session,
            phase=RuntimePhase.READY,
            completion=CompletionPolicy.evaluate(session),
        )
        assert action == NextAction.START

    def test_planned_prepare(self):
        session = make_session(state=SessionState.NOT_STARTED)
        action = SchedulingPolicy.decide(
            session,
            phase=RuntimePhase.PLANNED,
            completion=CompletionPolicy.evaluate(session),
        )
        assert action == NextAction.PREPARE

    def test_paused_continue(self):
        session = make_session(state=SessionState.PAUSED)
        action = SchedulingPolicy.decide(
            session,
            phase=RuntimePhase.PAUSED,
            completion=CompletionPolicy.evaluate(session),
        )
        assert action == NextAction.CONTINUE

    def test_revise_after_thin_evidence(self):
        from datetime import UTC, datetime

        reflection = JourneyReflection.create_captured(
            "r1",
            "sess-1",
            "journey-1",
            what_was_learned="x",
            uncertainty="y",
            captured_at=datetime(2026, 7, 18, tzinfo=UTC),
        )
        session = make_session(
            state=SessionState.COMPLETED,
            reflection=reflection,
            evidence=[],
        )
        assert SchedulingPolicy.revise_after_thin_evidence(session)

    def test_no_revise_when_evidence_present(self):
        from datetime import UTC, datetime

        reflection = JourneyReflection.create_captured(
            "r1",
            "sess-1",
            "journey-1",
            what_was_learned="x",
            uncertainty="y",
            captured_at=datetime(2026, 7, 18, tzinfo=UTC),
        )
        session = make_session(
            state=SessionState.COMPLETED,
            reflection=reflection,
            evidence=[make_evidence()],
        )
        assert not SchedulingPolicy.revise_after_thin_evidence(session)
