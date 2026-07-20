"""Session Experience production adapters (V2-020A).

Connects Learning Session Experience application ports to Version 2
production services. Adapters translate only — they never calculate
educational outcomes.

Prefer explicit imports such as
``app.infrastructure.session.runtime_adapter.SessionRuntimeAdapter``.
"""

from __future__ import annotations

__all__ = [
    "SESSION_INFRASTRUCTURE_VERSION",
    "SessionActivityAdapter",
    "SessionAdaptiveAdapter",
    "SessionExperienceComposition",
    "SessionMissionAdapter",
    "SessionRuntimeAdapter",
    "SessionTwinAdapter",
    "build_production_session_experience",
]

SESSION_INFRASTRUCTURE_VERSION = "v2-020a-1.0.0"


def __getattr__(name: str):
    if name == "SessionRuntimeAdapter":
        from app.infrastructure.session.runtime_adapter import SessionRuntimeAdapter

        return SessionRuntimeAdapter
    if name == "SessionActivityAdapter":
        from app.infrastructure.session.activity_adapter import SessionActivityAdapter

        return SessionActivityAdapter
    if name == "SessionMissionAdapter":
        from app.infrastructure.session.mission_adapter import SessionMissionAdapter

        return SessionMissionAdapter
    if name == "SessionTwinAdapter":
        from app.infrastructure.session.twin_adapter import SessionTwinAdapter

        return SessionTwinAdapter
    if name == "SessionAdaptiveAdapter":
        from app.infrastructure.session.adaptive_adapter import SessionAdaptiveAdapter

        return SessionAdaptiveAdapter
    if name in {
        "SessionExperienceComposition",
        "build_production_session_experience",
    }:
        from app.infrastructure.session import composition as mod

        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
