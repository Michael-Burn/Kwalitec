"""Deterministic section templates for Founder Weekly Briefing (FOS-007).

Every string is predefined. Values are interpolated from
FounderOperationalState and RecommendationSet only — no free-form NLG.
"""

from __future__ import annotations

from app.founder.briefing.config import (
    RISK_PRIORITIES,
    SECTION_CAPABILITY,
    SECTION_ENGINEERING,
    SECTION_EXECUTIVE_SUMMARY,
    SECTION_INTERNAL_ALPHA,
    SECTION_NEXT_WEEK,
    SECTION_PRIORITIES,
    SECTION_RECOMMENDATIONS,
    SECTION_RELEASE,
    SECTION_RISKS,
    TOP_PRIORITY_LIMIT,
)
from app.founder.briefing.models import BriefSection
from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.models import Recommendation, RecommendationSet


def _format_bool(value: bool) -> str:
    return "pass" if value else "fail"


def _format_category_counts(state: FounderOperationalState) -> str:
    counts = state.internal_alpha.category_counts
    if not counts:
        return "none"
    parts = [f"{key}={counts[key]}" for key in sorted(counts)]
    return ", ".join(parts)


def _top_recommendations(
    recommendation_set: RecommendationSet, limit: int = TOP_PRIORITY_LIMIT
) -> tuple[Recommendation, ...]:
    return recommendation_set.recommendations[:limit]


def _bullet_list(lines: list[str]) -> str:
    if not lines:
        return "- None"
    return "\n".join(f"- {line}" for line in lines)


def build_executive_summary(
    state: FounderOperationalState,
    recommendation_set: RecommendationSet,
    *,
    order: int = 1,
) -> BriefSection:
    """Template 1 — Executive Summary."""
    rec_count = len(recommendation_set.recommendations)
    content = (
        f"Week: {state.internal_alpha.current_week}. "
        f"Overall status: {recommendation_set.overall_status}. "
        f"Recommendations: {rec_count}. "
        f"Engineering tests: {_format_bool(state.engineering.tests_pass)}. "
        f"Active capabilities: {state.capability.active_count}. "
        f"Internal Alpha feedback: {state.internal_alpha.feedback_count}. "
        f"Current release: {state.release.current_release}."
    )
    return BriefSection(
        title=SECTION_EXECUTIVE_SUMMARY,
        content=content,
        order=order,
    )


def build_engineering_overview(
    state: FounderOperationalState,
    recommendation_set: RecommendationSet,
    *,
    order: int = 2,
) -> BriefSection:
    """Template 2 — Engineering Overview."""
    del recommendation_set  # Inputs are fixed; section uses state only.
    eng = state.engineering
    knowledge = state.knowledge
    content = (
        f"Standards count: {eng.standards_count}. "
        f"Tests: {_format_bool(eng.tests_pass)}. "
        f"Validation errors: {eng.validation_errors}. "
        f"Knowledge artefacts indexed: {knowledge.indexed_artefacts}. "
        f"Architecture documents: {knowledge.architecture_documents}. "
        f"Research documents: {knowledge.research_documents}."
    )
    return BriefSection(
        title=SECTION_ENGINEERING,
        content=content,
        order=order,
    )


def build_internal_alpha_overview(
    state: FounderOperationalState,
    recommendation_set: RecommendationSet,
    *,
    order: int = 3,
) -> BriefSection:
    """Template 3 — Internal Alpha Overview."""
    del recommendation_set
    alpha = state.internal_alpha
    recent = ", ".join(alpha.recent_week_labels) if alpha.recent_week_labels else "none"
    content = (
        f"Current week: {alpha.current_week}. "
        f"Feedback count: {alpha.feedback_count}. "
        f"Duplicate count: {alpha.duplicate_count}. "
        f"Category counts: {_format_category_counts(state)}. "
        f"Recent weeks: {recent}."
    )
    return BriefSection(
        title=SECTION_INTERNAL_ALPHA,
        content=content,
        order=order,
    )


