"""EI-001C Generations 4–6 — Educational Policies, evidence grading, regression."""

from __future__ import annotations

from dataclasses import replace

from app.application.curriculum_intelligence.agents import (
    ConceptFormationAgent,
    EducationalReconciliationAgent,
    ObjectiveIntelligenceAgent,
    default_phase_b_runners,
    default_phase_c_runners,
)
from app.application.curriculum_intelligence.generation_orchestrator import (
    GenerationOrchestrator,
)
from app.application.curriculum_intelligence.in_memory_generation_store import (
    InMemoryGenerationStore,
)
from app.application.curriculum_intelligence.policies import (
    ConceptFormationPolicy,
    CoveragePolicy,
    ObjectivePolicy,
)
from app.application.curriculum_intelligence.regression_guard import RegressionGuard
from app.domain.curriculum_intelligence.confidence import (
    ConfidenceRecord,
    confidence_band_from_score,
)
from app.domain.curriculum_intelligence.evidence import (
    EvidenceGrade,
    best_evidence_grade,
    evidence_grade_weight,
)
from app.domain.curriculum_intelligence.extracted_document import (
    BlockKind,
    ExtractedBlock,
    ExtractedDocument,
    ExtractedPage,
)
from app.domain.curriculum_intelligence.generation import (
    EducationalNode,
    GenerationIndex,
    LineageOperationKind,
    LineageRecord,
    QualitySnapshot,
    RegressionPolicy,
    purpose_for_index,
)
from app.domain.curriculum_intelligence.policy import ConceptAction


def _syllabus_doc() -> ExtractedDocument:
    """Mini CS1 syllabus fixture (shared with EI-001B)."""
    return ExtractedDocument(
        extraction_id="ei001c-syl",
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
                ),
                raw_text="Associateship Qualification\nActuarial Statistics (CS1)",
            ),
            ExtractedPage(
                page_number=2,
                width=612.0,
                height=792.0,
                blocks=(
                    ExtractedBlock(
                        block_id="b8",
                        kind=BlockKind.HEADING,
                        text="1 Data analysis [10%]",
                        order_index=0,
                    ),
                    ExtractedBlock(
                        block_id="b9",
                        kind=BlockKind.PARAGRAPH,
                        text="1.1 Describe the purpose and function of data analysis",
                        order_index=1,
                    ),
                    ExtractedBlock(
                        block_id="b10",
                        kind=BlockKind.PARAGRAPH,
                        text="1.1.1 Aims of a data analysis (e.g. descriptive)",
                        order_index=2,
                    ),
                    ExtractedBlock(
                        block_id="b11",
                        kind=BlockKind.PARAGRAPH,
                        text=(
                            "1.1.2 Stages and suitable tools used "
                            "to conduct a data analysis"
                        ),
                        order_index=3,
                    ),
                    ExtractedBlock(
                        block_id="b12",
                        kind=BlockKind.PARAGRAPH,
                        text="1.2 Complete exploratory data analysis",
                        order_index=4,
                    ),
                    ExtractedBlock(
                        block_id="b13",
                        kind=BlockKind.PARAGRAPH,
                        text=(
                            "1.2.1 Appropriate tools to calculate "
                            "suitable summary statistics"
                        ),
                        order_index=5,
                    ),
                    ExtractedBlock(
                        block_id="b14",
                        kind=BlockKind.HEADING,
                        text="2 Random variables and distributions [20%]",
                        order_index=6,
                    ),
                    ExtractedBlock(
                        block_id="b15",
                        kind=BlockKind.PARAGRAPH,
                        text=(
                            "2.1 Understand the characteristics of "
                            "basic univariate distributions"
                        ),
                        order_index=7,
                    ),
                    ExtractedBlock(
                        block_id="b16",
                        kind=BlockKind.PARAGRAPH,
                        text=(
                            "2.1.1 Geometric, binomial, negative binomial "
                            "distributions"
                        ),
                        order_index=8,
                    ),
                ),
                raw_text="1 Data analysis [10%]\n2 Random variables…",
            ),
        ),
    )


