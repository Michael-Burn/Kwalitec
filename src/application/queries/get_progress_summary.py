"""GetProgressSummary query — progress presentation section."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetProgressSummary:
    """Request a progress summary read model for one student."""

    student_id: str
