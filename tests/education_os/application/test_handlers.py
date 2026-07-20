"""Handler and service coordination tests for APP-001/APP-002."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from application.commands import (
    CompleteLearningEpisode,
    EvidenceItemSpec,
    GenerateTeachingPlan,
    RecordEvidence,
    StartLearningSession,
    TeachingPlanStepSpec,
    TwinUpdateKind,
    UpdateDigitalTwin,
)
from application.errors import ConflictError, NotFoundError
from application.events import (
    DigitalTwinUpdatedApplicationEvent,
    EvidenceRecordedApplicationEvent,
    LearningEpisodeCompletedApplicationEvent,
    LearningSessionStartedApplicationEvent,
    TeachingPlanGeneratedApplicationEvent,
)
from application.handlers import (
    CompleteLearningEpisodeHandler,
    GenerateTeachingPlanHandler,
    GetEvidenceHistoryHandler,
    GetLearnerStateHandler,
    GetLearningTrajectoryHandler,
    GetTeachingPlanHandler,
    RecordEvidenceHandler,
    StartLearningSessionHandler,
    UpdateDigitalTwinHandler,
)
from application.queries import (
    GetEvidenceHistory,
    GetLearnerState,
    GetLearningTrajectory,
    GetTeachingPlan,
)
from application.services import (
    AssessmentApplicationService,
    LearningApplicationService,
    PlanningApplicationService,
    TwinApplicationService,
)
from domain.education.digital_twin import MasteryBand
from domain.education.foundation.enums import EvidenceType
from domain.education.foundation.ids import DigitalTwinId, LearningEpisodeId
from tests.education_os.application.helpers import (
    make_clock,
    make_events,
    make_planned_episode,
    make_twin,
    make_uow,
)


def test_start_learning_session_handler() -> None:
    uow = make_uow()
    events = make_events()
    episode = make_planned_episode()
    uow.episodes.save(episode)
    service = LearningApplicationService(uow, events, make_clock())
    handler = StartLearningSessionHandler(service)

    dto = handler.handle(StartLearningSession(episode_id="episode-001"))

    assert dto.status == "in_progress"
    assert dto.first_active_step_id == "step-001"
    assert len(events.of_type(LearningSessionStartedApplicationEvent)) == 1
    loaded = uow.episodes.get(episode.episode_id)
    assert loaded is not None
    assert loaded.status.value == "in_progress"
    assert uow.commit_count == 1
    assert uow.begin_count == 1


def test_start_learning_session_not_found() -> None:
    uow = make_uow()
    handler = StartLearningSessionHandler(
        LearningApplicationService(uow, make_events(), make_clock())
    )
    with pytest.raises(NotFoundError):
        handler.handle(StartLearningSession(episode_id="missing"))
    assert uow.rollback_count == 1
    assert uow.commit_count == 0


def test_generate_and_get_teaching_plan() -> None:
    uow = make_uow()
    events = make_events()
    service = PlanningApplicationService(uow, events, make_clock())
    generate = GenerateTeachingPlanHandler(service)
    query = GetTeachingPlanHandler(service)

    plan = generate.handle(
        GenerateTeachingPlan(
            plan_id="plan-001",
            episode_id="episode-plan",
            student_id="student-ada",
            goal_id="goal-001",
            goal_statement="Build intuition for force of mortality",
            goal_purpose="Establish continuous mortality intuition",
            primary_dimension="understanding",
            teaching_strategy_id="strategy-analogy",
            learning_objective_ids=("lo-001",),
            concept_ids=("concept-001",),
            steps=(
                TeachingPlanStepSpec(
                    step_id="step-001",
                    kind="explanation",
                    sequence_index=0,
                    label="Explain",
                ),
                TeachingPlanStepSpec(
                    step_id="step-002",
                    kind="worked_example",
                    sequence_index=1,
                    label="Worked example",
                ),
            ),
        )
    )

    assert plan.plan_id == "plan-001"
    assert plan.status == "planned"
    assert len(plan.steps) == 2
    assert len(events.of_type(TeachingPlanGeneratedApplicationEvent)) == 1
    assert (
        uow.teaching_plan.get_plan_id(LearningEpisodeId("episode-plan"))
        == "plan-001"
    )

    loaded = query.handle(GetTeachingPlan(episode_id="episode-plan"))
    assert loaded.episode_id == "episode-plan"
    assert loaded.teaching_strategy_id == "strategy-analogy"
    assert loaded.plan_id == "plan-001"


def test_generate_teaching_plan_unknown_concept() -> None:
    handler = GenerateTeachingPlanHandler(
        PlanningApplicationService(make_uow(), make_events(), make_clock())
    )
    with pytest.raises(NotFoundError):
        handler.handle(
            GenerateTeachingPlan(
                plan_id="plan-x",
                episode_id="episode-x",
                student_id="student-ada",
                goal_id="goal-001",
                goal_statement="Goal",
                goal_purpose="Purpose statement for learning",
                primary_dimension="understanding",
                teaching_strategy_id="strategy-analogy",
                learning_objective_ids=("lo-001",),
                concept_ids=("concept-unknown",),
                steps=(
                    TeachingPlanStepSpec(
                        step_id="step-001",
                        kind="explanation",
                        sequence_index=0,
                        label="Explain",
                    ),
                ),
            )
        )


def test_record_evidence_and_history() -> None:
    uow = make_uow()
    events = make_events()
    service = AssessmentApplicationService(uow, events, make_clock())
    record_handler = RecordEvidenceHandler(service)
    history_handler = GetEvidenceHistoryHandler(service)

    dto = record_handler.handle(
        RecordEvidence(
            evidence_id="evidence-001",
            student_id="student-ada",
            source_id="source-001",
            source_kind="assessment",
            source_label="Quiz probe",
            context_id="ctx-001",
            context_dimension="understanding",
            context_summary="Post-explanation probe",
            confidence_level="high",
            strength_level="strong",
            occurred_at=datetime(2026, 7, 20, 10, 0, tzinfo=UTC),
            items=(
                EvidenceItemSpec(
                    item_id="item-001",
                    kind="question_response",
                    summary="Correct discrimination of select vs ultimate",
                    concept_id="concept-001",
                ),
            ),
            concept_ids=("concept-001",),
        )
    )

    assert dto.evidence_id == "evidence-001"
    assert dto.item_count == 1
    assert len(events.of_type(EvidenceRecordedApplicationEvent)) == 1

    history = history_handler.handle(GetEvidenceHistory(student_id="student-ada"))
    assert history.count == 1
    assert history.records[0].evidence_id == "evidence-001"


def test_update_digital_twin_and_queries() -> None:
    uow = make_uow()
    events = make_events()
    make_twin(uow)
    service = TwinApplicationService(uow, events, make_clock())
    update_handler = UpdateDigitalTwinHandler(service)
    state_handler = GetLearnerStateHandler(service)
    traj_handler = GetLearningTrajectoryHandler(service)

    summary = update_handler.handle(
        UpdateDigitalTwin(
            twin_id="twin-001",
            update_kind=TwinUpdateKind.UPDATE_MASTERY,
            concept_id="concept-001",
            mastery_band=MasteryBand.DEVELOPING.value,
            mastery_ratio=0.55,
        )
    )
    assert summary.concept_count == 1
    assert summary.update_kind == "update_mastery"
    assert len(events.of_type(DigitalTwinUpdatedApplicationEvent)) == 1

    update_handler.handle(
        UpdateDigitalTwin(
            twin_id="twin-001",
            update_kind=TwinUpdateKind.RECORD_EVIDENCE,
            evidence_id="evidence-001",
            evidence_type=EvidenceType.PERFORMANCE.value,
            concept_id="concept-001",
        )
    )

    state = state_handler.handle(GetLearnerState(twin_id="twin-001"))
    assert state.evidence_count == 1
    assert state.concept_count == 1

    traj = traj_handler.handle(GetLearningTrajectory(student_id="student-ada"))
    assert traj.length >= 3


def test_complete_learning_episode_flow() -> None:
    uow = make_uow()
    events = make_events()
    uow.episodes.save(make_planned_episode())
    learning = LearningApplicationService(uow, events, make_clock())

    StartLearningSessionHandler(learning).handle(
        StartLearningSession(episode_id="episode-001")
    )
    learning.attach_evidence("episode-001", "evidence-001")

    dto = CompleteLearningEpisodeHandler(learning).handle(
        CompleteLearningEpisode(
            episode_id="episode-001",
            reflection_id="reflection-001",
            reflection_type="post_episode",
            reflection_content="I can now discriminate select and ultimate ages.",
            outcome_id="outcome-001",
            outcome_kind="goal_achieved",
            outcome_summary="Goal advanced through explanation and practice",
        )
    )

    assert dto.status == "completed"
    assert dto.has_reflection is True
    assert dto.outcome_kind == "goal_achieved"
    assert len(events.of_type(LearningEpisodeCompletedApplicationEvent)) == 1


def test_complete_without_start_conflicts() -> None:
    uow = make_uow()
    uow.episodes.save(make_planned_episode())
    handler = CompleteLearningEpisodeHandler(
        LearningApplicationService(uow, make_events(), make_clock())
    )
    with pytest.raises(ConflictError):
        handler.handle(
            CompleteLearningEpisode(
                episode_id="episode-001",
                reflection_id="reflection-001",
                reflection_type="post_episode",
                reflection_content="Not ready yet.",
                outcome_id="outcome-001",
                outcome_kind="goal_achieved",
                outcome_summary="Should not complete while planned",
            )
        )


def test_get_learner_state_missing_twin() -> None:
    handler = GetLearnerStateHandler(
        TwinApplicationService(make_uow(), make_events(), make_clock())
    )
    with pytest.raises(NotFoundError):
        handler.handle(GetLearnerState(twin_id="missing"))


def test_record_evidence_can_update_twin() -> None:
    uow = make_uow()
    events = make_events()
    make_twin(uow)
    service = AssessmentApplicationService(uow, events, make_clock())
    RecordEvidenceHandler(service).handle(
        RecordEvidence(
            evidence_id="evidence-twin",
            student_id="student-ada",
            source_id="source-001",
            source_kind="assessment",
            source_label="Probe",
            context_id="ctx-001",
            context_dimension="understanding",
            context_summary="Probe context",
            confidence_level="medium",
            strength_level="moderate",
            occurred_at=datetime(2026, 7, 20, 11, 0, tzinfo=UTC),
            items=(
                EvidenceItemSpec(
                    item_id="item-001",
                    kind="retrieval_attempt",
                    summary="Partial retrieval of definition",
                ),
            ),
            twin_id="twin-001",
            evidence_type_for_twin=EvidenceType.PERFORMANCE.value,
        )
    )
    stored = uow.digital_twins.get(DigitalTwinId("twin-001"))
    assert stored is not None
    assert stored.evidence_count() == 1
