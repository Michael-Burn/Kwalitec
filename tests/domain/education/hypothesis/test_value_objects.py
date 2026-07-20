"""Unit tests for Educational Hypothesis value objects."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.hypothesis import (
    ExplanatoryStrength,
    ExplanatoryStrengthLevel,
    Plausibility,
    PlausibilityLevel,
)


@pytest.mark.parametrize("level", list(PlausibilityLevel))
def test_plausibility_accepts_all_levels(level: PlausibilityLevel) -> None:
    measure = Plausibility.of(level)
    assert measure.level is level


@pytest.mark.parametrize("ratio", [None, 0.0, 0.25, 0.5, 0.75, 1.0])
def test_plausibility_ratio_matrix(ratio: float | None) -> None:
    measure = Plausibility.working(ratio=ratio)
    assert measure.ratio == (None if ratio is None else float(ratio))


@pytest.mark.parametrize("bad_ratio", [-0.01, 1.01, True, "0.5"])
def test_plausibility_rejects_bad_ratio(bad_ratio: object) -> None:
    with pytest.raises(EducationalInvariantViolation):
        Plausibility.of(PlausibilityLevel.WORKING, ratio=bad_ratio)  # type: ignore[arg-type]


def test_plausibility_factories() -> None:
    assert Plausibility.tentative().level is PlausibilityLevel.TENTATIVE
    assert Plausibility.working().level is PlausibilityLevel.WORKING
    assert Plausibility.strong().level is PlausibilityLevel.STRONG
    assert Plausibility.suspended().is_suspended()


def test_plausibility_strengthen_and_weaken() -> None:
    measure = Plausibility.tentative()
    stronger = measure.strengthened()
    assert stronger.level is PlausibilityLevel.WORKING
    assert stronger.strengthened().level is PlausibilityLevel.STRONG
    assert stronger.weakened().level is PlausibilityLevel.TENTATIVE


def test_plausibility_strengthen_at_max_raises() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        Plausibility.strong().strengthened()
    assert exc.value.invariant == "Plausibility.strengthen.max"


def test_plausibility_weaken_at_min_raises() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        Plausibility.tentative().weakened()
    assert exc.value.invariant == "Plausibility.weaken.min"


def test_plausibility_suspended_cannot_strengthen_or_weaken() -> None:
    suspended = Plausibility.suspended()
    with pytest.raises(EducationalInvariantViolation):
        suspended.strengthened()
    with pytest.raises(EducationalInvariantViolation):
        suspended.weakened()


def test_plausibility_is_at_least() -> None:
    assert Plausibility.strong().is_at_least(PlausibilityLevel.WORKING)
    assert not Plausibility.tentative().is_at_least(PlausibilityLevel.WORKING)
    assert not Plausibility.suspended().is_at_least(PlausibilityLevel.TENTATIVE)


def test_plausibility_str() -> None:
    assert str(Plausibility.working()) == "working"
    assert "0.50" in str(Plausibility.working(ratio=0.5))


@pytest.mark.parametrize("level", list(ExplanatoryStrengthLevel))
def test_explanatory_strength_accepts_all_levels(
    level: ExplanatoryStrengthLevel,
) -> None:
    strength = ExplanatoryStrength.of(level)
    assert strength.level is level


def test_explanatory_strength_factories() -> None:
    assert ExplanatoryStrength.weak().is_weak()
    assert ExplanatoryStrength.moderate().is_moderate()
    assert ExplanatoryStrength.strong().is_strong()
    assert ExplanatoryStrength.compelling().is_compelling()


def test_explanatory_strength_ladder() -> None:
    weak = ExplanatoryStrength.weak()
    moderate = weak.strengthened()
    strong = moderate.strengthened()
    compelling = strong.strengthened()
    assert compelling.is_compelling()
    assert compelling.weakened().is_strong()


def test_explanatory_strength_bounds() -> None:
    with pytest.raises(EducationalInvariantViolation):
        ExplanatoryStrength.compelling().strengthened()
    with pytest.raises(EducationalInvariantViolation):
        ExplanatoryStrength.weak().weakened()


def test_explanatory_strength_at_least() -> None:
    assert ExplanatoryStrength.strong().at_least(ExplanatoryStrength.moderate())
    assert not ExplanatoryStrength.weak().at_least(ExplanatoryStrength.moderate())


def test_explanatory_strength_at_least_type_error() -> None:
    with pytest.raises(EducationalInvariantViolation):
        ExplanatoryStrength.moderate().at_least("strong")  # type: ignore[arg-type]


def test_value_objects_immutable() -> None:
    plausibility = Plausibility.working()
    strength = ExplanatoryStrength.moderate()
    with pytest.raises(AttributeError):
        plausibility.level = PlausibilityLevel.STRONG  # type: ignore[misc]
    with pytest.raises(AttributeError):
        strength.level = ExplanatoryStrengthLevel.STRONG  # type: ignore[misc]


def test_plausibility_rejects_non_enum_level() -> None:
    with pytest.raises(EducationalInvariantViolation):
        Plausibility(level="working")  # type: ignore[arg-type]


def test_explanatory_strength_rejects_non_enum_level() -> None:
    with pytest.raises(EducationalInvariantViolation):
        ExplanatoryStrength(level="moderate")  # type: ignore[arg-type]
