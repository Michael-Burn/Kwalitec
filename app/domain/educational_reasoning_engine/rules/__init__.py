"""Modular reasoning rules package (EI-007)."""

from __future__ import annotations

from app.domain.educational_reasoning_engine.rules.base import (
    ReasoningRule,
    RuleProposal,
)
from app.domain.educational_reasoning_engine.rules.effort_estimation import (
    EffortEstimationRule,
)
from app.domain.educational_reasoning_engine.rules.incomplete_paths import (
    IncompletePathsRule,
)
from app.domain.educational_reasoning_engine.rules.low_confidence import (
    LowConfidenceRule,
)
from app.domain.educational_reasoning_engine.rules.prerequisite_satisfaction import (
    PrerequisiteSatisfactionRule,
)
from app.domain.educational_reasoning_engine.rules.revision_due import RevisionDueRule
from app.domain.educational_reasoning_engine.rules.study_continuity import (
    StudyContinuityRule,
)
from app.domain.educational_reasoning_engine.rules.syllabus_priority import (
    SyllabusPriorityRule,
)
from app.domain.educational_reasoning_engine.rules.topic_dependency import (
    TopicDependencyRule,
)


def default_rule_pack() -> tuple[ReasoningRule, ...]:
    """Ordered deterministic rule pack for ``ere.v1``."""
    return (
        PrerequisiteSatisfactionRule(),
        LowConfidenceRule(),
        IncompletePathsRule(),
        RevisionDueRule(),
        SyllabusPriorityRule(),
        TopicDependencyRule(),
        EffortEstimationRule(),
        StudyContinuityRule(),
    )


__all__ = [
    "EffortEstimationRule",
    "IncompletePathsRule",
    "LowConfidenceRule",
    "PrerequisiteSatisfactionRule",
    "ReasoningRule",
    "RevisionDueRule",
    "RuleProposal",
    "StudyContinuityRule",
    "SyllabusPriorityRule",
    "TopicDependencyRule",
    "default_rule_pack",
]
