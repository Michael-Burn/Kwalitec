"""Store / consumer fail-open tests (EP-004.1)."""

from __future__ import annotations

from app.infrastructure.adapters.learning_feedback.contracts import (
    CLAIM_PREFERENCE_JOURNAL,
    FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
    SOURCE_RECOMMENDATION,
    LearningFeedbackEvent,
    deterministic_feedback_id,
)
from app.infrastructure.adapters.personal_learning_profile import (
    REASON_FLAG_OFF,
    RESOLVE_STATUS_OK,
    RESOLVE_STATUS_SKIPPED,
    PersonalLearningProfileStore,
    bind_personal_learning_profile_store,
    build_personal_learning_profile_store,
    consume_personal_learning_profile,
    resolve_personal_learning_profile,
)


def setup_function() -> None:
    bind_personal_learning_profile_store(None)


def teardown_function() -> None:
    bind_personal_learning_profile_store(None)


def _accept_event(student_id: str = "10") -> LearningFeedbackEvent:
    payload = {"accepted": True}
    ts = "2026-07-26T09:00:00Z"
    feedback_id = deterministic_feedback_id(
        student_id=student_id,
        timestamp=ts,
        event_type=FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
        source_authority=SOURCE_RECOMMENDATION,
        claim_boundary=CLAIM_PREFERENCE_JOURNAL,
        payload=payload,
        correlation_id="x",
    )
    return LearningFeedbackEvent(
        feedback_id=feedback_id,
        timestamp=ts,
        event_type=FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
        source_authority=SOURCE_RECOMMENDATION,
        claim_boundary=CLAIM_PREFERENCE_JOURNAL,
        student_id=student_id,
        payload=payload,
        correlation_id="x",
    )


def test_build_store_returns_none_when_disabled():
    assert build_personal_learning_profile_store(enabled=False) is None


def test_disabled_store_skips_resolve():
    store = PersonalLearningProfileStore(enabled=False)
    result = store.resolve("1", events=[])
    assert result.ok is False
    assert result.status == RESOLVE_STATUS_SKIPPED
    assert result.reason == REASON_FLAG_OFF


def test_incremental_upsert_replaces_snapshot():
    store = PersonalLearningProfileStore(enabled=True)
    first = store.resolve(
        "10",
        events=[],
        as_of="2026-07-26T10:00:00Z",
    )
    assert first.ok and first.profile is not None
    second = store.resolve(
        "10",
        events=[_accept_event()],
        as_of="2026-07-26T11:00:00Z",
    )
    assert second.ok and second.profile is not None
    cached = store.get_cached("10")
    assert cached is not None
    assert cached.profile_id == second.profile.profile_id
    assert cached.evidence_event_count == 1
    assert store.stats()["update_count"] == 2


def test_consumer_fail_open_when_unbound():
    bind_personal_learning_profile_store(None)
    view = consume_personal_learning_profile(student_id="99")
    # Flag default OFF → None
    assert view is None


def test_consumer_returns_stable_view_when_bound():
    store = PersonalLearningProfileStore(enabled=True)
    bind_personal_learning_profile_store(store)
    view = consume_personal_learning_profile(
        student_id="10",
        events=[_accept_event()],
        as_of="2026-07-26T10:00:00Z",
    )
    assert view is not None
    assert view["student_id"] == "10"
    assert "attributes" in view
    assert "evidence_fingerprint" not in view


def test_resolve_fail_open_on_store_exception():
    class Boom:
        enabled = True

        def resolve(self, *args, **kwargs):  # noqa: ANN002, ANN003
            raise RuntimeError("store down")

    result = resolve_personal_learning_profile(
        student_id="1",
        store=Boom(),
    )
    assert result.ok is False
    assert result.status == "failed"


def test_resolve_ok_path():
    store = PersonalLearningProfileStore(enabled=True)
    result = resolve_personal_learning_profile(
        student_id="10",
        events=[_accept_event()],
        as_of="2026-07-26T10:00:00Z",
        store=store,
    )
    assert result.status == RESOLVE_STATUS_OK
    assert result.profile is not None
