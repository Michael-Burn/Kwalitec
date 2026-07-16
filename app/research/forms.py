"""WTForms for Research Intelligence check-in and Founder review."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    HiddenField,
    RadioField,
    SelectField,
    StringField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Optional

from app.models.research_feedback import (
    FEATURE_AREA_CHOICES,
    FINDING_STATUSES,
    SEVERITY_CHOICES,
    WORKFLOW_STATUSES,
)
from app.services.contributor_recognition_service import BADGE_LABELS
from app.services.founder_research_service import WORKFLOW_LABELS
from app.services.research_feedback_service import (
    CLASSIFICATION_CHOICES,
    CONFIDENCE_CHOICES,
    EXPERIENCE_CHOICES,
    FEATURE_CHOICES,
    FRICTION_CHOICES,
    RETURN_INTENT_CHOICES,
    SOURCE_SETTINGS,
    SOURCE_STUDY_SESSION,
)


def _choice_pairs(values: tuple[str, ...]) -> list[tuple[str, str]]:
    return [(value, value) for value in values]


class ProductCheckinForm(FlaskForm):
    """Structured product check-in — most answers are single-click."""

    experience_rating = RadioField(
        "How was your experience using Kwalitec today?",
        choices=_choice_pairs(EXPERIENCE_CHOICES),
        validators=[DataRequired(message="Please choose an experience rating.")],
    )
    feature_helped_most = RadioField(
        "Which part of Kwalitec helped you the most today?",
        choices=_choice_pairs(FEATURE_CHOICES),
        validators=[DataRequired(message="Please choose one feature.")],
    )
    friction_area = RadioField(
        "Did anything make studying harder today?",
        choices=_choice_pairs(FRICTION_CHOICES),
        validators=[DataRequired(message="Please choose one option.")],
    )
    confidence_rating = RadioField(
        "How confident are you that Kwalitec helped you study today?",
        choices=_choice_pairs(CONFIDENCE_CHOICES),
        validators=[DataRequired(message="Please choose a confidence level.")],
    )
    return_intent = RadioField(
        "Would you choose to open Kwalitec again tomorrow?",
        choices=_choice_pairs(RETURN_INTENT_CHOICES),
        validators=[DataRequired(message="Please choose one option.")],
    )
    free_text = TextAreaField(
        "Anything else you'd like us to know?",
        validators=[Optional(), Length(max=300)],
        render_kw={
            "placeholder": "Tell us anything that would help make Kwalitec better.",
            "rows": 3,
            "maxlength": 300,
        },
    )
    classification = RadioField(
        "How would you classify this note?",
        choices=_choice_pairs(CLASSIFICATION_CHOICES),
        validators=[Optional()],
    )

    submission_source = HiddenField(validators=[DataRequired()])
    mission_id = HiddenField()
    study_plan_id = HiddenField()

    def validate_classification(self, field: RadioField) -> None:
        """Require classification only when optional free-text is entered."""
        text = (self.free_text.data or "").strip()
        if text and not field.data:
            raise ValidationError(
                "Please classify your note with one tap."
            )


class FounderFeedbackReviewForm(FlaskForm):
    """Founder marks on a Product Check-in submission (RIP-002)."""

    helpful = BooleanField("Helpful")
    insightful = BooleanField("Insightful")
    implemented = BooleanField("Implemented")


def _optional_choice_pairs(
    values: tuple[str, ...],
    *,
    empty_label: str = "All",
) -> list[tuple[str, str]]:
    return [("", empty_label)] + [(value, value) for value in values]


def _workflow_choice_pairs() -> list[tuple[str, str]]:
    return [("", "All")] + [
        (status, WORKFLOW_LABELS.get(status, status)) for status in WORKFLOW_STATUSES
    ]


class ResearchInboxFilterForm(FlaskForm):
    """Filters for the Founder Research Inbox (RIP-003)."""

    version = StringField("Version", validators=[Optional()])
    badge = SelectField(
        "Badge",
        choices=_optional_choice_pairs(tuple(BADGE_LABELS.keys())),
        validators=[Optional()],
    )
    feature = SelectField(
        "Feature",
        choices=_optional_choice_pairs(FEATURE_CHOICES),
        validators=[Optional()],
    )
    severity = SelectField(
        "Severity",
        choices=_optional_choice_pairs(SEVERITY_CHOICES),
        validators=[Optional()],
    )
    status = SelectField(
        "Status",
        choices=_workflow_choice_pairs(),
        validators=[Optional()],
    )
    classification = SelectField(
        "Classification",
        choices=_optional_choice_pairs(CLASSIFICATION_CHOICES),
        validators=[Optional()],
    )
    date_from = StringField("From", validators=[Optional()])
    date_to = StringField("To", validators=[Optional()])
    submission_source = SelectField(
        "Source",
        choices=[
            ("", "All"),
            (SOURCE_STUDY_SESSION, "Study Session"),
            (SOURCE_SETTINGS, "Settings"),
        ],
        validators=[Optional()],
    )
    keyword = StringField("Search", validators=[Optional(), Length(max=100)])
    student = StringField("Student", validators=[Optional(), Length(max=100)])


class FounderNoteForm(FlaskForm):
    """Internal Founder note on feedback."""

    note_text = TextAreaField(
        "Internal note",
        validators=[DataRequired(), Length(max=1000)],
        render_kw={"rows": 3, "maxlength": 1000},
    )


class StatusTransitionForm(FlaskForm):
    """Workflow transition with optional rationale."""

    to_status = SelectField(
        "Status",
        choices=[
            (status, WORKFLOW_LABELS.get(status, status))
            for status in WORKFLOW_STATUSES
        ],
        validators=[DataRequired()],
    )
    rationale = TextAreaField(
        "Rationale",
        validators=[Optional(), Length(max=500)],
        render_kw={"rows": 2, "maxlength": 500},
    )


class ProductFindingForm(FlaskForm):
    """Create or update a product finding."""

    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    summary = TextAreaField(
        "Summary",
        validators=[DataRequired(), Length(max=1000)],
        render_kw={"rows": 3, "maxlength": 1000},
    )
    severity = SelectField(
        "Severity",
        choices=[(s, s) for s in SEVERITY_CHOICES],
        validators=[DataRequired()],
    )
    feature_area = SelectField(
        "Feature area",
        choices=[(f, f) for f in FEATURE_AREA_CHOICES],
        validators=[DataRequired()],
    )
    status = SelectField(
        "Status",
        choices=[(s, WORKFLOW_LABELS.get(s, s)) for s in FINDING_STATUSES],
        validators=[DataRequired()],
    )
    target_release = StringField(
        "Target release",
        validators=[Optional(), Length(max=32)],
        render_kw={"placeholder": "e.g. 1.0.1"},
    )
    notes = TextAreaField(
        "Notes",
        validators=[Optional(), Length(max=2000)],
        render_kw={"rows": 3, "maxlength": 2000},
    )
    linked_submission_ids = StringField(
        "Linked submission IDs",
        validators=[Optional()],
        render_kw={"placeholder": "Comma-separated submission ids"},
    )
