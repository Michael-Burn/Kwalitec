"""Student Home DTOs (SOP-001 / DX-005A / DX-006B / UX-001 / KWP-013).

Command-centre presentation only — projects existing Experience VMs.
No learning, recommendation, or session algorithm changes.

KWP-013 attaches an Adaptive Study Workspace projection so Home reads as
one coherent study environment rather than independent feature cards.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.presentation.student.dto.adaptive_workspace import AdaptiveStudyWorkspace


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
    # primary_kind: link | start_form | complete_runtime_c | revision_ack | none
    primary_href: str = ""
    duration_label: str = ""
    mission_id: str = ""
    session_id: str = ""
    recommendation_key: str = ""
    # UX-001 mission card enrichment (presentation only)
    title: str = ""
    difficulty_label: str = ""
    learning_objective: str = ""


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
class HomeStudySignals:
    """UX-001 compact orientation strip — one glance, no duplicate widgets."""

    subject_label: str = ""
    streak_label: str = ""
    progress_label: str = ""
    progress_percent: int | None = None
    countdown_label: str = ""
    estimated_study_label: str = ""


@dataclass(frozen=True)
class HomeBriefingSection:
    """Exam Week Briefing block on Home (KWP-006)."""

    has_briefing: bool = False
    title: str = "This Week"
    strengthened: tuple[str, ...] = ()
    needs_reinforcement: tuple[str, ...] = ()
    consistency_label: str = ""
    recommended_focus: str = ""
    recommended_detail: str = ""
    readiness_stage: str = ""
    summary_line: str = ""


@dataclass(frozen=True)
class HomeInsightRow:
    """One Home insight answering a command-centre question."""

    kind: str
    label: str
    body: str


@dataclass(frozen=True)
class StudentHomePage:
    """Student Home command centre (SOP-001 / UX-001 / KWP-006 / KWP-013).

    Surfaces: Adaptive Study Workspace (primary), Today's Mission, study
    signals, Exam Week Briefing (folded into workspace when present),
    Quick Actions. History owns session archives — ``recent_progress``
    stays empty as a queue; progress narrative lives on the workspace.
    Exam countdown lives in signals (not a second widget).
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
    greeting: str = "Welcome back."
    mission_section_title: str = "Today's Mission"
    signals: HomeStudySignals | None = None
    tutor_available: bool = False
    tutor_href: str = ""
    # KWP-006 — Exam Week Briefing + Home Insights (presentation only).
    briefing: HomeBriefingSection | None = None
    insights: tuple[HomeInsightRow, ...] = ()
    syllabus_position: str = ""
    # KWP-013 — Adaptive Study Workspace composition.
    workspace: AdaptiveStudyWorkspace | None = None
    # PX-004 / PX-B-048 — presentation density by account state (not selection).
    # day_zero | returning | established
    density_mode: str = "established"
    continuity_line: str = ""
    show_progress_strip: bool = True
    show_quick_actions: bool = True
    # PX-005 / PX-B-045 — calm near-exam support line (presentation only).
    exam_horizon_line: str = ""
    # PX-005 / PX-B-009 — honest preparing state when mission inventory unsettled.
    preparing_mission: bool = False
    # PX-006 / PX-B-046 — light Continuity Front / arc milestone acknowledgement.
    milestone_acknowledgement: str = ""
    # PX-006 / PX-B-047 — calm diligence reinforcement (no streak punishment).
    diligence_line: str = ""
    # Honest Progress: qualifying study day streak (plain count, including 0).
    current_streak_days: int = 0
    progress_href: str = ""
