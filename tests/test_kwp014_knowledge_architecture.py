"""KWP-014 — Knowledge Architecture / Curriculum Knowledge Graph tests.

Curriculum structure as graph, prerequisite reasoning, pathways, revision
paths, difficulty propagation, Curriculum Map, Adaptive Workspace why,
Educational Memory curriculum movement, and founder metrics.
Does not redesign Learning Runtime / Evidence / Progress / EI engines.
"""

from __future__ import annotations

from pathlib import Path

from app.application.educational_memory.dto import TimelineEventKind
from app.application.educational_memory.timeline import build_learning_timeline
from app.application.knowledge_architecture import (
    EducationalRelationship,
    KnowledgeArchitectureEngine,
    LearnerGraphContext,
    MapTopicStatus,
    RevisionPathKind,
    get_knowledge_architecture_engine,
    reset_knowledge_architecture_engine,
)
from app.application.knowledge_architecture.graph_adapter import (
    graph_from_topic_specs,
)
from app.application.knowledge_architecture.prerequisite_reasoning import (
    explain_topic,
)
from app.domain.curriculum.value_objects.dependency_type import (
    SOFT_DEPENDENCY_TYPES,
    DependencyType,
)
from app.presentation.product_language import APPROVED_TERMS
from app.presentation.student.dto.adaptive_workspace import WorkspaceCurrentFocus
from app.services.knowledge_architecture_metrics import KnowledgeArchitectureMetrics
from tests.domain.curriculum.helpers import build_graph, linear_curriculum

FOUNDER_ALPHA = Path(
    "app/founder/dashboard/templates/founder_dashboard/alpha_observability.html"
)
KG_TMPL = Path("app/templates/student/knowledge_graph.html")
HOME_TMPL = Path("app/templates/student/home.html")

_FORBIDDEN = (
    "digital twin",
    "evidence authority",
    "pass probability",
    "guaranteed",
    "will definitely",
    "cognitive load",
    "overloaded",
    "badge",
    "leaderboard",
)


def _probability_specs() -> list[dict]:
    return [
        {
            "topic_id": "prob",
            "title": "Probability",
            "difficulty": "foundational",
        },
        {
            "topic_id": "cond",
            "title": "Conditional Probability",
            "difficulty": "intermediate",
            "prerequisite_ids": ["prob"],
            "high_dependency_on": ["prob"],
        },
        {
            "topic_id": "bayes",
            "title": "Bayes",
            "difficulty": "intermediate",
            "prerequisite_ids": ["cond"],
            "high_dependency_on": ["cond"],
            "foundation_of": ["cond"],
        },
        {
            "topic_id": "infer",
            "title": "Statistical Inference",
            "difficulty": "advanced",
            "prerequisite_ids": ["bayes"],
        },
        {
            "topic_id": "risk",
            "title": "Risk Modelling",
            "difficulty": "capstone",
            "prerequisite_ids": ["infer"],
            "extension_of": ["infer"],
        },
    ]


def _interest_specs() -> list[dict]:
    return [
        {
            "topic_id": "interest",
            "title": "Interest Theory",
            "difficulty": "foundational",
        },
        {
            "topic_id": "annuities",
            "title": "Annuities",
            "difficulty": "intermediate",
            "prerequisite_ids": ["interest"],
        },
        {
            "topic_id": "loans",
            "title": "Loans",
            "difficulty": "intermediate",
            "prerequisite_ids": ["interest"],
        },
        {
            "topic_id": "bonds",
            "title": "Bonds",
            "difficulty": "advanced",
            "prerequisite_ids": ["interest", "annuities"],
            "revision_with": ["loans"],
            "optional_reinforcement": ["annuities"],
        },
    ]


def test_dependency_type_includes_kwp014_relationships() -> None:
    assert DependencyType.FOUNDATION in SOFT_DEPENDENCY_TYPES
    assert DependencyType.EXTENSION in SOFT_DEPENDENCY_TYPES
    assert DependencyType.HIGH_DEPENDENCY in SOFT_DEPENDENCY_TYPES
    assert DependencyType.REQUIRES not in SOFT_DEPENDENCY_TYPES


def test_graph_from_topic_specs_builds_prerequisites() -> None:
    graph = graph_from_topic_specs(_probability_specs())
    assert graph.topic_count() == 5
    prereqs = graph.find_prerequisites("bayes")
    assert [p.value for p in prereqs] == ["cond"]
    successors = graph.find_successors("cond")
    assert "bayes" in {s.value for s in successors}


