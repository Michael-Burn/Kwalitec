"""Founder Weekly Briefing (FOS-007).

Converts FounderOperationalState and RecommendationSet into a deterministic
executive weekly report.

Version 1 is template-driven — no AI, no LLMs, no Dashboard, no free-form NLG.
"""

from __future__ import annotations

from app.founder.briefing.models import (
    BriefMetadata,
    BriefSection,
    FounderWeeklyBrief,
)
from app.founder.briefing.services import FounderWeeklyBriefingService

__all__ = [
    "BriefMetadata",
    "BriefSection",
    "FounderWeeklyBrief",
    "FounderWeeklyBriefingService",
]
