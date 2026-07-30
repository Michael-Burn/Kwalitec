"""EI-001B Generation 1–3 Agents + generation hash + regression metrics."""

from __future__ import annotations

import pytest

from app.application.curriculum_intelligence.agents import (
    HierarchyConstructionAgent,
    NoiseEliminationAgent,
    RawGraphAgent,
    default_phase_b_runners,
)
from app.application.curriculum_intelligence.exceptions import SnapshotImmutableError
from app.application.curriculum_intelligence.generation_hash import (
    compute_generation_hash,
)
from app.application.curriculum_intelligence.generation_orchestrator import (
    GenerationOrchestrator,
)
from app.application.curriculum_intelligence.generation_quality import (
    compute_quality_snapshot,
)
from app.application.curriculum_intelligence.in_memory_generation_store import (
    InMemoryGenerationStore,
)
from app.application.curriculum_intelligence.mock_generation_runners import (
    MockPassThroughRunner,
    default_mock_runners,
)
from app.application.curriculum_intelligence.regression_guard import RegressionGuard
from app.domain.curriculum_intelligence.content_role import ContentRole
from app.domain.curriculum_intelligence.extracted_document import (
    BlockKind,
    ExtractedBlock,
    ExtractedDocument,
    ExtractedPage,
)
from app.domain.curriculum_intelligence.generation import (
    LineageOperationKind,
    QualitySnapshot,
    SnapshotStatus,
)


def _syllabus_doc() -> ExtractedDocument:
    """Mini CS1 syllabus fixture mirroring EQ-001 educational quality tests."""
    return ExtractedDocument(
        extraction_id="ei001b-syl",
        document_id=101,
        page_count=2,
        metadata=(
            ("title", "Actuarial Statistics (CS1) Syllabus"),
            ("document_kind", "syllabus"),
        ),
        pages=(
            ExtractedPage(
                page_number=1,
                width=612.0,
                height=792.0,
                blocks=(
                    ExtractedBlock(
                        block_id="b1",
                        kind=BlockKind.HEADING,
                        text="Associateship Qualification",
                        order_index=0,
                    ),
                    ExtractedBlock(
                        block_id="b2",
                        kind=BlockKind.HEADING,
                        text="Actuarial Statistics (CS1)",
                        order_index=1,
                    ),
                    ExtractedBlock(
                        block_id="b3",
                        kind=BlockKind.PARAGRAPH,
                        text="Syllabus for the 2026 Examinations",
                        order_index=2,
                    ),
                    ExtractedBlock(
                        block_id="b4",
                        kind=BlockKind.HEADING,
                        text="April 2025",
                        order_index=3,
                    ),
                ),
                raw_text="Associateship Qualification\nActuarial Statistics (CS1)",
            ),
            ExtractedPage(
                page_number=2,
                width=612.0,
                height=792.0,
                blocks=(
                    ExtractedBlock(
                        block_id="b5",
                        kind=BlockKind.HEADING,
                        text="Aim",
                        order_index=0,
                    ),
                    ExtractedBlock(
                        block_id="b6",
                        kind=BlockKind.PARAGRAPH,
                        text="This subject provides…",
                        order_index=1,
                    ),
                    ExtractedBlock(
                        block_id="b7",
                        kind=BlockKind.HEADING,
                        text="Objectives",
                        order_index=2,
                    ),
                    ExtractedBlock(
                        block_id="b8",
                        kind=BlockKind.HEADING,
                        text="1 Data analysis [10%]",
                        order_index=3,
                    ),
                    ExtractedBlock(
                        block_id="b9",
                        kind=BlockKind.PARAGRAPH,
                        text="1.1 Describe the purpose and function of data analysis",
                        order_index=4,
                    ),
                    ExtractedBlock(
                        block_id="b10",
                        kind=BlockKind.PARAGRAPH,
                        text="1.1.1 Aims of a data analysis (e.g. descriptive)",
                        order_index=5,
                    ),
                    ExtractedBlock(
                        block_id="b11",
                        kind=BlockKind.PARAGRAPH,
                        text=(
                            "1.1.2 Stages and suitable tools used "
                            "to conduct a data analysis"
                        ),
                        order_index=6,
                    ),
                    ExtractedBlock(
                        block_id="b12",
                        kind=BlockKind.PARAGRAPH,
                        text="1.2 Complete exploratory data analysis",
                        order_index=7,
                    ),
                    ExtractedBlock(
                        block_id="b13",
                        kind=BlockKind.PARAGRAPH,
                        text=(
                            "1.2.1 Appropriate tools to calculate "
                            "suitable summary statistics"
                        ),
                        order_index=8,
                    ),
                    ExtractedBlock(
                        block_id="b14",
                        kind=BlockKind.HEADING,
                        text="2 Random variables and distributions [20%]",
                        order_index=9,
                    ),
                    ExtractedBlock(
                        block_id="b15",
                        kind=BlockKind.PARAGRAPH,
                        text=(
                            "2.1 Understand the characteristics of "
                            "basic univariate distributions"
                        ),
                        order_index=10,
                    ),
                    ExtractedBlock(
                        block_id="b16",
                        kind=BlockKind.PARAGRAPH,
                        text=(
                            "2.1.1 Geometric, binomial, negative binomial "
                            "distributions"
                        ),
                        order_index=11,
                    ),
                ),
                raw_text="1 Data analysis [10%]\n2 Random variables…",
            ),
        ),
    )


