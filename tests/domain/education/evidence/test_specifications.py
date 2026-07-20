"""Specification tests for Evidence domain."""

from __future__ import annotations

import pytest

from domain.education.evidence import (
    EvidenceIsConsistentSpecification,
    EvidenceIsSufficientSpecification,
    EvidenceItemKind,
    EvidenceSourceKind,
    EvidenceStrength,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.domain.education.evidence.conftest import (
    make_confidence,
    make_item,
    make_record,
    make_source,
)


class TestEvidenceIsSufficientSpecification:
    def test_active_record_sufficient(self) -> None:
        record = make_record()
        assert EvidenceIsSufficientSpecification().is_satisfied_by(record)

    def test_invalidated_not_sufficient(self) -> None:
        record = make_record()
        record.invalidate("void")
        assert not EvidenceIsSufficientSpecification().is_satisfied_by(record)

    def test_amended_not_active_sufficient(self) -> None:
        record = make_record()
        record.amend()
        assert not EvidenceIsSufficientSpecification().is_satisfied_by(record)

    def test_assert_satisfied(self) -> None:
        EvidenceIsSufficientSpecification().assert_satisfied_by(make_record())

    def test_assert_unsatisfied(self) -> None:
        record = make_record()
        record.invalidate("void")
        with pytest.raises(EducationalInvariantViolation) as exc:
            EvidenceIsSufficientSpecification().assert_satisfied_by(record)
        assert exc.value.invariant == "EvidenceIsSufficientSpecification.unsatisfied"


class TestEvidenceIsConsistentSpecification:
    def test_consistent_record(self) -> None:
        record = make_record()
        assert EvidenceIsConsistentSpecification().is_satisfied_by(record)

    def test_invalidated_inconsistent_for_spec(self) -> None:
        record = make_record()
        record.invalidate("void")
        assert not EvidenceIsConsistentSpecification().is_satisfied_by(record)

    def test_assert_satisfied(self) -> None:
        EvidenceIsConsistentSpecification().assert_satisfied_by(make_record())

    def test_soft_very_strong_fails_construction(self) -> None:
        """Inconsistent soft+very_strong cannot enter the aggregate."""
        with pytest.raises(EducationalInvariantViolation):
            make_record(
                items=[
                    make_item(
                        kind=EvidenceItemKind.REFLECTION,
                        observation="Felt unsure about select ages",
                    )
                ],
                source=make_source(kind=EvidenceSourceKind.REFLECTION_CAPTURE),
                strength=EvidenceStrength.very_strong(),
                confidence=make_confidence(ConfidenceLevel.VERY_HIGH),
            )
