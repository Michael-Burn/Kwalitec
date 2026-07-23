"""Tests for Educational Evidence value objects and identities."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.educational_evidence import (
    CheckpointId,
    CompetencyId,
    EvidenceContext,
    EvidenceId,
    EvidenceMetadata,
    EvidenceSource,
    EvidenceSourceKind,
    EvidenceTimestamp,
    EvidenceWeight,
    EvidenceWeightBand,
    LearningContext,
    LearningEnvironment,
    LearningEnvironmentKind,
    MissionId,
    SubjectId,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId
from tests.domain.education.educational_evidence.conftest import make_environment


class TestIdentities:
    @pytest.mark.parametrize(
        "id_type",
        [EvidenceId, SubjectId, CompetencyId, MissionId, CheckpointId],
    )
    def test_strips_whitespace(self, id_type: type) -> None:
        assert id_type("  abc-1  ").value == "abc-1"

    @pytest.mark.parametrize(
        "id_type",
        [EvidenceId, SubjectId, CompetencyId, MissionId, CheckpointId],
    )
    def test_rejects_blank(self, id_type: type) -> None:
        with pytest.raises(EducationalInvariantViolation):
            id_type("   ")

    @pytest.mark.parametrize(
        "id_type",
        [EvidenceId, SubjectId, CompetencyId, MissionId, CheckpointId],
    )
    def test_rejects_internal_whitespace(self, id_type: type) -> None:
        with pytest.raises(EducationalInvariantViolation):
            id_type("abc 1")

    @pytest.mark.parametrize(
        "id_type",
        [EvidenceId, SubjectId, CompetencyId, MissionId, CheckpointId],
    )
    def test_str_returns_value(self, id_type: type) -> None:
        assert str(id_type("abc-1")) == "abc-1"

    def test_equality_is_structural_and_type_scoped(self) -> None:
        assert SubjectId("s1") == SubjectId("s1")
        assert SubjectId("s1") != SubjectId("s2")
        # Distinct bounded-context identity classes never compare equal even
        # with an identical string value.
        assert CompetencyId("s1") != SubjectId("s1")


class TestEvidenceSource:
    def test_student_action_factory(self) -> None:
        source = EvidenceSource.student_action("mission_engine")
        assert source.kind is EvidenceSourceKind.STUDENT_ACTION
        assert source.is_student_action()
        assert not source.is_self_report()
        assert not source.is_system_observation()

    def test_system_observation_factory(self) -> None:
        source = EvidenceSource.system_observation("scheduler")
        assert source.kind is EvidenceSourceKind.SYSTEM_OBSERVATION
        assert source.is_system_observation()

    def test_self_report_factory(self) -> None:
        source = EvidenceSource.self_report("confidence_widget")
        assert source.kind is EvidenceSourceKind.SELF_REPORT
        assert source.is_self_report()

    def test_rejects_wrong_kind_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceSource(kind="student_action", origin="x")  # type: ignore[arg-type]

    def test_rejects_blank_origin(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceSource.student_action("   ")

    def test_str_representation(self) -> None:
        source = EvidenceSource.student_action("mission_engine")
        assert str(source) == "student_action:mission_engine"


class TestEvidenceWeight:
    @pytest.mark.parametrize(
        "magnitude,band",
        [
            (0.0, EvidenceWeightBand.NEGLIGIBLE),
            (0.049, EvidenceWeightBand.NEGLIGIBLE),
            (0.05, EvidenceWeightBand.LOW),
            (0.29, EvidenceWeightBand.LOW),
            (0.30, EvidenceWeightBand.MODERATE),
            (0.59, EvidenceWeightBand.MODERATE),
            (0.60, EvidenceWeightBand.HIGH),
            (0.84, EvidenceWeightBand.HIGH),
            (0.85, EvidenceWeightBand.DECISIVE),
            (1.0, EvidenceWeightBand.DECISIVE),
        ],
    )
    def test_band_is_derived_deterministically(
        self, magnitude: float, band: EvidenceWeightBand
    ) -> None:
        assert EvidenceWeight.of(magnitude).band is band

    def test_rejects_out_of_range_low(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceWeight.of(-0.01)

    def test_rejects_out_of_range_high(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceWeight.of(1.01)

    def test_rejects_bool(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceWeight(magnitude=True)  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceWeight(magnitude="0.5")  # type: ignore[arg-type]

    def test_magnitude_is_rounded(self) -> None:
        assert EvidenceWeight.of(0.123456789).magnitude == 0.1235

    def test_is_at_least(self) -> None:
        assert EvidenceWeight.of(0.5).is_at_least(EvidenceWeight.of(0.4))
        assert not EvidenceWeight.of(0.3).is_at_least(EvidenceWeight.of(0.4))

    def test_is_at_least_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceWeight.of(0.5).is_at_least(0.4)  # type: ignore[arg-type]

    def test_str_representation(self) -> None:
        assert str(EvidenceWeight.of(0.5)) == "0.5000:moderate"


class TestLearningEnvironment:
    def test_construction(self) -> None:
        env = LearningEnvironment.of(LearningEnvironmentKind.STUDY_SESSION)
        assert env.kind is LearningEnvironmentKind.STUDY_SESSION
        assert env.label is None

    def test_rejects_wrong_kind_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningEnvironment(kind="mission")  # type: ignore[arg-type]

    def test_label_is_stripped(self) -> None:
        env = LearningEnvironment.of(
            LearningEnvironmentKind.MISSION, label="  Daily Mission  "
        )
        assert env.label == "Daily Mission"

    def test_str_representation(self) -> None:
        assert str(make_environment()) == "mission"


class TestLearningContext:
    def test_empty_context(self) -> None:
        context = LearningContext.empty()
        assert context.is_empty()

    def test_not_empty_when_any_field_set(self) -> None:
        context = LearningContext(subject_id=SubjectId("math"))
        assert not context.is_empty()

    def test_rejects_wrong_subject_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningContext(subject_id="math")  # type: ignore[arg-type]

    def test_rejects_wrong_competency_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningContext(competency_id="algebra")  # type: ignore[arg-type]

    def test_rejects_wrong_mission_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningContext(mission_id="mission-1")  # type: ignore[arg-type]

    def test_rejects_wrong_checkpoint_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningContext(checkpoint_id="checkpoint-1")  # type: ignore[arg-type]

    def test_rejects_wrong_learning_episode_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningContext(learning_episode_id="episode-1")  # type: ignore[arg-type]

    def test_accepts_all_fields_populated(self) -> None:
        context = LearningContext(
            subject_id=SubjectId("math"),
            competency_id=CompetencyId("algebra"),
            mission_id=MissionId("mission-1"),
            checkpoint_id=CheckpointId("checkpoint-1"),
            learning_episode_id=LearningEpisodeId("episode-1"),
        )
        assert not context.is_empty()


class TestEvidenceContext:
    def test_of_factory_defaults_to_empty_learning_context(self) -> None:
        context = EvidenceContext.of(make_environment())
        assert context.learning_context.is_empty()

    def test_has_helpers(self) -> None:
        context = EvidenceContext(
            learning_context=LearningContext(
                subject_id=SubjectId("math"),
                competency_id=CompetencyId("algebra"),
                mission_id=MissionId("mission-1"),
                checkpoint_id=CheckpointId("checkpoint-1"),
                learning_episode_id=LearningEpisodeId("episode-1"),
            ),
            learning_environment=make_environment(),
        )
        assert context.has_subject()
        assert context.has_competency()
        assert context.has_mission()
        assert context.has_checkpoint()
        assert context.has_learning_episode()

    def test_has_helpers_false_when_absent(self) -> None:
        context = EvidenceContext.of(make_environment())
        assert not context.has_subject()
        assert not context.has_competency()
        assert not context.has_mission()
        assert not context.has_checkpoint()
        assert not context.has_learning_episode()

    def test_rejects_wrong_learning_context_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceContext(
                learning_context="not-a-context",  # type: ignore[arg-type]
                learning_environment=make_environment(),
            )

    def test_rejects_wrong_learning_environment_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceContext(
                learning_context=LearningContext.empty(),
                learning_environment="mission",  # type: ignore[arg-type]
            )


class TestEvidenceMetadata:
    def test_empty_metadata(self) -> None:
        metadata = EvidenceMetadata.empty()
        assert metadata.is_empty()
        assert len(metadata) == 0

    def test_of_factory_sorts_entries(self) -> None:
        metadata = EvidenceMetadata.of(zebra=1, alpha=2)
        assert metadata.entries == (("alpha", 2), ("zebra", 1))

    def test_get_and_has(self) -> None:
        metadata = EvidenceMetadata.of(is_correct=True)
        assert metadata.has("is_correct")
        assert metadata.get("is_correct") is True
        assert metadata.get("missing") is None
        assert metadata.get("missing", "default") == "default"

    def test_as_dict(self) -> None:
        metadata = EvidenceMetadata.of(a=1, b="two")
        assert metadata.as_dict() == {"a": 1, "b": "two"}

    def test_with_entry_adds_new_key(self) -> None:
        metadata = EvidenceMetadata.of(a=1).with_entry("b", 2)
        assert metadata.as_dict() == {"a": 1, "b": 2}

    def test_with_entry_overwrites_existing_key(self) -> None:
        metadata = EvidenceMetadata.of(a=1).with_entry("a", 2)
        assert metadata.as_dict() == {"a": 2}

    def test_rejects_blank_key(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceMetadata(entries=(("   ", 1),))

    def test_rejects_non_string_key(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceMetadata(entries=((1, "x"),))  # type: ignore[arg-type]

    def test_rejects_duplicate_key(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceMetadata(entries=(("a", 1), ("a", 2)))

    def test_rejects_non_primitive_value(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceMetadata(entries=(("a", [1, 2]),))  # type: ignore[arg-type]

    def test_accepts_none_value(self) -> None:
        metadata = EvidenceMetadata.of(a=None)
        assert metadata.get("a") is None
        assert metadata.has("a")

    def test_equality_ignores_construction_order(self) -> None:
        assert EvidenceMetadata.of(a=1, b=2) == EvidenceMetadata.of(b=2, a=1)


class TestEvidenceTimestamp:
    def test_of_factory(self) -> None:
        occurred_at = datetime(2026, 7, 21, tzinfo=UTC)
        assert EvidenceTimestamp.of(occurred_at).occurred_at == occurred_at

    def test_rejects_naive_datetime(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceTimestamp(occurred_at=datetime(2026, 7, 21))

    def test_rejects_non_datetime(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceTimestamp(occurred_at="2026-07-21")  # type: ignore[arg-type]

    def test_is_before_and_is_after(self) -> None:
        earlier = EvidenceTimestamp.of(datetime(2026, 1, 1, tzinfo=UTC))
        later = EvidenceTimestamp.of(datetime(2026, 2, 1, tzinfo=UTC))
        assert earlier.is_before(later)
        assert later.is_after(earlier)
        assert not later.is_before(earlier)
        assert not earlier.is_after(later)

    def test_is_before_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceTimestamp.of(datetime(2026, 1, 1, tzinfo=UTC)).is_before(
                datetime(2026, 1, 2, tzinfo=UTC)  # type: ignore[arg-type]
            )

    def test_is_after_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceTimestamp.of(datetime(2026, 1, 1, tzinfo=UTC)).is_after(
                datetime(2026, 1, 2, tzinfo=UTC)  # type: ignore[arg-type]
            )

    def test_str_representation(self) -> None:
        occurred_at = datetime(2026, 7, 21, 12, 0, tzinfo=UTC)
        assert str(EvidenceTimestamp.of(occurred_at)) == occurred_at.isoformat()
