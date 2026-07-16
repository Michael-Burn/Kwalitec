"""Forms for mission review and learning recording."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, SelectField, TextAreaField, validators
from wtforms.validators import DataRequired, InputRequired, Optional, ValidationError

from app.services.study_session_service import (
    COMPLETION_NO,
    COMPLETION_PARTIAL,
    COMPLETION_YES,
)


class PracticeOutcomeCaptureForm(FlaskForm):
    """LXP-003 Practice Outcome Capture — observed practice facts only.

    Does not collect confidence, mastery, understanding, difficulty, or readiness.
    """

    questions_attempted = IntegerField(
        "Questions Attempted",
        validators=[
            InputRequired(message="Enter how many questions you attempted."),
            validators.NumberRange(
                min=1,
                message="Questions Attempted must be greater than zero.",
            ),
        ],
        render_kw={"placeholder": "e.g., 10", "min": 1},
    )

    questions_correct = IntegerField(
        "Questions Correct",
        validators=[
            InputRequired(message="Enter how many questions you got correct."),
            validators.NumberRange(
                min=0,
                message="Questions Correct must be zero or greater.",
            ),
        ],
        render_kw={"placeholder": "e.g., 7", "min": 0},
    )

    duration_minutes = IntegerField(
        "Time spent answering questions (minutes)",
        validators=[
            Optional(),
            validators.NumberRange(
                min=1,
                max=600,
                message="Time spent must be between 1 and 600 minutes.",
            ),
        ],
        render_kw={
            "placeholder": "Optional — e.g., 25",
            "min": 1,
            "max": 600,
        },
    )

    notes = TextAreaField(
        "Notes",
        validators=[Optional(), validators.Length(max=2000)],
        render_kw={
            "placeholder": "Optional notes about today's practice",
            "rows": 3,
        },
    )

    def validate_questions_correct(self, field: IntegerField) -> None:
        """Reject impossible scores: correct must be <= attempted."""
        attempted = self.questions_attempted.data
        correct = field.data
        if attempted is None or correct is None:
            return
        if correct > attempted:
            raise ValidationError(
                "Questions Correct cannot exceed Questions Attempted."
            )


class StudySessionReviewForm(FlaskForm):
    """LXP-002 Study Session Review — completion only (no performance).

    Retained for service-level compatibility tests. The student primary path
    after Finish Study Session is Practice Outcome Capture (LXP-003).
    """

    completion_status = RadioField(
        "Did you complete today's planned study?",
        choices=[
            (COMPLETION_YES, "Yes"),
            (COMPLETION_PARTIAL, "Partially"),
            (COMPLETION_NO, "No"),
        ],
        validators=[
            DataRequired(
                message="Please say whether you completed today's study.",
            ),
        ],
    )

    notes = TextAreaField(
        "Optional notes",
        validators=[Optional(), validators.Length(max=2000)],
        render_kw={
            "placeholder": (
                "Anything you want to remember about today's study (optional)"
            ),
            "rows": 3,
        },
    )


class MissionReviewForm(FlaskForm):
    """Retired Reflect on Your Learning form (PTP-002).

    Retained for import compatibility and historical templates. Student HTTP
    journeys must not render or submit this form — Practice Outcome Capture
    and Study Session Feedback are the Version 1 authority.
    """

    duration_minutes = IntegerField(
        "Time Spent (minutes)",
        validators=[
            DataRequired(),
            validators.NumberRange(
                min=1,
                max=600,
                message="Must be between 1 and 600 minutes",
            ),
        ],
        render_kw={"placeholder": "e.g., 45", "min": 1, "max": 600},
    )

    questions_attempted = IntegerField(
        "Questions Attempted",
        validators=[Optional(), validators.NumberRange(min=0)],
        render_kw={"placeholder": "e.g., 10"},
    )

    questions_correct = IntegerField(
        "Questions Correct",
        validators=[Optional(), validators.NumberRange(min=0)],
        render_kw={"placeholder": "e.g., 8"},
    )

    confidence_before = SelectField(
        "Confidence Before",
        choices=[
            ("Not Started", "Not Sure"),
            ("Low", "Not Confident"),
            ("Medium", "Somewhat Confident"),
            ("High", "Confident"),
            ("Mastered", "Very Confident"),
        ],
        validators=[DataRequired()],
    )

    confidence_after = SelectField(
        "Confidence After",
        choices=[
            ("Not Started", "Not Sure"),
            ("Low", "Not Confident"),
            ("Medium", "Somewhat Confident"),
            ("High", "Confident"),
            ("Mastered", "Very Confident"),
        ],
        validators=[DataRequired()],
    )

    notes = TextAreaField(
        "Notes",
        validators=[Optional()],
        render_kw={
            "placeholder": "What did you learn? What was difficult?",
            "rows": 4,
        },
    )

    def validate_questions_correct(self, field):
        """Validate that correct <= attempted."""
        if (
            self.questions_correct.data is not None
            and self.questions_attempted.data is not None
        ):
            if self.questions_correct.data > self.questions_attempted.data:
                raise ValidationError(
                    "Questions correct cannot exceed questions attempted."
                )


class MistakeForm(FlaskForm):
    """Form for recording a single mistake."""

    mistake_type = SelectField(
        "Type of Mistake",
        choices=[
            ("", "-- Select --"),
            ("Calculation", "Calculation Error"),
            ("Concept", "Conceptual Misunderstanding"),
            ("Misconception", "Misconception"),
            ("Careless", "Careless Error"),
            ("Misreading", "Misread Question"),
            ("Method", "Wrong Method"),
            ("Other", "Other"),
        ],
        validators=[DataRequired()],
    )

    description = TextAreaField(
        "What Went Wrong?",
        validators=[
            DataRequired(message="Please describe the mistake."),
            validators.Length(min=10, max=500),
        ],
        render_kw={
            "placeholder": "Explain what you did wrong and why...",
            "rows": 3,
        },
    )

    correct_solution = TextAreaField(
        "Correct Solution",
        validators=[Optional(), validators.Length(max=500)],
        render_kw={
            "placeholder": "What's the correct approach or answer?",
            "rows": 3,
        },
    )
