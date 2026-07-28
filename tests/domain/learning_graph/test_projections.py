"""Domain tests for AP-002D4 Learning Graph projection models."""

from __future__ import annotations

import pytest

from app.domain.learning_graph.projections.batch import ProjectionBatch
from app.domain.learning_graph.projections.context import ProjectionContext
from app.domain.learning_graph.projections.errors import (
    DuplicateProjection,
    UnknownProjectionRelationshipType,
)
from app.domain.learning_graph.projections.events import (
    GraphProjectionCreated,
    GraphProjectionSkipped,
    ProjectionEventKind,
)
from app.domain.learning_graph.projections.projection import GraphProjection
from app.domain.learning_graph.projections.reference import ProjectionReference
from app.domain.learning_graph.projections.relationship import RelationshipProjection
from app.domain.learning_graph.projections.relationship_type import (
    ProjectionRelationshipType,
    parse_projection_relationship_type,
)
from app.domain.learning_graph.projections.version import (
    PROJECTION_VERSION,
    ProjectionVersion,
)
from tests.application.learning_graph.conftest import FIXED_AT


def _context(**overrides) -> ProjectionContext:
    base = dict(
        twin_id="twin-1",
        student_id="student-1",
        graph_id="lg-1",
        reasoning_request_id="rr-1",
        evidence_bundle_id="bundle-1",
        session_id="sess-1",
        correlation_id="corr-1",
        projection_version=PROJECTION_VERSION,
        decision_version="AP-002D3.decision.v1",
        twin_version=2,
        decision_set_id="eds-1",
    )
    base.update(overrides)
    return ProjectionContext(**base)


def _reference(**overrides) -> ProjectionReference:
    base = dict(
        decision_id="ed-1",
        decision_version="AP-002D3.decision.v1",
        twin_version=2,
        evidence_bundle_id="bundle-1",
        educational_observation_ids=("obs-1",),
        reasoning_request_id="rr-1",
        assessment_session_id="sess-1",
        correlation_id="corr-1",
        projection_version=PROJECTION_VERSION,
        twin_id="twin-1",
        graph_id="lg-1",
        learning_objective_reference="lo-1",
        concept_reference="concept-bayes",
        projection_id="gp-1",
    )
    base.update(overrides)
    return ProjectionReference(**base)


def _relationship(**overrides) -> RelationshipProjection:
    base = dict(
        projection_id="gp:twin-1:ed-1:student_concept:student-1:concept-bayes",
        relationship_type=ProjectionRelationshipType.STUDENT_CONCEPT,
        from_ref="student-1",
        to_ref="concept-bayes",
        twin_id="twin-1",
        graph_id="lg-1",
        reference=_reference(),
        projection_version=PROJECTION_VERSION,
        created_at=FIXED_AT,
        decision_id="ed-1",
        provenance={
            "decision_id": "ed-1",
            "decision_version": "AP-002D3.decision.v1",
            "twin_version": 2,
            "evidence_bundle_id": "bundle-1",
            "educational_observation_ids": ["obs-1"],
            "reasoning_request_id": "rr-1",
            "assessment_session_id": "sess-1",
            "correlation_id": "corr-1",
            "projection_version": PROJECTION_VERSION,
        },
    )
    base.update(overrides)
    return RelationshipProjection(**base)


def test_projection_version_constant() -> None:
    assert PROJECTION_VERSION == "AP-002D4.projection.v1"
    assert str(ProjectionVersion()) == PROJECTION_VERSION


def test_relationship_types_are_approved_only() -> None:
    assert (
        parse_projection_relationship_type("student_concept")
        is ProjectionRelationshipType.STUDENT_CONCEPT
    )
    with pytest.raises(UnknownProjectionRelationshipType):
        parse_projection_relationship_type("invented_mastery_edge")


def test_relationship_projection_is_immutable() -> None:
    rel = _relationship()
    with pytest.raises(Exception):
        rel.from_ref = "other"  # type: ignore[misc]


def test_projection_batch_rejects_duplicate_ids() -> None:
    rel = _relationship()
    with pytest.raises(DuplicateProjection):
        ProjectionBatch(
            batch_id="batch-1",
            relationships=(rel, rel),
            context=_context(),
            projection_version=PROJECTION_VERSION,
        )


def test_graph_projection_and_events() -> None:
    context = _context()
    rel = _relationship()
    batch_rels = (rel,)
    projection = GraphProjection(
        projection_id="gpg-1",
        graph_id="lg-1",
        twin_id="twin-1",
        context=context,
        relationships=batch_rels,
        projection_version=PROJECTION_VERSION,
        twin_version=2,
        created_at=FIXED_AT,
    )
    assert len(projection) == 1
    assert projection.decision_ids == ("ed-1",)

    created = GraphProjectionCreated(
        event_id="ev-1",
        projection_id=rel.projection_id,
        graph_id="lg-1",
        twin_id="twin-1",
        decision_id="ed-1",
        relationship_type="student_concept",
        occurred_at=FIXED_AT,
        projection_version=PROJECTION_VERSION,
    )
    skipped = GraphProjectionSkipped(
        event_id="ev-2",
        graph_id="lg-1",
        twin_id="twin-1",
        decision_id="ed-2",
        reason_code="non_projectable_decision",
        occurred_at=FIXED_AT,
        projection_version=PROJECTION_VERSION,
    )
    assert created.kind is ProjectionEventKind.CREATED
    assert skipped.kind is ProjectionEventKind.SKIPPED
