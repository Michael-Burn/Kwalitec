"""Learner Lifecycle HTTP/runtime hooks (VP-001).

Thin adapters that invoke LP-001 orchestration from enrolment and session
paths. No educational reasoning lives here.
"""

from __future__ import annotations

from app.infrastructure.adapters.learner_lifecycle.enrolment_hook import (
    onboard_after_enrolment,
    resolve_published_edition_id,
)
from app.infrastructure.adapters.learner_lifecycle.evidence_hook import (
    record_session_evidence,
)

__all__ = [
    "onboard_after_enrolment",
    "record_session_evidence",
    "resolve_published_edition_id",
]
