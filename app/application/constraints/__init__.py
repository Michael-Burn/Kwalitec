"""Application Constraints Integration adapters.

Constructs immutable domain Constraints from product context without owning
educational judgement, Decision selection, or Mission optimisation.
"""

from __future__ import annotations

from app.application.constraints.constraint_builder import (
    ConstraintBuilder,
    ConstraintBuildError,
    ConstraintProductConfiguration,
    ConstraintProductContext,
    InvalidConstraintInputError,
    MissingIdentityError,
)

__all__ = [
    "ConstraintBuilder",
    "ConstraintBuildError",
    "ConstraintProductConfiguration",
    "ConstraintProductContext",
    "InvalidConstraintInputError",
    "MissingIdentityError",
]
