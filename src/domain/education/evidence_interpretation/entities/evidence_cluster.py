"""Evidence cluster — grouped evidence references within an Interpretation.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md
Concept
    Evidence Cluster
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
from domain.education.foundation.ids import ConceptId, EvidenceId, LearningEpisodeId


@dataclass(frozen=True, slots=True)
class EvidenceClusterId(EducationalValueObject):
    """Identity of an evidence cluster within an Interpretation."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "EvidenceClusterId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class EvidenceCluster(EducationalEntity):
    """Grouped educational evidence references sharing an observational theme.

    Clusters organise evidence for pattern recognition. They do not diagnose,
    recommend, or prioritise.
    """

    cluster_id: EvidenceClusterId
    theme: str
    evidence_ids: tuple[EvidenceId, ...]
    concept_id: ConceptId | None = None
    learning_episode_id: LearningEpisodeId | None = None

    @property
    def entity_id(self) -> EvidenceClusterId:
        return self.cluster_id

    def _validate(self) -> None:
        if not isinstance(self.cluster_id, EvidenceClusterId):
            raise EducationalInvariantViolation(
                "cluster_id must be an EvidenceClusterId",
                invariant="EvidenceCluster.cluster_id.type",
            )
        object.__setattr__(self, "theme", require_non_empty_text(self.theme, "theme"))
        object.__setattr__(
            self,
            "evidence_ids",
            self._validate_evidence_ids(self.evidence_ids),
        )
        if self.concept_id is not None and not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId when provided",
                invariant="EvidenceCluster.concept_id.type",
            )
        if self.learning_episode_id is not None and not isinstance(
            self.learning_episode_id, LearningEpisodeId
        ):
            raise EducationalInvariantViolation(
                "learning_episode_id must be a LearningEpisodeId when provided",
                invariant="EvidenceCluster.learning_episode_id.type",
            )

    @staticmethod
    def _validate_evidence_ids(
        evidence_ids: tuple[EvidenceId, ...] | list[EvidenceId],
    ) -> tuple[EvidenceId, ...]:
        items = tuple(evidence_ids)
        if not items:
            raise EducationalInvariantViolation(
                "evidence cluster must reference at least one evidence id",
                invariant="EvidenceCluster.evidence_ids.min_one",
            )
        seen: set[str] = set()
        for evidence_id in items:
            if not isinstance(evidence_id, EvidenceId):
                raise EducationalInvariantViolation(
                    "evidence_ids must be EvidenceId values",
                    invariant="EvidenceCluster.evidence_ids.type",
                )
            if evidence_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate evidence id is not allowed in a cluster",
                    invariant="EvidenceCluster.evidence_ids.no_duplicate",
                )
            seen.add(evidence_id.value)
        return items

    def size(self) -> int:
        return len(self.evidence_ids)

    def contains(self, evidence_id: EvidenceId) -> bool:
        return evidence_id in self.evidence_ids

    def with_evidence(self, evidence_id: EvidenceId) -> EvidenceCluster:
        """Return a copy that adds an evidence reference (no duplicates)."""
        if not isinstance(evidence_id, EvidenceId):
            raise EducationalInvariantViolation(
                "evidence_id must be an EvidenceId",
                invariant="EvidenceCluster.with_evidence.type",
            )
        if evidence_id in self.evidence_ids:
            raise EducationalInvariantViolation(
                "evidence id already present in cluster",
                invariant="EvidenceCluster.with_evidence.duplicate",
            )
        return EvidenceCluster(
            cluster_id=self.cluster_id,
            theme=self.theme,
            evidence_ids=(*self.evidence_ids, evidence_id),
            concept_id=self.concept_id,
            learning_episode_id=self.learning_episode_id,
        )

    def cluster_signature(self) -> tuple[str, str, str | None, str | None]:
        """Structural fingerprint for duplicate cluster detection."""
        return (
            self.theme.casefold(),
            "|".join(sorted(eid.value for eid in self.evidence_ids)),
            None if self.concept_id is None else self.concept_id.value,
            None
            if self.learning_episode_id is None
            else self.learning_episode_id.value,
        )
