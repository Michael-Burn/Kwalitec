"""Study Session DTOs (DX-005C / DX-006B Phase 6).

Practice-first presentation only — no KPI, coach, or celebration payloads.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SessionPersistentContext:
    """Always-visible orientation — identity and position only."""

    subject: str
    chapter: str
    objective: str
    activity_label: str
    session_progress: str
    elapsed_label: str = ""


@dataclass(frozen=True)
class LearningTask:
    """L0 Current Learning Task — what to do now."""

    activity: str
    expected_outcome: str
    estimated_duration: str
    next_milestone: str
    instruction: str


@dataclass(frozen=True)
class SessionDisclosure:
    """Collapsed L2 / L3 supporting material."""

    title: str
    body: str
    open: bool = False


@dataclass(frozen=True)
class StudySessionPage:
    """DX-005C Study Session page model (L0–L3)."""

    page_title: str
    surface: str
    # surface: overview | activity | reflection | summary | complete
    context: SessionPersistentContext
    task: LearningTask
    primary_label: str
    primary_kind: str
    # primary_kind: begin_form | answer_form | advance_form |
    #               reflection_form | complete_form | none
    primary_enabled: bool
    blocking_issue: str
    exit_href: str
    exit_label: str
    # L1 practice content
    content_title: str
    content_body: str
    content_support: str
    answer_prompt: str
    show_answer_input: bool
    feedback_outcome: str
    feedback_explanation: str
    # L2 / L3
    disclosures: tuple[SessionDisclosure, ...]
    technical_lines: tuple[str, ...]
    session_id: str
    activity_id: str
    mission_id: str = ""
