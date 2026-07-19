"""Student-facing terminology guards for the presentation layer."""

from __future__ import annotations

import pytest

from app.presentation.student.view_models import FORBIDDEN_LEARNER_TERMS
from tests.presentation.student.helpers import FORBIDDEN_TERMS, STUDENT_ROUTES


def test_forbidden_term_lists_align():
    for term in FORBIDDEN_TERMS:
        assert term in FORBIDDEN_LEARNER_TERMS


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_student_vocabulary_present(student_client, endpoint, path):
    html = student_client.get(path).get_data(as_text=True)
    # At least one student-facing concept appears somewhere in the shell.
    assert any(
        word in html
        for word in ("Home", "Journey", "Revision", "History", "Profile", "Kwalitec")
    )


@pytest.mark.parametrize("term", FORBIDDEN_LEARNER_TERMS)
def test_design_system_documents_forbidden_terms(term):
    from pathlib import Path

    path = Path("knowledge/version2/DESIGN_SYSTEM.md")
    doc = path.read_text(encoding="utf-8").lower()
    # Design system should mention the constraint (not use the engines as UI copy).
    assert "digital twin" in doc or "adaptive decision" in doc
