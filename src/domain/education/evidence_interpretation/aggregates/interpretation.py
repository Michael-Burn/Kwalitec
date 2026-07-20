"""Interpretation aggregate root — interpreted educational patterns.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md
Concept
    Interpretation
"""

from __future__ import annotations

from domain.education.evidence_interpretation.entities.evidence_cluster import (
    EvidenceCluster,
)
from domain.education.evidence_interpretation.entities.interpretation_context import (
    InterpretationContext,
)
from domain.education.evidence_interpretation.entities.interpreted_pattern import (
    InterpretedPattern,
)
from domain.education.evidence_interpretation.enums import (
    InterpretationStatus,
    PatternKind,
)
from domain.education.evidence_interpretation.events.interpretation_created import (
    InterpretationCreated,
)
from domain.education.evidence_interpretation.policies.clustering_policy import (
    ClusteringPolicy,
)
from domain.education.evidence_interpretation.policies.interpretation_validation_policy import (  # noqa: E501
    InterpretationId,
    InterpretationValidationPolicy,
)
from domain.education.evidence_interpretation.value_objects.interpretation_confidence import (  # noqa: E501
    InterpretationConfidence,
)
from domain.education.evidence_interpretation.value_objects.interpretation_summary import (  # noqa: E501
    InterpretationSummary,
)
from domain.education.foundation.base import require_non_empty_text
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    ConceptId,
    EvidenceId,
    LearningEpisodeId,
)
from domain.education.foundation.references import ConceptReference

DomainEvent = InterpretationCreated


