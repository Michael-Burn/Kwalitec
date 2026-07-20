"""Orchestration stage — one coordination stage within an orchestration turn.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
    ORCHESTRATION_INVARIANTS.md
Concept
    Orchestration Stage
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId
from domain.education.orchestrator.enums import (
    EvidenceCollectionPointKind,
    OrchestrationStageKind,
    StageStatus,
)


@dataclass(frozen=True, slots=True)
class OrchestrationStageId(EducationalValueObject):
    """Identity of a stage within an EducationalOrchestrator plan."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "OrchestrationStageId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class OrchestrationStage(EducationalEntity):
    """Ordered coordination stage inside an orchestration plan.

    Stages sequence execution progress and mark evidence collection points.
    They do not diagnose, interpret evidence, or select strategies.
    """

    stage_id: OrchestrationStageId
    kind: OrchestrationStageKind
    sequence_index: int
    label: str
    required: bool = True
    status: StageStatus = StageStatus.PENDING
    evidence_collection_point: EvidenceCollectionPointKind | None = None
    episode_id: LearningEpisodeId | None = None

    @property
    def entity_id(self) -> OrchestrationStageId:
        return self.stage_id

    def _validate(self) -> None:
        if not isinstance(self.stage_id, OrchestrationStageId):
            raise EducationalInvariantViolation(
                "stage_id must be an OrchestrationStageId",
                invariant="OrchestrationStage.stage_id.type",
            )
        if not isinstance(self.kind, OrchestrationStageKind):
            raise EducationalInvariantViolation(
                "kind must be an OrchestrationStageKind",
                invariant="OrchestrationStage.kind.type",
            )
        if not isinstance(self.sequence_index, int) or self.sequence_index < 0:
            raise EducationalInvariantViolation(
                "sequence_index must be a non-negative integer",
                invariant="OrchestrationStage.sequence_index.non_negative",
            )
        object.__setattr__(
            self,
            "label",
            require_non_empty_text(self.label, "label"),
        )
        if not isinstance(self.required, bool):
            raise EducationalInvariantViolation(
                "required must be a bool",
                invariant="OrchestrationStage.required.type",
            )
        if not isinstance(self.status, StageStatus):
            raise EducationalInvariantViolation(
                "status must be a StageStatus",
                invariant="OrchestrationStage.status.type",
            )
        if self.evidence_collection_point is not None and not isinstance(
            self.evidence_collection_point, EvidenceCollectionPointKind
        ):
            raise EducationalInvariantViolation(
                "evidence_collection_point must be an EvidenceCollectionPointKind",
                invariant="OrchestrationStage.evidence_collection_point.type",
            )
        if self.episode_id is not None and not isinstance(
            self.episode_id, LearningEpisodeId
        ):
            raise EducationalInvariantViolation(
                "episode_id must be a LearningEpisodeId when provided",
                invariant="OrchestrationStage.episode_id.type",
            )
        if (
            self.kind is OrchestrationStageKind.EVIDENCE_COLLECTION
            and self.evidence_collection_point is None
        ):
            raise EducationalInvariantViolation(
                "evidence collection stages must declare a collection point",
                invariant="OrchestrationStage.evidence_collection_point.required",
            )

    def is_pending(self) -> bool:
        return self.status is StageStatus.PENDING

    def is_active(self) -> bool:
        return self.status is StageStatus.ACTIVE

    def is_completed(self) -> bool:
        return self.status is StageStatus.COMPLETED

    def is_evidence_collection_point(self) -> bool:
        return self.evidence_collection_point is not None or (
            self.kind is OrchestrationStageKind.EVIDENCE_COLLECTION
        )

    def activate(self) -> OrchestrationStage:
        """Return this stage marked ACTIVE."""
        if self.status is StageStatus.COMPLETED:
            raise EducationalInvariantViolation(
                "cannot activate a completed orchestration stage",
                invariant="OrchestrationStage.activate.completed",
            )
        if self.status is StageStatus.ACTIVE:
            return self
        return OrchestrationStage(
            stage_id=self.stage_id,
            kind=self.kind,
            sequence_index=self.sequence_index,
            label=self.label,
            required=self.required,
            status=StageStatus.ACTIVE,
            evidence_collection_point=self.evidence_collection_point,
            episode_id=self.episode_id,
        )

    def complete(self) -> OrchestrationStage:
        """Return this stage marked COMPLETED."""
        if self.status is StageStatus.COMPLETED:
            raise EducationalInvariantViolation(
                "orchestration stage is already completed",
                invariant="OrchestrationStage.complete.already",
            )
        if self.status is not StageStatus.ACTIVE:
            raise EducationalInvariantViolation(
                "only an active orchestration stage can be completed",
                invariant="OrchestrationStage.complete.not_active",
            )
        return OrchestrationStage(
            stage_id=self.stage_id,
            kind=self.kind,
            sequence_index=self.sequence_index,
            label=self.label,
            required=self.required,
            status=StageStatus.COMPLETED,
            evidence_collection_point=self.evidence_collection_point,
            episode_id=self.episode_id,
        )

    def bind_episode(self, episode_id: LearningEpisodeId) -> OrchestrationStage:
        """Attach a coordinated Learning Episode identity to this stage."""
        if not isinstance(episode_id, LearningEpisodeId):
            raise EducationalInvariantViolation(
                "episode_id must be a LearningEpisodeId",
                invariant="OrchestrationStage.bind_episode.type",
            )
        if self.status is StageStatus.COMPLETED:
            raise EducationalInvariantViolation(
                "cannot bind an episode to a completed stage",
                invariant="OrchestrationStage.bind_episode.completed",
            )
        return OrchestrationStage(
            stage_id=self.stage_id,
            kind=self.kind,
            sequence_index=self.sequence_index,
            label=self.label,
            required=self.required,
            status=self.status,
            evidence_collection_point=self.evidence_collection_point,
            episode_id=episode_id,
        )
