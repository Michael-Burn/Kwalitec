"""Immutable view models for the Student Onboarding surface.

Presentation containers only. Fields are display strings and Design System
components — never domain aggregates or educational decision objects.
"""

from __future__ import annotations

from dataclasses import dataclass

from presentation.design_system import (
    Button,
    ContainerWidth,
    PageHeader,
    ProgressBar,
    Section,
    Stepper,
)


@dataclass(frozen=True, slots=True)
class OnboardingFieldView:
    """One labelled field on the current onboarding step."""

    name: str
    label: str
    value: str
    input_type: str = "text"
    help_text: str = ""
    required: bool = True
    options: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class OnboardingStepView:
    """Chrome for the active collection step."""

    key: str
    title: str
    description: str
    section: Section
    fields: tuple[OnboardingFieldView, ...]
    is_optional: bool = False


@dataclass(frozen=True, slots=True)
class OnboardingViewModel:
    """Structured first-run onboarding experience.

    Immutable and framework-independent. Collects declarations only —
    never diagnoses or recommends.
    """

    header: PageHeader
    stepper: Stepper
    progress_bar: ProgressBar
    current_step: OnboardingStepView
    primary_button: Button | None = None
    secondary_button: Button | None = None
    skip_button: Button | None = None
    primary_action_key: str = "advance"
    secondary_action_key: str = "back"
    skip_action_key: str = "skip"
    review_lines: tuple[str, ...] = ()
    container_width: ContainerWidth = ContainerWidth.CONTENT
    onboarding_id: str = ""
    student_id: str = ""
    status_label: str = ""
    progress_percent: float = 0.0
    is_complete: bool = False
    redirect_path: str = ""
