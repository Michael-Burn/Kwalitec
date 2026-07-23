"""ResourcesCard — study resources for the workspace."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.workspace.enums import ResourceKind
from application.student_experience.workspace.errors import WorkspaceInvariantViolation


@dataclass(frozen=True, slots=True)
class ResourceItem:
    """One study resource projected into the workspace."""

    resource_id: str
    title: str
    detail: str
    kind: ResourceKind
    estimated_minutes: int | None = None

    def __post_init__(self) -> None:
        resource_id = (self.resource_id or "").strip()
        if not resource_id:
            raise WorkspaceInvariantViolation(
                "resource_id must be a non-empty string",
                invariant="ResourceItem.resource_id.required",
            )
        object.__setattr__(self, "resource_id", resource_id)
        for name in ("title", "detail"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise WorkspaceInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ResourceItem.{name}.required",
                )
            object.__setattr__(self, name, value)
        if not isinstance(self.kind, ResourceKind):
            raise WorkspaceInvariantViolation(
                "kind must be a ResourceKind",
                invariant="ResourceItem.kind.type",
            )
        if self.estimated_minutes is not None:
            if isinstance(self.estimated_minutes, bool) or not isinstance(
                self.estimated_minutes, int
            ):
                raise WorkspaceInvariantViolation(
                    "estimated_minutes must be an integer when provided",
                    invariant="ResourceItem.estimated_minutes.type",
                )
            if self.estimated_minutes < 0:
                raise WorkspaceInvariantViolation(
                    "estimated_minutes must be >= 0",
                    invariant="ResourceItem.estimated_minutes.range",
                )


@dataclass(frozen=True, slots=True)
class ResourcesCard:
    """Immutable study resources card — never invents educational content."""

    items: tuple[ResourceItem, ...] = ()
    has_resources: bool = False
    summary: str = "Study resources will appear when available."

    def __post_init__(self) -> None:
        object.__setattr__(self, "items", tuple(self.items))
        for item in self.items:
            if not isinstance(item, ResourceItem):
                raise WorkspaceInvariantViolation(
                    "items must contain ResourceItem values",
                    invariant="ResourcesCard.items.type",
                )
        summary = (self.summary or "").strip()
        if not summary:
            raise WorkspaceInvariantViolation(
                "summary must be a non-empty string",
                invariant="ResourcesCard.summary.required",
            )
        object.__setattr__(self, "summary", summary)
