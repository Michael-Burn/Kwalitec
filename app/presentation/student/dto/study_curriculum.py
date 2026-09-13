"""Study Curriculum presentation DTOs (read-and-present only)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StudyObservationPanelView:
    """Informational 'What Kwalitec has observed' panel for one objective.

    Never carries raw readiness enum names; copy is already translated.
    Purely additive: does not gate Study actions.
    """

    objective_id: str
    objective_label: str
    brand_heading: str
    scenario_heading: str
    evidence_lines: tuple[str, ...]
    body_paragraphs: tuple[str, ...]
    meaning_paragraphs: tuple[str, ...]
    next_step: str
    keep_in_mind: str


@dataclass(frozen=True)
class StudyTopicView:
    """One syllabus topic row on Study's Curriculum view."""

    topic_id: str
    topic_code: str
    title: str
    state: str
    state_label: str
    state_icon: str
    why_it_matters: str
    is_quiet: bool
    can_study: bool = False
    unavailable_reason: str = ""
    study_action_label: str = ""
    observations: tuple[StudyObservationPanelView, ...] = ()


@dataclass(frozen=True)
class StudySectionView:
    """One section heading plus its topics, in published order."""

    section_id: str
    title: str
    topics: tuple[StudyTopicView, ...]


@dataclass(frozen=True)
class StudentStudyCurriculumPage:
    """Study Curriculum destination: syllabus map with honest learning states."""

    page_title: str
    page_question: str
    surface: str
    subject_label: str
    subject_code: str
    coverage_label: str
    covered_count: int
    topic_count: int
    coverage_ratio: float
    sections: tuple[StudySectionView, ...]
    continue_href: str
    continue_label: str
    empty_reason: str
    empty_action_label: str
    empty_action_href: str
    prior_knowledge_claimed_count: int = 0
    prior_knowledge_claim_label: str = ""
