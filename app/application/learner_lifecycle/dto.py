"""DTOs and result envelopes for Learner Lifecycle Orchestration (LP-001)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.application.educational_experience_engine.dto import ExperiencePortfolio
from app.application.educational_reasoning_engine.dto import EvaluateDecisionsResult
from app.application.learner_lifecycle.stages import (
    LifecycleStage,
    OperationStatus,
    OperationType,
)
from app.application.learner_lifecycle.versions import ORCHESTRATOR_VERSION
from app.application.learning_evidence.dto import RecordEvidenceResult
from app.application.student_curriculum_binding.dto import BindingResult
from app.application.twin_inference.dto import RebuildBeliefsResult


@dataclass(frozen=True, slots=True)
class StageExecutionRecord:
    """Operational record for one coordinated stage invocation."""

    stage: LifecycleStage
    succeeded: bool
    attempts: int
    duration_ms: float
    error: str | None = None


@dataclass(frozen=True, slots=True)
class LifecycleResult:
    """Outcome of one learner lifecycle orchestration run.

    Educational artefacts are passed through from EI/EX services unchanged.
    Operational fields are orchestration-only.
    """

    operation_id: str
    operation_type: OperationType
    status: OperationStatus
    student_id: int | None
    instance_id: str | None
    orchestrator_version: str = ORCHESTRATOR_VERSION
    correlation_id: str | None = None
    binding: BindingResult | None = None
    evidence: RecordEvidenceResult | None = None
    beliefs: RebuildBeliefsResult | None = None
    decisions: EvaluateDecisionsResult | None = None
    experience: ExperiencePortfolio | None = None
    stages: tuple[StageExecutionRecord, ...] = field(default_factory=tuple)
    completed_stages: tuple[LifecycleStage, ...] = field(default_factory=tuple)
    failed_stage: LifecycleStage | None = None
    failure_cause: str | None = None
    attempt_count: int = 1

    @property
    def succeeded(self) -> bool:
        return self.status == OperationStatus.COMPLETED

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "operation_type": self.operation_type.value,
            "status": self.status.value,
            "student_id": self.student_id,
            "instance_id": self.instance_id,
            "orchestrator_version": self.orchestrator_version,
            "correlation_id": self.correlation_id,
            "completed_stages": [s.value for s in self.completed_stages],
            "failed_stage": (
                self.failed_stage.value if self.failed_stage else None
            ),
            "failure_cause": self.failure_cause,
            "attempt_count": self.attempt_count,
            "belief_count": (
                self.beliefs.belief_count if self.beliefs is not None else None
            ),
            "decision_count": (
                self.decisions.decision_count if self.decisions is not None else None
            ),
            "experience_count": (
                self.experience.count if self.experience is not None else None
            ),
            "stages": [
                {
                    "stage": r.stage.value,
                    "succeeded": r.succeeded,
                    "attempts": r.attempts,
                    "duration_ms": r.duration_ms,
                    "error": r.error,
                }
                for r in self.stages
            ],
        }


@dataclass(frozen=True, slots=True)
class ConsistencyReport:
    """Snapshot of whether an SCI has complete Educational Intelligence state."""

    instance_id: str
    has_instance: bool
    node_state_count: int
    belief_count: int
    decision_count: int
    is_complete: bool
    missing: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "has_instance": self.has_instance,
            "node_state_count": self.node_state_count,
            "belief_count": self.belief_count,
            "decision_count": self.decision_count,
            "is_complete": self.is_complete,
            "missing": list(self.missing),
        }
