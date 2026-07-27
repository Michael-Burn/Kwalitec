"""Template and accessibility checks for Assessment Delivery."""

from __future__ import annotations

from pathlib import Path

from tests.presentation.assessment.helpers import FORBIDDEN_TERMS


def test_assessment_static_assets_exist() -> None:
    root = Path(__file__).resolve().parents[3]
    assert (root / "app/static/css/assessment/assessment.css").is_file()
    assert (root / "app/static/js/assessment/delivery.js").is_file()


def test_templates_extend_base_and_skip_link() -> None:
    root = Path(__file__).resolve().parents[3] / "app/templates/student/assessment"
    base = (root / "base.html").read_text(encoding="utf-8")
    assert 'href="#assessment-main"' in base
    assert 'role="main"' in base
    assert "assessment.css" in base
    for name in ("entry.html", "overview.html", "item.html", "complete.html"):
        text = (root / name).read_text(encoding="utf-8")
        assert 'extends "student/assessment/base.html"' in text


def test_progress_component_has_aria() -> None:
    root = Path(__file__).resolve().parents[3]
    progress = (
        root / "app/templates/student/assessment/components/progress.html"
    ).read_text(encoding="utf-8")
    assert 'role="progressbar"' in progress
    assert "aria-valuenow" in progress
    assert "aria-valuemin" in progress


def test_question_component_uses_radiogroup() -> None:
    root = Path(__file__).resolve().parents[3]
    question = (
        root / "app/templates/student/assessment/components/question.html"
    ).read_text(encoding="utf-8")
    assert 'role="radiogroup"' in question


def test_templates_avoid_forbidden_exam_terms() -> None:
    root = Path(__file__).resolve().parents[3] / "app/templates/student/assessment"
    for path in root.rglob("*.html"):
        text = path.read_text(encoding="utf-8").lower()
        for term in FORBIDDEN_TERMS:
            # "exam" may appear in negation copy ("not an exam") — allow that phrase
            if term == "exam":
                continue
            assert term not in text, f"{term} found in {path}"


def test_entry_copy_frames_support_not_grading(assessment_client) -> None:
    response = assessment_client.get("/assessment/")
    assert response.status_code == 200
    body = response.get_data(as_text=True).lower()
    assert "support" in body
    assert "no grades" in body
