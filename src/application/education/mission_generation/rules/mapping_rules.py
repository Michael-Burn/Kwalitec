"""MappingRules — map RecommendationCategory to MissionType and objectives."""

from __future__ import annotations

from dataclasses import dataclass

from application.education.mission_generation.enums import (
    MissionObjectiveCode,
    MissionRecurrenceBand,
    MissionStepAction,
    MissionType,
)
from domain.education.recommendation_engine.enums import RecommendationCategory
from domain.education.recommendation_engine.value_objects.recommendation import (
    Recommendation,
)

# Categories that express educational intent but do not produce missions.
_NON_MISSION_CATEGORIES: frozenset[RecommendationCategory] = frozenset(
    {
        RecommendationCategory.DELAY_ADVANCED_TOPIC,
    }
)

_CATEGORY_TO_TYPE: dict[RecommendationCategory, MissionType] = {
    RecommendationCategory.REVIEW_CONCEPT: MissionType.REVIEW_CONCEPT,
    RecommendationCategory.STUDY_PREREQUISITE: MissionType.REVISE_PREREQUISITE,
    RecommendationCategory.STRENGTHEN_WEAK_AREA: MissionType.STRENGTHEN_FOUNDATION,
    RecommendationCategory.REVISIT_FOUNDATION: MissionType.STRENGTHEN_FOUNDATION,
    RecommendationCategory.FOCUS_COMPETENCY: MissionType.PRACTICE_QUESTIONS,
    RecommendationCategory.CONSOLIDATE_KNOWLEDGE: MissionType.CONSOLIDATE_KNOWLEDGE,
    RecommendationCategory.INCREASE_REVISION_FREQUENCY: MissionType.REVISION_SESSION,
    RecommendationCategory.REDUCE_REVISION_FREQUENCY: MissionType.MAINTENANCE_REVIEW,
    RecommendationCategory.MAINTAIN_MASTERY: MissionType.MAINTENANCE_REVIEW,
    RecommendationCategory.ATTEMPT_CHECKPOINT: MissionType.CHECKPOINT_PREPARATION,
    RecommendationCategory.PREPARE_ASSESSMENT: MissionType.CHECKPOINT_PREPARATION,
    RecommendationCategory.CONTINUE_CURRENT_MISSION: MissionType.MIXED_PRACTICE,
}

_TYPE_TO_OBJECTIVE: dict[MissionType, MissionObjectiveCode] = {
    MissionType.PRACTICE_QUESTIONS: MissionObjectiveCode.COMPLETE_PRACTICE,
    MissionType.REVIEW_CONCEPT: MissionObjectiveCode.REVIEW_TARGET,
    MissionType.STRENGTHEN_FOUNDATION: MissionObjectiveCode.STRENGTHEN_TARGET,
    MissionType.REVISE_PREREQUISITE: MissionObjectiveCode.ADDRESS_PREREQUISITE,
    MissionType.CONSOLIDATE_KNOWLEDGE: MissionObjectiveCode.CONSOLIDATE_TARGET,
    MissionType.CHECKPOINT_PREPARATION: MissionObjectiveCode.PREPARE_CHECKPOINT,
    MissionType.REVISION_SESSION: MissionObjectiveCode.REVISE_TARGET,
    MissionType.MIXED_PRACTICE: MissionObjectiveCode.MIXED_COVERAGE,
    MissionType.CONFIDENCE_RECOVERY: MissionObjectiveCode.RECOVER_CONFIDENCE,
    MissionType.MAINTENANCE_REVIEW: MissionObjectiveCode.MAINTAIN_TARGET,
}

