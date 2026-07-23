"""StrengthCard — projected strengths from existing educational artefacts."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.readiness.enums import StrengthKind
from application.student_experience.readiness.errors import (
    ReadinessInvariantViolation,
)


@dataclass(frozen=True, slots=True)
class StrengthItem:
    """One projected strength summary."""

    kind: StrengthKind
    title: str
    message: str
    scope_label: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, StrengthKind):
            raise ReadinessInvariantViolation(
                "kind must be a StrengthKind",
                invariant="StrengthItem.kind.type",
            )
        for name in ("title", "message"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise ReadinessInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"StrengthItem.{name}.required",
                )
            object.__setattr__(self, name, value)
        object.__setattr__(
            self, "scope_label", (self.scope_label or "").strip() or None
        )


@dataclass(frozen=True, slots=True)
class StrengthCard:
    """Immutable strengths card — strongest subjects, competencies, improvements."""

    items: tuple[StrengthItem, ...] = ()
    summary: str = "Strengths will appear as your assessment develops."
    has_strengths: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "items", tuple(self.items))
        for item in self.items:
            if not isinstance(item, StrengthItem):
                raise ReadinessInvariantViolation(
                    "items must contain StrengthItem values",
                    invariant="StrengthCard.items.type",
                )
        summary = (self.summary or "").strip()
        if not summary:
            raise ReadinessInvariantViolation(
                "summary must be a non-empty string",
                invariant="StrengthCard.summary.required",
            )
        object.__setattr__(self, "summary", summary)
