"""Version 2 Student Experience — domain package.

Learner-facing projection vocabulary for Home, Journey, Revision,
History, and Profile. Owns presentation, workflow, projection, and
navigation only — never educational law.

No Flask, SQLAlchemy, UI, or persistence.

Prefer explicit imports such as
``app.domain.student_experience.student_home.StudentHome``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "CANONICAL_SURFACES",
    "FORBIDDEN_INTERNAL_TERMS",
    "SURFACE_LABELS",
    "TERMINOLOGY_MAP",
    "AccountSettings",
    "AchievementCard",
    "CompletedSessionCard",
    "ExperienceSession",
    "ExperienceSessionStatus",
    "ExperienceSnapshot",
    "ExperienceSurface",
    "ExperienceWorkspace",
    "ExperienceWorkspaceStatus",
    "HistoryProjection",
    "JourneyProjection",
    "JourneyTopicCard",
    "LearningGoal",
    "LearningStatistics",
    "ProfileProjection",
    "ReadinessPoint",
    "RecommendationExplanation",
    "RevisionOption",
    "RevisionProjection",
    "StartSessionAction",
    "StudentHome",
    "StudyPreferences",
    "assert_student_safe",
    "build_explanation",
    "is_canonical_surface",
    "is_student_safe",
    "readiness_band_label",
    "resolve_surface",
    "surface_index",
    "translate_to_student_language",
]

_EXPORT_MODULES = {
    "CANONICAL_SURFACES": "app.domain.student_experience.experience_workspace",
    "FORBIDDEN_INTERNAL_TERMS": (
        "app.domain.student_experience.recommendation_explanation"
    ),
    "SURFACE_LABELS": "app.domain.student_experience.experience_workspace",
    "TERMINOLOGY_MAP": (
        "app.domain.student_experience.recommendation_explanation"
    ),
    "AccountSettings": "app.domain.student_experience.profile_projection",
    "AchievementCard": "app.domain.student_experience.history_projection",
    "CompletedSessionCard": "app.domain.student_experience.history_projection",
    "ExperienceSession": "app.domain.student_experience.experience_session",
    "ExperienceSessionStatus": (
        "app.domain.student_experience.experience_session"
    ),
    "ExperienceSnapshot": "app.domain.student_experience.experience_snapshot",
    "ExperienceSurface": "app.domain.student_experience.experience_workspace",
    "ExperienceWorkspace": "app.domain.student_experience.experience_workspace",
    "ExperienceWorkspaceStatus": (
        "app.domain.student_experience.experience_workspace"
    ),
    "HistoryProjection": "app.domain.student_experience.history_projection",
    "JourneyProjection": "app.domain.student_experience.journey_projection",
    "JourneyTopicCard": "app.domain.student_experience.journey_projection",
    "LearningGoal": "app.domain.student_experience.profile_projection",
    "LearningStatistics": "app.domain.student_experience.profile_projection",
    "ProfileProjection": "app.domain.student_experience.profile_projection",
    "ReadinessPoint": "app.domain.student_experience.history_projection",
    "RecommendationExplanation": (
        "app.domain.student_experience.recommendation_explanation"
    ),
    "RevisionOption": "app.domain.student_experience.revision_projection",
    "RevisionProjection": "app.domain.student_experience.revision_projection",
    "StartSessionAction": "app.domain.student_experience.experience_session",
    "StudentHome": "app.domain.student_experience.student_home",
    "StudyPreferences": "app.domain.student_experience.profile_projection",
    "assert_student_safe": (
        "app.domain.student_experience.recommendation_explanation"
    ),
    "build_explanation": (
        "app.domain.student_experience.recommendation_explanation"
    ),
    "is_canonical_surface": (
        "app.domain.student_experience.experience_workspace"
    ),
    "is_student_safe": (
        "app.domain.student_experience.recommendation_explanation"
    ),
    "readiness_band_label": "app.domain.student_experience.student_home",
    "resolve_surface": "app.domain.student_experience.experience_workspace",
    "surface_index": "app.domain.student_experience.experience_workspace",
    "translate_to_student_language": (
        "app.domain.student_experience.recommendation_explanation"
    ),
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
