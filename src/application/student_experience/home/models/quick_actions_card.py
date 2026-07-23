"""QuickActionsCard — deterministic home quick actions."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.home.enums import QuickActionKind
from application.student_experience.home.errors import HomeInvariantViolation


@dataclass(frozen=True, slots=True)
class QuickAction:
    """One deterministic quick action on the home surface."""

    kind: QuickActionKind
    label: str
    enabled: bool = True
    mission_id: str | None = None
    detail: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, QuickActionKind):
            raise HomeInvariantViolation(
                "kind must be a QuickActionKind",
                invariant="QuickAction.kind.type",
            )
        label = (self.label or "").strip()
        if not label:
            raise HomeInvariantViolation(
                "label must be a non-empty string",
                invariant="QuickAction.label.required",
            )
        object.__setattr__(self, "label", label)
        object.__setattr__(
            self, "mission_id", (self.mission_id or "").strip() or None
        )
        object.__setattr__(self, "detail", (self.detail or "").strip() or None)


@dataclass(frozen=True, slots=True)
class QuickActionsCard:
    """Immutable card of deterministic quick actions."""

    actions: tuple[QuickAction, ...] = ()
    headline: str = "Quick actions"

    def __post_init__(self) -> None:
        object.__setattr__(self, "actions", tuple(self.actions))
        for action in self.actions:
            if not isinstance(action, QuickAction):
                raise HomeInvariantViolation(
                    "actions must contain QuickAction values",
                    invariant="QuickActionsCard.actions.type",
                )
        headline = (self.headline or "").strip()
        if not headline:
            raise HomeInvariantViolation(
                "headline must be a non-empty string",
                invariant="QuickActionsCard.headline.required",
            )
        object.__setattr__(self, "headline", headline)

    def enabled_actions(self) -> tuple[QuickAction, ...]:
        return tuple(action for action in self.actions if action.enabled)
