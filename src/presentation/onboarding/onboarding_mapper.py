"""OnboardingMapper — snapshot cargo → Design System field chrome.

Presentation mapping only. Never diagnoses, recommends, or persists.
"""

from __future__ import annotations

from typing import Any

from presentation.design_system import (
    Button,
    ProgressBar,
    Section,
    Stepper,
    StepperStep,
    ghost_button,
    primary_button,
    secondary_button,
)
from presentation.onboarding.onboarding_view_model import (
    OnboardingFieldView,
    OnboardingStepView,
)

_STEP_META: dict[str, tuple[str, str]] = {
    "welcome": (
        "Welcome",
        "A few short steps help Kwalitec begin from your real educational history "
        "— declarations only, not a test.",
    ),
    "ifoa_profile": (
        "IFoA Profile",
        "Tell us which pathway and paper you are preparing for.",
    ),
    "exam_history": (
        "Exam History",
        "Declare prior study and attempts for this paper — history, not scores.",
    ),
    "weekly_availability": (
        "Weekly Availability",
        "How much time can you typically give each week?",
    ),
    "confidence": (
        "Confidence",
        "Share a rough confidence band. This is a declaration, not a readiness score.",
    ),
    "study_habits": (
        "Study Habits",
        "How do you prefer to study? Preferences only — not a study plan.",
    ),
    "optional_diagnostic": (
        "Optional Diagnostic",
        "You may accept or skip a later optional diagnostic. Nothing is scored here.",
    ),
    "review": (
        "Review",
        "Confirm your declarations. After confirmation we initialise "
        "your Student Twin.",
    ),
}

_COLLECTION_ORDER: tuple[str, ...] = (
    "welcome",
    "ifoa_profile",
    "exam_history",
    "weekly_availability",
    "confidence",
    "study_habits",
    "optional_diagnostic",
    "review",
)


