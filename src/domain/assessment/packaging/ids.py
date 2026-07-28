"""Default identity factory for evidence packaging builders."""

from __future__ import annotations

from collections.abc import Callable
from itertools import count


def sequential_id_factory(start: int = 1) -> Callable[[str], str]:
    """Return a deterministic ``prefix-N`` id factory."""
    counter = count(start)

    def _next(prefix: str) -> str:
        return f"{prefix}-{next(counter)}"

    return _next
