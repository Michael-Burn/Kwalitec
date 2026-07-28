"""EvidenceBundle builder — deterministic packaging from observations.

Architecture Source
    knowledge/product/AP-002/EVIDENCE_MODEL.md
    knowledge/product/AP-002/SCORING_MODEL.md
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any

from domain.assessment.aggregation.observation_collection import (
    ObservationAggregator,
    ObservationCollection,
)
from domain.assessment.entities.assessment_observation import AssessmentObservation
from domain.assessment.enums import AttemptOutcome, EvidenceSource, ObservationKind
from domain.assessment.evidence.ids import EvidenceBundleId, EvidenceItemId
from domain.assessment.evidence.models import (
    PACKAGING_VERSION,
    EvidenceBundle,
    EvidenceContext,
    EvidenceItem,
    EvidenceMetadata,
    EvidenceReference,
    EvidenceSummary,
)
from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.assessment.packaging.ids import sequential_id_factory
from domain.assessment.packaging.strength import calculate_evidence_strength
from domain.assessment.packaging.validation import (
    validate_packaged_bundle,
    validate_packaging_inputs,
)
from domain.assessment.value_objects.evidence_dimensions import EvidenceDimensions
from domain.assessment.value_objects.ids import InstrumentId, SessionId
from domain.assessment.value_objects.levels import ConfidenceLevel, EvidenceStrength
from domain.assessment.value_objects.references import (
    ConceptReference,
    LearningObjectiveReference,
)


def enrich_dimensions_from_observation(
    observation: AssessmentObservation,
) -> EvidenceDimensions | None:
    """Derive EvidenceDimensions from observation fields / provenance.

    Never invents mastery. Leaves correctness uncoded when not already present.
    """
    if observation.dimensions is not None:
        return observation.dimensions
    provenance = dict(observation.provenance or {})
    confidence_raw = provenance.get("confidence")
    confidence: ConfidenceLevel | None = None
    if isinstance(confidence_raw, int) and not isinstance(confidence_raw, bool):
        try:
            confidence = ConfidenceLevel(confidence_raw)
        except Exception:  # noqa: BLE001 — leave soft signal absent if out of range
            confidence = None

    response_time = provenance.get("response_time_ms")
    if response_time is not None and (
        not isinstance(response_time, int) or isinstance(response_time, bool)
    ):
        response_time = None

    hints_used = provenance.get("hints_used", 0)
    if not isinstance(hints_used, int) or isinstance(hints_used, bool):
        hints_used = 0
    retries = provenance.get("retries", 0)
    if not isinstance(retries, int) or isinstance(retries, bool):
        retries = 0

    tags_raw = provenance.get("misconception_tags") or ()
    tags: tuple[str, ...] = ()
    if isinstance(tags_raw, list | tuple):
        tags = tuple(str(t) for t in tags_raw if str(t).strip())

    correctness: AttemptOutcome | None = None
    outcome_raw = provenance.get("outcome") or provenance.get("correctness")
    if isinstance(outcome_raw, str):
        try:
            correctness = AttemptOutcome(outcome_raw)
        except ValueError:
            correctness = None
    elif isinstance(outcome_raw, AttemptOutcome):
        correctness = outcome_raw

    if provenance.get("abandoned"):
        correctness = AttemptOutcome.ABANDONED
    elif provenance.get("skipped"):
        correctness = AttemptOutcome.SKIPPED

    if (
        confidence is None
        and response_time is None
        and hints_used == 0
        and retries == 0
        and not tags
        and correctness is None
        and observation.kind is not ObservationKind.QUESTION_ANSWERED
    ):
        return None

    return EvidenceDimensions(
        correctness=correctness,
        confidence=confidence,
        response_time_ms=response_time,
        hints_used=hints_used,
        retries=retries,
        misconception_tags=tags,
    )


class EvidenceBundleBuilder:
    """Build an immutable EvidenceBundle from observations + packaging context."""

    def __init__(
        self,
        *,
        packaging_version: str = PACKAGING_VERSION,
        collected_at: datetime | None = None,
        id_factory: Any | None = None,
    ) -> None:
        self._packaging_version = packaging_version
        self._collected_at = collected_at
        self._id_factory = id_factory or sequential_id_factory()
        self._observations: list[AssessmentObservation] = []
        self._session_id: SessionId | None = None
        self._instrument_id: InstrumentId | None = None
        self._assessment_id: str | None = None
        self._purpose: str | None = None
        self._assessment_type: str | None = None
        self._student_id: str | None = None
        self._learning_objectives: tuple[LearningObjectiveReference, ...] = ()
        self._concepts: tuple[ConceptReference, ...] = ()
        self._extra: dict[str, Any] = {}
        self._expected_question_count: int | None = None
        self._bundle_id: EvidenceBundleId | None = None
        self._evidence_source = EvidenceSource.ASSESSMENT_ENGINE

    def with_bundle_id(
        self, bundle_id: EvidenceBundleId | str
    ) -> EvidenceBundleBuilder:
        self._bundle_id = (
            bundle_id
            if isinstance(bundle_id, EvidenceBundleId)
            else EvidenceBundleId(bundle_id)
        )
        return self

    def with_context(
        self,
        *,
        session_id: SessionId | str,
        instrument_id: InstrumentId | str | None = None,
        assessment_id: str | None = None,
        purpose: str | None = None,
        assessment_type: str | None = None,
        student_id: str | None = None,
    ) -> EvidenceBundleBuilder:
        self._session_id = (
            session_id if isinstance(session_id, SessionId) else SessionId(session_id)
        )
        if instrument_id is not None:
            self._instrument_id = (
                instrument_id
                if isinstance(instrument_id, InstrumentId)
                else InstrumentId(instrument_id)
            )
        self._assessment_id = assessment_id
        self._purpose = purpose
        self._assessment_type = assessment_type
        self._student_id = student_id
        return self

    def with_learning_objectives(
        self, objectives: Sequence[LearningObjectiveReference]
    ) -> EvidenceBundleBuilder:
        self._learning_objectives = tuple(objectives)
        return self

    def with_concepts(
        self, concepts: Sequence[ConceptReference]
    ) -> EvidenceBundleBuilder:
        self._concepts = tuple(concepts)
        return self

    def with_expected_question_count(self, count: int) -> EvidenceBundleBuilder:
        self._expected_question_count = count
        return self

    def with_extra_metadata(self, extra: Mapping[str, Any]) -> EvidenceBundleBuilder:
        self._extra = dict(extra)
        return self

    def with_evidence_source(self, source: EvidenceSource) -> EvidenceBundleBuilder:
        self._evidence_source = source
        return self

    def add_observation(
        self, observation: AssessmentObservation
    ) -> EvidenceBundleBuilder:
        self._observations.append(observation)
        return self

    def add_observations(
        self, observations: Sequence[AssessmentObservation]
    ) -> EvidenceBundleBuilder:
        self._observations.extend(observations)
        return self

    def build(self) -> EvidenceBundle:
        if self._session_id is None:
            raise AssessmentInvariantViolation(
                "session_id is required to build EvidenceBundle",
                invariant="EvidenceBundleBuilder.session_id.required",
            )
        collection = ObservationAggregator.aggregate(self._observations)
        validate_packaging_inputs(collection)
        if (
            collection.session_id is not None
            and collection.session_id != self._session_id
        ):
            raise AssessmentInvariantViolation(
                "builder session_id does not match observation session_id",
                invariant="EvidenceBundleBuilder.session_id.match",
            )

        items = self._build_items(collection)
        summary = self._build_summary(collection, items)
        strength = calculate_evidence_strength(
            collection, expected_question_count=self._expected_question_count
        )
        metadata = EvidenceMetadata(
            evidence_source=self._evidence_source,
            packaging_version=self._packaging_version,
            collected_at=self._collected_at or datetime.now(UTC),
            question_ids=collection.distinct_question_ids(),
            learning_objectives=self._learning_objectives,
            concepts=self._concepts,
            extra=self._extra,
        )
        context = EvidenceContext(
            session_id=self._session_id,
            instrument_id=self._instrument_id,
            assessment_id=self._assessment_id,
            purpose=self._purpose,
            assessment_type=self._assessment_type,
            student_id=self._student_id,
        )
        bundle_id = self._bundle_id or EvidenceBundleId(
            str(self._id_factory("evidence-bundle"))
        )
        bundle = EvidenceBundle(
            bundle_id=bundle_id,
            context=context,
            metadata=metadata,
            summary=summary,
            strength=strength,
            items=items,
        )
        validate_packaged_bundle(collection, bundle)
        return bundle

    def _build_items(
        self, collection: ObservationCollection
    ) -> tuple[EvidenceItem, ...]:
        items: list[EvidenceItem] = []
        for observation in collection.observations:
            dimensions = enrich_dimensions_from_observation(observation)
            item = EvidenceItem(
                item_id=EvidenceItemId(str(self._id_factory("evidence-item"))),
                reference=EvidenceReference(
                    observation_id=observation.observation_id,
                    question_id=observation.question_id,
                    kind=observation.kind,
                ),
                kind=observation.kind,
                evidence_source=observation.evidence_source,
                dimensions=dimensions,
                provenance=dict(observation.provenance or {}),
            )
            items.append(item)
        return tuple(items)

    def _build_summary(
        self,
        collection: ObservationCollection,
        items: Sequence[EvidenceItem],
    ) -> EvidenceSummary:
        question_items = [
            item for item in items if item.kind is ObservationKind.QUESTION_ANSWERED
        ]
        correctness: dict[AttemptOutcome, int] = {}
        hint_total = 0
        retry_total = 0
        confidence_supplied = 0
        timing_available = 0
        misconception_tag_count = 0
        for item in question_items:
            dims = item.dimensions
            if dims is None:
                continue
            if dims.correctness is not None:
                correctness[dims.correctness] = (
                    correctness.get(dims.correctness, 0) + 1
                )
            hint_total += dims.hints_used
            retry_total += dims.retries
            if dims.confidence is not None:
                confidence_supplied += 1
            if dims.response_time_ms is not None:
                timing_available += 1
            misconception_tag_count += len(dims.misconception_tags)
        return EvidenceSummary(
            observation_count=len(items),
            question_observation_count=len(question_items),
            distinct_question_count=len(collection.distinct_question_ids()),
            correctness_counts=tuple(correctness.items()),
            hint_total=hint_total,
            retry_total=retry_total,
            confidence_supplied_count=confidence_supplied,
            timing_available_count=timing_available,
            misconception_tag_count=misconception_tag_count,
        )


def package_observations(
    observations: Sequence[AssessmentObservation],
    *,
    session_id: SessionId | str,
    bundle_id: EvidenceBundleId | str | None = None,
    instrument_id: InstrumentId | str | None = None,
    assessment_id: str | None = None,
    purpose: str | None = None,
    assessment_type: str | None = None,
    student_id: str | None = None,
    learning_objectives: Sequence[LearningObjectiveReference] = (),
    concepts: Sequence[ConceptReference] = (),
    expected_question_count: int | None = None,
    extra: Mapping[str, Any] | None = None,
    collected_at: datetime | None = None,
    id_factory: Any | None = None,
) -> tuple[EvidenceBundle, EvidenceStrength]:
    """Convenience packaging entry point used by application services."""
    builder = EvidenceBundleBuilder(
        collected_at=collected_at,
        id_factory=id_factory,
    ).with_context(
        session_id=session_id,
        instrument_id=instrument_id,
        assessment_id=assessment_id,
        purpose=purpose,
        assessment_type=assessment_type,
        student_id=student_id,
    ).add_observations(observations).with_learning_objectives(
        learning_objectives
    ).with_concepts(concepts)
    if bundle_id is not None:
        builder = builder.with_bundle_id(bundle_id)
    if expected_question_count is not None:
        builder = builder.with_expected_question_count(expected_question_count)
    if extra:
        builder = builder.with_extra_metadata(extra)
    bundle = builder.build()
    return bundle, bundle.strength
