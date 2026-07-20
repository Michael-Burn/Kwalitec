"""GetDashboard query — compose the full dashboard read model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetDashboard:
    """Request a closed dashboard presentation for one student."""

    student_id: str
    episode_id: str | None = None
