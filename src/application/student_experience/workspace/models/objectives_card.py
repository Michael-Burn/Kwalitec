"""ObjectivesCard — ordered session / mission objectives for the workspace."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.workspace.enums import ObjectiveStatus
from application.student_experience.workspace.errors import WorkspaceInvariantViolation


@dataclass(frozen=True, slots=True)
class ObjectiveItem:
    """One ordered objective projected into the workspace."""

    objective_id: str
    label: str
    status: ObjectiveStatus
    order: int
    estimated_minutes: int | None = None

    def __post_init__(self) -> None:
        objective_id = (self.objective_id or "").strip()
        if not objective_id:
            raise WorkspaceInvariantViolation(
                "objective_id must be a non-empty string",
                invariant="ObjectiveItem.objective_id.required",
            )
        object.__setattr__(self, "objective_id", objective_id)
        label = (self.label or "").strip()
        if not label:
            raise WorkspaceInvariantViolation(
                "label must be a non-empty string",
                invariant="ObjectiveItem.label.required",
            )
        object.__setattr__(self, "label", label)
        if not isinstance(self.status, ObjectiveStatus):
            raise WorkspaceInvariantViolation(
                "status must be an ObjectiveStatus",
                invariant="ObjectiveItem.status.type",
            )
        if isinstance(self.order, bool) or not isinstance(self.order, int):
            raise WorkspaceInvariantViolation(
                "order must be an integer",
                invariant="ObjectiveItem.order.type",
            )
        if self.order < 1:
            raise WorkspaceInvariantViolation(
                "order must be >= 1",
                invariant="ObjectiveItem.order.range",
            )
        if self.estimated_minutes is not None:
            if isinstance(self.estimated_minutes, bool) or not isinstance(
                self.estimated_minutes, int
            ):
                raise WorkspaceInvariantViolation(
                    "estimated_minutes must be an integer when provided",
                    invariant="ObjectiveItem.estimated_minutes.type",
                )
            if self.estimated_minutes < 0:
                raise WorkspaceInvariantViolation(
                    "estimated_minutes must be >= 0",
                    invariant="ObjectiveItem.estimated_minutes.range",
                )


@dataclass(frozen=True, slots=True)
class ObjectivesCard:
    """Immutable ordered objectives with current / completed / remaining views."""

    items: tuple[ObjectiveItem, ...]
    current: ObjectiveItem | None
    completed: tuple[ObjectiveItem, ...]
    remaining: tuple[ObjectiveItem, ...]
    has_objectives: bool
    summary: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "items", tuple(self.items))
        object.__setattr__(self, "completed", tuple(self.completed))
        object.__setattr__(self, "remaining", tuple(self.remaining))
        for item in self.items:
            if not isinstance(item, ObjectiveItem):
                raise WorkspaceInvariantViolation(
                    "items must contain ObjectiveItem values",
                    invariant="ObjectivesCard.items.type",
                )
        for item in self.completed:
            if not isinstance(item, ObjectiveItem):
                raise WorkspaceInvariantViolation(
                    "completed must contain ObjectiveItem values",
                    invariant="ObjectivesCard.completed.type",
                )
        for item in self.remaining:
            if not isinstance(item, ObjectiveItem):
                raise WorkspaceInvariantViolation(
                    "remaining must contain ObjectiveItem values",
                    invariant="ObjectivesCard.remaining.type",
                )
        if self.current is not None and not isinstance(self.current, ObjectiveItem):
            raise WorkspaceInvariantViolation(
                "current must be an ObjectiveItem when provided",
                invariant="ObjectivesCard.current.type",
            )
        summary = (self.summary or "").strip()
        if not summary:
            raise WorkspaceInvariantViolation(
                "summary must be a non-empty string",
                invariant="ObjectivesCard.summary.required",
            )
        object.__setattr__(self, "summary", summary)
