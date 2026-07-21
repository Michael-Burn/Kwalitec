"""Mission card mapping — today's mission and reason chrome.

Forwards already-decided workspace / pipeline mission fields into Design
System cards. Does not select missions, rewrite objectives, or invent reasons.
"""

from __future__ import annotations

from typing import Any

from presentation.design_system import MissionCard, RecommendationCard
from presentation.mission_workspace.workspace_view_model import (
    MissionWorkspaceViewModel,
)

_DEFAULT_TITLE = "Today's Mission"
_DEFAULT_BODY = "Your mission for today will appear here when available."
_DEFAULT_DURATION = "Duration not available"
_DEFAULT_STATUS = "Ready when you are"
_DEFAULT_REASON_TITLE = "Why this mission"
_DEFAULT_REASON_BODY = "Mission guidance will appear here when available."


class MissionCardMapper:
    """Map workspace / pipeline mission fields into dashboard mission chrome."""

    @classmethod
    def map_mission_card(
        cls,
        workspace: MissionWorkspaceViewModel | None,
        *,
        result: Any = None,
    ) -> MissionCard:
        """Project today's mission into a ``MissionCard``."""
        title = _text(
            getattr(workspace, "mission_title", None),
            fallback=_DEFAULT_TITLE,
        )
        body = _text(
            getattr(workspace, "mission_objective", None),
            fallback=_DEFAULT_BODY,
        )
        duration = _text(
            getattr(workspace, "estimated_duration", None),
            fallback=_DEFAULT_DURATION,
        )
        session_progress = (
            getattr(workspace, "session_progress", None) if workspace else None
        )
        progress_summary = (
            getattr(workspace, "progress_summary", None) if workspace else None
        )
        status = _text(
            getattr(session_progress, "progress_label", None)
            or getattr(progress_summary, "headline", None),
            fallback=_DEFAULT_STATUS,
        )

        if title == _DEFAULT_TITLE and result is not None:
            mission = getattr(result, "mission", None)
            objective = getattr(mission, "objective", None) if mission else None
            statement = _text(getattr(objective, "statement", None))
            if statement:
                title = _first_sentence(statement) or title
                if body == _DEFAULT_BODY:
                    body = statement

        return MissionCard(
            title=title,
            body=body,
            eyebrow="Today's Mission",
            duration_label=duration,
            status_label=status,
        )

    @classmethod
    def map_mission_reason(
        cls,
        workspace: MissionWorkspaceViewModel | None,
        *,
        result: Any = None,
    ) -> RecommendationCard:
        """Project mission explanation / recommendation reason into a card."""
        explanation = _text(getattr(workspace, "mission_explanation", None))
        recommendation = (
            getattr(workspace, "recommendation_summary", None) if workspace else None
        )
        reason_detail = _text(getattr(recommendation, "detail", None))
        category = _text(getattr(recommendation, "category_label", None))
        headline = _text(
            getattr(recommendation, "headline", None),
            fallback=_DEFAULT_REASON_TITLE,
        )

        body = explanation or reason_detail
        if not body and result is not None:
            pipeline_explanation = getattr(result, "explanation", None)
            body = _text(getattr(pipeline_explanation, "summary", None))
            if not body:
                mission = getattr(result, "mission", None)
                body = _text(getattr(mission, "educational_rationale", None))

        if not body:
            body = _DEFAULT_REASON_BODY

        return RecommendationCard(
            title=headline or _DEFAULT_REASON_TITLE,
            body=body,
            eyebrow="Mission reason",
            reason_label=body,
            category_label=category,
        )


def _text(value: Any, *, fallback: str = "") -> str:
    if value is None:
        return fallback
    cleaned = str(value).strip()
    return cleaned if cleaned else fallback


def _first_sentence(text: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        return ""
    for separator in (". ", "! ", "? "):
        index = cleaned.find(separator)
        if index != -1:
            return cleaned[: index + 1].strip()
    return cleaned
