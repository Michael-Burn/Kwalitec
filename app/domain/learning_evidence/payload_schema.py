"""Payload schema checks for Learning Evidence metadata (EI-005).

Schemas are observational only — they never encode mastery, confidence, or
recommendation intent. Unknown extensible types accept any JSON object.
"""

from __future__ import annotations

from typing import Any

from app.domain.learning_evidence.evidence_type import (
    EvidenceType,
    normalise_evidence_type,
)
from app.domain.learning_evidence.invariants import (
    EvidenceInvariant,
    EvidenceInvariantError,
)

# Required metadata keys per known catalogue type (empty = any object ok).
_REQUIRED_KEYS: dict[str, frozenset[str]] = {
    EvidenceType.READING_COMPLETED.value: frozenset(),
    EvidenceType.WORKED_EXAMPLE_COMPLETED.value: frozenset(),
    EvidenceType.PRACTICE_ATTEMPT.value: frozenset(),
    EvidenceType.ASSESSMENT_RESULT.value: frozenset(),
    EvidenceType.STUDY_SESSION.value: frozenset(),
    EvidenceType.REVISION_SESSION.value: frozenset(),
    EvidenceType.MANUAL_FOUNDER_OVERRIDE.value: frozenset({"reason"}),
}

# Optional keys with simple type expectations (advisory for known types).
_OPTIONAL_TYPED: dict[str, dict[str, type | tuple[type, ...]]] = {
    EvidenceType.READING_COMPLETED.value: {
        "duration_minutes": (int, float),
        "reference_id": str,
    },
    EvidenceType.WORKED_EXAMPLE_COMPLETED.value: {
        "duration_minutes": (int, float),
        "example_id": str,
    },
    EvidenceType.PRACTICE_ATTEMPT.value: {
        "correct": bool,
        "duration_minutes": (int, float),
        "item_id": str,
    },
    EvidenceType.ASSESSMENT_RESULT.value: {
        "score": (int, float),
        "passed": bool,
        "assessment_id": str,
    },
    EvidenceType.STUDY_SESSION.value: {
        "duration_minutes": (int, float),
        "session_id": str,
    },
    EvidenceType.REVISION_SESSION.value: {
        "duration_minutes": (int, float),
        "session_id": str,
    },
    EvidenceType.MANUAL_FOUNDER_OVERRIDE.value: {
        "reason": str,
        "actor": str,
        "note": str,
    },
}


def assert_payload_schema(
    evidence_type: str | EvidenceType,
    metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Validate and return a normalised metadata payload.

    Raises:
        EvidenceInvariantError: When payload is not an object or fails schema.
    """
    if metadata is None:
        payload: dict[str, Any] = {}
    elif not isinstance(metadata, dict):
        raise EvidenceInvariantError(
            EvidenceInvariant.PAYLOAD_SCHEMA,
            f"metadata must be a JSON object, got {type(metadata).__name__}",
        )
    else:
        payload = dict(metadata)

    normalised = normalise_evidence_type(evidence_type)
    required = _REQUIRED_KEYS.get(normalised)
    if required is not None:
        missing = sorted(key for key in required if key not in payload)
        if missing:
            raise EvidenceInvariantError(
                EvidenceInvariant.PAYLOAD_SCHEMA,
                f"metadata missing required keys for {normalised}: {missing}",
            )
        typed = _OPTIONAL_TYPED.get(normalised, {})
        for key, expected in typed.items():
            if key not in payload:
                continue
            if not isinstance(payload[key], expected):
                raise EvidenceInvariantError(
                    EvidenceInvariant.PAYLOAD_SCHEMA,
                    f"metadata[{key!r}] must be {expected}, "
                    f"got {type(payload[key]).__name__}",
                )
        if normalised == EvidenceType.MANUAL_FOUNDER_OVERRIDE.value:
            reason = payload.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                raise EvidenceInvariantError(
                    EvidenceInvariant.PAYLOAD_SCHEMA,
                    "manual_founder_override requires a non-empty reason string",
                )

    return payload
