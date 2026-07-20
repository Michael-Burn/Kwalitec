"""EvidenceRecord aggregate root — trustworthy educational observation.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md
Concept
    Evidence Record
"""

from __future__ import annotations

from domain.education.evidence.entities.evidence_context import EvidenceContext
from domain.education.evidence.entities.evidence_item import EvidenceItem
from domain.education.evidence.entities.evidence_source import EvidenceSource
from domain.education.evidence.enums import EvidenceRecordStatus
from domain.education.evidence.events.evidence_recorded import EvidenceRecorded
from domain.education.evidence.events.evidence_updated import EvidenceUpdated
from domain.education.evidence.policies.evidence_consistency_policy import (
    EvidenceConsistencyPolicy,
)
from domain.education.evidence.policies.evidence_validation_policy import (
    EvidenceValidationPolicy,
)
from domain.education.evidence.value_objects.confidence_measure import ConfidenceMeasure
from domain.education.evidence.value_objects.evidence_strength import EvidenceStrength
from domain.education.evidence.value_objects.evidence_timestamp import EvidenceTimestamp
from domain.education.foundation.base import require_non_empty_text
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    ConceptId,
    EvidenceId,
    LearningEpisodeId,
)
from domain.education.foundation.references import ConceptReference

DomainEvent = EvidenceRecorded | EvidenceUpdated


