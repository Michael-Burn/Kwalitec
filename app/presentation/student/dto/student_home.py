"""Student Home DTOs (DX-005A / DX-006B Phase 4).

Mission-centred presentation only — no KPI, coach, or Quick Action payloads.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HomeQueueRow:
    """One Learning Queue or Recent Progress row."""

    title: str
    status_label: str = ""
    meta_label: str = ""
    href: str = ""


@dataclass(frozen=True)
class HomeMission:
    """L0 Current Mission — subject, objective, one Primary."""

    subject_name: str
    objective: str
    status_label: str
    why_now: str
    after_completion: str
    primary_label: str
    primary_kind: str
    # primary_kind: link | start_form | revision_ack | none
    primary_href: str = ""
    duration_label: str = ""
    mission_id: str = ""
    session_id: str = ""
    recommendation_key: str = ""


@dataclass(frozen=True)
class StudentHomePage:
    """Student Home page model (DX-005A L0–L2)."""

    mission: HomeMission | None
    learning_queue: tuple[HomeQueueRow, ...]
    recent_progress: tuple[HomeQueueRow, ...]
    state: str
    # state: mission | day_complete | empty | quiet
    empty_reason: str
    empty_action_label: str
    empty_action_href: str
    day_complete_message: str = ""
    page_title: str = "Home"
