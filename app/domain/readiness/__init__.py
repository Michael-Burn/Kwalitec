"""Readiness Aggregation domain package.

Read-side derivation of factorable sitting preparedness from Twin + Curriculum
+ Goals. Not a Twin write domain. Not an Update Strategy. No scoring formulas,
pass probability, or mission generation.

Readiness does **not** select next actions — that ownership belongs to the
separate Decision Engine package (``app.domain.decision``), which consumes
``ReadinessState`` as context only.

Imports are lazy via ``__getattr__`` so Twin write-path packages can load
without circular import deadlocks when readiness is imported first.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "CRITICAL_SITTING_FACTORS",
    "CurriculumContext",
    "CurriculumFormat",
    "CurriculumTopicRef",
    "FACTOR_CATALOGUE",
    "FactorAttribution",
    "FactorId",
    "FactorJudgement",
    "FactorPosture",
    "OverallPosture",
    "ReadinessAggregation",
    "ReadinessScope",
    "ReadinessState",
    "WarrantPosture",
]

_EXPORT_MODULES = {
    "CRITICAL_SITTING_FACTORS": "app.domain.readiness.factors",
    "FACTOR_CATALOGUE": "app.domain.readiness.factors",
    "FactorId": "app.domain.readiness.factors",
    "FactorPosture": "app.domain.readiness.factors",
    "OverallPosture": "app.domain.readiness.factors",
    "WarrantPosture": "app.domain.readiness.factors",
    "CurriculumContext": "app.domain.readiness.curriculum_context",
    "CurriculumFormat": "app.domain.readiness.curriculum_context",
    "CurriculumTopicRef": "app.domain.readiness.curriculum_context",
    "FactorAttribution": "app.domain.readiness.readiness_state",
    "FactorJudgement": "app.domain.readiness.readiness_state",
    "ReadinessScope": "app.domain.readiness.readiness_state",
    "ReadinessState": "app.domain.readiness.readiness_state",
    "ReadinessAggregation": "app.domain.readiness.aggregation",
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
