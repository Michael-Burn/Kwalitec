"""DTO package for Curriculum Management."""

from __future__ import annotations

from typing import Any

__all__ = [
    "ApprovalSnapshot",
    "PreviewSnapshot",
    "PublicationSnapshot",
    "ReleaseSnapshot",
    "SubjectSnapshot",
    "SubjectSummary",
    "ValidationIssueSnapshot",
    "ValidationSnapshot",
    "VersionSnapshot",
]

_EXPORT_MODULES = {
    "ApprovalSnapshot": (
        "app.application.curriculum_management.dto.approval_snapshot"
    ),
    "PreviewSnapshot": (
        "app.application.curriculum_management.dto.preview_snapshot"
    ),
    "PublicationSnapshot": (
        "app.application.curriculum_management.dto.publication_snapshot"
    ),
    "ReleaseSnapshot": (
        "app.application.curriculum_management.dto.release_snapshot"
    ),
    "SubjectSnapshot": (
        "app.application.curriculum_management.dto.subject_snapshot"
    ),
    "SubjectSummary": (
        "app.application.curriculum_management.dto.subject_summary"
    ),
    "ValidationIssueSnapshot": (
        "app.application.curriculum_management.dto.validation_snapshot"
    ),
    "ValidationSnapshot": (
        "app.application.curriculum_management.dto.validation_snapshot"
    ),
    "VersionSnapshot": (
        "app.application.curriculum_management.dto.version_snapshot"
    ),
}


def __getattr__(name: str) -> Any:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
