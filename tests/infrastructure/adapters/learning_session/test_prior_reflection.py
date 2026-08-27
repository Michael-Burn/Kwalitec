"""Tier A prior-reflection lookup — resurface only, no interpretation."""

from __future__ import annotations

from datetime import date

import pytest

from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
    is_substantive_reflection_note,
)
from app.infrastructure.session.store import SessionDocumentStore


def _seed_handle(
    store: SessionDocumentStore,
    *,
    session_id: str,
    student_id: str = "stu-1",
    topic_id: str = "topic-glm",
    reflection_note: str = "",
    mission_instance_id: str = "",
    version: int | None = None,
) -> None:
    doc: dict = {
        "session_id": session_id,
        "student_id": student_id,
        "topic_id": topic_id,
        "mission_instance_id": mission_instance_id,
        "reflection_note": reflection_note,
        "status": "completed",
    }
    if version is not None:
        doc["_version"] = version
    store.save("lsr.handle", session_id, doc)


def test_is_substantive_reflection_note_thresholds() -> None:
    assert not is_substantive_reflection_note("")
    assert not is_substantive_reflection_note("   ")
    assert not is_substantive_reflection_note("ok")
    assert not is_substantive_reflection_note("fine")
    assert not is_substantive_reflection_note("good")
    assert not is_substantive_reflection_note("short")  # < 12
    assert is_substantive_reflection_note(
        "I got stuck on Bayes theorem again."
    )


def test_a_genuine_past_reflection_same_topic_returns_text() -> None:
    store = SessionDocumentStore()
    past = "I got stuck on the link function choice."
    _seed_handle(
        store,
        session_id="sess-past",
        reflection_note=past,
        mission_instance_id="m-past",
    )
    _seed_handle(
        store,
        session_id="sess-current",
        reflection_note="",
        mission_instance_id="m-now",
    )
    adapter = LearningSessionPersistenceAdapter(store=store)
    assert (
        adapter.find_prior_reflection_note(
            student_id="stu-1",
            topic_id="topic-glm",
            exclude_session_id="sess-current",
        )
        == past
    )


def test_b_trivial_past_reflection_filtered_out() -> None:
    store = SessionDocumentStore()
    _seed_handle(
        store,
        session_id="sess-past",
        reflection_note="ok",
    )
    _seed_handle(store, session_id="sess-current")
    adapter = LearningSessionPersistenceAdapter(store=store)
    assert (
        adapter.find_prior_reflection_note(
            student_id="stu-1",
            topic_id="topic-glm",
            exclude_session_id="sess-current",
        )
        is None
    )


def test_c_different_topic_id_does_not_match() -> None:
    store = SessionDocumentStore()
    _seed_handle(
        store,
        session_id="sess-past",
        topic_id="topic-other",
        reflection_note="I got stuck on the link function choice.",
    )
    _seed_handle(
        store,
        session_id="sess-current",
        topic_id="topic-glm",
    )
    adapter = LearningSessionPersistenceAdapter(store=store)
    assert (
        adapter.find_prior_reflection_note(
            student_id="stu-1",
            topic_id="topic-glm",
            exclude_session_id="sess-current",
        )
        is None
    )


def test_d_current_session_note_never_confused_with_past() -> None:
    store = SessionDocumentStore()
    past = "Last time the exponential family examples helped."
    current_note = "I am mid-session and this is the current draft."
    _seed_handle(
        store,
        session_id="sess-past",
        reflection_note=past,
        version=1,
    )
    _seed_handle(
        store,
        session_id="sess-current",
        reflection_note=current_note,
        version=99,
    )
    adapter = LearningSessionPersistenceAdapter(store=store)
    result = adapter.find_prior_reflection_note(
        student_id="stu-1",
        topic_id="topic-glm",
        exclude_session_id="sess-current",
    )
    assert result == past
    assert result != current_note


def test_e_most_recent_by_mission_date(monkeypatch: pytest.MonkeyPatch) -> None:
    store = SessionDocumentStore()
    older = "Older note about the canonical parameter."
    newer = "More recent note about the mean response."
    _seed_handle(
        store,
        session_id="sess-older",
        reflection_note=older,
        mission_instance_id="m-older",
    )
    _seed_handle(
        store,
        session_id="sess-newer",
        reflection_note=newer,
        mission_instance_id="m-newer",
    )
    _seed_handle(store, session_id="sess-current", mission_instance_id="m-now")

    dates = {
        "m-older": date(2026, 1, 10),
        "m-newer": date(2026, 2, 15),
    }

    def _fake_date(mid: str) -> date | None:
        return dates.get(mid)

    monkeypatch.setattr(
        "app.infrastructure.adapters.learning_session.persistence."
        "_mission_date_for_instance",
        _fake_date,
    )
    adapter = LearningSessionPersistenceAdapter(store=store)
    assert (
        adapter.find_prior_reflection_note(
            student_id="stu-1",
            topic_id="topic-glm",
            exclude_session_id="sess-current",
        )
        == newer
    )


def test_e_most_recent_by_version_when_no_dates() -> None:
    store = SessionDocumentStore()
    older = "Older versioned reflection on this topic."
    newer = "Newer versioned reflection on this topic."
    _seed_handle(
        store,
        session_id="sess-a",
        reflection_note=older,
        version=2,
    )
    _seed_handle(
        store,
        session_id="sess-b",
        reflection_note=newer,
        version=7,
    )
    _seed_handle(store, session_id="sess-current", version=8)
    adapter = LearningSessionPersistenceAdapter(store=store)
    assert (
        adapter.find_prior_reflection_note(
            student_id="stu-1",
            topic_id="topic-glm",
            exclude_session_id="sess-current",
        )
        == newer
    )
