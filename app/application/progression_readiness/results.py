"""Progression Readiness result vocabulary.

Answers whether evidence justifies introducing next material for an objective.
Does not claim permanent mastery.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ProgressionReadiness(str, Enum):
    """Outcome of a Progression Readiness evaluation."""

    READY = "READY"
    NOT_READY = "NOT_READY"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class InsufficientReason(str, Enum):
    """Machine-readable reason when result is INSUFFICIENT_EVIDENCE."""

    INSUFFICIENT_SAMPLE = "INSUFFICIENT_SAMPLE"
    REQUIRED_PREREQUISITE_UNVERIFIED = "REQUIRED_PREREQUISITE_UNVERIFIED"
    REQUIRED_MODALITY_NOT_OBSERVED = "REQUIRED_MODALITY_NOT_OBSERVED"
    CONFLICTING_EVIDENCE = "CONFLICTING_EVIDENCE"


@dataclass(frozen=True)
class ProgressionReadinessResult:
    """Frozen evaluation outcome for one student and one objective contract."""

    objective_id: str
    student_id: str
    readiness: ProgressionReadiness
    reason: InsufficientReason | None = None

    def __post_init__(self) -> None:
        if self.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE:
            if self.reason is None:
                raise ValueError(
                    "INSUFFICIENT_EVIDENCE requires a specific InsufficientReason"
                )
        elif self.reason is not None:
            raise ValueError(
                f"{self.readiness.value} must not carry an InsufficientReason"
            )
