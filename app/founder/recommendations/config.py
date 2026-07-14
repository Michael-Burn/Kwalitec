"""Configuration constants for Founder Recommendation Engine (FOS-006).

Thresholds are explicit and deterministic. No AI / ML tuning.
"""

from __future__ import annotations

# Engineering health: fire when tests fail or validation errors exceed this.
ENGINEERING_VALIDATION_ERROR_THRESHOLD = 0

# Duplicate feedback: fire when absolute count or ratio is met (feedback > 0).
DUPLICATE_FEEDBACK_ABSOLUTE_THRESHOLD = 3
DUPLICATE_FEEDBACK_RATIO_THRESHOLD = 0.4

# Priority labels (highest → lowest for sorting).
PRIORITY_CRITICAL = "Critical"
PRIORITY_HIGH = "High"
PRIORITY_MEDIUM = "Medium"
PRIORITY_LOW = "Low"

PRIORITY_ORDER: tuple[str, ...] = (
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    PRIORITY_LOW,
)

PRIORITY_RANK: dict[str, int] = {
    PRIORITY_CRITICAL: 0,
    PRIORITY_HIGH: 1,
    PRIORITY_MEDIUM: 2,
    PRIORITY_LOW: 3,
}

# Recommendation categories.
CATEGORY_RELEASE = "release"
CATEGORY_ARCHIVE = "archive"
CATEGORY_ENGINEERING = "engineering"
CATEGORY_FEEDBACK = "feedback"
CATEGORY_ROADMAP = "roadmap"

# Overall status derived from highest-priority recommendation present.
STATUS_HEALTHY = "healthy"
STATUS_ADVISORY = "advisory"
STATUS_ATTENTION = "attention"
STATUS_CRITICAL = "critical"

# Template identifiers (stable recommendation ids for V1).
TEMPLATE_WAIT_FOR_INTERNAL_ALPHA = "wait_for_internal_alpha"
TEMPLATE_RESOLVE_ARCHIVE_INCONSISTENCIES = "resolve_archive_inconsistencies"
TEMPLATE_PAUSE_FOR_ENGINEERING_HEALTH = "pause_for_engineering_health"
TEMPLATE_PRIORITISE_RECURRING_ISSUES = "prioritise_recurring_issues"
TEMPLATE_SELECT_ROADMAP_CAPABILITY = "select_roadmap_capability"

ALL_TEMPLATE_IDS: frozenset[str] = frozenset(
    {
        TEMPLATE_WAIT_FOR_INTERNAL_ALPHA,
        TEMPLATE_RESOLVE_ARCHIVE_INCONSISTENCIES,
        TEMPLATE_PAUSE_FOR_ENGINEERING_HEALTH,
        TEMPLATE_PRIORITISE_RECURRING_ISSUES,
        TEMPLATE_SELECT_ROADMAP_CAPABILITY,
    }
)