class EvidenceRecord:
    """Aggregate root for educational evidence observations.

    Owns evidence items, source, educational context, confidence, strength,
    concept references, and learning episode references. Behaviour is exposed
    only through methods — no public setters.

    This aggregate records observations only. It does not diagnose, recommend,
    or prioritise learning actions.
    """

    def __init__(
        self,
        evidence_id: EvidenceId,
        student_id: str,
        items: list[EvidenceItem] | tuple[EvidenceItem, ...],
        source: EvidenceSource,
        context: EvidenceContext,
        confidence: ConfidenceMeasure,
        strength: EvidenceStrength,
        timestamp: EvidenceTimestamp,
        *,
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
        status: EvidenceRecordStatus = EvidenceRecordStatus.ACTIVE,
        invalidation_reason: str | None = None,
        _record_created: bool = False,
    ) -> None:
        self._evidence_id = EvidenceValidationPolicy.assert_identity(evidence_id)
        self._student_id = EvidenceValidationPolicy.assert_student_id(student_id)
        self._source = EvidenceValidationPolicy.assert_source(source)
        self._context = EvidenceValidationPolicy.assert_context(context)
        self._confidence = EvidenceValidationPolicy.assert_confidence(confidence)
        self._strength = EvidenceValidationPolicy.assert_strength(strength)
        self._timestamp = EvidenceValidationPolicy.assert_timestamp(timestamp)
        self._items = list(EvidenceValidationPolicy.assert_items(items))
        self._status = EvidenceValidationPolicy.assert_status(status)
        self._invalidation_reason = (
            require_non_empty_text(invalidation_reason, "invalidation_reason")
            if invalidation_reason is not None
            else None
        )

        self._concept_references = list(
            EvidenceValidationPolicy.assert_concept_references(
                concept_references or ()
            )
        )
        self._learning_episode_ids = list(
            EvidenceValidationPolicy.assert_episode_references(
                learning_episode_ids or ()
            )
        )

        # Explicit allow-lists only — referenced identities must already be known.
        self._known_concept_ids: frozenset[ConceptId] = frozenset(
            known_concept_ids or ()
        )
        self._known_episode_ids: frozenset[LearningEpisodeId] = frozenset(
            known_episode_ids or ()
        )

        referenced_concepts = EvidenceValidationPolicy.collect_referenced_concept_ids(
            self._items, self._context, self._concept_references
        )
        EvidenceValidationPolicy.assert_known_concepts(
            self._known_concept_ids, referenced_concepts
        )
        referenced_episodes = EvidenceValidationPolicy.collect_referenced_episode_ids(
            self._items, self._context, self._learning_episode_ids
        )
        EvidenceValidationPolicy.assert_known_episodes(
            self._known_episode_ids, referenced_episodes
        )

        EvidenceConsistencyPolicy.assert_consistent(
            self._source, self._items, self._strength, self._confidence
        )

        self._pending_events: list[DomainEvent] = []
        if _record_created:
            self._pending_events.append(
                EvidenceRecorded(
                    evidence_id=self._evidence_id,
                    student_id=self._student_id,
                    item_count=len(self._items),
                    strength_level=self._strength.level,
                    recorded_at=self._timestamp,
                )
            )

    @classmethod
    def record(
        cls,
        evidence_id: EvidenceId,
        student_id: str,
        items: list[EvidenceItem] | tuple[EvidenceItem, ...],
        source: EvidenceSource,
        context: EvidenceContext,
        confidence: ConfidenceMeasure,
        strength: EvidenceStrength,
        timestamp: EvidenceTimestamp,
        *,
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
    ) -> EvidenceRecord:
        """Factory: record trustworthy educational evidence as observation."""
        return cls(
            evidence_id=evidence_id,
            student_id=student_id,
            items=items,
            source=source,
            context=context,
            confidence=confidence,
            strength=strength,
            timestamp=timestamp,
            known_concept_ids=known_concept_ids,
            known_episode_ids=known_episode_ids,
            concept_references=concept_references,
            learning_episode_ids=learning_episode_ids,
            status=EvidenceRecordStatus.ACTIVE,
            _record_created=True,
        )

    # --- identity / read models (no setters) ---

    @property
    def evidence_id(self) -> EvidenceId:
        return self._evidence_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def items(self) -> tuple[EvidenceItem, ...]:
        return tuple(self._items)

    @property
    def source(self) -> EvidenceSource:
        return self._source

    @property
    def context(self) -> EvidenceContext:
        return self._context

    @property
    def confidence(self) -> ConfidenceMeasure:
        return self._confidence

    @property
    def strength(self) -> EvidenceStrength:
        return self._strength

    @property
    def timestamp(self) -> EvidenceTimestamp:
        return self._timestamp

    @property
    def concept_references(self) -> tuple[ConceptReference, ...]:
        return tuple(self._concept_references)

    @property
    def learning_episode_ids(self) -> tuple[LearningEpisodeId, ...]:
        return tuple(self._learning_episode_ids)

    @property
    def known_concept_ids(self) -> frozenset[ConceptId]:
        return self._known_concept_ids

    @property
    def known_episode_ids(self) -> frozenset[LearningEpisodeId]:
        return self._known_episode_ids

    @property
    def status(self) -> EvidenceRecordStatus:
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

    def amend(
        self,
        *,
        items: list[EvidenceItem] | tuple[EvidenceItem, ...] | None = None,
        confidence: ConfidenceMeasure | None = None,
        strength: EvidenceStrength | None = None,
        timestamp: EvidenceTimestamp | None = None,
    ) -> None:
        """Amend observational detail without diagnosing or recommending."""
        EvidenceValidationPolicy.assert_mutable(self._status, action="amend")
        next_items = (
            list(EvidenceValidationPolicy.assert_items(items))
            if items is not None
            else list(self._items)
        )
        next_confidence = (
            EvidenceValidationPolicy.assert_confidence(confidence)
            if confidence is not None
            else self._confidence
        )
        next_strength = (
            EvidenceValidationPolicy.assert_strength(strength)
            if strength is not None
            else self._strength
        )
        next_timestamp = (
            EvidenceValidationPolicy.assert_timestamp(timestamp)
            if timestamp is not None
            else self._timestamp
        )

        referenced_concepts = EvidenceValidationPolicy.collect_referenced_concept_ids(
            next_items, self._context, self._concept_references
        )
        EvidenceValidationPolicy.assert_known_concepts(
            self._known_concept_ids, referenced_concepts
        )
        referenced_episodes = EvidenceValidationPolicy.collect_referenced_episode_ids(
            next_items, self._context, self._learning_episode_ids
        )
        EvidenceValidationPolicy.assert_known_episodes(
            self._known_episode_ids, referenced_episodes
        )
        EvidenceConsistencyPolicy.assert_consistent(
            self._source, next_items, next_strength, next_confidence
        )

        self._items = next_items
        self._confidence = next_confidence
        self._strength = next_strength
        self._timestamp = next_timestamp
        self._status = EvidenceRecordStatus.AMENDED
        self._pending_events.append(
            EvidenceUpdated(
                evidence_id=self._evidence_id,
                student_id=self._student_id,
                status=self._status,
                change_kind="amend",
            )
        )

    def invalidate(self, reason: str) -> None:
        """Void educational trust in this observation (compensating posture)."""
        EvidenceValidationPolicy.assert_mutable(self._status, action="invalidate")
        self._invalidation_reason = require_non_empty_text(reason, "reason")
        self._status = EvidenceRecordStatus.INVALIDATED
        self._pending_events.append(
            EvidenceUpdated(
                evidence_id=self._evidence_id,
                student_id=self._student_id,
                status=self._status,
                change_kind="invalidate",
            )
        )

    def merge(self, other: EvidenceRecord) -> None:
        """Absorb observationally compatible items from another record.

        ``other`` is marked MERGED. Identical duplicates are rejected.
        """
        EvidenceValidationPolicy.assert_mutable(self._status, action="merge")
        if not isinstance(other, EvidenceRecord):
            raise EducationalInvariantViolation(
                "other must be an EvidenceRecord",
                invariant="EvidenceRecord.merge.type",
            )
        if other.evidence_id == self._evidence_id:
            raise EducationalInvariantViolation(
                "cannot merge an evidence record with itself",
                invariant="EvidenceRecord.merge.self",
            )
        EvidenceValidationPolicy.assert_mutable(other.status, action="merge_into")
        EvidenceConsistencyPolicy.assert_merge_compatible(
            self._student_id,
            other.student_id,
            self._source,
            other.source,
        )

        # Expand known educational identities with other's known set.
        expanded_concepts = set(self._known_concept_ids) | set(other.known_concept_ids)
        expanded_episodes = set(self._known_episode_ids) | set(other.known_episode_ids)
        self._known_concept_ids = frozenset(expanded_concepts)
        self._known_episode_ids = frozenset(expanded_episodes)

        next_items = list(self._items)
        for item in other.items:
            EvidenceValidationPolicy.assert_item_not_duplicate(next_items, item)
            referenced = EvidenceValidationPolicy.collect_referenced_concept_ids(
                (item,), self._context, ()
            )
            EvidenceValidationPolicy.assert_known_concepts(
                self._known_concept_ids, referenced
            )
            referenced_eps = EvidenceValidationPolicy.collect_referenced_episode_ids(
                (item,), self._context, ()
            )
            EvidenceValidationPolicy.assert_known_episodes(
                self._known_episode_ids, referenced_eps
            )
            next_items.append(item)

        EvidenceConsistencyPolicy.assert_consistent(
            self._source, next_items, self._strength, self._confidence
        )
        self._items = next_items

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
        self._pending_events.append(
            EvidenceUpdated(
                evidence_id=self._evidence_id,
                student_id=self._student_id,
                status=self._status,
                change_kind="merge",
            )
        )

    def attach_context(self, context: EvidenceContext) -> None:
        """Attach or replace educational context under known-reference rules."""
        EvidenceValidationPolicy.assert_mutable(self._status, action="attach_context")
        validated = EvidenceValidationPolicy.assert_context(context)
        referenced_concepts = EvidenceValidationPolicy.collect_referenced_concept_ids(
            self._items, validated, self._concept_references
        )
        EvidenceValidationPolicy.assert_known_concepts(
            self._known_concept_ids, referenced_concepts
        )
        referenced_episodes = EvidenceValidationPolicy.collect_referenced_episode_ids(
            self._items, validated, self._learning_episode_ids
        )
        EvidenceValidationPolicy.assert_known_episodes(
            self._known_episode_ids, referenced_episodes
        )
        self._context = validated
        self._pending_events.append(
            EvidenceUpdated(
                evidence_id=self._evidence_id,
                student_id=self._student_id,
                status=self._status,
                change_kind="attach_context",
            )
        )

    def add_item(self, item: EvidenceItem) -> None:
        """Append an observational item when not identical to existing ones."""
        EvidenceValidationPolicy.assert_mutable(self._status, action="add_item")
        EvidenceValidationPolicy.assert_item_not_duplicate(self._items, item)
        referenced = EvidenceValidationPolicy.collect_referenced_concept_ids(
            (item,), self._context, ()
        )
        EvidenceValidationPolicy.assert_known_concepts(
            self._known_concept_ids, referenced
        )
        referenced_eps = EvidenceValidationPolicy.collect_referenced_episode_ids(
            (item,), self._context, ()
        )
        EvidenceValidationPolicy.assert_known_episodes(
            self._known_episode_ids, referenced_eps
        )
        next_items = [*self._items, item]
        EvidenceConsistencyPolicy.assert_consistent(
            self._source, next_items, self._strength, self._confidence
        )
        self._items = next_items
        self._pending_events.append(
            EvidenceUpdated(
                evidence_id=self._evidence_id,
                student_id=self._student_id,
                status=self._status,
                change_kind="add_item",
            )
        )

    def _mark_merged(self) -> None:
        """Internal: mark this record as absorbed by a merge target."""
        EvidenceValidationPolicy.assert_mutable(self._status, action="mark_merged")
        self._status = EvidenceRecordStatus.MERGED
        self._pending_events.append(
            EvidenceUpdated(
                evidence_id=self._evidence_id,
                student_id=self._student_id,
                status=self._status,
                change_kind="merged_away",
            )
        )

    # --- queries ---

    def is_active(self) -> bool:
        return self._status is EvidenceRecordStatus.ACTIVE

    def is_amended(self) -> bool:
        return self._status is EvidenceRecordStatus.AMENDED

    def is_invalidated(self) -> bool:
        return self._status is EvidenceRecordStatus.INVALIDATED

    def is_merged(self) -> bool:
        return self._status is EvidenceRecordStatus.MERGED

    def has_concept(self, concept_id: ConceptId) -> bool:
        if concept_id in self._context.concept_ids():
            return True
        if any(ref.concept_id == concept_id for ref in self._concept_references):
            return True
        return any(item.concept_id == concept_id for item in self._items)

    def has_learning_episode(self, episode_id: LearningEpisodeId) -> bool:
        if episode_id in self._learning_episode_ids:
            return True
        if episode_id in self._context.episode_ids():
            return True
        return any(item.learning_episode_id == episode_id for item in self._items)

    def item_count(self) -> int:
        return len(self._items)

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, EvidenceRecord):
            return NotImplemented
        return self._evidence_id == other._evidence_id

    def __hash__(self) -> int:
        return hash((type(self), self._evidence_id))

    def __repr__(self) -> str:
        return (
            f"EvidenceRecord(evidence_id={self._evidence_id!r}, "
            f"status={self._status!r})"
        )
