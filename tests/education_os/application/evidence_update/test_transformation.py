"""Transformation coverage for Educational Evidence Update (V3-007)."""

from __future__ import annotations

import pytest

from application.evidence_update import (
    EvidenceTransformer,
    EvidenceTransformError,
    EvidenceUpdateRequest,
)
from domain.education.evidence import EvidenceItemKind, EvidenceSourceKind
from tests.education_os.application.evidence_update import (
    make_captured,
    make_outcome,
    make_request,
)


def test_transform_maps_captured_evidence_to_record() -> None:
    request = make_request()
    record = EvidenceTransformer.transform(request)

    assert record.evidence_id.value == "evidence-session-001"
    assert record.student_id == "student-ada"
    assert record.source.kind is EvidenceSourceKind.REFLECTION_CAPTURE
    assert all(item.kind is EvidenceItemKind.REFLECTION for item in record.items)
    assert len(record.items) >= 4
    assert record.strength.level.value == "weak"
    assert record.timestamp.occurred_at.tzinfo is not None


def test_transform_includes_reflection_observation_fields() -> None:
    record = EvidenceTransformer.transform(make_request())
    observations = " | ".join(item.observation for item in record.items)

    assert "session_completion=completed" in observations
    assert "student_reported_confidence=confident" in observations
    assert "student_reported_difficulty=hard" in observations
    assert "student_noted_weak_concept=Conditional probability" in observations
    assert "student_notes=Need another worked example." in observations


def test_transform_attaches_known_concept_and_episode_ids() -> None:
    request = EvidenceUpdateRequest(
        captured=make_captured(),
        concept_ids=("concept-select",),
        learning_episode_ids=("episode-001",),
    )
    record = EvidenceTransformer.transform(request)

    assert any(
        ref.concept_id.value == "concept-select"
        for ref in record.concept_references
    )
    assert any(eid.value == "episode-001" for eid in record.learning_episode_ids)


def test_transform_rejects_missing_student_id() -> None:
    captured = make_captured(outcome=make_outcome(student_id=""))
    with pytest.raises(EvidenceTransformError, match="student_id"):
        EvidenceTransformer.from_captured(captured)


def test_transform_rejects_naive_timestamp() -> None:
    from datetime import datetime

    captured = make_captured(captured_at=datetime(2026, 7, 20, 14, 25, 30))
    with pytest.raises(EvidenceTransformError, match="timezone-aware"):
        EvidenceTransformer.from_captured(captured)


def test_transform_is_deterministic() -> None:
    request = make_request()
    first = EvidenceTransformer.transform(request)
    second = EvidenceTransformer.transform(request)

    assert first.evidence_id == second.evidence_id
    assert len(first.items) == len(second.items)
    assert [i.observation for i in first.items] == [
        i.observation for i in second.items
    ]
    assert first.confidence.level == second.confidence.level
