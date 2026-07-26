"""Immutable SessionOutcome DTO (P2-MS005).

Canonical presentation object after a guided study session.
Experience Layer only — no educational metrics or mastery values.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.unified_journey.contracts import (
    COMPLETION_COMPLETE,
    COMPLETION_IN_PROGRESS,
    COMPLETION_VALUES,
    CONTRACT_VERSION,
)


@dataclass(frozen=True)
class SessionOutcome:
    """Canonical post-session presentation object.

    Assembled after a guided study session concludes (Wrapping Up /
    Complete). Never carries educational metrics or mastery values.
    """

    mission_title: str = ""
    completion_status: str = ""
    reflection_available: bool = False
    summary_message: str = ""
    next_transition: str = ""
    upcoming_action: str = ""
    contract_version: str = CONTRACT_VERSION
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "mission_title", (self.mission_title or "").strip()
        )
        completion = (self.completion_status or "").strip().lower()
        if completion and completion not in COMPLETION_VALUES:
            raise ValueError(
                f"unknown session outcome completion_status: "
                f"{self.completion_status!r}"
            )
        object.__setattr__(self, "completion_status", completion)
        object.__setattr__(
            self, "reflection_available", bool(self.reflection_available)
        )
        object.__setattr__(
            self, "summary_message", (self.summary_message or "").strip()
        )
        object.__setattr__(
            self, "next_transition", (self.next_transition or "").strip()
        )
        object.__setattr__(
            self, "upcoming_action", (self.upcoming_action or "").strip()
        )


def empty_session_outcome() -> SessionOutcome:
    """Placeholder SessionOutcome when no post-session state exists."""
    return SessionOutcome(
        mission_title="",
        completion_status="",
        reflection_available=False,
        summary_message="",
        next_transition="",
        upcoming_action="",
        metadata=(("availability", "placeholder"),),
    )


def completion_status_for_outcome(*, wrapping_up: bool) -> str:
    """Map presentation phase onto SessionOutcome completion vocabulary."""
    if wrapping_up:
        return COMPLETION_IN_PROGRESS
    return COMPLETION_COMPLETE
