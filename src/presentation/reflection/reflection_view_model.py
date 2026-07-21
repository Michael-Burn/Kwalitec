"""Immutable view models for the Reflection Workspace surface.

Presentation containers only. Fields are already-formatted display strings and
Design System components — never domain aggregates or educational decision
objects. Captures student evidence chrome; does not interpret it.
"""

from __future__ import annotations

from dataclasses import dataclass

from presentation.design_system import (
    Badge,
    Button,
    Card,
    ContainerWidth,
    PageHeader,
    Section,
)
from presentation.reflection.confidence_scale import ConfidenceScaleView


@dataclass(frozen=True, slots=True)
class ConfidenceFieldView:
    """Confidence self-report capture field."""

    prompt: str
    scale: ConfidenceScaleView
    section: Section
    value_label: str = ""


@dataclass(frozen=True, slots=True)
class MissionCompletionFieldView:
    """Mission / session completion status chrome (presentation only)."""

    label: str
    detail: str
    is_complete: bool
    badge: Badge
    section: Section
    checklist: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DifficultyFieldView:
    """Perceived-difficulty self-report capture field."""

    prompt: str
    scale: ConfidenceScaleView
    section: Section
    value_label: str = ""


@dataclass(frozen=True, slots=True)
class WeakConceptFieldView:
    """Student-noted weak concept capture field (free text)."""

    prompt: str
    placeholder: str
    value: str
    section: Section


@dataclass(frozen=True, slots=True)
class StudentNotesFieldView:
    """Student notes forwarded from the study session (display / edit chrome)."""

    prompt: str
    value: str
    section: Section


@dataclass(frozen=True, slots=True)
class ReflectionSummaryFieldView:
    """Read-only summary of captured reflection evidence fields."""

    headline: str
    detail: str
    lines: tuple[str, ...]
    card: Card
    section: Section


@dataclass(frozen=True, slots=True)
class ReflectionViewModel:
    """Structured reflection experience after a completed study session.

    Immutable and framework-independent. Composes Design System contracts only.
    Captures educational evidence chrome — never diagnoses or decides next work.
    """

    header: PageHeader
    confidence: ConfidenceFieldView
    mission_completion: MissionCompletionFieldView
    difficulty: DifficultyFieldView
    weak_concept: WeakConceptFieldView
    student_notes: StudentNotesFieldView
    reflection_summary: ReflectionSummaryFieldView
    primary_button: Button | None = None
    container_width: ContainerWidth = ContainerWidth.CONTENT
    session_id: str = ""
    mission_title: str = ""
    stage_label: str = ""
    is_ready: bool = False
