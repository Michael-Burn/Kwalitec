"""Version 2 Student Experience — application layer.

Learner-facing projection / orchestration over Twin, Adaptive Decision,
Mission, Journey, and Orchestrator ports.

Framework-independent: no Flask, SQLAlchemy, UI, migrations, or persistence.
Does not import or modify educational engine packages.

Prefer explicit imports such as
``app.application.student_experience.student_experience_service.StudentExperienceService``.
"""

from __future__ import annotations

from typing import Any

from app.application.student_experience.student_experience_service import (
    StudentExperienceService,
)

__all__ = [
    "AdaptiveDecisionPort",
    "AchievementSnapshot",
    "AccountSettingsSnapshot",
    "CompletedSessionSnapshot",
    "DashboardService",
    "DashboardSnapshot",
    "DiagnosticReport",
    "Diagnostics",
    "EXPERIENCE_VERSION",
    "ExplanationError",
    "ExplanationService",
    "ExplanationSnapshot",
    "HistoryError",
    "HistoryService",
    "HistorySnapshot",
    "HomeError",
    "HomeService",
    "HomeSnapshot",
    "JourneyError",
    "JourneyService",
    "JourneySnapshot",
    "JourneyTopicSnapshot",
    "LearningGoalSnapshot",
    "LearningJourneyPort",
    "LearningOrchestratorPort",
    "LearningStatisticsSnapshot",
    "MissionPort",
    "NavigationError",
    "NavigationItemSnapshot",
    "PORT_NAMES",
    "PolicyViolation",
    "PortUnavailable",
    "ProfileError",
    "ProfileService",
    "ProfileSnapshot",
    "ProjectionError",
    "ReadinessPointSnapshot",
    "RevisionError",
    "RevisionOptionSnapshot",
    "RevisionService",
    "RevisionSnapshot",
    "SessionNotFound",
    "StartSessionActionSnapshot",
    "StudentExperienceError",
    "StudentExperienceService",
    "StudentTwinPort",
    "StudyPreferencesSnapshot",
    "WorkspaceNotFound",
]

_EXPORT_MODULES = {
    "AdaptiveDecisionPort": (
        "app.application.student_experience.ports.adaptive_decision_port"
    ),
    "AchievementSnapshot": (
        "app.application.student_experience.dto.history_snapshot"
    ),
    "AccountSettingsSnapshot": (
        "app.application.student_experience.dto.profile_snapshot"
    ),
    "CompletedSessionSnapshot": (
        "app.application.student_experience.dto.history_snapshot"
    ),
    "DashboardService": "app.application.student_experience.dashboard_service",
    "DashboardSnapshot": "app.application.student_experience.dashboard_service",
    "DiagnosticReport": "app.application.student_experience.diagnostics",
    "Diagnostics": "app.application.student_experience.diagnostics",
    "EXPERIENCE_VERSION": "app.application.student_experience.diagnostics",
    "ExplanationError": "app.application.student_experience.exceptions",
    "ExplanationService": (
        "app.application.student_experience.explanation_service"
    ),
    "ExplanationSnapshot": (
        "app.application.student_experience.dto.explanation_snapshot"
    ),
    "HistoryError": "app.application.student_experience.exceptions",
    "HistoryService": "app.application.student_experience.history_service",
    "HistorySnapshot": (
        "app.application.student_experience.dto.history_snapshot"
    ),
    "HomeError": "app.application.student_experience.exceptions",
    "HomeService": "app.application.student_experience.home_service",
    "HomeSnapshot": "app.application.student_experience.dto.home_snapshot",
    "JourneyError": "app.application.student_experience.exceptions",
    "JourneyService": "app.application.student_experience.journey_service",
    "JourneySnapshot": (
        "app.application.student_experience.dto.journey_snapshot"
    ),
    "JourneyTopicSnapshot": (
        "app.application.student_experience.dto.journey_snapshot"
    ),
    "LearningGoalSnapshot": (
        "app.application.student_experience.dto.profile_snapshot"
    ),
    "LearningJourneyPort": (
        "app.application.student_experience.ports.learning_journey_port"
    ),
    "LearningOrchestratorPort": (
        "app.application.student_experience.ports.learning_orchestrator_port"
    ),
    "LearningStatisticsSnapshot": (
        "app.application.student_experience.dto.profile_snapshot"
    ),
    "MissionPort": "app.application.student_experience.ports.mission_port",
    "NavigationError": "app.application.student_experience.exceptions",
    "NavigationItemSnapshot": (
        "app.application.student_experience.dashboard_service"
    ),
    "PORT_NAMES": "app.application.student_experience.ports",
    "PolicyViolation": "app.application.student_experience.exceptions",
    "PortUnavailable": "app.application.student_experience.exceptions",
    "ProfileError": "app.application.student_experience.exceptions",
    "ProfileService": "app.application.student_experience.profile_service",
    "ProfileSnapshot": (
        "app.application.student_experience.dto.profile_snapshot"
    ),
    "ProjectionError": "app.application.student_experience.exceptions",
    "ReadinessPointSnapshot": (
        "app.application.student_experience.dto.history_snapshot"
    ),
    "RevisionError": "app.application.student_experience.exceptions",
    "RevisionOptionSnapshot": (
        "app.application.student_experience.dto.revision_snapshot"
    ),
    "RevisionService": "app.application.student_experience.revision_service",
    "RevisionSnapshot": (
        "app.application.student_experience.dto.revision_snapshot"
    ),
    "SessionNotFound": "app.application.student_experience.exceptions",
    "StartSessionActionSnapshot": (
        "app.application.student_experience.dto.home_snapshot"
    ),
    "StudentExperienceError": "app.application.student_experience.exceptions",
    "StudentExperienceService": (
        "app.application.student_experience.student_experience_service"
    ),
    "StudentTwinPort": (
        "app.application.student_experience.ports.student_twin_port"
    ),
    "StudyPreferencesSnapshot": (
        "app.application.student_experience.dto.profile_snapshot"
    ),
    "WorkspaceNotFound": "app.application.student_experience.exceptions",
}


def __getattr__(name: str) -> Any:
    if name == "StudentExperienceService":
        return StudentExperienceService
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
