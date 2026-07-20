"""Value object tests for Learning Episode."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.learning_episode import (
    DurationBand,
    EpisodeDuration,
    EpisodeProgress,
    EpisodeSequence,
    EpisodeStepId,
    EpisodeStepKind,
)


class TestEpisodeStepKind:
    def test_custom_kind_allowed(self) -> None:
        kind = EpisodeStepKind.custom("socratic_probe")
        assert kind.value == "socratic_probe"

    @pytest.mark.parametrize(
        "factory",
        [
            EpisodeStepKind.explanation,
            EpisodeStepKind.worked_example,
            EpisodeStepKind.guided_practice,
            EpisodeStepKind.independent_practice,
            EpisodeStepKind.reflection,
        ],
    )
    def test_well_known_factories(self, factory) -> None:
        kind = factory()
        assert isinstance(kind, EpisodeStepKind)
        assert kind.value

    def test_blank_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeStepKind("  ")

    def test_equality(self) -> None:
        assert EpisodeStepKind.explanation() == EpisodeStepKind("explanation")

    def test_str(self) -> None:
        assert str(EpisodeStepKind.worked_example()) == "worked_example"

    def test_frozen(self) -> None:
        kind = EpisodeStepKind.explanation()
        with pytest.raises(Exception):
            kind.value = "other"  # type: ignore[misc]


class TestEpisodeStepId:
    def test_valid(self) -> None:
        assert EpisodeStepId("step-1").value == "step-1"

    def test_whitespace_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeStepId("step 1")

    def test_blank_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeStepId("")


class TestEpisodeSequence:
    def test_valid_sequence(self) -> None:
        a, b = EpisodeStepId("a"), EpisodeStepId("b")
        seq = EpisodeSequence(step_ids=(a, b), required_step_ids=(a,))
        assert seq.length == 2
        assert seq.is_required(a)
        assert not seq.is_required(b)
        assert seq.index_of(b) == 1
        assert seq.next_after(a) == b
        assert seq.next_after(b) is None

    def test_empty_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeSequence(step_ids=(), required_step_ids=())

    def test_duplicate_ids_rejected(self) -> None:
        a = EpisodeStepId("a")
        with pytest.raises(EducationalInvariantViolation):
            EpisodeSequence(step_ids=(a, a), required_step_ids=(a,))

    def test_required_must_belong(self) -> None:
        a, b = EpisodeStepId("a"), EpisodeStepId("b")
        with pytest.raises(EducationalInvariantViolation):
            EpisodeSequence(step_ids=(a,), required_step_ids=(b,))

    def test_no_required_rejected(self) -> None:
        a = EpisodeStepId("a")
        with pytest.raises(EducationalInvariantViolation):
            EpisodeSequence(step_ids=(a,), required_step_ids=())

    def test_index_of_missing(self) -> None:
        a, b = EpisodeStepId("a"), EpisodeStepId("b")
        seq = EpisodeSequence(step_ids=(a,), required_step_ids=(a,))
        with pytest.raises(EducationalInvariantViolation):
            seq.index_of(b)

    def test_duplicate_required_rejected(self) -> None:
        a = EpisodeStepId("a")
        with pytest.raises(EducationalInvariantViolation):
            EpisodeSequence(step_ids=(a,), required_step_ids=(a, a))


class TestEpisodeDuration:
    def test_minutes_only(self) -> None:
        d = EpisodeDuration(planned_minutes=10)
        assert d.is_short()

    def test_band_only(self) -> None:
        d = EpisodeDuration(band=DurationBand.LONG)
        assert not d.is_short()

    def test_short_band(self) -> None:
        assert EpisodeDuration(band=DurationBand.SHORT).is_short()

    def test_empty_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeDuration()

    def test_non_positive_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeDuration(planned_minutes=0)

    def test_negative_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeDuration(planned_minutes=-5)

    @pytest.mark.parametrize("minutes", [1, 5, 15, 16, 35, 60, 90])
    def test_various_minutes(self, minutes: int) -> None:
        d = EpisodeDuration(planned_minutes=minutes)
        assert d.planned_minutes == minutes
        assert d.is_short() == (minutes <= 15)

    @pytest.mark.parametrize("band", list(DurationBand))
    def test_all_bands(self, band: DurationBand) -> None:
        d = EpisodeDuration(band=band)
        assert d.band is band


class TestEpisodeProgress:
    def test_valid(self) -> None:
        p = EpisodeProgress(
            current_index=1,
            completed_steps=1,
            total_steps=3,
            completed_required_steps=1,
            total_required_steps=2,
        )
        assert not p.required_sequence_complete
        assert not p.all_steps_complete
        assert p.ratio == pytest.approx(1 / 3)

    def test_required_complete(self) -> None:
        p = EpisodeProgress(
            current_index=2,
            completed_steps=2,
            total_steps=2,
            completed_required_steps=2,
            total_required_steps=2,
        )
        assert p.required_sequence_complete
        assert p.all_steps_complete
        assert p.ratio == 1.0

    def test_zero_total_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeProgress(
                current_index=0,
                completed_steps=0,
                total_steps=0,
                completed_required_steps=0,
                total_required_steps=0,
            )

    def test_completed_exceeds_total(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeProgress(
                current_index=0,
                completed_steps=3,
                total_steps=2,
                completed_required_steps=0,
                total_required_steps=1,
            )

    def test_negative_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeProgress(
                current_index=-1,
                completed_steps=0,
                total_steps=1,
                completed_required_steps=0,
                total_required_steps=1,
            )

    def test_required_completed_exceeds(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeProgress(
                current_index=0,
                completed_steps=0,
                total_steps=2,
                completed_required_steps=2,
                total_required_steps=1,
            )

    def test_current_index_bounds(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeProgress(
                current_index=5,
                completed_steps=0,
                total_steps=2,
                completed_required_steps=0,
                total_required_steps=1,
            )
