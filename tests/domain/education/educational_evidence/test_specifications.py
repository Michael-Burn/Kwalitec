"""Tests for Educational Evidence specifications."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.educational_evidence import (
    EducationalEvidence,
    EvidenceBelongsToStudentSpecification,
    EvidenceIsConsistentSpecification,
    EvidenceMetadata,
    NormalisedEvidenceSpecification,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.domain.education.educational_evidence.conftest import (
    make_environment,
    make_evidence_id,
    make_source,
)


def _question_answer(**overrides) -> EducationalEvidence:
    kwargs = {
        "competency_id": "algebra",
        "is_correct": True,
    }
    kwargs.update(overrides)
    return EducationalEvidence.record_question_answer(
        make_evidence_id(),
        "student-ada",
        datetime(2026, 7, 21, tzinfo=UTC),
        make_source(),
        learning_environment=make_environment(),
        **kwargs,
    )


class TestEvidenceIsConsistentSpecification:
    def test_satisfied_for_freshly_recorded_evidence(self) -> None:
        evidence = _question_answer()
        spec = EvidenceIsConsistentSpecification()
        assert spec.is_satisfied_by(evidence)
        spec.assert_satisfied_by(evidence)

    def test_unsatisfied_when_metadata_is_stripped_of_required_key(self) -> None:
        evidence = _question_answer()
        evidence._metadata = EvidenceMetadata.empty()  # simulate corrupted state
        spec = EvidenceIsConsistentSpecification()
        assert not spec.is_satisfied_by(evidence)
        with pytest.raises(EducationalInvariantViolation):
            spec.assert_satisfied_by(evidence)


class TestEvidenceBelongsToStudentSpecification:
    def test_satisfied_for_matching_student(self) -> None:
        evidence = _question_answer()
        spec = EvidenceBelongsToStudentSpecification()
        assert spec.is_satisfied_by(evidence, "student-ada")
        spec.assert_satisfied_by(evidence, "student-ada")

    def test_unsatisfied_for_different_student(self) -> None:
        evidence = _question_answer()
        spec = EvidenceBelongsToStudentSpecification()
        assert not spec.is_satisfied_by(evidence, "student-other")
        with pytest.raises(EducationalInvariantViolation):
            spec.assert_satisfied_by(evidence, "student-other")

    def test_unsatisfied_for_blank_student_id(self) -> None:
        evidence = _question_answer()
        spec = EvidenceBelongsToStudentSpecification()
        assert not spec.is_satisfied_by(evidence, "   ")


class TestNormalisedEvidenceSpecification:
    def test_satisfied_for_freshly_recorded_evidence(self) -> None:
        evidence = _question_answer()
        spec = NormalisedEvidenceSpecification()
        assert spec.is_satisfied_by(evidence)
        spec.assert_satisfied_by(evidence)

    def test_satisfied_after_explicit_normalisation(self) -> None:
        evidence = _question_answer().normalise()
        spec = NormalisedEvidenceSpecification()
        assert spec.is_satisfied_by(evidence)
