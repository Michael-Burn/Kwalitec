"""EI-001D Generation 7 — Certification, Decision Ledger, Review Pack."""

from __future__ import annotations

from app.application.curriculum_intelligence.agents import (
    EducationalCertificationAgent,
    default_phase_c_runners,
    default_phase_d_runners,
)
from app.application.curriculum_intelligence.certification_engine import (
    DefaultCertificationEngine,
)
from app.application.curriculum_intelligence.decision_quality import (
    compute_decision_quality,
    summarise_decision_ledger,
)
from app.application.curriculum_intelligence.founder_preview import (
    CertifiedSnapshotPreviewService,
)
from app.application.curriculum_intelligence.generation_orchestrator import (
    GenerationOrchestrator,
)
from app.application.curriculum_intelligence.in_memory_generation_store import (
    InMemoryGenerationStore,
)
from app.application.curriculum_intelligence.regression_guard import RegressionGuard
from app.application.curriculum_intelligence.review_pack_emitter import (
    ReviewPackEmitter,
)
from app.domain.curriculum_intelligence.certification import (
    CertificationPolicy,
    CertifiedCurriculumSnapshot,
)
from app.domain.curriculum_intelligence.confidence import (
    ConfidenceRecord,
    confidence_band_from_score,
)
from app.domain.curriculum_intelligence.decision_ledger import (
    DecisionLedgerEntry,
    DecisionOutcome,
    DecisionType,
    infer_decision_type,
    ledger_entry_from_educational_decision,
)
from app.domain.curriculum_intelligence.evidence import EvidenceGrade
from app.domain.curriculum_intelligence.extracted_document import (
    BlockKind,
    ExtractedBlock,
    ExtractedDocument,
    ExtractedPage,
)
from app.domain.curriculum_intelligence.generation import (
    CertificationOutcome,
    EducationalNode,
    GenerationIndex,
    LineageRecord,
    QualitySnapshot,
    purpose_for_index,
)
from app.domain.curriculum_intelligence.policy import EducationalDecision


