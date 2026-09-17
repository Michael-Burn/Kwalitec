"""Canonical curriculum identity layer (application package)."""

from app.application.curriculum_identity.constants import (
    UNKNOWN_CURRICULUM_IDENTITY,
)
from app.application.curriculum_identity.service import (
    CurriculumIdentityService,
    ResolvedCurriculumIdentity,
)

__all__ = [
    "CurriculumIdentityService",
    "ResolvedCurriculumIdentity",
    "UNKNOWN_CURRICULUM_IDENTITY",
]
