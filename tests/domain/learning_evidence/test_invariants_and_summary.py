"""Domain tests for Learning Evidence Engine (EI-005)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from app.domain.learning_evidence.evidence_type import (
    EvidenceSource,
    EvidenceType,
    is_extensible_type_token,
    is_known_evidence_type,
    normalise_evidence_type,
)
from app.domain.learning_evidence.invariants import (
    EvidenceInvariant,
    EvidenceInvariantError,
    assert_can_record,
    assert_valid_timestamp,
)
from app.domain.learning_evidence.payload_schema import assert_payload_schema
from app.domain.learning_evidence.summary import count_by_type


def test_catalogue_and_extensible_types() -> None:
    assert is_known_evidence_type(EvidenceType.PRACTICE_ATTEMPT)
    assert is_known_evidence_type("reading_completed")
    assert not is_known_evidence_type("flashcard_review")
    assert is_extensible_type_token("flashcard_review")
    assert not is_extensible_type_token("Not Valid")
    assert normalise_evidence_type(" Study_Session ") == "study_session"


def test_assert_can_record_happy_path() -> None:
    now = datetime(2026, 7, 28, 12, 0, 0)
    result = assert_can_record(
        instance_id="sci-1",
        instance_is_active=True,
        node_stable_id="CS1.T1.S1.LO1",
        node_belongs_to_instance=True,
        evidence_type=EvidenceType.STUDY_SESSION,
        source=EvidenceSource.SESSION_RUNTIME,
        occurred_at=now,
        now=now,
    )
    assert result == "study_session"


def test_assert_can_record_rejects_inactive_and_foreign_node() -> None:
    now = datetime(2026, 7, 28, 12, 0, 0)
    with pytest.raises(EvidenceInvariantError) as inactive:
        assert_can_record(
            instance_id="sci-1",
            instance_is_active=False,
            node_stable_id="CS1.T1",
            node_belongs_to_instance=True,
            evidence_type="practice_attempt",
            source="student_runtime",
            occurred_at=now,
            now=now,
        )
    assert inactive.value.invariant is EvidenceInvariant.ACTIVE_INSTANCE_REQUIRED

    with pytest.raises(EvidenceInvariantError) as missing:
        assert_can_record(
            instance_id="sci-missing",
            instance_is_active=None,
            node_stable_id="CS1.T1",
            node_belongs_to_instance=False,
            evidence_type="practice_attempt",
            source="student_runtime",
            occurred_at=now,
            now=now,
        )
    assert missing.value.invariant is EvidenceInvariant.ACTIVE_INSTANCE_REQUIRED

    with pytest.raises(EvidenceInvariantError) as foreign:
        assert_can_record(
            instance_id="sci-1",
            instance_is_active=True,
            node_stable_id="OTHER.NODE",
            node_belongs_to_instance=False,
            evidence_type="practice_attempt",
            source="student_runtime",
            occurred_at=now,
            now=now,
        )
    assert foreign.value.invariant is EvidenceInvariant.NODE_IN_INSTANCE


def test_timestamp_and_source_validation() -> None:
    now = datetime(2026, 7, 28, 12, 0, 0, tzinfo=UTC).replace(tzinfo=None)
    assert_valid_timestamp(now, now=now)
    with pytest.raises(EvidenceInvariantError) as future:
        assert_valid_timestamp(now + timedelta(days=3), now=now)
    assert future.value.invariant is EvidenceInvariant.VALID_TIMESTAMP

    with pytest.raises(EvidenceInvariantError) as source:
        assert_can_record(
            instance_id="sci-1",
            instance_is_active=True,
            node_stable_id="CS1.T1",
            node_belongs_to_instance=True,
            evidence_type="study_session",
            source="telepathy",
            occurred_at=now,
            now=now,
        )
    assert source.value.invariant is EvidenceInvariant.VALID_SOURCE


def test_payload_schema_founder_override_and_typed_optional() -> None:
    with pytest.raises(EvidenceInvariantError):
        assert_payload_schema(
            EvidenceType.MANUAL_FOUNDER_OVERRIDE,
            {},
        )
    ok = assert_payload_schema(
        EvidenceType.MANUAL_FOUNDER_OVERRIDE,
        {"reason": "Correct mis-tagged node observation"},
    )
    assert ok["reason"].startswith("Correct")

    with pytest.raises(EvidenceInvariantError):
        assert_payload_schema(
            EvidenceType.PRACTICE_ATTEMPT,
            {"correct": "yes"},
        )
    assert assert_payload_schema(
        EvidenceType.PRACTICE_ATTEMPT,
        {"correct": True, "item_id": "q-1"},
    )["correct"] is True

    # Extensible types accept any object.
    assert assert_payload_schema("custom_observation", {"note": "ok"})["note"] == "ok"


def test_count_by_type_deterministic() -> None:
    summary = count_by_type(
        ["practice_attempt", "study_session", "practice_attempt", "reading_completed"]
    )
    assert summary.total == 4
    assert summary.by_type == (
        ("practice_attempt", 2),
        ("reading_completed", 1),
        ("study_session", 1),
    )
    assert summary.to_dict()["by_type"]["practice_attempt"] == 2
