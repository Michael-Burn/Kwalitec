"""Forms for the exam-aware Study Plan Wizard (PX-002 Subject Catalogue path)."""

from __future__ import annotations

from calendar import monthrange
from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    IntegerField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
    validators,
)
from wtforms.validators import Optional

from app.services import examination_catalogue as catalogue

_MONTH_CHOICES: list[tuple[int, str]] = [
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December"),
]

_DAY_CHOICES: list[tuple[int, str]] = [(d, str(d)) for d in range(1, 32)]


def _year_bounds(*, today: date | None = None) -> tuple[int, int]:
    """Inclusive year range for upcoming exam sittings."""
    current = today or date.today()
    return current.year, current.year + 8


def parse_date_parts(
    *,
    day: int | None,
    month: int | None,
    year: int | None,
) -> date | None:
    """Compose a calendar date from day/month/year, or None if incomplete."""
    if day is None or month is None or year is None:
        return None
    last_day = monthrange(year, month)[1]
    if day < 1 or day > last_day:
        raise ValueError("invalid day for month")
    return date(year, month, day)

# ─────────────────────────────────────────────────────────────────────────────
# Step 1 — Choose Exam (Subject Catalogue)
# ─────────────────────────────────────────────────────────────────────────────


class SubjectCatalogueForm(FlaskForm):
    """Select a Ready subject from the Subject Catalogue."""

    subject_key = RadioField(
        "Subject",
        choices=[],  # populated from SubjectCatalogueService
        validators=[validators.DataRequired("Please choose an exam.")],
    )
    submit = SubmitField("Continue")


class ExamCategoryForm(FlaskForm):
    """Legacy examining-body step (compat / internal)."""

    exam_category = RadioField(
        "Examination",
        choices=catalogue.get_category_choices(),
        validators=[validators.DataRequired("Please select an examination.")],
    )
    submit = SubmitField("Next")


# ─────────────────────────────────────────────────────────────────────────────
# Step 2 — Paper / subject
# ─────────────────────────────────────────────────────────────────────────────


class ExamPaperForm(FlaskForm):
    """Step 2: Select the paper or enter a free-text subject."""

    exam_paper = RadioField(
        "Paper / Subject",
        choices=[],  # populated dynamically in the route
        validators=[Optional()],
    )
    free_text_subject = StringField(
        "Subject",
        validators=[Optional(), validators.Length(max=255)],
    )
    submit = SubmitField("Next")


# ─────────────────────────────────────────────────────────────────────────────
# Step 3 — Sitting & exam date
# ─────────────────────────────────────────────────────────────────────────────


class ExamSittingForm(FlaskForm):
    """Step 2: Select exam sitting and date (keyboard-friendly parts)."""

    exam_sitting = SelectField(
        "Sitting",
        choices=[],  # populated dynamically in the route
        validators=[validators.DataRequired("Please select a sitting.")],
    )
    exam_day = SelectField(
        "Day",
        choices=_DAY_CHOICES,
        coerce=int,
        validators=[validators.DataRequired("Please choose a day.")],
    )
    exam_month = SelectField(
        "Month",
        choices=_MONTH_CHOICES,
        coerce=int,
        validators=[validators.DataRequired("Please choose a month.")],
    )
    exam_year = IntegerField(
        "Year",
        validators=[
            validators.DataRequired("Please enter the year."),
            validators.NumberRange(
                min=_year_bounds()[0],
                max=_year_bounds()[1],
                message=(
                    f"Year must be between {_year_bounds()[0]} "
                    f"and {_year_bounds()[1]}."
                ),
            ),
        ],
        render_kw={
            "inputmode": "numeric",
            "min": str(_year_bounds()[0]),
            "max": str(_year_bounds()[1]),
            "placeholder": str(_year_bounds()[0] + 1),
            "autocomplete": "off",
        },
    )
    submit = SubmitField("Continue")

    def populate_from_exam_date(self, value: date | str | None) -> None:
        """Prefill day/month/year from a stored exam date."""
        if value is None or value == "":
            return
        if isinstance(value, str):
            value = date.fromisoformat(value)
        self.exam_day.data = value.day
        self.exam_month.data = value.month
        self.exam_year.data = value.year

    @property
    def exam_date(self) -> date | None:
        """Composed exam date after successful validation."""
        return getattr(self, "_exam_date", None)

    def validate(self, extra_validators=None) -> bool:
        if not super().validate(extra_validators=extra_validators):
            return False
        try:
            composed = parse_date_parts(
                day=self.exam_day.data,
                month=self.exam_month.data,
                year=self.exam_year.data,
            )
        except ValueError:
            self.exam_day.errors.append(
                "That day is not valid for the selected month."
            )
            return False
        if composed is None:
            self.exam_year.errors.append("Exam date is required.")
            return False
        if composed <= date.today():
            self.exam_year.errors.append("Exam date must be in the future.")
            return False
        self._exam_date = composed
        return True


