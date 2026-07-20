"""Policy governing EvidenceRecord construction and identity integrity.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md
Concept
    Evidence Validation Policy
"""

from __future__ import annotations

from domain.education.evidence.entities.evidence_context import EvidenceContext
from domain.education.evidence.entities.evidence_item import EvidenceItem
from domain.education.evidence.entities.evidence_source import EvidenceSource
from domain.education.evidence.enums import EvidenceRecordStatus
from domain.education.evidence.value_objects.confidence_measure import ConfidenceMeasure
from domain.education.evidence.value_objects.evidence_strength import EvidenceStrength
from domain.education.evidence.value_objects.evidence_timestamp import EvidenceTimestamp
from domain.education.foundation.base import require_identity_value
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    ConceptId,
    EvidenceId,
    LearningEpisodeId,
)
from domain.education.foundation.references import ConceptReference


class EvidenceValidationPolicy:
    """Enforces EvidenceRecord identity, ownership, and observational invariants."""

    @staticmethod
    def assert_identity(evidence_id: EvidenceId) -> EvidenceId:
        if not isinstance(evidence_id, EvidenceId):
            raise EducationalInvariantViolation(
                "evidence must possess an EvidenceId identity",
                invariant="EvidenceRecord.identity.required",
            )
        return evidence_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_source(source: EvidenceSource) -> EvidenceSource:
        if not isinstance(source, EvidenceSource):
            raise EducationalInvariantViolation(
                "evidence must identify its source",
                invariant="EvidenceRecord.source.required",
            )
        return source

    @staticmethod
    def assert_context(context: EvidenceContext) -> EvidenceContext:
        if not isinstance(context, EvidenceContext):
            raise EducationalInvariantViolation(
                "evidence must identify its educational context",
                invariant="EvidenceRecord.context.required",
            )
        return context

    @staticmethod
    def assert_confidence(confidence: ConfidenceMeasure) -> ConfidenceMeasure:
        if not isinstance(confidence, ConfidenceMeasure):
            raise EducationalInvariantViolation(
                "evidence must possess confidence",
                invariant="EvidenceRecord.confidence.required",
            )
        return confidence

    @staticmethod
    def assert_strength(strength: EvidenceStrength) -> EvidenceStrength:
        if not isinstance(strength, EvidenceStrength):
            raise EducationalInvariantViolation(
                "evidence must possess strength",
                invariant="EvidenceRecord.strength.required",
            )
        return strength

    @staticmethod
    def assert_timestamp(timestamp: EvidenceTimestamp) -> EvidenceTimestamp:
        if not isinstance(timestamp, EvidenceTimestamp):
            raise EducationalInvariantViolation(
                "evidence must possess a timestamp",
                invariant="EvidenceRecord.timestamp.required",
            )
        return timestamp

    @staticmethod
    def assert_items(
        items: tuple[EvidenceItem, ...] | list[EvidenceItem],
    ) -> tuple[EvidenceItem, ...]:
        """Evidence must have at least one evidence item; no identical duplicates."""
        collected = tuple(items)
        if not collected:
            raise EducationalInvariantViolation(
                "evidence must have at least one evidence item",
                invariant="EvidenceRecord.items.min_one",
            )
        seen_ids: set[str] = set()
        seen_signatures: set[tuple[str, str, str | None, str | None]] = set()
        for item in collected:
            if not isinstance(item, EvidenceItem):
                raise EducationalInvariantViolation(
                    "items must be EvidenceItem entities",
                    invariant="EvidenceRecord.items.type",
                )
            if item.item_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate evidence item identity is not allowed",
                    invariant="EvidenceRecord.items.no_duplicate_id",
                )
            signature = item.observational_signature()
            if signature in seen_signatures:
                raise EducationalInvariantViolation(
                    "identical evidence must not be duplicated",
                    invariant="EvidenceRecord.items.no_identical_duplicate",
                )
            seen_ids.add(item.item_id.value)
            seen_signatures.add(signature)
        return collected

    @staticmethod
    def assert_item_not_duplicate(
        existing: tuple[EvidenceItem, ...] | list[EvidenceItem],
        candidate: EvidenceItem,
    ) -> None:
        if not isinstance(candidate, EvidenceItem):
            raise EducationalInvariantViolation(
                "candidate must be an EvidenceItem",
                invariant="EvidenceRecord.items.candidate_type",
            )
        for item in existing:
            if item.item_id == candidate.item_id:
                raise EducationalInvariantViolation(
                    "duplicate evidence item identity is not allowed",
                    invariant="EvidenceRecord.items.no_duplicate_id",
                )
            if item.observational_signature() == candidate.observational_signature():
                raise EducationalInvariantViolation(
                    "identical evidence must not be duplicated",
                    invariant="EvidenceRecord.items.no_identical_duplicate",
                )

    @staticmethod
    def assert_known_concepts(
        known: frozenset[ConceptId] | set[ConceptId] | tuple[ConceptId, ...],
        concept_ids: frozenset[ConceptId] | set[ConceptId] | tuple[ConceptId, ...],
    ) -> None:
        """Never reference unknown concepts."""
        known_set = frozenset(known)
        for concept_id in concept_ids:
            if not isinstance(concept_id, ConceptId):
                raise EducationalInvariantViolation(
                    "concept references must use ConceptId",
                    invariant="EvidenceRecord.concepts.type",
                )
            if concept_id not in known_set:
                raise EducationalInvariantViolation(
                    f"unknown concept referenced: {concept_id.value}",
                    invariant="EvidenceRecord.concepts.known",
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
        """Never reference unknown learning episodes."""
        known_set = frozenset(known)
        for episode_id in episode_ids:
            if not isinstance(episode_id, LearningEpisodeId):
                raise EducationalInvariantViolation(
                    "episode references must use LearningEpisodeId",
                    invariant="EvidenceRecord.episodes.type",
                )
            if episode_id not in known_set:
                raise EducationalInvariantViolation(
                    f"unknown learning episode referenced: {episode_id.value}",
                    invariant="EvidenceRecord.episodes.known",
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
                    invariant="EvidenceRecord.concept_references.type",
                )
            if ref.concept_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate concept reference is not allowed",
                    invariant="EvidenceRecord.concept_references.no_duplicate",
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
                    invariant="EvidenceRecord.learning_episode_ids.type",
                )
            if episode_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate learning episode reference is not allowed",
                    invariant="EvidenceRecord.learning_episode_ids.no_duplicate",
                )
            seen.add(episode_id.value)
        return items

    @staticmethod
    def assert_status(status: EvidenceRecordStatus) -> EvidenceRecordStatus:
        if not isinstance(status, EvidenceRecordStatus):
            raise EducationalInvariantViolation(
                "status must be an EvidenceRecordStatus",
                invariant="EvidenceRecord.status.type",
            )
        return status

    @staticmethod
    def assert_mutable(status: EvidenceRecordStatus, *, action: str) -> None:
        if status is EvidenceRecordStatus.INVALIDATED:
            raise EducationalInvariantViolation(
                f"cannot {action} an invalidated evidence record",
                invariant="EvidenceRecord.mutable.invalidated",
            )
        if status is EvidenceRecordStatus.MERGED:
            raise EducationalInvariantViolation(
                f"cannot {action} a merged evidence record",
                invariant="EvidenceRecord.mutable.merged",
            )

    @staticmethod
    def collect_referenced_concept_ids(
        items: tuple[EvidenceItem, ...] | list[EvidenceItem],
        context: EvidenceContext,
        concept_references: tuple[ConceptReference, ...] | list[ConceptReference],
    ) -> frozenset[ConceptId]:
        ids: set[ConceptId] = set()
        for item in items:
            if item.concept_id is not None:
                ids.add(item.concept_id)
        ids.update(context.concept_ids())
        for ref in concept_references:
            ids.add(ref.concept_id)
        return frozenset(ids)

    @staticmethod
    def collect_referenced_episode_ids(
        items: tuple[EvidenceItem, ...] | list[EvidenceItem],
        context: EvidenceContext,
        episode_ids: tuple[LearningEpisodeId, ...] | list[LearningEpisodeId],
    ) -> frozenset[LearningEpisodeId]:
        ids: set[LearningEpisodeId] = set()
        for item in items:
            if item.learning_episode_id is not None:
                ids.add(item.learning_episode_id)
        ids.update(context.episode_ids())
        ids.update(episode_ids)
        return frozenset(ids)
