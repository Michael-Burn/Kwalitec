"""Shared helpers for APP-001/APP-002 application-layer tests."""

from __future__ import annotations

from domain.education.digital_twin import EducationalDigitalTwin
from domain.education.foundation.enums import LearningDimension
from domain.education.foundation.ids import (
    DigitalTwinId,
    LearningEpisodeId,
    LearningObjectiveId,
    TeachingStrategyId,
)
from domain.education.foundation.references import LearningObjectiveReference
from domain.education.learning_episode import (
    EpisodeGoal,
    EpisodeGoalId,
    EpisodeStep,
    EpisodeStepId,
    EpisodeStepKind,
    LearningEpisode,
)
from tests.education_os.application.fakes import (
    FixedClock,
    InMemoryEventPublisher,
    InMemorySubjectKnowledgeRepository,
    InMemoryTeachingPlanRepository,
    InMemoryUnitOfWork,
    SequenceUUIDGenerator,
)


def make_planned_episode(
    *,
    episode_id: str = "episode-001",
    student_id: str = "student-ada",
) -> LearningEpisode:
    return LearningEpisode.create(
        episode_id=LearningEpisodeId(episode_id),
        student_id=student_id,
        teaching_goal=EpisodeGoal(
            goal_id=EpisodeGoalId("goal-001"),
            statement="Repair select-vs-ultimate mortality confusion",
            educational_purpose="Replace confusion with correct discrimination",
            primary_dimension=LearningDimension.UNDERSTANDING,
        ),
        teaching_strategy_id=TeachingStrategyId("strategy-worked-example"),
        learning_objectives=[
            LearningObjectiveReference(
                objective_id=LearningObjectiveId("lo-001"),
                label="Select vs ultimate",
            )
        ],
        steps=[
            EpisodeStep(
                step_id=EpisodeStepId("step-001"),
                kind=EpisodeStepKind.explanation(),
                sequence_index=0,
                label="Explanation",
                required=True,
            ),
            EpisodeStep(
                step_id=EpisodeStepId("step-002"),
                kind=EpisodeStepKind.guided_practice(),
                sequence_index=1,
                label="Practice",
                required=True,
            ),
        ],
    )


def make_uow(
    *,
    with_concept: str | None = "concept-001",
) -> InMemoryUnitOfWork:
    uow = InMemoryUnitOfWork()
    if with_concept is not None:
        assert isinstance(uow.subject_knowledge, InMemorySubjectKnowledgeRepository)
        uow.subject_knowledge.register_existence(with_concept)
    return uow


def make_twin(
    uow: InMemoryUnitOfWork,
    *,
    twin_id: str = "twin-001",
    student_id: str = "student-ada",
) -> EducationalDigitalTwin:
    created = EducationalDigitalTwin.create(
        twin_id=DigitalTwinId(twin_id),
        student_id=student_id,
    )
    created.pull_events()
    uow.digital_twins.save(created)
    return created


def make_subject_repo() -> InMemorySubjectKnowledgeRepository:
    repo = InMemorySubjectKnowledgeRepository()
    repo.register_existence("concept-001")
    return repo


def make_events() -> InMemoryEventPublisher:
    return InMemoryEventPublisher()


def make_clock() -> FixedClock:
    return FixedClock()


def make_uuids() -> SequenceUUIDGenerator:
    return SequenceUUIDGenerator()


def make_teaching_plans() -> InMemoryTeachingPlanRepository:
    return InMemoryTeachingPlanRepository()
