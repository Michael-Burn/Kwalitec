"""RiskCard — projected risks from existing educational artefacts."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.readiness.enums import RiskKind
from application.student_experience.readiness.errors import (
    ReadinessInvariantViolation,
)


@dataclass(frozen=True, slots=True)
class RiskItem:
    """One projected risk summary."""

    kind: RiskKind
    title: str
    message: str
    scope_label: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, RiskKind):
            raise ReadinessInvariantViolation(
                "kind must be a RiskKind",
                invariant="RiskItem.kind.type",
            )
        for name in ("title", "message"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise ReadinessInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"RiskItem.{name}.required",
                )
            object.__setattr__(self, name, value)
        object.__setattr__(
            self, "scope_label", (self.scope_label or "").strip() or None
        )


@dataclass(frozen=True, slots=True)
class RiskCard:
    """Immutable risks card — weakest areas, gaps, overdue work, pressure."""

    items: tuple[RiskItem, ...] = ()
    summary: str = "Risks will appear as your assessment develops."
    has_risks: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "items", tuple(self.items))
        for item in self.items:
            if not isinstance(item, RiskItem):
                raise ReadinessInvariantViolation(
                    "items must contain RiskItem values",
                    invariant="RiskCard.items.type",
                )
        summary = (self.summary or "").strip()
        if not summary:
            raise ReadinessInvariantViolation(
                "summary must be a non-empty string",
                invariant="RiskCard.summary.required",
            )
        object.__setattr__(self, "summary", summary)
