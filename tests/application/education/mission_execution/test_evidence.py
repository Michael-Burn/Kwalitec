"""Evidence generation and mapping tests."""

from __future__ import annotations

from datetime import datetime

from application.education.mission_execution import (
    ExecutionId,
    MissionExecutionEngine,
)
from application.education.mission_generation import MissionId, MissionStepId
from domain.education.educational_evidence.enums import EvidenceType
from domain.education.foundation.enums import ConfidenceLevel
from tests.application.education.mission_execution.conftest import (
    at,
    make_plan,
)


def _start(t0: datetime, execution_id: ExecutionId, mission_id: MissionId):
    plan = make_plan()
    result = MissionExecutionEngine.start_execution(
        plan, mission_id, execution_id=execution_id, at=t0
    )
    assert result.ok and result.execution is not None
    return result


def test_start_emits_study_session_evidence(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    result = _start(t0, execution_id, mission_id)
    types = {e.evidence_type for e in result.evidence}
    assert EvidenceType.STUDY_SESSION_STARTED in types


def test_step_completed_emits_practice_evidence(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    started = _start(t0, execution_id, mission_id).execution
    assert started is not None
    result = MissionExecutionEngine.complete_step(
        started, MissionStepId("step-1"), at=at(t0, minutes=5)
    )
    assert result.ok
    types = {e.evidence_type for e in result.evidence}
    assert EvidenceType.COMPETENCY_PRACTISED in types


def test_confidence_emits_self_confidence_evidence(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    started = _start(t0, execution_id, mission_id).execution
    assert started is not None
    result = MissionExecutionEngine.record_confidence(
        started, ConfidenceLevel.HIGH, at=at(t0, minutes=2)
    )
    assert result.ok
    types = {e.evidence_type for e in result.evidence}
    assert EvidenceType.CONFIDENCE_REPORTED in types


def test_reflection_emits_reflection_evidence(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    started = _start(t0, execution_id, mission_id).execution
    assert started is not None
    result = MissionExecutionEngine.record_reflection(
        started, "I understand linear equations better", at=at(t0, minutes=3)
    )
    assert result.ok
    types = {e.evidence_type for e in result.evidence}
    assert EvidenceType.REFLECTION_RECORDED in types


def test_complete_emits_mission_and_study_evidence(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    started = _start(t0, execution_id, mission_id).execution
    assert started is not None
    result = MissionExecutionEngine.complete_execution(
        started, at=at(t0, minutes=20)
    )
    assert result.ok
    types = {e.evidence_type for e in result.evidence}
    assert EvidenceType.MISSION_COMPLETED in types
    assert EvidenceType.STUDY_SESSION_COMPLETED in types
    assert EvidenceType.TIME_INVESTED in types


def test_abandon_emits_engagement_evidence(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    started = _start(t0, execution_id, mission_id).execution
    assert started is not None
    result = MissionExecutionEngine.abandon_execution(
        started, at=at(t0, minutes=4)
    )
    assert result.ok
    types = {e.evidence_type for e in result.evidence}
    assert EvidenceType.MISSION_ABANDONED in types
    abandoned = next(
        e for e in result.evidence if e.evidence_type is EvidenceType.MISSION_ABANDONED
    )
    assert abandoned.metadata.get("engagement") == "abandoned"


def test_evidence_ids_are_deterministic(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    a = _start(t0, execution_id, mission_id)
    b = _start(t0, execution_id, mission_id)
    assert [e.evidence_id for e in a.evidence] == [e.evidence_id for e in b.evidence]
