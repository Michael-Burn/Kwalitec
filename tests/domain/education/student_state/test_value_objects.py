"""Value object construction, immutability, and invariant tests."""

from __future__ import annotations

import dataclasses

import pytest

from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.student_state import (
    CheckpointId,
    CheckpointReference,
    CompetencyId,
    CompetencyState,
    ConfidenceSummary,
    EducationalHealth,
    EducationalHealthBand,
    EducationalTimelineId,
    EducationalTimelineReference,
    MasteryBand,
    MasterySummary,
    MissionId,
    MissionReference,
    SubjectId,
    SubjectState,
    SubjectStatus,
)
from tests.domain.education.student_state.conftest import (
    make_competency_state,
    make_confidence_summary,
    make_educational_health,
    make_mastery_summary,
    make_subject_state,
)


class TestIdentityStrRepresentations:
    def test_all_ids_stringify_to_their_value(self) -> None:
        from domain.education.student_state import (
            CheckpointId,
            CompetencyId,
            EducationalTimelineId,
            MissionId,
            StudentEducationalStateId,
            SubjectId,
        )

        assert str(StudentEducationalStateId("s1")) == "s1"
        assert str(SubjectId("subject-1")) == "subject-1"
        assert str(CompetencyId("competency-1")) == "competency-1"
        assert str(MissionId("mission-1")) == "mission-1"
        assert str(CheckpointId("checkpoint-1")) == "checkpoint-1"
        assert str(EducationalTimelineId("timeline-1")) == "timeline-1"


