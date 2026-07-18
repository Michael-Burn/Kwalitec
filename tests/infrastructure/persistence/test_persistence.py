"""Persistence contract, UoW, locking, and store tests."""

from __future__ import annotations

import pytest

from app.infrastructure.persistence.contracts import (
    AGGREGATE_CONTRACTS,
    AggregateOwner,
    contract_for,
    owner_for,
)
from app.infrastructure.persistence.evidence_store import EvidenceStore
from app.infrastructure.persistence.optimistic_locking import (
    OptimisticLockError,
    OptimisticLockGuard,
)
from app.infrastructure.persistence.snapshot_store import SnapshotStore
from app.infrastructure.persistence.unit_of_work import (
    UnitOfWork,
    UnitOfWorkError,
)
from tests.infrastructure.helpers import AGGREGATES, LEARNERS, SUBJECTS


@pytest.mark.parametrize(
    "name",
    [c.name for c in AGGREGATE_CONTRACTS],
)
def test_contract_lookup(name):
    contract = contract_for(name)
    assert contract is not None
    assert contract.name == name
    assert isinstance(contract.owner, AggregateOwner)


@pytest.mark.parametrize(
    "name,owner",
    [(c.name, c.owner) for c in AGGREGATE_CONTRACTS],
)
def test_owner_for(name, owner):
    assert owner_for(name) is owner


def test_unknown_contract():
    assert contract_for("Nope") is None
    assert owner_for("Nope") is None


@pytest.mark.parametrize("aggregate", AGGREGATES)
@pytest.mark.parametrize("agg_id", LEARNERS)
def test_optimistic_lock_bump(aggregate, agg_id):
    guard = OptimisticLockGuard()
    t1 = guard.bump(aggregate, agg_id)
    assert t1.version == 1
    t2 = guard.bump(aggregate, agg_id, expected=1)
    assert t2.version == 2
    with pytest.raises(OptimisticLockError):
        guard.bump(aggregate, agg_id, expected=1)


@pytest.mark.parametrize("aggregate", AGGREGATES)
def test_optimistic_lock_seed(aggregate):
    guard = OptimisticLockGuard()
    guard.seed(aggregate, "x", 5)
    assert guard.current(aggregate, "x") == 5


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("subject_id", SUBJECTS)
def test_evidence_store_append_list(learner_id, subject_id):
    store = EvidenceStore()
    rec = store.append(
        learner_id=learner_id,
        subject_id=subject_id,
        evidence_type="practice",
        payload={"score": 0.8},
        correlation_id="c",
    )
    assert store.get(rec.record_id) is not None
    rows = store.list_for_learner(learner_id, subject_id=subject_id)
    assert len(rows) == 1
    assert rows[0].learner_id == learner_id


@pytest.mark.parametrize("learner_id", LEARNERS)
def test_evidence_duplicate_id_rejected(learner_id):
    store = EvidenceStore()
    store.append(
        learner_id=learner_id,
        subject_id="S",
        evidence_type="practice",
        record_id="same",
    )
    with pytest.raises(ValueError, match="duplicate"):
        store.append(
            learner_id=learner_id,
            subject_id="S",
            evidence_type="practice",
            record_id="same",
        )


@pytest.mark.parametrize("aggregate", AGGREGATES)
@pytest.mark.parametrize("agg_id", LEARNERS)
def test_snapshot_store_latest(aggregate, agg_id):
    store = SnapshotStore()
    store.save(aggregate, agg_id, {"n": 1})
    store.save(aggregate, agg_id, {"n": 2})
    latest = store.latest(aggregate, agg_id)
    assert latest is not None
    assert latest.payload["n"] == 2
    assert len(store.list_for(aggregate, agg_id)) == 2


def test_uow_begin_commit():
    uow = UnitOfWork()
    uow.begin()
    uow.register("repo", "save", {"id": "1"})
    assert uow.commit() == 1
    assert uow.is_committed is True
    assert uow.is_active is False


def test_uow_register_requires_active():
    uow = UnitOfWork()
    with pytest.raises(UnitOfWorkError):
        uow.register("repo", "save")


def test_uow_double_begin_rejected():
    uow = UnitOfWork()
    uow.begin()
    with pytest.raises(UnitOfWorkError):
        uow.begin()


def test_uow_transaction_rollback_on_error():
    uow = UnitOfWork()
    rolled = {"n": 0}
    uow.on_rollback(lambda: rolled.__setitem__("n", rolled["n"] + 1))
    with pytest.raises(RuntimeError):
        with uow.transaction():
            uow.register("repo", "save")
            raise RuntimeError("boom")
    assert rolled["n"] == 1
    assert uow.is_active is False


@pytest.mark.parametrize("op", ["save", "delete", "append"])
@pytest.mark.parametrize("repo", ["twin", "mission", "evidence"])
def test_uow_registers_operations(op, repo):
    uow = UnitOfWork()
    with uow.transaction():
        uow.register(repo, op, {"x": 1})
        assert len(uow.items) == 1
        assert uow.items[0].repository == repo
        assert uow.items[0].operation == op
