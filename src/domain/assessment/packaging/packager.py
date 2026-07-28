"""Domain packaging facade producing EvidencePackagingResult + events."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

from domain.assessment.entities.assessment_observation import AssessmentObservation
from domain.assessment.events.evidence_events import (
    AssessmentEvidenceCreated,
    EvidencePackaged,
    EvidenceValidated,
)
from domain.assessment.evidence.ids import EvidenceBundleId
from domain.assessment.evidence.models import EvidencePackagingResult
from domain.assessment.packaging.builder import (
    EvidenceBundleBuilder,
    package_observations,
)
from domain.assessment.value_objects.ids import InstrumentId, ResultId, SessionId
from domain.assessment.value_objects.references import (
    ConceptReference,
    LearningObjectiveReference,
)


class EvidencePackager:
    """Package observations into an EvidenceBundle and emit factual domain events."""

    def __init__(self, *, id_factory: Any | None = None) -> None:
        self._id_factory = id_factory

    def package(
        self,
        observations: Sequence[AssessmentObservation],
        *,
        session_id: SessionId | str,
        result_id: ResultId | str | None = None,
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
    ) -> EvidencePackagingResult:
        bundle, _strength = package_observations(
            observations,
            session_id=session_id,
            bundle_id=bundle_id,
            instrument_id=instrument_id,
            assessment_id=assessment_id,
            purpose=purpose,
            assessment_type=assessment_type,
            student_id=student_id,
            learning_objectives=learning_objectives,
            concepts=concepts,
            expected_question_count=expected_question_count,
            extra=extra,
            collected_at=collected_at,
            id_factory=self._id_factory,
        )
        resolved_result_id = None
        if result_id is not None:
            resolved_result_id = (
                result_id if isinstance(result_id, ResultId) else ResultId(result_id)
            )
        sid = bundle.context.session_id
        events = (
            EvidencePackaged(
                session_id=sid,
                bundle_id=bundle.bundle_id,
                observation_count=len(bundle.items),
                strength_band=bundle.strength.band,
            ),
            EvidenceValidated(
                session_id=sid,
                bundle_id=bundle.bundle_id,
                validated=True,
            ),
            AssessmentEvidenceCreated(
                session_id=sid,
                bundle_id=bundle.bundle_id,
                result_id=resolved_result_id,
                strength_band=bundle.strength.band,
            ),
        )
        return EvidencePackagingResult(
            bundle=bundle,
            result_id=resolved_result_id,
            validated=True,
            events=events,
        )


__all__ = [
    "EvidenceBundleBuilder",
    "EvidencePackager",
    "package_observations",
]
