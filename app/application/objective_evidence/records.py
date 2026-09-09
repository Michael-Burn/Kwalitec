"""Append-only Assessment Evidence record (OEA Phase 2).

Stores scored practice outcomes tagged with a real curriculum objective_id.
No mastery, EK, strength, or other knowledge-interpretation fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AssessmentEvidenceRecord:
    """One durable Assessment Evidence observation."""

    evidence_id: str
    student_id: str
    objective_id: str
    item_id: str
    package_id: str
    session_id: str
    response_type: str
    scored_correct: bool | None
    occurred_at: datetime
    source: str
    selected_misconception_tag: str = ""
