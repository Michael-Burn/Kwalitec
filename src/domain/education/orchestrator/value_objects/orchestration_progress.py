"""Orchestration progress — stage advancement snapshot.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
Concept
    Orchestration Progress
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class OrchestrationProgress(EducationalValueObject):
    """Immutable snapshot of how far orchestration has advanced through stages."""

    current_index: int
    completed_stages: int
    total_stages: int
    completed_required_stages: int
    total_required_stages: int
    evidence_collection_points_reached: int
    total_evidence_collection_points: int

    def _validate(self) -> None:
        for name, value in (
            ("current_index", self.current_index),
            ("completed_stages", self.completed_stages),
            ("total_stages", self.total_stages),
            ("completed_required_stages", self.completed_required_stages),
            ("total_required_stages", self.total_required_stages),
            (
                "evidence_collection_points_reached",
                self.evidence_collection_points_reached,
            ),
            (
                "total_evidence_collection_points",
                self.total_evidence_collection_points,
            ),
        ):
            if not isinstance(value, int):
                raise EducationalInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"OrchestrationProgress.{name}.type",
                )
            if value < 0:
                raise EducationalInvariantViolation(
                    f"{name} must be non-negative",
                    invariant=f"OrchestrationProgress.{name}.non_negative",
                )
        if self.total_stages < 1:
            raise EducationalInvariantViolation(
                "total_stages must be at least 1",
                invariant="OrchestrationProgress.total_stages.min",
            )
        if self.completed_stages > self.total_stages:
            raise EducationalInvariantViolation(
                "completed_stages cannot exceed total_stages",
                invariant="OrchestrationProgress.completed_stages.bounds",
            )
        if self.completed_required_stages > self.total_required_stages:
            raise EducationalInvariantViolation(
                "completed_required_stages cannot exceed total_required_stages",
                invariant="OrchestrationProgress.completed_required.bounds",
            )
        if self.current_index > self.total_stages:
            raise EducationalInvariantViolation(
                "current_index cannot exceed total_stages",
                invariant="OrchestrationProgress.current_index.bounds",
            )
        if (
            self.evidence_collection_points_reached
            > self.total_evidence_collection_points
        ):
            raise EducationalInvariantViolation(
                "evidence collection points reached cannot exceed total",
                invariant="OrchestrationProgress.evidence_points.bounds",
            )

    @property
    def required_sequence_complete(self) -> bool:
        """True when every required stage is completed."""
        return (
            self.total_required_stages > 0
            and self.completed_required_stages >= self.total_required_stages
        )

    @property
    def all_stages_complete(self) -> bool:
        """True when every stage (required and optional) is completed."""
        return self.completed_stages >= self.total_stages

    @property
    def ratio(self) -> float:
        """Fraction of total stages completed in [0, 1]."""
        if self.total_stages == 0:
            return 0.0
        return self.completed_stages / self.total_stages

    @property
    def evidence_points_complete(self) -> bool:
        """True when every evidence collection point stage is completed."""
        if self.total_evidence_collection_points == 0:
            return True
        return (
            self.evidence_collection_points_reached
            >= self.total_evidence_collection_points
        )
