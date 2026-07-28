"""Shared product-language constants for presentation surfaces.

Aligned with knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md and
knowledge/governance/CANONICAL_EDUCATIONAL_LEXICON.md (DG-001.1).

Presentation / documentation only — no educational authority.
RR-001.3A reconciles Mission (focus) vs Session (practice) without
retiring Session CTAs.
"""

from __future__ import annotations

# Canonical product + educational nouns (UI).
APPROVED_TERMS: tuple[str, ...] = (
    "Session",
    "Today's Session",
    "Mission",
    "Today's Mission",
    "Study Sensei",
    "Guidance",
    "Recommendation",
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
    "why this tip",
    "mission tip",
    "the system chose",
)

# Preferred primary CTAs.
# Session CTAs remain practice-entry labels (DG-001.1-D02); Mission is the
# educational focus noun, not a CTA synonym here.
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
    # PX-002A T1-1 / terminology standard: "Home" (not "Dashboard") and
    # "History" (not "Analytics") — see TERMINOLOGY_STANDARD.md.
    "Home",
    "Journey",
    "Revision",
    "History",
    "Settings",
    "Study Plan",
    "Help",
)

FOUNDER_PRIMARY_NAV_LABELS: tuple[str, ...] = (
    "Overview",
    "Operations",
    "Students",
    "Learning",
    "Assessments",
    "Content",
    "Analytics",
    "Platform",
    "Settings",
    "Support",
)
