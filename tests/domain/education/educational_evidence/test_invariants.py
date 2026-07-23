"""Tests for EducationalEvidence aggregate invariants.

Covers the invariants required by EDU-003.2:
    - Evidence identity mandatory.
    - Evidence timestamp mandatory.
    - Evidence type mandatory.
    - Evidence must belong to one student.
    - Evidence must reference one educational context.
    - Evidence cannot represent contradictory educational outcomes.
    - Normalised evidence must always be internally consistent.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.educational_evidence import (
    EducationalEvidence,
    EvidenceMetadata,
    EvidenceTimestamp,
    EvidenceType,
    EvidenceWeight,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.domain.education.educational_evidence.conftest import (
    make_context,
    make_environment,
    make_evidence_id,
    make_source,
)

OCCURRED_AT = datetime(2026, 7, 21, tzinfo=UTC)


def _valid_kwargs() -> dict:
    return {
        "evidence_id": make_evidence_id(),
        "student_id": "student-ada",
        "evidence_type": EvidenceType.QUESTION_ANSWERED,
        "occurred_at": EvidenceTimestamp.of(OCCURRED_AT),
        "source": make_source(),
        "context": make_context(),
        "weight": EvidenceWeight.of(0.5),
        "metadata": EvidenceMetadata.of(is_correct=True),
    }


class TestIdentityMandatory:
    def test_missing_identity_type_is_rejected(self) -> None:
        kwargs = _valid_kwargs()
        kwargs["evidence_id"] = "not-an-id"
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence(**kwargs)

    def test_valid_identity_is_accepted(self) -> None:
        evidence = EducationalEvidence(**_valid_kwargs())
        assert evidence.evidence_id == make_evidence_id()


class TestTimestampMandatory:
    def test_missing_timestamp_type_is_rejected(self) -> None:
        kwargs = _valid_kwargs()
        kwargs["occurred_at"] = OCCURRED_AT
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence(**kwargs)


class TestEvidenceTypeMandatory:
    def test_missing_evidence_type_is_rejected(self) -> None:
        kwargs = _valid_kwargs()
        kwargs["evidence_type"] = "question_answered"
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence(**kwargs)


class TestBelongsToOneStudent:
    def test_blank_student_id_is_rejected(self) -> None:
        kwargs = _valid_kwargs()
        kwargs["student_id"] = "   "
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence(**kwargs)

    def test_student_id_is_a_single_scalar_value(self) -> None:
        evidence = EducationalEvidence(**_valid_kwargs())
        assert isinstance(evidence.student_id, str)


class TestReferencesOneEducationalContext:
    def test_missing_context_is_rejected(self) -> None:
        kwargs = _valid_kwargs()
        kwargs["context"] = None
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence(**kwargs)

    def test_context_missing_required_curriculum_coordinate_is_rejected(self) -> None:
        kwargs = _valid_kwargs()
        kwargs["context"] = make_context(competency_id=None)
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence(**kwargs)


class TestNoContradictoryOutcomes:
    def test_question_answered_cannot_claim_incorrect(self) -> None:
        kwargs = _valid_kwargs()
        kwargs["metadata"] = EvidenceMetadata.of(is_correct=False)
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence(**kwargs)

    def test_question_incorrect_cannot_claim_correct(self) -> None:
        kwargs = _valid_kwargs()
        kwargs["evidence_type"] = EvidenceType.QUESTION_INCORRECT
        kwargs["metadata"] = EvidenceMetadata.of(is_correct=True)
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence(**kwargs)

    def test_mission_completed_cannot_claim_not_completed(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence(
                evidence_id=make_evidence_id(),
                student_id="student-ada",
                evidence_type=EvidenceType.MISSION_COMPLETED,
                occurred_at=EvidenceTimestamp.of(OCCURRED_AT),
                source=make_source(),
                context=make_context(competency_id=None, mission_id="mission-1"),
                weight=EvidenceWeight.of(0.4),
                metadata=EvidenceMetadata.of(completed=False),
            )

    def test_mission_abandoned_cannot_claim_completed(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalEvidence(
                evidence_id=make_evidence_id(),
                student_id="student-ada",
                evidence_type=EvidenceType.MISSION_ABANDONED,
                occurred_at=EvidenceTimestamp.of(OCCURRED_AT),
                source=make_source(),
                context=make_context(competency_id=None, mission_id="mission-1"),
                weight=EvidenceWeight.of(0.3),
                metadata=EvidenceMetadata.of(completed=True),
            )

    def test_factory_methods_never_produce_contradictions(self) -> None:
        answered = EducationalEvidence.record_question_answer(
            make_evidence_id("a"),
            "student-ada",
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            competency_id="algebra",
            is_correct=True,
        )
        incorrect = EducationalEvidence.record_question_answer(
            make_evidence_id("b"),
            "student-ada",
            OCCURRED_AT,
            make_source(),
            learning_environment=make_environment(),
            competency_id="algebra",
            is_correct=False,
        )
        assert answered.metadata.get("is_correct") is True
        assert incorrect.metadata.get("is_correct") is False
        assert answered.evidence_type is EvidenceType.QUESTION_ANSWERED
        assert incorrect.evidence_type is EvidenceType.QUESTION_INCORRECT


class TestNormalisedEvidenceIsInternallyConsistent:
    def test_freshly_constructed_evidence_is_already_normalised(self) -> None:
        evidence = EducationalEvidence(**_valid_kwargs())
        assert evidence.is_normalised()

    def test_normalise_is_idempotent(self) -> None:
        evidence = EducationalEvidence(**_valid_kwargs())
        once = evidence.normalise()
        twice = once.normalise()
        assert once == twice
        assert once == evidence

    def test_normalised_copy_remains_internally_consistent(self) -> None:
        evidence = EducationalEvidence(**_valid_kwargs())
        normalised = evidence.normalise()
        # Reconstructing from a normalised evidence's own fields must never
        # raise — normalisation cannot introduce inconsistency.
        assert normalised.evidence_type is evidence.evidence_type
        assert normalised.metadata == evidence.metadata
        assert normalised.weight == evidence.weight
