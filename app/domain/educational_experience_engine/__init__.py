"""Educational Experience Engine domain (EX-001).

Transforms Educational Decisions into consistent, explainable, UI-agnostic
experience models. Does not create educational decisions, mutate Twin beliefs,
or alter Learning Evidence.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "CoachConversationContext",
    "DailyMissionExperience",
    "DashboardPriorityCard",
    "EXPERIENCE_VERSION",
    "EducationalExperienceEngine",
    "EffortPresentation",
    "ExperienceModel",
    "ExperienceTrace",
    "RevisionPlannerEntry",
    "StudySessionBriefing",
    "UrgencyLevel",
    "curriculum_area_label",
    "effort_label",
    "motivation_for",
    "next_steps_for",
    "outcome_for",
    "prerequisite_explanation",
    "summary_for",
    "title_for",
    "urgency_for",
]

_EXPORT_MODULES = {
    "EXPERIENCE_VERSION": "app.domain.educational_experience_engine.version",
    "UrgencyLevel": "app.domain.educational_experience_engine.urgency",
    "EffortPresentation": "app.domain.educational_experience_engine.experience",
    "ExperienceTrace": "app.domain.educational_experience_engine.experience",
    "ExperienceModel": "app.domain.educational_experience_engine.experience",
    "DailyMissionExperience": "app.domain.educational_experience_engine.surfaces",
    "CoachConversationContext": "app.domain.educational_experience_engine.surfaces",
    "DashboardPriorityCard": "app.domain.educational_experience_engine.surfaces",
    "RevisionPlannerEntry": "app.domain.educational_experience_engine.surfaces",
    "StudySessionBriefing": "app.domain.educational_experience_engine.surfaces",
    "EducationalExperienceEngine": "app.domain.educational_experience_engine.engine",
    "title_for": "app.domain.educational_experience_engine.presentation",
    "summary_for": "app.domain.educational_experience_engine.presentation",
    "outcome_for": "app.domain.educational_experience_engine.presentation",
    "motivation_for": "app.domain.educational_experience_engine.presentation",
    "next_steps_for": "app.domain.educational_experience_engine.presentation",
    "effort_label": "app.domain.educational_experience_engine.presentation",
    "urgency_for": "app.domain.educational_experience_engine.presentation",
    "prerequisite_explanation": (
        "app.domain.educational_experience_engine.presentation"
    ),
    "curriculum_area_label": "app.domain.educational_experience_engine.presentation",
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
