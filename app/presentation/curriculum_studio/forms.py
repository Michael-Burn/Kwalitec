"""WTForms for Curriculum Studio Founder actions."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

_REQUIRED = {"aria-required": "true"}


class CreateSubjectForm(FlaskForm):
    subject_code = StringField(
        "Subject code",
        validators=[
            DataRequired(
                message=(
                    "Subject code is required. Without a code students cannot "
                    "enrol against this subject. Enter a short syllabus code "
                    "such as CS1, then try again."
                )
            ),
            Length(max=64),
        ],
        render_kw={
            "placeholder": "e.g. CS1",
            "autocomplete": "off",
            "aria-describedby": "help-subject-code",
            **_REQUIRED,
        },
    )
    title = StringField(
        "Title",
        validators=[Optional(), Length(max=200)],
        render_kw={
            "placeholder": "Optional display title",
            "autocomplete": "off",
        },
    )
    submit = SubmitField("Create Subject")


class CreateWorkspaceForm(FlaskForm):
    subject_code = StringField(
        "Subject code",
        validators=[
            DataRequired(message="Subject code is required."),
            Length(max=64),
        ],
        render_kw={
            "placeholder": "e.g. CS1",
            "autocomplete": "off",
            "aria-describedby": "help-workspace-code",
            **_REQUIRED,
        },
    )
    submit = SubmitField("Open Workspace")


class AdvanceWorkflowForm(FlaskForm):
    workspace_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Continue")


class ValidateWorkspaceForm(FlaskForm):
    workspace_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Validate")


class PreviewWorkspaceForm(FlaskForm):
    workspace_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Generate preview")


class ApproveWorkspaceForm(FlaskForm):
    workspace_id = HiddenField(validators=[DataRequired()])
    reason = StringField(
        "Approval note",
        validators=[Optional(), Length(max=200)],
        render_kw={"placeholder": "Optional reason for approval"},
    )
    submit = SubmitField("Approve")


class PublishWorkspaceForm(FlaskForm):
    workspace_id = HiddenField(validators=[DataRequired()])
    reason = TextAreaField(
        "Publication note",
        validators=[Optional(), Length(max=500)],
        render_kw={
            "placeholder": "Optional note for this publication",
            "rows": 2,
        },
    )
    submit = SubmitField("Publish")


class AssignVersionForm(FlaskForm):
    workspace_id = HiddenField(validators=[DataRequired()])
    version_label = StringField(
        "Version label",
        validators=[
            DataRequired(
                message=(
                    "Version label is required. Enter a label such as 1.0.0 "
                    "so you can track published versions, then try again."
                )
            ),
            Length(max=64),
        ],
        render_kw={
            "placeholder": "e.g. 1.0.0",
            "autocomplete": "off",
            **_REQUIRED,
        },
    )
    submit = SubmitField("Assign version")
