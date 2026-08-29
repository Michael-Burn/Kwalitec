"""Immutable educational package models (EA-006 publication units)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class KnowledgeCheckChoice:
    """One MCQ option for a Knowledge Check (checkpoint / active recall)."""

    id: str
    label: str
    misconception_tag: str = ""


@dataclass(frozen=True)
class KnowledgeCheck:
    """One Active Recall or Checkpoint item from a certified package."""

    episode_id: str
    kind: str
    item_id: str
    title: str
    prompt: str
    response_type: str = "short_structured"
    body: str = ""
    hints: tuple[str, ...] = ()
    accepted_keywords: tuple[str, ...] = ()
    explanation: str = ""
    model_answer: str = ""
    common_mistake: str = ""
    success_criteria: tuple[str, ...] = ()
    # MCQ fields — unused for short_structured; additive and optional.
    choices: tuple[KnowledgeCheckChoice, ...] = ()
    correct_choice_id: str = ""


@dataclass(frozen=True)
class ReadingGuidance:
    """CMP Reading Guidance instance (EA-004 architecture)."""

    lead_line: str
    focus_questions: tuple[str, ...]
    misconception_watch: tuple[str, ...]
    open_point: str
    stop_condition: str
    out_of_scope_today: tuple[str, ...]
    annotation_task: str
    attempt_before_reveal: str
    exit_line: str
    return_cue: str
    pause_points: tuple[dict[str, str], ...]
    reentry_line: str


@dataclass(frozen=True)
class TomorrowPreviewPack:
    """Tomorrow Preview fields (Gate TP)."""

    next_topic_code: str
    next_topic_title: str
    continuity_line: str
    light_prep_cue: str = ""
    student_facing: str = ""


@dataclass(frozen=True)
class WorkedExampleGiven:
    """One concrete given value in a genuine numeric worked example."""

    symbol: str
    value: str
    note: str = ""


@dataclass(frozen=True)
class WorkedExampleStep:
    """One labelled step in a genuine numeric worked example."""

    id: str
    label: str
    attempt_cue: str = ""
    explanation: str = ""
    calculation: str = ""
    result: str = ""


@dataclass(frozen=True)
class WorkedExample:
    """Genuine step-by-step numeric worked example (optional package artefact).

    Distinct from the structure-walkthrough scaffold assembled from mission /
    reading fields. Presence is gated by a non-empty ``steps`` tuple.
    """

    title: str = ""
    problem_statement: str = ""
    given: tuple[WorkedExampleGiven, ...] = ()
    attempt_before_reveal: str = ""
    steps: tuple[WorkedExampleStep, ...] = ()
    final_answer: str = ""
    common_pitfall: str = ""
    syllabus_ref: str = ""


@dataclass(frozen=True)
class CertifiedEducationalPackage:
    """One publication-approved Mission+Session educational package."""

    package_id: str
    package_version: str
    publication_version: str
    status: str
    subject_id: str
    topic_code: str
    topic_title: str
    topic_aliases: tuple[str, ...]
    topic_title_keywords: tuple[str, ...]
    golden_id: str
    mode: str
    display_title: str
    mission_purpose: str
    learning_objective: str
    concept_focus: str
    prior_bridge: str
    why_now: str
    expected_benefit: str
    explainability: str
    success_criteria: tuple[str, ...]
    task_descriptions: tuple[str, ...]
    student_brief: str
    session_purpose: str
    wrap_up: str
    confidence_prompt: str
    reading: ReadingGuidance
    knowledge_checks: tuple[KnowledgeCheck, ...]
    reflection_framing: str
    reflection_prompt: str
    reflection_prompts: tuple[str, ...]
    tomorrow: TomorrowPreviewPack
    campaign_id: str = ""
    campaign_day: str = ""
    estimated_minutes_min: int = 50
    estimated_minutes_max: int = 70
    source_path: str = ""
    certification_refs: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    # Genuine numeric walkthrough — optional; None / empty steps → scaffold.
    worked_example: WorkedExample | None = None

    @property
    def is_publication_approved(self) -> bool:
        return (self.status or "").strip().lower() in {
            "publication_approved",
            "approved",
            "certified",
        }

    @property
    def mission_narrative(self) -> str:
        # Student-facing fallback when student_brief is empty.
        # Omit prior_bridge: campaign/LO continuity prose often leaks
        # authoring jargon onto Session Overview why_today. why_now alone
        # is the certified student-safe rationale; concept_focus is projected
        # separately on the episode.
        return (self.why_now or "").strip()

    @property
    def educational_rationale(self) -> str:
        return (self.why_now or self.explainability or self.mission_purpose).strip()

    @property
    def estimated_duration_minutes(self) -> int:
        mid = (self.estimated_minutes_min + self.estimated_minutes_max) // 2
        return mid if mid > 0 else 60
