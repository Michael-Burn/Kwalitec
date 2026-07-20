"""Messaging and copy consistency for Founder Studio UX."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.presentation.curriculum_studio import routes as studio_routes
from app.presentation.curriculum_studio.view_models import (
    FLASH_SUCCESS,
    FLASH_WARNING,
)

ROUTES_PATH = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "presentation"
    / "curriculum_studio"
    / "routes.py"
)


def test_routes_use_central_flash_constants():
    source = ROUTES_PATH.read_text(encoding="utf-8")
    assert "FLASH_SUCCESS" in source
    assert "FLASH_WARNING" in source
    assert 'flash("Validation complete.' not in source
    assert 'flash("Curriculum published."' not in source


def test_validation_success_message():
    assert FLASH_SUCCESS["validation_ok"] == (
        "We've completed validation successfully."
    )


def test_publish_success_message():
    assert FLASH_SUCCESS["published"] == (
        "We've published your curriculum successfully."
    )


@pytest.mark.parametrize("message", list(FLASH_SUCCESS.values())[:4])
def test_flash_success_messages_end_with_period(message):
    assert message.endswith(".")
    assert not message.endswith("..")


def test_flash_warning_messages_guide_recovery():
    for message in FLASH_WARNING.values():
        lowered = message.lower()
        assert message.endswith(".")
        assert "try again" in lowered or "check" in lowered

def test_no_execute_publish_in_presentation_package():
    root = (
        Path(__file__).resolve().parents[3]
        / "app"
        / "presentation"
        / "curriculum_studio"
    )
    for path in root.rglob("*.py"):
        lowered = path.read_text(encoding="utf-8").lower()
        assert "execute publish" not in lowered


def test_routes_module_imports_cleanly():
    assert studio_routes.index.__name__ == "index"
    assert callable(studio_routes.publish)


def test_routes_do_not_import_domain_engines():
    tree = ast.parse(ROUTES_PATH.read_text(encoding="utf-8"))
    forbidden = (
        "app.domain.student_twin",
        "app.application.adaptive_learning",
        "app.application.learning_session",
    )
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert node.module not in forbidden
