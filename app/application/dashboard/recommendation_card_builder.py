"""Recommendation Card builder — Stage A dashboard presentation projection.

Maps an Educational Experience into a RecommendationCardViewModel for the
dashboard Recommendation card path.

Owns presentation shaping only. Never scores readiness, selects next actions,
re-ranks Recommendations, alters Decisions or Missions, mutates Twin, or
imports Flask / routes / templates / ORM.

Gated by ``ENABLE_EI_RECOMMENDATIONS``. When the flag is off, returns ``None``
so legacy dashboard behaviour remains unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.config.feature_flags import (
    FEATURE_FLAGS,
    EducationalIntelligenceFeatureFlags,
)
from app.application.orchestration.educational_orchestrator import (
    EducationalExperience,
)
from app.domain.decision.action_types import ActionFamily
from app.domain.recommendation.affordances import AffordanceOutcome
from app.domain.recommendation.recommendation import Recommendation
from app.domain.recommendation.warrant import (
    THIN_WARRANT_CONFIDENCE_POSTURES,
    RecommendationConfidencePosture,
)

# Presentation labels for Decision-selected action families — display only.
_FAMILY_TITLE: dict[ActionFamily, str] = {
    ActionFamily.STUDY: "Study",
    ActionFamily.REVISE: "Revise",
    ActionFamily.ASSESS: "Assess",
    ActionFamily.DIAGNOSTIC: "Diagnostic",
    ActionFamily.REST_PROTECT_INTENSITY: "Protect intensity",
}

_FAMILY_PRIMARY_ACTION: dict[ActionFamily, str] = {
    ActionFamily.STUDY: "Start study",
    ActionFamily.REVISE: "Start revision",
    ActionFamily.ASSESS: "Start assessment",
    ActionFamily.DIAGNOSTIC: "Start diagnostic",
    ActionFamily.REST_PROTECT_INTENSITY: "Protect intensity",
}


@dataclass(frozen=True)
class RecommendationCardViewModel:
    """Dashboard Recommendation card presentation data only.

    Must never carry Decision, Recommendation, Mission, or Twin domain objects.
    """

    title: str
    subtitle: str | None
    primary_action: str | None
    estimated_duration: str | None
    reason_summary: str | None
    warning: str | None
    show_explanation: bool
    show_start_button: bool


class RecommendationCardBuilder:
    """Assemble RecommendationCardViewModel from Educational Experience.

    Presentation assembler (Application Layer). Reads domain packaging already
    composed into the Experience Contract; does not author educational meaning.
    """

    @staticmethod
    def build(
        experience: EducationalExperience,
        *,
        flags: EducationalIntelligenceFeatureFlags | None = None,
    ) -> RecommendationCardViewModel | None:
        """Project Today's Recommendation into a dashboard card ViewModel.

        Args:
            experience: Composed Educational Experience Contract snapshot.
            flags: Optional flag snapshot for tests / staged rollout.
                Defaults to the Application Layer ``FEATURE_FLAGS`` singleton.

        Returns:
            Immutable presentation ViewModel when ``ENABLE_EI_RECOMMENDATIONS``
            is True; ``None`` when the flag is off (legacy path unchanged).
        """
        active = flags if flags is not None else FEATURE_FLAGS
        if not active.ENABLE_EI_RECOMMENDATIONS:
            return None

        recommendation = experience.todays_recommendation
        warning = _compose_warning(
            experience_warnings=experience.warnings,
            recommendation=recommendation,
        )
        return RecommendationCardViewModel(
            title=_title(recommendation),
            subtitle=_subtitle(recommendation),
            primary_action=_primary_action(recommendation),
            estimated_duration=_estimated_duration(recommendation),
            reason_summary=_reason_summary(recommendation),
            warning=warning,
            show_explanation=_show_explanation(experience),
            show_start_button=_show_start_button(recommendation),
        )


def _title(recommendation: Recommendation) -> str:
    """Presentation title from Decision-selected action family — no re-selection."""
    family = recommendation.suggestion.family
    return _FAMILY_TITLE.get(family, family.value)


def _subtitle(recommendation: Recommendation) -> str | None:
    """Situating subtitle from curriculum scope and intent tags — display only."""
    suggestion = recommendation.suggestion
    parts: list[str] = []
    if suggestion.curriculum_entity_id:
        parts.append(suggestion.curriculum_entity_id)
    intent_value = suggestion.intent.value
    if intent_value and intent_value not in parts:
        parts.append(intent_value)
    if not parts:
        return None
    return " · ".join(parts)


def _primary_action(recommendation: Recommendation) -> str | None:
    """Primary CTA label projected from selected family — not a new action."""
    if AffordanceOutcome.ACCEPT not in recommendation.affordances.outcomes:
        return None
    family = recommendation.suggestion.family
    return _FAMILY_PRIMARY_ACTION.get(family, "Start")


def _estimated_duration(recommendation: Recommendation) -> str | None:
    """Forward Decision-derived duration / feasibility tags — never invent minutes."""
    tags = recommendation.urgency_duration_tags
    if not tags:
        return None
    duration_related = tuple(
        tag
        for tag in tags
        if "duration" in tag
        or tag.startswith("feasibility/")
        or tag.startswith("constraint/")
    )
    if not duration_related:
        return None
    return ", ".join(duration_related)


def _reason_summary(recommendation: Recommendation) -> str | None:
    """Short reason summary from Recommendation Reasons — narration already authored."""
    if not recommendation.reasons:
        return None
    primary = recommendation.reasons[0]
    notes = tuple(primary.note_tags)
    if notes:
        return ", ".join(notes)
    return primary.reason_id


def _compose_warning(
    *,
    experience_warnings: tuple[str, ...],
    recommendation: Recommendation,
) -> str | None:
    """Propagate honesty / thin-warrant signals — never upgrade warrant."""
    tags: list[str] = list(experience_warnings)
    confidence = recommendation.confidence_posture
    if confidence in THIN_WARRANT_CONFIDENCE_POSTURES:
        confidence_tag = f"confidence:{confidence.value}"
        if confidence_tag not in tags:
            tags.append(confidence_tag)
    if confidence is RecommendationConfidencePosture.COLD_START:
        if "cold_start" not in tags:
            tags.append("cold_start")
    if not tags:
        return None
    return "; ".join(tags)


def _show_explanation(experience: EducationalExperience) -> bool:
    """True when explainability cargo is present on the Experience."""
    return experience.explainability.explanation_chain is not None


def _show_start_button(recommendation: Recommendation) -> bool:
    """True when accept affordance exists — no dead-button theatre when absent."""
    return AffordanceOutcome.ACCEPT in recommendation.affordances.outcomes
