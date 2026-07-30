"""EI-001A Curriculum Intelligence Engine foundation tests."""

from __future__ import annotations

from dataclasses import replace

import pytest

from app.application.curriculum_intelligence.exceptions import (
    LineageAppendError,
    SnapshotImmutableError,
)
from app.application.curriculum_intelligence.generation_orchestrator import (
    GenerationOrchestrator,
)
from app.application.curriculum_intelligence.in_memory_generation_store import (
    InMemoryGenerationStore,
)
from app.application.curriculum_intelligence.mock_generation_runners import (
    default_mock_runners,
)
from app.application.curriculum_intelligence.ports.calibration_router_port import (
    DefaultCalibrationRouter,
    default_calibration_profile,
)
from app.application.curriculum_intelligence.ports.certification_engine_port import (
    UnimplementedCertificationEngine,
)
from app.application.curriculum_intelligence.regression_guard import RegressionGuard
from app.domain.curriculum_intelligence.generation import (
    GenerationIndex,
    GranularityStyle,
    HierarchyStyle,
    LineageOperation,
    LineageOperationKind,
    QualitySnapshot,
    SnapshotStatus,
    TopicDensityStyle,
)
from app.extensions import db
from app.infrastructure.adapters.curriculum_intelligence.generation_store import (
    SqlAlchemyGenerationStore,
)


def test_snapshot_immutability_rejects_rewrite() -> None:
    store = InMemoryGenerationStore()
    orch = GenerationOrchestrator(store, RegressionGuard(), default_mock_runners())
    result = orch.run_chain(
        chain_id="chain-imm",
        workspace_id="ws-1",
        source_document_ids=(1,),
        through=1,
    )
    snap = store.get_snapshot(result.accepted_snapshots[0].snapshot_id)
    assert snap is not None
    with pytest.raises(SnapshotImmutableError):
        store.append_snapshot(snap)


def test_generation_ordering_and_orchestrator_sequencing() -> None:
    store = InMemoryGenerationStore()
    orch = GenerationOrchestrator(store, RegressionGuard(), default_mock_runners())
    result = orch.run_chain(
        chain_id="chain-ord",
        workspace_id="ws-1",
        source_document_ids=(10, 11),
        through=4,
    )
    assert not result.rolled_back
    indices = [s.generation_index for s in result.accepted_snapshots]
    assert indices == [1, 2, 3, 4]
    listed = store.list_snapshots("chain-ord")
    assert [s.generation_index for s in listed] == [1, 2, 3, 4]
    # Prior accepted snapshots become superseded; head remains accepted.
    assert listed[-1].status is SnapshotStatus.ACCEPTED
    assert all(s.status is SnapshotStatus.SUPERSEDED for s in listed[:-1])


def test_rollback_keeps_active_on_last_accepted() -> None:
    store = InMemoryGenerationStore()
    runners = default_mock_runners(regressing_index=3)
    orch = GenerationOrchestrator(store, RegressionGuard(), runners)
    result = orch.run_chain(
        chain_id="chain-rb",
        workspace_id="ws-1",
        source_document_ids=(1,),
        through=4,
    )
    assert result.rolled_back
    assert result.stopped_at_index == 3
    assert len(result.rejected_snapshots) == 1
    assert result.rejected_snapshots[0].status is SnapshotStatus.REJECTED_BY_REGRESSION
    active = store.get_active_snapshot("chain-rb")
    assert active is not None
    assert active.generation_index == 2
    assert active.snapshot_id == result.active_snapshot_id
    reports = store.list_regression_reports("chain-rb")
    assert any(not r.accepted for r in reports)


def test_append_only_lineage_and_stable_node_identity() -> None:
    store = InMemoryGenerationStore()
    orch = GenerationOrchestrator(store, RegressionGuard(), default_mock_runners())
    result = orch.run_chain(
        chain_id="chain-lin",
        workspace_id="ws-1",
        source_document_ids=(1,),
        through=2,
    )
    g1 = result.accepted_snapshots[0]
    g2 = store.get_active_snapshot("chain-lin")
    assert g2 is not None
    # Stable ids survive across generations.
    g1_ids = {n.node_id for n in g1.nodes}
    g2_ids = {n.node_id for n in g2.nodes}
    assert g1_ids == g2_ids
    # Rejected noise is inactive, not deleted.
    rejected = [n for n in g2.nodes if not n.active]
    assert rejected
    assert all(n.node_id in g1_ids for n in rejected)
    node = next(n for n in g2.nodes if not n.active)
    lineage = store.get_lineage_for_node(chain_id="chain-lin", node_id=node.node_id)
    assert lineage is not None
    kinds = [op.kind for op in lineage.operations]
    assert LineageOperationKind.CREATED in kinds
    assert LineageOperationKind.REJECTED in kinds
    # Duplicate operation id is rejected (append-only).
    with pytest.raises(LineageAppendError):
        store.append_lineage_operation(
            chain_id="chain-lin",
            node_id=node.node_id,
            operation=lineage.operations[0],
        )


