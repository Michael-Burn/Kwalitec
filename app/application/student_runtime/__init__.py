"""Student Runtime Coordinator — compose-only Student OS spine (SR-002).

Composes Mission accept → LearningSessionRuntime → Session Experience HTTP
binding. Domain authorities keep educational math; this package wires them.
"""

from __future__ import annotations

from app.application.student_runtime.coordinator import StudentRuntimeCoordinator
from app.application.student_runtime.dto import SessionBindingResult
from app.application.student_runtime.exceptions import (
    MissionNotAcceptable,
    SessionSpineUnavailable,
    StudentRuntimeError,
)

__all__ = [
    "MissionNotAcceptable",
    "SessionBindingResult",
    "SessionSpineUnavailable",
    "StudentRuntimeCoordinator",
    "StudentRuntimeError",
]