FIXED_TS = "2026-07-30T12:00:00Z"


def _conf(node_id: str, score: float = 0.9) -> ConfidenceRecord:
    return ConfidenceRecord(
        confidence_id=f"conf-{node_id}",
        subject_kind="educational_node",
        subject_id=node_id,
        score=score,
        band=confidence_band_from_score(score),
        reason="test",
        factors=(),
        needs_review=False,
        review_threshold=0.6,
    )


def _lineage(node_id: str, *, syllabus_refs: tuple[str, ...] = ()) -> LineageRecord:
    return LineageRecord(
        created_generation="g3",
        created_generation_index=3,
        last_modified_generation="g3",
        last_modified_generation_index=3,
        operations=(),
        syllabus_refs=syllabus_refs,
    )


def _topic(
    node_id: str,
    title: str,
    *,
    parent: str | None = "chapter-1",
    syllabus_ref: str | None = None,
) -> EducationalNode:
    refs = (syllabus_ref,) if syllabus_ref else ()
    return EducationalNode(
        node_id=node_id,
        generation_local_id=node_id,
        title=title,
        kind="topic",
        role="educational",
        parent_node_id=parent,
        confidence=_conf(node_id),
        lineage=_lineage(node_id, syllabus_refs=refs),
        active=True,
        provenance_id=f"prov-{node_id}",
        evidence_grade=EvidenceGrade.A if syllabus_ref else None,
    )


def test_generation_4_renamed_concept_formation() -> None:
    assert purpose_for_index(4) == "concept_formation"
    assert int(GenerationIndex.CONCEPT_FORMATION) == 4
    assert int(GenerationIndex.TOPIC_CONSOLIDATION) == 4


def test_evidence_grading_weights_and_best() -> None:
    assert evidence_grade_weight(EvidenceGrade.A) == 1.0
    assert evidence_grade_weight(EvidenceGrade.D) == 0.25
    assert best_evidence_grade(EvidenceGrade.C, EvidenceGrade.A) is EvidenceGrade.A
    assert best_evidence_grade(None, None) is None


def test_concept_formation_policy_merge_split_retain() -> None:
    policy = ConceptFormationPolicy()
    nodes = (
        _topic("t1", "1.1 Purpose of data analysis", syllabus_ref="1.1"),
        _topic("t2", "1.1 Purpose of data analysis overview", syllabus_ref="1.1"),
        _topic(
            "t3",
            "1.1.1 Aims of analysis 1.1.2 Stages of analysis",
            syllabus_ref="1.1.1",
        ),
        _topic("t4", "1.2 Exploratory data analysis", syllabus_ref="1.2"),
    )
    plan = policy.plan(nodes, decision_prefix="test")
    actions = {d.action for d in plan.decisions}
    assert ConceptAction.MERGE.value in actions
    assert ConceptAction.SPLIT.value in actions
    assert ConceptAction.RETAIN.value in actions
    for decision in plan.decisions:
        assert decision.reason
        assert decision.policy_id == "concept_formation_policy"
        assert decision.evidence_grade in EvidenceGrade
        assert 0.0 <= decision.confidence <= 1.0
    assert plan.merges
    assert plan.splits
    survivor, absorbed = plan.merges[0]
    assert survivor in {"t1", "t2"}
    assert absorbed


