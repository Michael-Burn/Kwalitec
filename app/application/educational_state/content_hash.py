"""Deterministic content hash for Educational State snapshots.

Hashing is performed by the Educational State authority so analytics never
receives Educational State payloads — only the resulting SHA-256 hex digest.

Canonical serialisation is used solely as a hashing input; it is never stored
in the analytics event store.

Accepts duck-typed ``EducationalStateSnapshot`` instances (attribute protocol)
to avoid import cycles with the package ``__init__``.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

# Stable schema tag for the hashed representation (not Twin/education math).
SNAPSHOT_STATE_VERSION = "1"


def compute_educational_state_content_hash(snapshot: Any) -> str:
    """Return SHA-256 hex of the canonical Educational State representation.

    Deterministic for identical snapshot field values. Does not invent
    educational scores — hashes assembled port payloads as-is.
    """
    canonical = _canonical_bytes(snapshot)
    return hashlib.sha256(canonical).hexdigest()


def _canonical_bytes(snapshot: Any) -> bytes:
    document: dict[str, Any] = {
        "state_version": SNAPSHOT_STATE_VERSION,
        "student_id": snapshot.student_id,
        "learner_summary": snapshot.learner_summary,
        "readiness_summary": snapshot.readiness_summary,
        "recommendation": snapshot.recommendation,
        "todays_session": snapshot.todays_session,
        "journey_progress": snapshot.journey_progress,
        "journey_topics": list(snapshot.journey_topics),
        "learning_insights": snapshot.learning_insights,
        "revision_options": list(snapshot.revision_options),
        "twin_available": snapshot.twin_available,
        "adaptive_available": snapshot.adaptive_available,
        "mission_available": snapshot.mission_available,
        "journey_available": snapshot.journey_available,
    }
    text = json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        default=_json_default,
    )
    return text.encode("utf-8")


def _json_default(value: Any) -> Any:
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, set):
        return sorted(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serialisable")
