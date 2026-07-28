"""AP-001 evidence ingress — Assessment EvidenceBundle → StudentReasoningService.

Integration only. No new educational algorithms. Existing ``reason()`` path.
"""

from __future__ import annotations

import uuid

from app.application.assessment_pipeline.evidence_ingress.dto import (
    EvidenceIngressMapping,
    EvidenceIngressRequest,
    EvidenceIngressResult,
)
from app.application.assessment_pipeline.evidence_ingress.errors import (
    DuplicateEvidenceSubmission,
    IncompleteEvidenceBundle,
    InvalidEvidenceBundle,
)
from app.application.assessment_pipeline.evidence_ingress.mapper import (
    map_evidence_bundle,
)
from app.application.assessment_pipeline.evidence_ingress.repository import (
    EvidenceSubmissionRecord,
    EvidenceSubmissionRepository,
    InMemoryEvidenceSubmissionRepository,
    utc_now_naive,
)
from app.application.assessment_pipeline.evidence_ingress.validator import (
    validate_evidence_bundle,
)
from app.application.assessment_pipeline.evidence_ingress.versions import (
    SUPPORTED_PACKAGING_VERSIONS,
)
from app.application.student_digital_twin.observation_service import ObservationService
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.application.student_digital_twin.student_reasoning_service import (
    StudentReasoningService,
)
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from application.assessment.evidence.dto import EvidenceBundleDTO


