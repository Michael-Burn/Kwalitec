"""Dashboard mapping — greeting, actions, upcoming sessions, header chrome.

Assembles presentation snippets from already-decided Educational OS outputs.
Does not orchestrate learning, persist state, or invent next actions.
"""

from __future__ import annotations

from typing import Any

from presentation.dashboard.dashboard_view_model import (
    QuickActionView,
    UpcomingSessionView,
)
from presentation.design_system import (
    Button,
    Card,
    CardVariant,
    PageHeader,
    Section,
    ghost_button,
    primary_button,
    secondary_button,
)
from presentation.mission_workspace.workspace_view_model import (
    CompletionActionView,
    MissionWorkspaceViewModel,
)

_DEFAULT_GREETING = "Welcome back — ready for today's session."
_DEFAULT_HEADER_TITLE = "Learning Dashboard"
_DEFAULT_HEADER_DESCRIPTION = (
    "Your command centre for today's mission, progress, and next steps."
)
_DEFAULT_PRIMARY_LABEL = "Begin Session"
_DEFAULT_PRIMARY_KEY = "begin_session"
_MAX_UPCOMING = 5


class DashboardMapper:
    """Map pipeline / workspace inputs into dashboard shell chrome."""

    @classmethod
    def map_greeting(
        cls,
        workspace: MissionWorkspaceViewModel | None,
        *,
        result: Any = None,
        twin: Any = None,
    ) -> tuple[str, Section]:
        """Build greeting text and a greeting ``Section``."""
        text = _text(getattr(workspace, "greeting", None))
        # Empty-workspace default is a placeholder — allow Twin / experience
        # personalisation to replace it.
        if text == _DEFAULT_GREETING:
            text = ""
        if not text and result is not None:
            experience = getattr(result, "student_experience", None)
            motivation = getattr(experience, "motivation", None) if experience else None
            text = _text(getattr(motivation, "message", None))
            if not text:
                narrative = _text(getattr(experience, "presentation_narrative", None))
                text = _first_sentence(narrative)
        if not text:
            name = _text(
                getattr(twin, "display_name", None)
                or getattr(twin, "student_name", None)
                or getattr(twin, "name", None)
            )
            if name:
                text = f"Welcome back, {name}."
        if not text:
            text = _DEFAULT_GREETING

        section = Section(
            title="Greeting",
            description=text,
            eyebrow="Dashboard",
        )
        return text, section

    @classmethod
    def map_header(
        cls,
        *,
        greeting: str,
        mission_title: str,
    ) -> PageHeader:
        """Build the dashboard ``PageHeader``."""
        description = (
            mission_title
            if mission_title and mission_title != "Today's Mission"
            else _DEFAULT_HEADER_DESCRIPTION
        )
        return PageHeader(
            title=_DEFAULT_HEADER_TITLE,
            description=description,
            eyebrow=greeting or "Dashboard",
        )

    @classmethod
    def map_primary_action(
        cls,
        workspace: MissionWorkspaceViewModel | None,
    ) -> Button:
        """Project the primary CTA from already-decided completion actions."""
        actions = tuple(getattr(workspace, "completion_actions", ()) or ())
        primary = _primary_non_home(actions)
        if primary is not None and primary.label:
            return primary_button(primary.label)
        return primary_button(_DEFAULT_PRIMARY_LABEL)

    @classmethod
    def primary_action_key(
        cls,
        workspace: MissionWorkspaceViewModel | None,
    ) -> str:
        """Return the primary action key (presentation routing hint only)."""
        actions = tuple(getattr(workspace, "completion_actions", ()) or ())
        primary = _primary_non_home(actions)
        if primary is not None and primary.action_key:
            return primary.action_key
        return _DEFAULT_PRIMARY_KEY

    @classmethod
    def map_quick_actions(
        cls,
        workspace: MissionWorkspaceViewModel | None,
        *,
        result: Any = None,
    ) -> tuple[QuickActionView, ...]:
        """Project quick-action CTAs from completion actions and reminders."""
        views: list[QuickActionView] = []
        actions = tuple(getattr(workspace, "completion_actions", ()) or ())
        for action in actions:
            if not action or not action.label:
                continue
            if action.action_key == "return_home":
                button = ghost_button(action.label)
            elif views:
                button = secondary_button(action.label)
            else:
                button = primary_button(action.label)
            views.append(
                QuickActionView(
                    label=action.label,
                    detail=action.detail,
                    action_key=action.action_key,
                    button=button,
                )
            )

        experience = getattr(result, "student_experience", None) if result else None
        for reminder in _as_tuple(getattr(experience, "reminders", ())):
            message = _text(getattr(reminder, "message", None))
            if not message:
                continue
            kind = _enum_or_text(getattr(reminder, "kind", None))
            key = kind or "reminder"
            if any(view.action_key == key for view in views):
                continue
            views.append(
                QuickActionView(
                    label=_humanise(kind) if kind else "Reminder",
                    detail=message,
                    action_key=key,
                    button=secondary_button(_humanise(kind) if kind else "Reminder"),
                )
            )

        if not views:
            views.append(
                QuickActionView(
                    label=_DEFAULT_PRIMARY_LABEL,
                    detail="Open today's session when you are ready.",
                    action_key=_DEFAULT_PRIMARY_KEY,
                    button=primary_button(_DEFAULT_PRIMARY_LABEL),
                )
            )
            views.append(
                QuickActionView(
                    label="View Progress",
                    detail="Review your progress summary.",
                    action_key="view_progress",
                    button=secondary_button("View Progress"),
                )
            )
        return tuple(views)

    @classmethod
    def map_upcoming_sessions(
        cls,
        *,
        result: Any = None,
        statistics: Any = None,
    ) -> tuple[UpcomingSessionView, ...]:
        """Project upcoming study-plan sessions into preview cards."""
        sessions = _upcoming_from_result(result)
        if not sessions and statistics is not None:
            sessions = _as_tuple(
                getattr(statistics, "upcoming_sessions", None)
                or getattr(statistics, "sessions", None)
            )

        views: list[UpcomingSessionView] = []
        for session in sessions[:_MAX_UPCOMING]:
            if session is None:
                continue
            label = _text(
                getattr(session, "label", None) or getattr(session, "title", None),
                fallback="Upcoming session",
            )
            kind = _enum_or_text(getattr(session, "kind", None))
            day_index = getattr(session, "day_index", None)
            day_label = _day_label(day_index)
            minutes = _safe_int(
                getattr(session, "allocated_minutes", None)
                or getattr(session, "planned_minutes", None)
                or getattr(session, "duration_minutes", None)
            )
            duration_label = _duration_label(minutes)
            detail_parts = [
                part
                for part in (day_label, duration_label, _humanise(kind))
                if part
            ]
            detail = " · ".join(detail_parts)
            views.append(
                UpcomingSessionView(
                    label=label,
                    detail=detail,
                    day_label=day_label,
                    duration_label=duration_label,
                    kind_label=_humanise(kind),
                    card=Card(
                        title=label,
                        body=detail or "Scheduled study session",
                        eyebrow="Upcoming",
                        variant=CardVariant.DEFAULT,
                    ),
                )
            )

        if not views:
            empty_detail = (
                "Upcoming sessions will appear when a study plan is available."
            )
            return (
                UpcomingSessionView(
                    label="No upcoming sessions",
                    detail=empty_detail,
                    day_label="",
                    duration_label="",
                    kind_label="",
                    card=Card(
                        title="No upcoming sessions",
                        body=empty_detail,
                        eyebrow="Upcoming",
                        variant=CardVariant.DEFAULT,
                    ),
                ),
            )
        return tuple(views)


