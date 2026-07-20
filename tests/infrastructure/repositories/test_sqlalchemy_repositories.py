"""SQLAlchemy repository tests for V2 durable aggregates."""

from __future__ import annotations

import pytest

from app.infrastructure.persistence.optimistic_locking import OptimisticLockError
from app.infrastructure.repositories.sqlalchemy import (
    SqlAlchemyAggregateRepository,
    SqlAlchemyEvidenceRepository,
    SqlAlchemySnapshotRepository,
)


@pytest.fixture()
def durable_ctx(app, db, ctx):
    """Ensure V2 tables exist in the test database."""
    return ctx


def test_sqlalchemy_aggregate_roundtrip(durable_ctx, db):
    repo = SqlAlchemyAggregateRepository(
        repository_id="test_agg",
        aggregate_name="ExperienceTwin",
    )
    ack = repo.save("learner-1", {"student_id": "learner-1", "ready": True})
    assert ack["ok"] is True
    assert ack["version"] == 1
    loaded = repo.get("learner-1")
    assert loaded is not None
    assert loaded["student_id"] == "learner-1"
    assert loaded["_version"] == 1
    assert "learner-1" in repo.list_ids()
    assert repo.delete("learner-1") is True
    assert repo.get("learner-1") is None


def test_sqlalchemy_aggregate_optimistic_lock(durable_ctx, db):
    repo = SqlAlchemyAggregateRepository(aggregate_name="ExperienceMission")
    repo.save("m1", {"v": 1})
    repo.save("m1", {"v": 2}, expected_version=1)
    with pytest.raises(OptimisticLockError):
        repo.save("m1", {"v": 3}, expected_version=1)


def test_sqlalchemy_snapshot_and_evidence(durable_ctx, db):
    snaps = SqlAlchemySnapshotRepository()
    ack = snaps.save_snapshot(
        "ExperienceTwin",
        "learner-2",
        {"n": 1},
        correlation_id="c1",
    )
    assert "snapshot_id" in ack
    latest = snaps.load_latest("ExperienceTwin", "learner-2")
    assert latest is not None
    assert latest["payload"]["n"] == 1

    evidence = SqlAlchemyEvidenceRepository()
    eack = evidence.append_evidence(
        learner_id="learner-2",
        subject_id="MATH",
        evidence_type="practice",
        payload={"ok": True},
    )
    assert "record_id" in eack
    rows = evidence.list_evidence("learner-2", subject_id="MATH")
    assert len(rows) == 1