class OnboardingMapper:
    """Map onboarding snapshot fields into immutable presentation chrome."""

    @classmethod
    def map_stepper(cls, *, current_step: str, saved_steps: tuple[str, ...]) -> Stepper:
        saved = set(saved_steps)
        steps: list[StepperStep] = []
        for key in _COLLECTION_ORDER:
            title, _ = _STEP_META[key]
            steps.append(
                StepperStep(
                    label=title,
                    description="",
                    complete=key in saved and key != current_step,
                    current=key == current_step,
                )
            )
        return Stepper(steps=tuple(steps), label="Onboarding progress")

    @classmethod
    def map_progress(cls, percent: float) -> ProgressBar:
        return ProgressBar(
            label="Onboarding progress",
            percent=percent,
            value_text=f"{int(round(percent))}%",
        )

    @classmethod
    def map_current_step(
        cls,
        *,
        step_key: str,
        payloads: dict[str, dict[str, Any]],
    ) -> OnboardingStepView:
        title, description = _STEP_META.get(
            step_key, (step_key.replace("_", " ").title(), "")
        )
        section = Section(title=title, description=description)
        values = payloads.get(step_key, {})
        fields = cls._fields_for(step_key, values)
        return OnboardingStepView(
            key=step_key,
            title=title,
            description=description,
            section=section,
            fields=fields,
            is_optional=step_key == "optional_diagnostic",
        )

    @classmethod
    def map_review_lines(cls, payloads: dict[str, dict[str, Any]]) -> tuple[str, ...]:
        lines: list[str] = []
        profile = payloads.get("ifoa_profile", {})
        if profile:
            lines.append(
                f"Paper: {profile.get('exam_paper', '')} "
                f"({profile.get('pathway', '')})"
            )
        history = payloads.get("exam_history", {})
        if history:
            lines.append(
                f"History: {history.get('prior_study', '')}, "
                f"attempts={history.get('previous_attempts', 0)}, "
                f"intent={history.get('sitting_intent', '')}"
            )
        availability = payloads.get("weekly_availability", {})
        if availability:
            lines.append(
                "Availability: "
                f"weekday {availability.get('weekday_minutes', 0)} min, "
                f"weekend {availability.get('weekend_minutes', 0)} min, "
                f"session {availability.get('preferred_session_minutes', 0)} min"
            )
        confidence = payloads.get("confidence", {})
        if confidence:
            lines.append(f"Confidence: {confidence.get('band', '')}")
        habits = payloads.get("study_habits", {})
        if habits:
            lines.append(f"Habits: {habits.get('preference', '')}")
        diagnostic = payloads.get("optional_diagnostic", {})
        if diagnostic:
            lines.append(f"Diagnostic: {diagnostic.get('choice', 'skipped')}")
        return tuple(lines)

    @classmethod
    def primary_action(cls, *, step_key: str) -> Button:
        if step_key == "review":
            return primary_button("Confirm and build Student Twin")
        return primary_button("Continue")

    @classmethod
    def secondary_action(cls, *, step_key: str) -> Button | None:
        if step_key == "welcome":
            return None
        return secondary_button("Back")

    @classmethod
    def skip_action(cls, *, step_key: str) -> Button | None:
        if step_key != "optional_diagnostic":
            return None
        return ghost_button("Skip diagnostic")

    @classmethod
    def _fields_for(
        cls, step_key: str, values: dict[str, Any]
    ) -> tuple[OnboardingFieldView, ...]:
        if step_key == "welcome":
            return (
                OnboardingFieldView(
                    name="acknowledged",
                    label="I understand this collects history, not a diagnosis",
                    value=_as_str(values.get("acknowledged"), "false"),
                    input_type="checkbox",
                    required=True,
                ),
            )
        if step_key == "ifoa_profile":
            return (
                OnboardingFieldView(
                    name="pathway",
                    label="IFoA pathway",
                    value=_as_str(values.get("pathway")),
                    input_type="select",
                    options=(
                        ("core_principles", "Core Principles"),
                        ("core_practices", "Core Practices"),
                        ("specialist", "Specialist"),
                        ("other", "Other"),
                        ("unsure", "Unsure"),
                    ),
                ),
                OnboardingFieldView(
                    name="exam_paper",
                    label="Exam paper",
                    value=_as_str(values.get("exam_paper")),
                    help_text="e.g. CS1",
                ),
                OnboardingFieldView(
                    name="intended_sitting_label",
                    label="Intended sitting (optional)",
                    value=_as_str(values.get("intended_sitting_label")),
                    required=False,
                ),
            )
        if step_key == "exam_history":
            return (
                OnboardingFieldView(
                    name="prior_study",
                    label="Prior study",
                    value=_as_str(values.get("prior_study")),
                    input_type="select",
                    options=(
                        ("first_time", "First time"),
                        ("previously_studied", "Previously studied"),
                    ),
                ),
                OnboardingFieldView(
                    name="core_reading",
                    label="Core Reading",
                    value=_as_str(values.get("core_reading")),
                    input_type="select",
                    options=(
                        ("none", "None"),
                        ("partial", "Partial"),
                        ("whole_paper", "Whole paper"),
                    ),
                ),
                OnboardingFieldView(
                    name="previous_attempts",
                    label="Previous attempts",
                    value=_as_str(values.get("previous_attempts"), "0"),
                    input_type="number",
                ),
                OnboardingFieldView(
                    name="sitting_intent",
                    label="Sitting intent",
                    value=_as_str(values.get("sitting_intent")),
                    input_type="select",
                    options=(
                        ("first_sit", "First sit"),
                        ("resit", "Resit"),
                        ("revision", "Revision"),
                        ("finish_remaining", "Finish remaining"),
                    ),
                ),
            )
        if step_key == "weekly_availability":
            return (
                OnboardingFieldView(
                    name="weekday_minutes",
                    label="Weekday minutes",
                    value=_as_str(values.get("weekday_minutes"), "0"),
                    input_type="number",
                ),
                OnboardingFieldView(
                    name="weekend_minutes",
                    label="Weekend minutes",
                    value=_as_str(values.get("weekend_minutes"), "0"),
                    input_type="number",
                ),
                OnboardingFieldView(
                    name="preferred_session_minutes",
                    label="Preferred session minutes",
                    value=_as_str(values.get("preferred_session_minutes"), "60"),
                    input_type="number",
                ),
            )
        if step_key == "confidence":
            return (
                OnboardingFieldView(
                    name="band",
                    label="Confidence band",
                    value=_as_str(values.get("band")),
                    input_type="select",
                    options=(
                        ("low", "Low"),
                        ("moderate", "Moderate"),
                        ("high", "High"),
                        ("unsure", "Unsure"),
                    ),
                ),
                OnboardingFieldView(
                    name="notes",
                    label="Notes (optional)",
                    value=_as_str(values.get("notes")),
                    input_type="textarea",
                    required=False,
                ),
            )
        if step_key == "study_habits":
            return (
                OnboardingFieldView(
                    name="preference",
                    label="Study preference",
                    value=_as_str(values.get("preference")),
                    input_type="select",
                    options=(
                        ("reading_first", "Reading first"),
                        ("questions_first", "Questions first"),
                        ("mixed", "Mixed"),
                        ("unsure", "Unsure"),
                    ),
                ),
                OnboardingFieldView(
                    name="typical_start_time",
                    label="Typical start time (optional)",
                    value=_as_str(values.get("typical_start_time")),
                    required=False,
                ),
            )
        if step_key == "optional_diagnostic":
            return (
                OnboardingFieldView(
                    name="choice",
                    label="Optional diagnostic",
                    value=_as_str(values.get("choice"), "skipped"),
                    input_type="select",
                    required=False,
                    options=(
                        ("skipped", "Skip for now"),
                        ("accepted", "Accept later invitation"),
                        ("declined", "Decline"),
                    ),
                ),
            )
        if step_key == "review":
            return (
                OnboardingFieldView(
                    name="confirmed",
                    label="I confirm these declarations are accurate",
                    value=_as_str(values.get("confirmed"), "false"),
                    input_type="checkbox",
                ),
            )
        return ()


def _as_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)