class Interpretation:
    """Aggregate root for educational evidence interpretation.

    Owns evidence clusters, interpreted patterns, interpretation confidence,
    educational context, concept references, and learning episode references.
    Behaviour is exposed only through methods — no public setters.

    This aggregate produces interpreted educational observations only. It does
    not diagnose, recommend, or prioritise learning actions.
    """

    def __init__(
        self,
        interpretation_id: InterpretationId,
        student_id: str,
        clusters: list[EvidenceCluster] | tuple[EvidenceCluster, ...],
        patterns: list[InterpretedPattern] | tuple[InterpretedPattern, ...],
        context: InterpretationContext,
        confidence: InterpretationConfidence,
        summary: InterpretationSummary,
        *,
        known_evidence_ids: frozenset[EvidenceId]
        | set[EvidenceId]
        | tuple[EvidenceId, ...]
        | None = None,
        known_concept_ids: frozenset[ConceptId]
        | set[ConceptId]
        | tuple[ConceptId, ...]
        | None = None,
        known_episode_ids: frozenset[LearningEpisodeId]
        | set[LearningEpisodeId]
        | tuple[LearningEpisodeId, ...]
        | None = None,
        concept_references: list[ConceptReference]
        | tuple[ConceptReference, ...]
        | None = None,
        learning_episode_ids: list[LearningEpisodeId]
        | tuple[LearningEpisodeId, ...]
        | None = None,
        status: InterpretationStatus = InterpretationStatus.ACTIVE,
        invalidation_reason: str | None = None,
        _record_created: bool = False,
    ) -> None:
        self._interpretation_id = InterpretationValidationPolicy.assert_identity(
            interpretation_id
        )
        self._student_id = InterpretationValidationPolicy.assert_student_id(student_id)
        self._context = InterpretationValidationPolicy.assert_context(context)
        self._confidence = InterpretationValidationPolicy.assert_confidence(confidence)
        self._summary = InterpretationValidationPolicy.assert_summary(summary)
        self._clusters = list(InterpretationValidationPolicy.assert_clusters(clusters))
        self._patterns = list(InterpretationValidationPolicy.assert_patterns(patterns))
        self._status = InterpretationValidationPolicy.assert_status(status)
        self._invalidation_reason = (
            require_non_empty_text(invalidation_reason, "invalidation_reason")
            if invalidation_reason is not None
            else None
        )

        self._concept_references = list(
            InterpretationValidationPolicy.assert_concept_references(
                concept_references or ()
            )
        )
        self._learning_episode_ids = list(
            InterpretationValidationPolicy.assert_episode_references(
                learning_episode_ids or ()
            )
        )

        self._known_evidence_ids: frozenset[EvidenceId] = frozenset(
            known_evidence_ids or ()
        )
        self._known_concept_ids: frozenset[ConceptId] = frozenset(
            known_concept_ids or ()
        )
        self._known_episode_ids: frozenset[LearningEpisodeId] = frozenset(
            known_episode_ids or ()
        )

        referenced_evidence = InterpretationValidationPolicy.assert_references_evidence(
            self._clusters, self._patterns
        )
        InterpretationValidationPolicy.assert_known_evidence(
            self._known_evidence_ids, referenced_evidence
        )

        referenced_concepts = (
            InterpretationValidationPolicy.collect_referenced_concept_ids(
                self._clusters,
                self._patterns,
                self._context,
                self._concept_references,
            )
        )
        InterpretationValidationPolicy.assert_known_concepts(
            self._known_concept_ids, referenced_concepts
        )
        referenced_episodes = (
            InterpretationValidationPolicy.collect_referenced_episode_ids(
                self._clusters,
                self._patterns,
                self._context,
                self._learning_episode_ids,
            )
        )
        InterpretationValidationPolicy.assert_known_episodes(
            self._known_episode_ids, referenced_episodes
        )

        InterpretationValidationPolicy.assert_summary_counts(
            self._summary, self._patterns, self._clusters
        )
        ClusteringPolicy.assert_consistent(
            self._clusters, self._patterns, self._confidence
        )

        self._pending_events: list[DomainEvent] = []
        if _record_created:
            self._pending_events.append(
                InterpretationCreated(
                    interpretation_id=self._interpretation_id,
                    student_id=self._student_id,
                    pattern_count=len(self._patterns),
                    cluster_count=len(self._clusters),
                    confidence_level=self._confidence.level,
                )
            )

    @classmethod
    def interpret(
        cls,
        interpretation_id: InterpretationId,
        student_id: str,
        clusters: list[EvidenceCluster] | tuple[EvidenceCluster, ...],
        patterns: list[InterpretedPattern] | tuple[InterpretedPattern, ...],
        context: InterpretationContext,
        confidence: InterpretationConfidence,
        summary: InterpretationSummary,
        *,
        known_evidence_ids: frozenset[EvidenceId]
        | set[EvidenceId]
        | tuple[EvidenceId, ...]
        | None = None,
        known_concept_ids: frozenset[ConceptId]
        | set[ConceptId]
        | tuple[ConceptId, ...]
        | None = None,
        known_episode_ids: frozenset[LearningEpisodeId]
        | set[LearningEpisodeId]
        | tuple[LearningEpisodeId, ...]
        | None = None,
        concept_references: list[ConceptReference]
        | tuple[ConceptReference, ...]
        | None = None,
        learning_episode_ids: list[LearningEpisodeId]
        | tuple[LearningEpisodeId, ...]
        | None = None,
    ) -> Interpretation:
        """Factory: interpret educational evidence into observational patterns."""
        return cls(
            interpretation_id=interpretation_id,
            student_id=student_id,
            clusters=clusters,
            patterns=patterns,
            context=context,
            confidence=confidence,
            summary=summary,
            known_evidence_ids=known_evidence_ids,
            known_concept_ids=known_concept_ids,
            known_episode_ids=known_episode_ids,
            concept_references=concept_references,
            learning_episode_ids=learning_episode_ids,
            status=InterpretationStatus.ACTIVE,
            _record_created=True,
        )

    # --- identity / read models (no setters) ---

    @property
    def interpretation_id(self) -> InterpretationId:
        return self._interpretation_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def clusters(self) -> tuple[EvidenceCluster, ...]:
        return tuple(self._clusters)

    @property
    def patterns(self) -> tuple[InterpretedPattern, ...]:
        return tuple(self._patterns)

    @property
    def context(self) -> InterpretationContext:
        return self._context

    @property
    def confidence(self) -> InterpretationConfidence:
        return self._confidence

    @property
    def summary(self) -> InterpretationSummary:
        return self._summary

    @property
    def concept_references(self) -> tuple[ConceptReference, ...]:
        return tuple(self._concept_references)

    @property
    def learning_episode_ids(self) -> tuple[LearningEpisodeId, ...]:
        return tuple(self._learning_episode_ids)

    @property
    def known_evidence_ids(self) -> frozenset[EvidenceId]:
        return self._known_evidence_ids

    @property
    def known_concept_ids(self) -> frozenset[ConceptId]:
        return self._known_concept_ids

    @property
    def known_episode_ids(self) -> frozenset[LearningEpisodeId]:
        return self._known_episode_ids

    @property
    def status(self) -> InterpretationStatus:
        return self._status

    @property
    def invalidation_reason(self) -> str | None:
        return self._invalidation_reason

    def pull_events(self) -> list[DomainEvent]:
        """Return and clear pending domain events."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    # --- behaviour ---

    def revise(
        self,
        *,
        patterns: list[InterpretedPattern]
        | tuple[InterpretedPattern, ...]
        | None = None,
        clusters: list[EvidenceCluster] | tuple[EvidenceCluster, ...] | None = None,
        confidence: InterpretationConfidence | None = None,
        summary: InterpretationSummary | None = None,
        context: InterpretationContext | None = None,
    ) -> None:
        """Revise interpretive detail without diagnosing or recommending."""
        InterpretationValidationPolicy.assert_mutable(self._status, action="revise")
        next_patterns = (
            list(InterpretationValidationPolicy.assert_patterns(patterns))
            if patterns is not None
            else list(self._patterns)
        )
        next_clusters = (
            list(InterpretationValidationPolicy.assert_clusters(clusters))
            if clusters is not None
            else list(self._clusters)
        )
        next_confidence = (
            InterpretationValidationPolicy.assert_confidence(confidence)
            if confidence is not None
            else self._confidence
        )
        next_context = (
            InterpretationValidationPolicy.assert_context(context)
            if context is not None
            else self._context
        )
        next_summary = (
            InterpretationValidationPolicy.assert_summary(summary)
            if summary is not None
            else InterpretationSummary.of(
                self._summary.text,
                pattern_count=len(next_patterns),
                cluster_count=len(next_clusters),
            )
        )

        referenced_evidence = InterpretationValidationPolicy.assert_references_evidence(
            next_clusters, next_patterns
        )
        InterpretationValidationPolicy.assert_known_evidence(
            self._known_evidence_ids, referenced_evidence
        )
        referenced_concepts = (
            InterpretationValidationPolicy.collect_referenced_concept_ids(
                next_clusters,
                next_patterns,
                next_context,
                self._concept_references,
            )
        )
        InterpretationValidationPolicy.assert_known_concepts(
            self._known_concept_ids, referenced_concepts
        )
        referenced_episodes = (
            InterpretationValidationPolicy.collect_referenced_episode_ids(
                next_clusters,
                next_patterns,
                next_context,
                self._learning_episode_ids,
            )
        )
        InterpretationValidationPolicy.assert_known_episodes(
            self._known_episode_ids, referenced_episodes
        )
        InterpretationValidationPolicy.assert_summary_counts(
            next_summary, next_patterns, next_clusters
        )
        ClusteringPolicy.assert_consistent(
            next_clusters, next_patterns, next_confidence
        )

        self._patterns = next_patterns
        self._clusters = next_clusters
        self._confidence = next_confidence
        self._context = next_context
        self._summary = next_summary
        self._status = InterpretationStatus.REVISED

    def invalidate(self, reason: str) -> None:
        """Void interpretive trust in this pattern set (compensating posture)."""
        InterpretationValidationPolicy.assert_mutable(self._status, action="invalidate")
        self._invalidation_reason = (
            InterpretationValidationPolicy.assert_invalidation_reason(reason)
        )
        self._status = InterpretationStatus.INVALIDATED

    def merge(self, other: Interpretation) -> None:
        """Absorb observationally compatible clusters and patterns from another.

        ``other`` is marked MERGED. Identical duplicate patterns are rejected.
        """
        InterpretationValidationPolicy.assert_mutable(self._status, action="merge")
        if not isinstance(other, Interpretation):
            raise EducationalInvariantViolation(
                "other must be an Interpretation",
                invariant="Interpretation.merge.type",
            )
        if other.interpretation_id == self._interpretation_id:
            raise EducationalInvariantViolation(
                "cannot merge an interpretation with itself",
                invariant="Interpretation.merge.self",
            )
        InterpretationValidationPolicy.assert_mutable(
            other.status, action="merge_into"
        )
        ClusteringPolicy.assert_merge_compatible(self._student_id, other.student_id)

        expanded_evidence = set(self._known_evidence_ids) | set(
            other.known_evidence_ids
        )
        expanded_concepts = set(self._known_concept_ids) | set(other.known_concept_ids)
        expanded_episodes = set(self._known_episode_ids) | set(other.known_episode_ids)
        self._known_evidence_ids = frozenset(expanded_evidence)
        self._known_concept_ids = frozenset(expanded_concepts)
        self._known_episode_ids = frozenset(expanded_episodes)

        next_clusters = list(self._clusters)
        for cluster in other.clusters:
            already = any(
                existing.cluster_id == cluster.cluster_id
                or existing.cluster_signature() == cluster.cluster_signature()
                for existing in next_clusters
            )
            if not already:
                next_clusters.append(cluster)

        next_patterns = list(self._patterns)
        for pattern in other.patterns:
            InterpretationValidationPolicy.assert_pattern_not_duplicate(
                next_patterns, pattern
            )
            next_patterns.append(pattern)

        referenced_evidence = InterpretationValidationPolicy.assert_references_evidence(
            next_clusters, next_patterns
        )
        InterpretationValidationPolicy.assert_known_evidence(
            self._known_evidence_ids, referenced_evidence
        )
        referenced_concepts = (
            InterpretationValidationPolicy.collect_referenced_concept_ids(
                next_clusters,
                next_patterns,
                self._context,
                self._concept_references,
            )
        )
        InterpretationValidationPolicy.assert_known_concepts(
            self._known_concept_ids, referenced_concepts
        )
        referenced_episodes = (
            InterpretationValidationPolicy.collect_referenced_episode_ids(
                next_clusters,
                next_patterns,
                self._context,
                self._learning_episode_ids,
            )
        )
        InterpretationValidationPolicy.assert_known_episodes(
            self._known_episode_ids, referenced_episodes
        )
        ClusteringPolicy.assert_consistent(
            next_clusters, next_patterns, self._confidence
        )

        self._clusters = next_clusters
        self._patterns = next_patterns
        self._summary = InterpretationSummary.of(
            self._summary.text,
            pattern_count=len(self._patterns),
            cluster_count=len(self._clusters),
        )

        for ref in other.concept_references:
            already = any(
                existing.concept_id == ref.concept_id
                for existing in self._concept_references
            )
            if not already:
                self._concept_references.append(ref)
        for episode_id in other.learning_episode_ids:
            if episode_id not in self._learning_episode_ids:
                self._learning_episode_ids.append(episode_id)

        other._mark_merged()

    def _mark_merged(self) -> None:
        """Internal: mark this interpretation as absorbed by a merge target."""
        InterpretationValidationPolicy.assert_mutable(
            self._status, action="mark_merged"
        )
        self._status = InterpretationStatus.MERGED

    # --- queries ---

    def is_active(self) -> bool:
        return self._status is InterpretationStatus.ACTIVE

    def is_revised(self) -> bool:
        return self._status is InterpretationStatus.REVISED

    def is_invalidated(self) -> bool:
        return self._status is InterpretationStatus.INVALIDATED

    def is_merged(self) -> bool:
        return self._status is InterpretationStatus.MERGED

    def has_concept(self, concept_id: ConceptId) -> bool:
        if concept_id in self._context.concept_ids():
            return True
        if any(ref.concept_id == concept_id for ref in self._concept_references):
            return True
        if any(c.concept_id == concept_id for c in self._clusters):
            return True
        return any(p.concept_id == concept_id for p in self._patterns)

    def has_learning_episode(self, episode_id: LearningEpisodeId) -> bool:
        if episode_id in self._learning_episode_ids:
            return True
        if episode_id in self._context.episode_ids():
            return True
        if any(c.learning_episode_id == episode_id for c in self._clusters):
            return True
        return any(p.learning_episode_id == episode_id for p in self._patterns)

    def has_evidence(self, evidence_id: EvidenceId) -> bool:
        return evidence_id in self.referenced_evidence_ids()

    def referenced_evidence_ids(self) -> frozenset[EvidenceId]:
        ids: set[EvidenceId] = set()
        for cluster in self._clusters:
            ids.update(cluster.evidence_ids)
        for pattern in self._patterns:
            ids.update(pattern.evidence_ids)
        return frozenset(ids)

    def pattern_count(self) -> int:
        return len(self._patterns)

    def cluster_count(self) -> int:
        return len(self._clusters)

    def patterns_of_kind(self, kind: PatternKind) -> tuple[InterpretedPattern, ...]:
        return tuple(p for p in self._patterns if p.kind is kind)

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, Interpretation):
            return NotImplemented
        return self._interpretation_id == other._interpretation_id

    def __hash__(self) -> int:
        return hash((type(self), self._interpretation_id))

    def __repr__(self) -> str:
        return (
            f"Interpretation(interpretation_id={self._interpretation_id!r}, "
            f"status={self._status!r})"
        )
