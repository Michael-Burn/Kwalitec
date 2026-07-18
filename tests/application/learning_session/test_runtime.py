"""Tests for LearningSessionRuntime facade."""

from __future__ import annotations

import pytest

from app.application.learning_session.exceptions import (
    InvalidSessionState,
    ReflectionRequired,
    SessionAlreadyArchived,
    SessionAlreadyCompleted,
)
from app.application.learning_session.policies.scheduling_policy import NextAction
from app.application.learning_session.runtime import (
    LearningSessionRuntime,
)
from app.application.learning_session.runtime_phase import RuntimePhase
from app.domain.evidence.evidence_type import EvidenceType
from app.domain.learning_journey.entities.learning_objective import ObjectiveKind
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.session_state import SessionState
from tests.application.learning_session.helpers import (
    active_handle,
    completed_handle,
    make_journey,
    make_objective,
    make_runtime,
    make_session,
    phase_handle,
)


class TestLearningSessionRuntimeCreate:
    def test_create_session_planned(self):
        rt = make_runtime()
        handle = rt.create_session(
            make_journey(),
            objectives=[make_objective()],
        )
        assert handle.phase == RuntimePhase.PLANNED
        assert handle.session.state == SessionState.NOT_STARTED
        assert handle.plan is not None
        assert handle.plan.objective_ids == ("obj-1",)

    def test_create_session_with_effort(self):
        rt = make_runtime()
        handle = rt.create_session(
            make_journey(),
            estimated_effort=EffortEstimate.HIGH,
        )
        assert handle.session.estimated_effort == EffortEstimate.HIGH

    def test_plan_session_without_creating(self):
        rt = make_runtime()
        plan = rt.plan_session(
            make_journey(),
            objectives=[make_objective(kind=ObjectiveKind.APPLY)],
        )
        assert "worked_example" in plan.recommended_activities
        assert plan.session_id.startswith("sess-")


class TestLearningSessionRuntimeLifecycle:
    def test_prepare_start_pause_resume_complete_archive(self):
        rt = make_runtime()
        handle = rt.create_session(make_journey(), objectives=[make_objective()])
        handle = rt.prepare_session(handle)
        assert handle.phase == RuntimePhase.READY
        handle = rt.start_session(handle)
        assert handle.phase == RuntimePhase.ACTIVE
        handle = rt.pause_session(handle)
        assert handle.phase == RuntimePhase.PAUSED
        handle = rt.resume_session(handle)
        assert handle.phase == RuntimePhase.ACTIVE
        handle = rt.complete_session(handle, actual_duration_minutes=22)
        assert handle.phase == RuntimePhase.COMPLETED
        assert handle.session.reflection is not None
        handle, _ = rt.collect_reflection(
            handle,
            summary="Done",
            challenges="None",
        )
        handle = rt.archive_session(handle)
        assert handle.phase == RuntimePhase.ARCHIVED

    def test_start_from_planned_skips_prepare(self):
        rt = make_runtime()
        handle = rt.create_session(make_journey())
        handle = rt.start_session(handle)
        assert handle.phase == RuntimePhase.ACTIVE

    def test_complete_rejects_planned(self):
        rt = make_runtime()
        handle = rt.create_session(make_journey())
        with pytest.raises((InvalidSessionState, SessionAlreadyCompleted)):
            rt.complete_session(handle)

    def test_pause_rejects_ready(self):
        rt = make_runtime()
        handle = phase_handle(RuntimePhase.READY, runtime=rt)
        with pytest.raises(InvalidSessionState):
            rt.pause_session(handle)

    def test_archive_rejects_active(self):
        rt = make_runtime()
        handle = active_handle(rt)
        with pytest.raises((InvalidSessionState, SessionAlreadyCompleted)):
            rt.archive_session(handle)

    def test_double_archive_raises(self):
        rt = make_runtime()
        handle = phase_handle(RuntimePhase.ARCHIVED, runtime=rt)
        with pytest.raises(SessionAlreadyArchived):
            rt.archive_session(handle)


