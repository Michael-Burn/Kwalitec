"""Unit tests for Educational Priority value objects."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority import (
    InstructionalImpact,
    InstructionalImpactLevel,
    PriorityScore,
    PriorityScoreBand,
    Urgency,
    UrgencyLevel,
)


@pytest.mark.parametrize("band", list(PriorityScoreBand))
def test_priority_score_accepts_all_bands(band: PriorityScoreBand) -> None:
    score = PriorityScore.of(band, ratio=0.5)
    assert score.band is band
    assert score.is_at_least(PriorityScoreBand.NEGLIGIBLE)


def test_priority_score_rejects_invalid_ratio() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityScore.of(PriorityScoreBand.MEDIUM, ratio=1.5)
    with pytest.raises(EducationalInvariantViolation):
        PriorityScore.of(PriorityScoreBand.MEDIUM, ratio=-0.1)


def test_priority_score_rejects_blank_rationale() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityScore.of(PriorityScoreBand.HIGH, rationale="   ")


def test_priority_score_promote_and_demote() -> None:
    score = PriorityScore.of(PriorityScoreBand.MEDIUM)
    promoted = score.promoted()
    assert promoted.band is PriorityScoreBand.HIGH
    demoted = promoted.demoted()
    assert demoted.band is PriorityScoreBand.MEDIUM


def test_priority_score_promote_at_max_fails() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityScore.of(PriorityScoreBand.CRITICAL).promoted()


def test_priority_score_demote_at_min_fails() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityScore.of(PriorityScoreBand.NEGLIGIBLE).demoted()


def test_priority_score_immutable() -> None:
    score = PriorityScore.of(PriorityScoreBand.LOW)
    with pytest.raises(AttributeError):
        score.band = PriorityScoreBand.HIGH  # type: ignore[misc]


def test_priority_score_str() -> None:
    assert "medium" in str(PriorityScore.of(PriorityScoreBand.MEDIUM))
    assert "0.40" in str(PriorityScore.of(PriorityScoreBand.MEDIUM, ratio=0.4))


@pytest.mark.parametrize("level", list(UrgencyLevel))
def test_urgency_accepts_all_levels(level: UrgencyLevel) -> None:
    urgency = Urgency.of(level)
    assert urgency.level is level


def test_urgency_elevate_and_defer() -> None:
    urgency = Urgency.of(UrgencyLevel.ROUTINE)
    assert urgency.elevated().level is UrgencyLevel.ELEVATED
    assert urgency.elevated().deferred().level is UrgencyLevel.ROUTINE


def test_urgency_elevate_at_max_fails() -> None:
    with pytest.raises(EducationalInvariantViolation):
        Urgency.of(UrgencyLevel.CRITICAL).elevated()


def test_urgency_defer_at_min_fails() -> None:
    with pytest.raises(EducationalInvariantViolation):
        Urgency.of(UrgencyLevel.DEFERRED).deferred()


def test_urgency_rejects_blank_rationale() -> None:
    with pytest.raises(EducationalInvariantViolation):
        Urgency.of(UrgencyLevel.IMMEDIATE, rationale="")


def test_urgency_is_at_least() -> None:
    urgency = Urgency.of(UrgencyLevel.IMMEDIATE)
    assert urgency.is_at_least(UrgencyLevel.ELEVATED)
    assert not urgency.is_at_least(UrgencyLevel.CRITICAL)


@pytest.mark.parametrize("level", list(InstructionalImpactLevel))
def test_instructional_impact_accepts_all_levels(
    level: InstructionalImpactLevel,
) -> None:
    impact = InstructionalImpact.of(level, "Addresses blocking educational need")
    assert impact.level is level
    assert "blocking" in impact.statement


def test_instructional_impact_requires_statement() -> None:
    with pytest.raises(EducationalInvariantViolation):
        InstructionalImpact.of(InstructionalImpactLevel.MATERIAL, "  ")


def test_instructional_impact_is_at_least() -> None:
    impact = InstructionalImpact.of(
        InstructionalImpactLevel.SUBSTANTIAL, "Unlocks progress"
    )
    assert impact.is_at_least(InstructionalImpactLevel.MATERIAL)
    assert not impact.is_at_least(InstructionalImpactLevel.TRANSFORMATIONAL)


def test_severity_is_not_a_priority_score_band() -> None:
    # Explicit distinction: priority bands are instructional ordering labels.
    bands = {band.value for band in PriorityScoreBand}
    assert "mild" not in bands
    assert "severe" not in bands
    assert "critical" in bands
