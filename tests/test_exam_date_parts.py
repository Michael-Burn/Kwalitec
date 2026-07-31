"""Exam date parts — keyboard-friendly year entry."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.study_plan.forms import (
    EditStudyPlanForm,
    ExamSittingForm,
    parse_date_parts,
)


def test_parse_date_parts_valid():
    assert parse_date_parts(day=15, month=4, year=2027) == date(2027, 4, 15)


def test_parse_date_parts_rejects_invalid_day():
    with pytest.raises(ValueError):
        parse_date_parts(day=31, month=2, year=2027)


def test_exam_sitting_form_accepts_typed_year(app):
    future = date.today() + timedelta(days=200)
    with app.test_request_context(
        method="POST",
        data={
            "exam_sitting": "April 2027",
            "exam_day": str(future.day),
            "exam_month": str(future.month),
            "exam_year": str(future.year),
            "csrf_token": "unused",
        },
    ):
        form = ExamSittingForm(meta={"csrf": False})
        form.exam_sitting.choices = [("April 2027", "April 2027")]
        assert form.validate() is True
        assert form.exam_date == future


def test_exam_sitting_form_rejects_past_date(app):
    past = date.today() - timedelta(days=1)
    with app.test_request_context(
        method="POST",
        data={
            "exam_sitting": "April 2027",
            "exam_day": str(past.day),
            "exam_month": str(past.month),
            "exam_year": str(past.year),
            "csrf_token": "unused",
        },
    ):
        form = ExamSittingForm(meta={"csrf": False})
        form.exam_sitting.choices = [("April 2027", "April 2027")]
        assert form.validate() is False
        assert form.exam_year.errors


def test_edit_form_populate_from_exam_date(app):
    with app.test_request_context():
        form = EditStudyPlanForm(meta={"csrf": False})
        form.populate_from_exam_date(date(2027, 9, 3))
        assert form.exam_day.data == 3
        assert form.exam_month.data == 9
        assert form.exam_year.data == 2027
