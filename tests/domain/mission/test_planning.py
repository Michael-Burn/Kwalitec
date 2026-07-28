"""Domain invariants for AP-002D5 Mission planning."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.domain.mission.planning.activity_type import (
    KNOWN_PLANNING_ACTIVITY_TYPES,
    PlanningActivityType,
    parse_planning_activity_type,
)
from app.domain.mission.planning.batch import PlanningBatch
from app.domain.mission.planning.candidate import MissionCandidateProjection
from app.domain.mission.planning.context import PlanningContext
from app.domain.mission.planning.errors import DuplicateMissionRequest
from app.domain.mission.planning.events import (
    MissionGenerated,
    MissionPlanningCompleted,
    MissionPlanningSkipped,
    MissionPlanningStarted,
    PlanningEventKind,
)
from app.domain.mission.planning.reference import PlanningReference
from app.domain.mission.planning.version import PLANNING_VERSION

FIXED_AT = datetime(2026, 7, 28, 14, 0, 0, tzinfo=UTC).replace(tzinfo=None)


def _context(**overrides) -> PlanningContext:
    base = dict(
        twin_id="twin-1",
        student_id="student-1",
        reasoning_request_id="rr-1",
        evidence_bundle_id="bundle-1",
        session_id="sess-1",
        correlation_id="corr-1",
        planning_version=PLANNING_VERSION,
        decision_version="AP-002D3.decision.v1",
        twin_version=1,
        decision_set_id="eds-1",
    )
    base.update(overrides)
    return PlanningContext(**base)


def _reference(**overrides) -> PlanningReference:
    base = dict(
        decision_id="ed-1",
        decision_version="AP-002D3.decision.v1",
        twin_version=1,
        evidence_bundle_id="bundle-1",
        educational_observation_ids=("obs-1",),
        reasoning_request_id="rr-1",
        assessment_session_id="sess-1",
        correlation_id="corr-1",
        planning_version=PLANNING_VERSION,
        twin_id="twin-1",
        concept_reference="concept-a",
    )
    base.update(overrides)
    return PlanningReference(**base)


def _candidate(**overrides) -> MissionCandidateProjection:
    base = dict(
        candidate_id="mc:1",
        activity_type=PlanningActivityType.PRACTICE,
        concept_id="concept-a",
        concept_title="Concept A",
        twin_id="twin-1",
        reference=_reference(),
        planning_version=PLANNING_VERSION,
        created_at=FIXED_AT,
        decision_id="ed-1",
        priority_score=42.0,
        priority_band="medium",
        provenance={
            "decision_id": "ed-1",
            "decision_version": "AP-002D3.decision.v1",
            "twin_version": 1,
            "evidence_bundle_id": "bundle-1",
            "educational_observation_ids": ["obs-1"],
            "reasoning_request_id": "rr-1",
            "assessment_session_id": "sess-1",
            "correlation_id": "corr-1",
            "planning_version": PLANNING_VERSION,
        },
    )
    base.update(overrides)
    return MissionCandidateProjection(**base)


def test_planning_version_constant() -> None:
    assert PLANNING_VERSION == "AP-002D5.planning.v1"


def test_known_activity_types() -> None:
    assert "practice" in KNOWN_PLANNING_ACTIVITY_TYPES
    assert "recovery" in KNOWN_PLANNING_ACTIVITY_TYPES
    with pytest.raises(Exception):
        parse_planning_activity_type("invented_activity")


def test_context_requires_fields() -> None:
    with pytest.raises(ValueError, match="twin_id"):
        _context(twin_id="")
    with pytest.raises(ValueError, match="twin_version"):
        _context(twin_version=0)


def test_batch_rejects_duplicate_candidates() -> None:
    ctx = _context()
    cand = _candidate()
    with pytest.raises(DuplicateMissionRequest):
        PlanningBatch(
            batch_id="batch-1",
            candidates=(cand, cand),
            context=ctx,
            planning_version=PLANNING_VERSION,
        )


def test_events_are_immutable_and_kinds_match() -> None:
    started = MissionPlanningStarted(
        event_id="e1",
        twin_id="twin-1",
        decision_set_id="eds-1",
        mission_request_id="mreq-1",
        occurred_at=FIXED_AT,
        planning_version=PLANNING_VERSION,
    )
    generated = MissionGenerated(
        event_id="e2",
        plan_id="smp-1",
        mission_id="sm-1",
        twin_id="twin-1",
        decision_id="ed-1",
        concept_id="concept-a",
        occurred_at=FIXED_AT,
        planning_version=PLANNING_VERSION,
    )
    skipped = MissionPlanningSkipped(
        event_id="e3",
        twin_id="twin-1",
        decision_id="ed-2",
        reason_code="non_plannable_decision",
        occurred_at=FIXED_AT,
        planning_version=PLANNING_VERSION,
    )
    completed = MissionPlanningCompleted(
        event_id="e4",
        twin_id="twin-1",
        decision_set_id="eds-1",
        mission_request_id="mreq-1",
        plan_id="smp-1",
        candidate_count=1,
        skipped_count=1,
        occurred_at=FIXED_AT,
        planning_version=PLANNING_VERSION,
    )
    assert started.kind is PlanningEventKind.STARTED
    assert generated.kind is PlanningEventKind.GENERATED
    assert skipped.kind is PlanningEventKind.SKIPPED
    assert completed.kind is PlanningEventKind.COMPLETED
    with pytest.raises(Exception):
        started.twin_id = "mutated"  # type: ignore[misc]
