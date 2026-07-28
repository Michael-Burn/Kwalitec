"""Map domain PlanningResult → application DTOs."""

from __future__ import annotations

from app.application.mission_engine.dto.planning_dto import (
    MissionCandidateDTO,
    PlanningEventDTO,
    PlanningResultDTO,
)
from app.domain.mission.planning.candidate import MissionCandidateProjection
from app.domain.mission.planning.events import (
    MissionGenerated,
    MissionPlanningCompleted,
    MissionPlanningSkipped,
    MissionPlanningStarted,
)
from app.domain.mission.planning.result import PlanningEvent, PlanningResult


def map_planning_result(result: PlanningResult) -> PlanningResultDTO:
    """Project an immutable domain planning result into an application DTO."""
    context = result.context
    candidates = tuple(_map_candidate(c) for c in result.batch.candidates)
    events = tuple(_map_event(event) for event in result.events)
    plan = result.study_mission_plan
    return PlanningResultDTO(
        twin_id=context.twin_id,
        student_id=context.student_id,
        reasoning_request_id=context.reasoning_request_id,
        evidence_bundle_id=context.evidence_bundle_id,
        session_id=context.session_id,
        correlation_id=context.correlation_id,
        planning_version=context.planning_version,
        decision_version=context.decision_version,
        twin_version=context.twin_version,
        batch_id=result.batch.batch_id,
        plan_id=plan.plan_id,
        mission_id=plan.mission_id,
        mission_request_id=context.mission_request_id,
        planned_at=result.planned_at,
        goal=plan.goal,
        educational_explanation=plan.educational_explanation,
        candidates=candidates,
        candidate_ids=result.candidate_ids,
        decision_ids=result.batch.decision_ids,
        skipped_decision_ids=result.batch.skipped_decision_ids,
        events=events,
        generated_count=result.generated_count,
        skipped_count=result.skipped_count,
        candidate_count=result.candidate_count,
        validation_passed=plan.validation_passed,
        validation_summary=plan.validation_summary,
    )


def _map_candidate(cand: MissionCandidateProjection) -> MissionCandidateDTO:
    return MissionCandidateDTO(
        candidate_id=cand.candidate_id,
        activity_type=cand.activity_type.value,
        concept_id=cand.concept_id,
        concept_title=cand.concept_title,
        twin_id=cand.twin_id,
        decision_id=cand.decision_id,
        decision_version=cand.reference.decision_version,
        twin_version=cand.reference.twin_version,
        evidence_bundle_id=cand.reference.evidence_bundle_id,
        educational_observation_ids=cand.reference.educational_observation_ids,
        reasoning_request_id=cand.reference.reasoning_request_id,
        assessment_session_id=cand.reference.assessment_session_id,
        correlation_id=cand.reference.correlation_id,
        planning_version=cand.planning_version,
        created_at=cand.created_at,
        priority_score=cand.priority_score,
        priority_band=cand.priority_band,
        learning_objective_id=cand.learning_objective_id,
        recommendation_id=cand.recommendation_id,
        gap_id=cand.gap_id,
        recovery_path_concept_ids=cand.recovery_path_concept_ids,
        evidence_ids=cand.evidence_ids,
        priority_explanation=cand.priority_explanation,
        provenance=dict(cand.provenance),
        payload=dict(cand.payload),
    )


def _map_event(event: PlanningEvent) -> PlanningEventDTO:
    if isinstance(event, MissionPlanningStarted):
        return PlanningEventDTO(
            event_id=event.event_id,
            kind=event.kind.value,
            twin_id=event.twin_id,
            occurred_at=event.occurred_at,
            planning_version=event.planning_version,
            decision_set_id=event.decision_set_id,
            mission_request_id=event.mission_request_id,
        )
    if isinstance(event, MissionGenerated):
        return PlanningEventDTO(
            event_id=event.event_id,
            kind=event.kind.value,
            twin_id=event.twin_id,
            occurred_at=event.occurred_at,
            planning_version=event.planning_version,
            decision_id=event.decision_id,
            plan_id=event.plan_id,
            mission_id=event.mission_id,
            concept_id=event.concept_id,
        )
    if isinstance(event, MissionPlanningSkipped):
        return PlanningEventDTO(
            event_id=event.event_id,
            kind=event.kind.value,
            twin_id=event.twin_id,
            occurred_at=event.occurred_at,
            planning_version=event.planning_version,
            decision_id=event.decision_id,
            reason_code=event.reason_code,
            candidate_id=event.candidate_id,
            plan_id=event.plan_id,
        )
    if isinstance(event, MissionPlanningCompleted):
        return PlanningEventDTO(
            event_id=event.event_id,
            kind=event.kind.value,
            twin_id=event.twin_id,
            occurred_at=event.occurred_at,
            planning_version=event.planning_version,
            decision_set_id=event.decision_set_id,
            mission_request_id=event.mission_request_id,
            plan_id=event.plan_id,
            candidate_count=event.candidate_count,
            skipped_count=event.skipped_count,
        )
    return PlanningEventDTO(
        event_id=getattr(event, "event_id", ""),
        kind=getattr(getattr(event, "kind", None), "value", ""),
        twin_id=getattr(event, "twin_id", ""),
        occurred_at=getattr(event, "occurred_at"),
        planning_version=getattr(event, "planning_version", ""),
    )
