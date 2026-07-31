"""WTForms for Student Experience presentation actions.

Forms collect presentation intent only. Educational decisions remain in
Student Experience application services / ports.
"""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import HiddenField, RadioField, StringField, SubmitField
from wtforms.validators import Length, Optional


class StartSessionForm(FlaskForm):
    """Primary Home CTA — request Today's Session start.

    EP-008.3 Pattern A: starting also records conscious commitment
    ("Starting means you're doing this next.").
    """

    mission_id = HiddenField(validators=[Optional()])
    session_id = HiddenField(validators=[Optional()])
    recommendation_key = HiddenField(validators=[Optional()])
    record_commitment = HiddenField(default="1", validators=[Optional()])
    submit = SubmitField("Start Today's Session")


class CompleteRuntimeMissionForm(FlaskForm):
    """PR-001B — mark today's Runtime C mission complete from Home.

    Pilot study loop write-back only. Does not start Guided Session or
    change educational algorithms.
    """

    mission_id = HiddenField(validators=[Optional()])
    submit = SubmitField("Confirm today's Mission")


class BeginRevisionForm(FlaskForm):
    """Primary Revision CTA — begin the highest-value revision option."""

    option_id = HiddenField(validators=[Optional()])
    mission_id = HiddenField(validators=[Optional()])
    session_id = HiddenField(validators=[Optional()])
    submit = SubmitField("Begin Revision")


class DeferCommitmentForm(FlaskForm):
    """Honest deferral — catalogue reason; preference / intent only."""

    recommendation_key = HiddenField(validators=[Optional()])
    reason_code = RadioField(
        "What's getting in the way?",
        choices=[
            ("not_enough_time", "Not enough time"),
            ("need_prerequisite", "Need a prerequisite first"),
            ("studying_elsewhere", "Already studying elsewhere"),
            ("not_today", "Not today"),
            ("other", "Something else"),
        ],
        default="not_today",
        validators=[Optional()],
    )
    reason_note = StringField(
        validators=[Optional(), Length(max=140)],
    )
    submit = SubmitField("Save and continue")


class ReflectionAckForm(FlaskForm):
    """One-tap acknowledgement advancing C3 → C4 (observational)."""

    recommendation_key = HiddenField(validators=[Optional()])
    submit = SubmitField("Got it")


class EducationalReflectionForm(FlaskForm):
    """ILE-005 — optional educational reflection on a journal recommendation.

    Preference / educational judgement only. Never engagement scoring.
    """

    entry_id = HiddenField(validators=[Optional()])
    helped = RadioField(
        "Did this recommendation help?",
        choices=[
            ("yes", "Yes"),
            ("mostly", "Mostly"),
            ("no", "No"),
            ("skipped", "Prefer not to say"),
        ],
        default="skipped",
        validators=[Optional()],
    )
    timing = RadioField(
        "Was the timing appropriate?",
        choices=[
            ("yes", "Yes"),
            ("mostly", "Mostly"),
            ("no", "No"),
            ("skipped", "Prefer not to say"),
        ],
        default="skipped",
        validators=[Optional()],
    )
    understood_why = RadioField(
        "Did you understand why it was recommended?",
        choices=[
            ("yes", "Yes"),
            ("mostly", "Mostly"),
            ("no", "No"),
            ("skipped", "Prefer not to say"),
        ],
        default="skipped",
        validators=[Optional()],
    )
    same_decision = RadioField(
        "Would you make the same decision again?",
        choices=[
            ("yes", "Yes"),
            ("mostly", "Mostly"),
            ("no", "No"),
            ("skipped", "Prefer not to say"),
        ],
        default="skipped",
        validators=[Optional()],
    )
    free_text = StringField(
        validators=[Optional(), Length(max=500)],
    )
    submit = SubmitField("Save reflection")


class ExplainMissionTutorForm(FlaskForm):
    """TUTOR-001 — ask the Tutor to explain today's mission (evidence-backed)."""

    submit = SubmitField("Explain today's mission")
