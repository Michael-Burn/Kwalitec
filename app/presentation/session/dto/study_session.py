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
    #               reflection_form | complete_form | finish_review_form | none
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
    # UX-001 — reading progress for calm session chrome (0–100).
    reading_progress_percent: int = 0
    # LXP-003 / P2 product controls
    show_pause: bool = False
    finish_review_required: bool = False
    lifecycle_label: str = ""
    checklist: tuple[tuple[str, str, bool], ...] = ()
    # checklist items: (item_id, label, done)
    # LXP-004A / P3 educational substance
    learning_objectives: tuple[str, ...] = ()
    activity_type: str = ""
    stage_label: str = ""
    educational_flow_label: str = ""
    # UX-001 Session Overview briefing (relocated from Home)
    why_today: str = ""
    concept_focus: tuple[str, ...] = ()
    session_stages: tuple[str, ...] = ()
    expected_outcome: str = ""
    checkpoint_preview: str = ""
    reflection_preview: str = ""
    # KWP-002 completion moment
    journey_update_label: str = ""
    finish_outcome_label: str = ""
    learning_insights: tuple[str, ...] = ()
    next_recommendation: str = ""
    completion_headline: str = ""
    # KWP-004 assessable practice feedback
    model_answer: str = ""
    common_mistake: str = ""
    feedback_next_action: str = ""
    # KWP-005 Sitting Report
    what_studied: str = ""
    performance_summary: str = ""
    progress_explanation: str = ""
    tomorrow_preview: str = ""
    assessment_mode_active: bool = False
    assessment_summary: str = ""
    exercises_assigned: tuple[str, ...] = ()
    exercises_completed: tuple[str, ...] = ()
    strengthened: tuple[str, ...] = ()
    needs_reinforcement: tuple[str, ...] = ()
    syllabus_refs: tuple[str, ...] = ()
    sitting_report_ready: bool = False
    # KWP-007 Learning Strategy
    strategy_title: str = ""
    strategy_body: str = ""
    strategy_explanation: str = ""
    strategy_spacing_guidance: str = ""
    strategy_momentum_guidance: str = ""
    strategy_confidence_guidance: str = ""
    # KWP-008 Learning Diagnostics (guidance; never category labels)
    diagnostic_guidance: str = ""
    diagnostic_explanation: str = ""
    # KWP-009 Learning Difficulty (guidance; never band labels)
    difficulty_title: str = ""
    difficulty_guidance: str = ""
    difficulty_explanation: str = ""
    # KWP-010 Intervention Effectiveness (natural feedback; never verdict labels)
    effectiveness_feedback: str = ""
    effectiveness_explanation: str = ""
    # PX-003 — visible session journey chrome (presentation only)
    workflow_steps: tuple[str, ...] = ()
    workflow_step_index: int = 0
    page_eyebrow: str = ""
    estimated_time_label: str = ""
