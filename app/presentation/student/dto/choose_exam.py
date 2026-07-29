"""Choose Exam DTOs (DX-005B / DX-006B Phase 5).

Discovery presentation only — no KPI, readiness %, or recommendation essays.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExamOfferingRow:
    """One Ready or Coming Soon catalogue row."""

    subject_key: str
    exam_code: str
    title: str
    description: str
    scope_label: str
    updated_label: str
    availability_label: str
    selectable: bool
    preparation_line: str = ""
    recommended: bool = False
    family: str = ""


@dataclass(frozen=True)
class SelectedExamSummary:
    """Quiet selected-exam summary on discovery / confirm."""

    exam_title: str
    exam_code: str
    qualification_stage: str
    expected_path: str
    estimated_duration: str
    next_step: str


@dataclass(frozen=True)
class ChooseExamFilterOption:
    """One select option for L1 filters."""

    value: str
    label: str


@dataclass(frozen=True)
class ChooseExamPage:
    """Choose Exam discovery page model (DX-005B L0–L2)."""

    ready_offerings: tuple[ExamOfferingRow, ...]
    coming_soon: tuple[ExamOfferingRow, ...]
    selected_key: str
    selected_summary: SelectedExamSummary | None
    query: str
    status_filter: str
    sort: str
    family_filter: str
    status_options: tuple[ChooseExamFilterOption, ...]
    sort_options: tuple[ChooseExamFilterOption, ...]
    family_options: tuple[ChooseExamFilterOption, ...]
    primary_enabled: bool
    empty_ready: bool
    zero_matches: bool
    page_title: str = "Choose Exam"
    primary_label: str = "Continue"
    support_line: str = "Select an exam to begin."
