"""Application-layer exceptions for the Adaptive Decision Engine.

Framework-independent. Raised when decision inputs or policies are violated.
"""

from __future__ import annotations


class AdaptiveLearningError(Exception):
    """Base exception for Adaptive Decision Engine failures."""


class DecisionError(AdaptiveLearningError):
    """A decision could not be produced."""


class PriorityError(AdaptiveLearningError):
    """Priority calculation failed."""


class ROIError(AdaptiveLearningError):
    """Educational ROI estimation failed."""


class RevisionPlanError(AdaptiveLearningError):
    """Revision plan could not be produced."""


class InterventionSelectionError(AdaptiveLearningError):
    """Intervention selection failed."""


class ExplanationError(AdaptiveLearningError):
    """Explanation could not be produced."""


class PolicyViolation(AdaptiveLearningError):  # noqa: N818
    """An adaptive-learning policy rejected the operation."""


class InsufficientEvidence(AdaptiveLearningError):  # noqa: N818
    """Not enough Twin evidence to make a confident revision decision."""


class UnsupportedIntervention(AdaptiveLearningError):  # noqa: N818
    """Requested intervention type is not implemented in this phase."""
