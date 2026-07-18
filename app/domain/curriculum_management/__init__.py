"""Version 2 Curriculum Management domain package.

Bounded context for curriculum asset and publication management.
No PDF storage, no parsing, no Flask / SQLAlchemy.

Prefer explicit imports such as
``app.domain.curriculum_management.subject.Subject``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "Approval",
    "ApprovalDecision",
    "AssetKind",
    "BlueprintAssignment",
    "CurriculumAsset",
    "CurriculumPackage",
    "Publication",
    "PublicationHistory",
    "PublicationHistoryEntry",
    "PublicationState",
    "PublicationTransitionEvent",
    "ReleaseNoteEntry",
    "ReleaseNotes",
    "Subject",
    "SubjectIdentifier",
    "SubjectMetadata",
    "SubjectVersion",
    "ValidationIssue",
    "ValidationIssueCode",
    "ValidationReport",
    "ValidationSeverity",
    "has_reached",
    "is_editable_publication_state",
    "is_terminal_publication_state",
    "next_publication_state",
    "pipeline_index",
    "resolve_asset_kind",
    "resolve_publication_state",
]

_EXPORT_MODULES = {
    "Approval": "app.domain.curriculum_management.approval",
    "ApprovalDecision": "app.domain.curriculum_management.approval",
    "AssetKind": "app.domain.curriculum_management.curriculum_asset",
    "BlueprintAssignment": "app.domain.curriculum_management.blueprint_assignment",
    "CurriculumAsset": "app.domain.curriculum_management.curriculum_asset",
    "CurriculumPackage": "app.domain.curriculum_management.curriculum_package",
    "Publication": "app.domain.curriculum_management.publication",
    "PublicationHistory": "app.domain.curriculum_management.publication_history",
    "PublicationHistoryEntry": (
        "app.domain.curriculum_management.publication_history"
    ),
    "PublicationState": "app.domain.curriculum_management.publication_state",
    "PublicationTransitionEvent": (
        "app.domain.curriculum_management.publication_state"
    ),
    "ReleaseNoteEntry": "app.domain.curriculum_management.release_notes",
    "ReleaseNotes": "app.domain.curriculum_management.release_notes",
    "Subject": "app.domain.curriculum_management.subject",
    "SubjectIdentifier": "app.domain.curriculum_management.subject_identifier",
    "SubjectMetadata": "app.domain.curriculum_management.subject_metadata",
    "SubjectVersion": "app.domain.curriculum_management.subject_version",
    "ValidationIssue": "app.domain.curriculum_management.validation_report",
    "ValidationIssueCode": "app.domain.curriculum_management.validation_report",
    "ValidationReport": "app.domain.curriculum_management.validation_report",
    "ValidationSeverity": "app.domain.curriculum_management.validation_report",
    "has_reached": "app.domain.curriculum_management.publication_state",
    "is_editable_publication_state": (
        "app.domain.curriculum_management.publication_state"
    ),
    "is_terminal_publication_state": (
        "app.domain.curriculum_management.publication_state"
    ),
    "next_publication_state": "app.domain.curriculum_management.publication_state",
    "pipeline_index": "app.domain.curriculum_management.publication_state",
    "resolve_asset_kind": "app.domain.curriculum_management.curriculum_asset",
    "resolve_publication_state": (
        "app.domain.curriculum_management.publication_state"
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
