"""Curriculum Publishing (EI-003) — Founder educational governance domain.

Transforms validated Draft Curriculum Knowledge Graph editions into
Founder-approved Published editions with auditability and edition history.

Pure domain only: no Flask, SQLAlchemy, Twin, missions, or student UI.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "AuditEventType",
    "EditorialAction",
    "NodeReviewStatus",
    "PublicationInvariant",
    "PublicationInvariantError",
    "PublicationState",
    "ReviewStatus",
    "ValidationStatus",
    "assert_can_approve_edition",
    "assert_can_publish",
    "assert_draft_only_editorial",
]

_EXPORT_MODULES = {
    "PublicationState": "app.domain.curriculum_extraction.publication_state",
    "ValidationStatus": "app.domain.curriculum_extraction.publication_state",
    "NodeReviewStatus": "app.domain.curriculum_publishing.review_state",
    "ReviewStatus": "app.domain.curriculum_publishing.review_state",
    "EditorialAction": "app.domain.curriculum_publishing.editorial_action",
    "AuditEventType": "app.domain.curriculum_publishing.audit",
    "PublicationInvariant": "app.domain.curriculum_publishing.invariants",
    "PublicationInvariantError": "app.domain.curriculum_publishing.invariants",
    "assert_can_approve_edition": "app.domain.curriculum_publishing.invariants",
    "assert_can_publish": "app.domain.curriculum_publishing.invariants",
    "assert_draft_only_editorial": "app.domain.curriculum_publishing.invariants",
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
