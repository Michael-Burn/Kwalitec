"""Completion mapping — completion summary and next-step chrome.

Forwards already-decided workspace completion actions and recommendation
summaries into runner view snippets. Does not decide what happens next.
"""

from __future__ import annotations

from presentation.design_system import (
    RecommendationCard,
    primary_button,
)
from presentation.mission_workspace.workspace_view_model import (
    CompletionActionView,
    MissionWorkspaceViewModel,
    RecommendationSummaryView,
)
from presentation.study_session.session_view_model import (
    CompletionSummaryView,
    NextStepView,
)

_DEFAULT_COMPLETION_HEADLINE = "Completion"
_DEFAULT_COMPLETION_DETAIL = (
    "Complete the session checks when you are ready, then choose a next step."
)
_DEFAULT_NEXT_HEADLINE = "Next step"
_DEFAULT_NEXT_DETAIL = "No next-step guidance is available yet."
_DEFAULT_ACTION_LABEL = "Return Home"
_DEFAULT_ACTION_KEY = "return_home"


class CompletionMapper:
    """Map workspace completion / recommendation fields into runner views."""

    @classmethod
    def map_completion(
        cls,
        workspace: MissionWorkspaceViewModel | None,
    ) -> CompletionSummaryView:
        """Project completion actions into a ``CompletionSummaryView``."""
        if workspace is None:
            return CompletionSummaryView(
                headline=_DEFAULT_COMPLETION_HEADLINE,
                detail=_DEFAULT_COMPLETION_DETAIL,
                checklist=(),
                actions=(
                    CompletionActionView(
                        label=_DEFAULT_ACTION_LABEL,
                        detail="Return when you are ready to continue.",
                        action_key=_DEFAULT_ACTION_KEY,
                    ),
                ),
            )

        actions = tuple(workspace.completion_actions or ())
        checklist = tuple(
            action.detail or action.label
            for action in actions
            if action.action_key != "return_home"
            and (action.detail or action.label)
        )
        if not checklist:
            checklist = tuple(
                action.label for action in actions if action.label
            )

        primary = _primary_non_home(actions)
        if primary is not None:
            headline = primary.label or _DEFAULT_COMPLETION_HEADLINE
            detail = primary.detail or _DEFAULT_COMPLETION_DETAIL
        else:
            headline = _DEFAULT_COMPLETION_HEADLINE
            detail = _DEFAULT_COMPLETION_DETAIL

        if not actions:
            actions = (
                CompletionActionView(
                    label=_DEFAULT_ACTION_LABEL,
                    detail="Return to Home when you are finished.",
                    action_key=_DEFAULT_ACTION_KEY,
                ),
            )

        return CompletionSummaryView(
            headline=headline,
            detail=detail,
            checklist=checklist,
            actions=actions,
        )

    @classmethod
    def map_next_step(
        cls,
        workspace: MissionWorkspaceViewModel | None,
    ) -> NextStepView:
        """Project recommendation / completion CTA into a ``NextStepView``."""
        if workspace is None:
            return cls._empty_next_step()

        recommendation = workspace.recommendation_summary
        actions = tuple(workspace.completion_actions or ())
        primary = _primary_non_home(actions)

        headline = _text(
            getattr(recommendation, "headline", None),
            fallback=_DEFAULT_NEXT_HEADLINE,
        )
        detail = _text(
            getattr(recommendation, "detail", None),
            fallback=_DEFAULT_NEXT_DETAIL,
        )
        category = _text(getattr(recommendation, "category_label", None))
        expected = _text(getattr(recommendation, "expected_outcome", None))
        if expected and expected not in detail:
            detail = f"{detail} {expected}".strip()

        action_label = (
            primary.label
            if primary is not None and primary.label
            else _DEFAULT_ACTION_LABEL
        )
        action_key = (
            primary.action_key
            if primary is not None and primary.action_key
            else _DEFAULT_ACTION_KEY
        )
        if primary is not None and primary.detail and not _has_recommendation(
            recommendation
        ):
            detail = primary.detail

        card = RecommendationCard(
            title=headline or _DEFAULT_NEXT_HEADLINE,
            body=detail or _DEFAULT_NEXT_DETAIL,
            eyebrow="Next step",
            reason_label=detail,
            category_label=category,
        )
        button = primary_button(action_label)
        return NextStepView(
            headline=headline or _DEFAULT_NEXT_HEADLINE,
            detail=detail or _DEFAULT_NEXT_DETAIL,
            category_label=category,
            action_key=action_key,
            action_label=action_label,
            card=card,
            primary_button=button,
        )

    @classmethod
    def completion_section_body(cls, completion: CompletionSummaryView) -> str:
        """Format completion summary into a section body string."""
        parts: list[str] = []
        if completion.detail:
            parts.append(completion.detail)
        for item in completion.checklist:
            if item and item not in parts:
                parts.append(item)
        return "\n".join(parts) if parts else _DEFAULT_COMPLETION_DETAIL

    @classmethod
    def _empty_next_step(cls) -> NextStepView:
        card = RecommendationCard(
            title=_DEFAULT_NEXT_HEADLINE,
            body=_DEFAULT_NEXT_DETAIL,
            eyebrow="Next step",
            reason_label=_DEFAULT_NEXT_DETAIL,
            category_label="",
        )
        return NextStepView(
            headline=_DEFAULT_NEXT_HEADLINE,
            detail=_DEFAULT_NEXT_DETAIL,
            category_label="",
            action_key=_DEFAULT_ACTION_KEY,
            action_label=_DEFAULT_ACTION_LABEL,
            card=card,
            primary_button=primary_button(_DEFAULT_ACTION_LABEL),
        )


def _primary_non_home(
    actions: tuple[CompletionActionView, ...],
) -> CompletionActionView | None:
    for action in actions:
        if action.action_key and action.action_key != "return_home":
            return action
    return None


def _has_recommendation(recommendation: RecommendationSummaryView | None) -> bool:
    if recommendation is None:
        return False
    detail = _text(getattr(recommendation, "detail", None))
    return bool(detail) and detail != _DEFAULT_NEXT_DETAIL


def _text(value: str | None, *, fallback: str = "") -> str:
    if value is None:
        return fallback
    cleaned = str(value).strip()
    return cleaned if cleaned else fallback
