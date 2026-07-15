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

# Student-facing action labels — educational intent only (never domain enum text).
_FAMILY_TITLE: dict[ActionFamily, str] = {
    ActionFamily.STUDY: "Continue studying",
    ActionFamily.REVISE: "Review and strengthen",
    ActionFamily.ASSESS: "Check your understanding",
    ActionFamily.DIAGNOSTIC: "Find your next focus",
    ActionFamily.REST_PROTECT_INTENSITY: "Protect today's study energy",
}

_FAMILY_SUBTITLE: dict[ActionFamily, str] = {
    ActionFamily.STUDY: "The next useful step on your active study plan",
    ActionFamily.REVISE: "Reinforce material you have already started",
    ActionFamily.ASSESS: "See what has stuck and what still needs practice",
    ActionFamily.DIAGNOSTIC: "A short check to guide today's recommendation",
    ActionFamily.REST_PROTECT_INTENSITY: "A lighter day supports lasting progress",
}

_FAMILY_PRIMARY_ACTION: dict[ActionFamily, str] = {
    ActionFamily.STUDY: "Start Today's Session",
    ActionFamily.REVISE: "Continue Studying",
    ActionFamily.ASSESS: "Start Today's Session",
    ActionFamily.DIAGNOSTIC: "Start Today's Session",
    ActionFamily.REST_PROTECT_INTENSITY: "Take a Lighter Session",
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
    """Educational title from Decision-selected family — no re-selection."""
    family = recommendation.suggestion.family
    return _FAMILY_TITLE.get(family, "Today's recommended focus")


def _subtitle(recommendation: Recommendation) -> str | None:
    """Educational situating line — never dump ids, intent enums, or tags.

    ``curriculum_entity_id`` is an internal syllabus key (often a numeric PK).
    ``intent.value`` is domain vocabulary (e.g. ``evidence_creating``). Neither
    belongs on a student surface.
    """
    family = recommendation.suggestion.family
    return _FAMILY_SUBTITLE.get(family)


def _primary_action(recommendation: Recommendation) -> str | None:
    """Primary CTA label projected from selected family — not a new action."""
    if AffordanceOutcome.ACCEPT not in recommendation.affordances.outcomes:
        return None
    family = recommendation.suggestion.family
    return _FAMILY_PRIMARY_ACTION.get(family, "Continue Studying")


def _estimated_duration(recommendation: Recommendation) -> str | None:
    """Student-facing duration hint — never dump internal feasibility tags."""
    tags = recommendation.urgency_duration_tags
    if not tags:
        return None
    # Internal tags (feasibility/*, constraint/*, *duration*) stay in the
    # Recommendation warrant; Internal Alpha UI shows no raw diagnostic strings.
    return None


_STUDENT_REASON_BY_FAMILY: dict[ActionFamily, str] = {
    ActionFamily.STUDY: (
        "Based on your recent progress, this is the most useful next topic "
        "on your study plan."
    ),
    ActionFamily.REVISE: (
        "Based on your recent study activity, revisiting this material will "
        "strengthen what you have already started."
    ),
    ActionFamily.ASSESS: (
        "Based on your recent progress, a short practice check will clarify "
        "what to focus on next."
    ),
    ActionFamily.DIAGNOSTIC: (
        "You've completed valuable study activities. A short check now will "
        "help identify the most useful next step."
    ),
    ActionFamily.REST_PROTECT_INTENSITY: (
        "Based on your recent study load, a lighter day today supports "
        "steady, sustainable progress."
    ),
}

_DEFAULT_STUDENT_REASON = (
    "Based on your recent progress, this is the most useful next step "
    "on your study plan."
)


def _reason_summary(recommendation: Recommendation) -> str | None:
    """Concise student explanation — never expose internal warrant note tags."""
    if not recommendation.reasons:
        return _DEFAULT_STUDENT_REASON
    family = recommendation.suggestion.family
    return _STUDENT_REASON_BY_FAMILY.get(family, _DEFAULT_STUDENT_REASON)


def _compose_warning(
    *,
    experience_warnings: tuple[str, ...],
    recommendation: Recommendation,
) -> str | None:
    """Keep thin-warrant honesty internal — do not render diagnostic tags in UI.

    Domain warnings and confidence postures remain on the Recommendation /
    Experience for explainability consumers. The Internal Alpha dashboard
    card must never surface tags such as ``cold_start`` or ``thin_warrant``.
    """
    del experience_warnings, recommendation
    return None


def _show_explanation(experience: EducationalExperience) -> bool:
    """True when explainability cargo is present on the Experience."""
    return experience.explainability.explanation_chain is not None


def _show_start_button(recommendation: Recommendation) -> bool:
    """True when accept affordance exists — no dead-button theatre when absent."""
    return AffordanceOutcome.ACCEPT in recommendation.affordances.outcomes
