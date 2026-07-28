"""Evidence type and source catalogues (EI-005).

Types are stored as strings so additional catalogue members can be added in
code without Alembic schema redesign. Known initial types are enumerated here.
"""

from __future__ import annotations

import re
from enum import StrEnum

_SNAKE_CASE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")


class EvidenceType(StrEnum):
    """Initial Learning Evidence type catalogue.

    Values are stable snake_case identifiers. Extending the catalogue is a
    code change only — the persistence column remains a free-form string.
    """

    READING_COMPLETED = "reading_completed"
    WORKED_EXAMPLE_COMPLETED = "worked_example_completed"
    PRACTICE_ATTEMPT = "practice_attempt"
    ASSESSMENT_RESULT = "assessment_result"
    STUDY_SESSION = "study_session"
    REVISION_SESSION = "revision_session"
    MANUAL_FOUNDER_OVERRIDE = "manual_founder_override"


class EvidenceSource(StrEnum):
    """Where an evidence observation originated."""

    STUDENT_RUNTIME = "student_runtime"
    SESSION_RUNTIME = "session_runtime"
    FOUNDER_OVERRIDE = "founder_override"
    SYSTEM_IMPORT = "system_import"
    MANUAL_ENTRY = "manual_entry"


def normalise_evidence_type(value: str | EvidenceType) -> str:
    """Return a stripped snake_case evidence type string."""
    if isinstance(value, EvidenceType):
        return value.value
    return (value or "").strip().lower()


def is_known_evidence_type(value: str | EvidenceType) -> bool:
    """True when value matches the initial EI-005 catalogue."""
    normalised = normalise_evidence_type(value)
    return normalised in {member.value for member in EvidenceType}


def is_extensible_type_token(value: str) -> bool:
    """True when value is a non-empty snake_case token suitable for storage."""
    return bool(_SNAKE_CASE.fullmatch((value or "").strip().lower()))