def _upcoming_from_result(result: Any) -> tuple[Any, ...]:
    if result is None:
        return ()
    plan = getattr(result, "study_plan", None)
    if plan is None:
        return ()
    ordered = getattr(plan, "ordered_sessions", None)
    if callable(ordered):
        try:
            sessions = _as_tuple(ordered())
        except TypeError:
            sessions = ()
    else:
        sessions = _as_tuple(ordered)
    if not sessions:
        schedule = getattr(plan, "schedule", None)
        sessions = _as_tuple(getattr(schedule, "sessions", ()))
    # Skip the first session (treated as today's focus) when more exist.
    if len(sessions) > 1:
        return sessions[1:]
    return sessions


def _primary_non_home(
    actions: tuple[CompletionActionView, ...],
) -> CompletionActionView | None:
    for action in actions:
        if action.action_key and action.action_key != "return_home":
            return action
    for action in actions:
        if action.label:
            return action
    return None


def _day_label(day_index: Any) -> str:
    if day_index is None or isinstance(day_index, bool):
        return ""
    try:
        value = int(day_index)
    except (TypeError, ValueError):
        return ""
    if value < 0:
        return ""
    if value == 0:
        return "Day 1"
    return f"Day {value + 1}"


def _duration_label(minutes: int) -> str:
    if minutes <= 0:
        return ""
    if minutes == 1:
        return "1 minute"
    return f"{minutes} minutes"


def _as_tuple(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    try:
        return tuple(value)
    except TypeError:
        return ()


def _safe_int(value: Any) -> int:
    if value is None or isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return max(0, value)
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def _enum_or_text(value: Any) -> str:
    if value is None:
        return ""
    raw = getattr(value, "value", value)
    return _text(str(raw) if raw is not None else None)


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


def _humanise(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        return cleaned
    return cleaned.replace("_", " ").replace("-", " ").strip().capitalize()
