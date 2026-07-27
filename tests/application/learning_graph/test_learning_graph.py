"""SDT-003 Learning Graph tests."""

from __future__ import annotations

from datetime import datetime
from unittest.mock import MagicMock

from app.application.educational_reasoning.educational_reasoning_service import (
    EducationalReasoningService,
)
from app.application.learning_graph.learning_graph_service import LearningGraphService
from app.application.learning_graph.learning_graph_traversal_service import (
    LearningGraphTraversalService,
)
from app.application.learning_graph.persistence import LearningGraphPersistenceService
from app.application.student_digital_twin.observation_service import ObservationService
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.application.student_digital_twin.student_reasoning_service import (
    StudentReasoningService,
)
from app.domain.curriculum_retrieval.intent import QueryIntent
from app.domain.curriculum_retrieval.profile import RetrievalProfile
from app.domain.curriculum_retrieval.ranking import RankingBreakdown
from app.domain.curriculum_retrieval.result import (
    EvidenceItem,
    RankedEvidence,
    RetrievalResult,
)
from app.domain.educational_reasoning.gap_analysis import PrerequisiteAnalysisRule
from app.domain.educational_reasoning.reasoning_context import (
    CurriculumEvidenceBundle,
    ReasoningContext,
)
from app.domain.educational_reasoning.recommendation_rule import RecommendationRule
from app.domain.learning_graph.graph_edge import GraphEdge
from app.domain.learning_graph.graph_node import GraphNode, PrerequisiteStatus
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.learning_graph.relationship import RelationshipType
from app.domain.student_digital_twin.knowledge_gap import GapSeverity, KnowledgeGap
from app.domain.student_digital_twin.mastery import MasteryMap, MasteryRecord
from app.domain.student_digital_twin.observation import ObservationKind
from app.models.learning_graph import (
    LgGraphEdge,
    LgGraphNode,
    LgLearningGraph,
)
from tests.presentation.curriculum_studio.helpers import login_founder


def _ranking() -> RankingBreakdown:
    return RankingBreakdown(
        semantic_similarity=0.5,
        graph_proximity=0.8,
        confidence=0.9,
        founder_verification=1.0,
        document_version=0.5,
        entity_freshness=0.5,
        relationship_strength=0.7,
        evidence_count=0.5,
        rank_score=0.88,
    )


def _make_retrieval_stub(
    *,
    concept_id: str = "concept-bayes",
    prerequisites: tuple[str, ...] = ("concept-conditional",),
    related: tuple[str, ...] = (),
) -> MagicMock:
    stub = MagicMock()
    evidence = (
        EvidenceItem(
            evidence_id="ev-1",
            role="definition",
            excerpt="Bayes theorem definition",
            entity_id=concept_id,
        ),
    )
    ranked = RankedEvidence(
        entity_id=concept_id,
        kind="concept",
        title="Bayes Theorem",
        body="definition",
        document_id=1,
        version_label="2026",
        confidence=0.9,
        confidence_band="high",
        verified=True,
        provenance_id="prov-1",
        rank_score=0.88,
        ranking=_ranking(),
        evidence=evidence,
        prerequisites=prerequisites,
        related_concepts=related,
        supporting_formulae=(),
        worked_examples=(),
        practice_questions=(),
        learning_objectives=(),
        graph_distance=1,
    )
    # Also return evidence for prerequisite so multi-hop sync can expand if needed.
    stub.retrieve.return_value = RetrievalResult(
        query_text="Bayes",
        intent=QueryIntent.DEFINITION,
        profile=RetrievalProfile.STUDENT_DIGITAL_TWIN,
        results=(ranked,),
        concept_ids=(concept_id,),
        learning_objective_ids=(),
        definition_ids=(),
        formula_ids=(),
        example_ids=(),
        practice_question_ids=(),
        prerequisite_ids=prerequisites,
        related_concept_ids=related,
        retrieval_log_id="retr-1",
    )
    return stub


