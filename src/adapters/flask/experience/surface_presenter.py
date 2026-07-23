"""Surface view models — project XP experience onto dedicated EOS pages."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from application.student_experience.integration.enums import JourneySurface
from application.student_experience.integration.models import (
    ExperienceJourneyViewModel,
)
from application.student_experience.integration.navigation import (
    action_key_for_focus,
)
from presentation.provenance import ProvenanceMapper, ProvenanceViewModel


@dataclass(frozen=True, slots=True)
class ExperienceSurfaceView:
    """Null-safe chrome for one continuous-journey surface page."""

    surface: str
    title: str
    headline: str
    body: str
    detail: str
    empty: bool
    empty_reason: str
    success_message: str
    action_label: str
    action_key: str
    readiness_change_message: str
    celebration_message: str
    provenance: ProvenanceViewModel | None = None


class ExperienceSurfacePresenter:
    """Map ``ExperienceJourneyViewModel`` into surface page chrome."""

    _TITLES: dict[str, str] = {
        JourneySurface.HOME.value: "Home",
        JourneySurface.JOURNEY.value: "Learning journey",
        JourneySurface.READINESS.value: "Exam readiness",
        JourneySurface.COACH.value: "Learning coach",
        JourneySurface.WORKSPACE.value: "Study workspace",
        JourneySurface.REFLECTION.value: "Reflection",
    }

    @classmethod
    def present(
        cls,
        experience: ExperienceJourneyViewModel | None,
        surface: JourneySurface | str,
        *,
        result: Any = None,
    ) -> ExperienceSurfaceView:
        key = (
            surface.value
            if isinstance(surface, JourneySurface)
            else str(surface or "").strip().lower()
        )
        title = cls._TITLES.get(key, "Student experience")
        if experience is None:
            return ExperienceSurfaceView(
                surface=key or "home",
                title=title,
                headline="",
                body="",
                detail="",
                empty=True,
                empty_reason="Your learning overview will appear here once session "
                "outcomes start updating your experience.",
                success_message="",
                action_label="",
                action_key="",
                readiness_change_message="",
                celebration_message="",
                provenance=ProvenanceMapper.for_surface(key, result=result),
            )

        surface_state = cls._surface_state(experience, key)
        readiness_change = ""
        if experience.readiness_change.changed:
            readiness_change = experience.readiness_change.message

        celebration = ""
        moments = getattr(experience.celebrations, "moments", ()) or ()
        if moments:
            first = moments[0]
            celebration = (
                getattr(first, "message", None)
                or getattr(first, "title", None)
                or ""
            ).strip()

        headline, body, detail, action_label, action_key = cls._copy(
            experience, key
        )
        empty = bool(surface_state and surface_state.is_empty)
        empty_reason = ""
        success = ""
        if surface_state is not None:
            empty_reason = (surface_state.empty_reason or "").strip()
            success = (surface_state.success_message or "").strip()
        if empty and not empty_reason:
            empty_reason = (
                "This view updates as you complete missions and reflection."
            )

        provenance = ProvenanceMapper.for_surface(
            key, experience=experience, result=result
        )

        return ExperienceSurfaceView(
            surface=key,
            title=title,
            headline=headline,
            body=body,
            detail=detail,
            empty=empty and not (headline or body),
            empty_reason=empty_reason if empty else "",
            success_message=success,
            action_label=action_label,
            action_key=action_key,
            readiness_change_message=readiness_change,
            celebration_message=celebration,
            provenance=provenance,
        )

    @classmethod
    def _surface_state(
        cls, experience: ExperienceJourneyViewModel, key: str
    ) -> Any:
        for state in experience.surface_states or ():
            surface = getattr(state, "surface", None)
            value = getattr(surface, "value", surface)
            if str(value) == key:
                return state
        return None

    @classmethod
    def _copy(
        cls, experience: ExperienceJourneyViewModel, key: str
    ) -> tuple[str, str, str, str, str]:
        next_action = experience.next_action
        action_label = (getattr(next_action, "label", None) or "").strip()
        action_kind = getattr(next_action, "action_kind", None)
        try:
            action_key = action_key_for_focus(action_kind) if action_kind else ""
        except Exception:
            action_key = (
                getattr(action_kind, "value", None) or str(action_kind or "")
            ).strip()

        if key == JourneySurface.HOME.value:
            home_snap = experience.home_snapshot
            focus = experience.primary_focus
            todays = getattr(experience.home, "todays_focus", None)
            headline = (
                getattr(todays, "headline", None)
                or getattr(home_snap, "focus_headline", None)
                or ""
            ).strip()
            return (
                headline,
                (getattr(focus, "reason", None) or "").strip(),
                (getattr(focus, "mission_title", None) or "").strip(),
                action_label
                or (getattr(focus, "action_label", None) or "").strip(),
                action_key,
            )
        if key == JourneySurface.JOURNEY.value:
            snap = experience.journey_snapshot
            return (
                (getattr(snap, "trajectory_message", None) or "").strip(),
                (getattr(snap, "consistency_message", None) or "").strip(),
                (getattr(snap, "home_focus_headline", None) or "").strip(),
                action_label,
                action_key,
            )
        if key == JourneySurface.READINESS.value:
            snap = experience.readiness_snapshot
            return (
                (getattr(snap, "readiness_label", None) or "").strip(),
                (getattr(snap, "direction_message", None) or "").strip(),
                (getattr(snap, "journey_trajectory_message", None) or "").strip(),
                action_label,
                action_key,
            )
        if key == JourneySurface.COACH.value:
            snap = experience.coach_snapshot
            return (
                (getattr(snap, "focus_headline", None) or "").strip(),
                (getattr(snap, "journey_message", None) or "").strip(),
                (getattr(snap, "readiness_label", None) or "").strip(),
                action_label,
                action_key,
            )
        return ("", "", "", action_label, action_key)