def _syllabus_doc() -> ExtractedDocument:
    """Mini CS1 syllabus fixture (shared with EI-001B/C)."""
    return ExtractedDocument(
        extraction_id="ei001d-syl",
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


def _metrics(**overrides: float) -> QualitySnapshot:
    data = {
        "coverage": 1.0,
        "hierarchy": 0.8,
        "duplicates": 0.0,
        "noise": 0.0,
        "granularity": 0.85,
        "confidence": 0.92,
        "evidence_quality": 0.95,
        "active_node_count": 10,
        "rejected_node_count": 0,
        "low_confidence_share": 0.0,
        "chapters": 2,
        "sections": 0,
        "topics": 3,
        "objectives": 4,
    }
    data.update(overrides)
    return QualitySnapshot(
        coverage=float(data["coverage"]),
        hierarchy=float(data["hierarchy"]),
        duplicates=float(data["duplicates"]),
        noise=float(data["noise"]),
        granularity=float(data["granularity"]),
        confidence=float(data["confidence"]),
        active_node_count=int(data["active_node_count"]),
        rejected_node_count=int(data["rejected_node_count"]),
        low_confidence_share=float(data["low_confidence_share"]),
        chapters=int(data["chapters"]),
        sections=int(data["sections"]),
        topics=int(data["topics"]),
        objectives=int(data["objectives"]),
        evidence_quality=float(data["evidence_quality"]),
    )


def test_generation_7_purpose() -> None:
    assert purpose_for_index(7) == "educational_certification"
    assert int(GenerationIndex.CERTIFICATION) == 7


def test_decision_ledger_entry_from_educational_decision() -> None:
    decision = EducationalDecision(
        decision_id="d-1",
        action="merge",
        subject_node_ids=("t1",),
        reason="Sibling topics form one coherent learning unit",
        evidence_refs=("prov-t1",),
        confidence=0.91,
        policy_id="concept_formation_policy",
        evidence_grade=EvidenceGrade.A,
        related_node_ids=("t2",),
    )
    entry = ledger_entry_from_educational_decision(
        decision,
        chain_id="c1",
        generation_index=4,
        generation_id="g4",
        agent_id="concept_formation_agent",
        created_at_iso=FIXED_TS,
        snapshot_id="s4",
    )
    assert entry.decision_id == "d-1"
    assert entry.decision_type is DecisionType.MERGE
    assert entry.evidence_grade is EvidenceGrade.A
    assert entry.affected_node_ids == ("t1", "t2")
    assert entry.decision_outcome is DecisionOutcome.ACCEPTED
    assert 0.0 < entry.reasoning_confidence <= 1.0


def test_infer_decision_type_mapping() -> None:
    assert (
        infer_decision_type("obj:learning_objective")
        is DecisionType.ATTACH_OBJECTIVE
    )
    assert infer_decision_type("cover:missing") is DecisionType.MISSING
    assert infer_decision_type("certify") is DecisionType.CERTIFY


def test_decision_ledger_persistence_append_only() -> None:
    store = InMemoryGenerationStore()
    entry = DecisionLedgerEntry(
        decision_id="led-1",
        chain_id="chain-d",
        generation_index=4,
        generation_id="g4",
        agent_id="concept_formation_agent",
        policy_id="concept_formation_policy",
        evidence_refs=("e1",),
        evidence_grade=EvidenceGrade.A,
        confidence=0.9,
        reasoning_confidence=0.88,
        affected_node_ids=("n1",),
        decision_type=DecisionType.RETAIN,
        created_at_iso=FIXED_TS,
        decision_outcome=DecisionOutcome.ACCEPTED,
        reason="retain coherent unit",
    )
    store.append_decision(entry)
    listed = store.list_decisions("chain-d")
    assert len(listed) == 1
    assert listed[0].decision_id == "led-1"
    try:
        store.append_decision(entry)
        raise AssertionError("duplicate decision should raise")
    except Exception as exc:  # noqa: BLE001
        assert "already recorded" in str(exc)


def test_decision_quality_scoring() -> None:
    entries = (
        DecisionLedgerEntry(
            decision_id="m1",
            chain_id="c",
            generation_index=4,
            generation_id="g4",
            agent_id="a",
            policy_id="concept_formation_policy",
            evidence_refs=(),
            evidence_grade=EvidenceGrade.A,
            confidence=0.9,
            reasoning_confidence=0.88,
            affected_node_ids=("t1", "t2"),
            decision_type=DecisionType.MERGE,
            created_at_iso=FIXED_TS,
            decision_outcome=DecisionOutcome.ACCEPTED,
        ),
        DecisionLedgerEntry(
            decision_id="o1",
            chain_id="c",
            generation_index=5,
            generation_id="g5",
            agent_id="a",
            policy_id="objective_policy",
            evidence_refs=(),
            evidence_grade=EvidenceGrade.A,
            confidence=0.95,
            reasoning_confidence=0.93,
            affected_node_ids=("lo1",),
            decision_type=DecisionType.ATTACH_OBJECTIVE,
            created_at_iso=FIXED_TS,
            decision_outcome=DecisionOutcome.ACCEPTED,
        ),
        DecisionLedgerEntry(
            decision_id="c1",
            chain_id="c",
            generation_index=6,
            generation_id="g6",
            agent_id="a",
            policy_id="coverage_policy",
            evidence_refs=(),
            evidence_grade=EvidenceGrade.A,
            confidence=0.97,
            reasoning_confidence=0.95,
            affected_node_ids=(),
            decision_type=DecisionType.COVERED,
            created_at_iso=FIXED_TS,
            decision_outcome=DecisionOutcome.ACCEPTED,
        ),
    )
    scores = compute_decision_quality(entries, metrics=_metrics())
    assert scores.merge_quality > 0.7
    assert scores.objective_quality > 0.7
    assert scores.coverage_quality > 0.5
    assert scores.policy_consistency == 1.0
    assert 0.0 < scores.aggregate <= 1.0
    summary = summarise_decision_ledger("c", entries)
    assert summary.entry_count == 3
    assert summary.accepted_count == 3


def test_certification_outcomes_certified() -> None:
    from app.domain.curriculum_intelligence.generation import (
        CurriculumGenerationSnapshot,
        Generation,
        SnapshotStatus,
    )

    engine = DefaultCertificationEngine()
    generation = Generation(
        generation_id="g6",
        chain_id="c",
        generation_index=6,
        purpose="educational_reconciliation",
        parent_generation_ids=(),
        source_document_ids=(1,),
        workspace_id="ws",
        created_at_iso=FIXED_TS,
    )
    lo = EducationalNode(
        node_id="lo1",
        generation_local_id="lo1",
        title="1.1.1 Aims",
        kind="learning_objective",
        role="learning_objective",
        parent_node_id="t1",
        confidence=_conf("lo1"),
        lineage=_lineage("lo1", syllabus_refs=("1.1.1",)),
        active=True,
        evidence_grade=EvidenceGrade.A,
    )
    snap = CurriculumGenerationSnapshot(
        snapshot_id="s6",
        generation=generation,
        nodes=(lo,),
        rejected_nodes=(),
        metrics=_metrics(),
        provenance_bundle_id="b",
        created_at_iso=FIXED_TS,
        status=SnapshotStatus.ACCEPTED,
    )
    decision = engine.certify(
        snap,
        quality_history=(snap,),
        regression_history=(),
        created_at_iso=FIXED_TS,
        decision_id="cert-ok",
    )
    assert decision.outcome is CertificationOutcome.CERTIFIED
    assert decision.quality_score > 50
    assert decision.hard_gate_failures == ()
    assert decision.certification_status is CertificationOutcome.CERTIFIED


def test_certification_not_certified_on_noise() -> None:
    from app.domain.curriculum_intelligence.generation import (
        CurriculumGenerationSnapshot,
        Generation,
        SnapshotStatus,
    )

    engine = DefaultCertificationEngine()
    generation = Generation(
        generation_id="g6",
        chain_id="c",
        generation_index=6,
        purpose="educational_reconciliation",
        parent_generation_ids=(),
        source_document_ids=(1,),
        workspace_id="ws",
        created_at_iso=FIXED_TS,
    )
    noise = EducationalNode(
        node_id="fm",
        generation_local_id="fm",
        title="Copyright",
        kind="chrome",
        role="front_matter",
        parent_node_id=None,
        confidence=_conf("fm", 0.5),
        lineage=_lineage("fm"),
        active=True,
    )
    snap = CurriculumGenerationSnapshot(
        snapshot_id="s6b",
        generation=generation,
        nodes=(noise,),
        rejected_nodes=(),
        metrics=_metrics(noise=0.5, coverage=0.5, hierarchy=0.2, evidence_quality=0.2),
        provenance_bundle_id="b",
        created_at_iso=FIXED_TS,
        status=SnapshotStatus.ACCEPTED,
    )
    report = engine.certify_report(
        snap,
        quality_history=(snap,),
        regression_history=(),
        created_at_iso=FIXED_TS,
    )
    assert report.outcome is CertificationOutcome.NOT_CERTIFIED
    assert report.hard_gate_failures
    assert any(
        "front_matter" in f or "coverage" in f for f in report.hard_gate_failures
    )


def test_certification_with_warnings() -> None:
    from app.domain.curriculum_intelligence.generation import (
        CurriculumGenerationSnapshot,
        Generation,
        SnapshotStatus,
    )

    engine = DefaultCertificationEngine(
        CertificationPolicy(coverage_floor=0.90)
    )
    generation = Generation(
        generation_id="g6",
        chain_id="c",
        generation_index=6,
        purpose="educational_reconciliation",
        parent_generation_ids=(),
        source_document_ids=(1,),
        workspace_id="ws",
        created_at_iso=FIXED_TS,
    )
    lo = EducationalNode(
        node_id="lo1",
        generation_local_id="lo1",
        title="1.1.1 Aims",
        kind="learning_objective",
        role="learning_objective",
        parent_node_id="t1",
        confidence=_conf("lo1"),
        lineage=_lineage("lo1", syllabus_refs=("1.1.1",)),
        active=True,
        evidence_grade=EvidenceGrade.A,
    )
    snap = CurriculumGenerationSnapshot(
        snapshot_id="s6w",
        generation=generation,
        nodes=(lo,),
        rejected_nodes=(),
        metrics=_metrics(coverage=0.93),
        provenance_bundle_id="b",
        created_at_iso=FIXED_TS,
        status=SnapshotStatus.ACCEPTED,
    )
    decision = engine.certify(
        snap,
        quality_history=(snap,),
        regression_history=(),
        created_at_iso=FIXED_TS,
    )
    assert decision.outcome is CertificationOutcome.CERTIFIED_WITH_WARNINGS
    assert any("partial_coverage" in w for w in decision.warnings)
    assert decision.hard_gate_failures == ()


def test_phase_d_full_chain_certification_and_review_pack(tmp_path) -> None:
    store = InMemoryGenerationStore()
    orch = GenerationOrchestrator(
        store,
        RegressionGuard(),
        default_phase_d_runners(),
        certification_engine=DefaultCertificationEngine(),
    )
    result = orch.run_chain(
        chain_id="chain-d",
        workspace_id="ws-d",
        source_document_ids=(101,),
        through=7,
        source_documents=(_syllabus_doc(),),
        subject_code="CS1",
        version_label="2026",
        fixed_created_at_iso=FIXED_TS,
    )
    assert not result.rolled_back, [
        (r.reason, r.gate_failures) for r in store.list_regression_reports("chain-d")
    ]
    assert result.active_snapshot_id is not None
    assert len(result.accepted_snapshots) == 7
    assert result.accepted_snapshots[-1].generation_index == 7

    # Decision Ledger populated from G4–G7.
    decisions = store.list_decisions("chain-d")
    assert len(decisions) >= 3
    assert any(d.generation_index == 4 for d in decisions)
    assert any(d.generation_index == 7 for d in decisions)
    assert any(d.decision_type is DecisionType.CERTIFY for d in decisions)

    # Certification persisted.
    assert result.certification is not None
    assert result.certification.outcome in {
        CertificationOutcome.CERTIFIED,
        CertificationOutcome.CERTIFIED_WITH_WARNINGS,
    }
    assert result.certification.quality_score > 0
    assert result.certification.decision_quality > 0
    stored = store.get_certification(result.accepted_snapshots[-1].snapshot_id)
    assert stored is not None
    assert stored.outcome is result.certification.outcome

    # Certified snapshot for Founder Preview.
    assert result.certified_snapshot is not None
    assert result.certified_snapshot.is_preview_eligible
    assert isinstance(result.certified_snapshot, CertifiedCurriculumSnapshot)

    # Review Pack.
    assert result.review_pack is not None
    pack = result.review_pack
    assert pack.generation_comparison
    assert pack.decision_ledger_summary.entry_count == len(decisions)
    assert "08_certification_report.md" in pack.artefacts_markdown
    assert "01_generation_comparison.md" in pack.artefacts_markdown
    written = ReviewPackEmitter().write_to_directory(pack, str(tmp_path / "pack"))
    assert any(path.endswith("README.md") for path in written)
    assert (tmp_path / "pack" / "08_certification_report.md").exists()

    # Certification report node present on Gen 7.
    g7 = result.accepted_snapshots[-1]
    assert any(n.kind == "certification_report" for n in g7.nodes)


def test_founder_preview_refuses_not_certified() -> None:
    from app.application.curriculum_intelligence.decision_quality import (
        compute_decision_quality,
    )
    from app.domain.curriculum_intelligence.certification import CertificationReport
    from app.domain.curriculum_intelligence.generation import (
        CertificationDecision,
        CurriculumGenerationSnapshot,
        Generation,
        SnapshotStatus,
    )

    generation = Generation(
        generation_id="g7",
        chain_id="c",
        generation_index=7,
        purpose="educational_certification",
        parent_generation_ids=(),
        source_document_ids=(1,),
        workspace_id="ws",
        created_at_iso=FIXED_TS,
    )
    snap = CurriculumGenerationSnapshot(
        snapshot_id="s7",
        generation=generation,
        nodes=(),
        rejected_nodes=(),
        metrics=_metrics(coverage=0.2, noise=0.5),
        provenance_bundle_id="b",
        created_at_iso=FIXED_TS,
        status=SnapshotStatus.ACCEPTED,
    )
    decision = CertificationDecision(
        decision_id="bad",
        chain_id="c",
        snapshot_id="s7",
        outcome=CertificationOutcome.NOT_CERTIFIED,
        quality_score=10.0,
        confidence=0.4,
        coverage=0.2,
        hierarchy_score=0.1,
        granularity_score=0.1,
        warnings=(),
        hard_gate_failures=("coverage_floor: too low",),
        created_at_iso=FIXED_TS,
        failure_reasons=("coverage_floor: too low",),
    )
    report = CertificationReport(
        decision=decision,
        decision_quality=compute_decision_quality(()),
        quality_vector=snap.metrics,
        hard_gate_failures=decision.hard_gate_failures,
        warnings=(),
        reasons=decision.failure_reasons,
    )
    certified = CertifiedCurriculumSnapshot(
        snapshot=snap,
        certification=decision,
        report=report,
    )
    assert not certified.is_preview_eligible
    service = CertifiedSnapshotPreviewService()
    try:
        service.project(certified)
        raise AssertionError("NOT_CERTIFIED must be refused")
    except ValueError as exc:
        assert "NOT_CERTIFIED" in str(exc)


def test_founder_preview_projects_certified() -> None:
    from app.domain.curriculum_intelligence.certification import CertificationReport
    from app.domain.curriculum_intelligence.generation import (
        CertificationDecision,
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
        parent_node_id=None,
        confidence=_conf("ch1"),
        lineage=_lineage("ch1", syllabus_refs=("1",)),
        active=True,
        evidence_grade=EvidenceGrade.A,
    )
    topic = EducationalNode(
        node_id="t1",
        generation_local_id="t1",
        title="1.1 Purpose",
        kind="concept",
        role="educational",
        parent_node_id="ch1",
        confidence=_conf("t1"),
        lineage=_lineage("t1", syllabus_refs=("1.1",)),
        active=True,
        evidence_grade=EvidenceGrade.A,
    )
    lo = EducationalNode(
        node_id="lo1",
        generation_local_id="lo1",
        title="1.1.1 Aims",
        kind="learning_objective",
        role="learning_objective",
        parent_node_id="t1",
        confidence=_conf("lo1"),
        lineage=_lineage("lo1", syllabus_refs=("1.1.1",)),
        active=True,
        evidence_grade=EvidenceGrade.A,
    )
    generation = Generation(
        generation_id="g7",
        chain_id="c",
        generation_index=7,
        purpose="educational_certification",
        parent_generation_ids=(),
        source_document_ids=(1,),
        workspace_id="ws",
        created_at_iso=FIXED_TS,
    )
    snap = CurriculumGenerationSnapshot(
        snapshot_id="s7",
        generation=generation,
        nodes=(chapter, topic, lo),
        rejected_nodes=(),
        metrics=_metrics(),
        provenance_bundle_id="b",
        created_at_iso=FIXED_TS,
        status=SnapshotStatus.ACCEPTED,
    )
    decision = CertificationDecision(
        decision_id="ok",
        chain_id="c",
        snapshot_id="s7",
        outcome=CertificationOutcome.CERTIFIED,
        quality_score=88.0,
        confidence=0.92,
        coverage=1.0,
        hierarchy_score=0.8,
        granularity_score=0.85,
        warnings=(),
        hard_gate_failures=(),
        created_at_iso=FIXED_TS,
        evidence_quality=0.95,
        reasoning_confidence=0.9,
        decision_quality=0.88,
    )
    report = CertificationReport(
        decision=decision,
        decision_quality=compute_decision_quality(()),
        quality_vector=snap.metrics,
        hard_gate_failures=(),
        warnings=(),
        reasons=("All hard and soft certification gates passed.",),
    )
    certified = CertifiedCurriculumSnapshot(
        snapshot=snap, certification=decision, report=report
    )
    projected = CertifiedSnapshotPreviewService().project(certified)
    assert projected.preview_eligible
    assert projected.section_ids == ("ch1",)
    assert projected.topic_ids == ("t1",)
    assert projected.objective_ids == ("lo1",)
    assert projected.source == "certified_snapshot"


def test_phase_c_compatibility_still_runs() -> None:
    store = InMemoryGenerationStore()
    orch = GenerationOrchestrator(
        store, RegressionGuard(), default_phase_c_runners()
    )
    result = orch.run_chain(
        chain_id="chain-c-compat",
        workspace_id="ws",
        source_document_ids=(101,),
        through=6,
        source_documents=(_syllabus_doc(),),
        subject_code="CS1",
        version_label="2026",
        fixed_created_at_iso=FIXED_TS,
    )
    assert not result.rolled_back
    assert len(result.accepted_snapshots) == 6
    # Decisions still recorded even without Gen 7.
    assert store.list_decisions("chain-c-compat")


def test_certification_agent_descriptor() -> None:
    agent = EducationalCertificationAgent()
    assert agent.descriptor.agent_id == "educational_certification_agent"
    assert agent.descriptor.deterministic is True
    assert agent.generation_index == 7
