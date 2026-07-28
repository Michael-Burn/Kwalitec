"""Factual domain events for assessment evidence packaging.

Events describe packaging facts only — no orchestration, Twin, or Reasoning.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.assessment.enums import EvidenceStrengthBand
from domain.assessment.evidence.ids import EvidenceBundleId
from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.assessment.value_objects.ids import ResultId, SessionId
from domain.education.foundation.base import EducationalValueObject


@dataclass(frozen=True, slots=True)
class EvidencePackaged(EducationalValueObject):
    """Observations were packaged into an EvidenceBundle."""

    session_id: SessionId
    bundle_id: EvidenceBundleId
    observation_count: int
    strength_band: EvidenceStrengthBand

    def _validate(self) -> None:
        if not isinstance(self.session_id, SessionId):
            raise AssessmentInvariantViolation(
                "session_id must be a SessionId",
                invariant="EvidencePackaged.session_id.type",
            )
        if not isinstance(self.bundle_id, EvidenceBundleId):
            raise AssessmentInvariantViolation(
                "bundle_id must be an EvidenceBundleId",
                invariant="EvidencePackaged.bundle_id.type",
            )
        if (
            not isinstance(self.observation_count, int)
            or isinstance(self.observation_count, bool)
            or self.observation_count < 0
        ):
            raise AssessmentInvariantViolation(
                "observation_count must be a non-negative integer",
                invariant="EvidencePackaged.observation_count.range",
            )
        if not isinstance(self.strength_band, EvidenceStrengthBand):
            raise AssessmentInvariantViolation(
                "strength_band must be an EvidenceStrengthBand",
                invariant="EvidencePackaged.strength_band.type",
            )


@dataclass(frozen=True, slots=True)
class EvidenceValidated(EducationalValueObject):
    """Packaged evidence passed structural validation."""

    session_id: SessionId
    bundle_id: EvidenceBundleId
    validated: bool = True

    def _validate(self) -> None:
        if not isinstance(self.session_id, SessionId):
            raise AssessmentInvariantViolation(
                "session_id must be a SessionId",
                invariant="EvidenceValidated.session_id.type",
            )
        if not isinstance(self.bundle_id, EvidenceBundleId):
            raise AssessmentInvariantViolation(
                "bundle_id must be an EvidenceBundleId",
                invariant="EvidenceValidated.bundle_id.type",
            )
        if not isinstance(self.validated, bool):
            raise AssessmentInvariantViolation(
                "validated must be a bool",
                invariant="EvidenceValidated.validated.type",
            )


@dataclass(frozen=True, slots=True)
class AssessmentEvidenceCreated(EducationalValueObject):
    """AssessmentResult-linked evidence package created (AP-001 export surface)."""

    session_id: SessionId
    bundle_id: EvidenceBundleId
    strength_band: EvidenceStrengthBand
    result_id: ResultId | None = None

    def _validate(self) -> None:
        if not isinstance(self.session_id, SessionId):
            raise AssessmentInvariantViolation(
                "session_id must be a SessionId",
                invariant="AssessmentEvidenceCreated.session_id.type",
            )
        if not isinstance(self.bundle_id, EvidenceBundleId):
            raise AssessmentInvariantViolation(
                "bundle_id must be an EvidenceBundleId",
                invariant="AssessmentEvidenceCreated.bundle_id.type",
            )
        if not isinstance(self.strength_band, EvidenceStrengthBand):
            raise AssessmentInvariantViolation(
                "strength_band must be an EvidenceStrengthBand",
                invariant="AssessmentEvidenceCreated.strength_band.type",
            )
        if self.result_id is not None and not isinstance(self.result_id, ResultId):
            raise AssessmentInvariantViolation(
                "result_id must be a ResultId when provided",
                invariant="AssessmentEvidenceCreated.result_id.type",
            )
