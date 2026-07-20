"""GetEvidenceHistory query."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetEvidenceHistory:
    """Load evidence history projection for a student."""

    student_id: str