def _chain_graph() -> LearningGraph:
    """Bayes → Conditional → Probability Trees (prerequisites point to foundations)."""
    graph = LearningGraph.create(
        graph_id="lg-test",
        twin_id="twin-test",
        student_id="student-1",
        created_at=datetime(2026, 7, 27, 12, 0, 0),
    )
    nodes = (
        GraphNode(
            node_id="n-bayes",
            graph_id="lg-test",
            concept_id="concept-bayes",
            concept_title="Bayes Theorem",
            mastery_link_id="m-bayes",
            mastery_score=0.30,
            confidence=0.5,
            evidence_count=3,
            prerequisite_status=PrerequisiteStatus.UNMET,
        ),
        GraphNode(
            node_id="n-cond",
            graph_id="lg-test",
            concept_id="concept-conditional",
            concept_title="Conditional Probability",
            mastery_link_id="m-cond",
            mastery_score=0.40,
            confidence=0.5,
            evidence_count=2,
            prerequisite_status=PrerequisiteStatus.UNMET,
        ),
        GraphNode(
            node_id="n-trees",
            graph_id="lg-test",
            concept_id="concept-trees",
            concept_title="Probability Trees",
            mastery_link_id="m-trees",
            mastery_score=0.35,
            confidence=0.5,
            evidence_count=2,
            prerequisite_status=PrerequisiteStatus.NONE,
        ),
    )
    edges = (
        GraphEdge(
            edge_id="e1",
            graph_id="lg-test",
            from_concept_id="concept-bayes",
            to_concept_id="concept-conditional",
            relationship_type=RelationshipType.PREREQUISITE,
            strength=0.9,
            confidence=0.9,
            provenance="test",
            supporting_evidence=("ev-1",),
        ),
        GraphEdge(
            edge_id="e2",
            graph_id="lg-test",
            from_concept_id="concept-conditional",
            to_concept_id="concept-trees",
            relationship_type=RelationshipType.PREREQUISITE,
            strength=0.85,
            confidence=0.85,
            provenance="test",
            supporting_evidence=("ev-2",),
        ),
    )
    return graph.with_structure(nodes=nodes, edges=edges)


# ── Domain traversal ─────────────────────────────────────────────────────


def test_prerequisite_traversal_is_deterministic():
    graph = _chain_graph()
    first = graph.traverse_prerequisites("concept-bayes")
    second = graph.traverse_prerequisites("concept-bayes")
    assert first.visited_concept_ids == second.visited_concept_ids
    assert "concept-conditional" in first.visited_concept_ids
    assert "concept-trees" in first.visited_concept_ids
    depths = first.depths()
    assert depths["concept-bayes"] == 0
    assert depths["concept-conditional"] == 1
    assert depths["concept-trees"] == 2


def test_dependency_traversal_finds_dependents():
    graph = _chain_graph()
    result = graph.traverse_dependencies("concept-trees")
    assert "concept-conditional" in result.visited_concept_ids
    assert "concept-bayes" in result.visited_concept_ids


def test_recovery_path_orders_foundations_first():
    graph = _chain_graph()
    path = graph.recovery_path("concept-bayes")
    assert path.concept_ids[0] == "concept-trees"
    assert path.concept_ids[-1] == "concept-bayes"
    assert "concept-conditional" in path.concept_ids


def test_learning_path_and_impact():
    graph = _chain_graph()
    trav = LearningGraphTraversalService()
    path = trav.learning_path(graph, "concept-bayes")
    assert path.concept_ids[-1] == "concept-bayes"
    impact = trav.impact(graph, "concept-trees")
    assert "concept-bayes" in impact.impacted_concept_ids


# ── Graph lifecycle / persistence ────────────────────────────────────────


def test_graph_created_with_twin(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-lg-1",
        display_name="Learner",
        workspace_id="ws-1",
        subject_code="CS1",
    )
    graph = LearningGraphService().get_for_twin(twin.twin_id)
    assert graph is not None
    assert graph.twin_id == twin.twin_id
    assert LgLearningGraph.query.filter_by(twin_id=twin.twin_id).count() == 1


def test_node_and_edge_creation_via_sync(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-lg-2",
        workspace_id="ws-1",
        subject_code="CS1",
    )
    twin, _ = ObservationService().record(
        twin,
        kind=ObservationKind.QUESTION_ANSWERED,
        curriculum_entity_id="concept-bayes",
        metadata={"concept_title": "Bayes Theorem", "correct": False, "score": 0.2},
        persist=True,
    )
    twin = StudentDigitalTwinService().get(twin.twin_id)
    stub = _make_retrieval_stub(
        prerequisites=("concept-conditional",),
        related=("concept-related",),
    )
    # Seed prior mastery so sync has a node to attach edges to.
    from app.domain.student_digital_twin.mastery import MasteryTrend

    twin = twin.with_inferences(
        mastery=MasteryMap(
            records=(
                MasteryRecord(
                    mastery_id="m-bayes",
                    twin_id=twin.twin_id,
                    concept_id="concept-bayes",
                    concept_title="Bayes Theorem",
                    mastery_score=0.3,
                    confidence=0.5,
                    trend=MasteryTrend.DECLINING,
                    evidence_count=2,
                ),
            )
        )
    )
    evidence = CurriculumEvidenceBundle(
        by_concept={
            "concept-bayes": stub.retrieve.return_value,
        },
        all_evidence_ids=("ev-1",),
        retrieval_log_ids=("retr-1",),
    )
    graph = LearningGraphService().sync(twin, evidence=evidence, persist=True)
    assert graph.get_node("concept-bayes") is not None
    assert graph.get_node("concept-conditional") is not None  # stub from edge
    prereqs = graph.direct_prerequisites("concept-bayes")
    assert "concept-conditional" in prereqs
    assert LgGraphNode.query.filter_by(graph_id=graph.graph_id).count() >= 2
    assert LgGraphEdge.query.filter_by(graph_id=graph.graph_id).count() >= 1


