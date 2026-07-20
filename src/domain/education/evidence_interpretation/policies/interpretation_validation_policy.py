"""Policy governing Interpretation construction and identity integrity.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md
Concept
    Interpretation Validation Policy
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.evidence_interpretation.entities.evidence_cluster import (
    EvidenceCluster,
)
from domain.education.evidence_interpretation.entities.interpretation_context import (
    InterpretationContext,
)
from domain.education.evidence_interpretation.entities.interpreted_pattern import (
    InterpretedPattern,
)
from domain.education.evidence_interpretation.enums import InterpretationStatus
from domain.education.evidence_interpretation.value_objects.interpretation_confidence import (  # noqa: E501
    InterpretationConfidence,
)
from domain.education.evidence_interpretation.value_objects.interpretation_summary import (  # noqa: E501
    InterpretationSummary,
)
from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    ConceptId,
    EvidenceId,
    LearningEpisodeId,
)
from domain.education.foundation.references import ConceptReference


@dataclass(frozen=True, slots=True)
class InterpretationId(EducationalValueObject):
    """Identity of an Interpretation aggregate."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "InterpretationId"),
        )

    def __str__(self) -> str:
        return self.value


class InterpretationValidationPolicy:
    """Enforces Interpretation identity, ownership, and pattern invariants."""

    @staticmethod
    def assert_identity(interpretation_id: InterpretationId) -> InterpretationId:
        if not isinstance(interpretation_id, InterpretationId):
            raise EducationalInvariantViolation(
                "interpretation must possess an InterpretationId identity",
                invariant="Interpretation.identity.required",
            )
        return interpretation_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_context(context: InterpretationContext) -> InterpretationContext:
        if not isinstance(context, InterpretationContext):
            raise EducationalInvariantViolation(
                "interpretation must identify its educational context",
                invariant="Interpretation.context.required",
            )
        if not context.educational_scope.strip():
            raise EducationalInvariantViolation(
                "interpretation must identify educational scope",
                invariant="Interpretation.scope.required",
            )
        return context

    @staticmethod
    def assert_confidence(
        confidence: InterpretationConfidence,
    ) -> InterpretationConfidence:
        if not isinstance(confidence, InterpretationConfidence):
            raise EducationalInvariantViolation(
                "interpretation must possess confidence",
                invariant="Interpretation.confidence.required",
            )
        return confidence

    @staticmethod
    def assert_summary(summary: InterpretationSummary) -> InterpretationSummary:
        if not isinstance(summary, InterpretationSummary):
            raise EducationalInvariantViolation(
                "interpretation must possess a summary",
                invariant="Interpretation.summary.required",
            )
        return summary

    @staticmethod
    def assert_clusters(
        clusters: tuple[EvidenceCluster, ...] | list[EvidenceCluster],
    ) -> tuple[EvidenceCluster, ...]:
        """Interpretation must have at least one evidence cluster."""
        collected = tuple(clusters)
        if not collected:
            raise EducationalInvariantViolation(
                "interpretation cannot exist without evidence "
                "(at least one evidence cluster required)",
                invariant="Interpretation.clusters.min_one",
            )
        seen_ids: set[str] = set()
        seen_signatures: set[tuple[str, str, str | None, str | None]] = set()
        for cluster in collected:
            if not isinstance(cluster, EvidenceCluster):
                raise EducationalInvariantViolation(
                    "clusters must be EvidenceCluster entities",
                    invariant="Interpretation.clusters.type",
                )
            if cluster.cluster_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate evidence cluster identity is not allowed",
                    invariant="Interpretation.clusters.no_duplicate_id",
                )
            signature = cluster.cluster_signature()
            if signature in seen_signatures:
                raise EducationalInvariantViolation(
                    "identical evidence clusters must not be duplicated",
                    invariant="Interpretation.clusters.no_identical_duplicate",
                )
            seen_ids.add(cluster.cluster_id.value)
            seen_signatures.add(signature)
        return collected

    @staticmethod
    def assert_patterns(
        patterns: tuple[InterpretedPattern, ...] | list[InterpretedPattern],
    ) -> tuple[InterpretedPattern, ...]:
        """Interpretation must identify at least one pattern; no duplicates."""
        collected = tuple(patterns)
        if not collected:
            raise EducationalInvariantViolation(
                "interpretation must identify at least one educational pattern",
                invariant="Interpretation.patterns.min_one",
            )
        seen_ids: set[str] = set()
        seen_signatures: set[tuple[str, str, str | None, str | None]] = set()
        for pattern in collected:
            if not isinstance(pattern, InterpretedPattern):
                raise EducationalInvariantViolation(
                    "patterns must be InterpretedPattern entities",
                    invariant="Interpretation.patterns.type",
                )
            if pattern.pattern_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate interpreted pattern identity is not allowed",
                    invariant="Interpretation.patterns.no_duplicate_id",
                )
            signature = pattern.pattern_signature()
            if signature in seen_signatures:
                raise EducationalInvariantViolation(
                    "cannot duplicate patterns",
                    invariant="Interpretation.patterns.no_duplicate",
                )
            seen_ids.add(pattern.pattern_id.value)
            seen_signatures.add(signature)
        return collected

    @staticmethod
    def assert_pattern_not_duplicate(
        existing: tuple[InterpretedPattern, ...] | list[InterpretedPattern],
        candidate: InterpretedPattern,
    ) -> None:
        if not isinstance(candidate, InterpretedPattern):
            raise EducationalInvariantViolation(
                "candidate must be an InterpretedPattern",
                invariant="Interpretation.patterns.candidate_type",
            )
        for pattern in existing:
            if pattern.pattern_id == candidate.pattern_id:
                raise EducationalInvariantViolation(
                    "duplicate interpreted pattern identity is not allowed",
                    invariant="Interpretation.patterns.no_duplicate_id",
                )
            if pattern.pattern_signature() == candidate.pattern_signature():
                raise EducationalInvariantViolation(
                    "cannot duplicate patterns",
                    invariant="Interpretation.patterns.no_duplicate",
                )

    @staticmethod
    def assert_references_evidence(
        clusters: tuple[EvidenceCluster, ...] | list[EvidenceCluster],
        patterns: tuple[InterpretedPattern, ...] | list[InterpretedPattern],
    ) -> frozenset[EvidenceId]:
        """Interpretation must reference evidence; collect all evidence ids."""
        evidence_ids: set[EvidenceId] = set()
        for cluster in clusters:
            evidence_ids.update(cluster.evidence_ids)
        for pattern in patterns:
            evidence_ids.update(pattern.evidence_ids)
        if not evidence_ids:
            raise EducationalInvariantViolation(
                "interpretation must reference evidence",
                invariant="Interpretation.evidence.required",
            )
        return frozenset(evidence_ids)

    @staticmethod
    def assert_known_concepts(
        known: frozenset[ConceptId] | set[ConceptId] | tuple[ConceptId, ...],
        concept_ids: frozenset[ConceptId] | set[ConceptId] | tuple[ConceptId, ...],
    ) -> None:
        known_set = frozenset(known)
        for concept_id in concept_ids:
            if not isinstance(concept_id, ConceptId):
                raise EducationalInvariantViolation(
                    "concept references must use ConceptId",
                    invariant="Interpretation.concepts.type",
                )
            if concept_id not in known_set:
                raise EducationalInvariantViolation(
                    f"unknown concept referenced: {concept_id.value}",
                    invariant="Interpretation.concepts.known",
                )

    @staticmethod
    def assert_known_episodes(
        known: frozenset[LearningEpisodeId]
        | set[LearningEpisodeId]
        | tuple[LearningEpisodeId, ...],
        episode_ids: frozenset[LearningEpisodeId]
        | set[LearningEpisodeId]
        | tuple[LearningEpisodeId, ...],
    ) -> None:
        known_set = frozenset(known)
        for episode_id in episode_ids:
            if not isinstance(episode_id, LearningEpisodeId):
                raise EducationalInvariantViolation(
                    "episode references must use LearningEpisodeId",
                    invariant="Interpretation.episodes.type",
                )
            if episode_id not in known_set:
                raise EducationalInvariantViolation(
                    f"unknown learning episode referenced: {episode_id.value}",
                    invariant="Interpretation.episodes.known",
                )

    @staticmethod
    def assert_known_evidence(
        known: frozenset[EvidenceId] | set[EvidenceId] | tuple[EvidenceId, ...],
        evidence_ids: frozenset[EvidenceId] | set[EvidenceId] | tuple[EvidenceId, ...],
    ) -> None:
        known_set = frozenset(known)
        for evidence_id in evidence_ids:
            if not isinstance(evidence_id, EvidenceId):
                raise EducationalInvariantViolation(
                    "evidence references must use EvidenceId",
                    invariant="Interpretation.evidence.type",
                )
            if evidence_id not in known_set:
                raise EducationalInvariantViolation(
                    f"unknown evidence referenced: {evidence_id.value}",
                    invariant="Interpretation.evidence.known",
                )

    @staticmethod
    def assert_concept_references(
        references: tuple[ConceptReference, ...] | list[ConceptReference],
    ) -> tuple[ConceptReference, ...]:
        items = tuple(references)
        seen: set[str] = set()
        for ref in items:
            if not isinstance(ref, ConceptReference):
                raise EducationalInvariantViolation(
                    "concept references must be ConceptReference values",
                    invariant="Interpretation.concept_references.type",
                )
            if ref.concept_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate concept reference is not allowed",
                    invariant="Interpretation.concept_references.no_duplicate",
                )
            seen.add(ref.concept_id.value)
        return items

    @staticmethod
    def assert_episode_references(
        episode_ids: tuple[LearningEpisodeId, ...] | list[LearningEpisodeId],
    ) -> tuple[LearningEpisodeId, ...]:
        items = tuple(episode_ids)
        seen: set[str] = set()
        for episode_id in items:
            if not isinstance(episode_id, LearningEpisodeId):
                raise EducationalInvariantViolation(
                    "learning episode references must be LearningEpisodeId values",
                    invariant="Interpretation.learning_episode_ids.type",
                )
            if episode_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate learning episode reference is not allowed",
                    invariant="Interpretation.learning_episode_ids.no_duplicate",
                )
            seen.add(episode_id.value)
        return items

    @staticmethod
    def assert_status(status: InterpretationStatus) -> InterpretationStatus:
        if not isinstance(status, InterpretationStatus):
            raise EducationalInvariantViolation(
                "status must be an InterpretationStatus",
                invariant="Interpretation.status.type",
            )
        return status

    @staticmethod
    def assert_mutable(status: InterpretationStatus, *, action: str) -> None:
        if status is InterpretationStatus.INVALIDATED:
            raise EducationalInvariantViolation(
                f"cannot {action} an invalidated interpretation",
                invariant="Interpretation.mutable.invalidated",
            )
        if status is InterpretationStatus.MERGED:
            raise EducationalInvariantViolation(
                f"cannot {action} a merged interpretation",
                invariant="Interpretation.mutable.merged",
            )

    @staticmethod
    def assert_summary_counts(
        summary: InterpretationSummary,
        patterns: tuple[InterpretedPattern, ...] | list[InterpretedPattern],
        clusters: tuple[EvidenceCluster, ...] | list[EvidenceCluster],
    ) -> None:
        if summary.pattern_count != len(tuple(patterns)):
            raise EducationalInvariantViolation(
                "summary pattern_count must match patterns length",
                invariant="Interpretation.summary.pattern_count",
            )
        if summary.cluster_count != len(tuple(clusters)):
            raise EducationalInvariantViolation(
                "summary cluster_count must match clusters length",
                invariant="Interpretation.summary.cluster_count",
            )

    @staticmethod
    def collect_referenced_concept_ids(
        clusters: tuple[EvidenceCluster, ...] | list[EvidenceCluster],
        patterns: tuple[InterpretedPattern, ...] | list[InterpretedPattern],
        context: InterpretationContext,
        concept_references: tuple[ConceptReference, ...] | list[ConceptReference],
    ) -> frozenset[ConceptId]:
        ids: set[ConceptId] = set()
        for cluster in clusters:
            if cluster.concept_id is not None:
                ids.add(cluster.concept_id)
        for pattern in patterns:
            if pattern.concept_id is not None:
                ids.add(pattern.concept_id)
        ids.update(context.concept_ids())
        for ref in concept_references:
            ids.add(ref.concept_id)
        return frozenset(ids)

    @staticmethod
    def collect_referenced_episode_ids(
        clusters: tuple[EvidenceCluster, ...] | list[EvidenceCluster],
        patterns: tuple[InterpretedPattern, ...] | list[InterpretedPattern],
        context: InterpretationContext,
        episode_ids: tuple[LearningEpisodeId, ...] | list[LearningEpisodeId],
    ) -> frozenset[LearningEpisodeId]:
        ids: set[LearningEpisodeId] = set()
        for cluster in clusters:
            if cluster.learning_episode_id is not None:
                ids.add(cluster.learning_episode_id)
        for pattern in patterns:
            if pattern.learning_episode_id is not None:
                ids.add(pattern.learning_episode_id)
        ids.update(context.episode_ids())
        ids.update(episode_ids)
        return frozenset(ids)

    @staticmethod
    def assert_invalidation_reason(reason: str) -> str:
        return require_non_empty_text(reason, "reason")
