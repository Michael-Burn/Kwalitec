"""AssessmentObservation — immutable educational fact.

Architecture Source
    knowledge/product/AP-002/EVIDENCE_MODEL.md
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from domain.assessment.enums import EvidenceSource, ObservationKind
from domain.assessment.validation.observation_validation import (
    assert_observation_identity,
    assert_observation_payload,
)
from domain.assessment.value_objects.evidence_dimensions import EvidenceDimensions
from domain.assessment.value_objects.ids import ObservationId, QuestionId, SessionId
from domain.education.foundation.base import EducationalEntity


@dataclass(frozen=True, slots=True, eq=False)
class AssessmentObservation(EducationalEntity):
    """Immutable fact about what happened in an assessment session.

    Observations never assert Twin mastery. Emission through AP-001 is deferred.
    """

    observation_id: ObservationId
    session_id: SessionId
    kind: ObservationKind
    evidence_source: EvidenceSource = EvidenceSource.ASSESSMENT_ENGINE
    dimensions: EvidenceDimensions | None = None
    question_id: QuestionId | None = None
    provenance: Mapping[str, Any] | None = None

    @property
    def entity_id(self) -> ObservationId:
        return self.observation_id

    def _validate(self) -> None:
        assert_observation_identity(self.observation_id)
        (
            session_id,
            kind,
            evidence_source,
            dimensions,
            question_id,
            provenance,
        ) = assert_observation_payload(
            session_id=self.session_id,
            kind=self.kind,
            evidence_source=self.evidence_source,
            dimensions=self.dimensions,
            question_id=self.question_id,
            provenance=self.provenance,
        )
        object.__setattr__(self, "session_id", session_id)
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "evidence_source", evidence_source)
        object.__setattr__(self, "dimensions", dimensions)
        object.__setattr__(self, "question_id", question_id)
        object.__setattr__(self, "provenance", provenance)