def test_prerequisite_reasoning_explains_why_topic_matters() -> None:
    engine = KnowledgeArchitectureEngine.from_topic_specs(_probability_specs())
    explanation = engine.explain("bayes")
    assert explanation.has_explanation
    text = explanation.explanation.lower()
    assert "bayes" in text
    assert "conditional probability" in text
    assert "strengthen" in text or "improving" in text or "improve" in text
    for fragment in _FORBIDDEN:
        assert fragment not in text


def test_prerequisite_reasoning_mentions_recent_strengthening() -> None:
    engine = KnowledgeArchitectureEngine.from_topic_specs(_probability_specs())
    ctx = LearnerGraphContext(
        current_topic_id="bayes",
        recently_strengthened_ids=frozenset({"cond", "conditional probability"}),
    )
    text = engine.why_matters("bayes", context=ctx).lower()
    assert "builds directly" in text or "strengthened" in text


def test_curriculum_pathway_probability_chain() -> None:
    engine = KnowledgeArchitectureEngine.from_topic_specs(_probability_specs())
    paths = engine.pathways()
    assert paths
    topo = paths[0]
    assert "prob" in topo.topic_ids
    assert "bayes" in topo.topic_ids
    assert "risk" in topo.topic_ids
    # Topological: foundations before dependents.
    assert topo.topic_ids.index("prob") < topo.topic_ids.index("cond")
    assert topo.topic_ids.index("cond") < topo.topic_ids.index("bayes")


def test_revision_paths_weak_recovery_exam_mastery() -> None:
    engine = KnowledgeArchitectureEngine.from_topic_specs(_probability_specs())
    ctx = LearnerGraphContext(
        completed_topic_ids=frozenset({"prob"}),
        weak_topic_ids=frozenset({"cond"}),
        current_topic_id="bayes",
        days_to_exam=10,
    )
    paths = engine.revision_paths(context=ctx, seed_topic_id="bayes")
    kinds = {p.kind for p in paths}
    assert RevisionPathKind.WEAK_PREREQUISITE in kinds
    assert RevisionPathKind.RECOVERY in kinds
    assert RevisionPathKind.EXAM_REVISION in kinds
    weak = next(p for p in paths if p.kind is RevisionPathKind.WEAK_PREREQUISITE)
    assert "cond" in weak.topic_ids
    assert weak.has_path


def test_difficulty_propagation_to_successors() -> None:
    engine = KnowledgeArchitectureEngine.from_topic_specs(_interest_specs())
    ctx = LearnerGraphContext(weak_topic_ids=frozenset({"interest"}))
    attention = engine.difficulty_attention(context=ctx, source_topic_id="interest")
    assert attention.has_attention
    titles = {t.lower() for t in attention.attention_titles}
    assert "annuities" in titles
    assert "loans" in titles
    assert "bonds" in titles
    assert "interest theory" in attention.guidance.lower()
    assert "attention" in attention.guidance.lower()


def test_curriculum_map_highlights_statuses() -> None:
    engine = KnowledgeArchitectureEngine.from_topic_specs(_probability_specs())
    ctx = LearnerGraphContext(
        completed_topic_ids=frozenset({"prob"}),
        weak_topic_ids=frozenset({"cond"}),
        current_topic_id="bayes",
    )
    cmap = engine.curriculum_map(context=ctx, subject_label="CS1")
    assert cmap.has_map
    assert cmap.current_topic_title == "Bayes"
    assert cmap.why_current_matters
    by_id = {n.topic_id: n for n in cmap.nodes}
    assert by_id["prob"].status is MapTopicStatus.COMPLETED
    assert by_id["bayes"].status is MapTopicStatus.CURRENT
    assert by_id["cond"].status in {
        MapTopicStatus.WEAK_PREREQUISITE,
        MapTopicStatus.ATTENTION,
    }
    assert by_id["risk"].status is MapTopicStatus.FUTURE


def test_educational_relationship_catalogue() -> None:
    engine = KnowledgeArchitectureEngine.from_topic_specs(_interest_specs())
    rels = {e.relationship for e in engine.edges()}
    assert EducationalRelationship.PREREQUISITE in rels
    assert EducationalRelationship.FREQUENTLY_REVISED_TOGETHER in rels
    assert EducationalRelationship.OPTIONAL_REINFORCEMENT in rels


def test_reuses_existing_curriculum_graph() -> None:
    curriculum = linear_curriculum()
    engine = KnowledgeArchitectureEngine.from_curriculum(curriculum)
    assert engine.graph.topic_count() == 3
    explanation = explain_topic(engine.graph, "c")
    assert explanation.has_explanation
    assert "expectation" in explanation.topic_title.lower()


