"""Explainability enumerations.

Vocabulary for deterministic EducationalExplanation projections. Sections
follow the four-question explainability framework. Traces and evidence
references cite Educational OS decisions — they never invent mastery or
invoke AI.
"""

from __future__ import annotations

from enum import StrEnum


class ExplanationSectionKind(StrEnum):
    """Four-question explainability section catalogue.

    Maps to EIP-003: What we know / What we estimate / Why / What next.
    """

    OBSERVED_FACTS = "observed_facts"
    ESTIMATES = "estimates"
    WHY = "why"
    NEXT_ACTION = "next_action"


class DecisionStage(StrEnum):
    """Ordered educational decision stages in a DecisionTrace."""

    MISSION = "mission"
    STUDY_PLAN = "study_plan"
    PROGRESS = "progress"
    RECOMMENDATION = "recommendation"


class EvidenceSourceKind(StrEnum):
    """Lawful Educational OS sources cited by EvidenceReference."""

    MISSION = "mission"
    STUDY_PLAN = "study_plan"
    PROGRESS = "progress"
    RECOMMENDATION = "recommendation"
    TWIN = "twin"
    DIAGNOSIS = "diagnosis"
    PRIORITY = "priority"
    STRATEGY = "strategy"
