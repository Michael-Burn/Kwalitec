"""PlanningApplicationService — teaching plan generation and retrieval."""

from __future__ import annotations

from application.commands.generate_teaching_plan import GenerateTeachingPlan
from application.dto.teaching_plan import TeachingPlanDTO
from application.errors import ApplicationError, ConflictError, NotFoundError
from application.events.planning import TeachingPlanGeneratedApplicationEvent
from application.ports.clock import Clock
from application.ports.event_publisher import ApplicationEventPublisher
from application.ports.unit_of_work import UnitOfWork
from application.queries.get_teaching_plan import GetTeachingPlan
from application.services.mappers import to_teaching_plan_dto
from domain.education.foundation.enums import LearningDimension
from domain.education.foundation.errors import EducationalDomainError
from domain.education.foundation.ids import (
    ConceptId,
    LearningEpisodeId,
    LearningObjectiveId,
    TeachingStrategyId,
)
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
)
from domain.education.learning_episode import (
    EpisodeGoal,
    EpisodeGoalId,
    EpisodeStep,
    EpisodeStepId,
    EpisodeStepKind,
    LearningEpisode,
)
from domain.education.learning_episode.enums import EpisodeStatus


class PlanningApplicationService:
    """Coordinates teaching-plan persistence as planned Learning Episodes.

    Does not choose strategies, prioritise, or diagnose. Educational inputs are
    supplied on the command; subject-knowledge ports only verify concept
    existence.
    """

    def __init__(
        self,
        uow: UnitOfWork,
        events: ApplicationEventPublisher,
        clock: Clock,
    ) -> None:
        self._uow = uow
        self._events = events
        self._clock = clock

    def generate_teaching_plan(self, command: GenerateTeachingPlan) -> TeachingPlanDTO:
        """Validate concept refs, create planned episode, commit, publish."""
        if not command.steps:
            raise ApplicationError("GenerateTeachingPlan requires at least one step")
        if not command.learning_objective_ids:
            raise ApplicationError(
                "GenerateTeachingPlan requires at least one learning objective"
            )

        with self._uow:
            for concept_key in command.concept_ids:
                if not self._uow.subject_knowledge.exists(ConceptId(concept_key)):
                    raise NotFoundError("Concept", concept_key)

            existing = self._uow.episodes.get(LearningEpisodeId(command.episode_id))
            if existing is not None:
                raise ConflictError(
                    f"episode {command.episode_id} already exists"
                )

            try:
                episode = self._build_episode(command)
            except EducationalDomainError as exc:
                raise ConflictError(str(exc)) from exc

            self._uow.episodes.save(episode)
            self._uow.teaching_plan.save(command.plan_id, episode.episode_id)
            self._uow.commit()

        self._events.publish(
            TeachingPlanGeneratedApplicationEvent.create(
                plan_id=command.plan_id,
                episode_id=episode.episode_id.value,
                student_id=episode.student_id,
                occurred_at=self._clock.now(),
            )
        )
        return to_teaching_plan_dto(episode, plan_id=command.plan_id)

    def get_teaching_plan(self, query: GetTeachingPlan) -> TeachingPlanDTO:
        with self._uow:
            episode = self._uow.episodes.get(LearningEpisodeId(query.episode_id))
            if episode is None:
                raise NotFoundError("LearningEpisode", query.episode_id)
            plan_id = self._uow.teaching_plan.get_plan_id(episode.episode_id)
        resolved = plan_id if plan_id is not None else f"plan-{query.episode_id}"
        return to_teaching_plan_dto(episode, plan_id=resolved)

    def _build_episode(self, command: GenerateTeachingPlan) -> LearningEpisode:
        goal = EpisodeGoal(
            goal_id=EpisodeGoalId(command.goal_id),
            statement=command.goal_statement,
            educational_purpose=command.goal_purpose,
            primary_dimension=LearningDimension(command.primary_dimension),
        )
        objectives = [
            LearningObjectiveReference(
                objective_id=LearningObjectiveId(oid),
                label=oid,
            )
            for oid in command.learning_objective_ids
        ]
        steps = [
            EpisodeStep(
                step_id=EpisodeStepId(spec.step_id),
                kind=EpisodeStepKind(spec.kind),
                sequence_index=spec.sequence_index,
                label=spec.label,
                required=spec.required,
            )
            for spec in command.steps
        ]
        concepts = [
            ConceptReference(concept_id=ConceptId(cid), label=cid)
            for cid in command.concept_ids
        ]
        episode = LearningEpisode.create(
            episode_id=LearningEpisodeId(command.episode_id),
            student_id=command.student_id,
            teaching_goal=goal,
            teaching_strategy_id=TeachingStrategyId(command.teaching_strategy_id),
            learning_objectives=objectives,
            steps=steps,
            concept_references=concepts or None,
            selection_rationale=command.selection_rationale,
        )
        if episode.status is not EpisodeStatus.PLANNED:
            raise ConflictError("generated teaching plan must be planned")
        return episode
