"""Independent recommendation rules for FOS-006 Version 1."""

from __future__ import annotations

from app.founder.recommendations.rules.archive_validation import (
    ArchiveValidationFailedRule,
)
from app.founder.recommendations.rules.engineering_health import (
    EngineeringHealthBelowThresholdRule,
)
from app.founder.recommendations.rules.high_duplicate_feedback import (
    HighDuplicateFeedbackRule,
)
from app.founder.recommendations.rules.no_active_capabilities import (
    NoActiveCapabilitiesRule,
)
from app.founder.recommendations.rules.no_internal_alpha import (
    NoInternalAlphaFeedbackRule,
)
from app.founder.recommendations.rules.protocols import RecommendationRule


def default_rules() -> tuple[RecommendationRule, ...]:
    """Return the Version 1 rule set in registration order."""
    return (
        NoInternalAlphaFeedbackRule(),
        ArchiveValidationFailedRule(),
        EngineeringHealthBelowThresholdRule(),
        HighDuplicateFeedbackRule(),
        NoActiveCapabilitiesRule(),
    )


__all__ = [
    "ArchiveValidationFailedRule",
    "EngineeringHealthBelowThresholdRule",
    "HighDuplicateFeedbackRule",
    "NoActiveCapabilitiesRule",
    "NoInternalAlphaFeedbackRule",
    "RecommendationRule",
    "default_rules",
]
