"""Study Session Runtime — lifecycle execution for one guided mission session.

Tracks progress through a single study session. Never makes educational
decisions, never persists, never orchestrates learning engines, and never
invokes AI.

Allowed: deterministic stage transitions, pause/resume, immutable events,
checkpoints, and replay.

Forbidden: mastery, diagnosis, prioritisation, strategy selection,
persistence, Flask/SQLAlchemy, educational content generation.
"""

from __future__ import annotations

from application.session_runtime.session_actions import (
    ACTIVE_STAGES,
    STAGE_ORDER,
    SessionAction,
    next_stage,
    previous_stage,
)
from application.session_runtime.session_checkpoint import SessionCheckpoint
from application.session_runtime.session_event import (
    SessionEvent,
    SessionEventKind,
)
from application.session_runtime.session_runtime import (
    InvalidSessionTransitionError,
    SessionRuntime,
    SessionRuntimeError,
)
from application.session_runtime.session_state import SessionStage, SessionState

__all__ = [
    "ACTIVE_STAGES",
    "STAGE_ORDER",
    "InvalidSessionTransitionError",
    "SessionAction",
    "SessionCheckpoint",
    "SessionEvent",
    "SessionEventKind",
    "SessionRuntime",
    "SessionRuntimeError",
    "SessionStage",
    "SessionState",
    "next_stage",
    "previous_stage",
]
