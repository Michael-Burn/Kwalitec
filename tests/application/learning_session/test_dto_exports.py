"""DTO immutability and package export tests."""

from __future__ import annotations

import pytest

from app.application import learning_session as pkg
from app.application.learning_session.dto.completion_result import CompletionResult
from app.application.learning_session.dto.evidence_summary import EvidenceSummary
from app.application.learning_session.dto.learning_session_plan import (
    LearningSessionPlan,
)
from app.application.learning_session.dto.reflection_summary import ReflectionSummary
from app.application.learning_session.dto.runtime_snapshot import RuntimeSnapshot
from app.application.learning_session.exceptions import LearningSessionRuntimeError
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.session_state import SessionState


class TestDtoImmutability:
    def test_learning_session_plan_frozen(self):
        plan = LearningSessionPlan(
            session_id="s1",
            journey_id="j1",
            topic_id="t1",
            sequence_index=0,
            objective_ids=("o1",),
            estimated_effort=EffortEstimate.MEDIUM,
            recommended_activities=("focused_study",),
            previous_evidence_count=0,
            rationale_tags=("no_mastery_claim",),
        )
        with pytest.raises(Exception):
            plan.session_id = "x"  # type: ignore[misc]

    def test_evidence_summary_frozen(self):
        summary = EvidenceSummary(
            evidence_count=0,
            evidence_types=(),
            confidence_levels=(),
            has_evidence=False,
            session_id="s1",
        )
        with pytest.raises(Exception):
            summary.evidence_count = 1  # type: ignore[misc]

    def test_reflection_summary_frozen(self):
        summary = ReflectionSummary(
            session_id="s1",
            posture="pending",
            is_captured=False,
            questions_remaining=(),
            confidence=None,
            summary=None,
            challenges=None,
            next_intention=None,
        )
        with pytest.raises(Exception):
            summary.is_captured = True  # type: ignore[misc]

    def test_completion_result_journey_complete_default_false(self):
        result = CompletionResult(
            is_complete=True,
            session_finished=True,
            reflection_required=True,
            reflection_satisfied=True,
            evidence_recorded=True,
            blockers=(),
            reason="ok",
        )
        assert result.journey_complete is False
        with pytest.raises(Exception):
            result.journey_complete = True  # type: ignore[misc]

    def test_runtime_snapshot_frozen(self):
        snap = RuntimeSnapshot(
            session_id="s1",
            journey_id="j1",
            topic_id="t1",
            phase="active",
            session_state=SessionState.ACTIVE,
            objective_id="o1",
            plan=None,
            evidence_summary=EvidenceSummary(
                evidence_count=0,
                evidence_types=(),
                confidence_levels=(),
                has_evidence=False,
                session_id="s1",
            ),
            reflection_summary=ReflectionSummary(
                session_id="s1",
                posture="not_required",
                is_captured=False,
                questions_remaining=(),
                confidence=None,
                summary=None,
                challenges=None,
                next_intention=None,
            ),
            completion=CompletionResult(
                is_complete=False,
                session_finished=False,
                reflection_required=False,
                reflection_satisfied=False,
                evidence_recorded=False,
                blockers=("session_not_finished",),
                reason="not finished",
            ),
            next_action="continue",
            actual_duration_minutes=None,
        )
        with pytest.raises(Exception):
            snap.next_action = "break"  # type: ignore[misc]


class TestPackageExports:
    def test_lazy_exports(self):
        assert pkg.LearningSessionRuntime is not None
        assert pkg.RuntimePhase is not None
        assert pkg.NextAction is not None
        assert pkg.LearningSessionPlan is not None
        assert pkg.RuntimeSnapshot is not None
        assert pkg.EvidenceSummary is not None
        assert pkg.ReflectionSummary is not None
        assert pkg.CompletionResult is not None
        assert pkg.LifecycleManager is not None
        assert pkg.LearningSessionPlanner is not None
        assert pkg.EvidenceCollector is not None
        assert pkg.ReflectionManager is not None
        assert pkg.CompletionEvaluator is not None
        assert pkg.ActivityScheduler is not None
        assert pkg.PlanningPolicy is not None
        assert pkg.ReflectionPolicy is not None
        assert pkg.CompletionPolicy is not None
        assert pkg.SchedulingPolicy is not None

    def test_exception_hierarchy(self):
        assert issubclass(pkg.InvalidSessionState, LearningSessionRuntimeError)
        assert issubclass(pkg.SessionAlreadyCompleted, LearningSessionRuntimeError)
        assert issubclass(pkg.SessionAlreadyArchived, LearningSessionRuntimeError)
        assert issubclass(pkg.ReflectionRequired, LearningSessionRuntimeError)
        assert issubclass(pkg.EvidenceCollectionError, LearningSessionRuntimeError)
        assert issubclass(pkg.PlanningError, LearningSessionRuntimeError)
        assert issubclass(pkg.SessionNotFound, LearningSessionRuntimeError)

    def test_dir_includes_exports(self):
        names = dir(pkg)
        assert "LearningSessionRuntime" in names
        assert "RuntimePhase" in names

    def test_unknown_export_raises(self):
        with pytest.raises(AttributeError):
            _ = pkg.DoesNotExist  # type: ignore[attr-defined]
