"""Explicit evidence ingress errors (AP-002D1).

Never silently repair malformed evidence. Callers must handle these explicitly.
"""

from __future__ import annotations


class EvidenceIngressError(Exception):
    """Base application error for AP-001 evidence ingress failures."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or self.__class__.__name__


class InvalidEvidenceBundle(EvidenceIngressError):  # noqa: N818
    """Bundle fails structural / contract validation (corrupted or malformed)."""


class UnsupportedEvidenceVersion(EvidenceIngressError):  # noqa: N818
    """Bundle packaging_version is not accepted by the ingress contract."""


class MissingObservationReference(EvidenceIngressError):  # noqa: N818
    """An evidence item lacks a valid observation reference."""


class IncompleteEvidenceBundle(EvidenceIngressError):  # noqa: N818
    """Required metadata, items, or identity fields are missing."""


class DuplicateEvidenceSubmission(EvidenceIngressError):  # noqa: N818
    """The same evidence bundle_id was already accepted by ingress."""
