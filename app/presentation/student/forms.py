"""WTForms for Student Experience presentation actions.

Forms collect presentation intent only. Educational decisions remain in
Student Experience application services / ports.
"""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField
from wtforms.validators import Optional


class StartSessionForm(FlaskForm):
    """Primary Home CTA — request Today's Session start."""

    mission_id = HiddenField(validators=[Optional()])
    session_id = HiddenField(validators=[Optional()])
    submit = SubmitField("Start Today's Session")


class BeginRevisionForm(FlaskForm):
    """Primary Revision CTA — begin the highest-value revision option."""

    option_id = HiddenField(validators=[Optional()])
    mission_id = HiddenField(validators=[Optional()])
    session_id = HiddenField(validators=[Optional()])
    submit = SubmitField("Begin Revision")
