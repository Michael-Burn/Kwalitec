"""Shared product-language constants for presentation surfaces.

Aligned with knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md.
Presentation / documentation only — no educational authority.
"""

from __future__ import annotations

# Canonical product nouns (UI).
APPROVED_TERMS: tuple[str, ...] = (
    "Session",
    "Today's Session",
    "Publish",
    "Journey",
    "Learning Insights",
    "Revision",
    "Exam Readiness",
    "Curriculum Studio",
    "Evidence Gates",
    "Home",
)

# Rejected learner-facing synonyms (lowercase match).
REJECTED_SYNONYMS: tuple[str, ...] = (
    "study session",
    "learning session",
    "go live",
    "progress path",
    "twin insights",
    "student analysis",
    "digital twin",
    "student twin",
    "mission engine",
    "curriculum graph",
)

# Preferred primary CTAs.
STUDENT_PRIMARY_CTAS: tuple[str, ...] = (
    "Start Today's Session",
    "Begin Session",
    "Continue",
    "Submit Answer",
    "Continue to Summary",
    "Return Home",
)

FOUNDER_STUDIO_CTAS: tuple[str, ...] = (
    "Create Subject",
    "Open Workspace",
    "Advance to Next Stage",
    "Validate Curriculum",
    "Build Preview",
    "Approve Curriculum",
    "Publish Curriculum",
    "Assign Version",
)

STUDENT_NAV_LABELS: tuple[str, ...] = (
    "Home",
    "Journey",
    "Revision",
    "History",
    "Profile",
)

FOUNDER_PRIMARY_NAV_LABELS: tuple[str, ...] = (
    "Overview",
    "Operational Health",
    "Studio",
    "Intelligence",
    "Evidence Gates",
    "Feedback",
    "Research",
    "Vision Journal",
    "Releases",
    "Settings",
)
