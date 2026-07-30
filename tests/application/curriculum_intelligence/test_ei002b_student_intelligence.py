"""EI-002B — Certified Learning Experience: student integrations + observatory."""

from __future__ import annotations

import pytest

from app.application.curriculum_intelligence.certified_adaptive_learning_service import (  # noqa: E501
    CertifiedAdaptiveLearningService,
)
from app.application.curriculum_intelligence.certified_learning_service import (
    CertifiedLearningService,
)
from app.application.curriculum_intelligence.certified_mission_engine import (
    CertifiedMissionEngine,
)
from app.application.curriculum_intelligence.certified_progress_engine import (
    CertifiedProgressEngine,
)
from app.application.curriculum_intelligence.certified_tutor_context_service import (
    CertifiedTutorContextService,
)
from app.application.curriculum_intelligence.curriculum_observatory import (
    CurriculumObservatory,
)
from app.application.curriculum_intelligence.in_memory_generation_store import (
    InMemoryGenerationStore,
)
from app.application.curriculum_intelligence.learner_knowledge_graph_service import (
    LearnerKnowledgeGraphBuilder,
    assert_certified_package,
)
from app.domain.curriculum_intelligence.certified_learning import (
    CertifiedNodeKind,
    MissionSelectionReason,
)
from app.domain.curriculum_intelligence.confidence import (
    ConfidenceBand,
    ConfidenceRecord,
)
from app.domain.curriculum_intelligence.generation import (
    CalibrationProfile,
    CertificationDecision,
    CertificationOutcome,
    CurriculumGenerationSnapshot,
    DifficultyBiasStyle,
    EducationalNode,
    Generation,
    GranularityStyle,
    HierarchyStyle,
    LineageRecord,
    QualitySnapshot,
    SnapshotStatus,
    TopicDensityStyle,
)

FIXED_TS = "2026-07-30T12:00:00Z"


def _certified_package(**overrides: object) -> dict:
    package = {
        "subject_code": "CS1",
        "version_label": "2026.7",
        "certification": {
            "chain_id": "chain-cs1",
            "snapshot_id": "snap-g7",
            "status": "certified",
            "authority": "certified_snapshot",
        },
        "structure": {
            "sections": [
                {
                    "section_id": "cs1-ch1",
                    "code": "1",
                    "title": "Foundations",
                    "number": "1",
                    "order_index": 1,
                },
                {
                    "section_id": "cs1-ch2",
                    "code": "2",
                    "title": "Systems",
                    "number": "2",
                    "order_index": 2,
                },
            ],
            "topics": [
                {
                    "topic_id": "cs1-t1",
                    "code": "1.1",
                    "title": "Binary representation",
                    "section_ref": "cs1-ch1",
                    "number": "1.1",
                    "order_index": 1,
                    "estimated_minutes": 45,
                    "difficulty": "foundational",
                    "prerequisite_ids": [],
                },
                {
                    "topic_id": "cs1-t2",
                    "code": "1.2",
                    "title": "Logic gates",
                    "section_ref": "cs1-ch1",
                    "number": "1.2",
                    "order_index": 2,
                    "estimated_minutes": 60,
                    "difficulty": "intermediate",
                    "prerequisite_ids": ["cs1-t1"],
                },
                {
                    "topic_id": "cs1-t3",
                    "code": "2.1",
                    "title": "Operating systems intro",
                    "section_ref": "cs1-ch2",
                    "number": "2.1",
                    "order_index": 3,
                    "estimated_minutes": 90,
                    "difficulty": "advanced",
                    "prerequisite_ids": ["cs1-t2"],
                },
            ],
            "objectives": [
                {
                    "objective_id": "cs1-o1",
                    "code": "1.1.1",
                    "text": "Convert between binary and decimal",
                    "topic_ref": "cs1-t1",
                    "number": "1.1.1",
                    "order_index": 1,
                    "estimated_minutes": 20,
                },
                {
                    "objective_id": "cs1-o2",
                    "code": "1.2.1",
                    "text": "Explain AND/OR/NOT gate behaviour",
                    "topic_ref": "cs1-t2",
                    "number": "1.2.1",
                    "order_index": 1,
                    "estimated_minutes": 25,
                },
                {
                    "objective_id": "cs1-o3",
                    "code": "2.1.1",
                    "text": "Describe process scheduling basics",
                    "topic_ref": "cs1-t3",
                    "number": "2.1.1",
                    "order_index": 1,
                    "estimated_minutes": 30,
                },
            ],
            "prerequisite_edges": [["cs1-t2", "cs1-t1"], ["cs1-t3", "cs1-t2"]],
            "calibration": {
                "difficulty_bias": "balanced",
                "topic_density": "consolidated",
                "granularity": "balanced",
            },
            "metadata": [["provider", "EI-002B"]],
        },
    }
    package.update(overrides)
    return package


