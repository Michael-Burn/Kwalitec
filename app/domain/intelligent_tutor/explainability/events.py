"""Factual Tutor explanation events (AP-002D6).

No orchestration. No Reasoning callbacks. No Mission mutations.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class ExplanationEventKind(StrEnum):
    """Kinds of factual Tutor explanation events."""

    REQUESTED = "tutor_explanation_requested"
    GENERATED = "tutor_explanation_generated"
    UNAVAILABLE = "tutor_explanation_unavailable"


@dataclass(frozen=True, slots=True)
class TutorExplanationRequested:
    """Tutor explanation cycle began for validated educational provenance."""

    event_id: str
    twin_id: str
    decision_set_id: str
    explanation_request_id: str
    occurred_at: datetime
    explanation_version: str
    kind: ExplanationEventKind = ExplanationEventKind.REQUESTED

    def __post_init__(self) -> None:
        _require_nonblank(
            self,
            "event_id",
            "twin_id",
            "decision_set_id",
            "explanation_request_id",
            "explanation_version",
        )
        when = self.occurred_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "occurred_at", when.astimezone(UTC).replace(tzinfo=None)
            )


@dataclass(frozen=True, slots=True)
class TutorExplanationGenerated:
    """A fully traceable Tutor explanation was generated."""

    event_id: str
    explanation_id: str
    twin_id: str
    decision_set_id: str
    section_count: int
    occurred_at: datetime
    explanation_version: str
    mission_plan_id: str = ""
    kind: ExplanationEventKind = ExplanationEventKind.GENERATED

    def __post_init__(self) -> None:
        _require_nonblank(
            self,
            "event_id",
            "explanation_id",
            "twin_id",
            "decision_set_id",
            "explanation_version",
        )
        when = self.occurred_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "occurred_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(self, "section_count", int(self.section_count))


@dataclass(frozen=True, slots=True)
class TutorExplanationUnavailable:
    """Explanation could not be produced honestly (insufficient provenance)."""

    event_id: str
    twin_id: str
    decision_set_id: str
    reason_code: str
    occurred_at: datetime
    explanation_version: str
    explanation_id: str = ""
    explanation_request_id: str = ""
    kind: ExplanationEventKind = ExplanationEventKind.UNAVAILABLE

    def __post_init__(self) -> None:
        _require_nonblank(
            self,
            "event_id",
            "twin_id",
            "decision_set_id",
            "reason_code",
            "explanation_version",
        )
        when = self.occurred_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "occurred_at", when.astimezone(UTC).replace(tzinfo=None)
            )


def _require_nonblank(obj: object, *fields: str) -> None:
    for field_name in fields:
        if not (getattr(obj, field_name) or "").strip():
            raise ValueError(f"{field_name} is required")