class TestLearningSessionRuntimeEvidenceReflection:
    def test_collect_evidence_and_summary(self):
        rt = make_runtime()
        handle = active_handle(rt)
        handle, je, summary = rt.collect_evidence(
            handle,
            evidence_type=EvidenceType.QUESTION_ATTEMPT,
        )
        assert je.session_id == handle.session.session_id
        assert summary.has_evidence
        assert summary.evidence_count == 1

    def test_collect_evidence_rejects_planned(self):
        rt = make_runtime()
        handle = rt.create_session(make_journey())
        with pytest.raises(InvalidSessionState):
            rt.collect_evidence(handle)

    def test_collect_reflection(self):
        rt = make_runtime()
        handle = completed_handle(rt, with_reflection=False)
        handle, summary = rt.collect_reflection(
            handle,
            summary="Understood integrals",
            challenges="Substitution steps",
            questions_remaining=["When to use parts?"],
            next_intention="Do practice set",
        )
        assert summary.is_captured
        assert summary.next_intention == "Do practice set"
        assert rt.evaluate_completion(handle).is_complete

    def test_collect_reflection_requires_content(self):
        rt = make_runtime()
        handle = completed_handle(rt)
        with pytest.raises(ReflectionRequired):
            rt.collect_reflection(handle, summary="", challenges="x")

    def test_defer_reflection(self):
        rt = make_runtime()
        handle = completed_handle(rt)
        handle = rt.defer_reflection(handle)
        assert handle.session.reflection.posture.value == "deferred_capture"

    def test_reflection_rejects_active(self):
        rt = make_runtime()
        handle = active_handle(rt)
        with pytest.raises(InvalidSessionState):
            rt.collect_reflection(handle, summary="x", challenges="y")


class TestLearningSessionRuntimeSnapshotAndActions:
    def test_snapshot_fields(self):
        rt = make_runtime()
        handle = completed_handle(rt, with_reflection=True)
        snap = rt.generate_runtime_snapshot(handle)
        assert snap.session_id == handle.session.session_id
        assert snap.phase == RuntimePhase.COMPLETED.value
        assert snap.completion.journey_complete is False
        assert snap.evidence_summary.has_evidence
        assert snap.reflection_summary.is_captured
        assert snap.next_action in {
            NextAction.NEXT_SESSION.value,
            NextAction.REVISE.value,
            NextAction.ARCHIVE.value,
        }

    def test_next_action_active_continue(self):
        rt = make_runtime()
        handle = active_handle(rt)
        assert rt.generate_next_action(handle) == NextAction.CONTINUE

    def test_next_action_completed_reflect(self):
        rt = make_runtime()
        handle = completed_handle(rt, with_reflection=False)
        assert rt.generate_next_action(handle) == NextAction.REFLECT

    def test_evaluate_completion_never_journey(self):
        rt = make_runtime()
        handle = completed_handle(rt, with_reflection=True)
        result = rt.evaluate_completion(handle)
        assert result.journey_complete is False

    def test_rehydrate_active(self):
        rt = make_runtime()
        session = make_session(state=SessionState.ACTIVE)
        handle = rt.rehydrate(session)
        assert handle.phase == RuntimePhase.ACTIVE

    def test_rehydrate_prepared_not_started(self):
        rt = make_runtime()
        handle = rt.rehydrate(make_session(), prepared=True)
        assert handle.phase == RuntimePhase.READY

    def test_rehydrate_archived(self):
        rt = make_runtime()
        handle = rt.rehydrate(
            make_session(state=SessionState.COMPLETED),
            archived=True,
        )
        assert handle.phase == RuntimePhase.ARCHIVED

    def test_rejects_completed_mutation_guard(self):
        rt = make_runtime()
        handle = completed_handle(rt, with_reflection=True)
        with pytest.raises(SessionAlreadyCompleted):
            LearningSessionRuntime.rejects_completed_mutation(handle)

    def test_end_to_end_deterministic(self):
        rt = make_runtime()
        journey = make_journey(
            objectives=[
                make_objective("obj-1"),
                make_objective("obj-2", kind=ObjectiveKind.APPLY, sequence_index=1),
            ]
        )
        h1 = rt.create_session(journey, objectives=[make_objective("obj-1")])
        h2 = rt.create_session(journey, objectives=[make_objective("obj-1")])
        assert h1.plan.recommended_activities == h2.plan.recommended_activities
        assert h1.plan.rationale_tags == h2.plan.rationale_tags

    def test_session_complete_does_not_complete_journey(self):
        rt = make_runtime()
        journey = make_journey()
        handle = rt.create_session(journey, objectives=list(journey.objectives))
        handle = rt.start_session(handle)
        handle, _, _ = rt.collect_evidence(handle)
        handle = rt.complete_session(handle)
        handle, _ = rt.collect_reflection(
            handle,
            summary="ok",
            challenges="ok",
        )
        # Journey object was never mutated by the runtime.
        assert journey.state.value == "active"
        assert rt.evaluate_completion(handle).journey_complete is False


class TestFrameworkIndependence:
    def test_no_flask_import_in_package(self):
        import pathlib
        import re

        import app.application.learning_session as pkg

        root = pathlib.Path(pkg.__file__).parent
        import_pattern = re.compile(
            r"^\s*(?:from|import)\s+(flask|sqlalchemy)\b",
            re.IGNORECASE | re.MULTILINE,
        )
        for path in root.rglob("*.py"):
            text = path.read_text()
            assert import_pattern.search(text) is None, path

    def test_handle_is_immutable(self):
        handle = active_handle()
        with pytest.raises(Exception):
            handle.phase = RuntimePhase.PAUSED  # type: ignore[misc]
