"""Student Home DTOs (SOP-001 / DX-005A / DX-006B).

Command-centre presentation only — projects existing Experience VMs.
No learning, recommendation, or session algorithm changes.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HomeQueueRow:
    """One attention row (Learning Queue heritage / Quick Action source)."""

    title: str
    status_label: str = ""
    meta_label: str = ""
    href: str = ""


@dataclass(frozen=True)
class HomeMission:
    """Today's Mission or Continue Session — subject, objective, one Primary."""

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
class HomeExamination:
    """Current Examination — identity context for today's work."""

    label: str
    countdown_label: str = ""
    detail: str = ""


@dataclass(frozen=True)
class HomeStudyHealth:
    """Calm study-health signal — not a KPI wall."""

    status_label: str
    detail: str = ""
    tone: str = "neutral"  # neutral | positive | caution


@dataclass(frozen=True)
class HomeDeadline:
    """One upcoming deadline / milestone row."""

    title: str
    detail: str = ""


@dataclass(frozen=True)
class HomeQuickAction:
    """Contextual next-step shortcut answering “what should I do now?”."""

    label: str
    href: str
    detail: str = ""


@dataclass(frozen=True)
class StudentHomePage:
    """Student Home command centre (SOP-001).

    Surfaces: Today's Mission / Continue Session, Current Examination,
    Study Health, Quick Actions, Upcoming Deadlines.

    History owns session archives — ``recent_progress`` stays empty.
    """

    mission: HomeMission | None
    learning_queue: tuple[HomeQueueRow, ...]
    recent_progress: tuple[HomeQueueRow, ...]
    examination: HomeExamination | None
    study_health: HomeStudyHealth | None
    quick_actions: tuple[HomeQuickAction, ...]
    deadlines: tuple[HomeDeadline, ...]
    state: str
    # state: mission | day_complete | empty | quiet
    empty_reason: str
    empty_action_label: str
    empty_action_href: str
    day_complete_message: str = ""
    page_title: str = "Home"
    page_question: str = "What should I do now?"
    mission_section_title: str = "Today's Mission"
