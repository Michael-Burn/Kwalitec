"""WTForms for the Founder Vision Journal (V1SP-001D)."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional

from app.models.vision_journal import (
    POTENTIAL_VALUE_LABELS,
    POTENTIAL_VALUES,
    RELATION_TYPE_LABELS,
    RELATION_TYPES,
    TARGET_VERSION_LABELS,
    TARGET_VERSIONS,
    VISION_CATEGORIES,
    VISION_STATUS_LABELS,
    VISION_STATUSES,
)


def _choices(values: tuple[str, ...], labels: dict[str, str] | None = None):
    if labels:
        return [(v, labels.get(v, v)) for v in values]
    return [(v, v) for v in values]


class VisionEntryForm(FlaskForm):
    """Create / edit a structured vision entry."""

    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=200)],
    )
    description = TextAreaField(
        "Description",
        validators=[DataRequired(), Length(max=8000)],
    )
    reason = TextAreaField(
        "Reason",
        validators=[DataRequired(), Length(max=4000)],
    )
    potential_value = SelectField(
        "Potential Value",
        choices=_choices(POTENTIAL_VALUES, POTENTIAL_VALUE_LABELS),
        validators=[DataRequired()],
    )
    expected_impact = TextAreaField(
        "Expected Impact",
        validators=[DataRequired(), Length(max=4000)],
    )
    target_version = SelectField(
        "Target Version",
        choices=_choices(TARGET_VERSIONS, TARGET_VERSION_LABELS),
        validators=[DataRequired()],
    )
    category = SelectField(
        "Category",
        choices=_choices(VISION_CATEGORIES),
        validators=[DataRequired()],
    )
    status = SelectField(
        "Status",
        choices=_choices(VISION_STATUSES, VISION_STATUS_LABELS),
        validators=[DataRequired()],
    )
    tags = StringField(
        "Tags",
        validators=[Optional(), Length(max=500)],
        description="Comma-separated tags",
    )
    future_milestone = StringField(
        "Future Milestone",
        validators=[Optional(), Length(max=200)],
    )
    submit = SubmitField("Save")


class VisionFilterForm(FlaskForm):
    """Search / filter controls for the journal list."""

    q = StringField("Search", validators=[Optional(), Length(max=200)])
    category = SelectField("Category", validators=[Optional()])
    status = SelectField("Status", validators=[Optional()])
    target_version = SelectField("Target Version", validators=[Optional()])
    tag = StringField("Tag", validators=[Optional(), Length(max=100)])
    author = SelectField("Author", validators=[Optional()])
    sort = SelectField("Sort", validators=[Optional()])
    submit = SubmitField("Apply")

    def __init__(self, *args, author_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [("", "All categories")] + _choices(
            VISION_CATEGORIES
        )
        self.status.choices = [("", "All statuses")] + _choices(
            VISION_STATUSES, VISION_STATUS_LABELS
        )
        self.target_version.choices = [("", "All versions")] + _choices(
            TARGET_VERSIONS, TARGET_VERSION_LABELS
        )
        from app.services.vision_journal_service import SORT_LABELS, SORT_OPTIONS

        self.sort.choices = [(s, SORT_LABELS[s]) for s in SORT_OPTIONS]
        self.author.choices = [("", "All authors")] + list(author_choices or [])


class VisionRelationForm(FlaskForm):
    """Link this entry to another vision entry."""

    to_entry_id = SelectField(
        "Related entry",
        coerce=int,
        validators=[DataRequired()],
    )
    relation_type = SelectField(
        "Relationship",
        choices=_choices(RELATION_TYPES, RELATION_TYPE_LABELS),
        validators=[DataRequired()],
    )
    submit = SubmitField("Add link")


class VisionPromoteForm(FlaskForm):
    """Promote to Development — creates a traceability placeholder only."""

    placeholder_ref = StringField(
        "Architecture placeholder",
        validators=[Optional(), Length(max=200)],
        description="Optional reference id for future architecture work",
    )
    notes = TextAreaField(
        "Notes",
        validators=[Optional(), Length(max=1000)],
    )
    submit = SubmitField("Promote to Development")


class VisionConfirmForm(FlaskForm):
    """Confirm soft-delete / archive actions."""

    submit = SubmitField("Confirm")