class TestSubjectState:
    def test_construction(self) -> None:
        state = make_subject_state()
        assert state.subject_id == SubjectId("subject-math")
        assert state.status is SubjectStatus.ACTIVE
        assert state.coverage_ratio == 0.4

    def test_immutable(self) -> None:
        state = make_subject_state()
        with pytest.raises(dataclasses.FrozenInstanceError):
            state.status = SubjectStatus.COMPLETED  # type: ignore[misc]

    def test_rejects_wrong_subject_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            SubjectState(subject_id="not-an-id", status=SubjectStatus.ACTIVE)  # type: ignore[arg-type]

    def test_rejects_wrong_status_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            SubjectState(subject_id=SubjectId("s1"), status="active")  # type: ignore[arg-type]

    @pytest.mark.parametrize("ratio", [-0.01, 1.01])
    def test_rejects_out_of_range_coverage_ratio(self, ratio: float) -> None:
        with pytest.raises(EducationalInvariantViolation):
            SubjectState(
                subject_id=SubjectId("s1"),
                status=SubjectStatus.ACTIVE,
                coverage_ratio=ratio,
            )

    def test_rejects_non_numeric_coverage_ratio(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            SubjectState(
                subject_id=SubjectId("s1"),
                status=SubjectStatus.ACTIVE,
                coverage_ratio="high",  # type: ignore[arg-type]
            )

    def test_rejects_bool_coverage_ratio(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            SubjectState(
                subject_id=SubjectId("s1"),
                status=SubjectStatus.ACTIVE,
                coverage_ratio=True,  # type: ignore[arg-type]
            )

    def test_rejects_blank_label(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            SubjectState(
                subject_id=SubjectId("s1"), status=SubjectStatus.ACTIVE, label="  "
            )

    def test_with_status_returns_new_instance(self) -> None:
        state = make_subject_state(status=SubjectStatus.ACTIVE)
        updated = state.with_status(SubjectStatus.COMPLETED)
        assert updated.status is SubjectStatus.COMPLETED
        assert state.status is SubjectStatus.ACTIVE
        assert updated.subject_id == state.subject_id

    def test_with_coverage_ratio_returns_new_instance(self) -> None:
        state = make_subject_state(coverage_ratio=0.1)
        updated = state.with_coverage_ratio(0.9)
        assert updated.coverage_ratio == 0.9
        assert state.coverage_ratio == 0.1

    def test_structural_equality(self) -> None:
        a = make_subject_state()
        b = make_subject_state()
        assert a == b

    def test_str(self) -> None:
        state = make_subject_state()
        assert str(state) == "subject-math:active"


class TestCompetencyState:
    def test_construction(self) -> None:
        state = make_competency_state()
        assert state.competency_id == CompetencyId("competency-algebra")
        assert state.subject_id == SubjectId("subject-math")
        assert state.band is MasteryBand.DEVELOPING
        assert state.mastery_ratio == 0.5

    def test_immutable(self) -> None:
        state = make_competency_state()
        with pytest.raises(dataclasses.FrozenInstanceError):
            state.band = MasteryBand.MASTERED  # type: ignore[misc]

    def test_rejects_wrong_competency_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CompetencyState(
                competency_id="not-an-id",  # type: ignore[arg-type]
                subject_id=SubjectId("s1"),
                band=MasteryBand.DEVELOPING,
            )

    def test_rejects_wrong_subject_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CompetencyState(
                competency_id=CompetencyId("c1"),
                subject_id="not-an-id",  # type: ignore[arg-type]
                band=MasteryBand.DEVELOPING,
            )

    def test_rejects_wrong_band_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CompetencyState(
                competency_id=CompetencyId("c1"),
                subject_id=SubjectId("s1"),
                band="developing",  # type: ignore[arg-type]
            )

    @pytest.mark.parametrize("ratio", [-1.0, 1.5])
    def test_rejects_out_of_range_mastery_ratio(self, ratio: float) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CompetencyState(
                competency_id=CompetencyId("c1"),
                subject_id=SubjectId("s1"),
                band=MasteryBand.DEVELOPING,
                mastery_ratio=ratio,
            )

    def test_with_band_returns_new_instance(self) -> None:
        state = make_competency_state(band=MasteryBand.DEVELOPING)
        updated = state.with_band(MasteryBand.MASTERED)
        assert updated.band is MasteryBand.MASTERED
        assert state.band is MasteryBand.DEVELOPING

    def test_with_mastery_ratio_returns_new_instance(self) -> None:
        state = make_competency_state(mastery_ratio=0.2)
        updated = state.with_mastery_ratio(0.9)
        assert updated.mastery_ratio == 0.9
        assert state.mastery_ratio == 0.2

    def test_rejects_non_numeric_mastery_ratio(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CompetencyState(
                competency_id=CompetencyId("c1"),
                subject_id=SubjectId("s1"),
                band=MasteryBand.DEVELOPING,
                mastery_ratio="high",  # type: ignore[arg-type]
            )

    def test_accepts_optional_label(self) -> None:
        state = CompetencyState(
            competency_id=CompetencyId("c1"),
            subject_id=SubjectId("s1"),
            band=MasteryBand.DEVELOPING,
            label="Algebra basics",
        )
        assert state.label == "Algebra basics"

    def test_rejects_blank_label(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CompetencyState(
                competency_id=CompetencyId("c1"),
                subject_id=SubjectId("s1"),
                band=MasteryBand.DEVELOPING,
                label="   ",
            )

    def test_str(self) -> None:
        state = make_competency_state()
        assert str(state) == "competency-algebra:developing"


class TestMasterySummary:
    def test_construction(self) -> None:
        summary = make_mastery_summary()
        assert summary.overall_band is MasteryBand.DEVELOPING
        assert summary.overall_ratio == 0.5

    def test_unknown_factory(self) -> None:
        summary = MasterySummary.unknown()
        assert summary.overall_band is MasteryBand.UNKNOWN
        assert summary.overall_ratio is None
        assert summary.total_count() == 0

    def test_rejects_wrong_band_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasterySummary(overall_band="developing")  # type: ignore[arg-type]

    @pytest.mark.parametrize("ratio", [-0.5, 1.2])
    def test_rejects_out_of_range_ratio(self, ratio: float) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasterySummary(overall_band=MasteryBand.DEVELOPING, overall_ratio=ratio)

    def test_rejects_non_numeric_ratio(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasterySummary(overall_band=MasteryBand.DEVELOPING, overall_ratio="high")  # type: ignore[arg-type]

    def test_rejects_bool_ratio(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasterySummary(overall_band=MasteryBand.DEVELOPING, overall_ratio=True)  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "field_name",
        ["mastered_count", "secure_count", "developing_count", "not_started_count"],
    )
    def test_rejects_negative_counts(self, field_name: str) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasterySummary(overall_band=MasteryBand.UNKNOWN, **{field_name: -1})

    def test_rejects_non_int_counts(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasterySummary(overall_band=MasteryBand.UNKNOWN, mastered_count=1.5)  # type: ignore[arg-type]

    def test_total_count(self) -> None:
        summary = MasterySummary(
            overall_band=MasteryBand.DEVELOPING,
            mastered_count=2,
            secure_count=3,
            developing_count=1,
            not_started_count=4,
        )
        assert summary.total_count() == 10


class TestConfidenceSummary:
    def test_construction(self) -> None:
        summary = make_confidence_summary()
        assert summary.overall is ConfidenceLevel.MEDIUM
        assert summary.overall_ratio == 0.6

    def test_unknown_factory(self) -> None:
        summary = ConfidenceSummary.unknown()
        assert summary.overall is ConfidenceLevel.UNKNOWN

    def test_rejects_wrong_overall_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConfidenceSummary(overall="medium")  # type: ignore[arg-type]

    def test_rejects_non_numeric_overall_ratio(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConfidenceSummary(overall=ConfidenceLevel.MEDIUM, overall_ratio="high")  # type: ignore[arg-type]

    @pytest.mark.parametrize("ratio", [-0.1, 1.1])
    def test_rejects_out_of_range_overall_ratio(self, ratio: float) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConfidenceSummary(overall=ConfidenceLevel.MEDIUM, overall_ratio=ratio)

    def test_rejects_negative_subjects_considered(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConfidenceSummary(overall=ConfidenceLevel.MEDIUM, subjects_considered=-1)

    def test_rejects_non_int_subjects_considered(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConfidenceSummary(
                overall=ConfidenceLevel.MEDIUM,
                subjects_considered=1.5,  # type: ignore[arg-type]
            )

    def test_rejects_bool_subjects_considered(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConfidenceSummary(
                overall=ConfidenceLevel.MEDIUM,
                subjects_considered=True,  # type: ignore[arg-type]
            )

    def test_rejects_wrong_lowest_confidence_subject_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConfidenceSummary(
                overall=ConfidenceLevel.MEDIUM,
                lowest_confidence_subject_id="not-an-id",  # type: ignore[arg-type]
            )

    def test_accepts_valid_lowest_confidence_subject(self) -> None:
        summary = ConfidenceSummary(
            overall=ConfidenceLevel.LOW,
            lowest_confidence_subject_id=SubjectId("subject-physics"),
        )
        assert summary.lowest_confidence_subject_id == SubjectId("subject-physics")


class TestEducationalHealth:
    def test_construction(self) -> None:
        health = make_educational_health(reasons=("overdue_review",))
        assert health.band is EducationalHealthBand.STABLE
        assert health.reasons == ("overdue_review",)

    def test_unknown_factory(self) -> None:
        health = EducationalHealth.unknown()
        assert health.band is EducationalHealthBand.UNKNOWN
        assert health.reasons == ()

    def test_rejects_wrong_band_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalHealth(band="stable")  # type: ignore[arg-type]

    def test_rejects_non_numeric_ratio(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalHealth(band=EducationalHealthBand.STABLE, ratio="high")  # type: ignore[arg-type]

    @pytest.mark.parametrize("ratio", [-0.1, 1.1])
    def test_rejects_out_of_range_ratio(self, ratio: float) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalHealth(band=EducationalHealthBand.STABLE, ratio=ratio)

    def test_rejects_wrong_reasons_container_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalHealth(band=EducationalHealthBand.STABLE, reasons="not-a-tuple")  # type: ignore[arg-type]

    def test_rejects_blank_reason(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalHealth(band=EducationalHealthBand.STABLE, reasons=("  ",))

    def test_normalizes_list_reasons_to_tuple(self) -> None:
        health = EducationalHealth(
            band=EducationalHealthBand.AT_RISK, reasons=["a", "b"]
        )
        assert health.reasons == ("a", "b")


class TestStateReferences:
    def test_mission_reference_construction(self) -> None:
        ref = MissionReference(mission_id=MissionId("mission-001"))
        assert ref.mission_id.value == "mission-001"

    def test_mission_reference_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MissionReference(mission_id="mission-001")  # type: ignore[arg-type]

    def test_checkpoint_reference_construction(self) -> None:
        ref = CheckpointReference(checkpoint_id=CheckpointId("checkpoint-001"))
        assert ref.checkpoint_id.value == "checkpoint-001"

    def test_checkpoint_reference_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CheckpointReference(checkpoint_id="checkpoint-001")  # type: ignore[arg-type]

    def test_checkpoint_reference_accepts_label(self) -> None:
        ref = CheckpointReference(
            checkpoint_id=CheckpointId("checkpoint-001"), label="Week 3 checkpoint"
        )
        assert ref.label == "Week 3 checkpoint"

    def test_timeline_reference_construction(self) -> None:
        ref = EducationalTimelineReference(
            timeline_id=EducationalTimelineId("timeline-001")
        )
        assert ref.timeline_id.value == "timeline-001"

    def test_timeline_reference_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EducationalTimelineReference(timeline_id="timeline-001")  # type: ignore[arg-type]

    def test_timeline_reference_accepts_label(self) -> None:
        ref = EducationalTimelineReference(
            timeline_id=EducationalTimelineId("timeline-001"), label="Sitting 2026"
        )
        assert ref.label == "Sitting 2026"

    def test_references_reject_blank_label(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MissionReference(mission_id=MissionId("m1"), label="   ")
