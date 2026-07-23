"""MergeRules — merge related recommendations into coherent missions."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from application.education.mission_generation.enums import (
    MissionRecurrenceBand,
    MissionType,
)
from application.education.mission_generation.rules.mapping_rules import (
    MappingRules,
    MissionIntent,
)
from domain.education.recommendation_engine.value_objects.recommendation import (
    Recommendation,
)

# Types that may merge when subject+competency match.
_MERGEABLE_TYPES: frozenset[MissionType] = frozenset(
    {
        MissionType.PRACTICE_QUESTIONS,
        MissionType.REVIEW_CONCEPT,
        MissionType.STRENGTHEN_FOUNDATION,
        MissionType.CONSOLIDATE_KNOWLEDGE,
        MissionType.REVISION_SESSION,
        MissionType.MAINTENANCE_REVIEW,
        MissionType.CONFIDENCE_RECOVERY,
        MissionType.CHECKPOINT_PREPARATION,
    }
)


@dataclass(frozen=True, slots=True)
class MergedRecommendationGroup:
    """One coherent group of recommendations destined for a single mission."""

    intent: MissionIntent
    recommendations: tuple[Recommendation, ...]


class MergeRules:
    """Merge similar recommendations into coherent mission groups.

    Merge key: mission_type + subject_id + competency_id (for mergeable types).
    Prerequisite and mixed-practice missions never merge with others.
    """

    @staticmethod
    def merge_key(intent: MissionIntent) -> tuple[str, str, str] | None:
        if intent.mission_type not in _MERGEABLE_TYPES:
            return None
        if intent.mission_type is MissionType.REVISE_PREREQUISITE:
            return None
        return (
            intent.mission_type.value,
            intent.subject_id or "-",
            intent.competency_id or "-",
        )

    @staticmethod
    def merge_similar_recommendations(
        recommendations: Sequence[Recommendation],
    ) -> tuple[MergedRecommendationGroup, ...]:
        """Group mergeable recommendations; preserve encounter order of keys."""
        groups: dict[
            tuple[str, str, str], list[tuple[Recommendation, MissionIntent]]
        ] = {}
        singles: list[tuple[Recommendation, MissionIntent]] = []
        key_order: list[tuple[str, str, str]] = []

        for recommendation in recommendations:
            intent = MappingRules.resolve(recommendation)
            if intent is None:
                continue
            key = MergeRules.merge_key(intent)
            if key is None:
                singles.append((recommendation, intent))
                continue
            if key not in groups:
                groups[key] = []
                key_order.append(key)
            groups[key].append((recommendation, intent))

        result: list[MergedRecommendationGroup] = []
        for key in key_order:
            members = groups[key]
            result.append(MergeRules._collapse(members))
        for recommendation, intent in singles:
            result.append(
                MergedRecommendationGroup(
                    intent=intent,
                    recommendations=(recommendation,),
                )
            )
        return tuple(result)

    @staticmethod
    def _collapse(
        members: list[tuple[Recommendation, MissionIntent]],
    ) -> MergedRecommendationGroup:
        recommendations = tuple(item[0] for item in members)
        intents = tuple(item[1] for item in members)
        primary = intents[0]
        priority = max(intent.priority_magnitude for intent in intents)
        source_ids = tuple(
            rid
            for intent in intents
            for rid in intent.source_recommendation_ids
        )
        # Same-subject multi-type merges become mixed practice when types differ.
        types = {intent.mission_type for intent in intents}
        mission_type = primary.mission_type
        if len(types) > 1:
            mission_type = MissionType.MIXED_PRACTICE
        # Prefer the strongest recurrence signal in the group.
        recurrence = primary.recurrence
        for intent in intents[1:]:
            if intent.recurrence is MissionRecurrenceBand.INCREASED:
                recurrence = intent.recurrence
                break
        merged_intent = MissionIntent(
            mission_type=mission_type,
            objective_code=MappingRules.objective_code_for(mission_type),
            step_action=MappingRules.step_action_for(mission_type),
            recurrence=recurrence,
            subject_id=primary.subject_id,
            competency_id=primary.competency_id,
            priority_magnitude=priority,
            source_recommendation_ids=source_ids,
        )
        return MergedRecommendationGroup(
            intent=merged_intent,
            recommendations=recommendations,
        )
