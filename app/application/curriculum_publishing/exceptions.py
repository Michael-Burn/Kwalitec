"""Exceptions for the Founder curriculum publishing workflow."""

from __future__ import annotations

from app.domain.curriculum_publishing.invariants import PublicationInvariantError


class CurriculumPublishingError(Exception):
    """Base error for curriculum publishing application services."""


class EditionNotFoundError(CurriculumPublishingError):
    """Requested graph edition does not exist."""


class NodeNotFoundError(CurriculumPublishingError):
    """Requested curriculum node does not exist in the edition."""


class PublishingGateError(CurriculumPublishingError):
    """Publication or editorial gate failed."""

    def __init__(self, message: str, *, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


def gate_from_invariant(exc: PublicationInvariantError) -> PublishingGateError:
    return PublishingGateError(str(exc), cause=exc)
