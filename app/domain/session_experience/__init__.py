"""Version 2 Learning Session Experience — domain package.

Focused study environment vocabulary for Overview, Activity, Reflection,
Summary, and Complete. Owns presentation, workflow, projection, and
navigation only — never educational law.

No Flask, SQLAlchemy, UI, or persistence.

Prefer explicit imports such as
``app.domain.session_experience.learning_session.LearningSession``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "CANONICAL_SURFACES",
    "FLOW_STEP_LABELS",
    "FORBIDDEN_ACTIVITY_TERMS",
    "FORBIDDEN_REFLECTION_TERMS",
    "SESSION_FLOW",
    "SURFACE_LABELS",
    "ActivityPhase",
    "ActivityProjection",
    "BeginSessionAction",
    "CompletionProjection",
    "LearningSession",
    "LearningSessionStatus",
    "ReflectionProjection",
    "ReturnHomeAction",
    "SessionProgress",
    "SessionSurface",
    "SessionWorkspace",
    "SessionWorkspaceStatus",
    "assert_linear_advance",
    "can_advance",
    "can_retreat",
    "flow_position",
    "is_canonical_surface",
    "is_entry",
    "is_reflection_safe",
    "is_student_safe_copy",
    "is_terminal",
    "next_surface",
    "previous_surface",
    "readiness_change_label",
    "resolve_surface",
    "step_label",
    "surface_index",
]

_EXPORT_MODULES = {
    "CANONICAL_SURFACES": "app.domain.session_experience.session_workspace",
    "FLOW_STEP_LABELS": "app.domain.session_experience.session_navigation",
    "FORBIDDEN_ACTIVITY_TERMS": (
        "app.domain.session_experience.activity_projection"
    ),
    "FORBIDDEN_REFLECTION_TERMS": (
        "app.domain.session_experience.reflection_projection"
    ),
    "SESSION_FLOW": "app.domain.session_experience.session_navigation",
    "SURFACE_LABELS": "app.domain.session_experience.session_workspace",
    "ActivityPhase": "app.domain.session_experience.activity_projection",
    "ActivityProjection": "app.domain.session_experience.activity_projection",
    "BeginSessionAction": "app.domain.session_experience.learning_session",
    "CompletionProjection": (
        "app.domain.session_experience.completion_projection"
    ),
    "LearningSession": "app.domain.session_experience.learning_session",
    "LearningSessionStatus": "app.domain.session_experience.learning_session",
    "ReflectionProjection": (
        "app.domain.session_experience.reflection_projection"
    ),
    "ReturnHomeAction": "app.domain.session_experience.completion_projection",
    "SessionProgress": "app.domain.session_experience.session_progress",
    "SessionSurface": "app.domain.session_experience.session_workspace",
    "SessionWorkspace": "app.domain.session_experience.session_workspace",
    "SessionWorkspaceStatus": "app.domain.session_experience.session_workspace",
    "assert_linear_advance": "app.domain.session_experience.session_navigation",
    "can_advance": "app.domain.session_experience.session_navigation",
    "can_retreat": "app.domain.session_experience.session_navigation",
    "flow_position": "app.domain.session_experience.session_navigation",
    "is_canonical_surface": "app.domain.session_experience.session_workspace",
    "is_entry": "app.domain.session_experience.session_navigation",
    "is_reflection_safe": "app.domain.session_experience.reflection_projection",
    "is_student_safe_copy": "app.domain.session_experience.activity_projection",
    "is_terminal": "app.domain.session_experience.session_navigation",
    "next_surface": "app.domain.session_experience.session_navigation",
    "previous_surface": "app.domain.session_experience.session_navigation",
    "readiness_change_label": (
        "app.domain.session_experience.completion_projection"
    ),
    "resolve_surface": "app.domain.session_experience.session_workspace",
    "step_label": "app.domain.session_experience.session_navigation",
    "surface_index": "app.domain.session_experience.session_workspace",
}


def __getattr__(name: str) -> Any:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