def test_assert_certified_package_rejects_raw_authority():
    package = _certified_package()
    package["certification"] = {
        "authority": "raw_parser",
        "status": "draft",
    }
    with pytest.raises(ValueError, match="non-certified"):
        assert_certified_package(package)


def test_knowledge_graph_integrity_from_certified_nodes():
    graph = LearnerKnowledgeGraphBuilder().build(_certified_package())
    assert graph.curriculum_identity == "CS1:2026.7"
    assert graph.provenance.is_certified
    assert graph.provenance.snapshot_id == "snap-g7"
    assert {n.node_id for n in graph.objectives()} == {
        "cs1-o1",
        "cs1-o2",
        "cs1-o3",
    }
    assert graph.prerequisites("cs1-t2") == ("cs1-t1",)
    assert "cs1-o1" in graph.children("cs1-t1")
    assert graph.node("cs1-ch1").kind is CertifiedNodeKind.CHAPTER


def test_mission_generation_from_certified_learning_objectives():
    mission = CertifiedMissionEngine().generate(
        _certified_package(),
        mission_id="msn-test-1",
    )
    assert mission.mission_id == "msn-test-1"
    assert mission.topic_id == "cs1-t1"
    assert mission.objective_ids == ("cs1-o1",)
    assert MissionSelectionReason.NEXT_UNCOVERED_OBJECTIVE in mission.selection_reasons
    assert mission.provenance.authority == "certified_snapshot"
    assert mission.calibration_notes


def test_mission_generation_respects_prerequisites_and_progress():
    mission = CertifiedMissionEngine().generate(
        _certified_package(),
        completed_node_ids=("cs1-t1",),
        mastered_objective_ids=("cs1-o1",),
    )
    assert mission.topic_id == "cs1-t2"
    assert mission.objective_ids == ("cs1-o2",)
    assert MissionSelectionReason.PREREQUISITE_READY in mission.selection_reasons


def test_mission_generation_blocks_when_prerequisites_unsatisfied():
    # Completing t1 only; t3 still blocked by t2.
    mission = CertifiedMissionEngine().generate(
        _certified_package(),
        completed_node_ids=("cs1-t1",),
        mastered_objective_ids=("cs1-o1",),
        preferred_difficulty="advanced",
        calibration={"difficulty_bias": "advanced"},
    )
    # Even with advanced preference, t3 is blocked; t2 is selected.
    assert mission.topic_id == "cs1-t2"


def test_tutor_context_certified_nodes_only():
    ctx = CertifiedTutorContextService().build(
        _certified_package(),
        primary_node_id="cs1-o1",
        candidate_node_ids=("cs1-o2", "foreign-node", "cs1-t1"),
        excerpts=(
            ("cs1-o1", "Convert binary"),
            ("foreign-node", "should be dropped"),
        ),
        context_id="ctc-1",
    )
    assert ctx.context_id == "ctc-1"
    assert ctx.primary_node_id == "cs1-o1"
    assert "foreign-node" in ctx.rejected_foreign_ids
    assert all(nid != "foreign-node" for nid, _ in ctx.excerpts)
    assert ctx.provenance.snapshot_id == "snap-g7"
    assert "cs1-o1" in ctx.allowed_node_ids


