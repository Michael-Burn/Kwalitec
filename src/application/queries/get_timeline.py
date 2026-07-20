"""GetTimeline query — timeline presentation section."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetTimeline:
    """Request a timeline read model for one student."""

    student_id: str
