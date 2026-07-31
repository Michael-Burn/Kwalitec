"""Evidence Before Completion gate orchestration (EV-001B).

Coordinates package assembly + EducationalEvidenceAuthority validation.
Does not redefine grades or authority columns — EV-001A is binding.
"""

from __future__ import annotations

from typing import Any

from app.application.learning_session.dto.candidate_observation import (
    CandidateObservation,
)
from app.application.learning_session.dto.evidence_package import (
    EvidenceDisposition,
    EvidenceLifecycleState,
    SessionEvidencePackage,
)
from app.application.learning_session.evidence_package_builder import (
    EvidencePackageBuilder,
)
from app.application.learning_session.exceptions import EvidenceGateRejected
from app.services.educational_evidence_authority import EducationalEvidenceAuthority


class EvidenceBeforeCompletionGate:
    """Apply EV-001A Evidence Before Completion to a sitting package."""

    def __init__(self, *, builder: EvidencePackageBuilder | None = None) -> None:
        self._builder = builder or EvidencePackageBuilder()

    @property
    def builder(self) -> EvidencePackageBuilder:
        return self._builder

    def build_and_validate(
        self,
        *,
        student_id: str,
        session_id: str,
        observations: list[CandidateObservation] | tuple[CandidateObservation, ...],
        mission_instance_id: str = "",
        topic_id: str = "",
        topic_title: str = "",
        curriculum_identity: str = "",
        learning_objectives: tuple[str, ...] | list[str] = (),
        finish_review_verdict: str | None = None,
        finish_review_notes: str | None = None,
        session_metadata: dict[str, Any] | None = None,
    ) -> SessionEvidencePackage:
        """Build a Generated package and return it Validated / Accepted / Rejected."""
        package = self._builder.build(
            student_id=student_id,
            session_id=session_id,
            observations=observations,
            mission_instance_id=mission_instance_id,
            topic_id=topic_id,
            topic_title=topic_title,
            curriculum_identity=curriculum_identity,
            learning_objectives=learning_objectives,
            finish_review_verdict=finish_review_verdict,
            finish_review_notes=finish_review_notes,
            session_metadata=session_metadata,
        )
        validation = EducationalEvidenceAuthority.validate_session_evidence_package(
            package
        )
        return package.with_validation(validation)

    def assert_session_may_complete(
        self, package: SessionEvidencePackage
    ) -> SessionEvidencePackage:
        """Raise EvidenceGateRejected when session close is unlawful."""
        validation = package.validation
        if validation is None:
            raise EvidenceGateRejected(
                "Evidence package has not been validated",
                reason="not_validated",
                package_id=package.package_id,
            )
        if not validation.may_complete_session:
            raise EvidenceGateRejected(
                validation.reason or "evidence_gate_rejected",
                reason=validation.reason,
                student_explanation=validation.student_explanation,
                package_id=package.package_id,
            )
        return package

    @staticmethod
    def is_accepted(package: SessionEvidencePackage) -> bool:
        validation = package.validation
        if validation is None:
            return False
        return validation.disposition in {
            EvidenceDisposition.ACCEPTED,
            EvidenceDisposition.ACCEPTED_WITH_RESTRICTIONS,
        }

    @staticmethod
    def mark_persisted(package: SessionEvidencePackage) -> SessionEvidencePackage:
        if not EvidenceBeforeCompletionGate.is_accepted(package):
            # Rejected packages may still be retained as Informational history.
            return package.with_lifecycle(EvidenceLifecycleState.REJECTED)
        return package.with_lifecycle(EvidenceLifecycleState.PERSISTED)
