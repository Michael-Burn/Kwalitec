"""XP snapshot projection — map Student Experience cargo into dashboard chrome.

Presentation only. Reuses already-composed XP snapshots / view models via
structural duck-typing. Never estimates mastery, generates recommendations,
generates missions, schedules work, or invokes AI.
"""

from __future__ import annotations

from typing import Any

from presentation.dashboard.dashboard_view_model import (
    CoachInsightView,
    JourneyStoryView,
    MilestoneView,
    MissionHeroView,
    QuickActionView,
    ReadinessSummaryView,
)
from presentation.design_system import (
    Card,
    CardVariant,
    MissionCard,
    primary_button,
    secondary_button,
)

_MAX_COACH_SENTENCES = 3
_MAX_STORY_SENTENCES = 3
_MAX_QUICK_ACTIONS = 4
_MAX_MILESTONES = 3


class XpProjectionMapper:
    """Project XP home / journey / readiness / coach cargo into dashboard views."""

    @classmethod
    def has_experience_cargo(cls, experience: Any) -> bool:
        if experience is None:
            return False
        return bool(
            getattr(experience, "home", None)
            or getattr(experience, "home_snapshot", None)
            or getattr(experience, "todays_focus", None)
        )

    @classmethod
    def map_hero(
        cls,
        experience: Any,
        *,
        fallback_greeting: str = "",
        fallback_mission: MissionCard | None = None,
        fallback_cta_label: str = "Continue",
        fallback_action_key: str = "begin_session",
    ) -> MissionHeroView:
        home = _home(experience)
        focus = getattr(home, "todays_focus", None) if home else None
        if focus is None:
            focus = getattr(experience, "todays_focus", None)
        snapshot = getattr(experience, "home_snapshot", None)
        next_action = getattr(experience, "next_action", None)
        has_mission_focus = bool(
            getattr(focus, "mission_title", None)
            or getattr(snapshot, "focus_mission_title", None)
            or getattr(focus, "has_focus", False)
        )

        greeting = _text(
            fallback_greeting
            or getattr(snapshot, "focus_headline", None)
            or getattr(focus, "headline", None),
            fallback="Welcome back — ready for today's mission.",
        )
        mission_title = _text(
            getattr(focus, "mission_title", None)
            or getattr(snapshot, "focus_mission_title", None)
            or (fallback_mission.title if fallback_mission else None),
            fallback="Today's Mission",
        )
        duration = _duration_label(
            getattr(focus, "estimated_duration_minutes", None)
        ) or _text(
            getattr(fallback_mission, "duration_label", None),
            fallback="Duration not available",
        )
        if has_mission_focus:
            purpose_source = getattr(focus, "study_objective", None) or getattr(
                focus, "reason", None
            )
        else:
            purpose_source = fallback_mission.body if fallback_mission else None
        purpose = _text(
            purpose_source,
            fallback="Your mission purpose will appear when available.",
        )
        cta_label = _text(
            getattr(next_action, "label", None)
            or getattr(focus, "primary_action_label", None)
            or getattr(snapshot, "focus_action_label", None),
            fallback=fallback_cta_label,
        )
        action_key = _text(
            getattr(next_action, "action_key", None)
            or _enum_or_text(getattr(focus, "primary_action_kind", None)),
            fallback=fallback_action_key,
        )
        status = _text(getattr(focus, "reason", None), fallback="")
        mission_card = MissionCard(
            title=mission_title,
            body=purpose,
            eyebrow="Today's Mission",
            duration_label=duration,
            status_label=status or _text(
                getattr(fallback_mission, "status_label", None),
                fallback="Ready when you are",
            ),
        )
        return MissionHeroView(
            greeting=greeting,
            mission_title=mission_title,
            duration_label=duration,
            purpose=purpose,
            cta_label=cta_label,
            action_key=action_key or fallback_action_key,
            status_label=mission_card.status_label,
            mission_card=mission_card,
            primary_action=primary_button(cta_label),
        )

    @classmethod
    def map_readiness(cls, experience: Any) -> ReadinessSummaryView:
        readiness = getattr(experience, "readiness", None)
        snapshot = getattr(experience, "readiness_snapshot", None)
        home = _home(experience)
        exam = getattr(home, "exam_readiness", None) if home else None

        category = _text(
            getattr(snapshot, "readiness_label", None)
            or getattr(readiness, "readiness_label", None)
            or getattr(exam, "readiness_label", None),
            fallback="Readiness",
        )
        trend = _text(
            getattr(snapshot, "direction_message", None)
            or _enum_or_text(getattr(snapshot, "direction", None))
            or getattr(exam, "trend_message", None)
            or _enum_or_text(getattr(exam, "trend", None)),
            fallback="Trend not available yet",
        )
        reason = _text(
            getattr(snapshot, "journey_trajectory_message", None)
            or getattr(exam, "trend_message", None)
            or getattr(snapshot, "assessment_confidence_label", None),
            fallback="Readiness detail will appear as you study.",
        )
        percent = getattr(snapshot, "readiness_percent", None)
        if percent is None:
            percent = getattr(exam, "readiness_percent", None)
        percent_label = _percent_label(percent)
        available = bool(
            getattr(snapshot, "readiness_available", None)
            or getattr(exam, "available", None)
            or percent is not None
        )
        action_label = "Review readiness" if available else "Start studying"
        action_key = "view_readiness" if available else "begin_session"
        card = Card(
            title=category,
            body=_clip_sentences(f"{trend} {reason}".strip(), 2),
            eyebrow="Readiness",
            variant=CardVariant.PROGRESS,
        )
        return ReadinessSummaryView(
            category_label=category,
            trend_label=trend,
            reason=reason,
            action_label=action_label,
            action_key=action_key,
            percent_label=percent_label,
            available=available,
            card=card,
        )

    @classmethod
    def map_journey(cls, experience: Any) -> JourneyStoryView:
        journey_snap = getattr(experience, "journey_snapshot", None)
        home = _home(experience)
        progress = getattr(home, "progress", None) if home else None
        momentum = getattr(home, "momentum", None) if home else None
        coach_snap = getattr(experience, "coach_snapshot", None)

        parts: list[str] = []
        for candidate in (
            getattr(journey_snap, "trajectory_message", None),
            getattr(coach_snap, "journey_message", None),
            getattr(progress, "weekly_growth_message", None),
            getattr(progress, "mastery_message", None),
            getattr(momentum, "momentum_message", None),
            getattr(journey_snap, "consistency_message", None),
        ):
            text = _text(candidate)
            if text and text not in parts:
                parts.append(text)
            if len(parts) >= _MAX_STORY_SENTENCES:
                break

        if not parts:
            story = (
                "Your learning story will appear here as you complete sessions."
            )
            available = False
        else:
            story = _clip_sentences(" ".join(parts), _MAX_STORY_SENTENCES)
            available = True

        return JourneyStoryView(
            story=story,
            available=available,
            card=Card(
                title="Learning journey",
                body=story,
                eyebrow="Journey",
                variant=CardVariant.DEFAULT,
            ),
        )

    @classmethod
    def map_coach(cls, experience: Any) -> CoachInsightView:
        coach = getattr(experience, "coach_context", None)
        coach_snap = getattr(experience, "coach_snapshot", None)
        home = _home(experience)
        insights = getattr(home, "learning_insights", None) if home else None
        celebration = getattr(experience, "celebrations", None)

        candidates: list[str] = []
        if insights is not None:
            for item in _as_tuple(getattr(insights, "insights", ())):
                message = _text(
                    getattr(item, "message", None) or getattr(item, "title", None)
                )
                if message:
                    candidates.append(message)
                    break
        for candidate in (
            getattr(coach_snap, "focus_headline", None),
            getattr(coach, "focus_headline", None),
            getattr(getattr(coach, "current_focus", None), "headline", None),
            getattr(coach_snap, "journey_message", None),
        ):
            text = _text(candidate)
            if text:
                candidates.append(text)

        moments = _as_tuple(getattr(celebration, "moments", None) or celebration)
        for moment in moments[:1]:
            text = _text(
                getattr(moment, "message", None) or getattr(moment, "title", None)
            )
            if text:
                candidates.append(text)

        if not candidates:
            insight = (
                "Your coach insight will appear after your next study session."
            )
            available = False
        else:
            insight = _clip_sentences(
                " ".join(candidates[:2]), _MAX_COACH_SENTENCES
            )
            available = True

        return CoachInsightView(
            insight=insight,
            available=available,
            card=Card(
                title="Coach",
                body=insight,
                eyebrow="Coach",
                variant=CardVariant.RECOMMENDATION,
            ),
        )

    @classmethod
    def map_milestones(cls, experience: Any) -> tuple[MilestoneView, ...]:
        home = _home(experience)
        milestone = getattr(home, "upcoming_milestone", None) if home else None
        views: list[MilestoneView] = []
        if milestone is not None and (
            getattr(milestone, "has_milestone", False)
            or _text(getattr(milestone, "title", None))
        ):
            title = _text(getattr(milestone, "title", None), fallback="Milestone")
            detail = _text(getattr(milestone, "detail", None))
            days = getattr(milestone, "days_until", None)
            days_label = _days_label(days)
            views.append(
                MilestoneView(
                    title=title,
                    detail=detail,
                    days_label=days_label,
                    card=Card(
                        title=title,
                        body=detail or days_label or "Upcoming milestone",
                        eyebrow="Upcoming",
                        variant=CardVariant.DEFAULT,
                    ),
                )
            )

        readiness = getattr(experience, "readiness", None)
        for item in _as_tuple(getattr(readiness, "milestones", ()))[
            : _MAX_MILESTONES - len(views)
        ]:
            title = _text(
                getattr(item, "title", None) or getattr(item, "label", None),
                fallback="Milestone",
            )
            detail = _text(
                getattr(item, "detail", None) or getattr(item, "message", None)
            )
            views.append(
                MilestoneView(
                    title=title,
                    detail=detail,
                    days_label=_days_label(getattr(item, "days_until", None)),
                    card=Card(
                        title=title,
                        body=detail or "Upcoming milestone",
                        eyebrow="Upcoming",
                        variant=CardVariant.DEFAULT,
                    ),
                )
            )

        if not views:
            empty = "Upcoming milestones will appear as your plan unfolds."
            views.append(
                MilestoneView(
                    title="No upcoming milestones",
                    detail=empty,
                    card=Card(
                        title="No upcoming milestones",
                        body=empty,
                        eyebrow="Upcoming",
                        variant=CardVariant.DEFAULT,
                    ),
                )
            )
        return tuple(views[:_MAX_MILESTONES])

    @classmethod
    def map_quick_actions(
        cls,
        experience: Any,
        *,
        fallback: tuple[QuickActionView, ...] = (),
    ) -> tuple[QuickActionView, ...]:
        home = _home(experience)
        next_action = getattr(experience, "next_action", None)
        views: list[QuickActionView] = []

        if next_action is not None and _text(getattr(next_action, "label", None)):
            label = _text(getattr(next_action, "label", None))
            key = _text(
                getattr(next_action, "action_key", None),
                fallback="begin_session",
            )
            views.append(
                QuickActionView(
                    label=label,
                    detail=_text(getattr(next_action, "detail", None)),
                    action_key=key,
                    button=primary_button(label),
                )
            )

        actions_card = getattr(home, "quick_actions", None) if home else None
        for action in _as_tuple(getattr(actions_card, "actions", ())):
            if not getattr(action, "enabled", True):
                continue
            label = _text(getattr(action, "label", None))
            if not label:
                continue
            key = _enum_or_text(getattr(action, "kind", None)) or "quick_action"
            if any(view.action_key == key for view in views):
                continue
            views.append(
                QuickActionView(
                    label=label,
                    detail=_text(getattr(action, "detail", None)),
                    action_key=key,
                    button=secondary_button(label),
                )
            )
            if len(views) >= _MAX_QUICK_ACTIONS:
                break

        if not views:
            return fallback[:_MAX_QUICK_ACTIONS] if fallback else (
                QuickActionView(
                    label="Resume Mission",
                    detail="Continue today's mission when you are ready.",
                    action_key="begin_session",
                    button=primary_button("Resume Mission"),
                ),
            )
        return tuple(views[:_MAX_QUICK_ACTIONS])


