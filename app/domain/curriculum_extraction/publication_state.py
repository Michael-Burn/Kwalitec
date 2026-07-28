"""Draft publication state for Curriculum Knowledge Graph editions (EI-002)."""

from __future__ import annotations

from enum import StrEnum


class PublicationState(StrEnum):
    """Lifecycle of a CKG graph edition.

    EI-002 only writes ``draft``. Publish / approve transitions belong to a
    future Founder programme.
    """

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ValidationStatus(StrEnum):
    """Validation outcome recorded on a graph edition."""

    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
