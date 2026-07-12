"""Decision Engine domain package.

Read-side next-action selection from Twin + ReadinessState + CurriculumContext
+ Goals + Constraints. Not a Twin write domain. Not an Update Strategy.
No scoring formulas, pass probability, or missions.

Decision selects the next action and authors reason codes. Product-facing
suggestion packaging (titles, journal affordances, narration) belongs to the
separate Recommendation Engine package (``app.domain.recommendation``) —
Decision does not own product titles. Session/day Mission composition belongs
to Mission Intelligence (``app.domain.mission``) — Decision does not own day
composition; Mission operationalises Decision and never re-selects.

Imports are lazy via ``__getattr__`` so Twin write-path packages can load
without circular import deadlocks when decision is imported first.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "ACTION_FAMILY_CATALOGUE",
    "ENGINE_VERSION",
    "REASON_CODE_CATALOGUE",
    "REASON_CODE_VOCABULARY_VERSION",
    "ActionFamily",
    "ActionIntent",
    "CandidateAction",
    "CandidateStatus",
    "ConstraintAcknowledgement",
    "ConstraintClass",
    "Constraints",
    "Decision",
    "DecisionEngine",
    "DecisionHistory",
    "DecisionLineage",
    "DecisionScope",
    "DecisionState",
    "DecisionWarrantPosture",
    "FeasibilityEnvelope",
    "HistoryEntry",
    "HistoryOutcome",
    "IntensityPosture",
    "JournalLinkage",
    "ReasonCodeFamily",
    "ReasonCodeId",
    "ReasonCodeRef",
    "SelectedAction",
]

_EXPORT_MODULES = {
    "ACTION_FAMILY_CATALOGUE": "app.domain.decision.action_types",
    "ActionFamily": "app.domain.decision.action_types",
    "ActionIntent": "app.domain.decision.action_types",
    "SelectedAction": "app.domain.decision.action_types",
    "ENGINE_VERSION": "app.domain.decision.reason_codes",
    "REASON_CODE_CATALOGUE": "app.domain.decision.reason_codes",
    "REASON_CODE_VOCABULARY_VERSION": "app.domain.decision.reason_codes",
    "ReasonCodeFamily": "app.domain.decision.reason_codes",
    "ReasonCodeId": "app.domain.decision.reason_codes",
    "ReasonCodeRef": "app.domain.decision.reason_codes",
    "CandidateAction": "app.domain.decision.candidate",
    "CandidateStatus": "app.domain.decision.candidate",
    "FeasibilityEnvelope": "app.domain.decision.candidate",
    "ConstraintClass": "app.domain.decision.constraints",
    "Constraints": "app.domain.decision.constraints",
    "IntensityPosture": "app.domain.decision.constraints",
    "DecisionHistory": "app.domain.decision.history",
    "HistoryEntry": "app.domain.decision.history",
    "HistoryOutcome": "app.domain.decision.history",
    "ConstraintAcknowledgement": "app.domain.decision.decision",
    "Decision": "app.domain.decision.decision",
    "DecisionLineage": "app.domain.decision.decision",
    "DecisionScope": "app.domain.decision.decision",
    "DecisionWarrantPosture": "app.domain.decision.decision",
    "DecisionState": "app.domain.decision.decision_state",
    "JournalLinkage": "app.domain.decision.decision_state",
    "DecisionEngine": "app.domain.decision.engine",
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