class EvidenceIngressService:
    """Single integration point: EvidenceBundle → Twin facts → existing reason()."""

    def __init__(
        self,
        *,
        twins: StudentDigitalTwinService | None = None,
        observations: ObservationService | None = None,
        reasoning: StudentReasoningService | None = None,
        submissions: EvidenceSubmissionRepository | None = None,
        supported_versions: frozenset[str] | None = None,
    ) -> None:
        self._twins = twins or StudentDigitalTwinService()
        self._observations = observations or ObservationService()
        self._reasoning = reasoning or StudentReasoningService()
        self._submissions = submissions or InMemoryEvidenceSubmissionRepository()
        self._supported_versions = supported_versions or SUPPORTED_PACKAGING_VERSIONS

    def accept(
        self,
        request: EvidenceIngressRequest,
        *,
        twin: StudentDigitalTwin | None = None,
        persist: bool = True,
        reason: bool = True,
    ) -> EvidenceIngressResult:
        """Validate, map, append facts, then invoke existing reasoning.

        Args:
            request: Twin identity + EvidenceBundleDTO + correlation id.
            twin: Optional pre-loaded Twin (must match request.twin_id).
            persist: Whether Twin observations / inferences persist.
            reason: When False, only append observations (tests / staged ingress).

        Returns:
            EvidenceIngressResult with preserved traceability identifiers.

        Raises:
            InvalidEvidenceBundle / IncompleteEvidenceBundle /
            MissingObservationReference / UnsupportedEvidenceVersion /
            DuplicateEvidenceSubmission
        """
        self._validate_request(request)
        validate_evidence_bundle(
            request.bundle, supported_versions=self._supported_versions
        )
        self._reject_duplicate(request.bundle.bundle_id)

        current = twin
        if current is None:
            current = self._twins.get(request.twin_id)
        if current is None:
            raise InvalidEvidenceBundle(
                f"Student Digital Twin {request.twin_id!r} not found"
            )
        if current.twin_id != request.twin_id:
            raise InvalidEvidenceBundle(
                "twin_id mismatch between request and loaded Twin"
            )

        mapping = map_evidence_bundle(request)
        twin_observation_ids: list[str] = []
        for draft in mapping.observations:
            current, recorded = self._observations.record(
                current,
                kind=draft.kind,
                curriculum_entity_id=draft.curriculum_entity_id,
                curriculum_entity_kind=draft.curriculum_entity_kind,
                evidence_reference=draft.evidence_reference,
                provenance=draft.provenance,
                metadata=dict(draft.metadata),
                observation_id=draft.observation_id,
                persist=persist,
            )
            twin_observation_ids.append(recorded.observation_id)

        if reason:
            current = self._reasoning.reason(
                current,
                triggered_by=mapping.triggered_by,
                observation_ids=tuple(twin_observation_ids),
                persist=persist,
            )
            # Prefer engine run id when reasoning executed; keep pre-assigned otherwise.
            reasoning_request_id = mapping.reasoning_request_id
            if current.reasoning_history:
                reasoning_request_id = current.reasoning_history[-1].reasoning_id
            mapping = _with_reasoning_request_id(mapping, reasoning_request_id)

        self._submissions.save(
            EvidenceSubmissionRecord(
                bundle_id=request.bundle.bundle_id,
                twin_id=request.twin_id,
                session_id=request.bundle.session_id,
                correlation_id=mapping.correlation_id,
                reasoning_request_id=mapping.reasoning_request_id,
                accepted_at=utc_now_naive(),
            )
        )

        return EvidenceIngressResult(
            twin_id=current.twin_id,
            twin_observation_ids=tuple(twin_observation_ids),
            triggered_by=mapping.triggered_by,
            traceability=mapping.traceability,
            mapping=mapping,
        )

    def accept_bundle(
        self,
        *,
        twin_id: str,
        bundle: EvidenceBundleDTO,
        correlation_id: str | None = None,
        reasoning_request_id: str | None = None,
        twin: StudentDigitalTwin | None = None,
        persist: bool = True,
        reason: bool = True,
    ) -> EvidenceIngressResult:
        """Convenience wrapper building EvidenceIngressRequest."""
        return self.accept(
            EvidenceIngressRequest(
                twin_id=twin_id,
                bundle=bundle,
                correlation_id=correlation_id or f"corr-{uuid.uuid4().hex[:16]}",
                reasoning_request_id=reasoning_request_id,
            ),
            twin=twin,
            persist=persist,
            reason=reason,
        )

    def _reject_duplicate(self, bundle_id: str) -> None:
        if self._submissions.exists(bundle_id):
            raise DuplicateEvidenceSubmission(
                f"evidence bundle already submitted: {bundle_id!r}"
            )

    @staticmethod
    def _validate_request(request: EvidenceIngressRequest) -> None:
        if request is None:
            raise InvalidEvidenceBundle("ingress request is null")
        if not (request.twin_id or "").strip():
            raise IncompleteEvidenceBundle("missing twin_id")
        if not (request.correlation_id or "").strip():
            raise IncompleteEvidenceBundle("missing correlation_id")
        if request.bundle is None:
            raise IncompleteEvidenceBundle("missing evidence bundle")


def _with_reasoning_request_id(
    mapping: EvidenceIngressMapping, reasoning_request_id: str
) -> EvidenceIngressMapping:
    if mapping.reasoning_request_id == reasoning_request_id:
        return mapping
    traceability = mapping.traceability
    updated_trace = type(traceability)(
        assessment_session_id=traceability.assessment_session_id,
        evidence_bundle_id=traceability.evidence_bundle_id,
        observation_ids=traceability.observation_ids,
        question_references=traceability.question_references,
        learning_objective_references=traceability.learning_objective_references,
        correlation_id=traceability.correlation_id,
        reasoning_request_id=reasoning_request_id,
        ingress_contract_version=traceability.ingress_contract_version,
        packaging_version=traceability.packaging_version,
    )
    # Also stamp observation metadata copies are already recorded; mapping reflects
    # the authoritative reasoning request id for callers / audits.
    return EvidenceIngressMapping(
        twin_id=mapping.twin_id,
        correlation_id=mapping.correlation_id,
        reasoning_request_id=reasoning_request_id,
        triggered_by=mapping.triggered_by,
        traceability=updated_trace,
        observations=mapping.observations,
    )
