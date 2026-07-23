"""Additional edge-case coverage for Mission Execution Engine."""

from __future__ import annotations

from datetime import datetime

from application.education.mission_execution import (
    ConfidenceTrend,
    ExecutionId,
    MetricsRules,
    MissionExecution,
    MissionExecutionEngine,
)
from application.education.mission_execution.models.confidence_record import (
    ConfidenceRecord,
)
from application.education.mission_generation import MissionId, MissionStepId
from domain.education.foundation.enums import ConfidenceLevel
from tests.application.education.mission_execution.conftest import (
    at,
    make_plan,
)


def test_unknown_confidence_rejected(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    started = MissionExecutionEngine.start_execution(
        make_plan(), mission_id, execution_id=execution_id, at=t0
    ).execution
    assert started is not None
    result = MissionExecutionEngine.record_confidence(
        started, ConfidenceLevel.UNKNOWN, at=at(t0, minutes=1)
    )
    assert not result.ok
    assert result.error is not None
    assert result.error.code == "invalid_confidence"


def test_start_identity_mismatch(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    plan = make_plan()
    planned = MissionExecution.plan_execution(
        execution_id=execution_id, mission_plan=plan, mission_id=mission_id
    )
    result = MissionExecutionEngine.start_execution(
        plan,
        mission_id,
        execution_id=ExecutionId("other-exec"),
        at=t0,
        execution=planned,
    )
    assert not result.ok
    assert result.error is not None
    assert result.error.code == "execution_id_mismatch"


def test_skip_step_while_paused(
    t0: datetime, execution_id: ExecutionId, mission_id: MissionId
) -> None:
    started = MissionExecutionEngine.start_execution(
        make_plan(), mission_id, execution_id=execution_id, at=t0
    ).execution
    assert started is not None
    paused = MissionExecutionEngine.pause_execution(
        started, at=at(t0, minutes=5)
    ).execution
    assert paused is not None
    skipped = MissionExecutionEngine.skip_step(
        paused, MissionStepId("step-1"), at=at(t0, minutes=6)
    )
    assert skipped.ok
    assert skipped.execution is not None
    assert MissionStepId("step-1") in skipped.execution.skipped_step_ids


def test_confidence_trends() -> None:
    t0 = datetime(2026, 7, 23, 12, 0, 0)
    rising = (
        ConfidenceRecord(level=ConfidenceLevel.LOW, recorded_at=t0),
        ConfidenceRecord(level=ConfidenceLevel.HIGH, recorded_at=at(t0, minutes=1)),
    )
    falling = (
        ConfidenceRecord(level=ConfidenceLevel.HIGH, recorded_at=t0),
        ConfidenceRecord(level=ConfidenceLevel.LOW, recorded_at=at(t0, minutes=1)),
    )
    mixed = (
        ConfidenceRecord(level=ConfidenceLevel.LOW, recorded_at=t0),
        ConfidenceRecord(level=ConfidenceLevel.HIGH, recorded_at=at(t0, minutes=1)),
        ConfidenceRecord(level=ConfidenceLevel.MEDIUM, recorded_at=at(t0, minutes=2)),
    )
    assert MetricsRules.confidence_trend(rising) is ConfidenceTrend.RISING
    assert MetricsRules.confidence_trend(falling) is ConfidenceTrend.FALLING
    assert MetricsRules.confidence_trend(mixed) is ConfidenceTrend.MIXED
    assert MetricsRules.confidence_trend(()) is ConfidenceTrend.NONE


def test_evidence_mapping_rules_lazy_export() -> None:
    from application.education.mission_execution.rules import EvidenceMappingRules

    assert EvidenceMappingRules is not None
