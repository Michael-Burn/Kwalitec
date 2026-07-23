"""Policy governing how weak structural prerequisites influence mastery.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
Concept
    Prerequisite Influence Policy
"""

from __future__ import annotations

from domain.education.knowledge_graph.enums import DependencyStrengthBand
from domain.education.knowledge_graph.value_objects.dependency_strength import (
    DependencyStrength,
)
from domain.education.mastery_estimation.enums import KnowledgeGapSeverity
from domain.education.mastery_estimation.value_objects.mastery_score import (
    MasteryScore,
)

# A prerequisite below this magnitude is considered weak enough to
# structurally influence its dependents. Prerequisites with no evidence at
# all are never classified as weak — absence of data is not itself a
# demonstrated weakness.
_WEAK_PREREQUISITE_THRESHOLD = 0.50

# How strongly each structural dependency band dampens a dependent's
# mastery when the prerequisite is weak. A critical prerequisite that is
# entirely unmastered can dampen a dependent by up to 60%; an optional
# prerequisite dampens by at most 5%.
_BAND_INTENSITY: dict[DependencyStrengthBand, float] = {
    DependencyStrengthBand.CRITICAL: 0.60,
    DependencyStrengthBand.IMPORTANT: 0.40,
    DependencyStrengthBand.HELPFUL: 0.20,
    DependencyStrengthBand.OPTIONAL: 0.05,
}

_SEVERITY_ORDER: tuple[KnowledgeGapSeverity, ...] = (
    KnowledgeGapSeverity.MINOR,
    KnowledgeGapSeverity.MODERATE,
    KnowledgeGapSeverity.SEVERE,
    KnowledgeGapSeverity.CRITICAL,
)

_SEVERITY_FLOOR_BY_BAND: dict[DependencyStrengthBand, KnowledgeGapSeverity] = {
    DependencyStrengthBand.CRITICAL: KnowledgeGapSeverity.SEVERE,
    DependencyStrengthBand.IMPORTANT: KnowledgeGapSeverity.MODERATE,
    DependencyStrengthBand.HELPFUL: KnowledgeGapSeverity.MINOR,
    DependencyStrengthBand.OPTIONAL: KnowledgeGapSeverity.MINOR,
}

_ESCALATION_DEFICIENCY_THRESHOLD = 0.50
_CRITICAL_ESCALATION_DEFICIENCY_THRESHOLD = 0.75


class PrerequisiteInfluencePolicy:
    """Deterministically classifies and weighs weak structural prerequisites.

    Every decision here is table-driven from the prerequisite's own
    mastery magnitude and the structural ``DependencyStrength`` of the edge
    connecting it to its dependent — never from randomness or estimation.
    """

    @staticmethod
    def is_weak(prerequisite_score: MasteryScore) -> bool:
        """True when a prerequisite is weak enough to influence dependents.

        A prerequisite with no evidence at all is never classified as weak
        — this policy cannot judge what it has not observed.
        """
        return (
            prerequisite_score.evidence_count > 0
            and prerequisite_score.magnitude < _WEAK_PREREQUISITE_THRESHOLD
        )

    @staticmethod
    def dampening_factor(
        strength: DependencyStrength, prerequisite_score: MasteryScore
    ) -> float:
        """Multiplicative dampening factor applied to a dependent's mastery."""
        if not PrerequisiteInfluencePolicy.is_weak(prerequisite_score):
            return 1.0
        deficiency = 1.0 - prerequisite_score.magnitude
        intensity = _BAND_INTENSITY[strength.band]
        factor = 1.0 - (deficiency * intensity)
        return max(0.0, min(1.0, factor))

    @staticmethod
    def classify_severity(
        prerequisite_score: MasteryScore, strength: DependencyStrength
    ) -> KnowledgeGapSeverity:
        """Severity of a weak-prerequisite gap.

        The structural strength of the dependency sets a severity floor;
        a sufficiently large deficiency escalates by one band, and a
        critical-strength prerequisite with a very large deficiency always
        escalates to ``CRITICAL``.
        """
        deficiency = 1.0 - prerequisite_score.magnitude
        floor = _SEVERITY_FLOOR_BY_BAND[strength.band]
        floor_index = _SEVERITY_ORDER.index(floor)
        if (
            strength.band is DependencyStrengthBand.CRITICAL
            and deficiency >= _CRITICAL_ESCALATION_DEFICIENCY_THRESHOLD
        ):
            return KnowledgeGapSeverity.CRITICAL
        if deficiency >= _ESCALATION_DEFICIENCY_THRESHOLD:
            escalated_index = min(floor_index + 1, len(_SEVERITY_ORDER) - 1)
            return _SEVERITY_ORDER[escalated_index]
        return floor