def _home(experience: Any) -> Any:
    if experience is None:
        return None
    return getattr(experience, "home", None) or experience


def _duration_label(minutes: Any) -> str:
    if minutes is None or isinstance(minutes, bool):
        return ""
    try:
        value = int(minutes)
    except (TypeError, ValueError):
        return ""
    if value <= 0:
        return ""
    if value == 1:
        return "1 minute"
    return f"{value} minutes"


def _percent_label(value: Any) -> str:
    if value is None or isinstance(value, bool):
        return ""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if number <= 1.0:
        number *= 100.0
    return f"{int(round(number))}%"


def _days_label(days: Any) -> str:
    if days is None or isinstance(days, bool):
        return ""
    try:
        value = int(days)
    except (TypeError, ValueError):
        return ""
    if value < 0:
        return ""
    if value == 0:
        return "Today"
    if value == 1:
        return "In 1 day"
    return f"In {value} days"


def _clip_sentences(text: str, maximum: int) -> str:
    cleaned = " ".join(text.split()).strip()
    if not cleaned or maximum < 1:
        return cleaned
    sentences: list[str] = []
    remainder = cleaned
    while remainder and len(sentences) < maximum:
        cut = -1
        for separator in (". ", "! ", "? "):
            index = remainder.find(separator)
            if index != -1 and (cut == -1 or index < cut):
                cut = index + 1
        if cut == -1:
            sentences.append(remainder.strip())
            break
        sentences.append(remainder[:cut].strip())
        remainder = remainder[cut:].lstrip()
    return " ".join(sentences)


def _as_tuple(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    try:
        return tuple(value)
    except TypeError:
        return ()


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
