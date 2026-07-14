"""Configuration constants for Founder Weekly Briefing (FOS-007).

All wording and ordering are explicit. No AI / LLM tuning.
"""

from __future__ import annotations

# Report / cargo contract versions.
REPORT_VERSION = "1.0"
RECOMMENDATION_VERSION = "1.0"

# Canonical export filenames (writers only; no business logic).
MARKDOWN_FILENAME = "FOUNDER_WEEKLY_REPORT.md"
JSON_FILENAME = "founder_weekly_report.json"

# Section titles and stable order (1-based).
SECTION_EXECUTIVE_SUMMARY = "Executive Summary"
SECTION_ENGINEERING = "Engineering Overview"
SECTION_INTERNAL_ALPHA = "Internal Alpha"
SECTION_CAPABILITY = "Capability Progress"
SECTION_RELEASE = "Release Readiness"
SECTION_PRIORITIES = "Top Priorities"
SECTION_RECOMMENDATIONS = "Recommendations"
SECTION_RISKS = "Risks"
SECTION_NEXT_WEEK = "Next Week Focus"

SECTION_SPECS: tuple[tuple[int, str], ...] = (
    (1, SECTION_EXECUTIVE_SUMMARY),
    (2, SECTION_ENGINEERING),
    (3, SECTION_INTERNAL_ALPHA),
    (4, SECTION_CAPABILITY),
    (5, SECTION_RELEASE),
    (6, SECTION_PRIORITIES),
    (7, SECTION_RECOMMENDATIONS),
    (8, SECTION_RISKS),
    (9, SECTION_NEXT_WEEK),
)

REQUIRED_SECTION_TITLES: tuple[str, ...] = tuple(title for _, title in SECTION_SPECS)

# How many recommendations appear in Top Priorities / Next Week Focus.
TOP_PRIORITY_LIMIT = 3

# Risk priorities surfaced in the Risks section.
RISK_PRIORITIES: frozenset[str] = frozenset({"Critical", "High"})
