"""ARP-004 cross-surface product language matrix."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.presentation.curriculum_studio.view_models import (
    FLASH_SUCCESS as STUDIO_SUCCESS,
)
from app.presentation.curriculum_studio.view_models import (
    FLASH_WARNING as STUDIO_WARNING,
)
from app.presentation.product_language import (
    APPROVED_TERMS,
    FOUNDER_STUDIO_CTAS,
    REJECTED_SYNONYMS,
    STUDENT_PRIMARY_CTAS,
)
from app.presentation.session.messages import (
    FLASH_SUCCESS as SESSION_SUCCESS,
)
from app.presentation.session.messages import (
    FLASH_WARNING as SESSION_WARNING,
)
from app.presentation.student.view_models import FORBIDDEN_LEARNER_TERMS

GUIDE = Path("knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md")


@pytest.mark.parametrize("term", APPROVED_TERMS)
def test_approved_terms_documented(term):
    assert term in GUIDE.read_text(encoding="utf-8")


@pytest.mark.parametrize("cta", STUDENT_PRIMARY_CTAS)
def test_student_ctas_documented(cta):
    assert cta in GUIDE.read_text(encoding="utf-8")


@pytest.mark.parametrize("cta", FOUNDER_STUDIO_CTAS)
def test_founder_ctas_documented(cta):
    assert cta in GUIDE.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "message",
    list(SESSION_SUCCESS.values()) + list(STUDIO_SUCCESS.values()),
)
def test_all_success_flashes_end_with_period(message):
    assert message.endswith(".")
    assert not message.endswith("..")


@pytest.mark.parametrize(
    "message",
    list(SESSION_WARNING.values()) + list(STUDIO_WARNING.values()),
)
def test_all_warning_flashes_end_with_period(message):
    assert message.endswith(".")


@pytest.mark.parametrize(
    "message",
    list(SESSION_WARNING.values()) + list(STUDIO_WARNING.values()),
)
def test_all_warning_flashes_offer_recovery(message):
    lowered = message.lower()
    assert any(
        token in lowered
        for token in (
            "try again",
            "return home",
            "return to",
            "check",
            "enter an answer",
            "assign",
            "complete",
        )
    )


@pytest.mark.parametrize("term", FORBIDDEN_LEARNER_TERMS)
def test_forbidden_learner_terms_still_guarded(term):
    assert term
    assert term == term.lower()


def test_rejected_synonyms_include_session_variants():
    assert "study session" in REJECTED_SYNONYMS
    assert "learning session" in REJECTED_SYNONYMS


def test_no_execute_in_central_flash_tables():
    blob = " ".join(
        list(SESSION_SUCCESS.values())
        + list(SESSION_WARNING.values())
        + list(STUDIO_SUCCESS.values())
        + list(STUDIO_WARNING.values())
    ).lower()
    assert "execute" not in blob
    assert "launch" not in blob
    assert "proceed" not in blob


def test_readme_indexes_product_language_guide():
    readme = Path("knowledge/version2/README.md").read_text(encoding="utf-8")
    assert "PRODUCT_LANGUAGE_GUIDE.md" in readme


def test_design_system_still_references_forbidden_engines():
    path = Path("knowledge/version2/DESIGN_SYSTEM.md")
    doc = path.read_text(encoding="utf-8").lower()
    assert "digital twin" in doc or "adaptive decision" in doc


@pytest.mark.parametrize(
    "path",
    (
        "app/presentation/session/messages.py",
        "app/presentation/curriculum_studio/view_models.py",
        "app/presentation/product_language.py",
        "knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md",
    ),
)
def test_language_artifacts_exist(path):
    assert Path(path).is_file()
