"""Providers for Founder Weekly Briefing (FOS-007)."""

from __future__ import annotations

from app.founder.briefing.providers.protocols import SectionBuilder
from app.founder.briefing.providers.section_provider import SectionTemplateProvider

__all__ = [
    "SectionBuilder",
    "SectionTemplateProvider",
]
