"""Mission Intelligence domain package.

Execution / projection layer that operationalises Decision(s) into session/day
Mission / MissionTask structure. Not a Twin write domain. Not an Update
Strategy. Not selection authority. Not Recommendation packaging. Not WeekPlan
policy. No scheduling optimisation, scoring formulas, Flask, or ORM.

Domain ``Mission`` / ``MissionTask`` are distinct from
``app.models.mission.Mission`` / ``MissionTask`` (Stage A coexistence —
named dual truth).

Decision selects; Recommendation packages; Mission operationalises.
Decision does not own day composition. Mission never re-selects.

Imports are lazy via ``__getattr__`` so Twin write-path packages can load
without circular import deadlocks when mission is imported first.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "COMPLETION_OUTCOME_CATALOGUE",
    "MISSION_INTELLIGENCE_VERSION",
    "THIN_MISSION_WARRANT_POSTURES",
    "BehaviourEvidenceCategoryHint",
    "CandidateContrastHook",
    "DecisionAttribution",
    "DecisionCitation",
    "FeasibilityAcknowledgement",
    "FeasibilityEffect",
    "Mission",
    "MissionEngine",
    "MissionEvidenceHooks",
    "MissionExecutionContext",
    "MissionExplanationChain",
    "MissionExplanationChainLayer",
    "MissionIntelligence",
    "MissionOutcomeIdentity",
    "MissionRegenerationIdentity",
    "MissionScope",
    "MissionTask",
    "MissionWarrantPosture",
    "RecommendationLanguageHook",
    "aggregate_mission_warrant",
    "inherit_mission_warrant",
]

_EXPORT_MODULES = {
    "COMPLETION_OUTCOME_CATALOGUE": "app.domain.mission.evidence_hooks",
    "BehaviourEvidenceCategoryHint": "app.domain.mission.evidence_hooks",
    "MissionEvidenceHooks": "app.domain.mission.evidence_hooks",
    "MissionOutcomeIdentity": "app.domain.mission.evidence_hooks",
    "CandidateContrastHook": "app.domain.mission.attribution",
    "DecisionAttribution": "app.domain.mission.attribution",
    "DecisionCitation": "app.domain.mission.attribution",
    "MissionExplanationChain": "app.domain.mission.attribution",
    "MissionExplanationChainLayer": "app.domain.mission.attribution",
    "FeasibilityAcknowledgement": "app.domain.mission.feasibility",
    "FeasibilityEffect": "app.domain.mission.feasibility",
    "MissionExecutionContext": "app.domain.mission.context",
    "MISSION_INTELLIGENCE_VERSION": "app.domain.mission.mission",
    "Mission": "app.domain.mission.mission",
    "MissionRegenerationIdentity": "app.domain.mission.mission",
    "MissionScope": "app.domain.mission.mission",
    "MissionTask": "app.domain.mission.task",
    "RecommendationLanguageHook": "app.domain.mission.task",
    "THIN_MISSION_WARRANT_POSTURES": "app.domain.mission.warrant",
    "MissionWarrantPosture": "app.domain.mission.warrant",
    "aggregate_mission_warrant": "app.domain.mission.warrant",
    "inherit_mission_warrant": "app.domain.mission.warrant",
    "MissionIntelligence": "app.domain.mission.engine",
    "MissionEngine": "app.domain.mission.engine",
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
