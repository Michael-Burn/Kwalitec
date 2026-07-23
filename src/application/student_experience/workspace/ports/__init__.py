"""Ports for Adaptive Study Workspace — interfaces only."""

from __future__ import annotations

from application.student_experience.workspace.ports.workspace_publisher import (
    WorkspacePublisher,
)
from application.student_experience.workspace.ports.workspace_resource_provider import (
    WorkspaceResource,
    WorkspaceResourceProvider,
)

__all__ = [
    "WorkspacePublisher",
    "WorkspaceResource",
    "WorkspaceResourceProvider",
]