def test_regression_api_quality_vector_gates() -> None:
    guard = RegressionGuard()
    baseline = QualitySnapshot(
        coverage=0.9,
        hierarchy=0.8,
        duplicates=0.1,
        noise=0.05,
        granularity=0.7,
        confidence=0.85,
    )
    better = replace(baseline, coverage=0.95, noise=0.04, hierarchy=0.85)
    worse = replace(baseline, coverage=0.7, noise=0.2)
    assert guard.compare(better, (baseline,)).accepted
    verdict = guard.compare(worse, (baseline,))
    assert not verdict.accepted
    assert verdict.gate_failures
    report = guard.build_report(
        report_id="r1",
        chain_id="c1",
        candidate_generation_id="g2",
        candidate_snapshot_id="s2",
        baseline_generation_ids=("g1",),
        verdict=verdict,
        candidate_metrics=worse,
        created_at_iso="2026-07-30T00:00:00Z",
    )
    assert report.accepted is False
    assert report.candidate_metrics.coverage == 0.7


def test_certification_and_calibration_interfaces() -> None:
    engine = UnimplementedCertificationEngine()
    with pytest.raises(NotImplementedError):
        engine.certify(
            snapshot=None,  # type: ignore[arg-type]
            quality_history=(),
            regression_history=(),
        )
    router = DefaultCalibrationRouter()
    base = default_calibration_profile(
        profile_id="cal-1",
        workspace_id="ws",
        created_at_iso="2026-07-30T00:00:00Z",
    )
    denser = replace(base, topic_density=TopicDensityStyle.CONSOLIDATED)
    gens = router.select_generations(denser, previous=base)
    assert gens[0] == int(GenerationIndex.TOPIC_CONSOLIDATION)
    assert gens[-1] == int(GenerationIndex.CERTIFICATION)
    hierarchy_change = replace(base, hierarchy=HierarchyStyle.STRICT_SYLLABUS)
    gens_h = router.select_generations(hierarchy_change, previous=base)
    assert gens_h[0] == int(GenerationIndex.HIERARCHY)
    granularity_change = replace(base, granularity=GranularityStyle.VERY_DETAILED)
    assert router.select_generations(granularity_change, previous=base)[0] == 4


def test_sqlalchemy_generation_store_persistence(app, ctx) -> None:
    _ = app
    store = SqlAlchemyGenerationStore()
    orch = GenerationOrchestrator(store, RegressionGuard(), default_mock_runners())
    result = orch.run_chain(
        chain_id="chain-db",
        workspace_id="ws-db",
        source_document_ids=(42,),
        through=2,
    )
    db.session.commit()

    reloaded = store.get_active_snapshot("chain-db")
    assert reloaded is not None
    assert reloaded.snapshot_id == result.active_snapshot_id
    assert reloaded.generation_index == 2
    assert len(reloaded.nodes) >= 1
    # Provenance integration present on Gen 1 nodes.
    assert any(n.provenance_id for n in reloaded.nodes)
    # Immutability still enforced at durable layer.
    with pytest.raises(SnapshotImmutableError):
        store.append_snapshot(reloaded)
    reports = store.list_regression_reports("chain-db")
    assert reports
    assert all(r.accepted for r in reports)


def test_domain_contracts_are_frozen() -> None:
    metrics = QualitySnapshot(
        coverage=1.0,
        hierarchy=1.0,
        duplicates=0.0,
        noise=0.0,
        granularity=0.5,
        confidence=0.9,
    )
    with pytest.raises(Exception):
        metrics.coverage = 0.1  # type: ignore[misc]
    op = LineageOperation(
        operation_id="op-1",
        kind=LineageOperationKind.CREATED,
        generation_id="g1",
        generation_index=1,
        reason_code="created",
        reason_label="created",
    )
    with pytest.raises(Exception):
        op.kind = LineageOperationKind.MERGED  # type: ignore[misc]
