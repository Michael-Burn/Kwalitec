"""Prove ContentDraft rows cannot reach the student package resolution path."""

from __future__ import annotations

import ast
from pathlib import Path

from app.application.content_lifecycle import (
    STATUS_APPROVED,
    STATUS_READY_FOR_REVIEW,
    ContentDraftService,
)
from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    find_package_by_id,
    reset_educational_package_cache,
)
from app.extensions import db

# Student-facing package resolution modules must never import draft storage.
_STUDENT_PACKAGE_MODULES = (
    Path("app/application/educational_packages/loader.py"),
    Path("app/application/educational_packages/selection.py"),
    Path("app/application/educational_packages/substance.py"),
    Path("app/application/educational_packages/guard.py"),
    Path("app/application/learning_session/substance_planner.py"),
    Path("app/application/student_runtime/coordinator.py"),
)

_FORBIDDEN_IMPORT_PREFIXES = (
    "app.models.content_draft",
    "app.application.content_lifecycle",
)


def test_student_package_modules_do_not_import_content_draft() -> None:
    for path in _STUDENT_PACKAGE_MODULES:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for name in names:
                for prefix in _FORBIDDEN_IMPORT_PREFIXES:
                    assert not name.startswith(prefix), (
                        f"{path} must not import {name} "
                        f"(draft store is founder-only)."
                    )


def test_approved_draft_in_db_is_invisible_to_package_loader(app, ctx):
    """Even an approved DB draft with a live-looking package_id is not served."""
    reset_educational_package_cache()
    ghost_package_id = "CS1-CONTENT-DRAFT-GHOST-NEVER-LIVE"

    # Confirm the ghost id is not already a live package.
    assert find_package_by_id(ghost_package_id) is None

    service = ContentDraftService()
    draft = service.create_draft(
        subject_id="CS1",
        payload={
            "package_id": ghost_package_id,
            "package_version": "1.0.0",
            "publication_version": "1",
            "status": "publication_approved",
            "subject_id": "CS1",
            "topic_code": "9.9.9",
            "topic_title": "Ghost draft topic",
            "knowledge_checks": [],
        },
        created_by="founder",
        live_package_id=ghost_package_id,
    )
    service.transition_status(draft, STATUS_READY_FOR_REVIEW)
    service.transition_status(draft, STATUS_APPROVED, approved_by="reviewer")
    db.session.commit()

    reset_educational_package_cache()
    assert find_package_by_id(ghost_package_id) is None

    approved_ids = {
        p.package_id for p in EducationalPackageLoader().all_approved()
    }
    assert ghost_package_id not in approved_ids
