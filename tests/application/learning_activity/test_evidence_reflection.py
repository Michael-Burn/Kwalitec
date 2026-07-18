"""Evidence and reflection routing tests."""

from __future__ import annotations

import pytest

from app.application.learning_activity.evidence_router import EvidenceRouter
from app.application.learning_activity.exceptions import (
    ActivityNotFound,
    EvidenceRoutingError,
    ReflectionRoutingError,
)
from app.application.learning_activity.reflection_router import ReflectionRouter
from app.domain.learning_activity.value_objects.activity_state import ActivityState
from app.domain.learning_activity.value_objects.activity_type import ActivityType
from tests.application.learning_activity.helpers import make_engine, make_sequence


class TestEvidenceRouter:
    def test_route_to_explicit_activity(self):
        router = EvidenceRouter()
        sequence = make_sequence(
            states=(
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
                ActivityState.NOT_STARTED,
            )
        )
        aid = sequence.activities[0].activity_id
        result = router.route(sequence, evidence_id="ev-1", activity_id=aid)
        assert result.evidence_id == "ev-1"
        assert "ev-1" in result.activity.evidence_ids

    def test_route_to_active_by_default(self):
        router = EvidenceRouter()
        sequence = make_sequence(
            states=(
                ActivityState.NOT_STARTED,
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
            )
        )
        result = router.route(sequence, evidence_id="ev-2")
        assert result.activity.sequence_index == 1

    def test_route_rejects_empty_evidence_id(self):
        with pytest.raises(EvidenceRoutingError, match="evidence_id"):
            EvidenceRouter().route(make_sequence(), evidence_id="  ")

    def test_route_requires_single_active_without_id(self):
        sequence = make_sequence()
        with pytest.raises(EvidenceRoutingError, match="exactly one ACTIVE"):
            EvidenceRouter().route(sequence, evidence_id="ev-1")

    def test_route_unknown_activity(self):
        with pytest.raises(ActivityNotFound):
            EvidenceRouter().route(
                make_sequence(), evidence_id="ev-1", activity_id="missing"
            )

    def test_route_rejects_not_started_when_require_active(self):
        sequence = make_sequence()
        aid = sequence.activities[0].activity_id
        with pytest.raises(EvidenceRoutingError, match="state"):
            EvidenceRouter().route(
                sequence, evidence_id="ev-1", activity_id=aid
            )

    def test_route_allows_paused(self):
        sequence = make_sequence(
            states=(
                ActivityState.PAUSED,
                ActivityState.NOT_STARTED,
                ActivityState.NOT_STARTED,
            )
        )
        aid = sequence.activities[0].activity_id
        result = EvidenceRouter().route(
            sequence, evidence_id="ev-1", activity_id=aid
        )
        assert "ev-1" in result.activity.evidence_ids

    def test_evidence_for(self):
        router = EvidenceRouter()
        sequence = make_sequence(
            states=(
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
                ActivityState.NOT_STARTED,
            )
        )
        aid = sequence.activities[0].activity_id
        routed = router.route(sequence, evidence_id="ev-1", activity_id=aid)
        assert router.evidence_for(routed.sequence, aid) == ("ev-1",)

    def test_engine_route_evidence(self):
        engine = make_engine()
        handle = engine.create_sequence(
            session_id="sess-1",
            activity_types=(ActivityType.CONCEPT_LEARNING, ActivityType.SUMMARY),
        )
        handle, _ = engine.start_activity(handle)
        handle = engine.route_evidence(handle, evidence_id="ev-9")
        current = engine.current_activity(handle)
        assert "ev-9" in current.evidence_ids