_TYPE_TO_ACTION: dict[MissionType, MissionStepAction] = {
    MissionType.PRACTICE_QUESTIONS: MissionStepAction.PRACTICE,
    MissionType.REVIEW_CONCEPT: MissionStepAction.REVIEW,
    MissionType.STRENGTHEN_FOUNDATION: MissionStepAction.REVISE,
    MissionType.REVISE_PREREQUISITE: MissionStepAction.REVISE,
    MissionType.CONSOLIDATE_KNOWLEDGE: MissionStepAction.CONSOLIDATE,
    MissionType.CHECKPOINT_PREPARATION: MissionStepAction.PREPARE,
    MissionType.REVISION_SESSION: MissionStepAction.REVISE,
    MissionType.MIXED_PRACTICE: MissionStepAction.MIX,
    MissionType.CONFIDENCE_RECOVERY: MissionStepAction.RECOVER,
    MissionType.MAINTENANCE_REVIEW: MissionStepAction.MAINTAIN,
}

_LOW_CONFIDENCE_THRESHOLD = 0.40


@dataclass(frozen=True, slots=True)
class MissionIntent:
    """Resolved mission intent for one recommendation (or merged group)."""

    mission_type: MissionType
    objective_code: MissionObjectiveCode
    step_action: MissionStepAction
    recurrence: MissionRecurrenceBand
    subject_id: str | None
    competency_id: str | None
    priority_magnitude: float
    source_recommendation_ids: tuple[str, ...]


class MappingRules:
    """Deterministically maps educational recommendations to mission intent."""

    @staticmethod
    def produces_mission(recommendation: Recommendation) -> bool:
        return recommendation.category not in _NON_MISSION_CATEGORIES

    @staticmethod
    def mission_type_for(category: RecommendationCategory) -> MissionType | None:
        return _CATEGORY_TO_TYPE.get(category)

    @staticmethod
    def objective_code_for(mission_type: MissionType) -> MissionObjectiveCode:
        return _TYPE_TO_OBJECTIVE[mission_type]

    @staticmethod
    def step_action_for(mission_type: MissionType) -> MissionStepAction:
        return _TYPE_TO_ACTION[mission_type]

    @staticmethod
    def recurrence_for(category: RecommendationCategory) -> MissionRecurrenceBand:
        if category is RecommendationCategory.INCREASE_REVISION_FREQUENCY:
            return MissionRecurrenceBand.INCREASED
        if category is RecommendationCategory.REDUCE_REVISION_FREQUENCY:
            return MissionRecurrenceBand.REDUCED
        if category is RecommendationCategory.MAINTAIN_MASTERY:
            return MissionRecurrenceBand.REDUCED
        return MissionRecurrenceBand.NORMAL

    @staticmethod
    def resolve(recommendation: Recommendation) -> MissionIntent | None:
        """Resolve a single recommendation into mission intent, or None."""
        if not MappingRules.produces_mission(recommendation):
            return None

        mission_type = MappingRules.mission_type_for(recommendation.category)
        if mission_type is None:
            return None

        # Low confidence on review/focus work → confidence recovery mission.
        if (
            recommendation.confidence.magnitude < _LOW_CONFIDENCE_THRESHOLD
            and recommendation.category
            in {
                RecommendationCategory.REVIEW_CONCEPT,
                RecommendationCategory.FOCUS_COMPETENCY,
                RecommendationCategory.STRENGTHEN_WEAK_AREA,
            }
        ):
            mission_type = MissionType.CONFIDENCE_RECOVERY

        subject_id = (
            recommendation.target.subject_id.value
            if recommendation.target.subject_id is not None
            else None
        )
        competency_id = (
            recommendation.target.competency_id.value
            if recommendation.target.competency_id is not None
            else None
        )
        return MissionIntent(
            mission_type=mission_type,
            objective_code=MappingRules.objective_code_for(mission_type),
            step_action=MappingRules.step_action_for(mission_type),
            recurrence=MappingRules.recurrence_for(recommendation.category),
            subject_id=subject_id,
            competency_id=competency_id,
            priority_magnitude=recommendation.priority.magnitude,
            source_recommendation_ids=(recommendation.recommendation_id.value,),
        )