# ─────────────────────────────────────────────────────────────────────────────
# Step 4 — Current position
# ─────────────────────────────────────────────────────────────────────────────


class CurrentPositionForm(FlaskForm):
    """Step 4: Where are you currently?"""

    current_position = RadioField(
        "Current Position",
        choices=[
            ("not_started", "I haven't started"),
            ("learning", "I've started but I'm still learning new material"),
            ("completed", "I've completed the syllabus once"),
            ("revising", "I'm currently revising"),
        ],
        validators=[validators.DataRequired("Please select your current position.")],
    )
    current_topic = StringField(
        "What topic are you currently studying?",
        validators=[Optional(), validators.Length(max=255)],
    )
    submit = SubmitField("Next")


# ─────────────────────────────────────────────────────────────────────────────
# Step 5 — Study availability & session length
# ─────────────────────────────────────────────────────────────────────────────


class StudyAvailabilityForm(FlaskForm):
    """Step 5: How much time can you realistically study?"""

    weekday_study_minutes = IntegerField(
        "Weekdays (minutes per day)",
        validators=[
            validators.DataRequired("Weekday study time is required."),
            validators.NumberRange(
                min=15,
                max=480,
                message="Must be between 15 and 480 minutes.",
            ),
        ],
    )
    weekend_study_minutes = IntegerField(
        "Weekend (minutes per day)",
        validators=[
            validators.DataRequired("Weekend study time is required."),
            validators.NumberRange(
                min=15,
                max=480,
                message="Must be between 15 and 480 minutes.",
            ),
        ],
    )
    preferred_session_minutes = RadioField(
        "Preferred study session length",
        choices=[(30, "30 minutes"), (45, "45 minutes"), (60, "60 minutes"),
                 (90, "90 minutes"), (120, "120 minutes")],
        coerce=int,
        default=60,
        validators=[validators.DataRequired()],
    )
    submit = SubmitField("Continue")


# ─────────────────────────────────────────────────────────────────────────────
# Step 6 — Learning style
# ─────────────────────────────────────────────────────────────────────────────


class StudyPreferenceForm(FlaskForm):
    """Step 6: How do you prefer to learn?"""

    study_preference = RadioField(
        "Learning Style",
        choices=[
            ("Reading First", "Reading First"),
            ("Questions First", "Questions First"),
            ("Mixed", "Mixed"),
        ],
        default="Mixed",
        validators=[validators.DataRequired()],
    )
    submit = SubmitField("Next")


# ─────────────────────────────────────────────────────────────────────────────
# Step 7 — Target result
# ─────────────────────────────────────────────────────────────────────────────


class TargetResultForm(FlaskForm):
    """Step 7: What result are you aiming for?"""

    target_grade = RadioField(
        "Target Result",
        choices=[],  # populated dynamically in the route
        validators=[validators.DataRequired("Please select a target result.")],
    )
    submit = SubmitField("Create Study Plan")


# ─────────────────────────────────────────────────────────────────────────────
# Step 8 — Review
# ─────────────────────────────────────────────────────────────────────────────


class StudyPlanReviewForm(FlaskForm):
    """Begin Learning — confirm Study Plan creation."""

    # Quiet confirm — Change selection is a Secondary link, not a twin Primary.
    confirm = HiddenField(default="yes")
    submit = SubmitField("Begin Learning")