class TestReflectionRouter:
    def test_associate_explicit(self):
        router = ReflectionRouter()
        sequence = make_sequence(
            types=(
                ActivityType.INTRODUCTION,
                ActivityType.REFLECTION,
                ActivityType.SUMMARY,
            ),
            states=(
                ActivityState.COMPLETED,
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
            ),
        )
        aid = sequence.activities[1].activity_id
        result = router.associate(
            sequence, reflection_id="ref-1", activity_id=aid
        )
        assert "ref-1" in result.activity.reflection_ids

    def test_prefer_reflection_type(self):
        router = ReflectionRouter()
        sequence = make_sequence(
            types=(
                ActivityType.INTRODUCTION,
                ActivityType.REFLECTION,
                ActivityType.SUMMARY,
            ),
            states=(
                ActivityState.ACTIVE,
                ActivityState.COMPLETED,
                ActivityState.NOT_STARTED,
            ),
        )
        result = router.associate(sequence, reflection_id="ref-2")
        assert result.activity.activity_type is ActivityType.REFLECTION

    def test_fallback_to_active(self):
        router = ReflectionRouter()
        sequence = make_sequence(
            types=(
                ActivityType.INTRODUCTION,
                ActivityType.CONCEPT_LEARNING,
                ActivityType.SUMMARY,
            ),
            states=(
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
                ActivityState.NOT_STARTED,
            ),
        )
        result = router.associate(
            sequence, reflection_id="ref-3", prefer_reflection_type=True
        )
        assert result.activity.state is ActivityState.ACTIVE

    def test_rejects_empty_reflection_id(self):
        with pytest.raises(ReflectionRoutingError, match="reflection_id"):
            ReflectionRouter().associate(make_sequence(), reflection_id="")

    def test_rejects_not_started(self):
        sequence = make_sequence()
        with pytest.raises(ReflectionRoutingError, match="not_started"):
            ReflectionRouter().associate(
                sequence,
                reflection_id="ref-1",
                activity_id=sequence.activities[0].activity_id,
            )

    def test_rejects_skipped(self):
        sequence = make_sequence(
            states=(
                ActivityState.SKIPPED,
                ActivityState.NOT_STARTED,
                ActivityState.NOT_STARTED,
            )
        )
        with pytest.raises(ReflectionRoutingError, match="skipped"):
            ReflectionRouter().associate(
                sequence,
                reflection_id="ref-1",
                activity_id=sequence.activities[0].activity_id,
            )

    def test_unknown_activity(self):
        with pytest.raises(ActivityNotFound):
            ReflectionRouter().associate(
                make_sequence(), reflection_id="ref-1", activity_id="missing"
            )

    def test_no_suitable_default(self):
        sequence = make_sequence(
            types=(
                ActivityType.INTRODUCTION,
                ActivityType.CONCEPT_LEARNING,
                ActivityType.SUMMARY,
            ),
            states=(
                ActivityState.COMPLETED,
                ActivityState.COMPLETED,
                ActivityState.COMPLETED,
            ),
        )
        # No REFLECTION type, no ACTIVE
        with pytest.raises(ReflectionRoutingError, match="No suitable"):
            ReflectionRouter().associate(
                sequence, reflection_id="ref-1", prefer_reflection_type=True
            )

    def test_reflections_for(self):
        router = ReflectionRouter()
        sequence = make_sequence(
            states=(
                ActivityState.ACTIVE,
                ActivityState.NOT_STARTED,
                ActivityState.NOT_STARTED,
            )
        )
        aid = sequence.activities[0].activity_id
        routed = router.associate(
            sequence, reflection_id="ref-1", activity_id=aid
        )
        assert router.reflections_for(routed.sequence, aid) == ("ref-1",)

    def test_engine_associate_reflection(self):
        engine = make_engine()
        handle = engine.create_sequence(
            session_id="sess-1",
            activity_types=(
                ActivityType.CONCEPT_LEARNING,
                ActivityType.REFLECTION,
            ),
        )
        handle, _ = engine.start_activity(handle)
        handle, _, _ = engine.complete_activity(handle, start_next=True)
        handle = engine.associate_reflection(handle, reflection_id="ref-9")
        reflection_activity = handle.sequence.activities[1]
        assert "ref-9" in reflection_activity.reflection_ids

    def test_reflections_not_session_scoped(self):
        """Reflection router attributes to activities only — no session field."""
        assert not hasattr(ReflectionRouter, "associate_session")
        assert not hasattr(ReflectionRouter, "session_reflection")
