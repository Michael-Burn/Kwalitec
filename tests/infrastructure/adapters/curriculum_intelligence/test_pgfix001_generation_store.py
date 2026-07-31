"""PGFIX-001 — PostgreSQL / FK-safe generation store persistence.

Reproduces the RCV-001 failure mode:

1. ``append_snapshot`` adds snapshot + educational nodes to the session.
2. ``_ensure_lineage_op`` issues a SELECT (existence check).
3. SQLAlchemy autoflush INSERTs pending nodes before the snapshot row.
4. PostgreSQL (and SQLite with ``PRAGMA foreign_keys=ON``) rejects the node
   INSERT via ``ei_educational_nodes.snapshot_id_fkey``.

These tests run under SQLite with foreign keys enforced (see ``tests/conftest.py``).
When ``TEST_POSTGRES_URL`` is set, the same cases also run against PostgreSQL.
"""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest
from sqlalchemy.exc import IntegrityError

from app.application.curriculum_intelligence.generation_orchestrator import (
    GenerationOrchestrator,
)
from app.application.curriculum_intelligence.mock_generation_runners import (
    default_mock_runners,
)
from app.application.curriculum_intelligence.regression_guard import RegressionGuard
from app.domain.curriculum_intelligence.confidence import (
    ConfidenceBand,
    ConfidenceRecord,
)
from app.domain.curriculum_intelligence.generation import (
    CurriculumGenerationSnapshot,
    EducationalNode,
    Generation,
    LineageOperation,
    LineageOperationKind,
    LineageRecord,
    QualitySnapshot,
    SnapshotStatus,
)
from app.extensions import db
from app.infrastructure.adapters.curriculum_intelligence.generation_store import (
    SqlAlchemyGenerationStore,
)
from app.models.curriculum_generation import (
    EiEducationalNode,
    EiGenerationSnapshot,
)


def _metrics() -> QualitySnapshot:
    return QualitySnapshot(
        coverage=1.0,
        hierarchy=1.0,
        duplicates=0.0,
        noise=0.0,
        granularity=0.5,
        confidence=0.9,
    )


def _snapshot_with_lineage(
    *,
    chain_id: str,
    snapshot_id: str,
    generation_id: str,
    workspace_id: str = "ws-pgfix",
) -> CurriculumGenerationSnapshot:
    """Build a Gen-1-shaped snapshot that triggers the RCV-001 autoflush path."""
    generation = Generation(
        generation_id=generation_id,
        chain_id=chain_id,
        generation_index=1,
        purpose="raw_graph_capture",
        parent_generation_ids=(),
        source_document_ids=(101,),
        workspace_id=workspace_id,
        created_at_iso="2026-07-30T12:00:00Z",
    )
    op = LineageOperation(
        operation_id=f"op-{snapshot_id}",
        kind=LineageOperationKind.CREATED,
        generation_id=generation_id,
        generation_index=1,
        reason_code="created",
        reason_label="created",
    )
    node_id = f"node-{snapshot_id}"
    confidence = ConfidenceRecord(
        confidence_id=f"conf-{node_id}",
        subject_kind="educational_node",
        subject_id=node_id,
        score=0.75,
        band=ConfidenceBand.MEDIUM,
        reason="pgfix_fixture",
        factors=(),
        needs_review=False,
        review_threshold=0.6,
        provenance_id=f"prov-{snapshot_id}",
    )
    node = EducationalNode(
        node_id=node_id,
        generation_local_id="g1-0",
        title="Associateship Qualification",
        kind="candidate_qualification_information",
        role="qualification_information",
        parent_node_id=None,
        active=True,
        body="Associateship Qualification",
        provenance_id=f"prov-{snapshot_id}",
        confidence=confidence,
        lineage=LineageRecord(
            created_generation=generation_id,
            created_generation_index=1,
            last_modified_generation=generation_id,
            last_modified_generation_index=1,
            operations=(op,),
        ),
        provenance=None,
        attributes=(("source_page", "1"),),
    )
    return CurriculumGenerationSnapshot(
        snapshot_id=snapshot_id,
        generation=generation,
        nodes=(node,),
        rejected_nodes=(),
        metrics=_metrics(),
        provenance_bundle_id=f"bundle-{snapshot_id}",
        created_at_iso="2026-07-30T12:00:00Z",
        status=SnapshotStatus.ACCEPTED,
        generation_hash="hash-pgfix",
        agent_id="mock",
        agent_version="1",
    )


def test_sqlite_foreign_keys_are_enforced(app, ctx) -> None:
    """Guardrail: the suite must not re-mask FK bugs with SQLite defaults."""
    _ = app
    with db.engine.connect() as connection:
        enabled = connection.exec_driver_sql("PRAGMA foreign_keys").scalar()
    assert int(enabled or 0) == 1


def test_append_snapshot_with_lineage_persists_under_fk(app, ctx) -> None:
    """Exact RCV-001 failure shape: nodes + lineage SELECT during append."""
    _ = app
    store = SqlAlchemyGenerationStore()
    snap = _snapshot_with_lineage(
        chain_id="pgfix-chain-1",
        snapshot_id="snap-pgfix-1",
        generation_id="gen-pgfix-1",
    )
    store.append_snapshot(snap)
    db.session.commit()

    assert EiGenerationSnapshot.query.filter_by(snapshot_id="snap-pgfix-1").one()
    assert EiEducationalNode.query.filter_by(snapshot_id="snap-pgfix-1").count() == 1
    reloaded = store.get_snapshot("snap-pgfix-1")
    assert reloaded is not None
    assert len(reloaded.nodes) == 1
    assert reloaded.nodes[0].lineage.operations