FIXED_TS = "2026-07-30T12:00:00Z"


def test_agent_descriptors_expose_required_fields() -> None:
    agents = (RawGraphAgent(), NoiseEliminationAgent(), HierarchyConstructionAgent())
    for agent in agents:
        d = agent.descriptor
        assert d.agent_id
        assert d.name
        assert d.purpose
        assert d.consumes
        assert d.produces
        assert d.version
        assert d.deterministic is True
        assert d.supports_rollback is True
        assert "coverage" in d.quality_metrics_produced
        assert agent.generation_index in {1, 2, 3}


def test_generation_reproducibility_and_stable_hashes() -> None:
    docs = (_syllabus_doc(),)
    store_a = InMemoryGenerationStore()
    store_b = InMemoryGenerationStore()
    orch_a = GenerationOrchestrator(
        store_a, RegressionGuard(), default_phase_b_runners()
    )
    orch_b = GenerationOrchestrator(
        store_b, RegressionGuard(), default_phase_b_runners()
    )
    kwargs = dict(
        workspace_id="ws-b",
        source_document_ids=(101,),
        through=3,
        source_documents=docs,
        subject_code="CS1",
        version_label="2026",
        fixed_created_at_iso=FIXED_TS,
    )
    result_a = orch_a.run_chain(chain_id="chain-repro-a", **kwargs)
    result_b = orch_b.run_chain(chain_id="chain-repro-b", **kwargs)
    assert not result_a.rolled_back
    assert not result_b.rolled_back
    hashes_a = [s.generation_hash for s in result_a.accepted_snapshots]
    hashes_b = [s.generation_hash for s in result_b.accepted_snapshots]
    assert hashes_a == hashes_b
    assert all(len(h) == 64 for h in hashes_a)
    assert len(set(hashes_a)) == 3
    # Node ids stable across independent chains with same inputs.
    nodes_a = {n.node_id for n in result_a.accepted_snapshots[0].nodes}
    nodes_b = {n.node_id for n in result_b.accepted_snapshots[0].nodes}
    assert nodes_a == nodes_b


def test_agent_execution_order_and_snapshot_immutability() -> None:
    store = InMemoryGenerationStore()
    orch = GenerationOrchestrator(store, RegressionGuard(), default_phase_b_runners())
    result = orch.run_chain(
        chain_id="chain-order",
        workspace_id="ws",
        source_document_ids=(101,),
        through=3,
        source_documents=(_syllabus_doc(),),
        fixed_created_at_iso=FIXED_TS,
    )
    indices = [s.generation_index for s in result.accepted_snapshots]
    assert indices == [1, 2, 3]
    assert [s.agent_id for s in result.accepted_snapshots] == [
        "raw_graph_agent",
        "noise_elimination_agent",
        "hierarchy_construction_agent",
    ]
    snap = result.accepted_snapshots[0]
    with pytest.raises(SnapshotImmutableError):
        store.append_snapshot(snap)


def test_noise_rejection_inactive_not_deleted() -> None:
    store = InMemoryGenerationStore()
    orch = GenerationOrchestrator(store, RegressionGuard(), default_phase_b_runners())
    result = orch.run_chain(
        chain_id="chain-noise",
        workspace_id="ws",
        source_document_ids=(101,),
        through=2,
        source_documents=(_syllabus_doc(),),
        fixed_created_at_iso=FIXED_TS,
    )
    g1 = result.accepted_snapshots[0]
    g2 = result.accepted_snapshots[1]
    assert len(g2.nodes) == len(g1.nodes)
    rejected = [n for n in g2.nodes if not n.active]
    assert rejected
    assert all(n.node_id in {x.node_id for x in g1.nodes} for n in rejected)
    assert g2.metrics.noise <= g1.metrics.noise
    for node in rejected:
        assert node.lineage.rejection_reason_code
        assert node.lineage.rejection_reason_label
        assert any(
            op.kind is LineageOperationKind.REJECTED
            for op in node.lineage.operations
        )
        assert node.created_generation
        assert node.current_generation
        assert node.confidence is not None
        assert node.role in {
            ContentRole.FRONT_MATTER.value,
            ContentRole.QUALIFICATION_INFORMATION.value,
            ContentRole.PUBLISHER_METADATA.value,
            ContentRole.NAVIGATION.value,
            ContentRole.TABLE_OF_CONTENTS.value,
            ContentRole.ASSESSMENT_LOGISTICS.value,
            ContentRole.BLANK_ARTEFACT.value,
            ContentRole.COPYRIGHT.value,
        }


