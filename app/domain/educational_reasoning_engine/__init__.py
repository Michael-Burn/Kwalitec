"""Educational Reasoning Engine domain (EI-007).

Determines highest-value educational actions from published curriculum, SCI,
learning evidence references, and Twin beliefs. Does not generate mission
text, Coach responses, UI content, or mutate trusted educational assets.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "DecisionExplanation",
    "DecisionType",
    "EducationalDecision",
    "EducationalReasoningEngine",
    "ExpectedOutcome",
    "NodeReasoningState",
    "PriorityCalculation",
    "REASONING_VERSION",
    "ReasoningContext",
    "ReasoningResult",
    "ReasoningResultItem",
    "ReasoningRule",
    "RuleProposal",
    "RuleProposalRecord",
    "clamp01",
    "default_rule_pack",
]

_EXPORT_MODULES = {
    "REASONING_VERSION": "app.domain.educational_reasoning_engine.version",
    "DecisionType": "app.domain.educational_reasoning_engine.decision_type",
    "ExpectedOutcome": "app.domain.educational_reasoning_engine.decision_type",
    "EducationalDecision": "app.domain.educational_reasoning_engine.decision",
    "clamp01": "app.domain.educational_reasoning_engine.decision",
    "DecisionExplanation": "app.domain.educational_reasoning_engine.explanation",
    "PriorityCalculation": "app.domain.educational_reasoning_engine.explanation",
    "RuleProposalRecord": "app.domain.educational_reasoning_engine.explanation",
    "NodeReasoningState": "app.domain.educational_reasoning_engine.context",
    "ReasoningContext": "app.domain.educational_reasoning_engine.context",
    "RuleProposal": "app.domain.educational_reasoning_engine.rules.base",
    "ReasoningRule": "app.domain.educational_reasoning_engine.rules.base",
    "default_rule_pack": "app.domain.educational_reasoning_engine.rules",
    "EducationalReasoningEngine": "app.domain.educational_reasoning_engine.engine",
    "ReasoningResult": "app.domain.educational_reasoning_engine.engine",
    "ReasoningResultItem": "app.domain.educational_reasoning_engine.engine",
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