def test_founder_metrics_snapshot() -> None:
    engine = KnowledgeArchitectureEngine.from_topic_specs(_probability_specs())
    metrics = KnowledgeArchitectureMetrics.from_engine(
        engine,
        completed_topic_ids={"prob", "cond"},
        event_counts={"knowledge_map_opened": 4, "revision_opened": 2},
        subject_label="Demo",
    )
    assert metrics.node_count == 5
    assert metrics.edge_count > 0
    assert metrics.completeness_ratio > 0
    assert metrics.curriculum_coverage_ratio == 0.4
    assert metrics.curriculum_map_opens == 4
    assert metrics.revision_pathway_usage == 2
    assert metrics.bottleneck_topic_ids
    opaque = metrics.to_opaque()
    assert opaque["node_count"] == 5


def test_timeline_curriculum_movement_foundation() -> None:
    packages = [
        {
            "package_id": "p1",
            "student_id": "s1",
            "session_id": "sess-1",
            "topic_title": "Discount Factors",
            "topic_id": "df",
            "difficulty": "foundational",
            "created_at": "2026-01-01T10:00:00+00:00",
            "observations": [
                {"type_id": "EV-RT-07", "payload": {}},
                {"type_id": "EV-RT-07", "payload": {}},
            ],
            "progress_advanced": True,
            "finish_review_verdict": "yes",
        }
    ]
    timeline = build_learning_timeline(packages, student_id="s1")
    kinds = {e.kind for e in timeline}
    assert TimelineEventKind.FOUNDATION_COMPLETE in kinds
    movement = next(
        e for e in timeline if e.kind is TimelineEventKind.FOUNDATION_COMPLETE
    )
    assert movement.curriculum_movement
    assert "foundation" in movement.curriculum_movement.lower()


def test_workspace_current_focus_supports_curriculum_why() -> None:
    focus = WorkspaceCurrentFocus(
        topic_title="Bayes",
        guidance="Practice conditional setups.",
        curriculum_why=(
            "Bayes relies heavily on Conditional Probability. "
            "Strengthening Conditional Probability is expected to improve "
            "your understanding of Bayes."
        ),
        has_focus=True,
    )
    assert focus.curriculum_why
    assert "relies heavily" in focus.curriculum_why


def test_product_language_includes_curriculum_map() -> None:
    assert "Curriculum Map" in APPROVED_TERMS
    assert "Knowledge Architecture" in APPROVED_TERMS


def test_templates_wire_curriculum_map_and_founder() -> None:
    kg = KG_TMPL.read_text(encoding="utf-8")
    assert "Curriculum Map" in kg or "curriculum-map" in kg
    assert "why_current_matters" in kg or "014-why" in kg
    home = HOME_TMPL.read_text(encoding="utf-8")
    # Selective Home: curriculum_why may appear behind "Why this topic matters";
    # Curriculum Map remains a Quick Action. Full current-focus card stays off Home.
    assert "why-this-matters" in home or "Why this topic matters" in home
    assert "Curriculum Map" in home or "knowledge_graph" in home or "quick-actions" in home
    assert 'data-workspace-section="current-focus"' not in home
    session_body = (
        Path("app/templates/session/partials/session_body.html")
    ).read_text(encoding="utf-8")
    assert "session-briefing" in session_body
    founder = FOUNDER_ALPHA.read_text(encoding="utf-8")
    assert "Knowledge Architecture" in founder
    assert "curriculum_map_opens" in founder or "Curriculum Map opens" in founder


def test_curriculum_map_node_omits_placeholder_duration_claims() -> None:
    """Curriculum Map must not render decorative uniform minutes (e.g. '20 min').

    Published packages historically stamped estimated_minutes=20 on every LO.
    Prefer no duration label over false precision until honest per-node data is wired.
    """
    node = Path(
        "app/templates/student/components/knowledge_graph_node.html"
    ).read_text(encoding="utf-8")
    assert "estimated_minutes" not in node or "Do not show estimated_minutes" in node
    assert " min{% endif %}" not in node
    assert "{{ node.estimated_minutes }}" not in node


def test_engine_singleton_reset() -> None:
    reset_knowledge_architecture_engine()
    a = get_knowledge_architecture_engine()
    b = get_knowledge_architecture_engine()
    assert a is b
    reset_knowledge_architecture_engine()


def test_snapshot_completeness_and_bottlenecks() -> None:
    engine = KnowledgeArchitectureEngine.from_topic_specs(_interest_specs())
    snap = engine.snapshot(subject_label="CM1")
    assert snap.node_count == 4
    assert "interest" in snap.bottleneck_topic_ids
    chains = engine.difficult_prerequisite_chains()
    assert chains
    assert len(chains[0]) >= 2


def test_graph_builder_parity_with_domain_helper() -> None:
    graph = build_graph(linear_curriculum())
    engine = KnowledgeArchitectureEngine(graph)
    assert engine.completeness_ratio() > 0
    assert engine.nodes()
    assert engine.edges()
