"""Immutable Founder Weekly Briefing models (FOS-007).

Deterministic executive report cargo. Sections are assembled from
predefined templates — no AI, LLM, or free-form NLG.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.founder.briefing.config import REPORT_VERSION

__all__ = [
    "REPORT_VERSION",
    "BriefMetadata",
    "BriefSection",
    "FounderWeeklyBrief",
]


@dataclass(frozen=True)
class BriefSection:
    """One ordered section of the weekly briefing."""

    title: str
    content: str
    order: int


@dataclass(frozen=True)
class BriefMetadata:
    """Footer metadata for a generated weekly briefing."""

    generated_at: datetime
    snapshot_version: str
    report_version: str


@dataclass(frozen=True)
class FounderWeeklyBrief:
    """Immutable Founder Weekly Briefing report.

    Constructed only from FounderOperationalState and RecommendationSet.
    Advisory / documentary — never authorises releases or mutations.
    """

    week: str
    generated_at: datetime
    snapshot_version: str
    recommendation_version: str
    executive_summary: BriefSection
    engineering_summary: BriefSection
    internal_alpha_summary: BriefSection
    capability_summary: BriefSection
    release_summary: BriefSection
    priorities: BriefSection
    recommendations: BriefSection
    risks: BriefSection
    next_week_focus: BriefSection
    metadata: BriefMetadata

    def ordered_sections(self) -> tuple[BriefSection, ...]:
        """Return all body sections sorted by ``order``."""
        sections = (
            self.executive_summary,
            self.engineering_summary,
            self.internal_alpha_summary,
            self.capability_summary,
            self.release_summary,
            self.priorities,
            self.recommendations,
            self.risks,
            self.next_week_focus,
        )
        return tuple(sorted(sections, key=lambda section: section.order))
