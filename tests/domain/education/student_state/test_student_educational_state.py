"""Construction, behaviour, and snapshot tests for StudentEducationalState."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId
from domain.education.student_state import (
    CheckpointId,
    CompetencyId,
    EducationalHealthBand,
    MasteryBand,
    MissionId,
    StudentEducationalState,
    StudentEducationalStateId,
    SubjectId,
    SubjectStatus,
)
from tests.domain.education.student_state.conftest import (
    make_checkpoint_reference,
    make_competency_state,
    make_confidence_summary,
    make_educational_health,
    make_episode_id,
    make_mastery_summary,
    make_mission_reference,
    make_state,
    make_subject_state,
    make_timeline_reference,
)


class TestConstruction:
    def test_create_factory_defaults(self) -> None:
        state = make_state()
        assert state.student_id == "student-ada"
        assert state.subject_states == ()
        assert state.competency_states == ()
        assert state.mastery_summary.overall_band is MasteryBand.UNKNOWN
        assert state.confidence_summary is not None
        assert state.educational_health.band is EducationalHealthBand.UNKNOWN
        assert state.active_learning_episode_id is None
        assert state.current_mission is None
        assert state.current_checkpoint is None
        assert state.educational_timeline is None
        assert state.last_updated_at is None

    def test_create_with_last_updated_at(self) -> None:
        as_of = datetime(2026, 1, 1, tzinfo=UTC)
        state = StudentEducationalState.create(
            StudentEducationalStateId("s1"), "student-1", last_updated_at=as_of
        )
        assert state.last_updated_at == as_of

    def test_construct_with_full_state(self) -> None:
        state = StudentEducationalState(
            state_id=StudentEducationalStateId("s1"),
            student_id="student-1",
            subject_states=[make_subject_state()],
            competency_states=[make_competency_state()],
            mastery_summary=make_mastery_summary(),
            confidence_summary=make_confidence_summary(),
            educational_health=make_educational_health(),
            active_learning_episode_id=make_episode_id(),
            current_mission=make_mission_reference(),
            current_checkpoint=make_checkpoint_reference(),
            educational_timeline=make_timeline_reference(),
        )
        assert state.subject_count() == 1
        assert state.competency_count() == 1
        assert state.has_active_learning_episode()
        assert state.has_current_mission()
        assert state.has_current_checkpoint()
        assert state.has_educational_timeline()


class TestIdentityInvariant:
    def test_student_id_is_mandatory(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StudentEducationalState(
                state_id=StudentEducationalStateId("s1"), student_id=""
            )

    def test_student_id_none_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StudentEducationalState(
                state_id=StudentEducationalStateId("s1"),
                student_id=None,  # type: ignore[arg-type]
            )

    def test_state_id_type_required(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StudentEducationalState(state_id="not-an-id", student_id="student-1")  # type: ignore[arg-type]


class TestDuplicatePrevention:
    def test_duplicate_subject_states_rejected_at_construction(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StudentEducationalState(
                state_id=StudentEducationalStateId("s1"),
                student_id="student-1",
                subject_states=[
                    make_subject_state(subject_id="math"),
                    make_subject_state(subject_id="math"),
                ],
            )

    def test_duplicate_competency_states_rejected_at_construction(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            StudentEducationalState(
                state_id=StudentEducationalStateId("s1"),
                student_id="student-1",
                competency_states=[
                    make_competency_state(competency_id="algebra"),
                    make_competency_state(competency_id="algebra"),
                ],
            )

    def test_update_subject_state_replaces_not_duplicates(self) -> None:
        state = make_state()
        state.update_subject_state(
            make_subject_state(subject_id="math", status=SubjectStatus.ACTIVE)
        )
        state.update_subject_state(
            make_subject_state(subject_id="math", status=SubjectStatus.COMPLETED)
        )
        assert state.subject_count() == 1
        assert state.subject_state_for("math").status is SubjectStatus.COMPLETED

    def test_update_competency_replaces_not_duplicates(self) -> None:
        state = make_state()
        state.update_competency(
            make_competency_state(competency_id="algebra", band=MasteryBand.DEVELOPING)
        )
        state.update_competency(
            make_competency_state(competency_id="algebra", band=MasteryBand.MASTERED)
        )
        assert state.competency_count() == 1
        assert state.competency_state_for("algebra").band is MasteryBand.MASTERED


class TestSubjectAndCompetencyUpdates:
    def test_update_subject_state_adds_new_subject(self) -> None:
        state = make_state()
        state.update_subject_state(make_subject_state(subject_id="math"))
        state.update_subject_state(make_subject_state(subject_id="physics"))
        assert state.subject_count() == 2
        assert state.has_subject(SubjectId("math"))
        assert state.has_subject("physics")
        assert not state.has_subject("chemistry")

    def test_update_subject_state_preserves_other_subjects(self) -> None:
        state = make_state()
        state.update_subject_state(
            make_subject_state(subject_id="math", status=SubjectStatus.ACTIVE)
        )
        state.update_subject_state(
            make_subject_state(subject_id="physics", status=SubjectStatus.PAUSED)
        )
        state.update_subject_state(
            make_subject_state(subject_id="math", status=SubjectStatus.COMPLETED)
        )
        assert state.subject_state_for("math").status is SubjectStatus.COMPLETED
        assert state.subject_state_for("physics").status is SubjectStatus.PAUSED

    def test_update_subject_state_rejects_wrong_type(self) -> None:
        state = make_state()
        with pytest.raises(EducationalInvariantViolation):
            state.update_subject_state("not-a-subject-state")  # type: ignore[arg-type]

    def test_update_competency_adds_new_competency(self) -> None:
        state = make_state()
        state.update_competency(make_competency_state(competency_id="algebra"))
        state.update_competency(make_competency_state(competency_id="calculus"))
        assert state.competency_count() == 2
        assert state.has_competency(CompetencyId("algebra"))
        assert state.has_competency("calculus")
        assert not state.has_competency("geometry")

    def test_update_competency_preserves_other_competencies(self) -> None:
        state = make_state()
        state.update_competency(
            make_competency_state(competency_id="algebra", band=MasteryBand.DEVELOPING)
        )
        state.update_competency(
            make_competency_state(
                competency_id="calculus", band=MasteryBand.NOT_STARTED
            )
        )
        state.update_competency(
            make_competency_state(competency_id="algebra", band=MasteryBand.MASTERED)
        )
        assert state.competency_state_for("algebra").band is MasteryBand.MASTERED
        assert state.competency_state_for("calculus").band is MasteryBand.NOT_STARTED

    def test_update_competency_rejects_wrong_type(self) -> None:
        state = make_state()
        with pytest.raises(EducationalInvariantViolation):
            state.update_competency(123)  # type: ignore[arg-type]

    def test_subject_state_for_missing_returns_none(self) -> None:
        state = make_state()
        assert state.subject_state_for("missing") is None

    def test_competency_state_for_missing_returns_none(self) -> None:
        state = make_state()
        assert state.competency_state_for("missing") is None


class TestSummaryUpdates:
    def test_update_mastery_summary(self) -> None:
        state = make_state()
        summary = make_mastery_summary(MasteryBand.SECURE, ratio=0.8)
        state.update_mastery_summary(summary)
        assert state.mastery_summary is summary

    def test_update_mastery_summary_rejects_wrong_type(self) -> None:
        state = make_state()
        with pytest.raises(EducationalInvariantViolation):
            state.update_mastery_summary("not-a-summary")  # type: ignore[arg-type]

    def test_update_confidence_summary(self) -> None:
        state = make_state()
        summary = make_confidence_summary()
        state.update_confidence_summary(summary)
        assert state.confidence_summary is summary

    def test_update_confidence_summary_rejects_wrong_type(self) -> None:
        state = make_state()
        with pytest.raises(EducationalInvariantViolation):
            state.update_confidence_summary(object())  # type: ignore[arg-type]

    def test_update_educational_health(self) -> None:
        state = make_state()
        health = make_educational_health(EducationalHealthBand.AT_RISK)
        state.update_educational_health(health)
        assert state.educational_health is health

    def test_update_educational_health_rejects_wrong_type(self) -> None:
        state = make_state()
        with pytest.raises(EducationalInvariantViolation):
            state.update_educational_health("not-health")  # type: ignore[arg-type]


class TestLearningEpisodeReplacement:
    def test_attach_learning_episode_sets_reference(self) -> None:
        state = make_state()
        state.attach_learning_episode("episode-1")
        assert state.active_learning_episode_id == LearningEpisodeId("episode-1")
        assert state.has_active_learning_episode()

    def test_attach_learning_episode_accepts_typed_id(self) -> None:
        state = make_state()
        state.attach_learning_episode(LearningEpisodeId("episode-1"))
        assert state.active_learning_episode_id == LearningEpisodeId("episode-1")

    def test_only_one_active_learning_episode(self) -> None:
        state = make_state()
        state.attach_learning_episode("episode-1")
        state.attach_learning_episode("episode-2")
        # Only the most recently attached episode is remembered — never two.
        assert state.active_learning_episode_id == LearningEpisodeId("episode-2")

    def test_clear_learning_episode(self) -> None:
        state = make_state()
        state.attach_learning_episode("episode-1")
        state.clear_learning_episode()
        assert state.active_learning_episode_id is None
        assert not state.has_active_learning_episode()


class TestMissionReplacement:
    def test_attach_current_mission_sets_reference(self) -> None:
        state = make_state()
        state.attach_current_mission("mission-1")
        assert state.current_mission.mission_id.value == "mission-1"

    def test_only_one_current_mission(self) -> None:
        state = make_state()
        state.attach_current_mission("mission-1")
        state.attach_current_mission("mission-2")
        assert state.current_mission.mission_id.value == "mission-2"

    def test_attach_current_mission_accepts_mission_reference(self) -> None:
        state = make_state()
        ref = make_mission_reference("mission-99")
        state.attach_current_mission(ref)
        assert state.current_mission is ref

    def test_attach_current_mission_accepts_mission_id(self) -> None:
        state = make_state()
        state.attach_current_mission(MissionId("mission-7"))
        assert state.current_mission.mission_id.value == "mission-7"

    def test_clear_current_mission(self) -> None:
        state = make_state()
        state.attach_current_mission("mission-1")
        state.clear_current_mission()
        assert state.current_mission is None


class TestCheckpointReplacement:
    def test_attach_checkpoint_sets_reference(self) -> None:
        state = make_state()
        state.attach_checkpoint("checkpoint-1")
        assert state.current_checkpoint.checkpoint_id.value == "checkpoint-1"

    def test_only_one_current_checkpoint(self) -> None:
        state = make_state()
        state.attach_checkpoint("checkpoint-1")
        state.attach_checkpoint("checkpoint-2")
        assert state.current_checkpoint.checkpoint_id.value == "checkpoint-2"

    def test_attach_checkpoint_accepts_checkpoint_id(self) -> None:
        state = make_state()
        state.attach_checkpoint(CheckpointId("checkpoint-42"))
        assert state.current_checkpoint.checkpoint_id.value == "checkpoint-42"

    def test_clear_checkpoint(self) -> None:
        state = make_state()
        state.attach_checkpoint("checkpoint-1")
        state.clear_checkpoint()
        assert state.current_checkpoint is None

    def test_attach_checkpoint_accepts_checkpoint_reference(self) -> None:
        state = make_state()
        ref = make_checkpoint_reference("checkpoint-77")
        state.attach_checkpoint(ref)
        assert state.current_checkpoint is ref


class TestEducationalTimeline:
    def test_attach_educational_timeline_sets_reference(self) -> None:
        state = make_state()
        state.attach_educational_timeline("timeline-1")
        assert state.educational_timeline.timeline_id.value == "timeline-1"

    def test_attach_educational_timeline_replaces_prior(self) -> None:
        state = make_state()
        state.attach_educational_timeline("timeline-1")
        state.attach_educational_timeline("timeline-2")
        assert state.educational_timeline.timeline_id.value == "timeline-2"

    def test_clear_educational_timeline(self) -> None:
        state = make_state()
        state.attach_educational_timeline("timeline-1")
        state.clear_educational_timeline()
        assert state.educational_timeline is None

    def test_attach_educational_timeline_accepts_timeline_reference(self) -> None:
        state = make_state()
        ref = make_timeline_reference("timeline-77")
        state.attach_educational_timeline(ref)
        assert state.educational_timeline is ref

    def test_attach_educational_timeline_accepts_timeline_id(self) -> None:
        from domain.education.student_state import EducationalTimelineId

        state = make_state()
        state.attach_educational_timeline(EducationalTimelineId("timeline-88"))
        assert state.educational_timeline.timeline_id.value == "timeline-88"


class TestLastUpdatedTimestamp:
    def test_touch_updates_timestamp_when_supplied(self) -> None:
        state = make_state()
        as_of = datetime(2026, 3, 1, tzinfo=UTC)
        state.update_educational_health(make_educational_health(), occurred_at=as_of)
        assert state.last_updated_at == as_of

    def test_touch_preserves_timestamp_when_not_supplied(self) -> None:
        as_of = datetime(2026, 3, 1, tzinfo=UTC)
        state = StudentEducationalState.create(
            StudentEducationalStateId("s1"), "student-1", last_updated_at=as_of
        )
        state.update_educational_health(make_educational_health())
        assert state.last_updated_at == as_of

    def test_touch_rejects_non_datetime(self) -> None:
        state = make_state()
        with pytest.raises(EducationalInvariantViolation):
            state.update_educational_health(
                make_educational_health(), occurred_at="2026-01-01"  # type: ignore[arg-type]
            )

    def test_timestamp_advances_across_multiple_updates(self) -> None:
        state = make_state()
        first = datetime(2026, 1, 1, tzinfo=UTC)
        second = datetime(2026, 2, 1, tzinfo=UTC)
        state.attach_current_mission("mission-1", occurred_at=first)
        assert state.last_updated_at == first
        state.attach_checkpoint("checkpoint-1", occurred_at=second)
        assert state.last_updated_at == second


class TestSnapshotGeneration:
    def test_snapshot_reflects_empty_state(self) -> None:
        state = make_state()
        snapshot = state.produce_snapshot()
        assert snapshot.state_id == state.state_id
        assert snapshot.student_id == state.student_id
        assert snapshot.subject_states == ()
        assert snapshot.competency_states == ()

    def test_snapshot_reflects_populated_state(self) -> None:
        state = make_state()
        state.update_subject_state(make_subject_state(subject_id="math"))
        state.update_competency(make_competency_state(competency_id="algebra"))
        state.update_mastery_summary(make_mastery_summary())
        state.update_confidence_summary(make_confidence_summary())
        state.update_educational_health(make_educational_health())
        state.attach_learning_episode("episode-1")
        state.attach_current_mission("mission-1")
        state.attach_checkpoint("checkpoint-1")
        state.attach_educational_timeline("timeline-1")

        snapshot = state.produce_snapshot()

        assert snapshot.subject_states == state.subject_states
        assert snapshot.competency_states == state.competency_states
        assert snapshot.mastery_summary == state.mastery_summary
        assert snapshot.confidence_summary == state.confidence_summary
        assert snapshot.educational_health == state.educational_health
        assert snapshot.active_learning_episode_id == state.active_learning_episode_id
        assert snapshot.current_mission == state.current_mission
        assert snapshot.current_checkpoint == state.current_checkpoint
        assert snapshot.educational_timeline == state.educational_timeline
        assert snapshot.subject_count() == 1
        assert snapshot.competency_count() == 1
        assert snapshot.has_active_learning_episode()
        assert snapshot.has_current_mission()
        assert snapshot.has_current_checkpoint()
        assert snapshot.has_educational_timeline()

    def test_snapshot_is_independent_of_further_mutation(self) -> None:
        state = make_state()
        state.update_subject_state(make_subject_state(subject_id="math"))
        snapshot = state.produce_snapshot()
        state.update_subject_state(
            make_subject_state(subject_id="physics", status=SubjectStatus.ACTIVE)
        )
        assert snapshot.subject_count() == 1
        assert state.subject_count() == 2

    def test_two_snapshots_from_same_state_are_equal(self) -> None:
        state = make_state()
        state.update_subject_state(make_subject_state(subject_id="math"))
        first = state.produce_snapshot()
        second = state.produce_snapshot()
        assert first == second


class TestAggregateEqualityAndRepr:
    def test_equality_by_state_id(self) -> None:
        a = make_state(state_id="s1", student_id="student-a")
        b = make_state(state_id="s1", student_id="student-b")
        assert a == b  # identity equality, not attribute equality

    def test_inequality_across_ids(self) -> None:
        a = make_state(state_id="s1")
        b = make_state(state_id="s2")
        assert a != b

    def test_hashable(self) -> None:
        a = make_state(state_id="s1")
        assert hash(a) == hash(a)

    def test_repr_contains_identity(self) -> None:
        state = make_state(state_id="s1", student_id="student-ada")
        text = repr(state)
        assert "s1" in text
        assert "student-ada" in text

    def test_equality_with_non_aggregate(self) -> None:
        state = make_state()
        assert state != "not-a-state"

    def test_equality_with_identical_object_reference(self) -> None:
        state = make_state()
        assert state == state  # noqa: PLR0124 - explicit identity check


class TestEdgeCases:
    def test_many_subjects_and_competencies(self) -> None:
        state = make_state()
        for i in range(50):
            state.update_subject_state(make_subject_state(subject_id=f"subject-{i}"))
        for i in range(50):
            state.update_competency(
                make_competency_state(
                    competency_id=f"competency-{i}", subject_id="subject-0"
                )
            )
        assert state.subject_count() == 50
        assert state.competency_count() == 50
        snapshot = state.produce_snapshot()
        assert snapshot.subject_count() == 50
        assert snapshot.competency_count() == 50

    def test_has_subject_accepts_typed_and_raw_ids(self) -> None:
        state = make_state()
        state.update_subject_state(make_subject_state(subject_id="math"))
        assert state.has_subject(SubjectId("math"))
        assert state.has_subject("math")

    def test_has_competency_accepts_typed_and_raw_ids(self) -> None:
        state = make_state()
        state.update_competency(make_competency_state(competency_id="algebra"))
        assert state.has_competency(CompetencyId("algebra"))
        assert state.has_competency("algebra")
