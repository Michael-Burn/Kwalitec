"""MissionCard — current mission projection for the workspace."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.workspace.enums import PriorityLabel
from application.student_experience.workspace.errors import WorkspaceInvariantViolation


@dataclass(frozen=True, slots=True)
class MissionCard:
    """Immutable mission projection — title, purpose, priority, dependencies."""

    available: bool
    mission_id: str | None
    title: str
    purpose: str
    priority: PriorityLabel
    priority_label: str
    dependencies_satisfied: bool
    dependencies_summary: str
    dependency_labels: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.priority, PriorityLabel):
            raise WorkspaceInvariantViolation(
                "priority must be a PriorityLabel",
                invariant="MissionCard.priority.type",
            )
        object.__setattr__(
            self, "mission_id", (self.mission_id or "").strip() or None
        )
        for name in ("title", "purpose", "priority_label", "dependencies_summary"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise WorkspaceInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"MissionCard.{name}.required",
                )
            object.__setattr__(self, name, value)
        object.__setattr__(self, "dependency_labels", tuple(self.dependency_labels))
        for label in self.dependency_labels:
            if not isinstance(label, str) or not label.strip():
                raise WorkspaceInvariantViolation(
                    "dependency_labels must contain non-empty strings",
                    invariant="MissionCard.dependency_labels.type",
                )
        object.__setattr__(
            self,
            "dependency_labels",
            tuple(label.strip() for label in self.dependency_labels),
        )