def test_objective_policy_attachments() -> None:
    policy = ObjectivePolicy()
    lo = EducationalNode(
        node_id="lo1",
        generation_local_id="lo1",
        title="1.1.1 Describe aims of a data analysis",
        kind="learning_objective",
        role="learning_objective",
        parent_node_id="t1",
        confidence=_conf("lo1"),
        lineage=_lineage("lo1", syllabus_refs=("1.1.1",)),
        active=True,
        evidence_grade=EvidenceGrade.A,
    )
    chapter = EducationalNode(
        node_id="ch1",
        generation_local_id="ch1",
        title="1 Data analysis [10%]",
        kind="chapter",
        role="educational",
        parent_node_id="sub",
        confidence=_conf("ch1"),
        lineage=_lineage("ch1", syllabus_refs=("1",)),
        active=True,
        attributes=(("weight", "10%"),),
    )
    topic = replace(
        lo,
        node_id="t1",
        kind="concept",
        title="1.1 Data analysis",
        parent_node_id="ch1",
    )
    # Fix topic lineage parent chain via chapter in pool
    plan = policy.plan((chapter, topic, lo))
    kinds = {a.kind.value for a in plan.attachments}
    assert "learning_objective" in kinds
    assert "competency" in kinds
    assert "knowledge_statement" in kinds
    assert "exam_expectation" in kinds
    for att in plan.attachments:
        assert att.evidence_grade is EvidenceGrade.A
        assert att.policy_id == "objective_policy"
        assert att.syllabus_ref or att.kind.value == "exam_expectation"


def test_coverage_policy_matrix() -> None:
    policy = CoveragePolicy()
    nodes = (
        _topic("t1", "1.1.1 Aims of a data analysis", syllabus_ref="1.1.1"),
        _topic("t2", "Unexpected CMP fragment without syllabus"),
    )
    # Force unexpected: no syllabus refs on t2
    t2 = replace(nodes[1], lineage=_lineage("t2"), evidence_grade=EvidenceGrade.B)
    matrix = policy.reconcile(
        working_nodes=(nodes[0], t2),
        syllabus_objectives=(
            ("1.1.1", "Aims of a data analysis"),
            ("1.1.2", "Stages of a data analysis"),
        ),
    )
    assert matrix.covered >= 1
    assert matrix.missing >= 1
    assert matrix.unexpected >= 1
    assert 0.0 <= matrix.completeness <= 1.0
    assert matrix.decisions
    assert all(
        d.evidence_grade is EvidenceGrade.A or d.action == "cover:unexpected"
        for d in matrix.decisions
    )


def test_phase_c_full_chain_concept_objective_reconciliation() -> None:
    store = InMemoryGenerationStore()
    orch = GenerationOrchestrator(
        store, RegressionGuard(), default_phase_c_runners()
    )
    result = orch.run_chain(
        chain_id="chain-c",
        workspace_id="ws",
        source_document_ids=(101,),
        through=6,
        source_documents=(_syllabus_doc(),),
        subject_code="CS1",
        version_label="2026",
        fixed_created_at_iso=FIXED_TS,
    )
    assert not result.rolled_back, [
        (r.reason, r.gate_failures) for r in store.list_regression_reports("chain-c")
    ]
    assert [s.generation_index for s in result.accepted_snapshots] == [1, 2, 3, 4, 5, 6]
    assert [s.agent_id for s in result.accepted_snapshots] == [
        "raw_graph_agent",
        "noise_elimination_agent",
        "hierarchy_construction_agent",
        "concept_formation_agent",
        "objective_intelligence_agent",
        "educational_reconciliation_agent",
    ]
    g4, g5, g6 = result.accepted_snapshots[3:]
    assert g4.generation.purpose == "concept_formation"
    concepts = [n for n in g4.active_nodes() if n.kind == "concept"]
    assert concepts
    assert all(n.evidence_grade is not None for n in concepts)
    assert all(n.policy_id == "concept_formation_policy" for n in concepts)

    # Objective attachments present on LOs.
    los = [n for n in g5.active_nodes() if n.kind == "learning_objective"]
    assert los
    assert any(
        any(k.startswith("obj:") for k, _v in n.attributes) for n in los
    )
    assert all(n.evidence_grade is not None for n in los)

    # Coverage matrix summary node.
    reports = [n for n in g6.active_nodes() if n.kind == "coverage_report"]
    assert len(reports) == 1
    attrs = dict(reports[0].attributes)
    assert "coverage_completeness" in attrs
    assert float(attrs["coverage_completeness"]) >= 0.5
    assert g6.metrics.evidence_quality >= g4.metrics.evidence_quality - 0.01
    assert g6.metrics.coverage >= g3_coverage_floor(result)


