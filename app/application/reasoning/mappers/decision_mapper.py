"""Map domain DecisionResult → application DTOs."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.application.reasoning.dto.decision_dto import (
    DecisionReasonDTO,
    DecisionResultDTO,
    EducationalDecisionDTO,
)
from app.domain.reasoning.decisions.decision import EducationalDecision
from app.domain.reasoning.decisions.result import DecisionResult


def map_decision_result(result: DecisionResult) -> DecisionResultDTO:
    """Project an immutable domain decision result into an application DTO."""
    context = result.context
    decisions = tuple(
        _map_decision(decision) for decision in result.decision_set.decisions
    )
    return DecisionResultDTO(
        twin_id=context.twin_id,
        reasoning_request_id=context.reasoning_request_id,
        evidence_bundle_id=context.evidence_bundle_id,
        session_id=context.session_id,
        correlation_id=context.correlation_id,
        decision_version=context.decision_version,
        set_id=result.decision_set.set_id,
        decided_at=result.decided_at,
        prior_twin_version=context.prior_twin_version,
        decisions=decisions,
        decision_ids=result.decision_ids,
        observation_ids=result.decision_set.observation_ids,
    )


def _map_decision(decision: EducationalDecision) -> EducationalDecisionDTO:
    value: Any = decision.value
    if isinstance(value, Mapping):
        value = dict(value)
    return EducationalDecisionDTO(
        decision_id=decision.decision_id,
        category=decision.category.value,
        twin_id=decision.twin_id,
        subject_ref=decision.subject_ref,
        value=value,
        reason=DecisionReasonDTO(
            code=decision.reason.code,
            summary=decision.reason.summary,
            detail=decision.reason.detail,
            observation_ids=decision.reason.observation_ids,
            rule_code=decision.reason.rule_code,
        ),
        decision_version=decision.decision_version,
        created_at=decision.created_at,
        evidence_bundle_id=decision.reference.evidence_bundle_id,
        educational_observation_ids=decision.reference.educational_observation_ids,
        reasoning_request_id=decision.reference.reasoning_request_id,
        assessment_session_id=decision.reference.assessment_session_id,
        correlation_id=decision.reference.correlation_id,
        learning_objective_reference=decision.reference.learning_objective_reference,
        concept_reference=decision.reference.concept_reference,
        provenance=dict(decision.provenance),
        traceability=dict(decision.traceability),
        payload=dict(decision.payload),
    )