def build_capability_progress(
    state: FounderOperationalState,
    recommendation_set: RecommendationSet,
    *,
    order: int = 4,
) -> BriefSection:
    """Template 4 — Capability Progress."""
    del recommendation_set
    cap = state.capability
    recent = (
        ", ".join(cap.recent_capability_ids) if cap.recent_capability_ids else "none"
    )
    content = (
        f"Total capabilities: {cap.total_count}. "
        f"Completed: {cap.completed_count}. "
        f"Active: {cap.active_count}. "
        f"Archive inconsistencies: {cap.archive_inconsistencies}. "
        f"Recent capability ids: {recent}."
    )
    return BriefSection(
        title=SECTION_CAPABILITY,
        content=content,
        order=order,
    )


def build_release_readiness(
    state: FounderOperationalState,
    recommendation_set: RecommendationSet,
    *,
    order: int = 5,
) -> BriefSection:
    """Template 5 — Release Readiness."""
    release = state.release
    status = recommendation_set.overall_status
    content = (
        f"Current release: {release.current_release}. "
        f"Completed capabilities: {release.completed_capabilities}. "
        f"Recommendation overall status: {status}. "
        f"Engineering tests: {_format_bool(state.engineering.tests_pass)}. "
        f"Archive inconsistencies: {state.capability.archive_inconsistencies}."
    )
    return BriefSection(
        title=SECTION_RELEASE,
        content=content,
        order=order,
    )


def build_top_priorities(
    state: FounderOperationalState,
    recommendation_set: RecommendationSet,
    *,
    order: int = 6,
) -> BriefSection:
    """Template 6 — Top Priorities."""
    del state
    top = _top_recommendations(recommendation_set)
    if not top:
        lines = ["No active priorities (recommendation set is empty)."]
    else:
        lines = [
            f"[{item.priority}] {item.title} ({item.id})" for item in top
        ]
    return BriefSection(
        title=SECTION_PRIORITIES,
        content=_bullet_list(lines),
        order=order,
    )


def build_recommendation_summary(
    state: FounderOperationalState,
    recommendation_set: RecommendationSet,
    *,
    order: int = 7,
) -> BriefSection:
    """Template 7 — Recommendation Summary."""
    del state
    count = len(recommendation_set.recommendations)
    header = (
        f"Overall status: {recommendation_set.overall_status}. "
        f"Count: {count}."
    )
    if not recommendation_set.recommendations:
        body = "- No recommendations."
    else:
        body = _bullet_list(
            [
                f"[{item.priority}] {item.id}: {item.title}"
                for item in recommendation_set.recommendations
            ]
        )
    return BriefSection(
        title=SECTION_RECOMMENDATIONS,
        content=f"{header}\n{body}",
        order=order,
    )


def build_risks(
    state: FounderOperationalState,
    recommendation_set: RecommendationSet,
    *,
    order: int = 8,
) -> BriefSection:
    """Template 8 — Risks (Critical and High recommendations only)."""
    del state
    risks = [
        item
        for item in recommendation_set.recommendations
        if item.priority in RISK_PRIORITIES
    ]
    if not risks:
        lines = ["No Critical or High risks reported."]
    else:
        lines = [
            f"[{item.priority}] {item.title}: {item.explanation}" for item in risks
        ]
    return BriefSection(
        title=SECTION_RISKS,
        content=_bullet_list(lines),
        order=order,
    )


def build_next_week_focus(
    state: FounderOperationalState,
    recommendation_set: RecommendationSet,
    *,
    order: int = 9,
) -> BriefSection:
    """Template 9 — Next Week Focus."""
    top = _top_recommendations(recommendation_set)
    if not top:
        focus_lines = [
            "Maintain current healthy posture; select next roadmap capability "
            f"when ready (active capabilities: {state.capability.active_count})."
        ]
    else:
        focus_lines = [
            f"Address: {item.title} [{item.priority}]" for item in top
        ]
    week = state.internal_alpha.current_week
    content = f"Focus for week following {week}:\n{_bullet_list(focus_lines)}"
    return BriefSection(
        title=SECTION_NEXT_WEEK,
        content=content,
        order=order,
    )


SECTION_BUILDERS: tuple = (
    build_executive_summary,
    build_engineering_overview,
    build_internal_alpha_overview,
    build_capability_progress,
    build_release_readiness,
    build_top_priorities,
    build_recommendation_summary,
    build_risks,
    build_next_week_focus,
)