def g3_coverage_floor(result) -> float:
    return result.accepted_snapshots[2].metrics.coverage


def test_concept_formation_agent_records_merge_lineage() -> None:
    """Direct agent execution with mergeable siblings."""
    from app.application.curriculum_intelligence.mock_generation_runners import (
        GenerationRunContext,
    )
    from app.domain.curriculum_intelligence.generation import (
        CurriculumGenerationSnapshot,
        Generation,
        SnapshotStatus,
    )

    chapter = EducationalNode(
        node_id="ch1",
        generation_local_id="ch1",
        title="1 Data analysis",
        kind="chapter",
        role="educational",
        parent_node_id="sub",
        confidence=_conf("ch1"),
        lineage=_lineage("ch1", syllabus_refs=("1",)),
        active=True,
        evidence_grade=EvidenceGrade.A,
    )
    t1 = _topic("t1", "1.1 Purpose of data analysis", parent="ch1", syllabus_ref="1.1")
    t2 = _topic(
        "t2", "1.1 Purpose of data analysis overview", parent="ch1", syllabus_ref="1.1"
    )
    lo = EducationalNode(
        node_id="lo1",
        generation_local_id="lo1",
        title="1.1.1 Aims",
        kind="learning_objective",
        role="learning_objective",
        parent_node_id="t2",
        confidence=_conf("lo1"),
        lineage=_lineage("lo1", syllabus_refs=("1.1.1",)),
        active=True,
        evidence_grade=EvidenceGrade.A,
    )
    prior = CurriculumGenerationSnapshot(
        snapshot_id="snap-g3",
        generation=Generation(
            generation_id="gen-g3",
            chain_id="chain-merge",
            generation_index=3,
            purpose="hierarchy_construction",
            parent_generation_ids=(),
            source_document_ids=(101,),
            workspace_id="ws",
            created_at_iso=FIXED_TS,
        ),
        nodes=(chapter, t1, t2, lo),
        rejected_nodes=(),
        metrics=QualitySnapshot(
            coverage=0.7,
            hierarchy=0.7,
            duplicates=0.2,
            noise=0.0,
            granularity=0.5,
            confidence=0.9,
            evidence_quality=1.0,
        ),
        provenance_bundle_id="b",
        created_at_iso=FIXED_TS,
        status=SnapshotStatus.ACCEPTED,
        generation_hash="abc123",
        agent_id="hierarchy_construction_agent",
        agent_version="1.0.0",
    )
    agent = ConceptFormationAgent()
    snap = agent.execute(
        GenerationRunContext(
            chain_id="chain-merge",
            workspace_id="ws",
            source_document_ids=(101,),
            prior_snapshot=prior,
            fixed_created_at_iso=FIXED_TS,
        )
    )
    inactive = [n for n in snap.nodes if not n.active]
    assert any(
        op.kind is LineageOperationKind.MERGED
        for n in inactive
        for op in n.lineage.operations
    )
    # LO reassigned under survivor when parent absorbed.
    active_lo = next(n for n in snap.active_nodes() if n.kind == "learning_objective")
    assert active_lo.parent_node_id in {t1.node_id, t2.node_id}
    if active_lo.parent_node_id != "t2":
        assert any(
            op.kind is LineageOperationKind.REPARENTED
            for op in active_lo.lineage.operations
        )


