"""Prove Learning Session constructors default to the composition store.

Regression for the Twin-class silent-divergence defect: when
``KWALITEC_V2_DURABLE_STORE=1``, bare ``PackageActivityEngine()`` and
``LearningSessionPersistenceAdapter()`` must share SQL-backed documents
with ``build_session_document_store()``, not a separate empty memory map.
"""

from __future__ import annotations

from app.extensions import db
from app.infrastructure.adapters.learning_session.package_activity_engine import (
    PackageActivityEngine,
)
from app.infrastructure.adapters.learning_session.persistence import (
    NS_HANDLE,
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.composition import build_session_document_store
from app.infrastructure.session.store import SessionDocumentStore
from app.models.v2_aggregate import V2AggregateDocument


def test_bare_persistence_adapter_sees_durable_composition_writes(
    ctx, monkeypatch
) -> None:
    """Default LearningSessionPersistenceAdapter reads durable SQL rows."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")

    session_id = "lsr-bare-ctor-persist-1"
    student_id = "5152"
    write_store = build_session_document_store()
    write_store.save(
        NS_HANDLE,
        session_id,
        {
            "session_id": session_id,
            "student_id": student_id,
            "phase": "active",
        },
    )

    rows = (
        db.session.query(V2AggregateDocument)
        .filter_by(aggregate_name="LearningSessionDocument")
        .all()
    )
    handle_rows = [
        r
        for r in rows
        if NS_HANDLE in (r.aggregate_id or "") and session_id in (r.aggregate_id or "")
    ]
    assert handle_rows, (
        "expected durable handle row; "
        f"found aggregate_ids={[r.aggregate_id for r in rows]}"
    )

    del write_store

    # Bare default constructor (no injected store) must resolve composition.
    bare = LearningSessionPersistenceAdapter()
    loaded = bare.store.get(NS_HANDLE, session_id)
    assert loaded is not None
    assert loaded.get("student_id") == student_id


def test_bare_package_activity_engine_sees_durable_composition_writes(
    ctx, monkeypatch
) -> None:
    """Default PackageActivityEngine shares durable response documents."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")

    student_id = "5153"
    session_id = "lsr-bare-ctor-engine-1"
    key = f"{student_id}::{session_id}"
    write_store = build_session_document_store()
    write_store.save(
        PackageActivityEngine.NS_RESPONSES,
        key,
        {
            "student_id": student_id,
            "session_id": session_id,
            "items": [{"activity_id": "a1", "response": "42"}],
        },
    )
    del write_store

    bare = PackageActivityEngine()
    loaded = bare._store.get(PackageActivityEngine.NS_RESPONSES, key)
    assert loaded is not None
    assert loaded.get("session_id") == session_id
    assert len(loaded.get("items") or []) == 1


def test_explicit_bare_memory_store_still_isolates(ctx, monkeypatch) -> None:
    """Explicit SessionDocumentStore() must not see durable SQL rows."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")

    session_id = "lsr-bare-ctor-isolate-1"
    build_session_document_store().save(
        NS_HANDLE,
        session_id,
        {"session_id": session_id, "student_id": "5154"},
    )

    isolated = LearningSessionPersistenceAdapter(store=SessionDocumentStore())
    assert isolated.store.get(NS_HANDLE, session_id) is None

    isolated_engine = PackageActivityEngine(store=SessionDocumentStore())
    assert isolated_engine._store.get(NS_HANDLE, session_id) is None
