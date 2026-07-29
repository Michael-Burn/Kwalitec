"""Founder Home DTOs (DX-004A / DX-006B Phase 1).

Publication-centred presentation only — no KPI aggregates.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HomeQueueRow:
    """One Publication Queue or Recent Publications row."""

    title: str
    status_label: str = ""
    meta_label: str = ""
    href: str = ""


@dataclass(frozen=True)
class HomeCurrentWork:
    """L0 Current Work — subject, stage, one Primary."""

    subject_name: str
    stage_label: str
    primary_label: str
    primary_href: str
    supporting_text: str = ""


@dataclass(frozen=True)
class FounderHomePage:
    """Founder Home page model (DX-004A L0–L2)."""

    current_work: HomeCurrentWork | None
    queue: tuple[HomeQueueRow, ...]
    recent_publications: tuple[HomeQueueRow, ...]
    queue_truncated: bool
    empty_reason: str
    empty_action_label: str
    empty_action_href: str
    subjects_href: str
    page_title: str = "Home"
