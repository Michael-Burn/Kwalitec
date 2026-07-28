"""Mappers for assessment evidence packaging DTOs."""

from __future__ import annotations

from application.assessment.evidence.dto import (
    EvidenceBundleDTO,
    EvidenceContextDTO,
    EvidenceItemDTO,
    EvidenceMetadataDTO,
    EvidencePackagingResultDTO,
    EvidenceSummaryDTO,
)
from domain.assessment.evidence.models import EvidenceBundle, EvidencePackagingResult


def to_evidence_item_dto(item) -> EvidenceItemDTO:
    dims = item.dimensions
    return EvidenceItemDTO(
        item_id=item.item_id.value,
        observation_id=item.reference.observation_id.value,
        kind=item.kind.value,
        evidence_source=item.evidence_source.value,
        question_id=(
            item.reference.question_id.value if item.reference.question_id else None
        ),
        correctness=dims.correctness.value if dims and dims.correctness else None,
        confidence=dims.confidence.value if dims and dims.confidence else None,
        response_time_ms=dims.response_time_ms if dims else None,
        hints_used=dims.hints_used if dims else 0,
        retries=dims.retries if dims else 0,
        misconception_tags=dims.misconception_tags if dims else (),
        provenance=dict(item.provenance),
    )


def to_evidence_bundle_dto(bundle: EvidenceBundle) -> EvidenceBundleDTO:
    return EvidenceBundleDTO(
        bundle_id=bundle.bundle_id.value,
        session_id=bundle.context.session_id.value,
        evidence_strength=bundle.strength.band.value,
        context=EvidenceContextDTO(
            session_id=bundle.context.session_id.value,
            instrument_id=(
                bundle.context.instrument_id.value
                if bundle.context.instrument_id
                else None
            ),
            assessment_id=bundle.context.assessment_id,
            purpose=bundle.context.purpose,
            assessment_type=bundle.context.assessment_type,
            student_id=bundle.context.student_id,
        ),
        metadata=EvidenceMetadataDTO(
            evidence_source=bundle.metadata.evidence_source.value,
            packaging_version=bundle.metadata.packaging_version,
            collected_at=(
                bundle.metadata.collected_at.isoformat()
                if bundle.metadata.collected_at
                else None
            ),
            question_ids=tuple(q.value for q in bundle.metadata.question_ids),
            learning_objective_ids=tuple(
                o.objective_id.value for o in bundle.metadata.learning_objectives
            ),
            concept_ids=tuple(c.concept_id.value for c in bundle.metadata.concepts),
            extra=dict(bundle.metadata.extra),
        ),
        summary=EvidenceSummaryDTO(
            observation_count=bundle.summary.observation_count,
            question_observation_count=bundle.summary.question_observation_count,
            distinct_question_count=bundle.summary.distinct_question_count,
            correctness_counts={
                k.value: v for k, v in bundle.summary.correctness_counts
            },
            hint_total=bundle.summary.hint_total,
            retry_total=bundle.summary.retry_total,
            confidence_supplied_count=bundle.summary.confidence_supplied_count,
            timing_available_count=bundle.summary.timing_available_count,
            misconception_tag_count=bundle.summary.misconception_tag_count,
        ),
        items=tuple(to_evidence_item_dto(item) for item in bundle.items),
        observation_ids=tuple(oid.value for oid in bundle.observation_ids()),
    )


def to_evidence_packaging_result_dto(
    result: EvidencePackagingResult,
) -> EvidencePackagingResultDTO:
    return EvidencePackagingResultDTO(
        bundle=to_evidence_bundle_dto(result.bundle),
        result_id=result.result_id.value if result.result_id else None,
        validated=result.validated,
        evidence_strength=result.bundle.strength.band.value,
    )


class EvidenceMapper:
    """Application mapper for evidence packaging boundary types."""

    @staticmethod
    def to_bundle_dto(bundle: EvidenceBundle) -> EvidenceBundleDTO:
        return to_evidence_bundle_dto(bundle)

    @staticmethod
    def to_result_dto(result: EvidencePackagingResult) -> EvidencePackagingResultDTO:
        return to_evidence_packaging_result_dto(result)
