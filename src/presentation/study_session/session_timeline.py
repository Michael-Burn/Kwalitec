"""Session timeline — ordered guided-session section chrome.

Presentation ordering only. Does not decide what to study or when to advance
educationally; it formats an immutable timeline/stepper for the runner UI.
"""

from __future__ import annotations

from presentation.design_system import (
    Stepper,
    StepperStep,
    Timeline,
    TimelineItem,
)
from presentation.study_session.session_view_model import SessionSectionView

# Canonical guided-session section order (V3-003).
SECTION_ORDER: tuple[str, ...] = (
    "mission_header",
    "mission_objective",
    "educational_explanation",
    "estimated_duration",
    "learning_resources",
    "worked_example",
    "progress_indicator",
    "study_notes",
    "reflection_prompt",
    "completion_summary",
    "next_step",
)

SECTION_TITLES: dict[str, str] = {
    "mission_header": "Session",
    "mission_objective": "Objective",
    "educational_explanation": "Why this session",
    "estimated_duration": "Estimated duration",
    "learning_resources": "Learning resources",
    "worked_example": "Worked example",
    "progress_indicator": "Progress",
    "study_notes": "Study notes",
    "reflection_prompt": "Reflection",
    "completion_summary": "Completion",
    "next_step": "Next step",
}


class SessionTimeline:
    """Build ordered timeline and stepper chrome for the session runner."""

    @classmethod
    def section_keys(cls) -> tuple[str, ...]:
        """Return the canonical section key order."""
        return SECTION_ORDER

    @classmethod
    def title_for(cls, key: str) -> str:
        """Return the display title for a section key."""
        return SECTION_TITLES.get(key, key.replace("_", " ").capitalize())

    @classmethod
    def order_sections(
        cls,
        sections: tuple[SessionSectionView, ...] | list[SessionSectionView],
    ) -> tuple[SessionSectionView, ...]:
        """Sort sections into canonical runner order; drop unknown keys last."""
        by_key = {section.key: section for section in sections if section is not None}
        ordered: list[SessionSectionView] = []
        for key in SECTION_ORDER:
            section = by_key.pop(key, None)
            if section is not None:
                ordered.append(section)
        for key in sorted(by_key):
            ordered.append(by_key[key])
        return tuple(ordered)

    @classmethod
    def build_timeline(
        cls,
        sections: tuple[SessionSectionView, ...],
        *,
        active_key: str | None = None,
        label: str = "Session timeline",
    ) -> Timeline:
        """Project ordered sections into a Design System ``Timeline``."""
        ordered = cls.order_sections(sections)
        if active_key is None and ordered:
            active_key = ordered[0].key
        items = tuple(
            TimelineItem(
                title=section.title or cls.title_for(section.key),
                detail=section.body,
                timestamp_label="",
                active=section.key == active_key,
            )
            for section in ordered
        )
        return Timeline(items=items, label=label)

    @classmethod
    def build_stepper(
        cls,
        sections: tuple[SessionSectionView, ...],
        *,
        current_key: str | None = None,
        label: str = "Session progress",
    ) -> Stepper:
        """Project ordered sections into a Design System ``Stepper``."""
        ordered = cls.order_sections(sections)
        if current_key is None and ordered:
            current_key = ordered[0].key
        current_index = next(
            (
                index
                for index, section in enumerate(ordered)
                if section.key == current_key
            ),
            0,
        )
        steps = tuple(
            StepperStep(
                label=section.title or cls.title_for(section.key),
                description=section.eyebrow,
                complete=index < current_index,
                current=index == current_index,
            )
            for index, section in enumerate(ordered)
        )
        return Stepper(steps=steps, label=label)

    @classmethod
    def progress_percent(
        cls,
        sections: tuple[SessionSectionView, ...],
        *,
        current_key: str | None = None,
    ) -> float:
        """Display percent for runner chrome from section position only."""
        ordered = cls.order_sections(sections)
        if not ordered:
            return 0.0
        if current_key is None:
            current_key = ordered[0].key
        current_index = next(
            (
                index
                for index, section in enumerate(ordered)
                if section.key == current_key
            ),
            0,
        )
        if len(ordered) == 1:
            return 0.0 if current_index == 0 else 100.0
        return round(100.0 * current_index / (len(ordered) - 1), 2)