# ─────────────────────────────────────────────────────────────────────────────
# Edit Study Plan
# ─────────────────────────────────────────────────────────────────────────────


class EditStudyPlanForm(FlaskForm):
    """Form for editing an existing study plan."""

    exam_name = StringField(
        "Exam Name",
        validators=[validators.DataRequired(), validators.Length(max=255)],
    )
    exam_sitting = StringField(
        "Exam Sitting",
        validators=[validators.DataRequired(), validators.Length(max=100)],
    )
    exam_day = SelectField(
        "Day",
        choices=_DAY_CHOICES,
        coerce=int,
        validators=[validators.DataRequired("Please choose a day.")],
    )
    exam_month = SelectField(
        "Month",
        choices=_MONTH_CHOICES,
        coerce=int,
        validators=[validators.DataRequired("Please choose a month.")],
    )
    exam_year = IntegerField(
        "Year",
        validators=[
            validators.DataRequired("Please enter the year."),
            validators.NumberRange(
                min=_year_bounds()[0],
                max=_year_bounds()[1],
                message=(
                    f"Year must be between {_year_bounds()[0]} "
                    f"and {_year_bounds()[1]}."
                ),
            ),
        ],
        render_kw={
            "inputmode": "numeric",
            "min": str(_year_bounds()[0]),
            "max": str(_year_bounds()[1]),
            "placeholder": str(_year_bounds()[0] + 1),
            "autocomplete": "off",
        },
    )
    weekday_study_minutes = IntegerField(
        "Weekday Study Minutes",
        validators=[
            validators.DataRequired(),
            validators.NumberRange(
                min=15, max=480, message="Must be between 15 and 480 minutes."
            ),
        ],
    )
    weekend_study_minutes = IntegerField(
        "Weekend Study Minutes",
        validators=[
            validators.DataRequired(),
            validators.NumberRange(
                min=15, max=480, message="Must be between 15 and 480 minutes."
            ),
        ],
    )
    preferred_session_minutes = RadioField(
        "Preferred study session length",
        choices=[
            (30, "30 minutes"),
            (45, "45 minutes"),
            (60, "60 minutes"),
            (90, "90 minutes"),
            (120, "120 minutes"),
        ],
        coerce=int,
        default=60,
        validators=[validators.DataRequired()],
    )
    current_stage = StringField(
        "Current Stage",
        validators=[validators.DataRequired(), validators.Length(max=255)],
    )
    study_preference = RadioField(
        "Learning Style",
        choices=[
            ("Reading First", "Reading First"),
            ("Questions First", "Questions First"),
            ("Mixed", "Mixed"),
        ],
        validators=[validators.DataRequired()],
    )
    target_grade = StringField(
        "Target Grade",
        validators=[validators.DataRequired(), validators.Length(max=50)],
    )
    submit = SubmitField("Save Changes")

    def populate_from_exam_date(self, value: date | str | None) -> None:
        """Prefill day/month/year from a stored exam date."""
        if value is None or value == "":
            return
        if isinstance(value, str):
            value = date.fromisoformat(value)
        self.exam_day.data = value.day
        self.exam_month.data = value.month
        self.exam_year.data = value.year

    @property
    def exam_date(self) -> date | None:
        """Composed exam date after successful validation or prefill."""
        stored = getattr(self, "_exam_date", None)
        if stored is not None:
            return stored
        try:
            return parse_date_parts(
                day=self.exam_day.data,
                month=self.exam_month.data,
                year=self.exam_year.data,
            )
        except ValueError:
            return None

    def validate(self, extra_validators=None) -> bool:
        if not super().validate(extra_validators=extra_validators):
            return False
        try:
            composed = parse_date_parts(
                day=self.exam_day.data,
                month=self.exam_month.data,
                year=self.exam_year.data,
            )
        except ValueError:
            self.exam_day.errors.append(
                "That day is not valid for the selected month."
            )
            return False
        if composed is None:
            self.exam_year.errors.append("Exam date is required.")
            return False
        if composed <= date.today():
            self.exam_year.errors.append("Exam date must be in the future.")
            return False
        self._exam_date = composed
        return True
