"""Repository contract tests."""

from __future__ import annotations

import pytest

from app.infrastructure.persistence.optimistic_locking import OptimisticLockError
from app.infrastructure.persistence.unit_of_work import UnitOfWork
from app.infrastructure.repositories.in_memory import (
    InMemoryAggregateRepository,
    InMemoryEvidenceRepository,
    InMemorySnapshotRepository,
)
from tests.infrastructure.helpers import AGGREGATES, LEARNERS, SUBJECTS


@pytest.mark.parametrize("aggregate", AGGREGATES)
@pytest.mark.parametrize("agg_id", LEARNERS)
def test_aggregate_repo_save_get_delete(aggregate, agg_id):
    repo = InMemoryAggregateRepository(
        repository_id=f"{aggregate.lower()}_repo",
        aggregate_name=aggregate,
    )
    assert repo.is_available() is True
    ack = repo.save(agg_id, {"value": 1})
    assert ack["version"] == 1
    loaded = repo.get(agg_id)
    assert loaded is not None
    assert loaded["value"] == 1
    assert loaded["_version"] == 1
    assert repo.delete(agg_id) is True
    assert repo.get(agg_id) is None


@pytest.mark.parametrize("aggregate", AGGREGATES)
@pytest.mark.parametrize("agg_id", LEARNERS)
def test_aggregate_repo_optimistic_conflict(aggregate, agg_id):
    repo = InMemoryAggregateRepository(aggregate_name=aggregate)
    repo.save(agg_id, {"v": 1})
    repo.save(agg_id, {"v": 2}, expected_version=1)
    with pytest.raises(OptimisticLockError):
        repo.save(agg_id, {"v": 3}, expected_version=1)


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("subject_id", SUBJECTS)
def test_evidence_repository(learner_id, subject_id):
    repo = InMemoryEvidenceRepository()
    ack = repo.append_evidence(
        learner_id=learner_id,
        subject_id=subject_id,
        evidence_type="practice",
        payload={"ok": True},
        correlation_id="c",
    )
    assert "record_id" in ack
    rows = repo.list_evidence(learner_id, subject_id=subject_id)
    assert len(rows) == 1
    assert rows[0]["learner_id"] == learner_id


@pytest.mark.parametrize("aggregate", AGGREGATES)
@pytest.mark.parametrize("agg_id", LEARNERS)
def test_snapshot_repository(aggregate, agg_id):
    repo = InMemorySnapshotRepository()
    ack = repo.save_snapshot(
        aggregate,
        agg_id,
        {"n": 1},
        schema_version=1,
        correlation_id="c",
    )
    assert "snapshot_id" in ack
    latest = repo.load_latest(aggregate, agg_id)
    assert latest is not None
    assert latest["payload"]["n"] == 1


@pytest.mark.parametrize("aggregate", AGGREGATES)
def test_repositories_register_with_uow(aggregate):
    uow = UnitOfWork()
    agg = InMemoryAggregateRepository(aggregate_name=aggregate, uow=uow)
    snap = InMemorySnapshotRepository(uow=uow)
    evid = InMemoryEvidenceRepository(uow=uow)
    with uow.transaction():
        agg.save("id-1", {"a": 1})
        snap.save_snapshot(aggregate, "id-1", {"a": 1})
        evid.append_evidence(
            learner_id="L1",
            subject_id="S1",
            evidence_type="practice",
        )
        assert len(uow.items) == 3


@pytest.mark.parametrize("aggregate", AGGREGATES)
def test_list_ids_sorted(aggregate):
    repo = InMemoryAggregateRepository(aggregate_name=aggregate)
    repo.save("b", {})
    repo.save("a", {})
    assert repo.list_ids() == ("a", "b")
