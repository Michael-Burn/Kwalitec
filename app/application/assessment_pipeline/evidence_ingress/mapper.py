"""Map validated EvidenceBundleDTO → Twin observation drafts (facts only).

No educational inference. No Twin mutation. Mapping only.
"""

from __future__ import annotations

import uuid
from typing import Any

from app.application.assessment_pipeline.evidence_ingress.dto import (
    EvidenceIngressMapping,
    EvidenceIngressRequest,
    EvidenceIngressTraceability,
    MappedEvidenceObservation,
)
from app.application.assessment_pipeline.evidence_ingress.versions import (
    INGRESS_CONTRACT_VERSION,
    INGRESS_PROVENANCE_PREFIX,
    INGRESS_TRIGGERED_BY,
)
from app.domain.student_digital_twin.observation import ObservationKind
from application.assessment.evidence.dto import EvidenceBundleDTO, EvidenceItemDTO

_KIND_MAP: dict[str, ObservationKind] = {
    "question_answered": ObservationKind.QUESTION_ANSWERED,
    "quiz_completed": ObservationKind.QUIZ_COMPLETED,
    "formula_reviewed": ObservationKind.FORMULA_REVIEWED,
    "reflection_captured": ObservationKind.STUDY_SESSION_COMPLETED,
    "worked_solution_reviewed": ObservationKind.STUDY_SESSION_COMPLETED,
    "session_abandoned": ObservationKind.STUDY_SESSION_COMPLETED,
}


def _twin_kind(kind: str) -> ObservationKind:
    mapped = _KIND_MAP.get((kind or "").strip())
    if mapped is not None:
        return mapped
    try:
        return ObservationKind(kind)
    except ValueError:
        return ObservationKind.STUDY_SESSION_COMPLETED


def _correct_flag(correctness: str | None) -> bool | None:
    if correctness is None:
        return None
    value = correctness.strip().lower()
    if value == "correct":
        return True
    if value in {"incorrect", "partial", "skipped", "abandoned", "uncoded"}:
        return False
    return None


def _question_refs(bundle: EvidenceBundleDTO) -> tuple[str, ...]:
    refs: list[str] = []
    seen: set[str] = set()
    for qid in bundle.metadata.question_ids or ():
        if qid and qid not in seen:
            seen.add(qid)
            refs.append(qid)
    for item in bundle.items:
        if item.question_id and item.question_id not in seen:
            seen.add(item.question_id)
            refs.append(item.question_id)
    return tuple(refs)


def _lo_refs(bundle: EvidenceBundleDTO) -> tuple[str, ...]:
    return tuple(
        oid
        for oid in (bundle.metadata.learning_objective_ids or ())
        if (oid or "").strip()
    )


def map_evidence_bundle(
    request: EvidenceIngressRequest,
    *,
    reasoning_request_id: str | None = None,
) -> EvidenceIngressMapping:
    """Map a validated ingress request into observation drafts + traceability."""
    bundle = request.bundle
    request_id = (
        reasoning_request_id
        or request.reasoning_request_id
        or f"rrq-{uuid.uuid4().hex[:16]}"
    )
    correlation_id = request.correlation_id.strip()
    observations = tuple(
        _map_item(
            item,
            bundle=bundle,
            twin_id=request.twin_id,
            correlation_id=correlation_id,
            reasoning_request_id=request_id,
        )
        for item in bundle.items
    )
    observation_ids = tuple(o.source_observation_id for o in observations)
    traceability = EvidenceIngressTraceability(
        assessment_session_id=bundle.session_id,
        evidence_bundle_id=bundle.bundle_id,
        observation_ids=observation_ids,
        question_references=_question_refs(bundle),
        learning_objective_references=_lo_refs(bundle),
        correlation_id=correlation_id,
        reasoning_request_id=request_id,
        ingress_contract_version=INGRESS_CONTRACT_VERSION,
        packaging_version=bundle.metadata.packaging_version,
    )
    return EvidenceIngressMapping(
        twin_id=request.twin_id,
        correlation_id=correlation_id,
        reasoning_request_id=request_id,
        triggered_by=INGRESS_TRIGGERED_BY,
        traceability=traceability,
        observations=observations,
    )


def _map_item(
    item: EvidenceItemDTO,
    *,
    bundle: EvidenceBundleDTO,
    twin_id: str,
    correlation_id: str,
    reasoning_request_id: str,
) -> MappedEvidenceObservation:
    kind = _twin_kind(item.kind)
    curriculum_entity_id = ""
    curriculum_entity_kind = ""
    if bundle.metadata.learning_objective_ids:
        curriculum_entity_id = bundle.metadata.learning_objective_ids[0]
        curriculum_entity_kind = "learning_objective"
    elif bundle.metadata.concept_ids:
        curriculum_entity_id = bundle.metadata.concept_ids[0]
        curriculum_entity_kind = "concept"

    correct = _correct_flag(item.correctness)
    metadata: dict[str, Any] = {
        "source": "assessment_pipeline",
        "ingress_contract_version": INGRESS_CONTRACT_VERSION,
        "packaging_version": bundle.metadata.packaging_version,
        "evidence_strength": bundle.evidence_strength,
        "evidence_bundle_id": bundle.bundle_id,
        "evidence_item_id": item.item_id,
        "assessment_session_id": bundle.session_id,
        "assessment_observation_id": item.observation_id,
        "correlation_id": correlation_id,
        "reasoning_request_id": reasoning_request_id,
        "question_id": item.question_id,
        "question_references": list(_question_refs(bundle)),
        "learning_objective_references": list(_lo_refs(bundle)),
        "concept_ids": list(bundle.metadata.concept_ids or ()),
        "instrument_id": bundle.context.instrument_id,
        "assessment_id": bundle.context.assessment_id,
        "purpose": bundle.context.purpose,
        "assessment_type": bundle.context.assessment_type,
        "evidence_source": item.evidence_source,
        "correctness": item.correctness,
        "confidence": item.confidence,
        "response_time_ms": item.response_time_ms,
        "hints_used": item.hints_used,
        "retries": item.retries,
        "misconception_tags": list(item.misconception_tags or ()),
        "performance": item.correctness or "recorded",
    }
    if correct is not None:
        metadata["correct"] = correct
    if item.provenance:
        metadata["assessment_provenance"] = dict(item.provenance)

    return MappedEvidenceObservation(
        observation_id=item.observation_id,
        kind=kind.value,
        curriculum_entity_id=curriculum_entity_id,
        curriculum_entity_kind=curriculum_entity_kind,
        evidence_reference=f"evidence_bundle:{bundle.bundle_id}:{item.item_id}",
        provenance=(
            f"{INGRESS_PROVENANCE_PREFIX}:{bundle.session_id}:{bundle.bundle_id}"
        ),
        metadata=metadata,
        correct=correct,
        source_observation_id=item.observation_id,
        question_id=item.question_id,
    )