def test_hierarchy_correctness_syllabus_first() -> None:
    store = InMemoryGenerationStore()
    orch = GenerationOrchestrator(store, RegressionGuard(), default_phase_b_runners())
    result = orch.run_chain(
        chain_id="chain-hier",
        workspace_id="ws",
        source_document_ids=(101,),
        through=3,
        source_documents=(_syllabus_doc(),),
        subject_code="CS1",
        version_label="2026",
        fixed_created_at_iso=FIXED_TS,
    )
    g3 = result.accepted_snapshots[2]
    active = g3.active_nodes()
    chapters = [n for n in active if n.kind == "chapter"]
    topics = [n for n in active if n.kind == "topic"]
    objectives = [n for n in active if n.kind == "learning_objective"]
    subjects = [n for n in active if n.kind == "subject"]
    assert len(subjects) == 1
    assert len(chapters) == 2
    assert any("data analysis" in c.title.lower() for c in chapters)
    assert len(topics) >= 2
    assert len(objectives) >= 3
    assert any("1.1.1" in o.title for o in objectives)
    # No front-matter titles in active hierarchy.
    titles = {n.title.lower() for n in active}
    assert not any("associateship" in t for t in titles)
    assert "aim" not in titles
    # Parent chain integrity for objectives.
    by_id = {n.node_id: n for n in active}
    for obj in objectives:
        assert obj.parent_node_id is not None
        parent = by_id[obj.parent_node_id]
        assert parent.kind in {"topic", "section", "chapter", "subtopic"}


def test_regression_metrics_are_real_quality_snapshots() -> None:
    store = InMemoryGenerationStore()
    orch = GenerationOrchestrator(store, RegressionGuard(), default_phase_b_runners())
    result = orch.run_chain(
        chain_id="chain-reg",
        workspace_id="ws",
        source_document_ids=(101,),
        through=3,
        source_documents=(_syllabus_doc(),),
        fixed_created_at_iso=FIXED_TS,
    )
    assert not result.rolled_back
    g1, g2, g3 = result.accepted_snapshots
    assert g1.metrics.noise > 0.0
    assert g2.metrics.noise < g1.metrics.noise
    assert g3.metrics.hierarchy >= g2.metrics.hierarchy
    assert g3.metrics.chapters == 2
    assert g3.metrics.objectives >= 3
    reports = store.list_regression_reports("chain-reg")
    assert len(reports) == 2
    assert all(r.accepted for r in reports)
    # Recomputed metrics match snapshot metrics (not placeholders).
    recomputed = compute_quality_snapshot(
        g3.nodes, rejected_count=g3.metrics.rejected_node_count
    )
    assert recomputed.noise == g3.metrics.noise
    assert recomputed.hierarchy == g3.metrics.hierarchy


def test_rollback_with_real_agents() -> None:
    """Gen 3 regressing runner leaves active pointer on Gen 2."""
    store = InMemoryGenerationStore()
    runners = {
        1: RawGraphAgent(),
        2: NoiseEliminationAgent(),
        3: MockPassThroughRunner(
            3,
            metrics_override=QualitySnapshot(
                coverage=0.1,
                hierarchy=0.1,
                duplicates=0.5,
                noise=0.9,
                granularity=0.1,
                confidence=0.2,
            ),
        ),
    }
    orch = GenerationOrchestrator(store, RegressionGuard(), runners)
    result = orch.run_chain(
        chain_id="chain-rb-b",
        workspace_id="ws",
        source_document_ids=(101,),
        through=3,
        source_documents=(_syllabus_doc(),),
        fixed_created_at_iso=FIXED_TS,
    )
    assert result.rolled_back
    assert result.stopped_at_index == 3
    active = store.get_active_snapshot("chain-rb-b")
    assert active is not None
    assert active.generation_index == 2
    assert result.rejected_snapshots[0].status is SnapshotStatus.REJECTED_BY_REGRESSION
    assert orch.rollback_to_active("chain-rb-b").snapshot_id == active.snapshot_id


def test_generation_hash_inputs_change_digest() -> None:
    nodes = ()
    base = compute_generation_hash(
        source_document_ids=(1,),
        parent_snapshot_hash="",
        calibration_profile_id=None,
        agent_id="raw_graph_agent",
        agent_version="1.0.0",
        generation_index=1,
        nodes=nodes,
    )
    other = compute_generation_hash(
        source_document_ids=(2,),
        parent_snapshot_hash="",
        calibration_profile_id=None,
        agent_id="raw_graph_agent",
        agent_version="1.0.0",
        generation_index=1,
        nodes=nodes,
    )
    assert base != other


def test_ei001a_mock_path_still_works() -> None:
    """Existing CIP-adjacent mock orchestrator path remains functional."""
    store = InMemoryGenerationStore()
    orch = GenerationOrchestrator(store, RegressionGuard(), default_mock_runners())
    result = orch.run_chain(
        chain_id="chain-mock",
        workspace_id="ws",
        source_document_ids=(1,),
        through=2,
    )
    assert not result.rolled_back
    assert result.accepted_snapshots[0].generation_hash
