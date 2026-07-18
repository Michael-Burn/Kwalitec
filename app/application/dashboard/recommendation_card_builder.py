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
    ActionFamily.STUDY: "Start Study Session",
    ActionFamily.REVISE: "Continue Studying",
    ActionFamily.ASSESS: "Start Study Session",
    ActionFamily.DIAGNOSTIC: "Start Study Session",
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
    # EIP-003 claim-type fields (presentation only)
    observed_facts: tuple[str, ...] = ()
    estimates: tuple[str, ...] = ()
    educational_advice: str | None = None
    next_action: str | None = None


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
        narrative = _claim_narrative(recommendation)
        return RecommendationCardViewModel(
            title=_title(recommendation),
            subtitle=_subtitle(recommendation),
            primary_action=_primary_action(recommendation),
            estimated_duration=_estimated_duration(recommendation),
            reason_summary=narrative["reason_summary"],
            warning=warning,
            show_explanation=_show_explanation(experience),
            show_start_button=_show_start_button(recommendation),
            observed_facts=narrative["observed_facts"],
            estimates=narrative["estimates"],
            educational_advice=narrative["educational_advice"],
            next_action=narrative["next_action"],
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
        "Suggested: continue with the next useful topic on your study plan. "
        "This coaching supports Learning Mode — it does not replace Today's Study Session."
    ),
    ActionFamily.REVISE: (
        "Suggested: revisit material you have already started so it stays fresher. "
        "Optional review advice does not replace Today's Study Session."
    ),
    ActionFamily.ASSESS: (
        "Suggested: a short practice check to clarify what still needs work. "
        "Checks inform estimates — they do not create Estimated Knowledge by themselves."
    ),
    ActionFamily.DIAGNOSTIC: (
        "Suggested: a short check to identify the most useful next study step. "
        "This is advisory guidance alongside your study plan."
    ),
    ActionFamily.REST_PROTECT_INTENSITY: (
        "Suggested: a lighter day today to support steady, sustainable progress. "
        "Based on recent study load patterns — not a prediction of burnout."
    ),
}

_DEFAULT_STUDENT_REASON = (
    "Suggested: take the most useful next step on your study plan. "
    "This is educational advice — Today's Study Session still follows Learning Mode."
)

_OBSERVED_BY_FAMILY: dict[ActionFamily, str] = {
    ActionFamily.STUDY: (
        "You have an active study plan guiding syllabus order in Learning Mode."
    ),
    ActionFamily.REVISE: (
        "You have already started material that can benefit from another pass."
    ),
    ActionFamily.ASSESS: (
        "You have completed recent study activity that a short check can build on."
    ),
    ActionFamily.DIAGNOSTIC: (
        "You have completed valuable study activities on your active plan."
    ),
    ActionFamily.REST_PROTECT_INTENSITY: (
        "Recent study activity shows a heavier load than usual."
    ),
}

_ESTIMATE_BY_FAMILY: dict[ActionFamily, str] = {
    ActionFamily.STUDY: (
        "Estimated: continuing syllabus order is currently the most useful focus."
    ),
    ActionFamily.REVISE: (
        "Estimated: revisiting started material will strengthen what you retain."
    ),
    ActionFamily.ASSESS: (
        "Estimated: a practice check will clarify what to practise next."
    ),
    ActionFamily.DIAGNOSTIC: (
        "Estimated: a short diagnostic check will identify the next useful step."
    ),
    ActionFamily.REST_PROTECT_INTENSITY: (
        "Estimated: a lighter day supports lasting progress more than pushing harder."
    ),
}

_NEXT_BY_FAMILY: dict[ActionFamily, str] = {
    ActionFamily.STUDY: (
        "Open Today's Study Session to continue your Current Learning Topic."
    ),
    ActionFamily.REVISE: (
        "Continue studying today; treat review as optional coaching."
    ),
    ActionFamily.ASSESS: (
        "Start today's session, then use a short practice check if useful."
    ),
    ActionFamily.DIAGNOSTIC: (
        "Start today's session and complete the suggested short check."
    ),
    ActionFamily.REST_PROTECT_INTENSITY: (
        "Choose a lighter session or rest, then return tomorrow."
    ),
}


def _claim_narrative(recommendation: Recommendation) -> dict[str, object]:
    """EIP-003 claim types for the Recommendation card (educational speech only)."""
    family = recommendation.suggestion.family
    reason = _STUDENT_REASON_BY_FAMILY.get(family, _DEFAULT_STUDENT_REASON)
    observed = _OBSERVED_BY_FAMILY.get(
        family,
        "Your active study plan guides today's educational focus.",
    )
    estimate = _ESTIMATE_BY_FAMILY.get(family)
    next_action = _NEXT_BY_FAMILY.get(
        family,
        "Open Today's Study Session to take the next clear step.",
    )
    estimates: tuple[str, ...] = (estimate,) if estimate else ()
    return {
        "reason_summary": reason,
        "observed_facts": (observed,),
        "estimates": estimates,
        "educational_advice": reason,
        "next_action": next_action,
    }


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