def test_graph_persistence_roundtrip(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-lg-3",
        workspace_id="ws-1",
        subject_code="CS1",
    )
    graph = LearningGraphService().get_for_twin(twin.twin_id)
    assert graph is not None
    updated = graph.with_node(
        GraphNode(
            node_id="n1",
            graph_id=graph.graph_id,
            concept_id="c1",
            concept_title="Concept One",
            mastery_score=0.5,
            confidence=0.6,
            evidence_count=1,
        )
    )
    updated = updated.with_edge(
        GraphEdge(
            edge_id="e1",
            graph_id=graph.graph_id,
            from_concept_id="c1",
            to_concept_id="c0",
            relationship_type=RelationshipType.PREREQUISITE,
            strength=1.0,
            confidence=0.8,
            provenance="test",
        )
    )
    updated = LearningGraphService()._builder.ensure_stub_nodes(updated)
    LearningGraphPersistenceService().replace_structure(updated)
    from app.extensions import db

    db.session.commit()

    loaded = LearningGraphService().get_for_twin(twin.twin_id)
    assert loaded is not None
    assert loaded.get_node("c1") is not None
    assert loaded.get_node("c0") is not None
    assert any(
        e.relationship_type is RelationshipType.PREREQUISITE for e in loaded.edges
    )


# ── Educational Reasoning integration ────────────────────────────────────


def test_prerequisite_rule_uses_learning_graph():
    graph = _chain_graph()
    gap = KnowledgeGap(
        gap_id="gap-1",
        twin_id="twin-test",
        concept_id="concept-bayes",
        concept_title="Bayes Theorem",
        severity=GapSeverity.HIGH,
        confidence=0.8,
        supporting_evidence=("ev-1",),
        reason="weak mastery",
        identified_at=datetime(2026, 7, 27, 12, 0, 0),
    )
    context = ReasoningContext(
        twin_id="twin-test",
        student_id="student-1",
        workspace_id="ws-1",
        subject_code="CS1",
        observations=(),
        observation_ids=(),
        prior_mastery=MasteryMap.empty(),
        curriculum_evidence=CurriculumEvidenceBundle.empty(),
        triggered_by="test",
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
        learning_graph=graph,
        gaps=(gap,),
    )
    execution = PrerequisiteAnalysisRule().apply(context)
    assert execution.gaps
    assert execution.gaps[0].likely_prerequisite_id == "concept-conditional"
    assert execution.outputs.get("graph_sourced") == 1


def test_recommendation_rule_is_graph_driven():
    graph = _chain_graph()
    gap = KnowledgeGap(
        gap_id="gap-1",
        twin_id="twin-test",
        concept_id="concept-bayes",
        concept_title="Bayes Theorem",
        severity=GapSeverity.HIGH,
        confidence=0.8,
        likely_prerequisite_id="concept-conditional",
        likely_prerequisite_title="Conditional Probability",
        supporting_evidence=("ev-1",),
        reason="weak mastery",
        identified_at=datetime(2026, 7, 27, 12, 0, 0),
    )
    context = ReasoningContext(
        twin_id="twin-test",
        student_id="student-1",
        workspace_id="ws-1",
        subject_code="CS1",
        observations=(),
        observation_ids=(),
        prior_mastery=MasteryMap.empty(),
        curriculum_evidence=CurriculumEvidenceBundle.empty(),
        triggered_by="test",
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
        learning_graph=graph,
        gaps=(gap,),
    )
    execution = RecommendationRule().apply(context)
    assert execution.recommendations
    assert execution.outputs.get("graph_driven") == 1
    # Deepest foundation on recovery path
    assert "Probability Trees" in execution.recommendations[0].title
    assert "Graph recovery path" in execution.recommendations[0].reason