def test_tutor_rejects_non_certified_primary():
    with pytest.raises(ValueError, match="not a certified"):
        CertifiedTutorContextService().build(
            _certified_package(),
            primary_node_id="not-in-graph",
        )


def test_progress_tracking_stable_node_ids():
    progress = CertifiedProgressEngine().snapshot(
        _certified_package(),
        completed_node_ids=("cs1-t1",),
        objective_mastery={"cs1-o1": 0.9, "cs1-o2": 0.2},
        topic_mastery={"cs1-t1": 0.85, "cs1-t2": 0.2},
        attempts_by_node={"cs1-o1": 3},
    )
    assert progress.curriculum_identity == "CS1:2026.7"
    assert progress.provenance.chain_id == "chain-cs1"
    by_obj = {r.node_id: r for r in progress.objective_records}
    assert by_obj["cs1-o1"].mastery == 0.9
    assert by_obj["cs1-o1"].attempts == 3
    assert "cs1-o3" in progress.missed_objective_ids
    assert 0.0 <= progress.subject_mastery <= 1.0
    assert {r.node_id for r in progress.chapter_records} >= {"cs1-ch1", "cs1-ch2"}


def test_adaptive_learning_operational():
    plan = CertifiedAdaptiveLearningService().plan(
        _certified_package(),
        completed_node_ids=("cs1-t1",),
        objective_mastery={"cs1-o1": 0.95, "cs1-o2": 0.2, "cs1-o3": 0.0},
        topic_mastery={"cs1-t1": 0.9, "cs1-t2": 0.25, "cs1-t3": 0.0},
    )
    assert plan.missed_objectives
    assert any(s.node_id == "cs1-t2" for s in plan.weak_concepts)
    assert any(s.kind == "revision_priority" for s in plan.revision_priorities)
    # t3 depends on t2 which is weak / incomplete.
    assert any(s.kind == "concept_dependency" for s in plan.concept_dependencies)


def _node(
    node_id: str, *, kind: str = "topic", parent: str | None = None
) -> EducationalNode:
    return EducationalNode(
        node_id=node_id,
        generation_local_id=node_id,
        title=node_id,
        kind=kind,
        role=None,
        parent_node_id=parent,
        confidence=ConfidenceRecord(
            confidence_id=f"conf-{node_id}",
            subject_kind="node",
            subject_id=node_id,
            score=0.9,
            band=ConfidenceBand.HIGH,
            reason="fixture",
            factors=(),
            needs_review=False,
            review_threshold=0.55,
        ),
        lineage=LineageRecord(
            created_generation="g1",
            created_generation_index=1,
            last_modified_generation="g7",
            last_modified_generation_index=7,
            operations=(),
        ),
        active=True,
    )


def _snapshot(
    store: InMemoryGenerationStore,
    *,
    chain_id: str,
    snapshot_id: str,
    generation_index: int,
    workspace_id: str = "ws-obs",
) -> None:
    gen = Generation(
        generation_id=f"gen-{snapshot_id}",
        chain_id=chain_id,
        generation_index=generation_index,
        purpose=f"purpose-{generation_index}",
        parent_generation_ids=(),
        source_document_ids=(1,),
        workspace_id=workspace_id,
        created_at_iso=FIXED_TS,
    )
    snap = CurriculumGenerationSnapshot(
        snapshot_id=snapshot_id,
        generation=gen,
        nodes=(_node("n1", kind="topic"),),
        rejected_nodes=(),
        metrics=QualitySnapshot(
            coverage=0.95,
            hierarchy=0.8,
            duplicates=0.0,
            noise=0.0,
            granularity=0.7,
            confidence=0.9,
            evidence_quality=0.88,
        ),
        provenance_bundle_id=f"prov-{snapshot_id}",
        created_at_iso=FIXED_TS,
        status=SnapshotStatus.ACCEPTED,
    )
    store.append_snapshot(snap)
    store.set_active_snapshot(chain_id, snapshot_id)


