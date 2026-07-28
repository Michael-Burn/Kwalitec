"""Map domain ExplanationResult → application DTOs."""

from __future__ import annotations

from app.application.intelligent_tutor.dto.explanation_dto import (
    ExplanationEventDTO,
    ExplanationResultDTO,
    ExplanationSectionDTO,
)
from app.domain.intelligent_tutor.explainability.events import (
    TutorExplanationGenerated,
    TutorExplanationRequested,
    TutorExplanationUnavailable,
)
from app.domain.intelligent_tutor.explainability.result import (
    ExplanationEvent,
    ExplanationResult,
)
from app.domain.intelligent_tutor.explainability.section import ExplanationSection


def map_explanation_result(result: ExplanationResult) -> ExplanationResultDTO:
    """Project an immutable domain explanation result into an application DTO."""
    context = result.context
    explanation = result.explanation
    sections = tuple(_map_section(s) for s in explanation.sections)
    events = tuple(_map_event(event) for event in result.events)
    return ExplanationResultDTO(
        twin_id=context.twin_id,
        student_id=context.student_id,
        reasoning_request_id=context.reasoning_request_id,
        evidence_bundle_id=context.evidence_bundle_id,
        session_id=context.session_id,
        correlation_id=context.correlation_id,
        explanation_version=context.explanation_version,
        decision_version=context.decision_version,
        twin_version=context.twin_version,
        explanation_id=explanation.explanation_id,
        explanation_request_id=context.explanation_request_id,
        explained_at=result.explained_at,
        summary=explanation.summary,
        available=explanation.available,
        sections=sections,
        section_ids=result.section_ids,
        decision_ids=explanation.decision_ids,
        concept_ids=explanation.concept_ids,
        learning_objective_ids=explanation.learning_objective_ids,
        uncertainty_notes=explanation.uncertainty_notes,
        events=events,
        generated_count=result.generated_count,
        unavailable_count=result.unavailable_count,
        section_count=result.section_count,
        mission_plan_id=explanation.mission_plan_id,
        mission_id=explanation.mission_id,
        planning_version=context.planning_version,
        validation_passed=explanation.validation_passed,
        validation_summary=explanation.validation_summary,
        provenance=dict(explanation.provenance),
    )


def _map_section(section: ExplanationSection) -> ExplanationSectionDTO:
    ref = section.reference
    return ExplanationSectionDTO(
        section_id=section.section_id,
        kind=section.kind.value,
        title=section.title,
        body=section.body,
        decision_id=ref.decision_id,
        decision_version=ref.decision_version,
        twin_version=ref.twin_version,
        evidence_bundle_id=ref.evidence_bundle_id,
        educational_observation_ids=ref.educational_observation_ids,
        reasoning_request_id=ref.reasoning_request_id,
        assessment_session_id=ref.assessment_session_id,
        correlation_id=ref.correlation_id,
        explanation_version=ref.explanation_version,
        concept_ids=section.concept_ids,
        learning_objective_ids=section.learning_objective_ids,
        decision_ids=section.decision_ids,
        uncertainty_notes=section.uncertainty_notes,
        learning_objective=ref.learning_objective,
        concept=ref.concept,
        mission_plan_id=ref.mission_plan_id,
        mission_id=ref.mission_id,
        provenance=dict(section.provenance),
    )


def _map_event(event: ExplanationEvent) -> ExplanationEventDTO:
    if isinstance(event, TutorExplanationRequested):
        return ExplanationEventDTO(
            event_id=event.event_id,
            kind=event.kind.value,
            twin_id=event.twin_id,
            occurred_at=event.occurred_at,
            explanation_version=event.explanation_version,
            decision_set_id=event.decision_set_id,
            explanation_request_id=event.explanation_request_id,
        )
    if isinstance(event, TutorExplanationGenerated):
        return ExplanationEventDTO(
            event_id=event.event_id,
            kind=event.kind.value,
            twin_id=event.twin_id,
            occurred_at=event.occurred_at,
            explanation_version=event.explanation_version,
            decision_set_id=event.decision_set_id,
            explanation_id=event.explanation_id,
            mission_plan_id=event.mission_plan_id,
            section_count=event.section_count,
        )
    if isinstance(event, TutorExplanationUnavailable):
        return ExplanationEventDTO(
            event_id=event.event_id,
            kind=event.kind.value,
            twin_id=event.twin_id,
            occurred_at=event.occurred_at,
            explanation_version=event.explanation_version,
            decision_set_id=event.decision_set_id,
            explanation_id=event.explanation_id,
            explanation_request_id=event.explanation_request_id,
            reason_code=event.reason_code,
        )
    return ExplanationEventDTO(
        event_id=getattr(event, "event_id", ""),
        kind=getattr(getattr(event, "kind", None), "value", ""),
        twin_id=getattr(event, "twin_id", ""),
        occurred_at=getattr(event, "occurred_at"),
        explanation_version=getattr(event, "explanation_version", ""),
    )