def test_reasoning_pipeline_syncs_graph(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-lg-4",
        workspace_id="ws-1",
        subject_code="CS1",
    )
    twin, _ = ObservationService().record(
        twin,
        kind=ObservationKind.QUESTION_ANSWERED,
        curriculum_entity_id="concept-bayes",
        metadata={"concept_title": "Bayes Theorem", "correct": False, "score": 0.1},
        persist=True,
    )
    stub = _make_retrieval_stub()
    reasoning = EducationalReasoningService(retrieval=stub)
    result = reasoning.reason_for_twin(twin, triggered_by="test", persist=True)
    assert result.run_id
    graph = LearningGraphService().get_for_twin(twin.twin_id)
    assert graph is not None
    assert graph.node_count >= 1


def test_sdt001_sdt002_regression_with_graph(ctx):
    """Full Twin reasoning still works; Learning Graph coexists."""
    twin = StudentDigitalTwinService().create(
        student_id="s-lg-5",
        workspace_id="ws-1",
        subject_code="CS1",
    )
    twin, _ = ObservationService().record(
        twin,
        kind=ObservationKind.QUESTION_ANSWERED,
        curriculum_entity_id="concept-bayes",
        metadata={"concept_title": "Bayes Theorem", "correct": True, "score": 0.9},
        persist=True,
    )
    twin, _ = ObservationService().record(
        twin,
        kind=ObservationKind.QUESTION_ANSWERED,
        curriculum_entity_id="concept-bayes",
        metadata={"concept_title": "Bayes Theorem", "correct": False, "score": 0.2},
        persist=True,
    )
    stub = _make_retrieval_stub()
    updated = StudentReasoningService(retrieval=stub).reason(
        twin, triggered_by="regression", persist=True
    )
    assert updated.mastery.records
    assert updated.learning_state.snapshot_id
    graph = LearningGraphService().get_for_twin(updated.twin_id)
    assert graph is not None
    # Mastery projections refreshed from Twin
    node = graph.get_node("concept-bayes")
    assert node is not None
    assert node.mastery_link_id


# ── Founder diagnostics ──────────────────────────────────────────────────


def test_founder_learning_graph_endpoints(client, app, ctx):
    login_founder(client, app)
    twin = StudentDigitalTwinService().create(
        student_id="s-lg-diag",
        workspace_id="ws-1",
        subject_code="CS1",
    )
    graph = _chain_graph()
    real = LearningGraphService().get_for_twin(twin.twin_id)
    assert real is not None
    nodes = tuple(
        GraphNode(
            node_id=n.node_id,
            graph_id=real.graph_id,
            concept_id=n.concept_id,
            concept_title=n.concept_title,
            mastery_link_id=n.mastery_link_id,
            mastery_score=n.mastery_score,
            confidence=n.confidence,
            evidence_count=n.evidence_count,
            trend=n.trend,
            prerequisite_status=n.prerequisite_status,
        )
        for n in graph.nodes
    )
    edges = tuple(
        GraphEdge(
            edge_id=e.edge_id,
            graph_id=real.graph_id,
            from_concept_id=e.from_concept_id,
            to_concept_id=e.to_concept_id,
            relationship_type=e.relationship_type,
            strength=e.strength,
            confidence=e.confidence,
            provenance=e.provenance,
            supporting_evidence=e.supporting_evidence,
        )
        for e in graph.edges
    )
    synced = real.with_structure(nodes=nodes, edges=edges)
    LearningGraphPersistenceService().replace_structure(synced)
    from app.extensions import db

    db.session.commit()

    r = client.get(f"/founder/learning-graph/{twin.student.student_id}")
    assert r.status_code == 200
    assert r.get_json()["ok"] is True

    r = client.get(
        "/founder/learning-graph/prerequisites",
        query_string={
            "twin_id": twin.twin_id,
            "concept_id": "concept-bayes",
        },
    )
    assert r.status_code == 200
    body = r.get_json()
    assert "concept-trees" in body["prerequisites"]["visited_concept_ids"]

    r = client.get(
        "/founder/learning-graph/dependencies",
        query_string={
            "twin_id": twin.twin_id,
            "concept_id": "concept-trees",
        },
    )
    assert r.status_code == 200
    assert "concept-bayes" in r.get_json()["dependencies"]["visited_concept_ids"]

    r = client.get(
        "/founder/learning-graph/traverse",
        query_string={
            "twin_id": twin.twin_id,
            "concept_id": "concept-bayes",
            "kind": "recovery",
        },
    )
    assert r.status_code == 200
    assert r.get_json()["kind"] == "recovery"
