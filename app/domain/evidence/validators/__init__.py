"""Validator package for the Evidence Validation Stage.

Contains the abstract validator contract, structural rule validators, and the
registry coordinator. Future specialised validators register with
``EvidenceValidator`` without modifying the coordinator.
"""

from __future__ import annotations

from app.domain.evidence.validators.base_validator import BaseValidator
from app.domain.evidence.validators.evidence_validator import EvidenceValidator
from app.domain.evidence.validators.structural import (
    CategoryPresentValidator,
    IdentifierPresentValidator,
    MetadataPresentValidator,
    OriginatingEventPresentValidator,
    PayloadPresentValidator,
    SourcePresentValidator,
    TimestampPresentValidator,
    default_structural_validators,
)

__all__ = [
    "BaseValidator",
    "CategoryPresentValidator",
    "EvidenceValidator",
    "IdentifierPresentValidator",
    "MetadataPresentValidator",
    "OriginatingEventPresentValidator",
    "PayloadPresentValidator",
    "SourcePresentValidator",
    "TimestampPresentValidator",
    "default_structural_validators",
]
