"""Value object tests for Evidence domain."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.evidence import (
    ConfidenceMeasure,
    EvidenceStrength,
    EvidenceStrengthLevel,
    EvidenceTimestamp,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation


class TestEvidenceStrength:
    @pytest.mark.parametrize(
        "factory,level",
        [
            (EvidenceStrength.weak, EvidenceStrengthLevel.WEAK),
            (EvidenceStrength.moderate, EvidenceStrengthLevel.MODERATE),
            (EvidenceStrength.strong, EvidenceStrengthLevel.STRONG),
            (EvidenceStrength.very_strong, EvidenceStrengthLevel.VERY_STRONG),
        ],
    )
    def test_factories(self, factory, level) -> None:
        strength = factory()
        assert strength.level is level
        assert str(strength) == level.value

    @pytest.mark.parametrize(
        "quality,expected",
        [
            (0, EvidenceStrengthLevel.WEAK),
            (1, EvidenceStrengthLevel.WEAK),
            (2, EvidenceStrengthLevel.MODERATE),
            (3, EvidenceStrengthLevel.STRONG),
            (4, EvidenceStrengthLevel.VERY_STRONG),
        ],
    )
    def test_from_quality_level(
        self, quality: int, expected: EvidenceStrengthLevel
    ) -> None:
        assert EvidenceStrength.from_quality_level(quality).level is expected

    @pytest.mark.parametrize("bad", [-1, 5, 99])
    def test_quality_level_out_of_range(self, bad: int) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            EvidenceStrength.from_quality_level(bad)
        assert exc.value.invariant == "EvidenceStrength.quality_level.range"

    def test_quality_level_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceStrength.from_quality_level("3")  # type: ignore[arg-type]

    def test_level_type_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceStrength(level="strong")  # type: ignore[arg-type]

    def test_predicates(self) -> None:
        assert EvidenceStrength.weak().is_weak()
        assert EvidenceStrength.moderate().is_moderate()
        assert EvidenceStrength.strong().is_strong()
        assert EvidenceStrength.very_strong().is_very_strong()

    def test_at_least(self) -> None:
        assert EvidenceStrength.strong().at_least(EvidenceStrength.moderate())
        assert EvidenceStrength.moderate().at_least(EvidenceStrength.moderate())
        assert not EvidenceStrength.weak().at_least(EvidenceStrength.strong())

    def test_at_least_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceStrength.strong().at_least("moderate")  # type: ignore[arg-type]

    def test_frozen(self) -> None:
        strength = EvidenceStrength.strong()
        with pytest.raises(Exception):
            strength.level = EvidenceStrengthLevel.WEAK  # type: ignore[misc]

    def test_equality(self) -> None:
        assert EvidenceStrength.strong() == EvidenceStrength(
            level=EvidenceStrengthLevel.STRONG
        )


class TestEvidenceTimestamp:
    def test_of_aware(self) -> None:
        dt = datetime(2026, 7, 19, 12, 0, tzinfo=UTC)
        ts = EvidenceTimestamp.of(dt)
        assert ts.occurred_at == dt
        assert "2026-07-19" in str(ts)

    def test_from_utc_components(self) -> None:
        ts = EvidenceTimestamp.from_utc_components(2026, 1, 2, 3, 4, 5)
        assert ts.occurred_at.year == 2026
        assert ts.occurred_at.tzinfo is UTC

    def test_naive_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            EvidenceTimestamp.of(datetime(2026, 7, 19, 12, 0))
        assert exc.value.invariant == "EvidenceTimestamp.occurred_at.timezone_aware"

    def test_type_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceTimestamp(occurred_at="2026-07-19")  # type: ignore[arg-type]

    def test_ordering(self) -> None:
        earlier = EvidenceTimestamp.from_utc_components(2026, 7, 19, 9)
        later = EvidenceTimestamp.from_utc_components(2026, 7, 19, 11)
        assert earlier.is_before(later)
        assert later.is_after(earlier)
        assert not later.is_before(earlier)

    def test_ordering_type(self) -> None:
        ts = EvidenceTimestamp.from_utc_components(2026, 7, 19)
        with pytest.raises(EducationalInvariantViolation):
            ts.is_before("now")  # type: ignore[arg-type]
        with pytest.raises(EducationalInvariantViolation):
            ts.is_after("now")  # type: ignore[arg-type]

    def test_frozen(self) -> None:
        ts = EvidenceTimestamp.from_utc_components(2026, 7, 19)
        with pytest.raises(Exception):
            ts.occurred_at = datetime.now(UTC)  # type: ignore[misc]


class TestConfidenceMeasure:
    @pytest.mark.parametrize(
        "level",
        [
            ConfidenceLevel.VERY_LOW,
            ConfidenceLevel.LOW,
            ConfidenceLevel.MEDIUM,
            ConfidenceLevel.HIGH,
            ConfidenceLevel.VERY_HIGH,
        ],
    )
    def test_known_levels(self, level: ConfidenceLevel) -> None:
        measure = ConfidenceMeasure.of(level)
        assert measure.level is level
        assert measure.ratio is None

    def test_with_ratio(self) -> None:
        measure = ConfidenceMeasure.of(ConfidenceLevel.HIGH, ratio=0.9)
        assert measure.ratio == 0.9
        assert "high" in str(measure)

    def test_unknown_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            ConfidenceMeasure.of(ConfidenceLevel.UNKNOWN)
        assert exc.value.invariant == "ConfidenceMeasure.level.known"

    @pytest.mark.parametrize("ratio", [-0.1, 1.1, 2.0])
    def test_ratio_range(self, ratio: float) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConfidenceMeasure.of(ConfidenceLevel.MEDIUM, ratio=ratio)

    def test_ratio_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConfidenceMeasure.of(ConfidenceLevel.MEDIUM, ratio=True)  # type: ignore[arg-type]

    def test_level_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConfidenceMeasure(level="high")  # type: ignore[arg-type]

    def test_is_at_least(self) -> None:
        high = ConfidenceMeasure.of(ConfidenceLevel.HIGH)
        assert high.is_at_least(ConfidenceLevel.MEDIUM)
        assert high.is_at_least(ConfidenceLevel.HIGH)
        assert not high.is_at_least(ConfidenceLevel.VERY_HIGH)

    def test_is_at_least_unknown(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConfidenceMeasure.of(ConfidenceLevel.HIGH).is_at_least(
                ConfidenceLevel.UNKNOWN
            )

    def test_frozen(self) -> None:
        measure = ConfidenceMeasure.of(ConfidenceLevel.MEDIUM)
        with pytest.raises(Exception):
            measure.level = ConfidenceLevel.LOW  # type: ignore[misc]

    def test_int_ratio_coerced(self) -> None:
        measure = ConfidenceMeasure.of(ConfidenceLevel.MEDIUM, ratio=1)
        assert measure.ratio == 1.0
