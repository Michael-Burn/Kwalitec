"""Shared product-language constants for presentation surfaces.

Aligned with knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md and
knowledge/governance/CANONICAL_EDUCATIONAL_LEXICON.md (DG-001.1).

Presentation / documentation only — no educational authority.
RR-001.3A reconciles Mission (focus) vs Session (practice) without
retiring Session CTAs.
RR-001.3B publishes reflection-family and orientation constants
(DG-001.3 / EGC-R03–R05).
RR-001.3C publishes educational memory coherence constants
(DG-001.2-D06 / EGC-R06 / EGC-R12).
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
    "Decision Journal",
    "Educational Timeline",
    "History",
    "Session reflection",
    "Commitment reflection",
    "Sensei reflection",
    "Timeline reflection",
    "Guided Reflection preview",
    "Product Check-in",
    "Calibration",
)

# DG-001.3-D01 canonical student map (Help + orientation).
REFLECTION_FAMILY_MAP_SENTENCE: str = (
    "Reflection after a Session closes practice. "
    "Commitment reflection on Home confirms you finished what you chose. "
    "Optional reflection in the Decision Journal helps the Study Sensei "
    "learn whether guidance was useful. "
    "The Educational Timeline asks deeper questions about your learning story. "
    "Product Check-in is feedback for the product team — not educational reflection."
)

# DG-001.2-D06 / EGC-R06 — one coherent educational memory model.
EDUCATIONAL_MEMORY_MODEL_SENTENCE: str = (
    "The Decision Journal is Study Sensei’s durable educational memory of "
    "significant guidance, your choices, and what followed. "
    "The Educational Timeline is the chronological learning story drawn from "
    "that Journal — not a second memory store and not a scoreboard. "
    "History keeps practice archives and progress stats as context; "
    "educational meaning lives in the Journal and Timeline. "
    "After a Reflection, Session notes stay with the Session; optional Sensei "
    "reflection deepens Journal memory that Timeline can later interpret."
)

HISTORY_EPISTEMOLOGY_BRIDGE: str = (
    "History shows what you practiced — completed Sessions, study time, and "
    "readiness trends. Those numbers orient you; they are not Study Sensei’s "
    "mentor narrative. What happened educationally, why it mattered, what was "
    "learned, and how that shapes future guidance live in the Decision Journal "
    "and Educational Timeline."
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
    "daily reflection",
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
