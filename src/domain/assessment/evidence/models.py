"""Immutable educational evidence packaging models (Assessment Engine).

Observations are facts. Evidence is organised facts. Inference is forbidden here.

Architecture Source
    knowledge/product/AP-002/EVIDENCE_MODEL.md
    knowledge/product/AP-002/SCORING_MODEL.md
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any

from domain.assessment.enums import AttemptOutcome, EvidenceSource, ObservationKind
from domain.assessment.evidence.ids import EvidenceBundleId, EvidenceItemId
from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.assessment.value_objects.evidence_dimensions import EvidenceDimensions
from domain.assessment.value_objects.ids import (
    InstrumentId,
    ObservationId,
    QuestionId,
    ResultId,
    SessionId,
)
from domain.assessment.value_objects.levels import EvidenceStrength
from domain.assessment.value_objects.references import (
    ConceptReference,
    LearningObjectiveReference,
)
from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_non_empty_text,
)

PACKAGING_VERSION = "AP-002C.1"


@dataclass(frozen=True, slots=True)
class EvidenceReference(EducationalValueObject):
    """Traceability link from packaged evidence back to an observation."""

    observation_id: ObservationId
    question_id: QuestionId | None = None
    kind: ObservationKind | None = None

    def _validate(self) -> None:
        if not isinstance(self.observation_id, ObservationId):
            raise AssessmentInvariantViolation(
                "observation_id must be an ObservationId",
                invariant="EvidenceReference.observation_id.type",
            )
        if self.question_id is not None and not isinstance(
            self.question_id, QuestionId
        ):
            raise AssessmentInvariantViolation(
                "question_id must be a QuestionId when provided",
                invariant="EvidenceReference.question_id.type",
            )
        if self.kind is not None and not isinstance(self.kind, ObservationKind):
            raise AssessmentInvariantViolation(
                "kind must be an ObservationKind when provided",
                invariant="EvidenceReference.kind.type",
            )


@dataclass(frozen=True, slots=True)
class EvidenceContext(EducationalValueObject):
    """Session / instrument context for packaged evidence (no learner state)."""

    session_id: SessionId
    instrument_id: InstrumentId | None = None
    assessment_id: str | None = None
    purpose: str | None = None
    assessment_type: str | None = None
    student_id: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.session_id, SessionId):
            raise AssessmentInvariantViolation(
                "session_id must be a SessionId",
                invariant="EvidenceContext.session_id.type",
            )
        if self.instrument_id is not None and not isinstance(
            self.instrument_id, InstrumentId
        ):
            raise AssessmentInvariantViolation(
                "instrument_id must be an InstrumentId when provided",
                invariant="EvidenceContext.instrument_id.type",
            )
        if self.assessment_id is not None:
            object.__setattr__(
                self,
                "assessment_id",
                require_non_empty_text(self.assessment_id, "assessment_id"),
            )
        if self.purpose is not None:
            object.__setattr__(
                self, "purpose", require_non_empty_text(self.purpose, "purpose")
            )
        if self.assessment_type is not None:
            object.__setattr__(
                self,
                "assessment_type",
                require_non_empty_text(self.assessment_type, "assessment_type"),
            )
        if self.student_id is not None:
            object.__setattr__(
                self,
                "student_id",
                require_non_empty_text(self.student_id, "student_id"),
            )


@dataclass(frozen=True, slots=True)
class EvidenceMetadata(EducationalValueObject):
    """Provenance metadata for an evidence bundle (packaging facts only)."""

    evidence_source: EvidenceSource
    packaging_version: str = PACKAGING_VERSION
    collected_at: datetime | None = None
    question_ids: tuple[QuestionId, ...] = ()
    learning_objectives: tuple[LearningObjectiveReference, ...] = ()
    concepts: tuple[ConceptReference, ...] = ()
    extra: Mapping[str, Any] = MappingProxyType({})

    def _validate(self) -> None:
        if not isinstance(self.evidence_source, EvidenceSource):
            raise AssessmentInvariantViolation(
                "evidence_source must be an EvidenceSource",
                invariant="EvidenceMetadata.evidence_source.type",
            )
        object.__setattr__(
            self,
            "packaging_version",
            require_non_empty_text(self.packaging_version, "packaging_version"),
        )
        if self.collected_at is not None and not isinstance(
            self.collected_at, datetime
        ):
            raise AssessmentInvariantViolation(
                "collected_at must be a datetime when provided",
                invariant="EvidenceMetadata.collected_at.type",
            )
        qids: list[QuestionId] = []
        seen_q: set[str] = set()
        for qid in self.question_ids or ():
            if not isinstance(qid, QuestionId):
                raise AssessmentInvariantViolation(
                    "question_ids must contain QuestionId values",
                    invariant="EvidenceMetadata.question_ids.type",
                )
            if qid.value in seen_q:
                raise AssessmentInvariantViolation(
                    "duplicate question_id in EvidenceMetadata",
                    invariant="EvidenceMetadata.question_ids.unique",
                )
            seen_q.add(qid.value)
            qids.append(qid)
        object.__setattr__(self, "question_ids", tuple(qids))

        objectives: list[LearningObjectiveReference] = []
        for obj in self.learning_objectives or ():
            if not isinstance(obj, LearningObjectiveReference):
                raise AssessmentInvariantViolation(
                    "learning_objectives must contain LearningObjectiveReference",
                    invariant="EvidenceMetadata.learning_objectives.type",
                )
            objectives.append(obj)
        object.__setattr__(self, "learning_objectives", tuple(objectives))

        concepts: list[ConceptReference] = []
        for concept in self.concepts or ():
            if not isinstance(concept, ConceptReference):
                raise AssessmentInvariantViolation(
                    "concepts must contain ConceptReference",
                    invariant="EvidenceMetadata.concepts.type",
                )
            concepts.append(concept)
        object.__setattr__(self, "concepts", tuple(concepts))
        object.__setattr__(
            self, "extra", MappingProxyType(dict(self.extra or {}))
        )


@dataclass(frozen=True, slots=True)
class EvidenceSummary(EducationalValueObject):
    """Evidence-only rollup counts (not a grade or mastery estimate)."""

    observation_count: int
    question_observation_count: int
    distinct_question_count: int
    correctness_counts: tuple[tuple[AttemptOutcome, int], ...] = ()
    hint_total: int = 0
    retry_total: int = 0
    confidence_supplied_count: int = 0
    timing_available_count: int = 0
    misconception_tag_count: int = 0

    def _validate(self) -> None:
        for name, value in (
            ("observation_count", self.observation_count),
            ("question_observation_count", self.question_observation_count),
            ("distinct_question_count", self.distinct_question_count),
            ("hint_total", self.hint_total),
            ("retry_total", self.retry_total),
            ("confidence_supplied_count", self.confidence_supplied_count),
            ("timing_available_count", self.timing_available_count),
            ("misconception_tag_count", self.misconception_tag_count),
        ):
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or value < 0
            ):
                raise AssessmentInvariantViolation(
                    f"{name} must be a non-negative integer",
                    invariant=f"EvidenceSummary.{name}.range",
                )
        counts: list[tuple[AttemptOutcome, int]] = []
        for key, value in self.correctness_counts or ():
            if not isinstance(key, AttemptOutcome):
                raise AssessmentInvariantViolation(
                    "correctness_counts keys must be AttemptOutcome",
                    invariant="EvidenceSummary.correctness_counts.key",
                )
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise AssessmentInvariantViolation(
                    "correctness_counts values must be non-negative integers",
                    invariant="EvidenceSummary.correctness_counts.value",
                )
            counts.append((key, value))
        object.__setattr__(self, "correctness_counts", tuple(counts))

    def correctness_count_map(self) -> dict[AttemptOutcome, int]:
        return dict(self.correctness_counts)


@dataclass(frozen=True, slots=True, eq=False)
class EvidenceItem(EducationalEntity):
    """One packaged evidence unit with full observation traceability."""

    item_id: EvidenceItemId
    reference: EvidenceReference
    kind: ObservationKind
    evidence_source: EvidenceSource
    dimensions: EvidenceDimensions | None = None
    provenance: Mapping[str, Any] = MappingProxyType({})

    @property
    def entity_id(self) -> EvidenceItemId:
        return self.item_id

    def _validate(self) -> None:
        if not isinstance(self.item_id, EvidenceItemId):
            raise AssessmentInvariantViolation(
                "item_id must be an EvidenceItemId",
                invariant="EvidenceItem.item_id.type",
            )
        if not isinstance(self.reference, EvidenceReference):
            raise AssessmentInvariantViolation(
                "reference must be an EvidenceReference",
                invariant="EvidenceItem.reference.type",
            )
        if not isinstance(self.kind, ObservationKind):
            raise AssessmentInvariantViolation(
                "kind must be an ObservationKind",
                invariant="EvidenceItem.kind.type",
            )
        if not isinstance(self.evidence_source, EvidenceSource):
            raise AssessmentInvariantViolation(
                "evidence_source must be an EvidenceSource",
                invariant="EvidenceItem.evidence_source.type",
            )
        if self.dimensions is not None and not isinstance(
            self.dimensions, EvidenceDimensions
        ):
            raise AssessmentInvariantViolation(
                "dimensions must be EvidenceDimensions when provided",
                invariant="EvidenceItem.dimensions.type",
            )
        object.__setattr__(
            self, "provenance", MappingProxyType(dict(self.provenance or {}))
        )


@dataclass(frozen=True, slots=True, eq=False)
class EvidenceBundle(EducationalEntity):
    """Immutable organised observation facts for a completed assessment session.

    Does not estimate mastery, update the Twin, or invoke Reasoning.
    """

    bundle_id: EvidenceBundleId
    context: EvidenceContext
    metadata: EvidenceMetadata
    summary: EvidenceSummary
    strength: EvidenceStrength
    items: tuple[EvidenceItem, ...] = ()

    @property
    def entity_id(self) -> EvidenceBundleId:
        return self.bundle_id

    def _validate(self) -> None:
        if not isinstance(self.bundle_id, EvidenceBundleId):
            raise AssessmentInvariantViolation(
                "bundle_id must be an EvidenceBundleId",
                invariant="EvidenceBundle.bundle_id.type",
            )
        if not isinstance(self.context, EvidenceContext):
            raise AssessmentInvariantViolation(
                "context must be an EvidenceContext",
                invariant="EvidenceBundle.context.type",
            )
        if not isinstance(self.metadata, EvidenceMetadata):
            raise AssessmentInvariantViolation(
                "metadata must be an EvidenceMetadata",
                invariant="EvidenceBundle.metadata.type",
            )
        if not isinstance(self.summary, EvidenceSummary):
            raise AssessmentInvariantViolation(
                "summary must be an EvidenceSummary",
                invariant="EvidenceBundle.summary.type",
            )
        if not isinstance(self.strength, EvidenceStrength):
            raise AssessmentInvariantViolation(
                "strength must be an EvidenceStrength",
                invariant="EvidenceBundle.strength.type",
            )
        items: list[EvidenceItem] = []
        seen_items: set[str] = set()
        seen_obs: set[str] = set()
        for item in self.items or ():
            if not isinstance(item, EvidenceItem):
                raise AssessmentInvariantViolation(
                    "items must contain EvidenceItem values",
                    invariant="EvidenceBundle.items.type",
                )
            if item.item_id.value in seen_items:
                raise AssessmentInvariantViolation(
                    "duplicate EvidenceItem id in bundle",
                    invariant="EvidenceBundle.items.unique",
                )
            obs_id = item.reference.observation_id.value
            if obs_id in seen_obs:
                raise AssessmentInvariantViolation(
                    "duplicate observation reference in EvidenceBundle",
                    invariant="EvidenceBundle.observation_ids.unique",
                )
            seen_items.add(item.item_id.value)
            seen_obs.add(obs_id)
            items.append(item)
        object.__setattr__(self, "items", tuple(items))
        if self.summary.observation_count != len(items):
            raise AssessmentInvariantViolation(
                "summary.observation_count must equal items length",
                invariant="EvidenceBundle.summary.observation_count",
            )

    def observation_ids(self) -> tuple[ObservationId, ...]:
        return tuple(item.reference.observation_id for item in self.items)

    def item_for_observation(
        self, observation_id: ObservationId
    ) -> EvidenceItem | None:
        for item in self.items:
            if item.reference.observation_id == observation_id:
                return item
        return None


@dataclass(frozen=True, slots=True)
class EvidencePackagingResult(EducationalValueObject):
    """Outcome of packaging observations into EvidenceBundle + AssessmentResult."""

    bundle: EvidenceBundle
    result_id: ResultId | None = None
    validated: bool = True
    events: tuple[Any, ...] = ()

    def _validate(self) -> None:
        if not isinstance(self.bundle, EvidenceBundle):
            raise AssessmentInvariantViolation(
                "bundle must be an EvidenceBundle",
                invariant="EvidencePackagingResult.bundle.type",
            )
        if self.result_id is not None and not isinstance(self.result_id, ResultId):
            raise AssessmentInvariantViolation(
                "result_id must be a ResultId when provided",
                invariant="EvidencePackagingResult.result_id.type",
            )
        if not isinstance(self.validated, bool):
            raise AssessmentInvariantViolation(
                "validated must be a bool",
                invariant="EvidencePackagingResult.validated.type",
            )
        object.__setattr__(self, "events", tuple(self.events or ()))

    @property
    def strength(self) -> EvidenceStrength:
        return self.bundle.strength

    @property
    def observation_ids(self) -> Sequence[ObservationId]:
        return self.bundle.observation_ids()
