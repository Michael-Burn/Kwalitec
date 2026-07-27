"""Default composition factory for Twin rollback drills.

Kept outside ``digital_twin/*.py`` so Twin packages stay free of Experience
adapter import strings (T4 boundary).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


def default_composition_factory(**kwargs: Any) -> tuple[Any, Any]:
    """Build production Experience composition for observational Twin drills."""
    from app.infrastructure.adapters.student_experience.composition import (
        build_production_experience,
    )

    return build_production_experience(**kwargs)


CompositionFactory = Callable[..., tuple[Any, Any]]
