"""ActionPlanCard — deterministic guidance composed from existing recommendations."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.readiness.enums import ActionPlanItemKind
from application.student_experience.readiness.errors import (
    ReadinessInvariantViolation,
)


@dataclass(frozen=True, slots=True)
class ActionPlanItem:
    """One composed action-plan guidance item — never newly generated advice."""

    kind: ActionPlanItemKind
    title: str
    guidance: str
    scope_label: str | None = None
    mission_id: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, ActionPlanItemKind):
            raise ReadinessInvariantViolation(
                "kind must be an ActionPlanItemKind",
                invariant="ActionPlanItem.kind.type",
            )
        for name in ("title", "guidance"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise ReadinessInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ActionPlanItem.{name}.required",
                )
            object.__setattr__(self, name, value)
        object.__setattr__(
            self, "scope_label", (self.scope_label or "").strip() or None
        )
        object.__setattr__(
            self, "mission_id", (self.mission_id or "").strip() or None
        )


@dataclass(frozen=True, slots=True)
class ActionPlanCard:
    """Immutable action plan — composes existing recommendations into guidance."""

    items: tuple[ActionPlanItem, ...] = ()
    summary: str = "An action plan will appear when recommendations are available."
    has_actions: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "items", tuple(self.items))
        for item in self.items:
            if not isinstance(item, ActionPlanItem):
                raise ReadinessInvariantViolation(
                    "items must contain ActionPlanItem values",
                    invariant="ActionPlanCard.items.type",
                )
        summary = (self.summary or "").strip()
        if not summary:
            raise ReadinessInvariantViolation(
                "summary must be a non-empty string",
                invariant="ActionPlanCard.summary.required",
            )
        object.__setattr__(self, "summary", summary)