def test_generations_1_through_7_persist(app, ctx) -> None:
    """Full orchestrator chain must persist on an FK-enforcing store."""
    _ = app
    store = SqlAlchemyGenerationStore()
    orch = GenerationOrchestrator(store, RegressionGuard(), default_mock_runners())
    result = orch.run_chain(
        chain_id="pgfix-chain-g1g7",
        workspace_id="ws-pgfix-g1g7",
        source_document_ids=(42,),
        through=7,
        stop_on_regression=True,
    )
    db.session.commit()

    assert result.stopped_at_index is None
    assert not result.rolled_back
    accepted = [s.generation_index for s in result.accepted_snapshots]
    assert accepted == [1, 2, 3, 4, 5, 6, 7]
    listed = store.list_snapshots("pgfix-chain-g1g7")
    assert [s.generation_index for s in listed] == [1, 2, 3, 4, 5, 6, 7]
    active = store.get_active_snapshot("pgfix-chain-g1g7")
    assert active is not None
    assert active.generation_index == 7
    assert len(active.nodes) >= 1


# ---------------------------------------------------------------------------
# PostgreSQL regression (requires TEST_POSTGRES_URL)
# ---------------------------------------------------------------------------


def _postgres_url() -> str | None:
    raw = (os.environ.get("TEST_POSTGRES_URL") or "").strip()
    return raw or None


@pytest.fixture(scope="module")
def postgres_app() -> Iterator:
    """Isolated Flask app bound to PostgreSQL (EI tables only)."""
    url = _postgres_url()
    if not url:
        pytest.skip("TEST_POSTGRES_URL not set")

    from app import config
    from app.config import _normalize_postgres_url

    normalized = _normalize_postgres_url(url)
    os.environ["APP_ENV"] = "testing"
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"

    original_uri_fn = config._database_uri
    original_base_uri = config.BaseConfig.SQLALCHEMY_DATABASE_URI
    config._database_uri = lambda: normalized
    config.BaseConfig.SQLALCHEMY_DATABASE_URI = normalized

    from app import create_app
    from app.models import curriculum_generation as ei_models

    application = create_app()
    application.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_DATABASE_URI=normalized,
        SERVER_NAME="localhost.localdomain",
    )

    ei_tables = [
        ei_models.EiGenerationChain.__table__,
        ei_models.EiGeneration.__table__,
        ei_models.EiGenerationSnapshot.__table__,
        ei_models.EiEducationalNode.__table__,
        ei_models.EiLineageOperation.__table__,
        ei_models.EiRegressionReport.__table__,
        ei_models.EiDecisionLedgerEntry.__table__,
        ei_models.EiCertificationRecord.__table__,
        ei_models.EiCalibrationProfile.__table__,
    ]

    with application.app_context():
        db.metadata.create_all(db.engine, tables=ei_tables)

    yield application

    with application.app_context():
        db.session.remove()
        db.metadata.drop_all(db.engine, tables=list(reversed(ei_tables)))

    config._database_uri = original_uri_fn
    config.BaseConfig.SQLALCHEMY_DATABASE_URI = original_base_uri


@pytest.fixture()
def postgres_ctx(postgres_app) -> Iterator:
    with postgres_app.app_context():
        # Truncate EI tables between tests for isolation.
        for table in reversed(db.metadata.sorted_tables):
            if table.name.startswith("ei_"):
                db.session.execute(table.delete())
        db.session.commit()
        yield


@pytest.mark.postgres
def test_postgres_append_snapshot_with_lineage(postgres_app, postgres_ctx) -> None:
    _ = postgres_app
    store = SqlAlchemyGenerationStore()
    snap = _snapshot_with_lineage(
        chain_id="pgfix-pg-chain-1",
        snapshot_id="snap-pgfix-pg-1",
        generation_id="gen-pgfix-pg-1",
    )
    try:
        store.append_snapshot(snap)
        db.session.commit()
    except IntegrityError as exc:  # pragma: no cover - failure mode under test
        db.session.rollback()
        pytest.fail(f"PostgreSQL FK integrity error during append_snapshot: {exc}")

    assert EiGenerationSnapshot.query.filter_by(snapshot_id="snap-pgfix-pg-1").one()
    assert (
        EiEducationalNode.query.filter_by(snapshot_id="snap-pgfix-pg-1").count() == 1
    )


@pytest.mark.postgres
def test_postgres_generations_1_through_7(postgres_app, postgres_ctx) -> None:
    _ = postgres_app
    store = SqlAlchemyGenerationStore()
    orch = GenerationOrchestrator(store, RegressionGuard(), default_mock_runners())
    result = orch.run_chain(
        chain_id="pgfix-pg-g1g7",
        workspace_id="ws-pgfix-pg-g1g7",
        source_document_ids=(42,),
        through=7,
        stop_on_regression=True,
    )
    db.session.commit()

    assert result.stopped_at_index is None
    assert [s.generation_index for s in result.accepted_snapshots] == list(range(1, 8))
    active = store.get_active_snapshot("pgfix-pg-g1g7")
    assert active is not None
    assert active.generation_index == 7
