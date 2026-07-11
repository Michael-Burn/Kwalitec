"""Public update strategy contract for the Twin Update Pipeline.

Re-exports the abstract strategy interface defined under ``strategies/``.
Specialised educational strategies are implemented in later capabilities.
"""

from __future__ import annotations

from app.domain.twin.strategies.base_strategy import BaseUpdateStrategy

# Public alias matching ubiquitous language ("Update Strategy").
UpdateStrategy = BaseUpdateStrategy

__all__ = [
    "BaseUpdateStrategy",
    "UpdateStrategy",
]
