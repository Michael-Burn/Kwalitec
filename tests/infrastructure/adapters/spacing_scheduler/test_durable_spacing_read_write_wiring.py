"""Prove Spacing write/read share the durable SessionDocumentStore path.

Mirrors the Twin durability wiring tests: completions must land in
``v2_aggregate_documents`` when durable store is ON, and every consumer
(Revision, daily composer board, record_completed_exposure,
record_missed_review) must see that state through ``get_spacing_scheduler``
after a fresh construction (restart simulation).
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from app.application.spacing_scheduler import (
    SchedulingStatus,
    discard_canonical_spacing_scheduler_for_tests,
    get_spacing_scheduler,
)
from app.application.student_experience.revision_service import RevisionService
from app.extensions import db
from app.infrastructure.adapters.spacing_scheduler.document_store import (
    NS_SPACING_STATE,
    SessionDocumentSpacingStateStore,
)
from app.infrastructure.composition import build_spacing_state_store
from app.models.v2_aggregate import V2AggregateDocument

PACKAGE_A = "CS1-EP001-PKG-SPACING-DURABLE"
LEARNER = "4243"


def test_record_completed_exposure_survives_restart_via_sql(
    ctx, monkeypatch
) -> None:
    """Write via canonical facade; read after discarding the process singleton."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")
    discard_canonical_spacing_scheduler_for_tests()

    completed_on = date(2026, 9, 1)
    writer = get_spacing_scheduler()
    state = writer.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        completed_on=completed_on,
    )
    assert state.next_due_on == date(2026, 9, 2)

    rows = (
        db.session.query(V2AggregateDocument)
        .filter_by(aggregate_name="LearningSessionDocument")
        .all()
    )
    spacing_rows = [
        r
        for r in rows
        if NS_SPACING_STATE in (r.aggregate_id or "")
        and LEARNER in (r.aggregate_id or "")
        and PACKAGE_A in (r.aggregate_id or "")
    ]
    assert spacing_rows, (
        "expected durable spacing row in v2_aggregate_documents; "
        f"found aggregate_ids={[r.aggregate_id for r in rows]}"
    )

    # Simulate process restart: drop singleton, keep SQL rows.
    discard_canonical_spacing_scheduler_for_tests()
    del writer

    fresh = get_spacing_scheduler()
    restored = fresh.get_state(learner_id=LEARNER, package_id=PACKAGE_A)
    assert restored is not None
    assert restored.last_completed_on == completed_on
    assert restored.current_interval_days == 1
    assert restored.next_due_on == date(2026, 9, 2)

    board = fresh.revision_board(learner_id=LEARNER, as_of=date(2026, 9, 2))
    assert any(e.package_id == PACKAGE_A for e in board.due_now)

    revision = RevisionService(
        as_of_factory=lambda: date(2026, 9, 2),
    ).revision(LEARNER)
    assert any(item.package_id == PACKAGE_A for item in revision.due_now)


def test_all_consumers_share_single_canonical_durable_store(
    ctx, monkeypatch
) -> None:
    """Revision, board, completion, and miss all share durable SQL truth."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")
    discard_canonical_spacing_scheduler_for_tests()

    day0 = date(2026, 9, 1)
    scheduler = get_spacing_scheduler()
    scheduler.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        completed_on=day0,
    )
    # Advance past due (day0+1) without completing, then record the miss.
    miss_day = day0 + timedelta(days=3)
    scheduler.record_missed_review(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        as_of=miss_day,
    )

    discard_canonical_spacing_scheduler_for_tests()

    # Composer read path: revision_board via fresh canonical service.
    composer = get_spacing_scheduler()
    decision = composer.evaluate(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        as_of=miss_day,
    )
    assert decision.status is SchedulingStatus.NOT_DUE
    missed_state = composer.get_state(learner_id=LEARNER, package_id=PACKAGE_A)
    assert missed_state is not None
    assert missed_state.last_exposure_kind.value == "missed_review"

    # Revision read path: no injected store; must use get_spacing_scheduler.
    snapshot = RevisionService(as_of_factory=lambda: miss_day).revision(LEARNER)
    unit_ids = {item.package_id for item in snapshot.upcoming} | {
        item.package_id for item in snapshot.due_now
    } | {item.package_id for item in snapshot.recently_reviewed}
    assert PACKAGE_A in unit_ids

    # Independent factory construction still sees the same SQL rows.
    independent = build_spacing_state_store()
    assert isinstance(independent, SessionDocumentSpacingStateStore)
    again = independent.get(LEARNER, PACKAGE_A)
    assert again is not None
    assert again.review_cycle_count == missed_state.review_cycle_count


def test_bare_in_memory_spacing_store_isolates_when_durable_off(
    ctx, monkeypatch
) -> None:
    """Explicit in-memory adapter must not see durable SQL rows."""
    from app.application.spacing_scheduler.store import InMemorySpacingStateStore
    from app.infrastructure.session.store import SessionDocumentStore

    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")
    discard_canonical_spacing_scheduler_for_tests()
    get_spacing_scheduler().record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        completed_on=date(2026, 9, 1),
    )

    bare_memory = InMemorySpacingStateStore()
    assert bare_memory.get(LEARNER, PACKAGE_A) is None

    bare_docs = SessionDocumentSpacingStateStore(store=SessionDocumentStore())
    assert bare_docs.get(LEARNER, PACKAGE_A) is None


def test_production_consumers_do_not_construct_independent_stores() -> None:
    """Guard: Revision / ERE / routes must call get_spacing_scheduler only."""
    targets = [
        Path("app/application/student_experience/revision_service.py"),
        Path("app/application/educational_runtime_engine/service.py"),
        Path("app/presentation/student/routes.py"),
    ]
    forbidden = (
        "InMemorySpacingStateStore(",
        "SessionDocumentSpacingStateStore(",
        "build_spacing_state_store(",
        "SpacingSchedulerService(",
    )
    for path in targets:
        source = path.read_text(encoding="utf-8")
        assert "get_spacing_scheduler" in source, path.name
        for needle in forbidden:
            assert needle not in source, f"{path.name} must not contain {needle}"

    service_src = Path("app/application/spacing_scheduler/service.py").read_text(
        encoding="utf-8"
    )
    assert "build_spacing_state_store" in service_src
    assert "InMemorySpacingStateStore()" not in service_src
