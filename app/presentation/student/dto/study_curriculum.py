"""Study Curriculum presentation DTOs (read-and-present only)."""

from __future__ import annotations

from dataclasses import dataclass


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
