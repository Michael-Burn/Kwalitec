"""Modular inference rules package (EI-006)."""

from __future__ import annotations

from app.domain.twin_inference.rules.assessment_outcomes import AssessmentOutcomeRule
from app.domain.twin_inference.rules.base import (
    InferenceContext,
    InferenceRule,
    RuleContribution,
)
from app.domain.twin_inference.rules.evidence_weighting import EvidenceWeightingRule
from app.domain.twin_inference.rules.prerequisite_awareness import (
    PrerequisiteAwarenessRule,
)
from app.domain.twin_inference.rules.recency import RecencyRule, recency_factor
from app.domain.twin_inference.rules.repeated_attempts import RepeatedAttemptsRule
from app.domain.twin_inference.rules.revision_events import RevisionEventRule


def default_rule_pack() -> tuple[InferenceRule, ...]:
    """Ordered deterministic rule pack for ``tie.v1``.

    Prerequisite awareness runs last so it can read provisional mastery.
    """
    return (
        EvidenceWeightingRule(),
        RecencyRule(),
        RepeatedAttemptsRule(),
        AssessmentOutcomeRule(),
        RevisionEventRule(),
        PrerequisiteAwarenessRule(),
    )


__all__ = [
    "AssessmentOutcomeRule",
    "EvidenceWeightingRule",
    "InferenceContext",
    "InferenceRule",
    "PrerequisiteAwarenessRule",
    "RecencyRule",
    "RepeatedAttemptsRule",
    "RevisionEventRule",
    "RuleContribution",
    "default_rule_pack",
    "recency_factor",
]