def test_curriculum_observatory_metrics():
    store = InMemoryGenerationStore()
    store.ensure_chain("chain-cs1", "ws-obs")
    _snapshot(store, chain_id="chain-cs1", snapshot_id="s6", generation_index=6)
    _snapshot(store, chain_id="chain-cs1", snapshot_id="s7a", generation_index=7)
    _snapshot(store, chain_id="chain-cs1", snapshot_id="s7b", generation_index=7)
    store.append_certification(
        CertificationDecision(
            decision_id="d1",
            chain_id="chain-cs1",
            snapshot_id="s7a",
            outcome=CertificationOutcome.CERTIFIED_WITH_WARNINGS,
            quality_score=82.0,
            confidence=0.8,
            coverage=0.92,
            hierarchy_score=0.75,
            granularity_score=0.7,
            warnings=("diet_mismatch",),
            hard_gate_failures=(),
            created_at_iso=FIXED_TS,
            evidence_quality=0.8,
            decision_quality=0.78,
        )
    )
    store.append_certification(
        CertificationDecision(
            decision_id="d2",
            chain_id="chain-cs1",
            snapshot_id="s7b",
            outcome=CertificationOutcome.CERTIFIED,
            quality_score=90.0,
            confidence=0.93,
            coverage=0.97,
            hierarchy_score=0.85,
            granularity_score=0.8,
            warnings=(),
            hard_gate_failures=(),
            created_at_iso=FIXED_TS,
            evidence_quality=0.94,
            decision_quality=0.9,
        )
    )
    store.save_calibration_profile(
        CalibrationProfile(
            profile_id="cal-1",
            workspace_id="ws-obs",
            granularity=GranularityStyle.BALANCED,
            hierarchy=HierarchyStyle.BALANCED,
            topic_density=TopicDensityStyle.CONSOLIDATED,
            difficulty_bias=DifficultyBiasStyle.BALANCED,
            created_at_iso=FIXED_TS,
        )
    )

    report = CurriculumObservatory(store).report_for_workspace("ws-obs")
    assert report.chain_id == "chain-cs1"
    assert report.policy_warnings
    assert any(m.name.startswith("outcome_") for m in report.certification_trends)
    assert any(m.name == "calibration_runs" for m in report.calibration_frequency)
    assert report.decision_quality
    assert report.evidence_quality
    assert report.coverage_metrics


def test_certified_learning_facade_end_to_end():
    package = _certified_package()
    service = CertifiedLearningService(store=InMemoryGenerationStore())
    graph = service.knowledge_graph(package)
    mission = service.generate_daily_mission(package, mission_id="facade-1")
    progress = service.progress(package, completed_node_ids=())
    adaptive = service.adaptive_plan(package, progress=progress)
    tutor = service.tutor_context(package, primary_node_id="cs1-o1")

    assert graph.nodes
    assert mission.objective_ids
    assert progress.coverage_ratio == 0.0
    assert adaptive.missed_objectives
    assert tutor.provenance.authority == "certified_snapshot"


def test_certification_pipeline_unchanged_contract_surface():
    """EI-002B must not alter Gen 7 certification decision shape."""
    decision = CertificationDecision(
        decision_id="keep",
        chain_id="c",
        snapshot_id="s",
        outcome=CertificationOutcome.CERTIFIED,
        quality_score=90.0,
        confidence=0.9,
        coverage=1.0,
        hierarchy_score=0.8,
        granularity_score=0.8,
        warnings=(),
        hard_gate_failures=(),
        created_at_iso=FIXED_TS,
        evidence_quality=0.9,
        decision_quality=0.9,
    )
    assert decision.certification_status is CertificationOutcome.CERTIFIED
    assert decision.decision_quality == 0.9
