"""AP-002D4 — Twin decision projection into Learning Graph."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.application.learning_graph.mappers.projection_mapper import (
    map_projection_result,
)
from app.application.learning_graph.projections.persistence import (
    ProjectionPersistenceService,
)
from app.application.learning_graph.projections.relationship_builder import (
    RelationshipBuilder,
)
from app.application.learning_graph.projections.twin_projection_service import (
    TwinProjectionService,
)
from app.application.learning_graph.projections.validator import ProjectionValidator
from app.application.learning_graph.projections.versions import PROJECTION_VERSION
from app.application.reasoning.decisions.versions import DECISION_VERSION
from app.domain.learning_graph.projections.context import ProjectionContext
from app.domain.learning_graph.projections.errors import (
    DuplicateProjection,
    IncompleteProjectionProvenance,
    InvalidDecisionVersion,
    UnknownProjectionRelationshipType,
    UnsupportedProjectionVersion,
)
from app.domain.learning_graph.projections.relationship_type import (
    ProjectionRelationshipType,
)
from app.domain.reasoning.decisions.category import DecisionCategory
from tests.application.learning_graph.conftest import (
    FIXED_AT,
    make_decision,
    make_decision_set,
    make_graph,
    make_twin,
)


def test_projection_generation_from_mastery_decision() -> None:
    twin = make_twin(version=2)
    decision_set = make_decision_set(twin_id=twin.twin_id)
    service = TwinProjectionService()
    result = service.project(
        twin,
        decision_set,
        graph_id="lg-proj-1",
        projected_at=FIXED_AT,
    )

    types = {r.relationship_type for r in result.batch.relationships}
    assert ProjectionRelationshipType.STUDENT_CONCEPT in types
    assert ProjectionRelationshipType.LEARNING_OBJECTIVE_CONCEPT in types
    assert ProjectionRelationshipType.STUDENT_LEARNING_OBJECTIVE in types
    assert result.created_count >= 3
    assert result.context.projection_version == PROJECTION_VERSION
    assert all(
        r.reference.decision_id for r in result.batch.relationships
    )


def test_idempotent_repeated_projection() -> None:
    twin = make_twin(version=2)
    decision_set = make_decision_set(twin_id=twin.twin_id)
    service = TwinProjectionService()
    first = service.project(
        twin, decision_set, graph_id="lg-idem", projected_at=FIXED_AT
    )
    second = service.project(
        twin, decision_set, graph_id="lg-idem", projected_at=FIXED_AT
    )

    assert first.relationship_count > 0
    assert second.relationship_count == 0
    assert second.skipped_count > 0
    snap1 = service.graph_snapshot(twin_id=twin.twin_id, graph_id="lg-idem")
    snap2 = service.graph_snapshot(twin_id=twin.twin_id, graph_id="lg-idem")
    assert snap1["relationships"] == snap2["relationships"]


def test_identical_twin_state_projects_identical_graph() -> None:
    twin = make_twin(version=3)
    decision_set = make_decision_set(twin_id=twin.twin_id)

    a = TwinProjectionService()
    b = TwinProjectionService()
    ra = a.project(twin, decision_set, graph_id="lg-same", projected_at=FIXED_AT)
    rb = b.project(twin, decision_set, graph_id="lg-same", projected_at=FIXED_AT)

    assert [r.projection_id for r in ra.batch.relationships] == [
        r.projection_id for r in rb.batch.relationships
    ]
    assert [
        (
            r.relationship_type.value,
            r.from_ref,
            r.to_ref,
            r.decision_id,
            dict(r.provenance),
        )
        for r in ra.batch.relationships
    ] == [
        (
            r.relationship_type.value,
            r.from_ref,
            r.to_ref,
            r.decision_id,
            dict(r.provenance),
        )
        for r in rb.batch.relationships
    ]
    assert a.graph_snapshot(twin_id=twin.twin_id, graph_id="lg-same")[
        "relationships"
    ] == b.graph_snapshot(twin_id=twin.twin_id, graph_id="lg-same")["relationships"]


def test_replay_support() -> None:
    twin = make_twin(version=2)
    decision_set = make_decision_set(twin_id=twin.twin_id)
    service = TwinProjectionService()
    original = service.project(
        twin, decision_set, graph_id="lg-replay", projected_at=FIXED_AT
    )
    replayed = service.replay(
        twin, decision_set, graph_id="lg-replay", projected_at=FIXED_AT
    )
    assert [r.projection_id for r in original.batch.relationships] == [
        r.projection_id for r in replayed.batch.relationships
    ]
    assert original.graph_projection.projection_id == (
        replayed.graph_projection.projection_id
    )


def test_versioning_preserved() -> None:
    twin = make_twin(version=5)
    decision_set = make_decision_set(twin_id=twin.twin_id)
    result = TwinProjectionService().project(
        twin, decision_set, graph_id="lg-ver", projected_at=FIXED_AT
    )
    assert result.context.twin_version == 5
    assert result.context.projection_version == PROJECTION_VERSION
    assert result.context.decision_version == DECISION_VERSION
    assert result.graph_projection.twin_version == 5
    service = TwinProjectionService()
    service.project(twin, decision_set, graph_id="lg-ver2", projected_at=FIXED_AT)
    assert (
        len(
            service.persistence.version_history(
                twin_id=twin.twin_id, graph_id="lg-ver2"
            )
        )
        == 1
    )


def test_relationship_validation_rejects_unknown_type() -> None:
    twin = make_twin()
    context = ProjectionContext(
        twin_id=twin.twin_id,
        student_id=twin.student.student_id,
        graph_id="lg-1",
        reasoning_request_id="rr-1",
        evidence_bundle_id="bundle-1",
        session_id="sess-1",
        correlation_id="corr-1",
        projection_version=PROJECTION_VERSION,
        decision_version=DECISION_VERSION,
        twin_version=2,
        decision_set_id="eds-1",
    )
    builder = RelationshipBuilder(context=context, created_at=FIXED_AT)
    decision = make_decision(twin_id=twin.twin_id)
    with pytest.raises(UnknownProjectionRelationshipType):
        builder.build_explicit(
            relationship_type="not_a_real_relationship",
            from_ref="a",
            to_ref="b",
            decision=decision,
        )


def test_duplicate_protection_strict_mode() -> None:
    twin = make_twin(version=2)
    decision_set = make_decision_set(twin_id=twin.twin_id)
    service = TwinProjectionService()
    service.project(
        twin,
        decision_set,
        graph_id="lg-dup",
        projected_at=FIXED_AT,
        allow_idempotent_skip=True,
    )
    with pytest.raises(DuplicateProjection):
        service.project(
            twin,
            decision_set,
            graph_id="lg-dup",
            projected_at=FIXED_AT,
            allow_idempotent_skip=False,
        )


def test_traceability_on_every_edge() -> None:
    twin = make_twin(version=2)
    decision_set = make_decision_set(twin_id=twin.twin_id)
    result = TwinProjectionService().project(
        twin, decision_set, graph_id="lg-trace", projected_at=FIXED_AT
    )
    for rel in result.batch.relationships:
        ref = rel.reference
        assert ref.decision_id
        assert ref.decision_version == DECISION_VERSION
        assert ref.twin_version == 2
        assert ref.evidence_bundle_id == "bundle-1"
        assert ref.educational_observation_ids
        assert ref.reasoning_request_id == "rr-1"
        assert ref.assessment_session_id == "sess-1"
        assert ref.correlation_id == "corr-1"
        assert ref.projection_version == PROJECTION_VERSION
        for key in (
            "decision_id",
            "decision_version",
            "twin_version",
            "evidence_bundle_id",
            "educational_observation_ids",
            "reasoning_request_id",
            "assessment_session_id",
            "correlation_id",
            "projection_version",
        ):
            assert key in rel.provenance


def test_soft_decisions_are_skipped() -> None:
    twin = make_twin(version=2)
    soft = make_decision(
        twin_id=twin.twin_id,
        decision_id="ed:rr-1:bundle-1:uncertainty_preserved:twin",
        category=DecisionCategory.UNCERTAINTY_PRESERVED,
        subject_ref="twin",
        value={"preserved": True},
        concept_reference="",
        payload={},
    )
    decision_set = make_decision_set(twin_id=twin.twin_id, decisions=(soft,))
    result = TwinProjectionService().project(
        twin, decision_set, graph_id="lg-soft", projected_at=FIXED_AT
    )
    assert result.relationship_count == 0
    assert result.skipped_count == 1


def test_explicit_structure_and_misconceptions_from_payload() -> None:
    twin = make_twin(version=2)
    decision = make_decision(
        twin_id=twin.twin_id,
        payload={
            "mastery_id": "mst-concept-bayes",
            "mastery_score": 0.4,
            "confidence": 0.3,
            "trend": "stable",
            "evidence_count": 2,
            "related_concepts": ["concept-conditional"],
            "prerequisites": ["concept-probability"],
            "dependencies": ["concept-notation"],
            "misconception_tags": ["confuses_prior"],
        },
    )
    decision_set = make_decision_set(twin_id=twin.twin_id, decisions=(decision,))
    result = TwinProjectionService().project(
        twin, decision_set, graph_id="lg-struct", projected_at=FIXED_AT
    )
    types = {r.relationship_type for r in result.batch.relationships}
    assert ProjectionRelationshipType.CONCEPT_CONCEPT in types
    assert ProjectionRelationshipType.PREREQUISITE in types
    assert ProjectionRelationshipType.DEPENDENCY in types
    assert ProjectionRelationshipType.STUDENT_MISCONCEPTION in types


def test_validator_rejects_incomplete_provenance_and_bad_versions() -> None:
    from dataclasses import replace

    from app.domain.learning_graph.projections.batch import ProjectionBatch

    twin = make_twin()
    context = ProjectionContext(
        twin_id=twin.twin_id,
        student_id=twin.student.student_id,
        graph_id="lg-1",
        reasoning_request_id="rr-1",
        evidence_bundle_id="bundle-1",
        session_id="sess-1",
        correlation_id="corr-1",
        projection_version=PROJECTION_VERSION,
        decision_version=DECISION_VERSION,
        twin_version=2,
        decision_set_id="eds-1",
    )
    builder = RelationshipBuilder(context=context, created_at=FIXED_AT)
    decision = make_decision(twin_id=twin.twin_id)
    rel = builder.build_explicit(
        relationship_type=ProjectionRelationshipType.STUDENT_CONCEPT,
        from_ref=twin.student.student_id,
        to_ref="concept-bayes",
        decision=decision,
    )
    broken = replace(rel, provenance={"decision_id": decision.decision_id})
    batch = ProjectionBatch(
        batch_id="b1",
        relationships=(broken,),
        context=context,
        projection_version=PROJECTION_VERSION,
    )
    with pytest.raises(IncompleteProjectionProvenance):
        ProjectionValidator().validate(batch)

    bad_ctx = ProjectionContext(
        twin_id=twin.twin_id,
        student_id=twin.student.student_id,
        graph_id="lg-1",
        reasoning_request_id="rr-1",
        evidence_bundle_id="bundle-1",
        session_id="sess-1",
        correlation_id="corr-1",
        projection_version="AP-002D4.projection.v999",
        decision_version=DECISION_VERSION,
        twin_version=2,
        decision_set_id="eds-1",
    )
    bad_batch = ProjectionBatch(
        batch_id="b2",
        relationships=(),
        context=bad_ctx,
        projection_version="AP-002D4.projection.v999",
    )
    with pytest.raises(UnsupportedProjectionVersion):
        ProjectionValidator().validate(bad_batch)

    bad_decision_ctx = ProjectionContext(
        twin_id=twin.twin_id,
        student_id=twin.student.student_id,
        graph_id="lg-1",
        reasoning_request_id="rr-1",
        evidence_bundle_id="bundle-1",
        session_id="sess-1",
        correlation_id="corr-1",
        projection_version=PROJECTION_VERSION,
        decision_version="not-a-decision-version",
        twin_version=2,
        decision_set_id="eds-1",
    )
    bad_decision_batch = ProjectionBatch(
        batch_id="b3",
        relationships=(),
        context=bad_decision_ctx,
        projection_version=PROJECTION_VERSION,
    )
    with pytest.raises(InvalidDecisionVersion):
        ProjectionValidator().validate(bad_decision_batch)


def test_dto_mapper() -> None:
    twin = make_twin(version=2)
    decision_set = make_decision_set(twin_id=twin.twin_id)
    result = TwinProjectionService().project(
        twin, decision_set, graph_id="lg-dto", projected_at=FIXED_AT
    )
    dto = map_projection_result(result)
    assert dto.twin_id == twin.twin_id
    assert dto.projection_version == PROJECTION_VERSION
    assert len(dto.relationships) == result.relationship_count
    assert dto.created_count == result.created_count


def test_graph_argument_and_mismatch() -> None:
    twin = make_twin(version=2)
    graph = make_graph(twin=twin, graph_id="lg-bound")
    decision_set = make_decision_set(twin_id=twin.twin_id)
    result = TwinProjectionService().project(
        twin, decision_set, graph=graph, projected_at=FIXED_AT
    )
    assert result.context.graph_id == "lg-bound"

    other = make_twin(twin_id="twin-other", student_id="student-other", version=2)
    from app.domain.learning_graph.projections.errors import ProjectionRejected

    with pytest.raises(ProjectionRejected):
        TwinProjectionService().project(
            other, make_decision_set(twin_id=other.twin_id), graph=graph
        )


def test_persistence_ledger_lists_relationships() -> None:
    store = ProjectionPersistenceService()
    twin = make_twin(version=2)
    service = TwinProjectionService(persistence=store)
    service.project(
        twin,
        make_decision_set(twin_id=twin.twin_id),
        graph_id="lg-store",
        projected_at=FIXED_AT,
    )
    rels = store.list_relationships(twin_id=twin.twin_id, graph_id="lg-store")
    assert len(rels) >= 3
    events = store.list_events(twin_id=twin.twin_id, graph_id="lg-store")
    assert events
    batches = store.list_batches(twin_id=twin.twin_id, graph_id="lg-store")
    assert len(batches) == 1


def test_student_reasoning_service_untouched_by_projection_package() -> None:
    root = (
        Path(__file__).resolve().parents[3]
        / "app"
        / "application"
        / "student_digital_twin"
        / "student_reasoning_service.py"
    )
    # Regression: D4 must not modify StudentReasoningService. Confirm file still
    # has no TwinProjectionService import (architecture STOP boundary).
    tree = ast.parse(root.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    assert not any("projections" in name for name in imported)
    assert not any("TwinProjection" in name for name in imported)


def test_learning_graph_service_project_twin_decisions(ctx) -> None:
    from dataclasses import replace

    from app.application.learning_graph.learning_graph_service import (
        LearningGraphService,
    )
    from app.application.student_digital_twin.student_digital_twin_service import (
        StudentDigitalTwinService,
    )

    twin = StudentDigitalTwinService().create(
        student_id="s-proj-d4-1",
        display_name="Learner",
        workspace_id="ws-proj",
        subject_code="CS1",
    )
    twin = replace(twin, version=2)
    decision_set = make_decision_set(twin_id=twin.twin_id)
    service = LearningGraphService()
    result = service.project_twin_decisions(
        twin, decision_set, computed_at=FIXED_AT, persist=True
    )
    assert result.relationship_count >= 3
    loaded = service.get_for_twin(twin.twin_id)
    assert loaded is not None
    assert any(
        u.kind.value == "project_from_twin_decisions" for u in loaded.update_history
    )
