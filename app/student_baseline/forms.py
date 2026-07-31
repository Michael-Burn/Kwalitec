"""WTForms for SB-001A progressive Baseline steps."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField, StringField, SubmitField, validators
from wtforms.validators import Optional

from app.application.student_baseline.enums import (
    CONFIDENCE_LABELS,
    EXAM_HISTORY_LABELS,
    EXPERIENCE_LABELS,
    OBJECTIVE_LABELS,
    POSITION_MODE_LABELS,
    ConfidenceBand,
    ExamHistory,
    LearningObjective,
    PositionMode,
    PreviousExperience,
)


class ExperienceForm(FlaskForm):
    experience = RadioField(
        "Have you studied this subject before?",
        choices=[(e.value, EXPERIENCE_LABELS[e]) for e in PreviousExperience],
        validators=[validators.DataRequired()],
    )
    submit = SubmitField("Continue")


class PositionForm(FlaskForm):
    position_mode = RadioField(
        "Where should we begin?",
        choices=[(m.value, POSITION_MODE_LABELS[m]) for m in PositionMode],
        validators=[validators.DataRequired()],
    )
    curriculum_topic_code = SelectField(
        "Continue from topic",
        choices=[],
        validators=[Optional()],
    )
    submit = SubmitField("Continue")


class ExamHistoryForm(FlaskForm):
    exam_history = RadioField(
        "Exam history",
        choices=[(e.value, EXAM_HISTORY_LABELS[e]) for e in ExamHistory],
        validators=[validators.DataRequired()],
    )
    highest_mark = StringField(
        "Highest mark achieved (optional)",
        validators=[Optional(), validators.Length(max=64)],
    )
    submit = SubmitField("Continue")


class ObjectiveForm(FlaskForm):
    learning_objective = RadioField(
        "What would you like Kwalitec to do?",
        choices=[(o.value, OBJECTIVE_LABELS[o]) for o in LearningObjective],
        validators=[validators.DataRequired()],
    )
    submit = SubmitField("Continue")


class ConfidenceForm(FlaskForm):
    confidence = RadioField(
        "How confident do you currently feel?",
        choices=[(c.value, CONFIDENCE_LABELS[c]) for c in ConfidenceBand],
        validators=[validators.DataRequired()],
    )
    submit = SubmitField("Continue")


class ConfirmForm(FlaskForm):
    submit = SubmitField("Begin learning")
