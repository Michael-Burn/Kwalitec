"""Map domain ProjectionResult → application DTOs."""

from __future__ import annotations

from app.application.learning_graph.dto.projection_dto import (
    ProjectionEventDTO,
    ProjectionResultDTO,
    RelationshipProjectionDTO,
)
from app.domain.learning_graph.projections.events import (
    GraphProjectionCreated,
    GraphProjectionSkipped,
    GraphProjectionUpdated,
)
from app.domain.learning_graph.projections.relationship import RelationshipProjection
from app.domain.learning_graph.projections.result import ProjectionResult


def map_projection_result(result: ProjectionResult) -> ProjectionResultDTO:
    """Project an immutable domain projection result into an application DTO."""
    context = result.context
    relationships = tuple(
        _map_relationship(rel) for rel in result.batch.relationships
    )
    events = tuple(_map_event(event) for event in result.events)
    return ProjectionResultDTO(
        twin_id=context.twin_id,
        student_id=context.student_id,
        graph_id=context.graph_id,
        reasoning_request_id=context.reasoning_request_id,
        evidence_bundle_id=context.evidence_bundle_id,
        session_id=context.session_id,
        correlation_id=context.correlation_id,
        projection_version=context.projection_version,
        decision_version=context.decision_version,
        twin_version=context.twin_version,
        batch_id=result.batch.batch_id,
        graph_projection_id=result.graph_projection.projection_id,
        projected_at=result.projected_at,
        relationships=relationships,
        projection_ids=result.projection_ids,
        decision_ids=result.batch.decision_ids,
        skipped_decision_ids=result.batch.skipped_decision_ids,
        events=events,
        created_count=result.created_count,
        updated_count=result.updated_count,
        skipped_count=result.skipped_count,
    )


def _map_relationship(rel: RelationshipProjection) -> RelationshipProjectionDTO:
    return RelationshipProjectionDTO(
        projection_id=rel.projection_id,
        relationship_type=rel.relationship_type.value,
        from_ref=rel.from_ref,
        to_ref=rel.to_ref,
        twin_id=rel.twin_id,
        graph_id=rel.graph_id,
        decision_id=rel.decision_id,
        decision_version=rel.reference.decision_version,
        twin_version=rel.reference.twin_version,
        evidence_bundle_id=rel.reference.evidence_bundle_id,
        educational_observation_ids=rel.reference.educational_observation_ids,
        reasoning_request_id=rel.reference.reasoning_request_id,
        assessment_session_id=rel.reference.assessment_session_id,
        correlation_id=rel.reference.correlation_id,
        projection_version=rel.projection_version,
        created_at=rel.created_at,
        provenance=dict(rel.provenance),
        payload=dict(rel.payload),
    )


def _map_event(
    event: GraphProjectionCreated | GraphProjectionUpdated | GraphProjectionSkipped,
) -> ProjectionEventDTO:
    return ProjectionEventDTO(
        event_id=event.event_id,
        kind=event.kind.value,
        graph_id=event.graph_id,
        twin_id=event.twin_id,
        decision_id=event.decision_id,
        occurred_at=event.occurred_at,
        projection_version=event.projection_version,
        projection_id=getattr(event, "projection_id", "") or "",
        relationship_type=getattr(event, "relationship_type", "") or "",
        reason_code=getattr(event, "reason_code", "") or "",
    )