def test_regression_guard_rejects_evidence_and_granularity() -> None:
    guard = RegressionGuard()
    baseline = QualitySnapshot(
        coverage=0.9,
        hierarchy=0.8,
        duplicates=0.1,
        noise=0.05,
        granularity=0.8,
        confidence=0.9,
        evidence_quality=0.95,
    )
    worse_evidence = replace(baseline, evidence_quality=0.5)
    verdict = guard.compare(worse_evidence, (baseline,))
    assert not verdict.accepted
    assert any("evidence_quality" in f for f in verdict.gate_failures)

    worse_gran = replace(baseline, granularity=0.4)
    verdict_g = guard.compare(worse_gran, (baseline,))
    assert not verdict_g.accepted
    assert any("granularity" in f for f in verdict_g.gate_failures)

    worse_conf = replace(baseline, confidence=0.5)
    verdict_c = guard.compare(worse_conf, (baseline,))
    assert not verdict_c.accepted
    assert any("confidence" in f for f in verdict_c.gate_failures)

    # Soft-only policy can accept confidence dips.
    soft = RegressionGuard(
        RegressionPolicy(reject_on_confidence=False, prefer_confidence=True)
    )
    soft_verdict = soft.compare(worse_conf, (baseline,))
    assert soft_verdict.accepted

    # Production epsilon absorbs Gen2-scale noise-elimination dips (~0.011).
    eps = RegressionGuard(RegressionPolicy())
    mild_dip = replace(baseline, confidence=round(baseline.confidence - 0.011, 4))
    assert eps.compare(mild_dip, (baseline,)).accepted
    deep_dip = replace(baseline, confidence=round(baseline.confidence - 0.05, 4))
    assert not eps.compare(deep_dip, (baseline,)).accepted


def test_policy_descriptors_deterministic() -> None:
    for policy in (ConceptFormationPolicy(), ObjectivePolicy(), CoveragePolicy()):
        d = policy.descriptor
        assert d.deterministic is True
        assert d.policy_id
        assert d.version
        assert d.generation_index in {4, 5, 6}


def test_agent_descriptors_phase_c() -> None:
    agents = (
        ConceptFormationAgent(),
        ObjectiveIntelligenceAgent(),
        EducationalReconciliationAgent(),
    )
    for agent in agents:
        d = agent.descriptor
        assert d.deterministic is True
        assert d.supports_rollback is True
        assert "evidence_quality" in d.quality_metrics_produced
        assert agent.generation_index in {4, 5, 6}


def test_phase_c_reproducible_hashes() -> None:
    docs = (_syllabus_doc(),)
    kwargs = dict(
        workspace_id="ws",
        source_document_ids=(101,),
        through=6,
        source_documents=docs,
        subject_code="CS1",
        version_label="2026",
        fixed_created_at_iso=FIXED_TS,
    )
    a = GenerationOrchestrator(
        InMemoryGenerationStore(), RegressionGuard(), default_phase_c_runners()
    ).run_chain(chain_id="c-a", **kwargs)
    b = GenerationOrchestrator(
        InMemoryGenerationStore(), RegressionGuard(), default_phase_c_runners()
    ).run_chain(chain_id="c-b", **kwargs)
    assert not a.rolled_back and not b.rolled_back
    assert [s.generation_hash for s in a.accepted_snapshots] == [
        s.generation_hash for s in b.accepted_snapshots
    ]


def test_phase_b_path_still_functional() -> None:
    store = InMemoryGenerationStore()
    orch = GenerationOrchestrator(store, RegressionGuard(), default_phase_b_runners())
    result = orch.run_chain(
        chain_id="chain-b-compat",
        workspace_id="ws",
        source_document_ids=(101,),
        through=3,
        source_documents=(_syllabus_doc(),),
        fixed_created_at_iso=FIXED_TS,
    )
    assert not result.rolled_back
    assert len(result.accepted_snapshots) == 3


def test_cip_pipeline_regression_suite_still_imports() -> None:
    """Existing CIP/EQ modules remain importable alongside Phase C."""
    from app.application.curriculum_intelligence import (
        syllabus_reconciliation_service as srs,
    )
    from app.application.curriculum_intelligence.pipeline_coordinator import (
        PipelineCoordinator,
    )

    assert PipelineCoordinator is not None
    assert srs.SyllabusReconciliationService is not None
