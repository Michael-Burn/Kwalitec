"""Predefined recommendation wording templates (FOS-006).

Decision logic lives in rules. User-facing text lives here.
No natural-language generation beyond these fixed strings.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.founder.recommendations.config import (
    TEMPLATE_PAUSE_FOR_ENGINEERING_HEALTH,
    TEMPLATE_PRIORITISE_RECURRING_ISSUES,
    TEMPLATE_RESOLVE_ARCHIVE_INCONSISTENCIES,
    TEMPLATE_SELECT_ROADMAP_CAPABILITY,
    TEMPLATE_WAIT_FOR_INTERNAL_ALPHA,
)


@dataclass(frozen=True)
class RecommendationTemplate:
    """Fixed title / explanation / rationale for one template id."""

    template_id: str
    title: str
    explanation: str
    rationale: str


# Version 1 catalog — advisory wording only.
RECOMMENDATION_TEMPLATES: dict[str, RecommendationTemplate] = {
    TEMPLATE_WAIT_FOR_INTERNAL_ALPHA: RecommendationTemplate(
        template_id=TEMPLATE_WAIT_FOR_INTERNAL_ALPHA,
        title="Wait for Internal Alpha before releasing",
        explanation=(
            "No Internal Alpha feedback is present in the current operational "
            "snapshot. Release decisions should wait until Internal Alpha has "
            "produced feedback for the week."
        ),
        rationale=(
            "Internal Alpha is the primary user-signal gate before release. "
            "Proceeding without feedback removes founder visibility into "
            "recurring product issues."
        ),
    ),
    TEMPLATE_RESOLVE_ARCHIVE_INCONSISTENCIES: RecommendationTemplate(
        template_id=TEMPLATE_RESOLVE_ARCHIVE_INCONSISTENCIES,
        title="Resolve archive inconsistencies",
        explanation=(
            "The Capability Archive reports one or more inconsistencies. "
            "Resolve archive validation failures before treating inventory "
            "counts as authoritative."
        ),
        rationale=(
            "Archive inconsistencies undermine capability and release "
            "summaries in the operational snapshot."
        ),
    ),
    TEMPLATE_PAUSE_FOR_ENGINEERING_HEALTH: RecommendationTemplate(
        template_id=TEMPLATE_PAUSE_FOR_ENGINEERING_HEALTH,
        title="Pause new capabilities and improve engineering quality",
        explanation=(
            "Engineering health is below the Version 1 threshold (failing "
            "tests and/or validation errors). Pause starting new capabilities "
            "until engineering quality is restored."
        ),
        rationale=(
            "Adding capabilities on a failing engineering base increases "
            "risk and obscures whether new work improves product quality."
        ),
    ),
    TEMPLATE_PRIORITISE_RECURRING_ISSUES: RecommendationTemplate(
        template_id=TEMPLATE_PRIORITISE_RECURRING_ISSUES,
        title="Prioritise recurring user issues",
        explanation=(
            "Duplicate Internal Alpha feedback is high relative to Version 1 "
            "thresholds. Focus the next founder cycle on recurring user "
            "issues rather than one-off requests."
        ),
        rationale=(
            "High duplicate rates indicate concentrated pain points; fixing "
            "them yields higher learning and product leverage."
        ),
    ),
    TEMPLATE_SELECT_ROADMAP_CAPABILITY: RecommendationTemplate(
        template_id=TEMPLATE_SELECT_ROADMAP_CAPABILITY,
        title="Select highest-priority roadmap capability",
        explanation=(
            "No capabilities are currently active. Select the highest-"
            "priority roadmap capability and mark it active to restore "
            "forward progress."
        ),
        rationale=(
            "An empty active set stalls Founder OS delivery. Choosing one "
            "roadmap capability re-establishes a clear execution focus."
        ),
    ),
}
