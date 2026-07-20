"""Map LearningEpisode ↔ LearningEpisodeDTO."""

from __future__ import annotations

from domain.education.foundation.enums import (
    ConfidenceLevel,
    LearningDimension,
    ReflectionType,
)
from domain.education.foundation.ids import (
    EvidenceId,
    LearningEpisodeId,
    ReflectionId,
    TeachingStrategyId,
)
from domain.education.learning_episode import (
    DurationBand,
    EpisodeDuration,
    EpisodeGoal,
    EpisodeGoalId,
    EpisodeOutcome,
    EpisodeOutcomeId,
    EpisodeOutcomeKind,
    EpisodeReflection,
    EpisodeStatus,
    EpisodeStep,
    EpisodeStepId,
    EpisodeStepKind,
    EpisodeStepStatus,
    LearningEpisode,
)
from infrastructure.persistence.dto.learning_episode import (
    EpisodeDurationDTO,
    EpisodeGoalDTO,
    EpisodeOutcomeDTO,
    EpisodeReflectionDTO,
    EpisodeStepDTO,
    LearningEpisodeDTO,
)
from infrastructure.persistence.mappers.codec import (
    concept_ref_from_dto,
    concept_ref_to_dto,
    enum_value,
    id_value,
    objective_ref_from_dto,
    objective_ref_to_dto,
    optional_enum_value,
)


class LearningEpisodeMapper:
    """Pure structural mapper for LearningEpisode."""

    @staticmethod
    def to_persistence(episode: LearningEpisode) -> LearningEpisodeDTO:
        duration = None
        if episode.duration is not None:
            duration = EpisodeDurationDTO(
                planned_minutes=episode.duration.planned_minutes,
                band=optional_enum_value(episode.duration.band),
            )
        reflection = None
        if episode.reflection is not None:
            reflection = EpisodeReflectionDTO(
                reflection_id=id_value(episode.reflection.reflection_id),
                reflection_type=enum_value(episode.reflection.reflection_type),
                content=episode.reflection.content,
                perceived_difficulty=optional_enum_value(
                    episode.reflection.perceived_difficulty
                ),
                perceived_understanding=optional_enum_value(
                    episode.reflection.perceived_understanding
                ),
            )
        outcome = None
        if episode.outcome is not None:
            outcome = EpisodeOutcomeDTO(
                outcome_id=id_value(episode.outcome.outcome_id),
                kind=enum_value(episode.outcome.kind),
                summary=episode.outcome.summary,
            )
        return LearningEpisodeDTO(
            episode_id=id_value(episode.episode_id),
            student_id=episode.student_id,
            teaching_goal=EpisodeGoalDTO(
                goal_id=id_value(episode.teaching_goal.goal_id),
                statement=episode.teaching_goal.statement,
                educational_purpose=episode.teaching_goal.educational_purpose,
                primary_dimension=enum_value(
                    episode.teaching_goal.primary_dimension
                ),
            ),
            teaching_strategy_id=id_value(episode.teaching_strategy_id),
            learning_objectives=tuple(
                objective_ref_to_dto(ref) for ref in episode.learning_objectives
            ),
            steps=tuple(_step_to_dto(step) for step in episode.steps),
            concept_references=tuple(
                concept_ref_to_dto(ref) for ref in episode.concept_references
            ),
            primary_dimension=enum_value(episode.primary_dimension),
            duration=duration,
            selection_rationale=episode.selection_rationale,
            status=enum_value(episode.status),
            reflection=reflection,
            outcome=outcome,
            evidence_ids=tuple(id_value(eid) for eid in episode.evidence_ids),
        )

    @staticmethod
    def to_domain(dto: LearningEpisodeDTO) -> LearningEpisode:
        duration = None
        if dto.duration is not None:
            band = (
                DurationBand(dto.duration.band)
                if dto.duration.band is not None
                else None
            )
            duration = EpisodeDuration(
                planned_minutes=dto.duration.planned_minutes,
                band=band,
            )
        reflection = None
        if dto.reflection is not None:
            reflection = EpisodeReflection(
                reflection_id=ReflectionId(dto.reflection.reflection_id),
                reflection_type=ReflectionType(dto.reflection.reflection_type),
                content=dto.reflection.content,
                perceived_difficulty=(
                    ConfidenceLevel(dto.reflection.perceived_difficulty)
                    if dto.reflection.perceived_difficulty is not None
                    else None
                ),
                perceived_understanding=(
                    ConfidenceLevel(dto.reflection.perceived_understanding)
                    if dto.reflection.perceived_understanding is not None
                    else None
                ),
            )
        outcome = None
        if dto.outcome is not None:
            outcome = EpisodeOutcome(
                outcome_id=EpisodeOutcomeId(dto.outcome.outcome_id),
                kind=EpisodeOutcomeKind(dto.outcome.kind),
                summary=dto.outcome.summary,
            )
        return LearningEpisode(
            episode_id=LearningEpisodeId(dto.episode_id),
            student_id=dto.student_id,
            teaching_goal=EpisodeGoal(
                goal_id=EpisodeGoalId(dto.teaching_goal.goal_id),
                statement=dto.teaching_goal.statement,
                educational_purpose=dto.teaching_goal.educational_purpose,
                primary_dimension=LearningDimension(
                    dto.teaching_goal.primary_dimension
                ),
            ),
            teaching_strategy_id=TeachingStrategyId(dto.teaching_strategy_id),
            learning_objectives=tuple(
                objective_ref_from_dto(ref) for ref in dto.learning_objectives
            ),
            steps=tuple(_step_from_dto(step) for step in dto.steps),
            concept_references=tuple(
                concept_ref_from_dto(ref) for ref in dto.concept_references
            ),
            primary_dimension=LearningDimension(dto.primary_dimension),
            duration=duration,
            selection_rationale=dto.selection_rationale,
            status=EpisodeStatus(dto.status),
            reflection=reflection,
            outcome=outcome,
            evidence_ids=tuple(EvidenceId(eid) for eid in dto.evidence_ids),
        )


def _step_to_dto(step: EpisodeStep) -> EpisodeStepDTO:
    return EpisodeStepDTO(
        step_id=id_value(step.step_id),
        kind=step.kind.value,
        sequence_index=step.sequence_index,
        label=step.label,
        required=step.required,
        status=enum_value(step.status),
    )


def _step_from_dto(dto: EpisodeStepDTO) -> EpisodeStep:
    return EpisodeStep(
        step_id=EpisodeStepId(dto.step_id),
        kind=EpisodeStepKind(dto.kind),
        sequence_index=dto.sequence_index,
        label=dto.label,
        required=dto.required,
        status=EpisodeStepStatus(dto.status),
    )
