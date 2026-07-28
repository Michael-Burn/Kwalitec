"""WTForms for Quick Check learner experience."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import HiddenField, RadioField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class StartQuickCheckForm(FlaskForm):
    mission_ref = HiddenField(validators=[DataRequired(), Length(max=128)])
    subject_code = HiddenField(validators=[Optional(), Length(max=64)])
    return_endpoint = HiddenField(validators=[Optional(), Length(max=128)])
    return_session_id = HiddenField(validators=[Optional(), Length(max=128)])
    submit = SubmitField("Continue")


class WhyThisForm(FlaskForm):
    mission_ref = HiddenField(validators=[Optional(), Length(max=128)])
    subject_code = HiddenField(validators=[Optional(), Length(max=64)])
    experience_id = HiddenField(validators=[Optional(), Length(max=64)])
    submit = SubmitField("Why this?")


class DeferQuickCheckForm(FlaskForm):
    mission_ref = HiddenField(validators=[DataRequired(), Length(max=128)])
    subject_code = HiddenField(validators=[Optional(), Length(max=64)])
    experience_id = HiddenField(validators=[Optional(), Length(max=64)])
    return_endpoint = HiddenField(validators=[Optional(), Length(max=128)])
    return_session_id = HiddenField(validators=[Optional(), Length(max=128)])
    submit = SubmitField("Not now")


class BeginQuickCheckForm(FlaskForm):
    experience_id = HiddenField(validators=[DataRequired(), Length(max=64)])
    submit = SubmitField("Begin")


class HintQuickCheckForm(FlaskForm):
    experience_id = HiddenField(validators=[DataRequired(), Length(max=64)])
    submit = SubmitField("Show a hint")


class RespondQuickCheckForm(FlaskForm):
    experience_id = HiddenField(validators=[DataRequired(), Length(max=64)])
    item_id = HiddenField(validators=[DataRequired(), Length(max=64)])
    free_text = TextAreaField(validators=[Optional(), Length(max=4000)])
    choice = RadioField(validators=[Optional()], choices=[])
    submit = SubmitField("Continue")


class ReflectQuickCheckForm(FlaskForm):
    experience_id = HiddenField(validators=[DataRequired(), Length(max=64)])
    reflection = TextAreaField(validators=[Optional(), Length(max=4000)])
    recommendation_choice = HiddenField(validators=[Optional(), Length(max=32)])
    submit = SubmitField("Continue")


class ExpandExplanationForm(FlaskForm):
    experience_id = HiddenField(validators=[Optional(), Length(max=64)])
    subject_code = HiddenField(validators=[Optional(), Length(max=64)])
    surface = HiddenField(validators=[Optional(), Length(max=64)])
    submit = SubmitField("Expand")


class RecommendationChoiceForm(FlaskForm):
    experience_id = HiddenField(validators=[DataRequired(), Length(max=64)])
    choice = HiddenField(validators=[DataRequired(), Length(max=32)])
    surface = HiddenField(validators=[Optional(), Length(max=64)])
    submit = SubmitField("Continue")


class PauseQuickCheckForm(FlaskForm):
    experience_id = HiddenField(validators=[DataRequired(), Length(max=64)])
    submit = SubmitField("Pause")


class ResumeQuickCheckForm(FlaskForm):
    experience_id = HiddenField(validators=[DataRequired(), Length(max=64)])
    submit = SubmitField("Resume")


class ReturnToMissionForm(FlaskForm):
    experience_id = HiddenField(validators=[DataRequired(), Length(max=64)])
    return_endpoint = HiddenField(validators=[Optional(), Length(max=128)])
    return_session_id = HiddenField(validators=[Optional(), Length(max=128)])
    submit = SubmitField("Return to Mission")
