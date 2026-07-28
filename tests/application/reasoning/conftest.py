"""Shared fixtures for AP-002D2 educational evidence interpretation tests."""

from __future__ import annotations

from datetime import UTC, datetime

from application.assessment.evidence.dto import (
    EvidenceBundleDTO,
    EvidenceContextDTO,
    EvidenceItemDTO,
    EvidenceMetadataDTO,
    EvidenceSummaryDTO,
)

FIXED_AT = datetime(2026, 7, 28, 10, 0, 0, tzinfo=UTC).replace(tzinfo=None)


def make_item(
    *,
    item_id: str = "item-1",
    observation_id: str = "obs-1",
    kind: str = "question_answered",
    question_id: str | None = "q-1",
    correctness: str | None = "correct",
    confidence: int | None = 3,
    response_time_ms: int | None = 1200,
    hints_used: int = 0,
    retries: int = 0,
    misconception_tags: tuple[str, ...] = (),
) -> EvidenceItemDTO:
    return EvidenceItemDTO(
        item_id=item_id,
        observation_id=observation_id,
        kind=kind,
        evidence_source="student_response",
        question_id=question_id,
        correctness=correctness,
        confidence=confidence,
        response_time_ms=response_time_ms,
        hints_used=hints_used,
        retries=retries,
        misconception_tags=misconception_tags,
        provenance={"response_payload": {"selected_option": "a"}},
    )


def make_bundle(
    *,
    bundle_id: str = "bundle-1",
    session_id: str = "sess-1",
    packaging_version: str = "AP-002C.1",
    items: tuple[EvidenceItemDTO, ...] | None = None,
    observation_ids: tuple[str, ...] | None = None,
    learning_objective_ids: tuple[str, ...] = ("lo-1",),
    concept_ids: tuple[str, ...] = ("concept-bayes",),
    question_ids: tuple[str, ...] | None = None,
    evidence_strength: str = "moderate",
    summary_count: int | None = None,
) -> EvidenceBundleDTO:
    resolved_items = (
        items
        if items is not None
        else (
            make_item(item_id="item-1", observation_id="obs-1", question_id="q-1"),
            make_item(
                item_id="item-2",
                observation_id="obs-2",
                question_id="q-2",
                correctness="incorrect",
                confidence=4,
                hints_used=1,
                retries=1,
                misconception_tags=("confuses_prior",),
            ),
        )
    )
    resolved_obs = (
        observation_ids
        if observation_ids is not None
        else tuple(i.observation_id for i in resolved_items)
    )
    resolved_questions = question_ids or tuple(
        i.question_id for i in resolved_items if i.question_id
    )
    count = summary_count if summary_count is not None else len(resolved_items)
    return EvidenceBundleDTO(
        bundle_id=bundle_id,
        session_id=session_id,
        evidence_strength=evidence_strength,
        context=EvidenceContextDTO(
            session_id=session_id,
            instrument_id="inst-1",
            assessment_id="assess-1",
            purpose="diagnostic",
            assessment_type="diagnostic",
            student_id="student-1",
        ),
        metadata=EvidenceMetadataDTO(
            evidence_source="assessment_engine",
            packaging_version=packaging_version,
            collected_at="2026-07-28T10:00:00",
            question_ids=resolved_questions,
            learning_objective_ids=learning_objective_ids,
            concept_ids=concept_ids,
            extra={},
        ),
        summary=EvidenceSummaryDTO(
            observation_count=count,
            question_observation_count=len(resolved_items),
            distinct_question_count=len(resolved_questions),
            correctness_counts={"correct": 1, "incorrect": 1},
            hint_total=1,
            retry_total=1,
            confidence_supplied_count=len(resolved_items),
            timing_available_count=len(resolved_items),
            misconception_tag_count=1,
        ),
        items=resolved_items,
        observation_ids=resolved_obs,
    )
